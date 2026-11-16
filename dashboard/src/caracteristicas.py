"""
Qualidade por característica (ISO/IEC 25010), por release, a partir do histórico do SonarCloud.

O professor pediu que a qualidade fosse apresentada por característica, e não por cobertura,
duplicação e linhas de código (Ata 11). Este módulo calcula as quatro que o Plano de Qualidade
usa (segurança, confiabilidade, manutenibilidade e testabilidade) com a faixa e o sentido da
mudança em relação à release anterior.

Origem: `historico` de `analytics-raw-data/Sonar_API-Measures-*.json`, um ponto por análise do
SonarCloud. O valor de uma release é o último ponto até o fim dela (fim do dia em Brasília); a
release em andamento usa o ponto mais recente. Sem ponto até essa data, a característica é
"não medida", e nunca vira zero.

Faixas, do Plano de Qualidade (Tabela 5):
- segurança, confiabilidade e manutenibilidade usam a nota do SonarCloud: A é Adequado, B é
  Atenção e C a E é Crítico. A meta do plano é a nota A;
- testabilidade usa a cobertura: pelo menos 90% é Adequado (meta da cobertura global), de 80% a
  menos de 90% é Atenção (piso do quality gate) e abaixo de 80% é Crítico.

Limitações: o SonarCloud não separa os testes por nível, e os hotspots revisados e as evidências
E4 a E6 do plano ainda não são coletados. Essas lacunas aparecem como observação na característica.
"""

from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional

BRASILIA = timezone(timedelta(hours=-3))

ADEQUADO = "Adequado"
ATENCAO = "Atenção"
CRITICO = "Crítico"
NAO_MEDIDA = "Não medida"

MELHOROU = "Melhorou"
PIOROU = "Piorou"
MANTEVE = "Manteve"
PRIMEIRA = "Primeira medição"
SEM_COMPARACAO = "Sem comparação"

COBERTURA_ADEQUADA = 90.0
COBERTURA_MINIMA = 80.0
# Uma variação menor que isto, em nota ou em pontos de cobertura, é ruído, não mudança.
TOLERANCIA = 0.5

NOTAS = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}

_NOTA = "nota"
_COBERTURA = "cobertura"

CARACTERISTICAS = (
    {
        "chave": "seguranca", "nome": "Segurança", "metrica": "security_rating", "tipo": _NOTA,
        "apoio": ("vulnerabilities", "security_hotspots"),
        "observacao": "A nota considera só as vulnerabilidades abertas. Os hotspots revisados e as "
                      "evidências E4 a E6 do plano ainda não são coletados.",
    },
    {
        "chave": "confiabilidade", "nome": "Confiabilidade", "metrica": "reliability_rating", "tipo": _NOTA,
        "apoio": ("bugs",),
        "observacao": "A nota vem da gravidade do pior bug aberto.",
    },
    {
        "chave": "manutenibilidade", "nome": "Manutenibilidade", "metrica": "sqale_rating", "tipo": _NOTA,
        "apoio": ("code_smells", "sqale_index", "duplicated_lines_density"),
        "observacao": "A nota vem da razão entre o débito técnico estimado e o tamanho do código.",
    },
    {
        "chave": "testabilidade", "nome": "Testabilidade", "metrica": "coverage", "tipo": _COBERTURA,
        "apoio": ("tests", "test_failures"),
        "observacao": "A faixa vem da cobertura. O SonarCloud informa só o total de testes, sem "
                      "separar unitário, integração e funcional, então o nível do teste não é medido.",
        "niveis_medidos": False,
    },
)


def letra(nota: Optional[float]) -> Optional[str]:
    """Nota do SonarCloud (1.0 a 5.0) como letra, ou None se não existir."""
    if nota is None:
        return None
    return NOTAS.get(int(round(nota)))


def faixa_nota(nota: Optional[float]) -> str:
    if nota is None:
        return NAO_MEDIDA
    if nota <= 1:
        return ADEQUADO
    if nota <= 2:
        return ATENCAO
    return CRITICO


def faixa_cobertura(cobertura: Optional[float]) -> str:
    if cobertura is None:
        return NAO_MEDIDA
    if cobertura >= COBERTURA_ADEQUADA:
        return ADEQUADO
    if cobertura >= COBERTURA_MINIMA:
        return ATENCAO
    return CRITICO


