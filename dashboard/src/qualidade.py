"""
Qualidade interna do produto pelo modelo Q-Rapids, como define o Plano de Qualidade
(docs/processo/plano_de_qualidade.md, seção 3).

Entradas, todas em analytics-raw-data/:
- fga-eps-mds-<repositório>-<MM-DD-YYYY-HH-MM-SS>-vX.Y.Z.json: medidas do SonarCloud
  por arquivo, gravadas pelo pipeline de release de APP e IA;
- Sonar_API-Issues-<repositório>.json: problemas do SonarCloud por branch, para m7 e m8;
- GitHub_API-Releases-<repositório>.json: a branch que cada release mediu.

Uma métrica sem dado é "não medida" (None), nunca zero. Quando falta uma métrica ou um
fator, o peso dele é dividido entre os demais do mesmo nível, e o resultado é marcado
como parcial.

Uso, a partir da pasta dashboard/:
    python3 -m src.qualidade
"""

import glob
import json
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from .config import RAW_DATA_DIR

# Limiares por arquivo da Tabela 2 do plano.
LIMIAR_COMPLEXIDADE_POR_FUNCAO = 10
FAIXA_COMENTARIOS = (10, 30)
LIMIAR_DUPLICACAO = 5
LIMIAR_TESTE_RAPIDO_MS = 5000
LIMIAR_COBERTURA = 75
SEVERIDADES_GRAVES = {"HIGH", "BLOCKER"}

# Faixas da Tabela 3 e queda que pede análise entre duas releases seguidas (seção 3.5).
FAIXA_ADEQUADA = 0.80
FAIXA_ATENCAO = 0.60
QUEDA_RELEVANTE = 0.05

# O nome do .json da release usa o horário de Brasília, que não tem horário de verão.
BRASILIA = timezone(timedelta(hours=-3))

# Datas das releases major e da minor do cronograma. Cada marco é medido pela última
# versão gerada até o fim do dia.
MARCOS = {
    "R1": datetime(2026, 9, 28, 23, 59, 59, tzinfo=BRASILIA),
    "RM1": datetime(2026, 10, 13, 23, 59, 59, tzinfo=BRASILIA),
    "R2": datetime(2026, 10, 26, 23, 59, 59, tzinfo=BRASILIA),
    "R3": datetime(2026, 11, 30, 23, 59, 59, tzinfo=BRASILIA),
}

METRICAS = {
    "m1": "Densidade de arquivos não complexos",
    "m2": "Densidade de arquivos comentados",
    "m3": "Densidade de arquivos sem duplicação",
    "m4": "Taxa de sucesso dos testes",
    "m5": "Densidade de arquivos de teste rápidos",
    "m6": "Densidade de arquivos com cobertura adequada",
    "m7": "Densidade de arquivos sem problema grave de manutenibilidade",
    "m8": "Densidade de arquivos sem problema de confiabilidade",
}

# Seção 3.3: cada indicador é a média ponderada dos itens abaixo dele.
FATORES = {
    "QC": ("Qualidade do código", {"m1": 1, "m2": 1, "m3": 1}),
    "CB": ("Código bloqueante", {"m7": 1}),
    "T": ("Testabilidade", {"m5": 1, "m6": 2}),
    "ST": ("Sucesso dos testes", {"m4": 1}),
    "DP": ("Defeitos prováveis", {"m8": 1}),
}
CARACTERISTICAS = {
    "M": ("Manutenibilidade", {"QC": 1, "CB": 1, "T": 1}),
    "C": ("Confiabilidade", {"ST": 1, "DP": 1}),
}
INDICE = ("Q", "Índice de qualidade", {"M": 1, "C": 1})

_NOME_RELEASE = re.compile(
    r"fga-eps-mds-.+-(?P<repo>APP|IA)-(?P<data>\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-\d{2})-(?P<tag>v\d+\.\d+\.\d+)\.json$"
)


# ---------------------------------------------------------------------------
# Leitura
# ---------------------------------------------------------------------------

def _ler(caminho: str) -> Any:
    if not os.path.exists(caminho):
        return None
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def _medidas(componente: Dict[str, Any]) -> Dict[str, float]:
    valores = {}
    for medida in componente.get("measures", []):
        valor = medida.get("value")
        if valor is not None:
            valores[medida["metric"]] = float(valor)
    return valores


def _data_sonar(texto: Optional[str]) -> Optional[datetime]:
    # O SonarCloud escreve o fuso como "+0000", que o fromisoformat do Python 3.10 não lê.
    if not texto:
        return None
    return datetime.strptime(texto, "%Y-%m-%dT%H:%M:%S%z")


