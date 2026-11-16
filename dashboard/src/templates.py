"""
Templates e Utilitários de Apresentação
Preparado para a evolução modular da Release 2 (DA-R2: Qualidade de Produto Q-Rapids)
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from . import caracteristicas, qualidade
from .config import THEME_COLORS
from .metrics import classificar_indice
from .processo import INDICADORES

def get_status_pill(status: str) -> str:
    """Retorna uma tag visual para status."""
    st_clean = status.lower()
    if "finalizada" in st_clean or "closed" in st_clean:
        return '<span class="badge-pill badge-ok">Finalizada</span>'
    elif "andamento" in st_clean or "active" in st_clean:
        return '<span class="badge-pill badge-warn">Em Andamento</span>'
    else:
        return '<span class="badge-pill badge-info">Planejada</span>'


# ---------------------------------------------------------------------------
# Q-Rapids, processo e comparação R1 x R2 (DA-R2)
# ---------------------------------------------------------------------------

NAO_MEDIDO = "n/m"
INDICES_AGREGADOS = list(qualidade.FATORES) + list(qualidade.CARACTERISTICAS) + [qualidade.INDICE[0]]
_NOMES_AGREGADOS = {**{k: v[0] for k, v in qualidade.FATORES.items()},
                    **{k: v[0] for k, v in qualidade.CARACTERISTICAS.items()},
                    qualidade.INDICE[0]: qualidade.INDICE[1]}

_COR_DA_FAIXA = {
    "Adequado": THEME_COLORS["secondary"],
    "Atenção": THEME_COLORS["warning"],
    "Crítico": THEME_COLORS["danger"],
}


def formatar_indice(valor: Optional[float], parcial: bool = False) -> str:
    """Índice de 0 a 1 com duas casas; valor sem dado é n/m (não medido), nunca 0. `*` marca parcial."""
    if valor is None:
        return NAO_MEDIDO
    return f"{valor:.2f}" + ("*" if parcial else "")


def cor_da_faixa(valor: Optional[float]) -> str:
    """Cor do cartão pela faixa do plano de qualidade; sem dado, a cor neutra."""
    return _COR_DA_FAIXA.get(qualidade.faixa(valor), THEME_COLORS["accent"])


def rotulo_do_marco(nome: str, avaliacao: Dict[str, Any]) -> str:
    return f"{nome} ({avaliacao['versao']})"


def marcos_sem_medida(marcos: Dict[str, Optional[Dict[str, Any]]], agora: datetime) -> List[str]:
    """
    Marcos que já deveriam ter versão medida e não têm: os que já passaram e o da release em
    curso. Um marco futuro sem versão ainda não é falta de dado. Serve para o painel avisar
    que a IA, por exemplo, não tem medição na R2, em vez de mostrar só o que existe.
    """
    futuros = sorted((n for n in qualidade.MARCOS if qualidade.MARCOS[n] > agora), key=qualidade.MARCOS.get)
    em_curso = futuros[0] if futuros else None
    esperados = [n for n in qualidade.MARCOS if qualidade.MARCOS[n] <= agora or n == em_curso]
    return [n for n in esperados if marcos.get(n) is None]


def _nome_curto(descricao: str) -> str:
    """Tira o "Densidade de " inicial dos nomes das métricas, que é o que estoura a coluna da tabela."""
    prefixo = "Densidade de "
    if descricao.startswith(prefixo):
        resto = descricao[len(prefixo):]
        return resto[0].upper() + resto[1:]
    return descricao


def tabela_qrapids(marcos: Dict[str, Optional[Dict[str, Any]]]) -> pd.DataFrame:
    """m1 a m8, fatores, características e Q, com uma coluna por marco que tem versão medida."""
    medidos = {k: v for k, v in marcos.items() if v}
    colunas = {nome: rotulo_do_marco(nome, v) for nome, v in medidos.items()}
    linhas = []
    for chave, descricao in qualidade.METRICAS.items():
        linha = {"Indicador": f"{chave} {_nome_curto(descricao)}"}
        for nome, v in medidos.items():
            linha[colunas[nome]] = formatar_indice(v["metricas"][chave]["valor"])
        linhas.append(linha)
    for chave in INDICES_AGREGADOS:
        linha = {"Indicador": f"{chave} {_NOMES_AGREGADOS[chave]}"}
        for nome, v in medidos.items():
            item = v["agregacao"][chave]
            linha[colunas[nome]] = (NAO_MEDIDO if item["valor"] is None
                                    else f"{formatar_indice(item['valor'], item['parcial'])} {qualidade.faixa(item['valor'])}")
        linhas.append(linha)
    return pd.DataFrame(linhas)


def serie_do_indice(avaliacoes: List[Dict[str, Any]], chave: str = "Q") -> pd.DataFrame:
    """Evolução de um índice agregado versão a versão; versão não medida fica com valor vazio (None)."""
    return pd.DataFrame([
        {"versao": a["versao"], "valor": a["agregacao"][chave]["valor"], "parcial": a["agregacao"][chave]["parcial"]}
        for a in avaliacoes
    ])


def arquivos_fora_do_limiar(avaliacao: Dict[str, Any], chave: str) -> Dict[str, Any]:
    """Conformes, total e arquivos fora do limiar de uma métrica, para rastrear a causa de uma nota baixa."""
    metrica = avaliacao["metricas"][chave]
    return {
        "valor": metrica["valor"],
        "conformes": metrica["conformes"],
        "total": metrica["total"],
        "arquivos": metrica["fora_do_limiar"],
        "motivo": metrica.get("motivo"),
    }


def tabela_processo(processo_por_release: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """Uma linha por release. Os cabeçalhos P1, P2, P3 e P são curtos; os nomes ficam nos cartões e na legenda."""
    linhas = []
    for release, item in processo_por_release.items():
        linha = {"Release": release + (" (em andamento)" if item["em_andamento"] else ""),
                 "Sprints": ", ".join(item["sprints"]) or NAO_MEDIDO}
        for chave in INDICADORES:
            linha[chave] = formatar_indice(item["indicadores"][chave])
        linha["P"] = (NAO_MEDIDO if item["P"] is None
                                         else f"{formatar_indice(item['P'], item['parcial'])} {qualidade.faixa(item['P'])}")
        linhas.append(linha)
    return pd.DataFrame(linhas)


def _numero(valor: Optional[float], casas: int = 1) -> str:
    return NAO_MEDIDO if valor is None else f"{valor:.{casas}f}"


def _inteiro(valor: Optional[int]) -> str:
    return NAO_MEDIDO if valor is None else str(valor)


def tabela_comparativo(comparativo: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """Velocidade e planejados em pontos por sprint; bugs e defeito provável em quantidade."""
    linhas = []
    for release, item in comparativo.items():
        cobertura = item["cobertura"]
        linhas.append({
            "Release": release,
            "Versão": item["versao"] or NAO_MEDIDO,
            "Velocidade": _numero(item["velocidade"]),
            "Planejados": _numero(item["planejados_por_sprint"]),
            "Cobertura": NAO_MEDIDO if cobertura is None else f"{cobertura:.1f}%",
            "Bugs abertos": _inteiro(item["bugs_abertos_na_release"]),
            "Defeito provável": _inteiro(item["arquivos_com_defeito_provavel"]),
        })
    return pd.DataFrame(linhas)


def aviso_estado_nao_coletado() -> str:
    """Aviso da coleta sem `fechada`: história aceita que ficou em Aceitação PO pode contar duas vezes."""
    return (
        "A última coleta não trouxe se cada história está fechada (campo `fechada`). Sem ele, a "
        "história que o PO já aceitou e que o ZenHub manteve na coluna Aceitação PO pode estar "
        "contada duas vezes, como aceita e como à espera do aceite. Rode de novo a coleta de métricas "
        "e confira no log se o ZenHub aceitou o campo `state`."
    )


def aviso_modo_entregues(rotulo: str, aceitos: float, aguardando: float, historias: int) -> str:
    """Texto do modo com Aceitação PO: o que entra, o que já foi aceito e por que a velocity das sprints muda."""
    return (
        f"**Modo: {rotulo}.** Os pontos entregues desta release incluem "
        f"**{aguardando:.0f} SP** de {historias} história(s) em Aceitação PO, com o código "
        f"entregue e o aceite pendente. Já aceitos: {aceitos:.0f} SP. "
        "Cada história conta na sprint em que foi cotada, mesmo que o aceite saia depois: a velocity "
        "de uma sprint passada já inclui o que a equipe entregou nela e o PO ainda não aceitou. "
        "Para ver só as aceitas, mude a opção na barra lateral."
    )


def dados_dos_indices(releases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Dados do gráfico de SPI e CPI por release, só das releases que têm índice.

    Enquanto o custo real não é apurado, o AC é estimado e o CPI sai igual ao SPI. Nesse caso
    `iguais` é verdadeiro e o gráfico mostra um índice só, para não parecer que há duas medidas.
    `aguardando_aceite` marca a release com pontos planejados, nenhum aceito e histórias em
    Aceitação PO: o índice zero ali é espera de aceite, e não atraso do time. Sem nada em
    aceitação, o zero é entrega zero de fato e não leva o rótulo.
    """
    com_indice = [r for r in releases if r["spi"] is not None]
    spi = [r["spi"] for r in com_indice]
    cpi = [r["cpi"] for r in com_indice]
    iguais = all(c is None or abs(s - c) < 1e-9 for s, c in zip(spi, cpi))
    aguardando = [r["prp"] > 0 and r["rpc"] <= 0 and r.get("rpc_aguardando", 0.0) > 0 for r in com_indice]
    maior = max([v for v in spi + cpi if v is not None] or [0.0])
    return {
        "releases": [r["id"] for r in com_indice],
        "spi": spi,
        "cpi": cpi,
        "iguais": iguais,
        "aguardando_aceite": aguardando,
        "rotulos_spi": [_rotulo_do_indice(v, a) for v, a in zip(spi, aguardando)],
        "rotulos_cpi": [_rotulo_do_indice(v, a) for v, a in zip(cpi, aguardando)],
        # O eixo sempre mostra a referência 1,0 com folga acima, e começa em zero.
        "topo": max(1.5, round(maior * 1.15, 2)),
    }


