"""
Histórias entregues que aguardam o aceite do PO.

Uma história só é fechada depois do aceite (Ata 08), e os pontos de uma sprint no ZenHub
(`delivered_story_points`) só contam as histórias fechadas. Enquanto o PO não aceita, a
história fica aberta na coluna "Aceitação PO". Este módulo reconhece essas histórias nas
sprints e decide, pelo modo escolhido, se os pontos delas entram nos pontos entregues.

Fontes, da mais confiável à menos:
1. a coluna que a coleta grava em cada issue (`coluna`), com a lista das colunas que
   contam em `config.COLUNAS_ACEITACAO`;
2. uma lista manual de números de issue em `analytics-raw-data/aceitacao_po_manual.json`,
   usada só quando a coleta não trouxe as colunas.

Uma história que passa de uma sprint para a seguinte aparece nas duas. Ela conta uma vez,
na última sprint em que aparece.
"""

import unicodedata
from typing import Any, Dict, Iterable, List, Optional, Set

from .config import COLUNAS_ACEITACAO, MODO_ENTREGUES

FONTE_ZENHUB = "zenhub"
FONTE_MANUAL = "manual"


def _normalizar(texto: Any) -> str:
    """Compara nomes de coluna sem depender de acento, caixa nem espaços nas pontas."""
    sem_acento = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("ascii")
    return " ".join(sem_acento.casefold().split())


def _esta_em_aceitacao(issue: Dict[str, Any], colunas: Set[str], manual: Optional[Set[int]]) -> bool:
    coluna = issue.get("coluna")
    if coluna and _normalizar(coluna) in colunas:
        return True
    return bool(manual) and issue.get("numero") in manual


def marcar_aguardando(
    sprints: List[Dict[str, Any]],
    colunas: Iterable[str] = COLUNAS_ACEITACAO,
    manual: Optional[Iterable[int]] = None,
) -> Optional[str]:
    """
    Preenche em cada sprint `aguardando_issues` (as histórias em aceitação, com número,
    estimativa e a sprint em que contam) e `aguardando_pontos`, e devolve a fonte usada.

    Recebe as sprints em ordem cronológica, com `issues` (id, numero, estimativa e, quando a
    coleta trouxe, coluna). Sem coluna coletada nem lista manual, nada é marcado e a fonte é
    None: o painel avisa que o dado não existe, em vez de mostrar zero como se fosse medido.
    """
    nomes = {_normalizar(c) for c in colunas}
    numeros = set(manual) if manual else None
    coletou_coluna = any(
        issue.get("coluna") is not None
        for sprint in sprints
        for issue in (sprint.get("issues") or [])
    )
    usa_manual = bool(numeros) and not coletou_coluna
    fonte = FONTE_ZENHUB if coletou_coluna else (FONTE_MANUAL if usa_manual else None)

    ultimo: Dict[Any, int] = {}
    achadas: List[Dict[str, Any]] = []
    for indice, sprint in enumerate(sprints):
        for issue in sprint.get("issues") or []:
            if fonte is None or not _esta_em_aceitacao(issue, nomes, numeros if usa_manual else None):
                continue
            chave = issue.get("id") if issue.get("id") is not None else issue.get("numero")
            if chave is None:
                continue
            ultimo[chave] = indice
            achadas.append({"chave": chave, "indice": indice, "issue": issue})

    for sprint in sprints:
        sprint["aguardando_issues"] = []
    for item in achadas:
        # Só a ocorrência da última sprint vale; as anteriores são a mesma história.
        if ultimo[item["chave"]] != item["indice"]:
            continue
        issue = item["issue"]
        sprints[item["indice"]]["aguardando_issues"].append({
            "id": issue.get("id"),
            "numero": issue.get("numero"),
            "estimativa": float(issue.get("estimativa") or 0.0),
            "sprint": sprints[item["indice"]].get("name") or sprints[item["indice"]].get("nome"),
        })
    for sprint in sprints:
        sprint["aguardando_pontos"] = sum(i["estimativa"] for i in sprint["aguardando_issues"])
        sprint["aceitacao_fonte"] = fonte
    return fonte


def pontos_entregues(aceitos: float, aguardando: float, modo: str) -> float:
    """Pontos entregues: os aceitos e, no modo "entregues", também os que aguardam o aceite."""
    return float(aceitos) + (float(aguardando) if modo == MODO_ENTREGUES else 0.0)


def numeros_manuais(dados: Any) -> Optional[Set[int]]:
    """Números de issue do arquivo manual (`{"issues": [7, 8]}`), ou None se o formato não servir."""
    if not isinstance(dados, dict) or not isinstance(dados.get("issues"), list):
        return None
    numeros = {n for n in dados["issues"] if isinstance(n, int) and not isinstance(n, bool)}
    return numeros or None