def sentido(
    atual: Optional[float],
    anterior: Optional[float],
    menor_e_melhor: bool,
    ha_anterior: bool = True,
    tolerancia: float = TOLERANCIA,
) -> str:
    """Compara o valor da release com o da anterior. Sem um dos dois valores, não inventa sentido."""
    if atual is None:
        return SEM_COMPARACAO
    if not ha_anterior:
        return PRIMEIRA
    if anterior is None:
        return SEM_COMPARACAO
    diferenca = atual - anterior
    if abs(diferenca) < tolerancia:
        return MANTEVE
    melhorou = diferenca < 0 if menor_e_melhor else diferenca > 0
    return MELHOROU if melhorou else PIOROU


def _instante(texto: Any) -> Optional[datetime]:
    try:
        return datetime.strptime(str(texto), "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return None


def fim_da_release(release: Dict[str, Any]) -> datetime:
    """Primeiro instante depois do último dia da release, em Brasília. O ponto vale se vier antes dele."""
    dia = date.fromisoformat(release["fim"])
    return datetime.combine(dia + timedelta(days=1), time.min, tzinfo=BRASILIA)


def valor_ate(pontos: Optional[Iterable[Dict[str, Any]]], limite: datetime) -> Optional[float]:
    """Valor do último ponto anterior ao limite. Ponto sem data, sem valor ou ilegível é ignorado."""
    escolhido = None
    for ponto in pontos or []:
        instante = _instante(ponto.get("date"))
        if instante is None or instante >= limite:
            continue
        try:
            valor = float(ponto["value"])
        except (KeyError, TypeError, ValueError):
            continue
        if escolhido is None or instante >= escolhido[0]:
            escolhido = (instante, valor)
    return escolhido[1] if escolhido else None


def historico_por_metrica(dados: Optional[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Histórico do JSON de medidas do Sonar, por nome de métrica. As `medidas` da última coleta
    entram como o ponto mais recente: o histórico só traz as análises já fechadas.
    """
    dados = dados or {}
    resultado: Dict[str, List[Dict[str, Any]]] = {}
    for item in dados.get("historico") or []:
        nome = item.get("metric")
        if nome:
            resultado[nome] = list(item.get("history") or [])
    coletado = dados.get("coletado_em")
    if coletado and _instante(coletado):
        for nome, valor in (dados.get("medidas") or {}).items():
            resultado.setdefault(nome, []).append({"date": coletado, "value": valor})
    return resultado


def _caracteristica(spec: Dict[str, Any], historico, limite, anterior: Optional[Dict[str, Any]], ha_anterior: bool):
    valor = valor_ate(historico.get(spec["metrica"]), limite)
    e_nota = spec["tipo"] == _NOTA
    return {
        "chave": spec["chave"],
        "nome": spec["nome"],
        "metrica": spec["metrica"],
        "valor": valor,
        "nota": letra(valor) if e_nota else None,
        "faixa": faixa_nota(valor) if e_nota else faixa_cobertura(valor),
        "sentido": sentido(valor, anterior["valor"] if anterior else None,
                           menor_e_melhor=e_nota, ha_anterior=ha_anterior),
        "apoio": {m: valor_ate(historico.get(m), limite) for m in spec["apoio"]},
        "observacao": spec["observacao"],
        "niveis_medidos": spec.get("niveis_medidos", True),
    }


def calcular(
    historico: Dict[str, List[Dict[str, Any]]],
    releases: Iterable[Dict[str, Any]],
    hoje: Optional[datetime] = None,
) -> List[Dict[str, Any]]:
    """
    As quatro características de cada release que já começou, da mais antiga à mais recente.

    A release em andamento usa o ponto mais recente do histórico. `detalhe` traz todas as
    métricas do histórico com valor na data da release, para o bloco de detalhe da aba.
    """
    agora = (hoje or datetime.now(timezone.utc)).astimezone(BRASILIA)
    resultado: List[Dict[str, Any]] = []
    anteriores: Dict[str, Dict[str, Any]] = {}
    for release in releases:
        if date.fromisoformat(release["inicio"]) > agora.date():
            continue
        fim = fim_da_release(release)
        em_andamento = agora < fim
        limite = max(agora, fim) + timedelta(seconds=1) if em_andamento else fim
        itens = [
            _caracteristica(spec, historico, limite, anteriores.get(spec["chave"]), bool(resultado))
            for spec in CARACTERISTICAS
        ]
        anteriores = {c["chave"]: c for c in itens}
        detalhe = {m: v for m in historico if (v := valor_ate(historico[m], limite)) is not None}
        resultado.append({
            "release": release["id"],
            "nome": release.get("nome", release["id"]),
            "em_andamento": em_andamento,
            "caracteristicas": itens,
            "detalhe": detalhe,
        })
    return resultado