def _rotulo_do_indice(valor: Optional[float], aguardando_aceite: bool) -> str:
    if valor is None:
        return ""
    return f"{valor:.2f}" + (" (aguardando aceite)" if aguardando_aceite else "")


def tabela_de_custo_por_release(releases: List[Dict[str, Any]]) -> pd.DataFrame:
    """Custo planejado da release (BAC) ao lado do acumulado do projeto até ela, para não confundir os dois."""
    return pd.DataFrame([{
        "Release": r["id"],
        "Custo planejado da release (BAC)": f"R$ {r['bac']:,.2f}",
        "Acumulado do projeto até a release": f"R$ {r['orcamento_acumulado']:,.2f}",
    } for r in releases])



# ---------------------------------------------------------------------------
# Aceitas e entregues lado a lado (EVM)
# ---------------------------------------------------------------------------

def _pct(valor: Optional[float]) -> str:
    return "N/A" if valor is None else f"{valor * 100:.0f}%"


def _indice(valor: Optional[float]) -> str:
    return "N/A" if valor is None else f"{valor:.2f}"


def _reais(valor: Optional[float]) -> str:
    return "N/A" if valor is None else f"R$ {valor:,.2f}"


def tabela_lado_a_lado(linha: Dict[str, Any]) -> pd.DataFrame:
    """Os indicadores da release nos dois modos, para comparar o que foi aceito com o que foi entregue."""
    a, e = linha["aceitas"], linha["entregues"]
    return pd.DataFrame([
        {"Indicador": "Pontos entregues (RPC)", "Somente aceitas": f"{a['rpc']:.0f} SP",
         "Aceitas + em Aceitação PO": f"{e['rpc']:.0f} SP"},
        {"Indicador": "Escopo entregue (APC)", "Somente aceitas": _pct(a["apc"]),
         "Aceitas + em Aceitação PO": _pct(e["apc"])},
        {"Indicador": "Valor agregado (EV)", "Somente aceitas": _reais(a["ev"]),
         "Aceitas + em Aceitação PO": _reais(e["ev"])},
        {"Indicador": "SPI", "Somente aceitas": _indice(a["spi"]), "Aceitas + em Aceitação PO": _indice(e["spi"])},
        {"Indicador": "CPI", "Somente aceitas": _indice(a["cpi"]), "Aceitas + em Aceitação PO": _indice(e["cpi"])},
        {"Indicador": "Faixa do SPI", "Somente aceitas": classificar_indice(a["spi"]) or "N/A",
         "Aceitas + em Aceitação PO": classificar_indice(e["spi"]) or "N/A"},
    ])


