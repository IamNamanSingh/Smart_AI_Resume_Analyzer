import streamlit as st

def render_text_input(label, placeholder="", value="", type="default", key=None):
    """Render a text input with standard styles"""
    if type == "password":
        return st.text_input(label, placeholder=placeholder, value=value, type="password", key=key)
    else:
        return st.text_input(label, placeholder=placeholder, value=value, key=key)

def render_textarea(label, placeholder="", value="", height=150, key=None):
    """Render a text area with standard styles"""
    return st.text_area(label, placeholder=placeholder, value=value, height=height, key=key)

def render_selectbox(label, options, index=0, key=None):
    """Render a select box with standard styles"""
    return st.selectbox(label, options, index=index, key=key)

def render_file_uploader(label, type_list=['pdf', 'docx'], key=None):
    """Render a styled file uploader"""
    return st.file_uploader(label, type=type_list, key=key)
