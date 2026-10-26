"""
Templates e Utilitários de Apresentação
Preparado para a evolução modular da Release 2 (DA-R2: Qualidade de Produto Q-Rapids)
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from . import qualidade
from .config import THEME_COLORS
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


def aviso_modo_entregues(rotulo: str, aceitos: float, aguardando: float, historias: int) -> str:
    """Texto do modo com Aceitação PO: o que entra, o que já foi aceito e por que a velocity das sprints muda."""
    return (
        f"**Modo: {rotulo}.** Os pontos entregues desta release incluem "
        f"**{aguardando:.0f} SP** de {historias} história(s) em Aceitação PO, com o código "
        f"entregue e o aceite pendente. Já aceitos: {aceitos:.0f} SP. "
        "Cada história conta na última sprint em que aparece: as entregues numa sprint anterior e "
        "ainda sem aceite somam na sprint atual, e a velocity daquela sprint anterior fica mais baixa. "
        "Para ver só as aceitas, mude a opção na barra lateral."
    )
