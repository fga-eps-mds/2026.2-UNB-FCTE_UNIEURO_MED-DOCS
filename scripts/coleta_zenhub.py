#!/usr/bin/env python3
"""
Coleta as métricas de sprint do Zenhub e grava analytics/raw-data/zenhub_analytics.json,
no formato que o data_layer do dashboard espera.

Requer a variável de ambiente ZENHUB_TOKEN. Sem ela, o script apenas avisa e sai
sem erro, para não derrubar a esteira enquanto o segredo não estiver cadastrado.

Uso:
    ZENHUB_TOKEN=... python3 scripts/coleta_zenhub.py
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.zenhub.com/public/graphql"
WORKSPACE_ID = "6a8c447d652b15002979b829"

DESTINO = Path(__file__).resolve().parent.parent / "analytics" / "raw-data" / "zenhub_analytics.json"

CONSULTA = """
query($id: ID!) {
  workspace(id: $id) {
    displayName
    sprints(first: 50) {
      nodes {
        name
        state
        startAt
        endAt
        totalPoints
        completedPoints
        closedIssuesCount
        id
        issues(first: 100) { totalCount nodes { estimate { value } } }
      }
    }
  }
}
"""


# O Zenhub recusa scopeChange em consulta com várias sprints
# ("Batched queries are disabled"), então ele é buscado sprint a sprint.
CONSULTA_ESCOPO = """
query($id: ID!) {
  node(id: $id) {
    ... on Sprint {
      scopeChange(first: 100) { nodes { action estimateValue effectiveAt } }
    }
  }
}
"""


def executar(token, consulta, variaveis):
    corpo = json.dumps({"query": consulta, "variables": variaveis}).encode()
    req = urllib.request.Request(
        API,
        data=corpo,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        dados = json.loads(resp.read())

    if "errors" in dados:
        raise RuntimeError(dados["errors"][0].get("message", "erro desconhecido"))
    return dados["data"]


def consultar(token):
    workspace = executar(token, CONSULTA, {"id": WORKSPACE_ID})["workspace"]

    for sprint in workspace["sprints"]["nodes"]:
        try:
            no = executar(token, CONSULTA_ESCOPO, {"id": sprint["id"]})["node"]
            sprint["scopeChange"] = (no or {}).get("scopeChange", {"nodes": []})
        except (urllib.error.URLError, RuntimeError, KeyError):
            # Sem o histórico de escopo, a sprint segue com os demais dados.
            sprint["scopeChange"] = {"nodes": []}

    return workspace


def pontos_adicionados(sprint):
    """Soma os pontos que entraram na sprint depois de iniciada, menos os que saíram."""
    total = 0.0
    for ev in sprint.get("scopeChange", {}).get("nodes", []):
        valor = ev.get("estimateValue") or 0.0
        if ev.get("action") == "ISSUE_ADDED":
            total += valor
        elif ev.get("action") == "ISSUE_REMOVED":
            total -= valor
    return total


def montar(workspace):
    sprints = {}
    for s in workspace["sprints"]["nodes"]:
        issues = s.get("issues", {})
        nodes = issues.get("nodes", [])
        sem_estimativa = sum(1 for i in nodes if not i.get("estimate"))

        sprints[s["name"]] = {
            # Campos consumidos pelo data_layer do dashboard
            "delivered_story_points": s.get("completedPoints") or 0.0,
            "points_added": pontos_adicionados(s),
            "state": s.get("state", "CLOSED"),
            "start_at": s.get("startAt"),
            "end_at": s.get("endAt"),
            # Contexto adicional, útil para diagnóstico
            "total_points": s.get("totalPoints") or 0.0,
            "issues_total": issues.get("totalCount", 0),
            "issues_closed": s.get("closedIssuesCount", 0),
            "issues_sem_estimativa": sem_estimativa,
        }

    return {
        "workspace": workspace.get("displayName"),
        "coletado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sprints_velocity": sprints,
    }


def main():
    token = os.environ.get("ZENHUB_TOKEN", "").strip()
    if not token:
        print("ZENHUB_TOKEN não definido — coleta do Zenhub ignorada.", file=sys.stderr)
        return 0

    try:
        workspace = consultar(token)
    except (urllib.error.URLError, RuntimeError, KeyError) as e:
        print(f"Falha ao consultar o Zenhub: {e}", file=sys.stderr)
        print("Arquivo anterior preservado.", file=sys.stderr)
        return 0

    dados = montar(workspace)
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(json.dumps(dados, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    total = len(dados["sprints_velocity"])
    sem_est = sum(s["issues_sem_estimativa"] for s in dados["sprints_velocity"].values())
    print(f"{total} sprints coletadas em {DESTINO.name}")
    if sem_est:
        print(f"Atenção: {sem_est} issues sem estimativa — velocity e EVM ficam subestimados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
