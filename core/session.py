import streamlit as st
from datetime import datetime

def init_session():
    """Initialize all session state variables with sensible defaults"""
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
        
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
        
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 'default_user'
        
    if 'selected_role' not in st.session_state:
        st.session_state.selected_role = None
        
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = []
        
    if 'ai_analysis_stats' not in st.session_state:
        st.session_state.ai_analysis_stats = {
            'total_analyses': 0,
            'avg_score': 0.0
        }
        
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'personal_info': {},
            'summary': '',
            'experience': [],
            'education': [],
            'projects': [],
            'skills': [],
            'template': 'Modern'
        }
        
    if 'builder_step' not in st.session_state:
        st.session_state.builder_step = 0

def set_page(page_name):
    """Set active page and rerun Streamlit"""
    st.session_state.page = page_name
    st.rerun()

def get_page():
    """Get currently active page"""
    return st.session_state.get('page', 'home')

def is_admin():
    """Check if active user is admin"""
    return st.session_state.get('is_admin', False)

def set_admin(status=True):
    """Set admin login status"""
    st.session_state.is_admin = status
