import streamlit as st
from components.cards import page_header

def render_about_page():
    """Render the About Page with Creator credentials"""
    page_header(
        "About Smart Resume",
        "A professional AI platform built to help job seekers optimize resumes with smart guidance."
    )
    st.markdown(
        """
        <div class='panel-card' style='max-width: 800px; margin: 0 auto; padding: 2.5rem; border: 1px solid var(--surface-border); border-radius: 20px; background: var(--surface-soft);'>
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h3 style='color: var(--accent); font-size: 1.6rem; margin-top: 0; margin-bottom: 1rem;'>About the Platform</h3>
                <p style='color: var(--text-primary); font-size: 1.05rem; line-height: 1.7; max-width: 700px; margin: 0 auto;'>
                    Smart Resume combines advanced resume parsing, role-based job alignment, automated ATS scoring, and personalized AI recommendations into a unified, modern interface. The platform helps job seekers optimize their resumes to pass automated screening filters and stand out to recruiters.
                </p>
            </div>
            <hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin: 2rem 0;'>
            <div style='text-align: center;'>
                <h3 style='color: var(--accent); font-size: 1.4rem; margin-top: 0; margin-bottom: 0.5rem;'>Creator Information</h3>
                <h2 style='font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem; color: var(--text-primary);'>Naman Singh</h2>
                <p style='color: var(--text-secondary); font-size: 1rem; margin-bottom: 1.5rem; font-weight: 500;'>
                    AI & ML Developer | Full Stack Developer | Tech Enthusiast
                </p>
                <p style='color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; max-width: 600px; margin: 0 auto 2rem auto;'>
                    Passionate about building intelligent, human-centric software that empowers job seekers and enhances career development.
                </p>
                <div style='display: flex; justify-content: center; gap: 2rem; font-size: 2rem;'>
                    <a href="https://github.com/IamNamanSingh/" target="_blank" style="color: var(--text-primary); text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text-primary)'">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="https://www.linkedin.com/in/namansingh2405/" target="_blank" style="color: var(--text-primary); text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text-primary)'">
                        <i class="fab fa-linkedin"></i>
                    </a>
                    <a href="mailto:namansingh2475@gmail.com" target="_blank" style="color: var(--text-primary); text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text-primary)'">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.5, 2.0, 1.5])
    with col2:
        with st.container(border=True):
            st.markdown("<div class='admin-access-trigger'></div>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; margin-top: 0; margin-bottom: 1.5rem; font-weight: 600;'>Administrator Access</h3>", unsafe_allow_html=True)
            
            if not st.session_state.get('is_admin', False):
                from core.database import verify_admin, log_admin_action
                admin_email_input = st.text_input("Email", key="about_admin_email_input", placeholder="admin@example.com")
                admin_password = st.text_input("Password", type="password", key="about_admin_password_input", placeholder="••••••••")
                
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                if st.button("Login", key="about_login_button", use_container_width=True, type="primary"):
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
            else:
                from core.database import log_admin_action
                st.markdown(f"""
                    <div style='text-align: center; margin-bottom: 1.5rem;'>
                        <p style='color: var(--text-secondary); margin-bottom: 0.5rem;'>Logged in as:</p>
                        <p style='font-weight: 600; color: var(--accent); font-size: 1.1rem;'>{st.session_state.get('current_admin_email')}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("Open Dashboard", key="about_open_dashboard_button", use_container_width=True, type="primary"):
                    st.session_state.page = 'dashboard'
                    st.rerun()
                    
                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                
                if st.button("Logout", key="about_logout_button", use_container_width=True):
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
