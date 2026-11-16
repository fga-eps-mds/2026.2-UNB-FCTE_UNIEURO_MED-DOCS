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

Depois do aceite a história é fechada, mas o ZenHub mantém a coluna em que ela estava. Por
isso a coleta grava também se a issue está fechada (`fechada`) e quando (`fechada_em`), e a
fechada não conta aqui.

Uma história que passa de uma sprint para a seguinte aparece nas duas. Ela conta uma vez,
na última sprint em que aparece.

O aceite do PO costuma sair depois do fim da sprint em que a equipe entregou a história. O
ZenHub conta os pontos na sprint em que a história fecha, o que atribui à sprint seguinte uma
entrega que a anterior fez. `atribuir_aceites_tardios` devolve esses pontos à última sprint
encerrada em que a história aparece, e o painel lista as histórias movidas.

A coluna também guarda pull requests (já mesclados, por exemplo), que o ZenHub trata como
issues. Eles não têm estimativa, então só entra a issue com estimativa maior que zero: é o
que distingue uma história de um PR sem depender de rótulo.
"""

import unicodedata
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Set

from .config import COLUNAS_ACEITACAO, MODO_ENTREGUES

FONTE_ZENHUB = "zenhub"
FONTE_MANUAL = "manual"


def _normalizar(texto: Any) -> str:
    """Compara nomes de coluna sem depender de acento, caixa nem espaços nas pontas."""
    sem_acento = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("ascii")
    return " ".join(sem_acento.casefold().split())


def _e_historia(issue: Dict[str, Any]) -> bool:
    """Histórias têm estimativa em pontos; PRs e tarefas sem estimativa ficam de fora da conta."""
    estimativa = issue.get("estimativa")
    return isinstance(estimativa, (int, float)) and not isinstance(estimativa, bool) and estimativa > 0


def _fechada(issue: Dict[str, Any]) -> bool:
    """A coleta grava se a issue está fechada (`fechada`). Sem o campo, a issue é tratada como aberta."""
    return bool(issue.get("fechada"))


def estado_coletado(sprints: List[Dict[str, Any]]) -> bool:
    """
    Diz se a coleta trouxe o estado das issues (`fechada`) em alguma sprint.

    Sem o campo, a história já aceita que o ZenHub manteve na coluna Aceitação PO conta duas
    vezes: como aceita e como à espera do aceite. O painel usa este sinal para avisar.
    """
    return any("fechada" in issue for sprint in sprints for issue in (sprint.get("issues") or []))


def _esta_em_aceitacao(issue: Dict[str, Any], colunas: Set[str], manual: Optional[Set[int]]) -> bool:
    if not _e_historia(issue):
        return False
    # O ZenHub mantém na coluna a história que o PO já aceitou e fechou; ela já está nos pontos
    # aceitos e não pode contar de novo como história à espera do aceite.
    if _fechada(issue):
        return False
    coluna = issue.get("coluna")
    if coluna and _normalizar(coluna) in colunas:
        return True
    return bool(manual) and issue.get("numero") in manual


def marcar_aguardando(
    sprints: List[Dict[str, Any]],
    colunas: Iterable[str] = COLUNAS_ACEITACAO,
    manual: Optional[Iterable[int]] = None,
    coletada: Optional[bool] = None,
) -> Optional[str]:
    """
    Preenche em cada sprint `aguardando_issues` (as histórias em aceitação, com número,
    estimativa e a sprint em que contam), `aguardando_pontos` e `estado_coletado` (se a coleta
    trouxe `fechada`), e devolve a fonte usada.

    Recebe as sprints em ordem cronológica, com `issues` (id, numero, estimativa e, quando a
    coleta trouxe, coluna). Sem coluna coletada nem lista manual, nada é marcado e a fonte é
    None: o painel avisa que o dado não existe, em vez de mostrar zero como se fosse medido.

    `coletada` é o sinal que a coleta grava (`colunas_coletadas`). Com ele, uma coluna Aceitação PO
    vazia (coluna lida, nenhuma história nela) deixa de parecer coluna nunca coletada. Sem o
    sinal (JSON antigo), a coluna é dada como coletada se alguma issue traz o campo `coluna`.
    """
    nomes = {_normalizar(c) for c in colunas}
    numeros = set(manual) if manual else None
    if coletada is not None:
        coletou_coluna = bool(coletada)
    else:
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
    com_estado = estado_coletado(sprints)
    for sprint in sprints:
        sprint["aguardando_pontos"] = sum(i["estimativa"] for i in sprint["aguardando_issues"])
        sprint["aceitacao_fonte"] = fonte
        sprint["estado_coletado"] = com_estado
    return fonte


def _instante(valor: Any) -> Optional[datetime]:
    """Data ISO (ou datetime) como instante com fuso; sem fuso, o texto é lido como UTC."""
    if isinstance(valor, str):
        try:
            valor = datetime.fromisoformat(valor.replace("Z", "+00:00"))
        except ValueError:
            return None
    if not isinstance(valor, datetime):
        return None
    return valor if valor.tzinfo else valor.replace(tzinfo=timezone.utc)


def _janela(sprint: Dict[str, Any]) -> tuple:
    """Início e fim da sprint, aceitando as chaves do data_layer (`start_at`) e do processo (`inicio`)."""
    inicio = sprint.get("start_at") if sprint.get("start_at") is not None else sprint.get("inicio")
    fim = sprint.get("end_at") if sprint.get("end_at") is not None else sprint.get("fim")
    return _instante(inicio), _instante(fim)


def atribuir_aceites_tardios(
    sprints: List[Dict[str, Any]],
    campo_pontos: str = "delivered_sp",
    colunas: Iterable[str] = COLUNAS_ACEITACAO,
) -> None:
    """
    Devolve à sprint de origem os pontos das histórias que o PO aceitou depois do fim dela.

    Vale para a história fechada (`fechada`) que ainda está na coluna de aceitação, ou seja, que
    esperou o PO, e cujo fechamento (`fechada_em`) caiu depois do fim de uma sprint em que ela
    aparece. Os pontos saem da sprint em que a história fechou, onde o ZenHub os contou, e entram
    na última sprint encerrada em que ela aparece. História fechada dentro da própria sprint, ou
    que não passou pela aceitação, não muda de lugar.

    Muda `campo_pontos` de cada sprint e preenche `aceitos_depois_issues` (as histórias movidas
    para ela, com a sprint em que fecharam) e `aceitos_depois_pontos`. Sem `fechada` e
    `fechada_em` nas issues, que a coleta passou a gravar, nada se move.
    """
    nomes = {_normalizar(c) for c in colunas}
    for sprint in sprints:
        sprint["aceitos_depois_issues"] = []
        sprint["aceitos_depois_pontos"] = 0.0

    janelas = [_janela(s) for s in sprints]
    ocorrencias: Dict[Any, List[int]] = {}
    ultima: Dict[Any, Dict[str, Any]] = {}
    for indice, sprint in enumerate(sprints):
        for issue in sprint.get("issues") or []:
            chave = issue.get("id") if issue.get("id") is not None else issue.get("numero")
            if chave is None:
                continue
            ocorrencias.setdefault(chave, []).append(indice)
            ultima[chave] = issue

    for chave, issue in ultima.items():
        if not (_e_historia(issue) and _fechada(issue)):
            continue
        if _normalizar(issue.get("coluna") or "") not in nomes:
            continue
        fechada = _instante(issue.get("fechada_em"))
        if fechada is None:
            continue

        onde = ocorrencias[chave]
        fechamento = next(
            (i for i in onde if janelas[i][0] and janelas[i][1] and janelas[i][0] <= fechada < janelas[i][1]),
            None,
        )
        encerradas = [i for i in onde if janelas[i][1] and janelas[i][1] <= fechada]
        if fechamento is None or not encerradas:
            continue
        entrega = max(encerradas)
        if entrega == fechamento:
            continue

        pontos = float(issue["estimativa"])
        sprints[fechamento][campo_pontos] = max(0.0, float(sprints[fechamento].get(campo_pontos, 0.0)) - pontos)
        sprints[entrega][campo_pontos] = float(sprints[entrega].get(campo_pontos, 0.0)) + pontos
        sprints[entrega]["aceitos_depois_issues"].append({
            "id": issue.get("id"),
            "numero": issue.get("numero"),
            "estimativa": pontos,
            "sprint": sprints[fechamento].get("name") or sprints[fechamento].get("nome"),
            "fechada_em": issue.get("fechada_em"),
        })
        sprints[entrega]["aceitos_depois_pontos"] += pontos


def pontos_entregues(aceitos: float, aguardando: float, modo: str) -> float:
    """Pontos entregues: os aceitos e, no modo "entregues", também os que aguardam o aceite."""
    return float(aceitos) + (float(aguardando) if modo == MODO_ENTREGUES else 0.0)


def numeros_manuais(dados: Any) -> Optional[Set[int]]:
    """Números de issue do arquivo manual (`{"issues": [7, 8]}`), ou None se o formato não servir."""
    if not isinstance(dados, dict) or not isinstance(dados.get("issues"), list):
        return None
    numeros = {n for n in dados["issues"] if isinstance(n, int) and not isinstance(n, bool)}
    return numeros or None
