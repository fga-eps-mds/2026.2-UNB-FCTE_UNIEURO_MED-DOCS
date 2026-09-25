import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime, timezone

from src.config import (
    ORGANIZATION,
    PROJECT_PREFIX,
    INITIAL_PLANNED_SPRINTS_R1,
    INITIAL_PLANNED_POINTS_PRP0,
    WEEKLY_SPRINT_BUDGET_BRL,
    ANALYSIS_NOTES_DIR,
    THEME_COLORS,
    REPOS_CONFIG
)
from src.theme import apply_custom_theme, render_kpi, get_plotly_layout
from src.data_layer import get_zenhub_sprints_data, get_risks_data, get_github_runs_data, get_sonar_metrics_data
from src.metrics import compute_agile_evm_metrics, process_risks_summary

RATING_LETTERS = {1.0: "A", 2.0: "B", 3.0: "C", 4.0: "D", 5.0: "E"}


def rating_to_letter(value) -> str:
    """Converte a nota numérica do SonarCloud (1.0-5.0) para a letra A-E."""
    try:
        return RATING_LETTERS.get(round(float(value)), "N/A")
    except (TypeError, ValueError):
        return "N/A"


def filter_started_sprints(sprints: list) -> list:
    """Remove sprints cujo início ainda não chegou.

    O Zenhub devolve todas as sprints recorrentes já agendadas no workspace,
    inclusive as que só começam daqui a meses. Sem esse filtro o burnup/velocity
    esticaria até essas datas futuras. Sprints sem `start_at` (dado mock antigo)
    são mantidas, já que nesse caso não há como avaliar se já começaram.
    """
    hoje = datetime.now(timezone.utc)
    resultado = []
    for s in sprints:
        start_at = s.get("start_at")
        if not start_at:
            resultado.append(s)
            continue
        try:
            inicio = datetime.fromisoformat(start_at.replace("Z", "+00:00"))
        except (TypeError, ValueError):
            resultado.append(s)
            continue
        if inicio <= hoje:
            resultado.append(s)
    return resultado

PLOTLY_CONFIG = {"displaylogo": False, "responsive": True}


