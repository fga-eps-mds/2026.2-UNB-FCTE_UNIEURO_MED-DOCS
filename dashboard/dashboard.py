import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

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
from src.data_layer import (
    get_zenhub_sprints_data,
    get_risks_data,
    get_github_runs_data,
    get_sonar_metrics_data,
    get_qrapids_data,
    get_latest_collection_timestamp
)
from src.metrics import compute_agile_evm_metrics, process_risks_summary
from src.processo import INDICADORES
from src.qualidade import BRASILIA, FAIXA_ADEQUADA, FAIXA_ATENCAO, METRICAS, QUEDA_RELEVANTE, faixa
from src.templates import (
    arquivos_fora_do_limiar,
    cor_da_faixa,
    formatar_indice,
    marcos_sem_medida,
    rotulo_do_marco,
    serie_do_indice,
    tabela_comparativo,
    tabela_processo,
    tabela_qrapids,
)

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
    ultima_coleta = get_latest_collection_timestamp()
    if ultima_coleta:
        local = ultima_coleta.astimezone(ZoneInfo("America/Sao_Paulo"))
        texto_atualizacao = f"Atualizado em: {local.strftime('%d/%m/%Y %H:%M')} (horário de Brasília, última coleta real)"
    else:
        texto_atualizacao = "Atualizado em: dados de exemplo — nenhuma coleta real encontrada em analytics-raw-data/"
    st.caption(texto_atualizacao)
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


