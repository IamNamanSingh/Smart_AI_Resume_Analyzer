import streamlit as st
import pandas as pd

# Set page config at the very beginning
st.set_page_config(
    page_title="Smart Resume AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
from core.session import init_session
init_session()

# Run migrations once on application startup
if 'migrations_run' not in st.session_state:
    try:
        from database.migrations import run_migrations
        run_migrations()
        st.session_state.migrations_run = True
    except Exception as e:
        st.error(f"Error running database migrations: {e}")

# Inject modern CSS stylesheet and load fonts
from components.cards import load_css
load_css()

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
""", unsafe_allow_html=True)

# Render Desktop Navbar & Admin authentication popup controls
from components.navbar import render_navbar
page_keys = ["Home", "Resume Analyzer", "Resume Builder", "Dashboard", "Job Search", "Feedback", "About"]
selected_page = render_navbar(page_keys, st.session_state.page)

# If navigation changed, update and rerun
if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

# Page Routing
current_page = st.session_state.page

if current_page == 'home':
    from pages.home import render_home_page
    render_home_page()
elif current_page == 'resume_analyzer':
    from pages.analyzer import render_analyzer_page
    render_analyzer_page()
elif current_page == 'resume_builder':
    from pages.builder import render_builder_page
    render_builder_page()
elif current_page == 'dashboard':
    from pages.dashboard import render_dashboard_page
    render_dashboard_page()
elif current_page == 'job_search':
    from pages.jobs import render_jobs_page
    render_jobs_page()
elif current_page == 'feedback':
    from pages.feedback import render_feedback_page
    render_feedback_page()
elif current_page == 'about':
    from pages.about import render_about_page
    render_about_page()

# Global Footer
from components.footer import render_footer
render_footer()