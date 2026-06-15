import streamlit as st

def render_footer():
    """Render the standardized dashboard/page footer"""
    st.markdown("<hr style='margin-top: 50px; margin-bottom: 20px; border-color: var(--surface-border);'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="footer-wrapper" style="text-align: center; font-size: 0.9rem; color: var(--text-secondary); width: 100%; margin: 0 auto;">
        <p style="margin: 0 0 5px 0;"><b>© 2026 Smart Resume</b></p>
        <p style="margin: 0;">Designed & Developed by <b>Naman Singh</b></p>
    </div>
    """, unsafe_allow_html=True)
