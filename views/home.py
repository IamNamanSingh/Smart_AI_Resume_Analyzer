import streamlit as st
import pandas as pd
from datetime import datetime
from core.database import get_resume_stats
from core.session import set_page
from components.cards import hero_section
from components.metrics import render_metric_card

def render_home_page():
    """Render the landing home page with quick CTAs and statistics overview"""
    # Premium Hero Header
    hero_section(
        "Smart Resume",
        "Transform your career with AI-powered resume analysis and building.",
        "Analyze ATS compatibility, discover critical skill gaps, and design recruiter-ready resumes."
    )

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Quick actions
    col_btn1, col_btn2 = st.columns(2, gap="medium")
    with col_btn1:
        st.markdown("""
            <div class="panel-card" style="text-align: center; border: 1px solid var(--surface-border); border-radius: 16px; padding: 2rem; background: var(--surface-soft); min-height: 250px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 3rem; margin-bottom: 1rem; color: var(--accent);"><i class="fas fa-search"></i></div>
                    <h3 style="margin-top:0; color: var(--accent); font-size: 1.3rem;">ATS Resume Analyzer</h3>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">
                        Upload your resume, find critical skill gaps, and get instant recommendations to pass ATS filters.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Analyzing Resume", key="home_goto_analyzer", use_container_width=True, type="primary"):
            set_page('resume_analyzer')

    with col_btn2:
        st.markdown("""
            <div class="panel-card" style="text-align: center; border: 1px solid var(--surface-border); border-radius: 16px; padding: 2rem; background: var(--surface-soft); min-height: 250px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 3rem; margin-bottom: 1rem; color: var(--accent);"><i class="fas fa-edit"></i></div>
                    <h3 style="margin-top:0; color: var(--accent); font-size: 1.3rem;">Structured Builder</h3>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">
                        Build an ATS-compliant resume step-by-step with real-time validation and professional templates.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Building Resume", key="home_goto_builder", use_container_width=True):
            set_page('resume_builder')

    st.markdown("<br><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)

    # Recent Resume Stats (Admin Only)
    if st.session_state.get('is_admin', False):
        st.markdown("<h3 style='color: var(--text-primary); margin-bottom: 1.5rem;'>Recent Platform Stats</h3>", unsafe_allow_html=True)
        stats = get_resume_stats()
        if stats and stats['total_resumes'] > 0:
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                render_metric_card("Total Resumes Processed", f"{stats['total_resumes']}", "All time submissions", "fas fa-file-alt")
            with col_stat2:
                render_metric_card("Average ATS Score", f"{stats['avg_ats_score']:.1f}%", "Overall resume match quality", "fas fa-chart-line")

            if stats.get('recent_activity'):
                st.markdown("<br><h4 style='color: var(--text-secondary); margin-bottom: 1rem;'>Recent Submissions</h4>", unsafe_allow_html=True)
                activity_data = []
                for name_val, role_val, date_val in stats['recent_activity']:
                    try:
                        dt = datetime.strptime(date_val, "%Y-%m-%d %H:%M:%S")
                        formatted_date = dt.strftime("%B %d, %Y")
                    except:
                        formatted_date = date_val
                    activity_data.append([name_val, role_val, formatted_date])
                
                df_activity = pd.DataFrame(activity_data, columns=["Candidate Name", "Target Role", "Submission Date"])
                st.dataframe(df_activity, use_container_width=True, hide_index=True)
        else:
            st.markdown("""
                <div style="background: var(--surface-soft); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); text-align: center;">
                    <p style="color: var(--text-secondary); margin: 0; font-size: 0.95rem;">
                        No resume statistics are available yet. Complete your first resume analysis or build a resume to view metrics!
                    </p>
                </div>
            """, unsafe_allow_html=True)
