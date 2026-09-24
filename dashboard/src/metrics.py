from typing import Dict, List, Any
import pandas as pd


def compute_agile_evm_metrics(
    sprints: List[Dict[str, Any]],
    prp_0: float,
    planned_sprints: float,
    sprint_budget_brl: float
) -> Dict[str, Any]:
    """Calcula indicadores de prazo e custo do Agile EVM (Sulaiman et al., 2006)."""
    bac = prp_0 * (sprint_budget_brl / (prp_0 / planned_sprints if planned_sprints > 0 else 1))
    
    total_rpc = 0.0
    total_pa = 0.0
    accumulated_ac = 0.0
    
    burnup_labels = ["Início"]
    burnup_pv = [0.0]
    burnup_ev = [0.0]
    burnup_ideal = [0.0]
    
    spi_series = [1.0]
    cpi_series = [1.0]
    velocity_series = []
    velocity_labels = []
    
    table_rows = []

    for idx, s in enumerate(sprints):
        n = idx + 1
        name = s.get("name", f"Sprint {n}")
        delivered_sp = float(s.get("delivered_sp", 0.0))
        points_added = float(s.get("points_added", 0.0))
        is_done = s.get("status", "CLOSED").upper() == "CLOSED"

        total_pa += points_added
        prp_n = prp_0 + total_pa
        ppc = min(1.0, n / planned_sprints)
        pv = round(ppc * bac, 2)

        burnup_labels.append(name)
        burnup_pv.append(pv)
        burnup_ideal.append(round((n / planned_sprints) * bac, 2))

        if is_done:
            total_rpc += delivered_sp
            apc = total_rpc / prp_n if prp_n > 0 else 0.0
            ev = round(apc * bac, 2)
            accumulated_ac += sprint_budget_brl

            spi = round(ev / pv, 2) if pv > 0 else 1.0
            cpi = round(ev / accumulated_ac, 2) if accumulated_ac > 0 else 1.0
            sv = round(ev - pv, 2)
            cv = round(ev - accumulated_ac, 2)
            etc = round((bac - ev) / cpi, 2) if cpi > 0 else 0.0
            eac = round(accumulated_ac + etc, 2)

            burnup_ev.append(ev)
            spi_series.append(spi)
            cpi_series.append(cpi)
            velocity_series.append(delivered_sp)
            velocity_labels.append(name)

            table_rows.append({
                "Sprint": name,
                "PRP₀ (SP)": f"{prp_0:.1f}",
                "PA (SP)": f"{points_added:.1f}",
                "PRPₙ (SP)": f"{prp_n:.1f}",
                "PPC": f"{ppc*100:.1f}%",
                "PC (SP)": f"{delivered_sp:.1f}",
                "RPC (SP)": f"{total_rpc:.1f}",
                "PV (R$)": f"R$ {pv:,.2f}",
                "EV (R$)": f"R$ {ev:,.2f}",
                "AC (R$)": f"R$ {accumulated_ac:,.2f}",
                "SPI": f"{spi:.2f}",
                "CPI": f"{cpi:.2f}",
                "CV (R$)": f"R$ {cv:,.2f}",
                "SV (R$)": f"R$ {sv:,.2f}",
                "EAC (R$)": f"R$ {eac:,.2f}",
                "Status": "Finalizada"
            })
        else:
            burnup_ev.append(None)
            table_rows.append({
                "Sprint": name,
                "PRP₀ (SP)": f"{prp_0:.1f}",
                "PA (SP)": f"{points_added:.1f}",
                "PRPₙ (SP)": f"{prp_n:.1f}",
                "PPC": f"{ppc*100:.1f}%",
                "PC (SP)": f"{delivered_sp:.1f}",
                "RPC (SP)": "-",
                "PV (R$)": f"R$ {pv:,.2f}",
                "EV (R$)": "-",
                "AC (R$)": "-",
                "SPI": "-",
                "CPI": "-",
                "CV (R$)": "-",
                "SV (R$)": "-",
                "EAC (R$)": "-",
                "Status": "Em Andamento / Futura"
            })

    current_spi = spi_series[-1] if len(spi_series) > 1 else 1.0
    current_cpi = cpi_series[-1] if len(cpi_series) > 1 else 1.0
    current_ev_list = [v for v in burnup_ev if v is not None]
    current_ev = current_ev_list[-1] if current_ev_list else 0.0
    etc_current = round((bac - current_ev) / current_cpi, 2) if current_cpi > 0 else 0.0

    avg_velocity = round(sum(velocity_series) / len(velocity_series), 1) if velocity_series else 0.0

    return {
        "bac": bac,
        "current_ev": current_ev,
        "current_spi": current_spi,
        "current_cpi": current_cpi,
        "etc_current": etc_current,
        "avg_velocity": avg_velocity,
        "burnup_labels": burnup_labels,
        "burnup_pv": burnup_pv,
        "burnup_ev": burnup_ev,
        "burnup_ideal": burnup_ideal,
        "velocity_labels": velocity_labels,
        "velocity_series": velocity_series,
        "spi_series": spi_series,
        "cpi_series": cpi_series,
        "audit_df": pd.DataFrame(table_rows)
    }


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