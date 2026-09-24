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
WEEKLY_SPRINT_BUDGET_BRL = 3200.0

THEME_COLORS = {
    "primary": "#38BDF8",       # Sky Blue brilhante
    "secondary": "#34D399",     # Emerald brilhante (sucesso / no prazo)
    "accent": "#A78BFA",        # Roxo / Lilás claro
    "warning": "#FBBF24",       # Âmbar visível
    "danger": "#F87171",        # Vermelho claro visível
}