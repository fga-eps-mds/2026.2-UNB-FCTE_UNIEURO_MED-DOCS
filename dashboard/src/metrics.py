from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

import pandas as pd

from .aceitacao import pontos_entregues
from .config import FAIXAS_RISCO, FUSO_BRASILIA, MODO_PADRAO


def _data_brasilia(valor: Optional[str]) -> Optional[date]:
    """Converte um timestamp ISO (normalmente em UTC) para a data civil em Brasília."""
    if not valor:
        return None
    try:
        dt = datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(ZoneInfo(FUSO_BRASILIA)).date()


def _limites(release: Dict[str, Any]) -> tuple:
    return date.fromisoformat(release["inicio"]), date.fromisoformat(release["fim"])


def release_da_sprint(sprint: Dict[str, Any], releases: List[Dict[str, Any]]) -> Optional[str]:
    """Id da release a que a sprint pertence, ou None se cai fora de todas.

    Usa a data de término da sprint (em Brasília): uma sprint entrega o que
    foi planejado para a release em que ela termina, mesmo que comece antes dela.
    Sprints sem data de término usam a data de início.
    """
    referencia = _data_brasilia(sprint.get("end_at")) or _data_brasilia(sprint.get("start_at"))
    if referencia is None:
        return None
    for release in releases:
        inicio, fim = _limites(release)
        if inicio <= referencia <= fim:
            return release["id"]
    return None


def _ppc(release: Dict[str, Any], dia: date) -> float:
    """Percentual do prazo da release já decorrido em `dia` (0.0 a 1.0)."""
    inicio, fim = _limites(release)
    duracao = (fim - inicio).days + 1
    decorridos = min(max((dia - inicio).days + 1, 0), duracao)
    return decorridos / duracao


def pontos_distintos(sprints: List[Dict[str, Any]]) -> tuple:
    """PRP de uma release contando cada história uma só vez: (pontos, aproximado).

    Uma história que não termina na sprint passa para a seguinte, e o Zenhub a
    lista nas duas. Somar o `total_points` das sprints contaria seus pontos duas
    vezes. Com o detalhe por issue, cada história entra uma vez, com a estimativa
    da última sprint em que aparece (issue sem estimativa vale 0). Sem o detalhe,
    ou com a lista incompleta, volta à soma dos `total_points` e marca como
    aproximado. Com uma sprint só não há repetição possível, e o valor é exato.
    """
    soma = sum(float(s.get("total_points", 0.0)) for s in sprints)
    if len(sprints) <= 1:
        return soma, False

    por_id: Dict[Any, float] = {}
    for s in sprints:
        issues = s.get("issues")
        total = s.get("issues_total")
        completa = isinstance(issues, list) and (total is None or len(issues) >= total)
        if not completa or any(i.get("id") is None for i in issues):
            return soma, True
        for i in issues:
            por_id[i["id"]] = float(i.get("estimativa") or 0.0)
    return sum(por_id.values()), False