def _layout_barras(titulo: str, y_title: str, height: int) -> dict:
    """Layout para barras agrupadas: afasta a legenda para não cobrir os rótulos do eixo."""
    layout = get_plotly_layout(titulo, height=height, y_title=y_title)
    layout["legend"]["y"] = -0.32
    layout["margin"]["b"] = 105
    layout["barmode"] = "group"
    return layout


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

    # Largura cheia em vez de colunas lado a lado: com 2+ séries e legenda,
    # um gráfico espremido em meia coluna fica ilegível. Cada gráfico ganha
    # o espaço inteiro da aba, empilhado verticalmente.
    st.markdown("#### Evolução do Valor Agregado (Burnup)")
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
    fig_burnup.update_layout(get_plotly_layout("Burnup — Planejado (PV) × Realizado (EV)", y_title="R$"))
    st.plotly_chart(fig_burnup, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("#### Histórico de Velocity")
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
    fig_vel.update_layout(get_plotly_layout("Velocity por Sprint (Story Points Entregues)", height=360, y_title="Story Points"))
    st.plotly_chart(fig_vel, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("#### Burndown — Orçamento Restante a Entregar")
    # Espelha o burnup (BAC − PV/EV): mesma base de cálculo, sem precisar de novos
    # campos em metrics.py. Sprints sem EV apurado (ainda não concluídas) ficam
    # com gap no traço real, igual ao burnup faz com None.
    bac = evm["bac"]
    remaining_ideal = [round(bac - pv, 2) for pv in evm["burnup_pv"]]
    remaining_actual = [round(bac - ev, 2) if ev is not None else None for ev in evm["burnup_ev"]]
    fig_burndown = go.Figure()
    fig_burndown.add_trace(go.Scatter(
        x=evm["burnup_labels"],
        y=remaining_ideal,
        name="Restante Ideal (PV)",
        mode="lines+markers",
        line=dict(color="#94A3B8", width=2.5, dash="dash")
    ))
    fig_burndown.add_trace(go.Scatter(
        x=evm["burnup_labels"],
        y=remaining_actual,
        name="Restante Real (EV)",
        mode="lines+markers",
        fill="tozeroy",
        fillcolor="rgba(248, 113, 113, 0.15)",
        line=dict(color="#F87171", width=3)
    ))
    fig_burndown.update_layout(get_plotly_layout("Burndown — Orçamento Restante (BAC − PV / BAC − EV)", y_title="R$"))
    st.plotly_chart(fig_burndown, use_container_width=True, config=PLOTLY_CONFIG)

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
    fig_indices.update_layout(get_plotly_layout("Evolução Histórica do SPI e CPI por Sprint", height=360, y_title="Índice"))
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
        st.caption("🟢 Baixo (1–5) · 🟡 Médio (6–12) · 🟠 Alto (15–16) · 🔴 Crítico (20–25) — severidade = probabilidade × impacto")
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
        
        # Agrupa por célula (impacto, probabilidade): com muitos riscos mapeados é comum
        # mais de um cair na mesma combinação, e uma anotação por risco esconderia todas
        # menos a última desenhada.
        riscos_por_celula = {}
        for r in risks_raw:
            celula = (r["impacto"] - 1, r["probabilidade"] - 1)
            riscos_por_celula.setdefault(celula, []).append(r["id"])

        for (x, y), ids in riscos_por_celula.items():
            # Empilha verticalmente (<br>) em vez de lado a lado quando há 3+ na mesma
            # célula: a caixa cresce para cima/baixo em vez de invadir a célula vizinha.
            separador = ", " if len(ids) <= 2 else "<br>"
            fig_heat.add_annotation(
                x=x,
                y=y,
                text=f"<b>{separador.join(ids)}</b>",
                showarrow=False,
                font=dict(color="#FFFFFF", size=11 if len(ids) <= 2 else 9),
                bgcolor="rgba(15, 23, 42, 0.9)",
                bordercolor="#38BDF8",
                borderwidth=1.5,
                borderpad=4
            )

        layout_heat = get_plotly_layout("Matriz de Probabilidade × Impacto (5×5)", height=400)
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
        fig_cat.update_layout(get_plotly_layout("Distribuição de Riscos por Categoria", height=400))
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

    st.markdown("#### Achados Estáticos")
    fig_issues = go.Figure(go.Bar(
        x=["Bugs", "Vulnerabilidades", "Code Smells", "Security Hotspots"],
        y=[metrics["bugs"], metrics["vulnerabilities"], metrics["code_smells"], metrics["security_hotspots"]],
        marker=dict(color=["#F87171", "#FB923C", "#FBBF24", "#A78BFA"]),
        text=[metrics["bugs"], metrics["vulnerabilities"], metrics["code_smells"], metrics["security_hotspots"]],
        textposition="auto"
    ))
    fig_issues.update_layout(get_plotly_layout(f"Achados Estáticos — {REPOS_CONFIG[repo_key]['name']}", height=360, y_title="Ocorrências"))
    st.plotly_chart(fig_issues, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("#### Notas de Avaliação")
    n1, n2, n3 = st.columns(3)
    with n1:
        render_kpi("Manutenibilidade", rating_to_letter(metrics.get("maintainability_rating")), "Sqale Rating", THEME_COLORS["primary"])
    with n2:
        render_kpi("Confiabilidade", rating_to_letter(metrics.get("reliability_rating")), "Reliability Rating", THEME_COLORS["primary"])
    with n3:
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
        fig_hist.update_layout(get_plotly_layout("Métricas ao Longo do Tempo", height=360, y_title="Valor"))
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
        fig_ci.update_layout(get_plotly_layout("Tempo de Resposta dos Últimos Pipelines", height=360, y_title="Minutos"))
        st.plotly_chart(fig_ci, use_container_width=True, config=PLOTLY_CONFIG)

    with col_ci_donut:
        fig_donut = go.Figure(data=[go.Pie(
            labels=["Sucesso", "Falha"],
            values=[runs_data["success_rate"], 100 - runs_data["success_rate"]],
            hole=0.55,
            marker=dict(colors=["#34D399", "#F87171"])
        )])
        fig_donut.update_layout(get_plotly_layout("Estabilidade da Esteira de Integração", height=360))
        st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CONFIG)


def _linha_de_faixas(fig):
    """
    Marca no gráfico os limites das faixas Adequado e Atenção do Plano de Qualidade.

    O rótulo vai para a legenda: escrito sobre a linha ele cobriria as barras e os pontos.
    """
    for limite, cor, nome in ((FAIXA_ADEQUADA, THEME_COLORS["secondary"], "Adequado a partir de"),
                              (FAIXA_ATENCAO, THEME_COLORS["warning"], "Atenção a partir de")):
        fig.add_hline(y=limite, line_dash="dot", line_color=cor)
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name=f"{nome} {limite:.2f}",
                                 line=dict(color=cor, dash="dot")))


