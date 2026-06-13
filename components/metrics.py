import streamlit as st

def render_metric_card(label, value, delta=None, icon=None):
    """Render a modern SaaS metric card with custom styling compatible with style.css"""
    icon_html = f'<div class="metric-icon"><i class="{icon}"></i></div>' if icon else ''
    delta_html = f'<div class="stat-note" style="margin-top: 4px; font-size: 0.85em; color: var(--accent);">{delta}</div>' if delta else ''
    
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-top">
                {icon_html}
                <div class="metric-label">{label}</div>
            </div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_metrics_grid(metrics_list):
    """Render a responsive grid of metric cards"""
    cols = st.columns(len(metrics_list))
    for col, m in zip(cols, metrics_list):
        with col:
            render_metric_card(
                label=m.get("label", ""),
                value=m.get("value", ""),
                delta=m.get("delta"),
                icon=m.get("icon")
            )