def leitura_escopo_e_tempo(linha: Dict[str, Any]) -> str:
    """Frase que põe lado a lado o prazo decorrido, o escopo aceito e o escopo entregue da release."""
    if linha["prp"] <= 0:
        return "Sem pontos estimados nesta release, não há escopo para comparar com o prazo."
    if linha["fonte"] is None:
        return (
            "A coluna Aceitação PO ainda não foi coletada, então os dois modos coincidem e não dá para "
            "separar o escopo aceito do entregue."
        )
    ppc, apc_a, apc_e = linha["ppc"], linha["aceitas"]["apc"] or 0.0, linha["entregues"]["apc"] or 0.0
    frase = (
        f"Na {linha['id']}, {_pct(ppc)} do prazo já decorreu. O escopo entregue é {_pct(apc_e)} "
        f"e o aceito é {_pct(apc_a)}."
    )
    if linha["aguardando_pontos"] <= 0:
        return frase + " Nenhuma história aguarda o aceite do PO."
    frase += f" A diferença, de {linha['aguardando_pontos']:.0f} SP, depende do aceite do PO."
    if apc_e >= ppc > apc_a:
        frase += " O trabalho entregue acompanha o prazo; o que o atrasa nos índices é a espera do aceite."
    elif apc_e < ppc:
        frase += " Mesmo contando o que aguarda o aceite, o escopo entregue está abaixo do prazo decorrido."
    else:
        frase += " Os pontos aceitos já acompanham o prazo decorrido."
    return frase


