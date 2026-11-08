"""
Indicadores de processo, normalizados entre 0 e 1, e a comparação R1 × R2 de
velocidade, cobertura e defeitos que o cronograma da disciplina pede para o DA-R2.

Entradas, todas em analytics-raw-data/:
- zenhub_analytics.json: pontos planejados, entregues e adicionados por sprint;
- GitHub_API-Runs-<repositório>.json: execuções do CI;
- GitHub_API-Bugs-<repositório>.json: issues com o rótulo bug;
- as mesmas entradas do Q-Rapids (src/qualidade.py), para cobertura e defeitos prováveis.

Os pesos e as fórmulas são uma proposta do time, descrita em
docs/metricas/qualidade-do-produto.md. Como no Q-Rapids, valor sem dado é None, e não zero.

Uso, a partir da pasta dashboard/:
    python3 -m src.processo
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from . import aceitacao, qualidade
from .config import MODO_ACEITAS, RAW_DATA_DIR
from .metrics import pontos_distintos
from .qualidade import BRASILIA, MARCOS, faixa, media_ponderada

# O processo é avaliado nas releases major, e cada uma vai do fim da anterior até a sua data.
RELEASES = {k: MARCOS[k] for k in ("R1", "R2", "R3")}
REPOSITORIOS_DE_PRODUTO = ("APP", "IA")
# Execuções puladas ou canceladas não dizem se o código está estável.
CONCLUSOES_CONTADAS = {"success", "failure"}

# P2 é o APC do Agile EVM (RPC ÷ PRP da release, como na aba de EVM) e P3 mede a variação
# do PRP durante cada sprint.
INDICADORES = {
    "P1": "Estabilidade do CI",
    "P2": "APC: escopo concluído",
    "P3": "Estabilidade do PRP",
}
PESOS = {"P1": 1, "P2": 1, "P3": 1}


def _data(texto: Optional[str]) -> Optional[datetime]:
    if not texto:
        return None
    return datetime.fromisoformat(texto.replace("Z", "+00:00"))


def release_de(momento: Optional[datetime]) -> Optional[str]:
    """A release major em que o momento cai."""
    if momento is None:
        return None
    for nome, fim in sorted(RELEASES.items(), key=lambda item: item[1]):
        if momento <= fim:
            return nome
    return None


# ---------------------------------------------------------------------------
# Sprints
# ---------------------------------------------------------------------------

def sprints(pasta: str = RAW_DATA_DIR, modo: str = MODO_ACEITAS) -> List[Dict[str, Any]]:
    """
    Sprints com pontos planejados, em ordem. Cada sprint pertence à release em que
    termina. Sprints sem pontos planejados, como as de preparação, ficam de fora.

    `entregues` segue o `modo`: só os pontos das histórias aceitas (fechadas) ou também os
    das que estão em Aceitação PO (`aguardando`), como em `aceitacao.pontos_entregues`.
    Os pontos aceitos ficam sempre em `aceitos`.
    """
    dados = qualidade._ler(os.path.join(pasta, "zenhub_analytics.json")) or {}
    resultado = []
    for nome, info in dados.get("sprints_velocity", {}).items():
        planejados = float(info.get("total_points") or 0)
        if planejados <= 0:
            continue
        fim = _data(info.get("end_at"))
        resultado.append({
            "nome": nome,
            "estado": info.get("state"),
            "inicio": _data(info.get("start_at")),
            "fim": fim,
            "release": release_de(fim),
            "planejados": planejados,
            "aceitos": float(info.get("delivered_story_points") or 0),
            "adicionados": float(info.get("points_added") or 0),
            "issues": info.get("issues") if isinstance(info.get("issues"), list) else None,
            "issues_total": info.get("issues_total"),
        })
    resultado = sorted(resultado, key=lambda s: s["inicio"])
    manual = aceitacao.numeros_manuais(qualidade._ler(os.path.join(pasta, "aceitacao_po_manual.json")))
    aceitacao.marcar_aguardando(resultado, manual=manual, coletada=dados.get("colunas_coletadas"))
    for sprint in resultado:
        sprint["aguardando"] = sprint["aguardando_pontos"]
        sprint["entregues"] = aceitacao.pontos_entregues(sprint["aceitos"], sprint["aguardando"], modo)
    return resultado


def _entrega(sprint: Dict[str, Any]) -> float:
    return min(1.0, sprint["entregues"] / sprint["planejados"])


def prp_e_rpc_da_release(da_release: List[Dict[str, Any]]) -> tuple:
    """
    PRP e RPC da release, pelo mesmo cálculo da aba de EVM: (prp, rpc, aproximado).

    O PRP conta cada história uma vez só, mesmo que ela passe de uma sprint para a outra
    (`metrics.pontos_distintos`). O RPC soma os pontos entregues das sprints, e o ZenHub
    conta a história entregue só na sprint em que ela fecha.
    """
    prp, aproximado = pontos_distintos([
        {"total_points": s["planejados"], "issues": s["issues"], "issues_total": s["issues_total"]}
        for s in da_release
    ])
    return prp, sum(s["entregues"] for s in da_release), aproximado


def _apc(prp: float, rpc: float) -> Optional[float]:
    return min(1.0, rpc / prp) if prp > 0 else None


def _escopo(sprint: Dict[str, Any]) -> float:
    # Parte do comprometido final que já estava na sprint quando ela começou.
    return max(0.0, (sprint["planejados"] - sprint["adicionados"]) / sprint["planejados"])


# ---------------------------------------------------------------------------
# CI
# ---------------------------------------------------------------------------

def execucoes_por_release(pasta: str = RAW_DATA_DIR) -> Dict[str, Dict[str, int]]:
    """Execuções concluídas com sucesso e com falha, por release, somando APP e IA."""
    contagem: Dict[str, Dict[str, int]] = {}
    for repo in REPOSITORIOS_DE_PRODUTO:
        dados = qualidade._ler(os.path.join(pasta, f"GitHub_API-Runs-{repo}.json")) or {}
        for execucao in dados.get("workflow_runs", []):
            if execucao.get("conclusion") not in CONCLUSOES_CONTADAS:
                continue
            release = release_de(_data(execucao.get("created_at")))
            if release:
                item = contagem.setdefault(release, {"success": 0, "failure": 0})
                item[execucao["conclusion"]] += 1
    return contagem


# ---------------------------------------------------------------------------
# Defeitos
# ---------------------------------------------------------------------------

def bugs(pasta: str = RAW_DATA_DIR) -> Optional[List[Dict[str, Any]]]:
    """Issues com o rótulo bug de APP e IA, ou None se algum dos arquivos ainda não foi coletado."""
    lista = []
    for repo in REPOSITORIOS_DE_PRODUTO:
        dados = qualidade._ler(os.path.join(pasta, f"GitHub_API-Bugs-{repo}.json"))
        if dados is None:
            return None
        for bug in dados.get("bugs", []):
            lista.append({**bug, "repositorio": repo, "aberta_em": _data(bug.get("aberta_em")),
                          "fechada_em": _data(bug.get("fechada_em"))})
    return lista


def _problemas_de_confiabilidade(avaliacao: Optional[Dict[str, Any]]) -> Optional[int]:
    """Arquivos com problema de confiabilidade aberto no SonarCloud na versão (1 − m8, em quantidade)."""
    if not avaliacao:
        return None
    m8 = avaliacao["metricas"]["m8"]
    return None if m8["valor"] is None else len(m8["fora_do_limiar"])


# ---------------------------------------------------------------------------
# Indicadores e comparação
# ---------------------------------------------------------------------------

def indicadores_por_release(pasta: str = RAW_DATA_DIR, modo: str = MODO_ACEITAS) -> Dict[str, Dict[str, Any]]:
    """P1 a P3 e o índice de processo P de cada release que já tem dados. `modo` escolhe os pontos de P2."""
    lista_sprints = sprints(pasta, modo)
    execucoes = execucoes_por_release(pasta)
    resultado = {}
    for release in RELEASES:
        da_release = [s for s in lista_sprints if s["release"] == release]
        ci = execucoes.get(release)
        if not da_release and not ci:
            continue
        prp, rpc, prp_aproximado = prp_e_rpc_da_release(da_release)
        valores = {
            "P1": ci["success"] / (ci["success"] + ci["failure"]) if ci else None,
            # APC da release, igual ao da aba de EVM: cada história entra uma vez no PRP.
            "P2": _apc(prp, rpc) if da_release else None,
            # Média por sprint: a variação do PRP acontece dentro de cada sprint.
            "P3": sum(_escopo(s) for s in da_release) / len(da_release) if da_release else None,
        }
        indice, parcial = media_ponderada(valores, PESOS)
        resultado[release] = {
            "indicadores": valores,
            "P": indice,
            "parcial": parcial and indice is not None,
            "sprints": [s["nome"] for s in da_release],
            "em_andamento": any(s["estado"] != "CLOSED" for s in da_release),
            "execucoes": ci,
            "prp": prp,
            "rpc": rpc,
            "prp_aproximado": prp_aproximado,
            "pontos_aceitos": sum(s["aceitos"] for s in da_release),
            "pontos_em_aceitacao": sum(s["aguardando"] for s in da_release),
        }
    return resultado


def comparativo(pasta: str = RAW_DATA_DIR, modo: str = MODO_ACEITAS) -> Dict[str, Dict[str, Any]]:
    """
    Velocidade, cobertura e defeitos de cada release, como pede o cronograma do DA-R2.

    A velocidade é a média dos pontos de história entregues por sprint (só os aceitos ou, no
    modo "entregues", também os que estão em Aceitação PO); os pontos planejados acompanham
    o número, porque explicam uma velocidade baixa.
    """
    lista_sprints = sprints(pasta, modo)
    marcos = qualidade.por_marco(qualidade.avaliar_repositorio("APP", pasta))
    versoes = {v["versao"]: v for v in qualidade.carregar_versoes("APP", pasta)}
    lista_bugs = bugs(pasta)
    resultado = {}
    for release, fim in RELEASES.items():
        da_release = [s for s in lista_sprints if s["release"] == release]
        avaliacao = marcos.get(release)
        if not da_release and not avaliacao:
            continue
        inicio = max((d for d in RELEASES.values() if d < fim), default=None)
        cobertura = versoes[avaliacao["versao"]]["base"].get("coverage") if avaliacao else None
        resultado[release] = {
            "versao": avaliacao["versao"] if avaliacao else None,
            "sprints": [s["nome"] for s in da_release],
            "velocidade": (sum(s["entregues"] for s in da_release) / len(da_release)) if da_release else None,
            "planejados_por_sprint": (sum(s["planejados"] for s in da_release) / len(da_release)) if da_release else None,
            "pontos_em_aceitacao": sum(s["aguardando"] for s in da_release),
            "cobertura": cobertura,
            "bugs_abertos_na_release": None if lista_bugs is None else len(
                [b for b in lista_bugs if b["aberta_em"] and b["aberta_em"] <= fim
                 and (inicio is None or b["aberta_em"] > inicio)]),
            "arquivos_com_defeito_provavel": _problemas_de_confiabilidade(avaliacao),
        }
    return resultado


def variacao_do_prp(pasta: str = RAW_DATA_DIR, modo: str = MODO_ACEITAS) -> List[Dict[str, Any]]:
    """
    Uma linha por sprint com o PRP no início e no fim, os pontos adicionados, o RPC e o APC.

    O PRP do fim é o total de pontos de história da sprint no ZenHub. O do início é esse total
    menos os pontos adicionados com a sprint em andamento, e nunca fica negativo (uma história
    tirada da sprint pode fazer os adicionados passarem do total). O RPC são os pontos
    entregues, pela regra do `modo`, e o APC é RPC ÷ PRP do fim, da sprint. O APC da release,
    que é o P2, conta cada história uma vez e está em `indicadores_por_release`.
    """
    linhas = []
    for s in sprints(pasta, modo):
        linhas.append({
            "sprint": s["nome"],
            "release": s["release"],
            "prp_inicio": max(0.0, s["planejados"] - s["adicionados"]),
            "adicionados": s["adicionados"],
            "prp_fim": s["planejados"],
            "rpc": s["entregues"],
            "em_aceitacao": s["aguardando"],
            "apc": _entrega(s),
            "em_andamento": s["estado"] != "CLOSED",
        })
    return linhas


if __name__ == "__main__":
    fmt = qualidade._fmt
    print("## Indicadores de processo\n")
    print("| Release | Sprints | " + " | ".join(f"{k} {v}" for k, v in INDICADORES.items()) + " | P |")
    print("|---|---|" + "---:|" * (len(INDICADORES) + 1))
    for release, item in indicadores_por_release().items():
        valores = " | ".join(fmt(item["indicadores"][k]) for k in INDICADORES)
        andamento = " (em andamento)" if item["em_andamento"] else ""
        print(f"| {release}{andamento} | {', '.join(item['sprints'])} | {valores} | "
              f"{fmt(item['P'], item['parcial'])} {faixa(item['P'])} |")
    print("\n## Comparação R1 × R2\n")
    print("| Release | Versão | Velocidade (pontos/sprint) | Planejados (pontos/sprint) | Cobertura | "
          "Issues de bug abertas | Arquivos com defeito provável |")
    print("|---|---|---:|---:|---:|---:|---:|")
    for release, item in comparativo().items():
        cobertura = f"{item['cobertura']:.1f}%".replace(".", ",") if item["cobertura"] is not None else "n/m"
        print(f"| {release} | {item['versao']} | {fmt(item['velocidade'])} | {fmt(item['planejados_por_sprint'])} | "
              f"{cobertura} | {item['bugs_abertos_na_release']} | {item['arquivos_com_defeito_provavel']} |")
