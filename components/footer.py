import streamlit as st

def render_footer():
    """Render the standardized dashboard/page footer"""
    st.markdown("<hr style='margin-top: 50px; margin-bottom: 20px; border-color: var(--surface-border);'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 0.9rem; color: var(--text-secondary);">
            <p style="margin: 0 0 5px 0;"><b>© 2026 Smart Resume AI</b></p>
            <p style="margin: 0;">Designed & Developed by <b>Naman Singh</b></p>
        </div>
        """, unsafe_allow_html=True)
