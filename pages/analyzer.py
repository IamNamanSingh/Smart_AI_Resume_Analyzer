import streamlit as st
from core.constants import JOB_ROLES
from services.resume_service import ResumeAnalyzer, extract_text_from_pdf, extract_text_from_docx
from components.cards import page_header
from components.metrics import render_metric_card

def render_analyzer_page():
    """Render the Resume Analyzer page"""
    page_header(
        "Resume Analyzer",
        "Upload your resume and get a polished scorecard, gap analysis, and personalized improvement recommendations."
    )

    categories = list(JOB_ROLES.keys())
    selected_category = st.selectbox("Job Category", categories, key="analyzer_category")
    roles = list(JOB_ROLES[selected_category].keys())
    selected_role = st.selectbox("Specific Role", roles, key="analyzer_role")
    role_info = JOB_ROLES[selected_category][selected_role]

    st.markdown(
        f"""
        <div class='panel-card'>
            <div style='display: flex; justify-content: space-between; align-items: center; gap: 1rem; flex-wrap: wrap;'>
                <div>
                    <h3 style='margin: 0;'>{selected_role}</h3>
                    <p style='margin: 5px 0 0 0; color: var(--text-secondary);'>{role_info['description']}</p>
                </div>
                <div style='text-align: right;'>
                    <span class='skill-pill'>Role skills: {', '.join(role_info['required_skills'][:4])}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=['pdf', 'docx'],
        key='analyzer_upload',
        label_visibility='collapsed'
    )

    st.markdown(
        """
        <div class='upload-card'>
            <div class='upload-icon'>
                <i class='fas fa-cloud-upload-alt'></i>
            </div>
            <h4>Drag & drop your resume</h4>
            <p>PDF or DOCX. The analyzer will inspect formatting, skills, and ATS compatibility.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if uploaded_file is not None and st.button("Analyze Resume", key='analyze_resume_button', use_container_width=True):
        try:
            # Create a spinner and status indicators
            with st.spinner("Extracting text and analyzing resume..."):
                if uploaded_file.type == 'application/pdf':
                    text = extract_text_from_pdf(uploaded_file)
                else:
                    text = extract_text_from_docx(uploaded_file)

                analyzer = ResumeAnalyzer()
                result = analyzer.analyze_resume({'raw_text': text}, role_info)

            if result.get('document_type') != 'resume':
                st.error("Uploaded file does not appear to be a resume. Please upload a proper resume.")
                return

            avg_score = result.get('ats_score', 0)
            match_score = int(result.get('keyword_match', {}).get('score', 0))
            format_score = int(result.get('format_score', 0))
            resume_quality = int((avg_score * 0.55) + (match_score * 0.25) + (format_score * 0.2))

            missing_skills = result.get('keyword_match', {}).get('missing_skills', [])
            missing_count = len(missing_skills)

            card_items = [
                ("ATS Score", f"{avg_score}/100", "How well the resume passes ATS checks", "⚡"),
                ("JD Match", f"{match_score}%", "Role-specific keyword alignment", "📌"),
                ("Missing Skills", f"{missing_count}", "Skills not present in this resume", "🧩"),
                ("Resume Quality", f"{resume_quality}/100", "Readability and structure score", "✨")
            ]

            st.markdown("<div class='dashboard-grid'>", unsafe_allow_html=True)
            cols = st.columns(len(card_items), gap='medium')
            for col, (label, value, detail, icon) in zip(cols, card_items):
                with col:
                    render_metric_card(label, value, delta=detail, icon=icon)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
                <div class='dashboard-panel'>
                    <h3>Resume Summary</h3>
                    <p style="color: var(--text-secondary);">Our system has identified the key strengths and gaps in your resume based on the selected role.</p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class='panel-card'>
                        <h3>Missing Skills</h3>
                        <p style="color: var(--text-secondary); font-size: 0.9em;">The analyzer found the following role skills missing from your resume.</p>
                    """, unsafe_allow_html=True)
                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(f"<span class='skill-pill' style='display: inline-block; margin: 4px;'>{skill}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: var(--text-secondary);'>No missing skills detected.</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("""
                    <div class='panel-card'>
                        <h3>Improvement Recommendations</h3>
                        <p style="color: var(--text-secondary); font-size: 0.9em;">Focus on these high-impact updates to improve your resume score.</p>
                    """, unsafe_allow_html=True)
                for suggestion in result.get('suggestions', [])[:6]:
                    st.markdown(f"<p style='margin: 0.65rem 0; color: var(--text-secondary);'>• {suggestion}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
                <div class='panel-card'>
                    <h3>Resume Insights</h3>
                    <p style="color: var(--text-secondary);">Keep your resume focused on quantifiable results, keywords, and readable structure.</p>
                    <ul style='color: var(--text-secondary); margin-top: 1rem;'>
                        <li>Use keyword-rich bullet points.</li>
                        <li>Keep contact details clear and prominent.</li>
                        <li>Quantify achievements where possible.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Resume analysis failed: {str(e)}")
