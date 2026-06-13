import streamlit as st
from core.session import init_session, set_page, get_page, is_admin, set_admin

def test_session_state_initialization():
    """Verify that session state values are initialized to sensible defaults"""
    # Ensure variables are cleared before test
    for key in list(st.session_state.keys()):
        del st.session_state[key]
        
    init_session()
    
    assert get_page() == 'home'
    assert is_admin() is False
    assert st.session_state.user_id == 'default_user'
    assert isinstance(st.session_state.form_data, dict)

def test_page_switching():
    """Verify that page routing updates st.session_state correctly"""
    init_session()
    
    # Switch to resume analyzer tab
    try:
        set_page('resume_analyzer')
    except:
        # st.rerun() raises a specific Exception in Streamlit, which we catch
        pass
        
    assert st.session_state.page == 'resume_analyzer'

def test_admin_session_state():
    """Test updating and querying administrator state checks"""
    init_session()
    
    assert is_admin() is False
    
    set_admin(True)
    assert is_admin() is True
    
    set_admin(False)
    assert is_admin() is False