def _config_colunas(tabela: pd.DataFrame, largura_primeira: int, largura_demais: int) -> dict:
    """Larguras em pixels: sem isso a coluna de texto longo empurra as demais para fora da tabela."""
    return {
        coluna: st.column_config.TextColumn(coluna, width=largura_primeira if i == 0 else largura_demais)
        for i, coluna in enumerate(tabela.columns)
    }


def _render_qrapids_produto(produto: dict):
    """Q-Rapids do produto: índices por marco de release, evolução por versão e causa por arquivo."""
    repos = [r for r in ("APP", "IA") if produto[r]["avaliacoes"]]
    if not repos:
        st.info("Nenhuma versão do produto foi coletada ainda em `analytics-raw-data/`.")
        return

    repo = st.radio(
        "Repositório:",
        options=repos,
        format_func=lambda k: REPOS_CONFIG[k]["name"],
        horizontal=True,
        key="qrapids_repo_selector"
    )
    item = produto[repo]
    marcos = {nome: v for nome, v in item["marcos"].items() if v}
    if not marcos:
        st.info(
            f"A qualidade interna de **{REPOS_CONFIG[repo]['name']}** ainda não está medida: nenhuma versão "
            "tem arquivos de código com resultado do SonarCloud. Pelo Plano de Qualidade, o valor fica "
            "como não medido, e não como zero."
        )
        return

    sem_medida = marcos_sem_medida(item["marcos"], datetime.now(BRASILIA))
    if sem_medida:
        st.warning(
            f"Sem versão nova medida para: **{', '.join(sem_medida)}**. Nesses marcos o valor fica como não "
            "medido, e não como zero, e os índices abaixo são os dos marcos que tiveram versão."
        )

    ultimo_nome, ultimo = list(marcos.items())[-1]
    faixas_txt = (f"Adequado a partir de {FAIXA_ADEQUADA:.2f}, Atenção de {FAIXA_ATENCAO:.2f} a "
                  f"{FAIXA_ADEQUADA - 0.01:.2f} e Crítico abaixo de {FAIXA_ATENCAO:.2f}.")
    ajuda = {
        "Q": "Índice de qualidade do produto: média de Manutenibilidade (M) e Confiabilidade (C), de 0 a 1. ",
        "M": "Manutenibilidade: média da qualidade do código (QC), do código sem problema grave (CB) e da "
             "testabilidade (T). Indica o quanto o código é fácil de manter. ",
        "C": "Confiabilidade: média do sucesso dos testes (ST) e dos defeitos prováveis (DP). Indica o "
             "quanto se pode confiar que o código funciona. ",
    }
    colunas = st.columns(3)
    for coluna, chave, nome in zip(colunas, ("Q", "M", "C"), ("Índice de Qualidade", "Manutenibilidade", "Confiabilidade")):
        agregado = ultimo["agregacao"][chave]
        with coluna:
            render_kpi(
                f"{chave} {nome}",
                formatar_indice(agregado["valor"], agregado["parcial"]),
                f"{faixa(agregado['valor'])} em {rotulo_do_marco(ultimo_nome, ultimo)}",
                cor_da_faixa(agregado["valor"]),
                help_text=ajuda[chave] + faixas_txt,
            )
    st.markdown("<br>", unsafe_allow_html=True)

    if item["quedas"]:
        linhas = "\n".join(
            f"- **{q['indicador']}** caiu de {q['antes']:.2f} ({q['de']}) para {q['depois']:.2f} ({q['para']})."
            for q in item["quedas"]
        )
        st.warning(
            f"Queda de {QUEDA_RELEVANTE:.2f} ou mais entre duas versões medidas seguidas. O plano pede "
            f"a análise da causa e o registro da decisão:\n\n{linhas}"
        )
    else:
        st.caption(
            f"Nenhum fator, característica ou índice caiu {QUEDA_RELEVANTE:.2f} ou mais entre duas "
            "versões medidas seguidas, o que dispensa a análise de queda do plano."
        )

    st.markdown("#### Índices por Release")
    nomes = [rotulo_do_marco(n, v) for n, v in marcos.items()]
    fig_marcos = go.Figure()
    for chave, cor in (("Q", THEME_COLORS["primary"]), ("M", THEME_COLORS["accent"]), ("C", THEME_COLORS["secondary"])):
        fig_marcos.add_trace(go.Bar(
            x=nomes, y=[v["agregacao"][chave]["valor"] for v in marcos.values()], name=chave,
            marker_color=cor, text=[formatar_indice(v["agregacao"][chave]["valor"]) for v in marcos.values()],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>" + chave + ": %{y:.2f}<extra></extra>"
        ))
    _linha_de_faixas(fig_marcos)
    layout = _layout_barras("Qualidade do produto por marco de release", "Índice de 0 a 1", 400)
    layout["yaxis"]["range"] = [0, 1.1]
    fig_marcos.update_layout(layout)
    st.plotly_chart(fig_marcos, use_container_width=True, config=PLOTLY_CONFIG)
    st.caption(
        "Cada release é representada pela última versão medida até a data dela. Os asteriscos nas "
        "tabelas marcam valores parciais: faltava uma métrica abaixo deles e o peso foi dividido entre as demais."
    )

    tabela = tabela_qrapids(marcos)
    st.dataframe(tabela, use_container_width=True, hide_index=True,
                 column_config=_config_colunas(tabela, 360, 115), height=(len(tabela) + 1) * 35 + 3)
    st.caption("n/m: métrica não medida na versão. * valor parcial.")

    st.markdown("#### Evolução do Índice Q por Versão")
    serie = serie_do_indice(item["avaliacoes"])
    fig_serie = go.Figure(go.Scatter(
        x=serie["versao"], y=serie["valor"], mode="lines+markers", connectgaps=False,
        line=dict(color=THEME_COLORS["primary"], width=3),
        marker=dict(size=9, symbol=["circle-open" if p else "circle" for p in serie["parcial"]]),
        hovertemplate="<b>%{x}</b><br>Q: %{y:.2f}<extra></extra>"
    ))
    _linha_de_faixas(fig_serie)
    layout = get_plotly_layout("Índice Q de cada versão", height=360, y_title="Índice Q")
    layout["yaxis"]["range"] = [0, 1.05]
    fig_serie.update_layout(layout)
    st.plotly_chart(fig_serie, use_container_width=True, config=PLOTLY_CONFIG)
    st.caption(
        "Círculos vazados são versões com valor parcial. Uma versão sem ponto não teve dado no .json "
        "da release, e a linha é interrompida em vez de cair a zero."
    )

    st.markdown("#### De Onde Vem Cada Nota")
    c1, c2 = st.columns(2)
    with c1:
        marco_escolhido = st.selectbox("Release:", options=list(marcos), key="qrapids_marco_selector")
    with c2:
        metrica = st.selectbox(
            "Métrica:", options=list(METRICAS), format_func=lambda k: f"{k} {METRICAS[k]}",
            key="qrapids_metrica_selector"
        )
    detalhe = arquivos_fora_do_limiar(marcos[marco_escolhido], metrica)
    if detalhe["valor"] is None:
        st.info(detalhe["motivo"] or "Métrica não medida nesta versão.")
    else:
        st.markdown(
            f"**{detalhe['conformes']} de {detalhe['total']}** itens estão dentro do limiar, "
            f"o que dá {formatar_indice(detalhe['valor'])}."
        )
        if detalhe["arquivos"]:
            st.dataframe(pd.DataFrame({"Fora do limiar": detalhe["arquivos"]}), use_container_width=True, hide_index=True)
        else:
            st.success("Nenhum arquivo fora do limiar nesta métrica.")

    with st.expander("Como ler o Q-Rapids"):
        st.markdown(
            "O Q-Rapids transforma medidas do SonarCloud em índices de 0 a 1, e cada nível é a média "
            "ponderada do nível abaixo: **métricas (m1 a m8)**, **fatores (QC, CB, T, ST, DP)**, "
            "**características (M e C)** e o **índice Q**. As métricas m1 a m3 e m5 a m8 são densidades: "
            "a parte dos arquivos que respeita o limiar do plano. A m4 é a taxa de testes que passam.\n\n"
            f"- {faixas_txt}\n"
            "- Como as métricas são densidades, o mesmo problema pesa menos em um código maior. Se uma "
            "nota sobe porque o código cresceu, e não porque o problema foi resolvido, a lista de "
            "arquivos acima mostra a diferença.\n"
            "- Métrica sem dado é **não medida (n/m)**, nunca zero. O peso dela é dividido entre as demais "
            "e o resultado é marcado como parcial. Uma comparação com valor parcial não gera alerta de queda.\n"
            "- A data de criação de um problema no SonarCloud é a do commit da linha, e não a da análise. "
            "Em versões antigas, m7 e m8 podem apontar um problema alguns dias antes de ele ter sido encontrado."
        )