def carregar_versoes(repo: str, pasta: str = RAW_DATA_DIR) -> List[Dict[str, Any]]:
    """Versões do repositório em ordem cronológica, com os componentes do .json da release."""
    releases = _ler(os.path.join(pasta, f"GitHub_API-Releases-{repo}.json")) or {}
    branch_por_tag = {r["tag"]: r.get("branch") for r in releases.get("releases", [])}

    versoes = []
    for caminho in glob.glob(os.path.join(pasta, f"fga-eps-mds-*-{repo}-*.json")):
        nome = _NOME_RELEASE.search(os.path.basename(caminho))
        if not nome or nome.group("repo") != repo:
            continue
        dados = _ler(caminho) or {}
        versoes.append({
            "repositorio": repo,
            "versao": nome.group("tag"),
            "momento": datetime.strptime(nome.group("data"), "%m-%d-%Y-%H-%M-%S").replace(tzinfo=BRASILIA),
            "branch": branch_por_tag.get(nome.group("tag")),
            "arquivo": os.path.basename(caminho),
            "base": _medidas(dados.get("baseComponent", {})),
            "componentes": dados.get("components", []),
        })
    return sorted(versoes, key=lambda v: v["momento"])


def carregar_problemas(repo: str, pasta: str = RAW_DATA_DIR) -> Optional[Dict[str, Optional[List[Dict[str, Any]]]]]:
    dados = _ler(os.path.join(pasta, f"Sonar_API-Issues-{repo}.json"))
    return dados.get("branches") if dados else None


def problemas_abertos_em(problemas: List[Dict[str, Any]], momento: datetime) -> List[Dict[str, Any]]:
    """
    Problemas que estavam abertos no momento dado: criados até ele e não fechados antes.

    O SonarCloud registra como criação a data do commit da linha, e não a da análise que
    encontrou o problema. Por isso a reconstrução pode antecipar um problema em alguns dias.
    """
    abertos = []
    for problema in problemas:
        criado = _data_sonar(problema.get("criado_em"))
        fechado = _data_sonar(problema.get("fechado_em"))
        if criado and criado <= momento and (fechado is None or fechado > momento):
            abertos.append(problema)
    return abertos


# ---------------------------------------------------------------------------
# Métricas (Tabela 2)
# ---------------------------------------------------------------------------

def _densidade(conforme: List[str], conjunto: List[str]) -> Dict[str, Any]:
    """Densidade com o numerador, o denominador e os arquivos fora do limiar, para rastrear a causa."""
    fora = sorted(set(conjunto) - set(conforme))
    return {
        "valor": len(conforme) / len(conjunto) if conjunto else None,
        "conformes": len(conforme),
        "total": len(conjunto),
        "fora_do_limiar": fora,
    }


def _nao_medida(motivo: str) -> Dict[str, Any]:
    return {"valor": None, "conformes": 0, "total": 0, "fora_do_limiar": [], "motivo": motivo}


