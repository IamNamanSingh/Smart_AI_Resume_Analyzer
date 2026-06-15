import streamlit as st
from core.database import log_admin_action
from components.cards import page_header

def render_admin_page():
    """Render the administrator control panel / settings page"""
    page_header(
        "Administrator Settings",
        "Manage your administrator session and view system status."
    )

    with st.container(border=True):
        st.write("### Active Session Information")
        st.write(f"**Admin Email:** `{st.session_state.get('current_admin_email', 'N/A')}`")
        st.write("**Account Role:** System Administrator")
        st.write("**Access Status:** Authenticated")
        
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        if st.button("Log Out of Session", type="primary", use_container_width=True):
            try:
                log_admin_action(
                    st.session_state.get('current_admin_email'),
                    "logout"
                )
                st.session_state.is_admin = False
                st.session_state.current_admin_email = None
                st.success("Logged out successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error during logout: {str(e)}")