def _render_qrapids_processo(processo_dados: dict):
    """Indicadores de processo P1 a P3 e o índice P por release."""
    if not processo_dados:
        st.info("Nenhuma sprint com pontos planejados nem execução de CI foi coletada ainda.")
        return

    ids = list(processo_dados)
    release = st.radio(
        "Release:", options=ids, index=len(ids) - 1, horizontal=True, key="processo_release_selector"
    )
    item = processo_dados[release]
    valores = item["indicadores"]

    ajuda = {
        "P1": "Execuções do CI que terminaram com sucesso sobre as concluídas com sucesso ou falha, no APP e na IA. "
              "Execuções puladas ou canceladas não entram. Mede se o código se mantém estável a cada mudança.",
        "P2": "Pontos de história aceitos pelo PO sobre os pontos planejados, em média por sprint. "
              "Uma história só conta depois do aceite.",
        "P3": "Parte do escopo final da sprint que já estava nela quando a sprint começou. "
              "Abaixo de 1,00, entraram pontos com a sprint em andamento.",
    }
    colunas = st.columns(4)
    for coluna, (chave, nome) in zip(colunas[:3], INDICADORES.items()):
        with coluna:
            render_kpi(f"{chave} {nome}", formatar_indice(valores[chave]), "Índice de 0 a 1",
                       cor_da_faixa(valores[chave]), help_text=ajuda[chave])
    with colunas[3]:
        render_kpi("P Índice de Processo", formatar_indice(item["P"], item["parcial"]), "Média de P1, P2 e P3",
                   cor_da_faixa(item["P"]),
                   help_text="Média simples de P1, P2 e P3, com as mesmas faixas do Q-Rapids: "
                             f"Adequado a partir de {FAIXA_ADEQUADA:.2f} e Crítico abaixo de {FAIXA_ATENCAO:.2f}.")
    st.markdown("<br>", unsafe_allow_html=True)

    if item["em_andamento"]:
        st.caption("Release em andamento: P2, P3 e a velocidade mudam até o fim das sprints.")
    ci = item["execucoes"]
    if ci:
        st.caption(f"CI: {ci['success']} de {ci['success'] + ci['failure']} execuções concluídas terminaram com sucesso (APP e IA).")
    if valores["P2"] == 0:
        st.info(
            "Nenhum ponto de história foi aceito pelo PO nas sprints desta release. Sem o aceite a "
            "história não conta como entregue, então P2 e a velocidade ficam em zero. É o mesmo efeito "
            "do aviso da aba de EVM: indica espera de aceite, e não necessariamente atraso do time."
        )
    if valores["P3"] is not None and valores["P3"] < 1:
        st.info(
            f"Entraram pontos nas sprints depois do início: só {valores['P3'] * 100:.0f}% do escopo "
            "final já estava planejado quando elas começaram."
        )

    st.markdown("#### Processo por Release")
    fig = go.Figure()
    cores = {"P1": THEME_COLORS["primary"], "P2": THEME_COLORS["accent"], "P3": THEME_COLORS["warning"]}
    rotulos = [r + (" (em andamento)" if processo_dados[r]["em_andamento"] else "") for r in ids]
    for chave, nome in INDICADORES.items():
        fig.add_trace(go.Bar(
            x=rotulos, y=[processo_dados[r]["indicadores"][chave] for r in ids], name=f"{chave} {nome}",
            marker_color=cores[chave],
            text=[formatar_indice(processo_dados[r]["indicadores"][chave]) for r in ids], textposition="outside",
            hovertemplate="<b>%{x}</b><br>" + chave + ": %{y:.2f}<extra></extra>"
        ))
    fig.add_trace(go.Scatter(
        x=rotulos, y=[processo_dados[r]["P"] for r in ids], name="P Índice de processo", mode="lines+markers",
        line=dict(color="#F8FAFC", width=2), hovertemplate="<b>%{x}</b><br>P: %{y:.2f}<extra></extra>"
    ))
    _linha_de_faixas(fig)
    layout = _layout_barras("Indicadores de processo por release", "Índice de 0 a 1", 420)
    layout["yaxis"]["range"] = [0, 1.15]
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    tabela = tabela_processo(processo_dados)
    st.dataframe(tabela, use_container_width=True, hide_index=True)
    st.caption(
        "P1 Estabilidade do CI, P2 Entrega do comprometido, P3 Estabilidade do escopo e P Índice de processo "
        "(média dos três). n/m: não medido. * valor parcial."
    )

    with st.expander("Como ler os indicadores de processo"):
        st.markdown(
            "O Plano de Qualidade define o modelo do produto, mas não o do processo. Estes três indicadores "
            "usam dados que a coleta diária já grava e seguem o mesmo princípio: valor de 0 a 1, sem dado é "
            "n/m, e as faixas são as do Q-Rapids. São uma **proposta do time** que ainda precisa ser "
            "validada com o professor.\n\n"
            "- **P1 Estabilidade do CI:** execuções com sucesso sobre execuções concluídas.\n"
            "- **P2 Entrega do comprometido:** pontos aceitos sobre pontos planejados, em média por sprint.\n"
            "- **P3 Estabilidade do escopo:** pontos que já estavam na sprint no início sobre os planejados ao final, "
            "em média por sprint.\n"
            "- **P Índice de processo:** média simples de P1, P2 e P3.\n\n"
            "P2 e P3 são médias por sprint porque somar os pontos da release contaria duas vezes a história "
            "que passa de uma sprint para a outra. Cada sprint entra na release em que termina, e sprints sem "
            "pontos planejados, como as de preparação, ficam de fora."
        )