def compute_release_evm(
    sprints: List[Dict[str, Any]],
    releases: List[Dict[str, Any]],
    hoje: Optional[date] = None,
    modo: str = MODO_PADRAO,
) -> Dict[str, Any]:
    """Agile EVM por release (Sulaiman et al., 2006), sem parâmetros de simulação.

    Entradas reais: BAC de cada release (config.RELEASES, vindo do Plano de Custos)
    e, por sprint, os pontos planejados (`total_points`) e entregues (`delivered_sp`).
    Hipóteses: PRP = pontos das histórias distintas das sprints que terminam na release
    (ver `pontos_distintos`); RPC = soma dos pontos entregues nessas sprints; PPC = fração
    dos dias da release já decorrida; AC é estimado pela linha de base de custo
    (PPC x BAC), pois não há custo real apurado, então CPI coincide com SPI.

    `modo` escolhe o que são pontos entregues (RPC): só os das histórias aceitas (fechadas)
    ou também os das que estão em Aceitação PO, com o código entregue e o aceite pendente.
    Os dois valores ficam sempre no resultado (`rpc_aceito` e `rpc_aguardando`), e só o
    `rpc`, e tudo que parte dele (APC, EV, SPI, CPI), segue o modo. O PRP não muda.
    """
    hoje = hoje or datetime.now(ZoneInfo(FUSO_BRASILIA)).date()

    por_release: Dict[str, List[Dict[str, Any]]] = {r["id"]: [] for r in releases}
    for s in sprints:
        destino = release_da_sprint(s, releases)
        if destino:
            por_release[destino].append(s)

    resultado = []
    for release in releases:
        inicio, fim = _limites(release)
        lista = sorted(por_release[release["id"]], key=lambda s: s.get("end_at") or "")
        bac = float(release["bac_brl"])

        prp, prp_aproximado = pontos_distintos(lista)
        rpc_aceito = sum(float(s.get("delivered_sp", 0.0)) for s in lista)
        rpc_aguardando = sum(float(s.get("aguardando_pontos", 0.0)) for s in lista)
        rpc = pontos_entregues(rpc_aceito, rpc_aguardando, modo)
        em_aceitacao = [i for s in lista for i in s.get("aguardando_issues", [])]

        if hoje < inicio:
            status = "Futura"
        elif hoje > fim:
            status = "Concluída"
        else:
            status = "Em andamento"

        ppc = _ppc(release, hoje)
        apc = min(1.0, rpc / prp) if prp > 0 else None
        pv = round(ppc * bac, 2)
        ac = round(ppc * bac, 2)
        ev = round(apc * bac, 2) if apc is not None else None

        calculavel = status != "Futura" and ev is not None and pv > 0
        spi = round(ev / pv, 2) if calculavel else None
        cpi = round(ev / ac, 2) if calculavel and ac > 0 else None
        sv = round(ev - pv, 2) if calculavel else None
        cv = round(ev - ac, 2) if calculavel else None
        etc = round((bac - ev) / cpi, 2) if cpi else None
        eac = round(ac + etc, 2) if etc is not None else None

        serie = []
        acumulado = 0.0
        aceito_acum = 0.0
        for s in lista:
            aceito_acum += float(s.get("delivered_sp", 0.0))
            acumulado += pontos_entregues(
                float(s.get("delivered_sp", 0.0)), float(s.get("aguardando_pontos", 0.0)), modo)
            fim_sprint = _data_brasilia(s.get("end_at")) or fim
            serie.append({
                "sprint": s.get("name", "Sprint"),
                "entregue_acum": acumulado,
                "aceito_acum": aceito_acum,
                "restante": max(prp - acumulado, 0.0),
                "restante_ideal": round(prp * (1 - _ppc(release, min(fim_sprint, fim))), 2),
            })

        resultado.append({
            "id": release["id"],
            "nome": release["nome"],
            "inicio": inicio,
            "fim": fim,
            "status": status,
            "bac": bac,
            "prp": prp,
            "prp_aproximado": prp_aproximado,
            "rpc": rpc,
            "rpc_aceito": rpc_aceito,
            "rpc_aguardando": rpc_aguardando,
            "em_aceitacao": em_aceitacao,
            "aceitacao_fonte": next((s.get("aceitacao_fonte") for s in lista if s.get("aceitacao_fonte")), None),
            "modo": modo,
            "n_sprints": len(lista),
            "ppc": ppc,
            "apc": apc,
            "pv": pv,
            "ev": ev,
            "ac": ac,
            "spi": spi,
            "cpi": cpi,
            "sv": sv,
            "cv": cv,
            "etc": etc,
            "eac": eac,
            "serie": serie,
        })

    # Release que ainda não começou não tem o que medir: fica de fora até a data de início.
    iniciadas = [r for r in resultado if r["status"] != "Futura"]
    resultado = iniciadas or resultado[:1]

    atual = next((r["id"] for r in resultado if r["status"] == "Em andamento"), None)
    if atual is None:
        concluidas = [r["id"] for r in resultado if r["status"] == "Concluída"]
        atual = concluidas[-1] if concluidas else resultado[0]["id"]

    return {"releases": resultado, "atual": atual, "audit_df": _tabela_auditoria(resultado)}


def _brl(valor: Optional[float]) -> str:
    return "-" if valor is None else f"R$ {valor:,.2f}"


def _num(valor: Optional[float], casas: int = 2) -> str:
    return "-" if valor is None else f"{valor:.{casas}f}"