def calcular_metricas(
    componentes: List[Dict[str, Any]],
    base: Dict[str, float],
    problemas_abertos: Optional[List[Dict[str, Any]]],
) -> Dict[str, Dict[str, Any]]:
    """
    m1 a m8 de uma versão. `problemas_abertos` é None quando não há dado dos problemas
    do SonarCloud para a branch da versão, o que deixa m7 e m8 como não medidas.
    """
    codigo = {}
    testes = {}
    for componente in componentes:
        caminho = componente.get("path") or componente.get("key", "")
        if componente.get("qualifier") == "FIL":
            medidas = _medidas(componente)
            if medidas.get("ncloc", 0) > 0:
                codigo[caminho] = medidas
        elif componente.get("qualifier") == "UTS":
            testes[caminho] = _medidas(componente)

    a = list(codigo)
    a_f = [c for c in a if codigo[c].get("functions", 0) > 0]
    a_c = [c for c in a if "coverage" in codigo[c]]
    u = [t for t in testes if "test_execution_time" in testes[t]]

    m = {}
    if not a:
        motivo = "Versão sem arquivos de código no .json"
        for chave in METRICAS:
            m[chave] = _nao_medida(motivo)
        return m

    m["m1"] = _densidade(
        [c for c in a_f if codigo[c].get("complexity", 0) / codigo[c]["functions"] < LIMIAR_COMPLEXIDADE_POR_FUNCAO], a_f)
    m["m2"] = _densidade(
        [c for c in a if FAIXA_COMENTARIOS[0] < codigo[c].get("comment_lines_density", 0) < FAIXA_COMENTARIOS[1]], a)
    m["m3"] = _densidade([c for c in a if codigo[c].get("duplicated_lines_density", 0) < LIMIAR_DUPLICACAO], a)

    # m4 é medida do projeto. O componente base traz a soma; sem ele, soma-se arquivo a arquivo.
    total_testes = base.get("tests")
    if total_testes is None and any("tests" in t for t in testes.values()):
        total_testes = sum(t.get("tests", 0) for t in testes.values())
        erros = sum(t.get("test_errors", 0) for t in testes.values())
        falhas = sum(t.get("test_failures", 0) for t in testes.values())
    else:
        erros, falhas = base.get("test_errors", 0), base.get("test_failures", 0)
    if total_testes:
        sucesso = total_testes - erros - falhas
        m["m4"] = {"valor": sucesso / total_testes, "conformes": int(sucesso), "total": int(total_testes),
                   "fora_do_limiar": []}
    else:
        m["m4"] = _nao_medida("O SonarCloud não recebeu o resultado dos testes nesta versão")

    m["m5"] = (_densidade([t for t in u if testes[t]["test_execution_time"] < LIMIAR_TESTE_RAPIDO_MS], u)
               if u else _nao_medida("O SonarCloud não recebeu o tempo dos testes nesta versão"))
    m["m6"] = (_densidade([c for c in a_c if codigo[c]["coverage"] >= LIMIAR_COBERTURA], a_c)
               if a_c else _nao_medida("Nenhum arquivo com cobertura medida"))

    if problemas_abertos is None:
        motivo = "Sem os problemas do SonarCloud da branch desta versão"
        m["m7"] = _nao_medida(motivo)
        m["m8"] = _nao_medida(motivo)
    else:
        graves, confiabilidade = set(), set()
        for problema in problemas_abertos:
            for impacto in problema["impactos"]:
                if impacto["qualidade"] == "MAINTAINABILITY" and impacto["severidade"] in SEVERIDADES_GRAVES:
                    graves.add(problema["arquivo"])
                if impacto["qualidade"] == "RELIABILITY":
                    confiabilidade.add(problema["arquivo"])
        m["m7"] = _densidade([c for c in a if c not in graves], a)
        m["m8"] = _densidade([c for c in a if c not in confiabilidade], a)
    return m


# ---------------------------------------------------------------------------
# Agregação (seção 3.3)
# ---------------------------------------------------------------------------

def media_ponderada(valores: Dict[str, Optional[float]], pesos: Dict[str, float]) -> Tuple[Optional[float], bool]:
    """Média dos itens com valor. Devolve também se algum item faltou (resultado parcial)."""
    presentes = {k: p for k, p in pesos.items() if valores.get(k) is not None}
    if not presentes:
        return None, True
    total = sum(presentes.values())
    return sum(valores[k] * p for k, p in presentes.items()) / total, len(presentes) < len(pesos)