def _render_qrapids_comparativo(comparativo: dict):
    """Comparação entre releases de velocidade, cobertura e defeitos, como pede o DA-R2."""
    if not comparativo:
        st.info("Ainda não há dados de nenhuma release para comparar.")
        return

    ids = list(comparativo)
    st.dataframe(tabela_comparativo(comparativo), use_container_width=True, hide_index=True)
    st.caption(
        "Velocidade e Planejados em pontos de história por sprint. Defeito provável é a quantidade de arquivos "
        "com problema de confiabilidade no SonarCloud. A cobertura e o defeito provável vêm da última versão do "
        "APP medida até o fim de cada release. Os bugs abertos contam só as issues com o rótulo `bug`; defeitos "
        "corrigidos direto em PR, sem issue, não aparecem."
    )

    velocidades = [comparativo[r]["velocidade"] or 0 for r in ids]
    if all(v == 0 for v in velocidades):
        st.info(
            "A velocidade é zero porque nenhuma história foi aceita pelo PO. Os pontos planejados por sprint "
            "mostram o quanto está esperando aceite."
        )

    col_a, col_b = st.columns(2)
    with col_a:
        fig_vel = go.Figure()
        fig_vel.add_trace(go.Bar(
            x=ids, y=velocidades, name="Velocidade (aceitos)", marker_color=THEME_COLORS["secondary"],
            text=[f"{v:.1f}" for v in velocidades], textposition="outside",
            hovertemplate="<b>%{x}</b><br>Aceitos por sprint: %{y:.1f}<extra></extra>"
        ))
        planejados = [comparativo[r]["planejados_por_sprint"] or 0 for r in ids]
        fig_vel.add_trace(go.Bar(
            x=ids, y=planejados, name="Planejados", marker_color=THEME_COLORS["primary"],
            text=[f"{v:.1f}" for v in planejados], textposition="outside",
            hovertemplate="<b>%{x}</b><br>Planejados por sprint: %{y:.1f}<extra></extra>"
        ))
        fig_vel.update_layout(_layout_barras("Velocidade e pontos planejados", "Pontos por sprint", 380))
        st.plotly_chart(fig_vel, use_container_width=True, config=PLOTLY_CONFIG)
    with col_b:
        fig_def = go.Figure()
        bugs = [comparativo[r]["bugs_abertos_na_release"] or 0 for r in ids]
        provaveis = [comparativo[r]["arquivos_com_defeito_provavel"] or 0 for r in ids]
        fig_def.add_trace(go.Bar(
            x=ids, y=bugs, name="Issues de bug abertas", marker_color=THEME_COLORS["danger"],
            text=bugs, textposition="outside",
            hovertemplate="<b>%{x}</b><br>Issues de bug: %{y}<extra></extra>"
        ))
        fig_def.add_trace(go.Bar(
            x=ids, y=provaveis, name="Arquivos com defeito provável", marker_color=THEME_COLORS["warning"],
            text=provaveis, textposition="outside",
            hovertemplate="<b>%{x}</b><br>Arquivos: %{y}<extra></extra>"
        ))
        fig_def.update_layout(_layout_barras("Defeitos por release", "Quantidade", 380))
        st.plotly_chart(fig_def, use_container_width=True, config=PLOTLY_CONFIG)

    with st.expander("Como ler a comparação"):
        st.markdown(
            "- **Velocidade:** média dos pontos de história aceitos por sprint. Os pontos planejados por "
            "sprint acompanham o número porque explicam uma velocidade baixa.\n"
            "- **Cobertura:** percentual do código do APP exercitado por testes na versão que representa a release.\n"
            "- **Issues de bug abertas:** issues com o rótulo `bug` abertas dentro do período da release.\n"
            "- **Arquivos com defeito provável:** arquivos com problema de confiabilidade aberto no SonarCloud "
            "(o que reduz a m8 do Q-Rapids)."
        )