def _tabela_auditoria(releases: List[Dict[str, Any]]) -> pd.DataFrame:
    linhas = []
    for r in releases:
        linhas.append({
            "Release": r["id"],
            "Período": f"{r['inicio']:%d/%m} a {r['fim']:%d/%m}",
            "Status": r["status"],
            "BAC (R$)": _brl(r["bac"]),
            "PRP (SP)": _num(r["prp"], 1) + (" (aprox.)" if r["prp_aproximado"] else ""),
            "RPC aceito (SP)": _num(r["rpc_aceito"], 1),
            "Em aceitação (SP)": _num(r["rpc_aguardando"], 1),
            "RPC considerado (SP)": _num(r["rpc"], 1),
            "PPC": f"{r['ppc'] * 100:.1f}%",
            "APC": "-" if r["apc"] is None else f"{r['apc'] * 100:.1f}%",
            "PV (R$)": _brl(r["pv"]),
            "EV (R$)": _brl(r["ev"]),
            "AC (R$)": _brl(r["ac"]),
            "SPI": _num(r["spi"]),
            "CPI": _num(r["cpi"]),
            "SV (R$)": _brl(r["sv"]),
            "CV (R$)": _brl(r["cv"]),
            "EAC (R$)": _brl(r["eac"]),
        })
    return pd.DataFrame(linhas)


def classificar_risco(severidade: int) -> str:
    """Grau do risco pela escala única do plano (FAIXAS_RISCO): Baixo, Médio ou Elevado."""
    for _minimo, maximo, grau in FAIXAS_RISCO:
        if severidade <= maximo:
            return grau
    return FAIXAS_RISCO[-1][2]


def process_risks_summary(risks: List[Dict[str, Any]],
                          ocorrencias: Optional[List[Dict[str, Any]]] = None) -> pd.DataFrame:
    """Calcula a severidade (P×I), o grau pela escala do plano e a situação de cada risco."""
    ocorridos = {o["risco"] for o in (ocorrencias or [])}
    rows = []
    for r in risks:
        score = r["probabilidade"] * r["impacto"]
        rows.append({
            "ID": r["id"],
            "Título do Risco": r["titulo"],
            "Categoria": r["categoria"],
            "Probabilidade (1-5)": r["probabilidade"],
            "Impacto (1-5)": r["impacto"],
            "Severidade (P×I)": score,
            "Grau": classificar_risco(score),
            "Situação": "Concretizado" if r["id"] in ocorridos else "Monitorado",
            "Ação Preventiva / Mitigatória": r.get("acao", "-")
        })
    return pd.DataFrame(rows)


def revisoes_realizadas(revisoes: List[Dict[str, Any]], hoje: Optional[date] = None) -> List[Dict[str, Any]]:
    """
    Revisões de riscos de sprints que já aconteceram, em ordem de data.

    Uma revisão só existe depois da sprint review: entrada com data futura (ou sem data)
    é descartada, para que o histórico nunca mostre sprints que ainda não ocorreram.
    """
    hoje = hoje or datetime.now(ZoneInfo(FUSO_BRASILIA)).date()
    validas = []
    for rev in revisoes or []:
        try:
            quando = date.fromisoformat(str(rev.get("data")))
        except ValueError:
            continue
        if quando <= hoje:
            validas.append(rev)
    return sorted(validas, key=lambda rev: rev["data"])


def tabela_historico_riscos(revisoes: List[Dict[str, Any]]) -> pd.DataFrame:
    """Severidade e grau de cada risco em cada revisão realizada (linhas: riscos; colunas: sprints)."""
    ids = sorted({rid for rev in revisoes for rid in rev.get("riscos", {})})
    linhas = []
    for rid in ids:
        linha = {"ID": rid}
        for rev in revisoes:
            pi = rev.get("riscos", {}).get(rid)
            if pi is None:
                linha[rev["sprint"]] = "—"
                continue
            sev = pi["probabilidade"] * pi["impacto"]
            linha[rev["sprint"]] = f"{pi['probabilidade']}×{pi['impacto']} = {sev} ({classificar_risco(sev)})"
        linhas.append(linha)
    return pd.DataFrame(linhas)