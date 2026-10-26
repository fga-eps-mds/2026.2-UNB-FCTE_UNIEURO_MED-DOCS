import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from src.aceitacao import pontos_entregues
from src.config import (
    MODO_ACEITAS,
    MODO_ENTREGUES,
    MODO_PADRAO,
    ORGANIZATION,
    PROJECT_PREFIX,
    RELEASES,
    ANALYSIS_NOTES_DIR,
    ROTULOS_MODO,
    ROTULOS_IMPACTO,
    ROTULOS_PROBABILIDADE,
    FAIXAS_RISCO,
    THEME_COLORS,
    REPOS_CONFIG
)
from src.theme import apply_custom_theme, render_kpi, get_plotly_layout
from src.data_layer import (
    get_zenhub_sprints_data,
    get_risks_data,
    get_risks_history,
    get_github_runs_data,
    get_sonar_metrics_data,
    get_qrapids_data,
    get_latest_collection_timestamp
)
from src.metrics import (
    compute_release_evm,
    process_risks_summary,
    revisoes_realizadas,
    tabela_historico_riscos,
)
from src.processo import INDICADORES
from src.qualidade import BRASILIA, FAIXA_ADEQUADA, FAIXA_ATENCAO, METRICAS, QUEDA_RELEVANTE, faixa
from src.templates import (
    aviso_modo_entregues,
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


def render_sidebar() -> str:
    """
    Barra lateral: a escolha do que conta como ponto entregue e os metadados do projeto.
    Devolve o modo escolhido, que vale para EVM, velocity, burnup, burndown e processo.
    """
    st.sidebar.markdown("### Pontos entregues")
    modos = list(ROTULOS_MODO)
    modo = st.sidebar.radio(
        "O que conta como entregue:",
        options=modos,
        index=modos.index(MODO_PADRAO),
        format_func=lambda m: ROTULOS_MODO[m],
        key="modo_pontos",
        help="Uma história só é fechada depois do aceite do PO. \"Somente aceitas\" conta só as "
             "fechadas. \"Aceitas + em Aceitação PO\" conta também as da coluna Aceitação PO do "
             "ZenHub: o código foi entregue e o aceite está pendente. A escolha vale para o EVM, "
             "a velocity, o burnup, o burndown e os indicadores de processo."
    )
    st.sidebar.caption("Os dois valores aparecem sempre separados nas tabelas e nos cartões.")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Governança do Projeto")
    st.sidebar.info(f"**Organização:** `{ORGANIZATION}`\n\n**Projeto:** `{PROJECT_PREFIX}`")

    st.sidebar.markdown("---")
    st.sidebar.caption("Repositórios Integrados:\n- `-DOCS` (Documentação e Analytics)\n- `-IA` (Módulo de Inteligência Artificial)\n- `-APP` (Aplicação Mobile)")
    return modo


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


def _rotulo_em_frase(modo: str) -> str:
    """Rótulo do modo no meio de uma frase: só a primeira letra vira minúscula, para "PO" continuar "PO"."""
    rotulo = ROTULOS_MODO[modo]
    return rotulo[0].lower() + rotulo[1:]


def _render_aviso_do_modo(r: dict, modo: str):
    """Diz qual modo de pontos está valendo e quanto ele soma, para ninguém ler o número sem saber a regra."""
    em_aceitacao = len(r["em_aceitacao"])
    if r["aceitacao_fonte"] is None:
        st.warning(
            "A coluna Aceitação PO ainda não foi coletada do ZenHub, então os dois modos mostram o mesmo "
            "valor: só as histórias aceitas. Ela passa a aparecer na próxima coleta de métricas."
        )
    elif modo == MODO_ENTREGUES:
        st.info(aviso_modo_entregues(ROTULOS_MODO[modo], r["rpc_aceito"], r["rpc_aguardando"], em_aceitacao))
    else:
        st.caption(
            f"Modo: {_rotulo_em_frase(modo)}. {r['rpc_aguardando']:.0f} SP de {em_aceitacao} história(s) "
            "em Aceitação PO ficam fora da conta. Para incluí-los, mude a opção na barra lateral."
        )


def _render_historias_em_aceitacao(r: dict):
    """Lista as histórias da release que estão em Aceitação PO, para conferir o que entra no modo entregues."""
    historias = r["em_aceitacao"]
    titulo = f"Histórias em Aceitação PO nesta release ({len(historias)}, {r['rpc_aguardando']:.0f} SP)"
    with st.expander(titulo):
        if r["aceitacao_fonte"] is None:
            st.markdown("A coluna Aceitação PO ainda não foi coletada.")
            return
        if not historias:
            st.markdown("Nenhuma história desta release está em Aceitação PO.")
            return
        tabela = pd.DataFrame([
            {"História": f"#{h['numero']}" if h.get("numero") is not None else "sem número",
             "Pontos (SP)": f"{h['estimativa']:.0f}", "Sprint": h.get("sprint") or "-"}
            for h in sorted(historias, key=lambda h: (h.get("numero") is None, h.get("numero") or 0))
        ])
        st.dataframe(tabela, use_container_width=True, hide_index=True)
        origem = "coluna do ZenHub" if r["aceitacao_fonte"] == "zenhub" else "lista manual (`aceitacao_po_manual.json`)"
        st.caption(
            f"Fonte: {origem}. Cada história conta uma vez, na última sprint em que aparece. "
            "História sem estimativa vale 0 ponto."
        )


def render_evm_tab(evm: dict, velocity_sprints: list, is_mock: bool, modo: str = MODO_PADRAO):
    """Renderiza a aba do Agile EVM por release, com burn de pontos e velocity."""
    if is_mock:
        render_mock_alert("Sprints e Agile EVM", "zenhub_analytics.json")

    st.markdown("### Desempenho de Prazo e Custos por Release (Agile EVM)")
    st.caption(
        "O EVM é calculado por release, com o orçamento (BAC) de cada release do Plano de Custos e "
        "os pontos reais do ZenHub. A única escolha é o que conta como ponto entregue (barra lateral): "
        "só as histórias aceitas ou também as que estão em Aceitação PO."
    )

    with st.expander("Como funciona o Agile EVM e como ler os índices"):
        st.markdown(
            "O Agile EVM compara, em reais, o que estava planejado com o que foi entregue e gasto. "
            "Ele é calculado por release porque é a release que tem orçamento e escopo próprios.\n\n"
            "- **BAC:** orçamento da release, vindo do Plano de Custos.\n"
            "- **PRP:** pontos de história planejados para a release, contando cada história uma "
            "só vez mesmo que ela passe de uma sprint para a seguinte.\n"
            "- **RPC:** pontos de história já entregues. Uma história só é fechada depois do aceite do "
            "PO. Por isso o RPC tem duas partes: os pontos **aceitos** (histórias fechadas) e os das "
            "histórias **em Aceitação PO**, com o código entregue e o aceite pendente. A barra lateral "
            "escolhe se a segunda parte entra no RPC e, portanto, no EV, no SPI e no CPI.\n"
            "- **PPC:** fração dos dias da release já decorrida. **APC:** RPC dividido pelo PRP.\n"
            "- **PV** = PPC × BAC, o valor que deveria estar entregue. **EV** = APC × BAC, o valor "
            "realmente entregue. **AC:** custo incorrido.\n"
            "- **SPI** = EV ÷ PV (prazo) e **CPI** = EV ÷ AC (custo). Abaixo de 1,0 há atraso ou "
            "custo acima do valor entregue; acima de 1,0, o contrário.\n\n"
            "**Limitações a considerar na leitura:**\n\n"
            "- O PRP só é confiável se todas as histórias da release estiverem estimadas.\n"
            "- No modo \"somente aceitas\", enquanto o PO não aceita as histórias o RPC fica em zero e "
            "EV, SPI e CPI saem zerados: isso indica espera de aceite e não, necessariamente, atraso do time. "
            "No modo \"aceitas + em Aceitação PO\", o número mostra o trabalho entregue, mas ainda não "
            "validado: uma história pode voltar para desenvolvimento se o PO pedir mudanças.\n"
            "- A coluna Aceitação PO é lida no momento da coleta. Uma história que sai dela (aceita ou "
            "devolvida) muda o número na coleta seguinte.\n"
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

    _render_aviso_do_modo(r, modo)
    sem_entrega = r["prp"] > 0 and r["rpc"] <= 0
    if sem_entrega and not (modo == MODO_ACEITAS and r["rpc_aguardando"] > 0):
        st.info(
            "Nenhuma história desta release foi entregue até agora"
            + (", nem está em Aceitação PO" if modo == MODO_ENTREGUES and r["aceitacao_fonte"] else "")
            + ". Uma história só conta como aceita depois do aceite do PO, então enquanto isso o RPC e o "
            "EV ficam em zero e o SPI e o CPI saem zerados. Isso indica espera de aceite, e não "
            "necessariamente atraso do time."
        )
    if r["prp_aproximado"]:
        st.caption(
            "PRP aproximado: o detalhe por história ainda não foi coletado, então os pontos de uma "
            "história que passou de uma sprint para a seguinte podem estar contados mais de uma vez. "
            "O valor se corrige na próxima coleta de métricas."
        )

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
            "EV (Valor Agregado)", ev_txt,
            "Entregue, incluindo Aceitação PO" if modo == MODO_ENTREGUES else "Entregue e aceito",
            THEME_COLORS["primary"],
            help_text="Valor do trabalho já entregue, convertido em reais pela fração do escopo "
                      "concluído (APC) aplicada ao BAC. No modo \"somente aceitas\" conta só o que o PO "
                      "aceitou; no modo \"aceitas + em Aceitação PO\" conta também o que aguarda o aceite. "
                      "Mede o que foi produzido, não o que foi gasto. Sem pontos estimados, não pode "
                      "ser calculado."
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    row2_c1, row2_c2, row2_c3 = st.columns(3)
    with row2_c1:
        spi = r["spi"]
        spi_color = THEME_COLORS["accent"] if spi is None or sem_entrega else (THEME_COLORS["secondary"] if spi >= 1.0 else THEME_COLORS["danger"])
        render_kpi(
            "SPI (Cronograma)", "N/A" if spi is None else f"{spi:.2f}", "EV ÷ PV, referência 1.0", spi_color,
            help_text="SPI = EV ÷ PV. Compara o valor entregue com o que deveria ter sido entregue "
                      "até este ponto do prazo. Abaixo de 1.0, entregou-se menos do que o planejado "
                      "para esta fase; acima de 1.0, mais."
        )
    with row2_c2:
        cpi = r["cpi"]
        cpi_color = THEME_COLORS["accent"] if cpi is None or sem_entrega else (THEME_COLORS["secondary"] if cpi >= 1.0 else THEME_COLORS["danger"])
        render_kpi(
            "CPI (Custo)", "N/A" if cpi is None else f"{cpi:.2f}", "EV ÷ AC, AC estimado", cpi_color,
            help_text="CPI = EV ÷ AC. Compara o valor entregue com o quanto foi gasto para "
                      "entregá-lo. Aqui o AC é estimado pela linha de base de custo, então o CPI "
                      "coincide com o SPI até que haja custo real apurado."
        )
    with row2_c3:
        apc_txt = f"{r['rpc']:.0f} de {r['prp']:.0f} SP"
        detalhe = (f"{r['rpc_aceito']:.0f} aceitos + {r['rpc_aguardando']:.0f} em aceitação"
                   if modo == MODO_ENTREGUES
                   else f"{r['rpc_aceito']:.0f} aceitos ({r['rpc_aguardando']:.0f} em aceitação fora)")
        render_kpi(
            "Escopo Entregue", apc_txt, detalhe, THEME_COLORS["secondary"],
            help_text="Pontos de história entregues (RPC) sobre os pontos planejados para a "
                      "release (PRP). O RPC separa os pontos aceitos dos que estão em Aceitação PO, e o "
                      "modo da barra lateral escolhe se os segundos entram. O PRP só é confiável quando "
                      "todas as histórias estão estimadas."
        )

    _render_historias_em_aceitacao(r)

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
        if modo == MODO_ENTREGUES:
            fig_up.add_trace(go.Scatter(
                x=rotulos, y=[p["entregue_acum"] for p in serie], name="Aceitos + em aceitação (acumulado)",
                mode="lines+markers", fill="tozeroy", fillcolor="rgba(251, 191, 36, 0.12)",
                line=dict(color="#FBBF24", width=3, dash="dot"),
                hovertemplate="<b>%{x}</b><br>Aceitos + em aceitação: %{y:.0f} SP<extra></extra>"
            ))
        fig_up.add_trace(go.Scatter(
            x=rotulos, y=[p["aceito_acum"] for p in serie], name="Pontos aceitos (acumulado)",
            mode="lines+markers", fill="tozeroy", fillcolor="rgba(56, 189, 248, 0.15)",
            line=dict(color="#38BDF8", width=3),
            hovertemplate="<b>%{x}</b><br>Aceitos: %{y:.0f} SP<extra></extra>"
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
                "O burnup acumula os pontos sprint a sprint e a linha tracejada marca o escopo "
                "planejado da release (PRP). A linha azul são os pontos aceitos; no modo \"aceitas + em "
                "Aceitação PO\" aparece também a linha pontilhada com os que aguardam o aceite. O burndown "
                "é o espelho: quanto ainda falta entregar (conforme o modo), comparado com o ritmo ideal "
                "para terminar no fim do prazo. Se o PRP mudar, as duas curvas se ajustam."
            )
    else:
        st.info("Nenhuma sprint termina dentro desta release até agora.")

    st.markdown("#### Histórico de Velocity")
    # Sprint em andamento só entra quando já tem pontos entregues no modo escolhido: antes disso
    # a barra seria uma sprint vazia, e não uma velocidade.
    def _pontos(sprint):
        return pontos_entregues(sprint["delivered_sp"], sprint.get("aguardando_pontos", 0.0), modo)

    fechadas = [s for s in velocity_sprints if s.get("status") == "CLOSED"]
    em_andamento = [s for s in velocity_sprints if s.get("status") != "CLOSED" and _pontos(s) > 0]
    barras = fechadas + (em_andamento if modo == MODO_ENTREGUES else [])
    if barras:
        rotulos_vel = [s["name"] + ("" if s in fechadas else " (em andamento)") for s in barras]
        fig_vel = go.Figure()
        fig_vel.add_trace(go.Bar(
            x=rotulos_vel, y=[s["delivered_sp"] for s in barras], name="Aceitos",
            marker=dict(color="#38BDF8"),
            text=[f"{s['delivered_sp']:.0f}" for s in barras], textposition="inside",
            hovertemplate="<b>%{x}</b><br>Aceitos: %{y} SP<extra></extra>"
        ))
        if modo == MODO_ENTREGUES:
            fig_vel.add_trace(go.Bar(
                x=rotulos_vel, y=[s.get("aguardando_pontos", 0.0) for s in barras], name="Em Aceitação PO",
                marker=dict(color="#FBBF24", pattern=dict(shape="/")),
                text=[f"{s.get('aguardando_pontos', 0.0):.0f}" for s in barras], textposition="inside",
                hovertemplate="<b>%{x}</b><br>Em Aceitação PO: %{y} SP<extra></extra>"
            ))
        layout_vel = get_plotly_layout("Velocity por Sprint (Story Points Entregues)", height=380, y_title="Story Points")
        layout_vel["barmode"] = "stack"
        layout_vel["legend"]["y"] = -0.25
        fig_vel.update_layout(layout_vel)
        st.plotly_chart(fig_vel, use_container_width=True, config=PLOTLY_CONFIG)
        if fechadas:
            media = sum(_pontos(s) for s in fechadas) / len(fechadas)
            st.caption(f"Média das sprints fechadas ({_rotulo_em_frase(modo)}): {media:.1f} SP por sprint.")
    else:
        st.info("Ainda não há sprints fechadas para calcular a velocity.")
    with st.expander("O que este gráfico mostra?"):
        st.markdown(
            "Quantos pontos de história cada sprint fechada entregou. A parte azul são os pontos aceitos e, "
            "no modo \"aceitas + em Aceitação PO\", a parte listrada são as histórias que aguardam o "
            "aceite; sprints em andamento aparecem só quando já têm pontos nesse modo. Uma sprint com poucos pontos "
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


def _data_br(iso: str) -> str:
    """AAAA-MM-DD para DD/MM/AAAA."""
    try:
        return datetime.fromisoformat(iso).strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        return str(iso)


def render_risks_tab(risks_raw: list, is_mock: bool, historico: dict = None):
    """Renderiza a aba de Gestão de Riscos com a escala única do plano de riscos."""
    if is_mock:
        render_mock_alert("Matriz de Riscos", "riscos_analytics.json")

    historico = historico or {"revisoes": [], "ocorrencias": []}
    ocorrencias = historico.get("ocorrencias", [])

    st.markdown("### Matriz de Exposição e Governança de Riscos")

    df_risks = process_risks_summary(risks_raw, ocorrencias)
    faixa = {grau: f"{minimo} a {maximo}" for minimo, maximo, grau in FAIXAS_RISCO}

    r1, r2, r3, r4 = st.columns(4)
    total_r = len(df_risks)
    elev_r = len(df_risks[df_risks["Grau"] == "Elevado"])
    medio_r = len(df_risks[df_risks["Grau"] == "Médio"])
    conc_r = len({o["risco"] for o in ocorrencias})

    with r1:
        render_kpi(
            "Total de Riscos", str(total_r), "Mapeados no projeto", THEME_COLORS["primary"],
            help_text="Quantidade de riscos formalmente registrados no plano de riscos. Um número "
                      "baixo não significa projeto sem risco: pode significar mapeamento incompleto."
        )
    with r2:
        render_kpi(
            "Riscos Elevados", str(elev_r), f"Severidade {faixa['Elevado']}",
            THEME_COLORS["danger"] if elev_r > 0 else THEME_COLORS["secondary"],
            help_text="Riscos de grau Elevado na escala do plano de riscos (probabilidade × impacto "
                      "de 15 a 25). Exigem ação preventiva ativa, não apenas monitoramento."
        )
    with r3:
        render_kpi(
            "Riscos Médios", str(medio_r), f"Severidade {faixa['Médio']}", THEME_COLORS["warning"],
            help_text="Riscos de grau Médio na escala do plano (6 a 12). Merecem plano de mitigação "
                      "acompanhado a cada sprint."
        )
    with r4:
        render_kpi(
            "Concretizados", str(conc_r), "Riscos que já ocorreram", THEME_COLORS["accent"],
            help_text="Riscos que deixaram de ser hipótese e aconteceram. O impacto e a resposta "
                      "aplicada estão registrados abaixo e no plano de riscos."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_matriz, col_cat = st.columns([1.35, 1.0])

    with col_matriz:
        st.caption(f"🟢 Baixo ({faixa['Baixo']}) · 🟡 Médio ({faixa['Médio']}) · 🔴 Elevado "
                   f"({faixa['Elevado']}). Severidade = probabilidade × impacto, escala do plano de riscos")
        z_scores = [
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],
            [3, 6, 9, 12, 15],
            [4, 8, 12, 16, 20],
            [5, 10, 15, 20, 25]
        ]
        fig_heat = go.Figure(data=go.Heatmap(
            z=z_scores,
            x=[f"{n} ({rotulo})" for n, rotulo in enumerate(ROTULOS_IMPACTO, start=1)],
            y=[f"{n} ({rotulo})" for n, rotulo in enumerate(ROTULOS_PROBABILIDADE, start=1)],
            # Faixas discretas, as mesmas de FAIXAS_RISCO: a cor muda só onde o grau muda
            # (5→6 e 12→15), nunca em degradê. A posição é (severidade - 1) / 24.
            colorscale=[
                [0.0, "rgba(52, 211, 153, 0.35)"], [0.19, "rgba(52, 211, 153, 0.35)"],
                [0.19, "rgba(251, 191, 36, 0.45)"], [0.52, "rgba(251, 191, 36, 0.45)"],
                [0.52, "rgba(239, 68, 68, 0.6)"], [1.0, "rgba(239, 68, 68, 0.6)"],
            ],
            zmin=1,
            zmax=25,
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

    st.markdown("#### Riscos concretizados")
    if not ocorrencias:
        st.caption("Nenhum risco concretizado registrado em `riscos_historico.json`.")
    for o in ocorrencias:
        with st.container(border=True):
            st.markdown(f"**{o['risco']}** · ocorreu em {_data_br(o['data'])} ({o.get('sprint', '—')}, {o.get('release', '—')})")
            st.markdown(f"{o.get('descricao', '')}\n\n**Impacto:** {o.get('impacto', '—')}\n\n"
                        f"**Resposta aplicada:** {o.get('resposta', '—')}")

    st.markdown("#### Histórico de revisões por sprint")
    revisoes = revisoes_realizadas(historico.get("revisoes", []))
    if not revisoes:
        st.caption("Nenhuma revisão de riscos registrada ainda.")
        return
    st.caption("Só entram sprints que já aconteceram: cada coluna é a revisão feita na sprint review. "
               "Formato: probabilidade × impacto = severidade (grau).")
    st.dataframe(tabela_historico_riscos(revisoes), use_container_width=True, hide_index=True)


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


def _legenda_do_modo(modo: str, em_aceitacao: float):
    """Nas abas de processo, lembra a regra dos pontos entregues e quanto dela vem de Aceitação PO."""
    texto = f"Pontos entregues: {_rotulo_em_frase(modo)} (opção da barra lateral)."
    if modo == MODO_ENTREGUES and em_aceitacao > 0:
        texto += f" Inclui {em_aceitacao:.0f} SP de histórias em Aceitação PO, com o aceite pendente."
    elif modo == MODO_ACEITAS and em_aceitacao > 0:
        texto += f" {em_aceitacao:.0f} SP em Aceitação PO ficam de fora."
    st.caption(texto)


def _render_qrapids_processo(processo_dados: dict, modo: str = MODO_PADRAO):
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

    _legenda_do_modo(modo, item.get("pontos_em_aceitacao", 0.0))
    if item["em_andamento"]:
        st.caption("Release em andamento: P2, P3 e a velocidade mudam até o fim das sprints.")
    ci = item["execucoes"]
    if ci:
        st.caption(f"CI: {ci['success']} de {ci['success'] + ci['failure']} execuções concluídas terminaram com sucesso (APP e IA).")
    if valores["P2"] == 0:
        if modo == MODO_ENTREGUES:
            st.info(
                "Nenhum ponto de história foi entregue nem está em Aceitação PO nas sprints desta release, "
                "então P2 e a velocidade ficam em zero."
            )
        else:
            st.info(
                "Nenhum ponto de história foi aceito pelo PO nas sprints desta release. Sem o aceite a "
                "história não conta como aceita, então P2 e a velocidade ficam em zero. É o mesmo efeito "
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


def _render_qrapids_comparativo(comparativo: dict, modo: str = MODO_PADRAO):
    """Comparação entre releases de velocidade, cobertura e defeitos, como pede o DA-R2."""
    if not comparativo:
        st.info("Ainda não há dados de nenhuma release para comparar.")
        return

    ids = list(comparativo)
    _legenda_do_modo(modo, sum(item.get("pontos_em_aceitacao", 0.0) for item in comparativo.values()))
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
            "A velocidade é zero porque nenhuma história foi "
            + ("entregue nem está em Aceitação PO." if modo == MODO_ENTREGUES else "aceita pelo PO.")
            + " Os pontos planejados por sprint mostram o tamanho do que ainda não foi concluído."
        )

    col_a, col_b = st.columns(2)
    with col_a:
        fig_vel = go.Figure()
        fig_vel.add_trace(go.Bar(
            x=ids, y=velocidades,
            name="Velocidade (entregues)" if modo == MODO_ENTREGUES else "Velocidade (aceitos)",
            marker_color=THEME_COLORS["secondary"],
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


def render_qrapids_tab(dados: dict, modo: str = MODO_PADRAO):
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
        _render_qrapids_processo(dados["processo"], modo)
    with aba_comparativo:
        _render_qrapids_comparativo(dados["comparativo"], modo)


def render_theory_tab():
    """Memória de cálculo e critérios formais."""
    st.markdown("### Fundamentação Teórica e Critérios Acadêmicos")
    st.markdown(r"""
    A formulação do **Agile EVM** segue o modelo de **Sulaiman, Barton e Blackburn (2006)** (*"AgileEVM - Earned Value Management in Scrum Projects"*), aplicado **por release**:

    1. **BAC (Budget at Completion)**: orçamento da release, do Plano de Custos.
    2. **PRP (Planned Release Points)**: pontos de história planejados para a release, contando cada história uma só vez entre as sprints que terminam nela.
    3. **PPC (Planned Percent Complete)**: fração dos dias da release já decorrida:
       $$PPC = \frac{\text{dias decorridos}}{\text{dias da release}}$$
    4. **APC (Actual Percent Complete)**: fração do escopo concluído, com $RPC$ os pontos entregues (os das histórias aceitas e, conforme o modo escolhido na barra lateral, também os das que estão em Aceitação PO):
       $$APC = \frac{RPC}{PRP}$$
    5. **PV (Planned Value)**: $PV = PPC \times BAC$
    6. **EV (Earned Value)**: $EV = APC \times BAC$
    7. **AC (Actual Cost)**: custo incorrido. Sem custo real apurado, é estimado por $AC = PPC \times BAC$.
    8. **SPI (Schedule Performance Index)**: $SPI = \frac{EV}{PV}$
    9. **CPI (Cost Performance Index)**: $CPI = \frac{EV}{AC}$
    10. **SV e CV**: $SV = EV - PV$ e $CV = EV - AC$
    11. **ETC e EAC**: $ETC = \frac{BAC - EV}{CPI}$ e $EAC = AC + ETC$

    **Pontos aceitos e em aceitação:** uma história só é fechada depois do aceite do PO, e o ZenHub só conta como entregue a história fechada. As histórias na coluna Aceitação PO têm o código entregue e o aceite pendente. O painel guarda as duas partes e a barra lateral escolhe se a segunda entra nos pontos entregues; o PRP não muda. Uma história que passa de uma sprint para a seguinte conta uma vez.

    **Hipóteses e limites:** o BAC de cada release é provisório e segue o Plano de Custos. O PRP depende de todas as histórias estarem estimadas no ZenHub. Cada sprint é atribuída à release em que termina. Uma história só conta como entregue depois do aceite do PO. Como o AC é estimado, o CPI coincide com o SPI até que o custo real seja registrado.
    """)


def main():
    apply_custom_theme()
    render_header()
    
    modo = render_sidebar()
    
    sprints_all, is_sprints_mock = get_zenhub_sprints_data()
    sprints_data = filter_started_sprints(sprints_all)
    risks_data, is_risks_mock = get_risks_data()
    risks_history = get_risks_history()
    sonar_data, is_sonar_mock = get_sonar_metrics_data()
    qrapids_data = get_qrapids_data(modo=modo)

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
    
    evm_results = compute_release_evm(sprints=sprints_all, releases=RELEASES, modo=modo)

    tab_evm, tab_riscos, tab_processo, tab_qualidade, tab_qrapids, tab_teoria = st.tabs([
        "Agile EVM e Velocity",
        "Gestão de Riscos",
        "Processo e CI/CD",
        "Qualidade de Produto",
        "Q-Rapids e R1 × R2",
        "Memória de Cálculo"
    ])

    with tab_evm:
        render_evm_tab(evm_results, sprints_data, is_sprints_mock, modo)

    with tab_riscos:
        render_risks_tab(risks_data, is_risks_mock, risks_history)

    with tab_processo:
        render_process_tab()

    with tab_qualidade:
        render_quality_tab(sonar_data, is_sonar_mock)

    with tab_qrapids:
        render_qrapids_tab(qrapids_data, modo)

    with tab_teoria:
        render_theory_tab()


if __name__ == "__main__":
    main()