def render_qrapids_tab(dados: dict):
    """Aba do DA-R2: Q-Rapids do produto, indicadores de processo e comparação entre releases."""
    st.markdown("### Q-Rapids, Processo e Comparação entre Releases (DA-R2)")
    st.caption(
        "Índices de 0 a 1 calculados com os arquivos de `analytics-raw-data/`, conforme o Plano de Qualidade. "
        "Valor sem dado aparece como n/m (não medido), nunca como zero."
    )
    st.warning(
        "Os limiares, os pesos e os indicadores de processo são uma proposta do time e aguardam a "
        "validação do professor."
    )

    if not dados["disponivel"]:
        st.info(
            "Os arquivos de qualidade, de CI e de sprints ainda não foram coletados em `analytics-raw-data/`. "
            "Esta aba não usa dados de exemplo, porque um índice inventado seria lido como resultado real."
        )
        return

    aba_produto, aba_processo, aba_comparativo = st.tabs([
        "Qualidade do Produto", "Processo", "Comparação entre Releases"
    ])
    with aba_produto:
        _render_qrapids_produto(dados["produto"])
    with aba_processo:
        _render_qrapids_processo(dados["processo"])
    with aba_comparativo:
        _render_qrapids_comparativo(dados["comparativo"])


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
    qrapids_data = get_qrapids_data()

    # Alerta global discreto caso algum dos eixos utilize dados mockados.
    # Nomeia a(s) fonte(s) em mock explicitamente: sem isso, o aviso genérico
    # aparece sempre que qualquer uma estiver mockada (ex: Riscos, bloqueado
    # pela issue #26) e passa a impressão de que TUDO está em modo demo,
    # mesmo quando as outras fontes já são dados reais.
    fontes_mock = []
    if is_sprints_mock:
        fontes_mock.append("Sprints/Agile EVM")
    if is_risks_mock:
        fontes_mock.append("Matriz de Riscos")
    if is_sonar_mock:
        fontes_mock.append("Qualidade de Produto")

    if fontes_mock:
        st.info(
            f"Modo de demonstração para: **{', '.join(fontes_mock)}**. "
            "As demais abas já consomem dados reais de `analytics-raw-data/`. "
            "Cada aba mostrada acima mostra seu próprio aviso quando usa dados simulados."
        )
    
    evm_results = compute_agile_evm_metrics(
        sprints=sprints_data,
        prp_0=sim_prp0,
        planned_sprints=sim_ps,
        sprint_budget_brl=sim_budget
    )

    tab_evm, tab_riscos, tab_processo, tab_qualidade, tab_qrapids, tab_teoria = st.tabs([
        "Agile EVM e Velocity",
        "Gestão de Riscos",
        "Processo e CI/CD",
        "Qualidade de Produto",
        "Q-Rapids e R1 × R2",
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

    with tab_qrapids:
        render_qrapids_tab(qrapids_data)

    with tab_teoria:
        render_theory_tab()


if __name__ == "__main__":
    main()