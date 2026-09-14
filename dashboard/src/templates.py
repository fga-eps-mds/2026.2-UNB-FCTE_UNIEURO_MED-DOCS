"""
Templates e Utilitários de Apresentação
Preparado para a evolução modular da Release 2 (DA-R2: Qualidade de Produto Q-Rapids)
"""

def get_status_pill(status: str) -> str:
    """Retorna uma tag visual para status."""
    st_clean = status.lower()
    if "finalizada" in st_clean or "closed" in st_clean:
        return '<span class="badge-pill badge-ok">Finalizada</span>'
    elif "andamento" in st_clean or "active" in st_clean:
        return '<span class="badge-pill badge-warn">Em Andamento</span>'
    else:
        return '<span class="badge-pill badge-info">Planejada</span>'