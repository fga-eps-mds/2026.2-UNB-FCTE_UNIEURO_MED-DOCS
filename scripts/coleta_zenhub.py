#!/usr/bin/env python3
"""
Coleta as métricas de sprint do Zenhub e grava analytics-raw-data/zenhub_analytics.json,
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

DESTINO = Path(__file__).resolve().parent.parent / "analytics-raw-data" / "zenhub_analytics.json"

# Coluna (pipeline) em que a issue está agora. O dashboard usa a coluna "Aceitação PO" para
# somar os pontos das histórias entregues que aguardam o aceite do PO.
CAMPO_COLUNA = "pipelineIssue(workspaceId: $id) { pipeline { name } }"

# Campos pedidos de cada issue, além da estimativa, do mais completo ao mais simples.
# O identificador permite ao dashboard contar uma história uma só vez quando ela passa
# de uma sprint para a seguinte. Como a API não pôde ser conferida aqui, se o Zenhub
# recusar um campo a coleta tenta a variante seguinte, e a última é a consulta original.
VARIANTES_ISSUE = (f"id number {CAMPO_COLUNA}", "id number", "id", "")

# Segunda forma de ler a coluna: em vez de perguntar a cada issue onde ela está, pergunta ao
# workspace quais são as colunas e quais issues cada uma guarda. Só é usada se a primeira for
# recusada. Lê até 100 issues por coluna, o que sobra para a coluna Aceitação PO.
CONSULTA_COLUNAS = """
query($id: ID!) {
  workspace(id: $id) {
    pipelinesConnection(first: 50) {
      nodes { name issues(first: 100) { totalCount nodes { id number } } }
    }
  }
}
"""

# Introspecção: se nenhuma das duas formas funcionar, o log mostra os campos que a API tem de
# verdade, para a próxima correção usar os nomes certos em vez de adivinhar.
CONSULTA_TIPO = """
query($tipo: String!) { __type(name: $tipo) { fields { name } } }
"""
TIPOS_DO_DIAGNOSTICO = ("Issue", "Pipeline", "PipelineIssue", "Workspace")

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
        issues(first: 100) { totalCount nodes { estimate { value }__CAMPOS_ISSUE__ } }
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


def buscar_colunas(token):
    """Mapa {id da issue: nome da coluna}, lido pelas colunas do workspace."""
    dados = executar(token, CONSULTA_COLUNAS, {"id": WORKSPACE_ID})
    colunas = ((dados.get("workspace") or {}).get("pipelinesConnection") or {}).get("nodes")
    if colunas is None:
        raise RuntimeError("a resposta não trouxe as colunas do workspace")

    mapa = {}
    for coluna in colunas:
        issues = coluna.get("issues") or {}
        nos = issues.get("nodes") or []
        if issues.get("totalCount", len(nos)) > len(nos):
            print(
                f"Atenção: a coluna '{coluna.get('name')}' tem {issues['totalCount']} issues e só "
                f"{len(nos)} foram lidas.",
                file=sys.stderr,
            )
        for issue in nos:
            if issue.get("id"):
                mapa[issue["id"]] = coluna.get("name")
    return mapa


def diagnosticar_esquema(token):
    """Imprime no log os campos dos tipos que importam, para corrigir a consulta com os nomes reais."""
    for tipo in TIPOS_DO_DIAGNOSTICO:
        try:
            dados = executar(token, CONSULTA_TIPO, {"tipo": tipo})
            campos = [c["name"] for c in ((dados.get("__type") or {}).get("fields") or [])]
        except (urllib.error.URLError, RuntimeError, KeyError, TypeError) as e:
            print(f"Esquema: não foi possível listar os campos de {tipo}: {e}", file=sys.stderr)
            return
        print(f"Esquema: campos de {tipo}: {', '.join(campos) if campos else '(tipo não encontrado)'}", file=sys.stderr)


def construir_consulta(campos_issue):
    return CONSULTA.replace("__CAMPOS_ISSUE__", f" {campos_issue}" if campos_issue else "")


def consultar(token):
    erro = None
    for campos in VARIANTES_ISSUE:
        try:
            workspace = executar(token, construir_consulta(campos), {"id": WORKSPACE_ID})["workspace"]
        except RuntimeError as e:
            erro = e
            print(f"Consulta com os campos '{campos or 'somente estimativa'}' recusada: {e}", file=sys.stderr)
            continue
        workspace["issues_detalhadas"] = bool(campos)
        workspace["issues_com_coluna"] = CAMPO_COLUNA in campos
        break
    else:
        raise erro

    workspace["colunas_fonte"] = "issue" if workspace["issues_com_coluna"] else None
    workspace["colunas_por_id"] = None
    if not workspace["issues_com_coluna"]:
        # A primeira forma foi recusada: tenta ler as colunas pelo workspace e juntar pelo id.
        if workspace["issues_detalhadas"]:
            try:
                workspace["colunas_por_id"] = buscar_colunas(token)
                workspace["colunas_fonte"] = "workspace"
                workspace["issues_com_coluna"] = True
            except (urllib.error.URLError, RuntimeError, KeyError, TypeError) as e:
                print(f"Leitura das colunas pelo workspace recusada: {e}", file=sys.stderr)
        if not workspace["issues_com_coluna"]:
            print("A coluna das issues não pôde ser coletada pelas duas formas.", file=sys.stderr)
            diagnosticar_esquema(token)

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


def _resumir_issue(issue, com_coluna, colunas_por_id=None):
    resumo = {
        "id": issue.get("id"),
        "numero": issue.get("number"),
        "estimativa": (issue.get("estimate") or {}).get("value"),
    }
    if com_coluna:
        coluna = (((issue.get("pipelineIssue") or {}).get("pipeline")) or {}).get("name")
        if coluna is None and colunas_por_id:
            coluna = colunas_por_id.get(issue.get("id"))
        resumo["coluna"] = coluna
    return resumo


def montar(workspace):
    sprints = {}
    for s in workspace["sprints"]["nodes"]:
        issues = s.get("issues", {})
        nodes = issues.get("nodes", [])
        sem_estimativa = sum(1 for i in nodes if not i.get("estimate"))

        detalhe = {}
        if workspace.get("issues_detalhadas"):
            # Uma entrada por issue, para contar cada história uma só vez entre sprints.
            detalhe["issues"] = [
                _resumir_issue(i, workspace.get("issues_com_coluna"), workspace.get("colunas_por_id"))
                for i in nodes
            ]

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
            **detalhe,
        }

    return {
        "workspace": workspace.get("displayName"),
        "coletado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        # Diz se a coluna das issues foi lida, e por qual forma. Sem isso, uma coluna Aceitação PO
        # vazia seria igual a uma coluna que nunca foi coletada.
        "colunas_coletadas": bool(workspace.get("issues_com_coluna")),
        "colunas_fonte": workspace.get("colunas_fonte"),
        "sprints_velocity": sprints,
    }


def resumir_colunas(dados):
    """Quantas issues distintas há em cada coluna, para o log da coleta mostrar o que foi lido."""
    por_coluna = {}
    vistas = set()
    for sprint in dados["sprints_velocity"].values():
        for issue in sprint.get("issues") or []:
            chave = issue.get("id") if issue.get("id") is not None else (issue.get("numero"), id(issue))
            if chave in vistas:
                continue
            vistas.add(chave)
            coluna = issue.get("coluna") or "(coluna não identificada)"
            por_coluna[coluna] = por_coluna.get(coluna, 0) + 1
    return por_coluna


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
    if dados["colunas_coletadas"]:
        resumo = ", ".join(f"{nome}: {n}" for nome, n in sorted(resumir_colunas(dados).items()))
        print(f"Colunas das issues lidas (forma: {dados['colunas_fonte']}). Issues por coluna: {resumo}")
    else:
        print(
            "Atenção: a coluna das issues não foi coletada. Os pontos em Aceitação PO não aparecem "
            "no dashboard. Veja acima as linhas 'recusada' e 'Esquema'."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
