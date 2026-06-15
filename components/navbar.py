import streamlit as st

def render_navbar(page_keys, current_page):
    """Render the single horizontal navigation bar containing brand logo and menu items"""
    # Prepend the brand/logo to the list of page keys
    nav_keys = ["Smart Resume"] + page_keys
    
    # Map page key to navigation label
    page_label_map = {name.lower().replace(' ', '_'): name for name in nav_keys}
    
    # Identify which index is currently active.
    # Note that both 'Smart Resume' and 'Home' map to 'home' page.
    # If current_page is 'home', we prefer selecting 'Home' in navigation for visual clarity,
    # or if current_page matches, select it.
    default_label = page_label_map.get(current_page, nav_keys[0])
    selected_index = nav_keys.index(default_label) if default_label in nav_keys else 0
    
    # Inject start anchor for linter/CSS scoping
    st.markdown('<div class="topbar-start"></div>', unsafe_allow_html=True)
    
    selected_page = st.radio(
        '',
        options=nav_keys,
        index=selected_index,
        horizontal=True,
        key='page_navigation'
    )
    
    # Normalize return page key
    normalized_page = selected_page.lower().replace(' ', '_')
    if normalized_page == "smart_resume":
        return 'home'
    return normalized_page
