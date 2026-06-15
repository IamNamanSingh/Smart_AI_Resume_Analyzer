import streamlit as st
from services.job_service import JobService
from services.linkedin_scraper import render_linkedin_scraper
from services.suggestions import JOB_SUGGESTIONS, LOCATION_SUGGESTIONS
from components.cards import page_header

def render_jobs_page():
    """Render the Job Search and LinkedIn Scraper page"""
    page_header(
        "Job Search",
        "Find relevant opportunities with improved filters and modern result cards."
    )

    job_service = JobService()

    # Search Card Container
    with st.container():
        # Portal selector
        tabs = st.radio(
            "Select Search Method",
            ["Global Job Portals Search", "LinkedIn Job Scraper"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if tabs == "Global Job Portals Search":
            st.markdown(
                """
                <div class="panel-card" style="padding: 1.5rem; border: 1px solid var(--surface-border); border-radius: 16px; margin-bottom: 2rem; background: var(--surface-soft);">
                    <h3 style="margin-top:0; color: var(--accent);"><i class="fas fa-search" style="margin-right: 0.5rem;"></i> Multi-Portal Search</h3>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem;">Enter job details to instantly build direct search links for Naukri, LinkedIn, Foundit, and Indeed.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Simple, clean input columns
            col1, col2 = st.columns([1, 1], gap="medium")
            with col1:
                job_query = st.text_input(
                    "Job Title / Core Skills",
                    placeholder="e.g. Software Engineer, React Developer",
                    key="portal_job_query"
                )
            with col2:
                location = st.text_input(
                    "Location / Work Mode",
                    placeholder="e.g. Bangalore, Remote",
                    key="portal_job_location"
                )
                
            # Advanced filters expander
            with st.expander("Filter Options"):
                f_cols = st.columns(3)
                filter_opts = job_service.get_filter_options()
                
                with f_cols[0]:
                    experience = st.selectbox(
                        "Experience Level",
                        options=filter_opts["experience_levels"],
                        format_func=lambda x: x["text"]
                    )
                with f_cols[1]:
                    salary_range = st.selectbox(
                        "Salary Range",
                        options=filter_opts["salary_ranges"],
                        format_func=lambda x: x["text"]
                    )
                with f_cols[2]:
                    job_type = st.selectbox(
                        "Job Type",
                        options=filter_opts["job_types"],
                        format_func=lambda x: x["text"]
                    )
            
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Search Jobs", use_container_width=True, type="primary"):
                if not job_query.strip():
                    st.warning("Please enter a job title or core skills to search.")
                else:
                    with st.spinner("Generating direct job search links..."):
                        search_results = job_service.build_search_links(
                            job_query, 
                            location, 
                            experience
                        )
                    
                    if search_results:
                        st.markdown("<h3 style='margin: 1.5rem 0 1rem 0;'>Direct Search Links</h3>", unsafe_allow_html=True)
                        st.markdown("<div class='grid'>", unsafe_allow_html=True)
                        
                        cols = st.columns(3)
                        for idx, result in enumerate(search_results):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                st.markdown(
                                    f"""
                                    <div class="panel-card" style="border: 1px solid var(--surface-border); padding: 1.25rem; border-radius: 12px; height: 180px; display: flex; flex-direction: column; justify-content: space-between; background: var(--surface-soft); margin-bottom: 15px;">
                                        <div>
                                            <h4 style="margin: 0; color: var(--text-primary);"><i class="{result['icon']}" style="margin-right: 0.5rem; color: {result['color']};"></i>{result['portal']}</h4>
                                            <p style="font-size: 0.8rem; color: var(--text-secondary); margin: 8px 0 0 0;">Search direct listings on {result['portal']}</p>
                                        </div>
                                        <a href="{result['url']}" target="_blank" class="stButton" style="text-decoration: none; width: 100%;">
                                            <button style="width: 100%; padding: 0.5rem; font-size: 0.85rem; border-radius: 8px; cursor: pointer; background: var(--accent); color: white; border: none;">Go to Portal <i class="fas fa-external-link-alt"></i></button>
                                        </a>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("No portal search links could be built. Please try different terms.")
        else:
            # Render the Selenium Scraper directly
            render_linkedin_scraper()