def render_header():
    """Renderiza o cabeçalho executivo do dashboard."""
    st.markdown(f"""
    <div class="hero-header">
        <div class="hero-title">Painel Analítico e Decisório — {PROJECT_PREFIX}</div>
        <div class="hero-sub">Engenharia de Produto de Software · Universidade de Brasília (UnB / FGA) · 2026.2</div>
        <div class="hero-badge">Release 1 (DA-R1) · Governança Ágil, EVM e Riscos</div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Barra lateral com metadados do projeto e filtros dinâmicos."""
    st.sidebar.markdown("### Governança do Projeto")
    st.sidebar.info(f"**Organização:** `{ORGANIZATION}`\n\n**Projeto:** `{PROJECT_PREFIX}`")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Parâmetros de Simulação (EVM)")
    
    sim_prp0 = st.sidebar.number_input(
        "Escopo Inicial (PRP₀ em SP):",
        min_value=10.0,
        max_value=300.0,
        value=INITIAL_PLANNED_POINTS_PRP0,
        step=5.0
    )
    sim_ps = st.sidebar.number_input(
        "Sprints Planejadas (PS):",
        min_value=1,
        max_value=15,
        value=INITIAL_PLANNED_SPRINTS_R1,
        step=1
    )
    sim_budget = st.sidebar.number_input(
        "Custo Médio / Sprint (R$):",
        min_value=500.0,
        max_value=20000.0,
        value=WEEKLY_SPRINT_BUDGET_BRL,
        step=200.0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Repositórios Integrados:\n- `-DOCS` (Documentação e Analytics)\n- `-IA` (Módulo de Inteligência Artificial)\n- `-APP` (Aplicação Mobile)")
    
    return sim_prp0, sim_ps, sim_budget


def render_mock_alert(metric_name: str, file_name: str):
    """Exibe alerta visual informativo quando os dados ainda são mockados."""
    st.warning(
        f"Aviso: Exibindo dados simulados (mock) para **{metric_name}**. "
        f"O arquivo `{file_name}` ainda não foi gerado pela esteira de CI/CD em `analytics-raw-data/`."
    )


def render_evm_tab(evm: dict, is_mock: bool):
    """Renderiza a aba do Agile EVM, Burnup e Velocity."""
    if is_mock:
        render_mock_alert("Sprints e Agile EVM", "zenhub_analytics.json")

    st.markdown("### Desempenho de Prazo e Custos (Agile EVM)")
    
    row1_c1, row1_c2, row1_c3 = st.columns(3)
    with row1_c1:
        render_kpi("BAC (Orçamento Total)", f"R$ {evm['bac']:,.2f}", "Escopo Inicial Valorizado", THEME_COLORS["primary"])
    with row1_c2:
        render_kpi("EV Acumulado", f"R$ {evm['current_ev']:,.2f}", "Valor de Negócio Entregue", THEME_COLORS["primary"])
    with row1_c3:
        render_kpi("Média Velocity", f"{evm['avg_velocity']} SP", "Média entregue por sprint", THEME_COLORS["accent"])

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        spi_color = THEME_COLORS["secondary"] if evm['current_spi'] >= 1.0 else THEME_COLORS["danger"]
        render_kpi("SPI (Eficiência de Cronograma)", f"{evm['current_spi']:.2f}", "Índice de prazo (≥ 1.0 no cronograma)", spi_color)
    with row2_c2:
        cpi_color = THEME_COLORS["secondary"] if evm['current_cpi'] >= 1.0 else THEME_COLORS["danger"]
        render_kpi("CPI (Eficiência de Custo)", f"{evm['current_cpi']:.2f}", "Índice de custo (≥ 1.0 no orçamento)", cpi_color)

    st.markdown("<br>", unsafe_allow_html=True)

    g1, g2 = st.columns([1.35, 1.0])
    with g1:
        fig_burnup = go.Figure()
        fig_burnup.add_trace(go.Scatter(
            x=evm["burnup_labels"],
            y=evm["burnup_pv"],
            name="PV (Planejado)",
            mode="lines+markers",
            line=dict(color="#94A3B8", width=2.5, dash="dash")
        ))
        fig_burnup.add_trace(go.Scatter(
            x=evm["burnup_labels"],
            y=evm["burnup_ev"],
            name="EV (Realizado)",
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(56, 189, 248, 0.15)",
            line=dict(color="#38BDF8", width=3)
        ))
        fig_burnup.update_layout(get_plotly_layout("Evolução do Valor Agregado — Burnup (PV × EV)", height=380))
        st.plotly_chart(fig_burnup, use_container_width=True, config=PLOTLY_CONFIG)

    with g2:
        fig_vel = go.Figure(go.Bar(
            x=evm["velocity_labels"],
            y=evm["velocity_series"],
            marker=dict(
                color=["#38BDF8" if i % 2 == 0 else "#0284C7" for i in range(len(evm["velocity_series"]))],
                line=dict(color="rgba(255, 255, 255, 0.3)", width=1)
            ),
            text=[f"{v} SP" for v in evm["velocity_series"]],
            textposition="auto"
        ))
        fig_vel.update_layout(get_plotly_layout("Histórico de Velocity (Story Points)", height=380))
        st.plotly_chart(fig_vel, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("#### Índices de Desempenho SPI e CPI")
    fig_indices = go.Figure()
    fig_indices.add_trace(go.Scatter(
        x=evm["burnup_labels"][1:len(evm["spi_series"])],
        y=evm["spi_series"][1:],
        name="SPI (Cronograma)",
        mode="lines+markers",
        line=dict(color="#FBBF24", width=2.5)
    ))
    fig_indices.add_trace(go.Scatter(
        x=evm["burnup_labels"][1:len(evm["cpi_series"])],
        y=evm["cpi_series"][1:],
        name="CPI (Custo)",
        mode="lines+markers",
        line=dict(color="#34D399", width=2.5)
    ))
    fig_indices.add_hline(y=1.0, line_dash="dot", line_color="#94A3B8", annotation_text="Meta (1.0)")
    fig_indices.update_layout(get_plotly_layout("Evolução Histórica do SPI e CPI por Sprint", height=300))
    st.plotly_chart(fig_indices, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("### Tabela de Auditoria e Rastreabilidade do Agile EVM")
    st.dataframe(evm["audit_df"], use_container_width=True, hide_index=True)
    
    csv_data = evm["audit_df"].to_csv(index=False, sep=";", encoding="utf-8-sig")
    st.download_button(
        label="Exportar Tabela de Auditoria (CSV)",
        data=csv_data,
        file_name=f"auditoria_evm_{PROJECT_PREFIX.lower()}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.markdown("### Parecer Técnico e Análise da Sprint")
    os.makedirs(ANALYSIS_NOTES_DIR, exist_ok=True)
    
    hoje_str = datetime.now().strftime("%Y-%m-%d")
    arquivo_nota = os.path.join(ANALYSIS_NOTES_DIR, f"{hoje_str}_analise_gerencial.txt")
    
    conteudo_salvo = ""
    if os.path.exists(arquivo_nota):
        with open(arquivo_nota, "r", encoding="utf-8") as f:
            conteudo_salvo = f.read()

    parecer = st.text_area(
        "Registro de justificativas técnicas para variações de escopo, velocity ou cronograma:",
        value=conteudo_salvo,
        placeholder="Ex: Na Sprint 2, a equipe ampliou a produtividade com a entrega do módulo de autenticação...",
        height=100
    )
    if st.button("Salvar Parecer Localmente"):
        with open(arquivo_nota, "w", encoding="utf-8") as f:
            f.write(parecer)
        st.success(f"Parecer registrado em: {os.path.basename(arquivo_nota)}")


def render_risks_tab(risks_raw: list, is_mock: bool):
    """Renderiza a aba de Gestão de Riscos."""
    if is_mock:
        render_mock_alert("Matriz de Riscos", "riscos_analytics.json")

    st.markdown("### Matriz de Exposição e Governança de Riscos")
    
    df_risks = process_risks_summary(risks_raw)
    
    r1, r2, r3, r4 = st.columns(4)
    total_r = len(df_risks)
    crit_r = len(df_risks[df_risks["Nível"] == "Crítico"])
    alto_r = len(df_risks[df_risks["Nível"] == "Alto"])
    media_sev = round(df_risks["Severidade (P×I)"].mean(), 1) if total_r > 0 else 0

    with r1:
        render_kpi("Total de Riscos", str(total_r), "Mapeados no projeto", THEME_COLORS["primary"])
    with r2:
        render_kpi("Riscos Críticos", str(crit_r), "Severidade ≥ 16", THEME_COLORS["danger"] if crit_r > 0 else THEME_COLORS["secondary"])
    with r3:
        render_kpi("Riscos Altos", str(alto_r), "Severidade 10 a 15", THEME_COLORS["warning"])
    with r4:
        render_kpi("Severidade Média", str(media_sev), "Média ponderada (P×I)", THEME_COLORS["accent"])

    st.markdown("<br>", unsafe_allow_html=True)

    col_matriz, col_cat = st.columns([1.35, 1.0])
    
    with col_matriz:
        z_scores = [
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],
            [3, 6, 9, 12, 15],
            [4, 8, 12, 16, 20],
            [5, 10, 15, 20, 25]
        ]
        fig_heat = go.Figure(data=go.Heatmap(
            z=z_scores,
            x=["1 (Muito Baixo)", "2 (Baixo)", "3 (Médio)", "4 (Alto)", "5 (Crítico)"],
            y=["1 (Muito Baixa)", "2 (Baixa)", "3 (Média)", "4 (Alta)", "5 (Muito Alta)"],
            colorscale=[
                [0.0, "rgba(52, 211, 153, 0.35)"],
                [0.25, "rgba(251, 191, 36, 0.45)"],
                [0.55, "rgba(249, 115, 22, 0.55)"],
                [1.0, "rgba(239, 68, 68, 0.65)"]
            ],
            showscale=False
        ))
        
        for r in risks_raw:
            fig_heat.add_annotation(
                x=r["impacto"] - 1,
                y=r["probabilidade"] - 1,
                text=f"<b>{r['id']}</b>",
                showarrow=False,
                font=dict(color="#FFFFFF", size=12),
                bgcolor="rgba(15, 23, 42, 0.9)",
                bordercolor="#38BDF8",
                borderwidth=1.5,
                borderpad=4
            )

        layout_heat = get_plotly_layout("Matriz de Probabilidade × Impacto (5×5)", height=380)
        layout_heat["xaxis"]["title"] = dict(text="Impacto no Projeto", font=dict(color="#94A3B8"))
        layout_heat["yaxis"]["title"] = dict(text="Probabilidade de Ocorrência", font=dict(color="#94A3B8"))
        fig_heat.update_layout(layout_heat)
        st.plotly_chart(fig_heat, use_container_width=True, config=PLOTLY_CONFIG)

    with col_cat:
        cat_counts = df_risks["Categoria"].value_counts()
        fig_cat = go.Figure(data=[go.Pie(
            labels=cat_counts.index,
            values=cat_counts.values,
            hole=0.45,
            marker=dict(colors=["#38BDF8", "#34D399", "#A78BFA", "#FBBF24", "#F87171"])
        )])
        fig_cat.update_layout(get_plotly_layout("Distribuição de Riscos por Categoria", height=380))
        st.plotly_chart(fig_cat, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("#### Detalhamento dos Riscos e Planos de Ação")
    st.dataframe(df_risks, use_container_width=True, hide_index=True)


def render_quality_tab(sonar_data: dict, is_mock: bool):
    """Renderiza a aba de Qualidade de Produto (SonarCloud), uma seção por repositório."""
    if is_mock:
        render_mock_alert("Qualidade de Produto", "Sonar_API-Measures-*.json")

    st.markdown("### Qualidade de Produto (SonarCloud)")

    repos_disponiveis = [key for key in REPOS_CONFIG if key in sonar_data]
    if not repos_disponiveis:
        st.info("Nenhuma métrica de qualidade disponível para os repositórios de código (APP/IA).")
        return

    repo_key = st.radio(
        "Repositório:",
        options=repos_disponiveis,
        format_func=lambda k: REPOS_CONFIG[k]["name"],
        horizontal=True,
        key="quality_repo_selector"
    )
    metrics = sonar_data[repo_key]

    q1, q2, q3, q4 = st.columns(4)
    with q1:
        render_kpi("Linhas de Código", f"{metrics['ncloc']:,}", "ncloc", THEME_COLORS["primary"])
    with q2:
        cobertura = metrics.get("coverage")
        cobertura_txt = f"{cobertura:.1f}%" if cobertura is not None else "N/A"
        cobertura_sub = "Cobertura de testes" if cobertura is not None else "Sem testes apurados ainda"
        render_kpi("Cobertura", cobertura_txt, cobertura_sub, THEME_COLORS["secondary"])
    with q3:
        gate = metrics.get("quality_gate") or "N/A"
        gate_color = THEME_COLORS["secondary"] if gate == "OK" else (THEME_COLORS["danger"] if gate == "ERROR" else THEME_COLORS["accent"])
        render_kpi("Quality Gate", gate, "Estado do portão de qualidade", gate_color)
    with q4:
        render_kpi("Débito Técnico", f"{metrics['technical_debt_min']} min", "Tempo estimado de correção", THEME_COLORS["warning"])

    st.markdown("<br>", unsafe_allow_html=True)

    col_issues, col_ratings = st.columns([1.35, 1.0])
    with col_issues:
        fig_issues = go.Figure(go.Bar(
            x=["Bugs", "Vulnerabilidades", "Code Smells", "Security Hotspots"],
            y=[metrics["bugs"], metrics["vulnerabilities"], metrics["code_smells"], metrics["security_hotspots"]],
            marker=dict(color=["#F87171", "#FB923C", "#FBBF24", "#A78BFA"]),
            text=[metrics["bugs"], metrics["vulnerabilities"], metrics["code_smells"], metrics["security_hotspots"]],
            textposition="auto"
        ))
        fig_issues.update_layout(get_plotly_layout(f"Achados Estáticos — {REPOS_CONFIG[repo_key]['name']}", height=340))
        st.plotly_chart(fig_issues, use_container_width=True, config=PLOTLY_CONFIG)

    with col_ratings:
        st.markdown("#### Notas de Avaliação")
        render_kpi("Manutenibilidade", rating_to_letter(metrics.get("maintainability_rating")), "Sqale Rating", THEME_COLORS["primary"])
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        render_kpi("Confiabilidade", rating_to_letter(metrics.get("reliability_rating")), "Reliability Rating", THEME_COLORS["primary"])
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        render_kpi("Segurança", rating_to_letter(metrics.get("security_rating")), "Security Rating", THEME_COLORS["primary"])

    # Restrito a ncloc/coverage: as demais métricas do histórico (ratings, contagens
    # de achados) misturam unidades diferentes e, com 1 ponto só por dia de coleta,
    # não formam uma série legível junto com essas duas.
    series_historico = {"ncloc": [], "coverage": []}
    for serie in metrics.get("history", []):
        if serie.get("metric") not in series_historico:
            continue
        pontos = [item for item in serie.get("history", []) if "value" in item]
        series_historico[serie["metric"]] = pontos

    if any(series_historico.values()):
        st.markdown("#### Evolução Histórica (Linhas de Código e Cobertura)")
        fig_hist = go.Figure()
        for nome_metrica, pontos in series_historico.items():
            if not pontos:
                continue
            fig_hist.add_trace(go.Scatter(
                x=[p["date"] for p in pontos],
                y=[float(p["value"]) for p in pontos],
                name=nome_metrica,
                mode="lines+markers"
            ))
        fig_hist.update_layout(get_plotly_layout("Métricas ao Longo do Tempo", height=320))
        st.plotly_chart(fig_hist, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("#### Detalhamento Completo")
    tabela = pd.DataFrame([{
        "Repositório": REPOS_CONFIG[repo_key]["name"],
        "Linhas de Código": metrics["ncloc"],
        "Testes": metrics["tests"],
        "Cobertura (%)": metrics.get("coverage") if metrics.get("coverage") is not None else "N/A",
        "Duplicidade (%)": metrics["duplicated_lines_density"],
        "Bugs": metrics["bugs"],
        "Vulnerabilidades": metrics["vulnerabilities"],
        "Code Smells": metrics["code_smells"],
        "Security Hotspots": metrics["security_hotspots"],
        "Débito Técnico (min)": metrics["technical_debt_min"],
        "Coletado em": metrics.get("collected_at") or "N/A"
    }])
    st.dataframe(tabela, use_container_width=True, hide_index=True)


def render_process_tab():
    """Renderiza a aba de Processo e CI/CD."""
    runs_data, is_runs_mock = get_github_runs_data()
    
    if is_runs_mock:
        render_mock_alert("Fluxo de CI/CD", "GitHub_API-Runs-*.json")

    st.markdown("### Métricas de Processo e Integração Contínua (CI/CD)")
    
    p1, p2, p3 = st.columns(3)
    with p1:
        render_kpi("Taxa de Sucesso CI/CD", f"{runs_data['success_rate']}%", "Builds sem erro", THEME_COLORS["secondary"])
    with p2:
        render_kpi("Tempo Médio de Feedback", f"{runs_data['avg_duration_min']} min", "Duração média de execução", THEME_COLORS["primary"])
    with p3:
        render_kpi("Total de Builds Monitoradas", str(runs_data['total_runs']), "Execuções rastreadas", THEME_COLORS["accent"])

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_ci_line, col_ci_donut = st.columns([1.35, 1.0])
    with col_ci_line:
        fig_ci = go.Figure()
        fig_ci.add_trace(go.Scatter(
            x=[f"Run {i+1}" for i in range(len(runs_data["recent_feedback_series"]))],
            y=runs_data["recent_feedback_series"],
            mode="lines+markers",
            line=dict(color="#38BDF8", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(56, 189, 248, 0.12)"
        ))
        fig_ci.update_layout(get_plotly_layout("Tempo de Resposta dos Últimos Pipelines (Minutos)", height=320))
        st.plotly_chart(fig_ci, use_container_width=True, config=PLOTLY_CONFIG)

    with col_ci_donut:
        fig_donut = go.Figure(data=[go.Pie(
            labels=["Sucesso", "Falha"],
            values=[runs_data["success_rate"], 100 - runs_data["success_rate"]],
            hole=0.55,
            marker=dict(colors=["#34D399", "#F87171"])
        )])
        fig_donut.update_layout(get_plotly_layout("Estabilidade da Esteira de Integração", height=320))
        st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CONFIG)


def render_theory_tab():
    """Memória de cálculo e critérios formais."""
    st.markdown("### Fundamentação Teórica e Critérios Acadêmicos")
    st.markdown(r"""
    A formulação do **Agile EVM** segue o modelo de **Sulaiman, Barton e Blackburn (2006)** (*"AgileEVM - Earned Value Management in Scrum Projects"*):

    1. **BAC (Budget at Completion)**: Orçamento total planejado da release:
       $$BAC = PRP_0 \times \text{Custo Unitário}$$
    2. **PRPₙ (Planned Release Points)**: Escopo total na Sprint $n$, considerando pontos adicionados ($PA$):
       $$PRP_n = PRP_0 + \sum_{k=1}^{n} PA_k$$
    3. **PPC (Planned Percent Complete)**: Percentual de tempo decorrido:
       $$PPC = \frac{n}{PS}$$
    4. **APC (Actual Percent Complete)**: Percentual de escopo concluído:
       $$APC_n = \frac{RPC_n}{PRP_n}$$
    5. **PV (Planned Value)**: $PV = PPC \times BAC$
    6. **EV (Earned Value)**: $EV = APC_n \times BAC$
    7. **SPI (Schedule Performance Index)**: $SPI = \frac{EV}{PV}$
    8. **CPI (Cost Performance Index)**: $CPI = \frac{EV}{AC_n}$
    """)


def main():
    apply_custom_theme()
    render_header()
    
    sim_prp0, sim_ps, sim_budget = render_sidebar()
    
    sprints_data, is_sprints_mock = get_zenhub_sprints_data()
    sprints_data = filter_started_sprints(sprints_data)
    risks_data, is_risks_mock = get_risks_data()
    sonar_data, is_sonar_mock = get_sonar_metrics_data()

    # Alerta global discreto caso algum dos eixos utilize dados mockados
    any_mock = is_sprints_mock or is_risks_mock or is_sonar_mock
    if any_mock:
        st.info(
            "Ambiente em modo de demonstração (dados simulados): "
            "Os arquivos `.json` em `analytics-raw-data/` serão consumidos automaticamente assim que forem gerados pelo pipeline de CI/CD."
        )
    
    evm_results = compute_agile_evm_metrics(
        sprints=sprints_data,
        prp_0=sim_prp0,
        planned_sprints=sim_ps,
        sprint_budget_brl=sim_budget
    )

    tab_evm, tab_riscos, tab_processo, tab_qualidade, tab_teoria = st.tabs([
        "Agile EVM e Velocity",
        "Gestão de Riscos",
        "Processo e CI/CD",
        "Qualidade de Produto",
        "Memória de Cálculo"
    ])

    with tab_evm:
        render_evm_tab(evm_results, is_sprints_mock)

    with tab_riscos:
        render_risks_tab(risks_data, is_risks_mock)

    with tab_processo:
        render_process_tab()

    with tab_qualidade:
        render_quality_tab(sonar_data, is_sonar_mock)

    with tab_teoria:
        render_theory_tab()


if __name__ == "__main__":
    main()