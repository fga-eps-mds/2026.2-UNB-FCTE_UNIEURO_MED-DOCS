import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from src.config import (
    ORGANIZATION,
    PROJECT_PREFIX,
    RELEASES,
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
    get_latest_collection_timestamp
)
from src.metrics import compute_release_evm, process_risks_summary

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


def agora_brasilia() -> datetime:
    """Data/hora atual no fuso de Brasília, para nomes de arquivo e carimbos de tempo."""
    return datetime.now(ZoneInfo("America/Sao_Paulo"))


def formatar_data_brasilia(valor) -> str:
    """Formata um timestamp (datetime ou string ISO) como dd/mm/aaaa HH:MM no horário de Brasília."""
    if not valor:
        return "N/A"
    dt = valor
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return "N/A"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")


def render_header():
    """Renderiza o cabeçalho executivo do dashboard."""
    ultima_coleta = get_latest_collection_timestamp()
    if ultima_coleta:
        texto_atualizacao = f"Atualizado em: {formatar_data_brasilia(ultima_coleta)} (horário de Brasília, última coleta real)"
    else:
        texto_atualizacao = "Atualizado em: dados de exemplo. Nenhuma coleta real encontrada em analytics-raw-data/"
    st.caption(texto_atualizacao)
    st.markdown(f"""
    <div class="hero-header">
        <div class="hero-title">Painel Analítico e Decisório — {PROJECT_PREFIX}</div>
        <div class="hero-sub">Engenharia de Produto de Software · Universidade de Brasília (UnB / FGA) · 2026.2</div>
        <div class="hero-badge">Release 1 (DA-R1) · Governança Ágil, EVM e Riscos</div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Barra lateral com metadados do projeto. O EVM não tem parâmetros ajustáveis."""
    st.sidebar.markdown("### Governança do Projeto")
    st.sidebar.info(f"**Organização:** `{ORGANIZATION}`\n\n**Projeto:** `{PROJECT_PREFIX}`")

    st.sidebar.markdown("---")
    st.sidebar.caption("Repositórios Integrados:\n- `-DOCS` (Documentação e Analytics)\n- `-IA` (Módulo de Inteligência Artificial)\n- `-APP` (Aplicação Mobile)")


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


def _formatar_release(r: dict) -> str:
    return f"{r['id']} ({r['inicio']:%d/%m} a {r['fim']:%d/%m})"


def render_evm_tab(evm: dict, velocity_sprints: list, is_mock: bool):
    """Renderiza a aba do Agile EVM por release, com burn de pontos e velocity."""
    if is_mock:
        render_mock_alert("Sprints e Agile EVM", "zenhub_analytics.json")

    st.markdown("### Desempenho de Prazo e Custos por Release (Agile EVM)")
    st.caption(
        "O EVM é calculado por release, com o orçamento (BAC) de cada release do Plano de Custos e "
        "os pontos reais do ZenHub. Não há parâmetros ajustáveis: o painel reflete o que aconteceu."
    )

    with st.expander("Como funciona o Agile EVM e como ler os índices"):
        st.markdown(
            "O Agile EVM compara, em reais, o que estava planejado com o que foi entregue e gasto. "
            "Ele é calculado por release porque é a release que tem orçamento e escopo próprios.\n\n"
            "- **BAC:** orçamento da release, vindo do Plano de Custos.\n"
            "- **PRP:** pontos de história planejados para a release (soma dos pontos das sprints "
            "que terminam dentro dela).\n"
            "- **RPC:** pontos de história já entregues.\n"
            "- **PPC:** fração dos dias da release já decorrida. **APC:** RPC dividido pelo PRP.\n"
            "- **PV** = PPC × BAC, o valor que deveria estar entregue. **EV** = APC × BAC, o valor "
            "realmente entregue. **AC:** custo incorrido.\n"
            "- **SPI** = EV ÷ PV (prazo) e **CPI** = EV ÷ AC (custo). Abaixo de 1,0 há atraso ou "
            "custo acima do valor entregue; acima de 1,0, o contrário.\n\n"
            "**Limitações a considerar na leitura:**\n\n"
            "- O PRP só é confiável se todas as histórias da release estiverem estimadas.\n"
            "- Ainda não há custo real apurado, então o AC é estimado pela linha de base de custo "
            "(PPC × BAC). Por isso o CPI coincide com o SPI até que o custo real seja registrado.\n"
            "- Uma sprint nem sempre coincide com os limites da release. Cada sprint é atribuída à "
            "release em que ela termina.\n"
            "- Releases que ainda não começaram não aparecem: só há o que medir depois da data de início."
        )

    releases = evm["releases"]
    ids = [r["id"] for r in releases]
    escolhido = st.radio(
        "Release:",
        options=ids,
        index=ids.index(evm["atual"]),
        format_func=lambda i: _formatar_release(next(r for r in releases if r["id"] == i)),
        horizontal=True,
        key="evm_release_selector"
    )
    r = next(x for x in releases if x["id"] == escolhido)

    if r["prp"] <= 0:
        st.warning(
            "Nenhum ponto estimado nas sprints desta release. Sem o PRP não é possível calcular "
            "o valor entregue (EV) nem os índices."
        )

    row1_c1, row1_c2, row1_c3 = st.columns(3)
    with row1_c1:
        render_kpi(
            "BAC da Release", f"R$ {r['bac']:,.2f}", f"Orçamento da {r['id']}", THEME_COLORS["primary"],
            help_text="Orçamento total da release, vindo do Plano de Custos. É fixo durante a "
                      "execução: só muda por uma mudança formal aprovada, nunca por variações de "
                      "desempenho."
        )
    with row1_c2:
        render_kpi(
            "PV (Valor Planejado)", f"R$ {r['pv']:,.2f}", f"{r['ppc'] * 100:.0f}% do prazo decorrido", THEME_COLORS["accent"],
            help_text="Quanto do orçamento já deveria ter sido entregue neste ponto do prazo da "
                      "release. É o percentual do prazo decorrido (PPC) aplicado ao BAC."
        )
    with row1_c3:
        ev_txt = "N/A" if r["ev"] is None else f"R$ {r['ev']:,.2f}"
        render_kpi(
            "EV (Valor Agregado)", ev_txt, "Valor realmente entregue", THEME_COLORS["primary"],
            help_text="Valor do trabalho já entregue e aceito, convertido em reais pela fração do "
                      "escopo concluído (APC) aplicada ao BAC. Mede o que foi produzido, não o que "
                      "foi gasto. Sem pontos estimados, não pode ser calculado."
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    row2_c1, row2_c2, row2_c3 = st.columns(3)
    with row2_c1:
        spi = r["spi"]
        spi_color = THEME_COLORS["accent"] if spi is None else (THEME_COLORS["secondary"] if spi >= 1.0 else THEME_COLORS["danger"])
        render_kpi(
            "SPI (Cronograma)", "N/A" if spi is None else f"{spi:.2f}", "EV ÷ PV, referência 1.0", spi_color,
            help_text="SPI = EV ÷ PV. Compara o valor entregue com o que deveria ter sido entregue "
                      "até este ponto do prazo. Abaixo de 1.0, entregou-se menos do que o planejado "
                      "para esta fase; acima de 1.0, mais."
        )
    with row2_c2:
        cpi = r["cpi"]
        cpi_color = THEME_COLORS["accent"] if cpi is None else (THEME_COLORS["secondary"] if cpi >= 1.0 else THEME_COLORS["danger"])
        render_kpi(
            "CPI (Custo)", "N/A" if cpi is None else f"{cpi:.2f}", "EV ÷ AC, AC estimado", cpi_color,
            help_text="CPI = EV ÷ AC. Compara o valor entregue com o quanto foi gasto para "
                      "entregá-lo. Aqui o AC é estimado pela linha de base de custo, então o CPI "
                      "coincide com o SPI até que haja custo real apurado."
        )
    with row2_c3:
        apc_txt = f"{r['rpc']:.0f} de {r['prp']:.0f} SP"
        render_kpi(
            "Escopo Entregue", apc_txt, "RPC de PRP, em pontos de história", THEME_COLORS["secondary"],
            help_text="Pontos de história entregues (RPC) sobre os pontos planejados para a "
                      "release (PRP). O PRP só é confiável quando todas as histórias estão estimadas."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    visiveis = releases
    st.markdown("#### Planejado, Entregue e Custo por Release")
    fig_rel = go.Figure()
    fig_rel.add_trace(go.Bar(
        x=[x["id"] for x in visiveis], y=[x["pv"] for x in visiveis], name="PV (Planejado)",
        marker=dict(color="#94A3B8"),
        hovertemplate="<b>%{x}</b><br>Planejado: R$ %{y:,.2f}<extra></extra>"
    ))
    fig_rel.add_trace(go.Bar(
        x=[x["id"] for x in visiveis], y=[x["ev"] for x in visiveis], name="EV (Entregue)",
        marker=dict(color="#38BDF8"),
        hovertemplate="<b>%{x}</b><br>Entregue: R$ %{y:,.2f}<extra></extra>"
    ))
    fig_rel.add_trace(go.Bar(
        x=[x["id"] for x in visiveis], y=[x["ac"] for x in visiveis], name="AC (Custo estimado)",
        marker=dict(color="#FBBF24"),
        hovertemplate="<b>%{x}</b><br>Custo estimado: R$ %{y:,.2f}<extra></extra>"
    ))
    fig_rel.update_layout(_layout_barras("PV, EV e AC por Release", "R$", 400))
    st.plotly_chart(fig_rel, use_container_width=True, config=PLOTLY_CONFIG)
    with st.expander("O que este gráfico mostra?"):
        st.markdown(
            "Para cada release que já começou, a barra cinza é o valor que deveria estar entregue "
            "(PV), a azul é o valor realmente entregue (EV) e a amarela é o custo estimado (AC). "
            "Quando o EV fica abaixo do PV, entregou-se menos do que o planejado até aquele ponto. "
            "Uma release sem barra azul ainda não tem pontos estimados para calcular o EV."
        )

    com_indice = [x for x in visiveis if x["spi"] is not None]
    st.markdown("#### Índices de Desempenho SPI e CPI por Release")
    if com_indice:
        fig_idx = go.Figure()
        fig_idx.add_trace(go.Bar(
            x=[x["id"] for x in com_indice], y=[x["spi"] for x in com_indice], name="SPI (Cronograma)",
            marker=dict(color="#FBBF24"),
            hovertemplate="<b>%{x}</b><br>SPI: %{y:.2f}<extra></extra>"
        ))
        fig_idx.add_trace(go.Bar(
            x=[x["id"] for x in com_indice], y=[x["cpi"] for x in com_indice], name="CPI (Custo)",
            marker=dict(color="#34D399"),
            hovertemplate="<b>%{x}</b><br>CPI: %{y:.2f}<extra></extra>"
        ))
        fig_idx.add_hline(y=1.0, line_dash="dot", line_color="#94A3B8", annotation_text="Referência (1.0)")
        fig_idx.update_layout(_layout_barras("SPI e CPI por Release", "Índice", 380))
        st.plotly_chart(fig_idx, use_container_width=True, config=PLOTLY_CONFIG)
    else:
        st.info("Nenhuma release tem pontos estimados suficientes para calcular SPI e CPI.")
    with st.expander("O que este gráfico mostra?"):
        st.markdown(
            "SPI (prazo) e CPI (custo) são acompanhados separadamente porque um projeto pode estar "
            "bem em um e comprometido no outro. A linha pontilhada em 1.0 é a referência neutra. "
            "Com o AC estimado pela linha de base, os dois índices coincidem; eles só passam a "
            "divergir quando o custo real for registrado."
        )

    serie = r["serie"]
    st.markdown(f"#### Burnup e Burndown de Pontos da {r['id']}")
    if serie:
        rotulos = [p["sprint"] for p in serie]
        fig_up = go.Figure()
        fig_up.add_trace(go.Scatter(
            x=rotulos, y=[p["entregue_acum"] for p in serie], name="Pontos entregues (acumulado)",
            mode="lines+markers", fill="tozeroy", fillcolor="rgba(56, 189, 248, 0.15)",
            line=dict(color="#38BDF8", width=3),
            hovertemplate="<b>%{x}</b><br>Entregues: %{y:.0f} SP<extra></extra>"
        ))
        fig_up.add_hline(y=r["prp"], line_dash="dash", line_color="#94A3B8",
                         annotation_text=f"Escopo planejado (PRP): {r['prp']:.0f} SP")
        fig_up.update_layout(get_plotly_layout(f"Burnup de Pontos da {r['id']}", height=360, y_title="Story Points"))
        st.plotly_chart(fig_up, use_container_width=True, config=PLOTLY_CONFIG)

        fig_down = go.Figure()
        fig_down.add_trace(go.Scatter(
            x=rotulos, y=[p["restante_ideal"] for p in serie], name="Restante ideal",
            mode="lines+markers", line=dict(color="#94A3B8", width=2.5, dash="dash"),
            hovertemplate="<b>%{x}</b><br>Deveria restar: %{y:.0f} SP<extra></extra>"
        ))
        fig_down.add_trace(go.Scatter(
            x=rotulos, y=[p["restante"] for p in serie], name="Restante real",
            mode="lines+markers", fill="tozeroy", fillcolor="rgba(248, 113, 113, 0.15)",
            line=dict(color="#F87171", width=3),
            hovertemplate="<b>%{x}</b><br>Falta entregar: %{y:.0f} SP<extra></extra>"
        ))
        fig_down.update_layout(get_plotly_layout(f"Burndown de Pontos da {r['id']}", height=360, y_title="Story Points"))
        st.plotly_chart(fig_down, use_container_width=True, config=PLOTLY_CONFIG)
        with st.expander("O que estes gráficos mostram?"):
            st.markdown(
                "O burnup acumula os pontos entregues sprint a sprint e a linha tracejada marca o "
                "escopo planejado da release (PRP). O burndown é o espelho: quanto ainda falta "
                "entregar, comparado com o ritmo ideal para terminar no fim do prazo. Se o PRP "
                "mudar, as duas curvas se ajustam."
            )
    else:
        st.info("Nenhuma sprint termina dentro desta release até agora.")

    st.markdown("#### Histórico de Velocity")
    fechadas = [s for s in velocity_sprints if s.get("status") == "CLOSED"]
    if fechadas:
        fig_vel = go.Figure(go.Bar(
            x=[s["name"] for s in fechadas],
            y=[s["delivered_sp"] for s in fechadas],
            marker=dict(
                color=["#38BDF8" if i % 2 == 0 else "#0284C7" for i in range(len(fechadas))],
                line=dict(color="rgba(255, 255, 255, 0.3)", width=1)
            ),
            text=[f"{s['delivered_sp']:.0f} SP" for s in fechadas],
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>Entregue: %{y} SP<extra></extra>"
        ))
        fig_vel.update_layout(get_plotly_layout("Velocity por Sprint (Story Points Entregues)", height=360, y_title="Story Points"))
        st.plotly_chart(fig_vel, use_container_width=True, config=PLOTLY_CONFIG)
        media = sum(s["delivered_sp"] for s in fechadas) / len(fechadas)
        st.caption(f"Média das sprints fechadas: {media:.1f} SP por sprint.")
    else:
        st.info("Ainda não há sprints fechadas para calcular a velocity.")
    with st.expander("O que este gráfico mostra?"):
        st.markdown(
            "Quantos pontos de história cada sprint fechada entregou. Uma sprint com poucos pontos "
            "não é necessariamente ruim: pode refletir histórias maiores do que o normal, feriados, "
            "ou trabalho técnico que não gera pontos diretamente. Se as histórias não foram "
            "estimadas, a velocity aparece zerada e deixa de refletir o trabalho feito."
        )

    st.markdown("### Tabela de Auditoria e Rastreabilidade do Agile EVM")
    st.dataframe(evm["audit_df"], use_container_width=True, hide_index=True)

    csv_data = evm["audit_df"].to_csv(index=False, sep=";", encoding="utf-8-sig")
    st.download_button(
        label="Exportar Tabela de Auditoria (CSV)",
        data=csv_data,
        file_name=f"auditoria_evm_{PROJECT_PREFIX.lower()}_{agora_brasilia().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.markdown("### Parecer Técnico e Análise da Sprint")
    os.makedirs(ANALYSIS_NOTES_DIR, exist_ok=True)
    
    hoje_str = agora_brasilia().strftime("%Y-%m-%d")
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
        render_kpi(
            "Total de Riscos", str(total_r), "Mapeados no projeto", THEME_COLORS["primary"],
            help_text="Quantidade de riscos formalmente registrados no plano de riscos. Um número "
                      "baixo não significa projeto sem risco: pode significar mapeamento incompleto."
        )
    with r2:
        render_kpi(
            "Riscos Críticos", str(crit_r), "Severidade ≥ 16", THEME_COLORS["danger"] if crit_r > 0 else THEME_COLORS["secondary"],
            help_text="Riscos com severidade (probabilidade × impacto) ≥ 16, o canto superior direito "
                      "da matriz. Segundo o plano de riscos, exigem ação preventiva ativa, não apenas "
                      "monitoramento passivo."
        )
    with r3:
        render_kpi(
            "Riscos Altos", str(alto_r), "Severidade 10 a 15", THEME_COLORS["warning"],
            help_text="Severidade entre 10 e 15. Merecem plano de mitigação acompanhado, mas sem a "
                      "mesma urgência dos críticos."
        )
    with r4:
        render_kpi(
            "Severidade Média", str(media_sev), "Média ponderada (P×I)", THEME_COLORS["accent"],
            help_text="Média aritmética simples da severidade de todos os riscos mapeados. É um "
                      "indicador geral de quão pesada é a carteira de riscos como um todo. Não "
                      "substitui olhar os riscos críticos individualmente."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_matriz, col_cat = st.columns([1.35, 1.0])

    with col_matriz:
        st.caption("🟢 Baixo (1–5) · 🟡 Médio (6–12) · 🟠 Alto (15–16) · 🔴 Crítico (20–25). Severidade = probabilidade × impacto")
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

    with st.expander("O que estes gráficos mostram?"):
        st.markdown(
            "**Matriz de Probabilidade × Impacto:** cruza a chance de o risco acontecer (linhas) com "
            "a gravidade se ele acontecer (colunas). Quanto mais próximo do canto superior direito, "
            "maior a severidade combinada. A cor de fundo de cada célula é fixa: mostra a faixa de "
            "severidade daquela combinação. Os IDs escritos dentro são os riscos que caem ali, não "
            "uma contagem.\n\n"
            "**Distribuição por Categoria:** mostra se a carteira de riscos está concentrada numa "
            "única frente (ex: só Técnico) ou espalhada entre Produto, Equipe, Infraestrutura etc. "
            "Útil para saber se o time de gestão de risco precisa de outros olhares além do técnico."
        )

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
        render_kpi(
            "Linhas de Código", f"{metrics['ncloc']:,}", "ncloc", THEME_COLORS["primary"],
            help_text="Linhas de código executável analisadas pelo SonarCloud (não conta comentários "
                      "nem linhas em branco). É uma medida de tamanho do projeto, não de qualidade."
        )
    with q2:
        cobertura = metrics.get("coverage")
        cobertura_txt = f"{cobertura:.1f}%" if cobertura is not None else "N/A"
        cobertura_sub = "Cobertura de testes" if cobertura is not None else "Sem testes apurados ainda"
        render_kpi(
            "Cobertura", cobertura_txt, cobertura_sub, THEME_COLORS["secondary"],
            help_text="Percentual do código exercitado por testes automatizados. Mede a superfície "
                      "testada, não garante ausência de bugs: código coberto também pode ter "
                      "asserções fracas ou testes que não checam o comportamento certo."
        )
    with q3:
        gate = metrics.get("quality_gate") or "N/A"
        gate_color = THEME_COLORS["secondary"] if gate == "OK" else (THEME_COLORS["danger"] if gate == "ERROR" else THEME_COLORS["accent"])
        render_kpi(
            "Quality Gate", gate, "Estado do portão de qualidade", gate_color,
            help_text="Selo geral do SonarCloud que resume se o código atende aos critérios mínimos "
                      "configurados (bugs, cobertura, duplicidade etc.) num único veredito. É um "
                      "agregado, não substitui olhar as métricas individuais abaixo."
        )
    with q4:
        render_kpi(
            "Débito Técnico", f"{metrics['technical_debt_min']} min", "Tempo estimado de correção", THEME_COLORS["warning"],
            help_text="Tempo estimado pelo próprio SonarCloud para corrigir todos os problemas de "
                      "manutenibilidade apontados na análise. É uma estimativa da ferramenta, não uma "
                      "medição direta do esforço real da equipe."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### Achados Estáticos")
    fig_issues = go.Figure(go.Bar(
        x=["Bugs", "Vulnerabilidades", "Code Smells", "Security Hotspots"],
        y=[metrics["bugs"], metrics["vulnerabilities"], metrics["code_smells"], metrics["security_hotspots"]],
        marker=dict(color=["#F87171", "#FB923C", "#FBBF24", "#A78BFA"]),
        text=[metrics["bugs"], metrics["vulnerabilities"], metrics["code_smells"], metrics["security_hotspots"]],
        textposition="auto",
        hovertemplate="<b>%{x}</b><br>Ocorrências: %{y}<extra></extra>"
    ))
    fig_issues.update_layout(get_plotly_layout(f"Achados Estáticos — {REPOS_CONFIG[repo_key]['name']}", height=360, y_title="Ocorrências"))
    st.plotly_chart(fig_issues, use_container_width=True, config=PLOTLY_CONFIG)
    with st.expander("O que cada tipo de achado significa?"):
        st.markdown(
            "- **Bugs**: trechos que o SonarCloud considera erros prováveis em tempo de execução.\n"
            "- **Vulnerabilidades**: brechas de segurança já confirmadas pela análise estática.\n"
            "- **Code Smells**: más práticas que não quebram o sistema, mas dificultam manutenção "
            "futura (ex: função grande demais, duplicação de lógica).\n"
            "- **Security Hotspots**: trechos sensíveis que merecem revisão manual; nem todo hotspot "
            "é uma vulnerabilidade real, é um convite para o time olhar com atenção."
        )

    st.markdown("#### Notas de Avaliação")
    st.caption(
        "Escala do SonarCloud: **A** é a melhor nota (menor risco) e **E** a pior. Cada nota reflete "
        "o pior problema não corrigido daquela categoria, não uma média."
    )
    n1, n2, n3 = st.columns(3)
    with n1:
        render_kpi(
            "Manutenibilidade", rating_to_letter(metrics.get("maintainability_rating")), "Sqale Rating", THEME_COLORS["primary"],
            help_text="Avalia o esforço para evoluir o código no futuro, com base nos Code Smells "
                      "encontrados e no débito técnico estimado para corrigi-los."
        )
    with n2:
        render_kpi(
            "Confiabilidade", rating_to_letter(metrics.get("reliability_rating")), "Reliability Rating", THEME_COLORS["primary"],
            help_text="Avalia a chance de o código apresentar bugs em produção, com base na "
                      "gravidade dos Bugs encontrados pela análise estática."
        )
    with n3:
        render_kpi(
            "Segurança", rating_to_letter(metrics.get("security_rating")), "Security Rating", THEME_COLORS["primary"],
            help_text="Avalia a exposição a vulnerabilidades de segurança, com base na gravidade das "
                      "Vulnerabilidades encontradas pela análise estática."
        )

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
        st.caption(
            "Cada ponto é uma coleta da esteira de CI/CD, não uma sprint. Com poucos pontos "
            "acumulados, a tendência ainda não é estatisticamente significativa."
        )

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
        "Coletado em": formatar_data_brasilia(metrics.get("collected_at"))
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
        render_kpi(
            "Taxa de Sucesso CI/CD", f"{runs_data['success_rate']}%", "Builds sem erro", THEME_COLORS["secondary"],
            help_text="Percentual de execuções da esteira (GitHub Actions) que terminaram sem erro. "
                      "Mede a estabilidade do processo de integração, não a qualidade do código "
                      "entregue. Uma esteira estável pode conviver com código de baixa qualidade."
        )
    with p2:
        render_kpi(
            "Tempo Mediano de Execução", f"{runs_data['median_duration_min']} min", "Mediana da duração das execuções", THEME_COLORS["primary"],
            help_text="Valor central da duração das execuções da esteira, do início ao fim. Usa a "
                      "mediana porque poucas execuções atípicas (como um deploy que ficou horas "
                      "aguardando) distorceriam a média. Quanto menor, mais rápido o time descobre "
                      "se uma mudança quebrou algo."
        )
    with p3:
        render_kpi(
            "Total de Builds Monitoradas", str(runs_data['total_runs']), "Execuções rastreadas", THEME_COLORS["accent"],
            help_text="Quantidade de execuções já registradas nas fontes de dados coletadas. Cresce "
                      "com o tempo; serve mais como contexto de volume do que como indicador isolado "
                      "de desempenho."
        )

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
            fillcolor="rgba(56, 189, 248, 0.12)",
            hovertemplate="<b>%{x}</b><br>Duração: %{y:.1f} min<extra></extra>"
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

    with st.expander("O que estes gráficos mostram?"):
        st.markdown(
            "**Tempo de Resposta:** duração das últimas execuções, ordenadas por data de início. Picos "
            "pontuais costumam ser normais (dependências reinstaladas, cache frio); uma tendência de "
            "alta sustentada ao longo de várias execuções é o sinal que vale investigar. O indicador "
            "acima usa a mediana de todas as execuções, que não é afetada por execuções atípicas.\n\n"
            "**Estabilidade:** proporção de execuções com sucesso versus falha em todo o histórico "
            "coletado até agora. Não reflete só as execuções recentes do gráfico ao lado."
        )


def render_theory_tab():
    """Memória de cálculo e critérios formais."""
    st.markdown("### Fundamentação Teórica e Critérios Acadêmicos")
    st.markdown(r"""
    A formulação do **Agile EVM** segue o modelo de **Sulaiman, Barton e Blackburn (2006)** (*"AgileEVM - Earned Value Management in Scrum Projects"*), aplicado **por release**:

    1. **BAC (Budget at Completion)**: orçamento da release, do Plano de Custos.
    2. **PRP (Planned Release Points)**: pontos de história planejados para a release, somados nas sprints que terminam nela.
    3. **PPC (Planned Percent Complete)**: fração dos dias da release já decorrida:
       $$PPC = \frac{\text{dias decorridos}}{\text{dias da release}}$$
    4. **APC (Actual Percent Complete)**: fração do escopo concluído, com $RPC$ os pontos entregues:
       $$APC = \frac{RPC}{PRP}$$
    5. **PV (Planned Value)**: $PV = PPC \times BAC$
    6. **EV (Earned Value)**: $EV = APC \times BAC$
    7. **AC (Actual Cost)**: custo incorrido. Sem custo real apurado, é estimado por $AC = PPC \times BAC$.
    8. **SPI (Schedule Performance Index)**: $SPI = \frac{EV}{PV}$
    9. **CPI (Cost Performance Index)**: $CPI = \frac{EV}{AC}$
    10. **SV e CV**: $SV = EV - PV$ e $CV = EV - AC$
    11. **ETC e EAC**: $ETC = \frac{BAC - EV}{CPI}$ e $EAC = AC + ETC$

    **Hipóteses e limites:** o BAC de cada release é provisório e segue o Plano de Custos. O PRP depende de todas as histórias estarem estimadas no ZenHub. Cada sprint é atribuída à release em que termina. Como o AC é estimado, o CPI coincide com o SPI até que o custo real seja registrado.
    """)


def main():
    apply_custom_theme()
    render_header()
    
    render_sidebar()
    
    sprints_all, is_sprints_mock = get_zenhub_sprints_data()
    sprints_data = filter_started_sprints(sprints_all)
    risks_data, is_risks_mock = get_risks_data()
    sonar_data, is_sonar_mock = get_sonar_metrics_data()

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
    
    evm_results = compute_release_evm(sprints=sprints_all, releases=RELEASES)

    tab_evm, tab_riscos, tab_processo, tab_qualidade, tab_teoria = st.tabs([
        "Agile EVM e Velocity",
        "Gestão de Riscos",
        "Processo e CI/CD",
        "Qualidade de Produto",
        "Memória de Cálculo"
    ])

    with tab_evm:
        render_evm_tab(evm_results, sprints_data, is_sprints_mock)

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