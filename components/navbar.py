import streamlit as st
from core.database import verify_admin, log_admin_action

def render_navbar(page_keys, current_page):
    """Render the horizontal horizontal navigation bar with admin auth controls"""
    page_label_map = {name.lower().replace(' ', '_'): name for name in page_keys}
    default_label = page_label_map.get(current_page, page_keys[0])
    selected_index = page_keys.index(default_label) if default_label in page_keys else 0

    # Custom header layout with columns: logo on left, navigation centered, admin on right.
    col_logo, col_nav, col_admin = st.columns([2.0, 5.0, 2.0])

    with col_logo:
        st.markdown("""
        <div class="logo-wrapper">
            <h2>Smart Resume AI</h2>
        </div>
        """, unsafe_allow_html=True)

    with col_nav:
        st.markdown('<div class="topbar-start"></div>', unsafe_allow_html=True)
        selected_page = st.radio(
            '',
            options=page_keys,
            index=selected_index,
            horizontal=True,
            key='page_navigation'
        )

    with col_admin:
        if st.session_state.get('is_admin', False):
            with st.popover("👤 Admin"):
                st.write(f"**Email:** {st.session_state.get('current_admin_email')}")
                st.write("**Role:** System Administrator")
                if st.button("Logout", key="logout_button", use_container_width=True):
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
        else:
            with st.popover("🔐 Admin Login"):
                admin_email_input = st.text_input(
                    "Email",
                    key="admin_email_input"
                )

                admin_password = st.text_input(
                    "Password",
                    type="password",
                    key="admin_password_input"
                )

                if st.button("Login", key="login_button", use_container_width=True):
                    try:
                        if verify_admin(admin_email_input, admin_password):
                            st.session_state.is_admin = True
                            st.session_state.current_admin_email = admin_email_input
                            log_admin_action(admin_email_input, "login")
                            st.success("Logged in successfully")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                    except Exception as e:
                        st.error(f"Error during login: {str(e)}")

    st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)
    return selected_page.lower().replace(' ', '_')
