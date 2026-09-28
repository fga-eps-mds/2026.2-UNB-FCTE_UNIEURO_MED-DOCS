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

INITIAL_PLANNED_SPRINTS_R1 = 5
INITIAL_PLANNED_POINTS_PRP0 = 65.0
# Sincronizado com a linha de base semanal do Plano de Custos
# (docs/processo/plano_de_custos.md, seção 4: BAC = R$ 58.144,41 / 17 semanas).
WEEKLY_SPRINT_BUDGET_BRL = 3613.49
# Cadência real confirmada em analytics-raw-data/zenhub_analytics.json: cada
# sprint cobre 14 dias corridos (ex: 17/08-31/08, 31/08-14/09), não 1 semana.
SPRINT_DURATION_WEEKS = 2
# Custo por sprint usado no EVM = taxa semanal do Plano de Custos × semanas/sprint.
SPRINT_BUDGET_BRL = round(WEEKLY_SPRINT_BUDGET_BRL * SPRINT_DURATION_WEEKS, 2)

THEME_COLORS = {
    "primary": "#38BDF8",       # Sky Blue brilhante
    "secondary": "#34D399",     # Emerald brilhante (sucesso / no prazo)
    "accent": "#A78BFA",        # Roxo / Lilás claro
    "warning": "#FBBF24",       # Âmbar visível
    "danger": "#F87171",        # Vermelho claro visível
}