from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

import pandas as pd

from .config import FUSO_BRASILIA


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


def compute_release_evm(
    sprints: List[Dict[str, Any]],
    releases: List[Dict[str, Any]],
    hoje: Optional[date] = None,
) -> Dict[str, Any]:
    """Agile EVM por release (Sulaiman et al., 2006), sem parâmetros de simulação.

    Entradas reais: BAC de cada release (config.RELEASES, vindo do Plano de Custos)
    e, por sprint, os pontos planejados (`total_points`) e entregues (`delivered_sp`).
    Hipóteses: PRP = soma dos pontos das sprints que terminam na release; PPC = fração
    dos dias da release já decorrida; AC é estimado pela linha de base de custo
    (PPC x BAC), pois não há custo real apurado, então CPI coincide com SPI.
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

        prp = sum(float(s.get("total_points", 0.0)) for s in lista)
        rpc = sum(float(s.get("delivered_sp", 0.0)) for s in lista)

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
        for s in lista:
            acumulado += float(s.get("delivered_sp", 0.0))
            fim_sprint = _data_brasilia(s.get("end_at")) or fim
            serie.append({
                "sprint": s.get("name", "Sprint"),
                "entregue_acum": acumulado,
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
            "rpc": rpc,
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
            "PRP (SP)": _num(r["prp"], 1),
            "RPC (SP)": _num(r["rpc"], 1),
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


def process_risks_summary(risks: List[Dict[str, Any]]) -> pd.DataFrame:
    """Calcula o índice de severidade e formata a tabela de riscos."""
    rows = []
    for r in risks:
        score = r["probabilidade"] * r["impacto"]
        if score >= 16:
            nivel = "Crítico"
        elif score >= 10:
            nivel = "Alto"
        elif score >= 5:
            nivel = "Médio"
        else:
            nivel = "Baixo"

        rows.append({
            "ID": r["id"],
            "Título do Risco": r["titulo"],
            "Categoria": r["categoria"],
            "Probabilidade (1-5)": r["probabilidade"],
            "Impacto (1-5)": r["impacto"],
            "Severidade (P×I)": score,
            "Nível": nivel,
            "Ação Preventiva / Mitigatória": r.get("acao", "-")
        })
    return pd.DataFrame(rows)