def dados_escopo_e_tempo(comparacao: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Séries em porcentagem do gráfico de escopo e prazo, só das releases com pontos planejados."""
    com_escopo = [r for r in comparacao if r["prp"] > 0]
    return {
        "releases": [r["id"] for r in com_escopo],
        "prazo": [round(r["ppc"] * 100, 1) for r in com_escopo],
        "aceitas": [round((r["aceitas"]["apc"] or 0.0) * 100, 1) for r in com_escopo],
        "entregues": [round((r["entregues"]["apc"] or 0.0) * 100, 1) for r in com_escopo],
    }


# ---------------------------------------------------------------------------
# Qualidade por característica (ISO/IEC 25010), por release
# ---------------------------------------------------------------------------

_COR_DA_FAIXA_CARACTERISTICA = {
    caracteristicas.ADEQUADO: THEME_COLORS["secondary"],
    caracteristicas.ATENCAO: THEME_COLORS["warning"],
    caracteristicas.CRITICO: THEME_COLORS["danger"],
}

# Rótulo, unidade e forma de escrever cada medida do SonarCloud no bloco de detalhe.
_DETALHE = {
    "security_rating": ("Nota de segurança", "nota"),
    "reliability_rating": ("Nota de confiabilidade", "nota"),
    "sqale_rating": ("Nota de manutenibilidade", "nota"),
    "vulnerabilities": ("Vulnerabilidades", "inteiro"),
    "security_hotspots": ("Security hotspots", "inteiro"),
    "bugs": ("Bugs", "inteiro"),
    "code_smells": ("Code smells", "inteiro"),
    "sqale_index": ("Débito técnico", "minutos"),
    "duplicated_lines_density": ("Duplicação", "percentual"),
    "coverage": ("Cobertura", "percentual"),
    "tests": ("Testes", "inteiro"),
    "test_failures": ("Testes com falha", "inteiro"),
    "test_errors": ("Testes com erro", "inteiro"),
    "ncloc": ("Linhas de código", "inteiro"),
    "files": ("Arquivos", "inteiro"),
    "functions": ("Funções", "inteiro"),
    "complexity": ("Complexidade", "inteiro"),
    "comment_lines_density": ("Comentários", "percentual"),
    "test_execution_time": ("Tempo de execução dos testes", "milissegundos"),
}


def _pct_ptbr(valor: float) -> str:
    return f"{valor:.1f}".replace(".", ",") + "%"


def _int_ptbr(valor: float) -> str:
    return f"{int(round(valor)):,}".replace(",", ".")


def _valor_da_caracteristica(item: Dict[str, Any]) -> str:
    if item["valor"] is None:
        return NAO_MEDIDO
    return item["nota"] or _pct_ptbr(item["valor"])


def cartao_caracteristica(item: Dict[str, Any]) -> Dict[str, str]:
    """Texto e cor do cartão de uma característica; sem dado, n/m em cor neutra, nunca zero."""
    if item["faixa"] == caracteristicas.NAO_MEDIDA:
        return {"rotulo": item["nome"], "valor": NAO_MEDIDO, "subtexto": caracteristicas.NAO_MEDIDA,
                "cor": THEME_COLORS["accent"]}
    sentido = item["sentido"]
    if sentido in (caracteristicas.MELHOROU, caracteristicas.PIOROU, caracteristicas.MANTEVE):
        complemento = f"{sentido} em relação à release anterior"
    elif sentido == caracteristicas.PRIMEIRA:
        complemento = caracteristicas.PRIMEIRA
    else:
        complemento = "Sem comparação com a release anterior"
    return {
        "rotulo": item["nome"],
        "valor": _valor_da_caracteristica(item),
        "subtexto": f"{item['faixa']} · {complemento}",
        "cor": _COR_DA_FAIXA_CARACTERISTICA[item["faixa"]],
    }


def tabela_caracteristicas(releases: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Uma linha por característica e uma coluna por release, com o valor e a faixa de cada uma."""
    if not releases:
        return []
    linhas = []
    for indice, base in enumerate(releases[0]["caracteristicas"]):
        linha = {"Característica": base["nome"]}
        for release in releases:
            item = release["caracteristicas"][indice]
            linha[release["nome"]] = (NAO_MEDIDO if item["valor"] is None
                                      else f"{_valor_da_caracteristica(item)} · {item['faixa']}")
        linhas.append(linha)
    return linhas


def _formatar_detalhe(tipo: str, valor: float) -> str:
    if tipo == "nota":
        return caracteristicas.letra(valor) or NAO_MEDIDO
    if tipo == "percentual":
        return _pct_ptbr(valor)
    if tipo == "minutos":
        return f"{_int_ptbr(valor)} min"
    if tipo == "milissegundos":
        return f"{valor / 1000:.1f}".replace(".", ",") + " s"
    return _int_ptbr(valor)


def tabela_detalhe(release: Dict[str, Any]) -> List[Dict[str, str]]:
    """Medidas do SonarCloud na data da release, para o bloco de detalhe. Só entra o que tem valor."""
    linhas = []
    # Primeiro as medidas conhecidas, na ordem da tabela; depois as que o painel ainda não nomeia.
    ordem = [m for m in _DETALHE if m in release["detalhe"]] + sorted(m for m in release["detalhe"] if m not in _DETALHE)
    for metrica in ordem:
        valor = release["detalhe"][metrica]
        rotulo, tipo = _DETALHE.get(metrica, (metrica, "inteiro"))
        linhas.append({"Medida": rotulo, "Valor": _formatar_detalhe(tipo, valor)})
    return linhas
