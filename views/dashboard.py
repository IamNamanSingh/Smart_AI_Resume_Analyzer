import streamlit as st
import pandas as pd
from core.session import is_admin
from core.database import get_all_resume_data, get_admin_logs
from services.dashboard_service import DashboardService
from services.resume_service import export_resumes_to_excel
from components.cards import page_header
from components.metrics import render_metrics_grid
from components.charts import (
    render_success_rate,
    render_resume_upload_trends,
    render_ats_score_distribution,
    render_most_targeted_roles
)

def render_dashboard_page():
    """Render the enterprise administrator dashboard containing metrics, charts, insights, and logs"""
    page_header("Admin Analytics Dashboard", "Comprehensive system metrics, analytics, and AI feedback data.")

    # Guard: Require Administrator Authentication
    if not st.session_state.get('is_admin', False):
        st.warning("Access Denied. Please log in as an administrator to view this page.")
        
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            with st.container(border=True):
                st.markdown("""
                    <div style='text-align: center; margin-bottom: 20px;'>
                        <h3 style='margin: 0 0 5px 0; font-weight: 600; color: var(--accent);'>Administrator Login</h3>
                        <p style='margin: 0; font-size: 0.9rem; color: var(--text-secondary);'>Provide system admin credentials to continue.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                email = st.text_input("Administrator Email", key="dash_admin_email", placeholder="admin@example.com")
                password = st.text_input("Password", type="password", key="dash_admin_password", placeholder="••••••••")
                
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                if st.button("Login to Dashboard", type="primary", use_container_width=True, key="dash_login_button"):
                    from core.database import verify_admin, log_admin_action
                    if verify_admin(email, password):
                        st.session_state.is_admin = True
                        st.session_state.current_admin_email = email
                        log_admin_action(email, "login")
                        st.success("Access Granted! Loading dashboard...")
                        st.rerun()
                    else:
                        st.error("Invalid administrator credentials.")
        return

    # Admin is authenticated, render full dashboard
    db_service = DashboardService()
    metrics = db_service.get_dashboard_metrics()

    # Toolbar row
    col_title, col_export = st.columns([6, 2])
    with col_export:
        excel_data = export_resumes_to_excel()
        if excel_data:
            st.download_button(
                label="Export Database (Excel)",
                data=excel_data,
                file_name=f"resume_platform_data_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="dashboard_export_btn"
            )

    # 1. KPI Cards Grid
    kpis = [
        {"label": "Total Analyses", "value": str(metrics["total_analyses"]), "icon": "fas fa-microscope", "delta": "All-time uploads"},
        {"label": "Avg ATS Score", "value": f"{metrics['avg_score']}%", "icon": "fas fa-check-double", "delta": "Target >= 75%"},
        {"label": "Resumes Built", "value": str(metrics["resumes_built"]), "icon": "fas fa-file-alt", "delta": "From builder form"},
        {"label": "Job Searches", "value": str(metrics["job_searches"]), "icon": "fas fa-search", "delta": "Scraper & portals"},
        {"label": "Feedback Received", "value": str(metrics["feedback_count"]), "icon": "fas fa-comments", "delta": "User ratings"}
    ]
    render_metrics_grid(kpis)

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    # 2. Advanced Interactive Charts Grid (2 Columns)
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("<h4 style='margin-top:0; margin-bottom: 10px; font-weight:600; color:var(--text-primary);'>Match Rate & Upload Traffic</h4>", unsafe_allow_html=True)
            render_success_rate(metrics['avg_score'])
            
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("<h4 style='margin-top:0; margin-bottom: 15px; font-weight:600; color:var(--text-primary);'>Resume Submission Trends (Last 7 Days)</h4>", unsafe_allow_html=True)
            dates, counts = db_service.get_upload_trends()
            render_resume_upload_trends(dates, counts)

    with col2:
        with st.container(border=True):
            st.markdown("<h4 style='margin-top:0; margin-bottom: 15px; font-weight:600; color:var(--text-primary);'>ATS Score Range Distribution</h4>", unsafe_allow_html=True)
            scores = db_service.get_ats_distribution()
            render_ats_score_distribution(scores)
            
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("<h4 style='margin-top:0; margin-bottom: 15px; font-weight:600; color:var(--text-primary);'>Most Targeted Job Roles</h4>", unsafe_allow_html=True)
            roles, role_counts = db_service.get_targeted_roles()
            render_most_targeted_roles(roles, role_counts)

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    # 3. Dynamic AI Platform Insights
    st.markdown("<h3 style='color: var(--text-primary); margin-bottom: 15px;'>Dynamic AI Platform Insights</h3>", unsafe_allow_html=True)
    insights = db_service.get_ai_insights()
    if insights:
        cols_ins = st.columns(len(insights))
        for col_i, ins in zip(cols_ins, insights):
            with col_i:
                st.markdown(f"""
                    <div style="background: var(--surface-soft); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); min-height: 120px;">
                        <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: var(--accent);"><i class="{ins.get('icon', '')}"></i></div>
                        <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5;">{ins.get('text', '')}</p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # 4. Detailed Data and Activity Log tables
    st.markdown("<h3 style='color: var(--text-primary); margin-bottom: 15px;'>Platform User Submissions & Audit Logs</h3>", unsafe_allow_html=True)
    tab_data, tab_logs = st.tabs(["User Resume Records", "Security Auth Logs"])
    
    with tab_data:
        resumes = get_all_resume_data()
        if resumes:
            df_resumes = pd.DataFrame(
                resumes,
                columns=[
                    "ID", "Name", "Email", "Phone", "LinkedIn", "GitHub", "Portfolio",
                    "Target Role", "Category", "Date Created", "ATS Score", "Keyword Score",
                    "Format Score", "Section Score"
                ]
            )
            st.dataframe(df_resumes, use_container_width=True, hide_index=True)
        else:
            st.info("No resume entries found in database yet.")
            
    with tab_logs:
        logs = get_admin_logs()
        if logs:
            df_logs = pd.DataFrame(
                logs,
                columns=["Admin Email", "Action Performed", "Timestamp"]
            )
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
        else:
            st.info("No security admin logs found yet.")
