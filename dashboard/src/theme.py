import streamlit as st
import plotly.graph_objects as go
from .config import THEME_COLORS


def apply_custom_theme():
    """Injeta estilos CSS de alto contraste com suporte total a temas Dark e Light."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Títulos do Streamlit com Alto Contraste */
    h1, h2, h3, h4, h5, h6, 
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: var(--text-color, #F8FAFC) !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }

    /* Cabeçalho Hero */
    .hero-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 55%, #0369A1 100%);
        color: #FFFFFF !important;
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .hero-title {
        font-size: 1.7rem;
        font-weight: 700;
        margin: 0;
        color: #FFFFFF !important;
        letter-spacing: -0.02em;
    }
    .hero-sub {
        font-size: 0.95rem;
        color: #E2E8F0 !important;
        margin-top: 0.4rem;
        margin-bottom: 0.6rem;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.25);
        color: #38BDF8 !important;
        border: 1px solid rgba(56, 189, 248, 0.5);
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    /* Cards de Indicadores (KPIs) com Alto Contraste */
    .kpi-container {
        background-color: var(--secondary-background-color, rgba(128, 128, 128, 0.12));
        border: 1px solid rgba(148, 163, 184, 0.35);
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        min-height: 115px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .kpi-container:hover {
        border-color: #38BDF8;
        transform: translateY(-2px);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .kpi-tag {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--text-color, #F1F5F9);
        letter-spacing: 0.04em;
    }
    .kpi-num {
        font-size: 1.85rem;
        font-weight: 800;
        color: var(--text-color, #F8FAFC);
        margin: 0.35rem 0;
        line-height: 1.2;
    }
    .kpi-desc {
        font-size: 0.82rem;
        color: var(--text-color, #CBD5E1);
        opacity: 0.9;
    }

    /* Caixas de Fórmulas e Informações */
    .formula-card {
        background-color: var(--secondary-background-color, rgba(128, 128, 128, 0.12));
        border: 1px solid rgba(148, 163, 184, 0.35);
        border-left: 4px solid #38BDF8;
        border-radius: 8px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.25rem;
    }
    .formula-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #38BDF8 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_kpi(label: str, value: str, subtext: str = "", color: str = None):
    """Renderiza card visual de KPI com contraste adaptativo."""
    color_style = f"style='color: {color};'" if color else ""
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-header">
            <span class="kpi-tag">{label}</span>
        </div>
        <div class="kpi-num" {color_style}>{value}</div>
        <div class="kpi-desc">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)


def get_plotly_layout(title: str, height: int = 380) -> dict:
    """Retorna layout Plotly com título em destaque nítido e sem sobreposição."""
    return dict(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=15, color="#38BDF8", family="Plus Jakarta Sans, sans-serif"),
            y=0.96,
            x=0,
            xanchor="left"
        ),
        height=height,
        margin=dict(l=25, r=25, t=65, b=60),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#CBD5E1", size=11),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.18)",
            zeroline=False,
            tickfont=dict(size=11, color="#94A3B8")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.18)",
            zeroline=False,
            tickfont=dict(size=11, color="#94A3B8")
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#CBD5E1")
        )
    )
