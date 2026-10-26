import os

ORGANIZATION = "fga-eps-mds"
PROJECT_PREFIX = "2026.2-UNB-FCTE_UNIEURO_MED"

REPOSITORIES = {
    "DOCS": f"{PROJECT_PREFIX}-DOCS",
    "IA": f"{PROJECT_PREFIX}-IA",
    "APP": f"{PROJECT_PREFIX}-APP",
}

REPOS_CONFIG = {
    "IA": {
        "name": "Módulo de Inteligência Artificial",
        "lang": "py",
        "sonar_key": f"{ORGANIZATION}_{REPOSITORIES['IA']}"
    },
    "APP": {
        "name": "Aplicativo Mobile",
        "lang": "ts",
        "sonar_key": f"{ORGANIZATION}_{REPOSITORIES['APP']}"
    }
}

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_DASH_ROOT = os.path.dirname(_CURRENT_DIR)
_DOCS_ROOT = os.path.dirname(_DASH_ROOT)

RAW_DATA_DIR = os.path.join(_DOCS_ROOT, "analytics-raw-data")
ANALYSIS_NOTES_DIR = os.path.join(_DASH_ROOT, "historico_analises")

FUSO_BRASILIA = "America/Sao_Paulo"

# Releases do projeto, com o orçamento (BAC) de cada uma. O Agile EVM é calculado
# por release, não por sprint. Datas do cronograma (docs/processo/cronograma.md).
# Os valores de BAC são os da seção 5 do Plano de Custos v2.0
# (docs/processo/plano_de_custos.md, PR #97), calculados pelo valor da hora. Este é o
# único lugar a atualizar quando o plano mudar.
RELEASES = [
    {"id": "R1", "nome": "Release 1", "inicio": "2026-08-10", "fim": "2026-09-28", "bac_brl": 62746.77},
    {"id": "R2", "nome": "Release 2", "inicio": "2026-09-29", "fim": "2026-10-26", "bac_brl": 12595.73},
    {"id": "R3", "nome": "Release 3", "inicio": "2026-10-27", "fim": "2026-11-30", "bac_brl": 15744.66},
    {"id": "RF", "nome": "Release final", "inicio": "2026-12-01", "fim": "2026-12-07", "bac_brl": 3148.93},
]

# Pontos entregues. Uma história só é fechada depois do aceite do PO (Ata 08), e o ZenHub só
# conta como entregue a história fechada. Por decisão da equipe, o painel mostra também as
# histórias da coluna "Aceitação PO": código entregue, aguardando o aceite. O modo escolhe o
# que entra nos pontos entregues, e a mesma escolha vale para EVM, velocity, burn e processo.
# O padrão conta só as aceitas, como o Agile EVM e a Ata 08; o outro modo é uma visão opcional.
COLUNAS_ACEITACAO = ("Aceitação PO",)
MODO_ACEITAS = "aceitas"
MODO_ENTREGUES = "entregues"
MODO_PADRAO = MODO_ACEITAS
ROTULOS_MODO = {
    MODO_ACEITAS: "Somente histórias aceitas (fechadas)",
    MODO_ENTREGUES: "Aceitas + em Aceitação PO",
}

THEME_COLORS = {
    "primary": "#38BDF8",       # Sky Blue brilhante
    "secondary": "#34D399",     # Emerald brilhante (sucesso / no prazo)
    "accent": "#A78BFA",        # Roxo / Lilás claro
    "warning": "#FBBF24",       # Âmbar visível
    "danger": "#F87171",        # Vermelho claro visível
}