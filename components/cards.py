import streamlit as st
import os
from core.config import CSS_PATH

def load_css():
    """Inject global style.css file content into the Streamlit app"""
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # Fallback if CSS file is missing
        st.warning("Assets CSS stylesheet not found.")

def page_header(title, subtitle=None):
    """Render a consistent page header with CSS variables compatible styling"""
    st.markdown(
        f'''
        <div class="page-header">
            <h1 class="header-title">{title}</h1>
            {f'<p class="header-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
        ''',
        unsafe_allow_html=True
    )

def hero_section(title, subtitle=None, description=None):
    """Render a modern hero section with gradient background"""
    if description and not subtitle:
        subtitle = description
        description = None
    
    st.markdown(
        f'''
        <div class="page-header hero-header">
            <h1 class="header-title">{title}</h1>
            {f'<div class="header-subtitle">{subtitle}</div>' if subtitle else ''}
            {f'<p class="header-caption">{description}</p>' if description else ''}
        </div>
        ''',
        unsafe_allow_html=True
    )

def glass_card_start(class_name="glass-card"):
    """Starts a div container for styled cards. MUST close with glass_card_end()"""
    st.markdown(f'<div class="{class_name}">', unsafe_allow_html=True)

def glass_card_end():
    """Ends the div container"""
    st.markdown('</div>', unsafe_allow_html=True)
