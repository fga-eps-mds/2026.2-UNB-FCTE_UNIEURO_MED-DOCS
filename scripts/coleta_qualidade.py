#!/usr/bin/env python3
"""
Coleta os dados que o cálculo do Q-Rapids precisa além do .json de cada release:

- os problemas do SonarCloud de APP e IA, por branch, inclusive os já resolvidos,
  para as métricas m7 e m8 do Plano de Qualidade (problemas graves de
  manutenibilidade e problemas de confiabilidade por arquivo);
- a branch de destino de cada release, porque o .json da release mede essa branch
  e os problemas precisam ser lidos da mesma;
- as issues com o rótulo bug, para a comparação de defeitos entre as releases.

Grava, por repositório:
    analytics-raw-data/Sonar_API-Issues-<repositório>.json
    analytics-raw-data/GitHub_API-Releases-<repositório>.json
    analytics-raw-data/GitHub_API-Bugs-<repositório>.json

A API do SonarCloud é aberta para projetos públicos. A do GitHub usa GH_TOKEN
quando ele existe; sem token, o limite é de 60 consultas por hora, o que basta
para rodar o script à mão. Quando uma fonte falha, o arquivo anterior é preservado.

Uso:
    python3 scripts/coleta_qualidade.py
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ORGANIZACAO = "fga-eps-mds"
PREFIXO = "2026.2-UNB-FCTE_UNIEURO_MED"
REPOSITORIOS = ["APP", "IA"]
# O pipeline de release roda nos merges para a main e para a develop.
BRANCHES = ["main", "develop"]

SONAR = "https://sonarcloud.io/api"
GITHUB = "https://api.github.com"
PASTA = Path(__file__).resolve().parent.parent / "analytics-raw-data"


def obter_json(url, token=None):
    cabecalhos = {"Accept": "application/json", "User-Agent": "med-coleta-qualidade"}
    if token:
        cabecalhos["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=cabecalhos), timeout=60) as resposta:
        return json.load(resposta)


def agora():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gravar(nome, dados):
    destino = PASTA / nome
    destino.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return destino


def problemas_da_branch(chave, branch):
    """Todos os problemas da branch, abertos e resolvidos, com as datas de criação e de
    fechamento, que permitem saber o que estava aberto no momento de cada release."""
    problemas, pagina = [], 1
    while True:
        consulta = urllib.parse.urlencode({"componentKeys": chave, "branch": branch, "ps": 500, "p": pagina})
        resposta = obter_json(f"{SONAR}/issues/search?{consulta}")
        for problema in resposta.get("issues", []):
            problemas.append({
                "chave": problema["key"],
                # O componente vem como "<projeto>:<caminho>"; o .json da release usa o caminho.
                "arquivo": problema["component"].split(":", 1)[-1],
                "regra": problema.get("rule"),
                "status": problema.get("status"),
                "resolucao": problema.get("resolution"),
                "criado_em": problema.get("creationDate"),
                "fechado_em": problema.get("closeDate"),
                "impactos": [
                    {"qualidade": i["softwareQuality"], "severidade": i["severity"]}
                    for i in problema.get("impacts", [])
                ],
            })
        if pagina * 500 >= resposta.get("paging", {}).get("total", 0):
            return problemas
        pagina += 1


def coletar_problemas(repo):
    chave = f"{ORGANIZACAO}_{PREFIXO}-{repo}"
    existentes = {r["name"] for r in obter_json(f"{SONAR}/project_branches/list?project={chave}").get("branches", [])}
    branches = {}
    for branch in BRANCHES:
        # A IA, por exemplo, pode ainda não ter a develop analisada no SonarCloud.
        branches[branch] = problemas_da_branch(chave, branch) if branch in existentes else None
    return {"repositorio": repo, "projeto_sonar": chave, "coletado_em": agora(), "branches": branches}


def branch_da_release(repo_completo, release, token):
    """A release guarda só o commit de merge. A branch de destino vem do PR desse commit."""
    alvo = release["target_commitish"]
    if alvo in BRANCHES:
        return alvo
    try:
        prs = obter_json(f"{GITHUB}/repos/{repo_completo}/commits/{alvo}/pulls", token)
    except urllib.error.HTTPError:
        return None
    for pr in prs:
        if pr.get("merge_commit_sha") == alvo:
            return pr["base"]["ref"]
    return None


def coletar_releases(repo, token):
    repo_completo = f"{ORGANIZACAO}/{PREFIXO}-{repo}"
    releases = obter_json(f"{GITHUB}/repos/{repo_completo}/releases?per_page=100", token)
    return {
        "repositorio": repo,
        "coletado_em": agora(),
        "releases": sorted(
            (
                {
                    "tag": r["tag_name"],
                    "commit": r["target_commitish"],
                    "publicada_em": r["published_at"],
                    "branch": branch_da_release(repo_completo, r, token),
                }
                for r in releases
            ),
            key=lambda r: r["publicada_em"] or "",
        ),
    }


def coletar_bugs(repo, token):
    repo_completo = f"{ORGANIZACAO}/{PREFIXO}-{repo}"
    issues = obter_json(f"{GITHUB}/repos/{repo_completo}/issues?labels=bug&state=all&per_page=100", token)
    return {
        "repositorio": repo,
        "coletado_em": agora(),
        "bugs": [
            {"numero": i["number"], "titulo": i["title"], "aberta_em": i["created_at"], "fechada_em": i["closed_at"]}
            # A API de issues também devolve pull requests.
            for i in issues if "pull_request" not in i
        ],
    }


def main():
    PASTA.mkdir(exist_ok=True)
    token = os.environ.get("GH_TOKEN")
    falhou = False
    for repo in REPOSITORIOS:
        for nome, coletar in (
            (f"Sonar_API-Issues-{repo}.json", lambda: coletar_problemas(repo)),
            (f"GitHub_API-Releases-{repo}.json", lambda: coletar_releases(repo, token)),
            (f"GitHub_API-Bugs-{repo}.json", lambda: coletar_bugs(repo, token)),
        ):
            try:
                print(f"{repo}: {gravar(nome, coletar()).name} gravado")
            except (urllib.error.URLError, KeyError, ValueError) as erro:
                print(f"::warning::Falha ao gerar {nome}: {erro}. Arquivo anterior preservado.")
                falhou = True
    # Falha de coleta não derruba a esteira: as demais fontes seguem.
    if falhou:
        print("::warning::Ao menos uma fonte de qualidade não pôde ser coletada")


if __name__ == "__main__":
    sys.exit(main())