def agregar(metricas: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Fatores, características e índice Q. Um nível é parcial se algum item abaixo dele faltou."""
    valores = {k: v["valor"] for k, v in metricas.items()}
    parciais = {k: False for k in metricas}
    resultado = {}
    for nivel in (FATORES, CARACTERISTICAS, {INDICE[0]: INDICE[1:]}):
        for chave, (nome, pesos) in nivel.items():
            valor, faltou = media_ponderada(valores, pesos)
            parcial = faltou or any(parciais.get(k) for k in pesos)
            valores[chave], parciais[chave] = valor, parcial
            resultado[chave] = {"nome": nome, "valor": valor, "parcial": parcial and valor is not None}
    return resultado


def faixa(valor: Optional[float]) -> str:
    """Tabela 3 do plano."""
    if valor is None:
        return "Não medida"
    if valor >= FAIXA_ADEQUADA:
        return "Adequado"
    if valor >= FAIXA_ATENCAO:
        return "Atenção"
    return "Crítico"


# ---------------------------------------------------------------------------
# Avaliação por versão e por marco
# ---------------------------------------------------------------------------

def avaliar_repositorio(repo: str, pasta: str = RAW_DATA_DIR) -> List[Dict[str, Any]]:
    """Métricas e agregação de cada versão do repositório, em ordem cronológica."""
    problemas = carregar_problemas(repo, pasta)
    avaliacoes = []
    for versao in carregar_versoes(repo, pasta):
        da_branch = (problemas or {}).get(versao["branch"]) if versao["branch"] else None
        abertos = problemas_abertos_em(da_branch, versao["momento"]) if da_branch is not None else None
        metricas = calcular_metricas(versao["componentes"], versao["base"], abertos)
        avaliacoes.append({
            "repositorio": repo,
            "versao": versao["versao"],
            "momento": versao["momento"],
            "branch": versao["branch"],
            "arquivo": versao["arquivo"],
            "metricas": metricas,
            "agregacao": agregar(metricas),
        })
    return avaliacoes


def _valor(avaliacao: Dict[str, Any], chave: str) -> Optional[float]:
    if chave in avaliacao["metricas"]:
        return avaliacao["metricas"][chave]["valor"]
    return avaliacao["agregacao"][chave]["valor"]


def quedas(avaliacoes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Quedas de 0,05 ou mais em fator, característica ou Q entre duas versões medidas seguidas.
    Valores parciais ficam de fora: a diferença viria da métrica que passou a ser medida,
    e não de uma mudança no código.
    """
    chaves = list(FATORES) + list(CARACTERISTICAS) + [INDICE[0]]
    medidas = [a for a in avaliacoes if a["agregacao"]["Q"]["valor"] is not None]
    encontradas = []
    for anterior, atual in zip(medidas, medidas[1:]):
        for chave in chaves:
            if anterior["agregacao"][chave]["parcial"] or atual["agregacao"][chave]["parcial"]:
                continue
            antes, depois = _valor(anterior, chave), _valor(atual, chave)
            if antes is not None and depois is not None and antes - depois >= QUEDA_RELEVANTE - 1e-9:
                encontradas.append({"indicador": chave, "de": anterior["versao"], "para": atual["versao"],
                                    "antes": antes, "depois": depois})
    return encontradas


def por_marco(avaliacoes: List[Dict[str, Any]],
              marcos: Dict[str, datetime] = MARCOS) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    A versão que representa cada marco: a última medida até a data do marco. O marco só
    aparece se houve versão nova desde o marco anterior; antes da data, ele mostra a
    situação até a última versão.
    """
    com_dados = [a for a in avaliacoes if a["agregacao"]["Q"]["valor"] is not None]
    resultado, anterior = {}, None
    for nome, data in sorted(marcos.items(), key=lambda item: item[1]):
        novas = [a for a in com_dados if a["momento"] <= data and (anterior is None or a["momento"] > anterior)]
        resultado[nome] = novas[-1] if novas else None
        anterior = data
    return resultado


# ---------------------------------------------------------------------------
# Saída em Markdown, usada para gerar a página de resultados
# ---------------------------------------------------------------------------

def _fmt(valor: Optional[float], parcial: bool = False) -> str:
    if valor is None:
        return "n/m"
    texto = f"{valor:.2f}".replace(".", ",")
    return f"{texto}*" if parcial else texto


def tabela_marcos(repo: str, pasta: str = RAW_DATA_DIR) -> str:
    avaliacoes = avaliar_repositorio(repo, pasta)
    marcos = {k: v for k, v in por_marco(avaliacoes).items() if v}
    if not marcos:
        return f"Sem versão medida de {repo}."
    cabecalho = "| Indicador | " + " | ".join(f"{k} ({v['versao']})" for k, v in marcos.items()) + " |"
    linhas = [cabecalho, "|---|" + "---:|" * len(marcos)]
    for chave, nome in METRICAS.items():
        linhas.append(f"| {chave} {nome} | " + " | ".join(_fmt(v["metricas"][chave]["valor"]) for v in marcos.values()) + " |")
    for chave in list(FATORES) + list(CARACTERISTICAS) + [INDICE[0]]:
        nome = ({**FATORES, **CARACTERISTICAS}.get(chave) or INDICE[1:])[0]
        celulas = []
        for v in marcos.values():
            item = v["agregacao"][chave]
            celulas.append(f"{_fmt(item['valor'], item['parcial'])} {faixa(item['valor'])}")
        linhas.append(f"| **{chave}** {nome} | " + " | ".join(celulas) + " |")
    return "\n".join(linhas)


if __name__ == "__main__":
    for repositorio in ("APP", "IA"):
        print(f"## {repositorio}\n")
        avaliacoes = avaliar_repositorio(repositorio)
        print("| Versão | Branch | " + " | ".join(METRICAS) + " | QC | CB | T | ST | DP | M | C | Q |")
        print("|---|---|" + "---:|" * (len(METRICAS) + 8))
        for a in avaliacoes:
            m = [_fmt(a["metricas"][k]["valor"]) for k in METRICAS]
            g = [_fmt(a["agregacao"][k]["valor"], a["agregacao"][k]["parcial"])
                 for k in list(FATORES) + list(CARACTERISTICAS) + ["Q"]]
            print(f"| {a['versao']} | {a['branch']} | " + " | ".join(m + g) + " |")
        print(f"\n### Marcos\n\n{tabela_marcos(repositorio)}\n")
        for q in quedas(avaliacoes):
            print(f"- Queda de {q['indicador']}: {_fmt(q['antes'])} em {q['de']} → {_fmt(q['depois'])} em {q['para']}")
        print()
