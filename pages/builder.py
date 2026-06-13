import streamlit as st
import re
from services.resume_service import ResumeBuilder
from core.database import save_resume_data
from components.cards import page_header

def render_builder_page():
    """Render the resume builder step-by-step form wizard"""
    page_header(
        "Resume Builder",
        "Build professional resumes with a step-based workflow and guided content structure."
    )

    if 'builder_step' not in st.session_state:
        st.session_state.builder_step = 0

    steps = ["Profile", "Experience", "Projects & Education", "Skills", "Review"]
    current_step = st.session_state.builder_step

    st.markdown(
        f"<div class='panel-card'><h3>Step {current_step + 1} of {len(steps)}: {steps[current_step]}</h3></div>",
        unsafe_allow_html=True
    )

    progress = int((current_step + 1) / len(steps) * 100)
    st.progress(progress)

    # Initialize builder form data relative to global form data
    if 'builder_form' not in st.session_state:
        st.session_state.builder_form = st.session_state.form_data

    # Ensure personal_info is initialized
    if 'personal_info' not in st.session_state.builder_form:
        st.session_state.builder_form['personal_info'] = {}

    if current_step == 0:
        st.subheader("Personal details")
        
        if 'step0_errors' in st.session_state and st.session_state.step0_errors:
            for err in st.session_state.step0_errors:
                st.error(f"⚠️ {err}")

        st.session_state.builder_form['personal_info']['full_name'] = st.text_input(
            "Full Name",
            value=st.session_state.builder_form['personal_info'].get('full_name', '')
        )
        st.session_state.builder_form['personal_info']['email'] = st.text_input(
            "Email",
            value=st.session_state.builder_form['personal_info'].get('email', '')
        )
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.builder_form['personal_info']['phone'] = st.text_input(
                "Phone",
                value=st.session_state.builder_form['personal_info'].get('phone', '')
            )
        with col2:
            st.session_state.builder_form['personal_info']['location'] = st.text_input(
                "Location",
                value=st.session_state.builder_form['personal_info'].get('location', '')
            )
        col3, col4 = st.columns(2)
        with col3:
            st.session_state.builder_form['personal_info']['linkedin'] = st.text_input(
                "LinkedIn Profile URL",
                value=st.session_state.builder_form['personal_info'].get('linkedin', '')
            )
        with col4:
            st.session_state.builder_form['personal_info']['portfolio'] = st.text_input(
                "Portfolio or GitHub URL",
                value=st.session_state.builder_form['personal_info'].get('portfolio', '')
            )

        # Dynamic warnings
        email_val = st.session_state.builder_form['personal_info'].get('email', '')
        phone_val = st.session_state.builder_form['personal_info'].get('phone', '')
        name_val = st.session_state.builder_form['personal_info'].get('full_name', '')
        
        email_valid = bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_val)) if email_val else False
        phone_valid = bool(re.match(r"^\d{10}$", phone_val)) if phone_val else False
        name_valid = len(name_val.strip()) > 0
        
        if not name_valid:
            st.warning("⚠️ Full Name is required.")
        if email_val and not email_valid:
            st.warning("⚠️ Please enter a valid email address (e.g. user@domain.com).")
        if phone_val and not phone_valid:
            st.warning("⚠️ Phone number must be exactly 10 digits.")

        st.session_state.builder_form['summary'] = st.text_area(
            "Professional Summary",
            value=st.session_state.builder_form.get('summary', ''),
            height=140,
            help="Write a concise summary that highlights your strongest qualifications."
        )

    elif current_step == 1:
        st.subheader("Work Experience 💼")
        experiences = st.session_state.builder_form.get('experiences', [])
        if not isinstance(experiences, list):
            experiences = []
        
        if not experiences:
            experiences = [{
                'company': '',
                'position': '',
                'start_date': '',
                'end_date': '',
                'description': '',
                'responsibilities': ''
            }]
            st.session_state.builder_form['experiences'] = experiences
        
        updated_experiences = []
        for i, exp in enumerate(experiences):
            with st.expander(f"Job #{i+1}: {exp.get('position', 'New Position')} at {exp.get('company', 'New Company')}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    company = st.text_input(f"Company Name", value=exp.get('company', ''), key=f"exp_company_{i}")
                    position = st.text_input(f"Job Title / Position", value=exp.get('position', ''), key=f"exp_pos_{i}")
                with col2:
                    start_date = st.text_input(f"Start Date (e.g. June 2024)", value=exp.get('start_date', ''), key=f"exp_start_{i}")
                    end_date = st.text_input(f"End Date (e.g. Present)", value=exp.get('end_date', ''), key=f"exp_end_{i}")
                
                description = st.text_area(f"Job Description", value=exp.get('description', ''), key=f"exp_desc_{i}", height=100)
                responsibilities = st.text_area(f"Key Responsibilities (One per line)", value=exp.get('responsibilities', ''), key=f"exp_resp_{i}", height=100)
                
                updated_experiences.append({
                    'company': company,
                    'position': position,
                    'start_date': start_date,
                    'end_date': end_date,
                    'description': description,
                    'responsibilities': responsibilities
                })
        
        st.session_state.builder_form['experiences'] = updated_experiences
        
        col_add, col_rem = st.columns(2)
        if col_add.button("➕ Add Experience", use_container_width=True):
            st.session_state.builder_form['experiences'].append({
                'company': '',
                'position': '',
                'start_date': '',
                'end_date': '',
                'description': '',
                'responsibilities': ''
            })
            st.rerun()
        
        if len(st.session_state.builder_form['experiences']) > 1:
            if col_rem.button("🗑️ Remove Last Experience", use_container_width=True):
                st.session_state.builder_form['experiences'].pop()
                st.rerun()

    elif current_step == 2:
        st.subheader("Projects & Achievements 🛠️")
        projects = st.session_state.builder_form.get('projects', [])
        if not isinstance(projects, list):
            projects = []
        if not projects:
            projects = [{
                'name': '',
                'technologies': '',
                'description': '',
                'responsibilities': ''
            }]
            st.session_state.builder_form['projects'] = projects
        
        updated_projects = []
        for i, proj in enumerate(projects):
            with st.expander(f"Project #{i+1}: {proj.get('name', 'New Project')}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input(f"Project Name", value=proj.get('name', ''), key=f"proj_name_{i}")
                with col2:
                    technologies = st.text_input(f"Technologies Used (comma separated)", value=proj.get('technologies', ''), key=f"proj_tech_{i}")
                
                description = st.text_area(f"Description", value=proj.get('description', ''), key=f"proj_desc_{i}", height=80)
                responsibilities = st.text_area(f"Key Accomplishments (One per line)", value=proj.get('responsibilities', ''), key=f"proj_resp_{i}", height=80)
                
                updated_projects.append({
                    'name': name,
                    'technologies': technologies,
                    'description': description,
                    'responsibilities': responsibilities
                })
        
        st.session_state.builder_form['projects'] = updated_projects
        
        col_add_proj, col_rem_proj = st.columns(2)
        if col_add_proj.button("➕ Add Project", use_container_width=True):
            st.session_state.builder_form['projects'].append({
                'name': '',
                'technologies': '',
                'description': '',
                'responsibilities': ''
            })
            st.rerun()
        if len(st.session_state.builder_form['projects']) > 1:
            if col_rem_proj.button("🗑️ Remove Last Project", use_container_width=True):
                st.session_state.builder_form['projects'].pop()
                st.rerun()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("Education 🎓")
        education = st.session_state.builder_form.get('education', [])
        if not isinstance(education, list):
            education = []
        if not education:
            education = [{
                'school': '',
                'degree': '',
                'field': '',
                'graduation_date': '',
                'gpa': ''
            }]
            st.session_state.builder_form['education'] = education
        
        updated_education = []
        for i, edu in enumerate(education):
            with st.expander(f"Education #{i+1}: {edu.get('degree', 'Degree')} in {edu.get('field', 'Field')} at {edu.get('school', 'School')}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    school = st.text_input(f"School/University", value=edu.get('school', ''), key=f"edu_school_{i}")
                    degree = st.text_input(f"Degree", value=edu.get('degree', ''), key=f"edu_degree_{i}")
                with col2:
                    field = st.text_input(f"Field of Study", value=edu.get('field', ''), key=f"edu_field_{i}")
                    graduation_date = st.text_input(f"Graduation Date (e.g. May 2026)", value=edu.get('graduation_date', ''), key=f"edu_grad_{i}")
                gpa = st.text_input(f"GPA / Grade", value=edu.get('gpa', ''), key=f"edu_gpa_{i}")
                
                updated_education.append({
                    'school': school,
                    'degree': degree,
                    'field': field,
                    'graduation_date': graduation_date,
                    'gpa': gpa
                })
        
        st.session_state.builder_form['education'] = updated_education
        
        col_add_edu, col_rem_edu = st.columns(2)
        if col_add_edu.button("➕ Add Education", use_container_width=True):
            st.session_state.builder_form['education'].append({
                'school': '',
                'degree': '',
                'field': '',
                'graduation_date': '',
                'gpa': ''
            })
            st.rerun()
        if len(st.session_state.builder_form['education']) > 1:
            if col_rem_edu.button("🗑️ Remove Last Education", use_container_width=True):
                st.session_state.builder_form['education'].pop()
                st.rerun()

    elif current_step == 3:
        st.subheader("Skills 🤹")
        
        if 'skills_categories' not in st.session_state.builder_form:
            st.session_state.builder_form['skills_categories'] = {
                'technical': [],
                'soft': [],
                'languages': [],
                'tools': []
            }
        
        tech_skills_str = ", ".join(st.session_state.builder_form['skills_categories'].get('technical', []))
        soft_skills_str = ", ".join(st.session_state.builder_form['skills_categories'].get('soft', []))
        languages_str = ", ".join(st.session_state.builder_form['skills_categories'].get('languages', []))
        tools_str = ", ".join(st.session_state.builder_form['skills_categories'].get('tools', []))
        
        tech_input = st.text_area(
            "Technical Skills (comma-separated)",
            value=tech_skills_str,
            help="E.g., Python, Machine Learning, SQL, Git"
        )
        soft_input = st.text_area(
            "Soft Skills (comma-separated)",
            value=soft_skills_str,
            help="E.g., Leadership, Communication, Problem Solving"
        )
        lang_input = st.text_area(
            "Languages (comma-separated)",
            value=languages_str,
            help="E.g., English, Spanish, French"
        )
        tools_input = st.text_area(
            "Tools & Technologies (comma-separated)",
            value=tools_str,
            help="E.g., Docker, AWS, Tableau, VS Code"
        )
        
        st.session_state.builder_form['skills_categories']['technical'] = [s.strip() for s in tech_input.split(",") if s.strip()]
        st.session_state.builder_form['skills_categories']['soft'] = [s.strip() for s in soft_input.split(",") if s.strip()]
        st.session_state.builder_form['skills_categories']['languages'] = [s.strip() for s in lang_input.split(",") if s.strip()]
        st.session_state.builder_form['skills_categories']['tools'] = [s.strip() for s in tools_input.split(",") if s.strip()]

    else:
        st.subheader("Review & Generate 📄")
        st.write("Please review your resume details before generation:")
        
        personal = st.session_state.builder_form.get('personal_info', {})
        
        col_rev1, col_rev2 = st.columns(2)
        with col_rev1:
            st.markdown(f"**Name:** {personal.get('full_name', '')}")
            st.markdown(f"**Email:** {personal.get('email', '')}")
            st.markdown(f"**Phone:** {personal.get('phone', '')}")
        with col_rev2:
            st.markdown(f"**Location:** {personal.get('location', '')}")
            st.markdown(f"**LinkedIn:** {personal.get('linkedin', '')}")
            st.markdown(f"**Portfolio/GitHub:** {personal.get('portfolio', '')}")
        
        st.markdown(f"**Professional Summary:** {st.session_state.builder_form.get('summary', '')}")
        st.markdown("---")
        
        template_options = ["Modern", "Professional", "Minimal", "Creative"]
        selected_template = st.selectbox(
            "Select Resume Template",
            template_options,
            key="builder_template_select"
        )
        st.success(f"🎨 Selected Template: {selected_template}")
        
        errors = []
        if not personal.get('full_name', '').strip():
            errors.append("Full Name is missing.")
        if not personal.get('email', '').strip():
            errors.append("Email is missing.")
        if not personal.get('phone', '').strip():
            errors.append("Phone number is missing.")
            
        if errors:
            for err in errors:
                st.error(f"⚠️ {err}")
            st.warning("Please go back to Step 1 and fill in the required fields before generating.")
        else:
            if st.button("Generate Resume 📄", use_container_width=True):
                resume_data = {
                    'personal_info': personal,
                    'summary': st.session_state.builder_form.get('summary', ''),
                    'experience': st.session_state.builder_form.get('experiences', []),
                    'education': st.session_state.builder_form.get('education', []),
                    'projects': st.session_state.builder_form.get('projects', []),
                    'skills': st.session_state.builder_form.get('skills_categories', {}),
                    'template': selected_template
                }
                try:
                    with st.spinner("Generating document..."):
                        builder = ResumeBuilder()
                        resume_buffer = builder.generate_resume(resume_data)
                        
                    if resume_buffer:
                        save_resume_data(resume_data)
                        st.success("🎉 Resume generated successfully!")
                        st.download_button(
                            "Download Resume (.docx)",
                            data=resume_buffer,
                            file_name=f"{personal.get('full_name','resume').replace(' ','_')}_resume.docx",
                            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            use_container_width=True
                        )
                    else:
                        st.error("Resume generation failed.")
                except Exception as ex:
                    st.error(f"Unable to generate resume: {str(ex)}")

    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns([1, 1], gap='medium')
    if cols[0].button("Previous", disabled=current_step == 0, use_container_width=True):
        st.session_state.builder_step = max(0, current_step - 1)
        st.rerun()
    if cols[1].button("Next", disabled=current_step == len(steps) - 1, use_container_width=True):
        if current_step == 0:
            name = st.session_state.builder_form['personal_info'].get('full_name', '').strip()
            email = st.session_state.builder_form['personal_info'].get('email', '').strip()
            phone = st.session_state.builder_form['personal_info'].get('phone', '').strip()
            
            email_pat = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            phone_pat = r"^\d{10}$"
            
            errors = []
            if not name:
                errors.append("Full Name is required.")
            if not email or not re.match(email_pat, email):
                errors.append("A valid Email is required.")
            if not phone or not re.match(phone_pat, phone):
                errors.append("A valid 10-digit Phone number is required.")
            
            if errors:
                st.session_state.step0_errors = errors
            else:
                if 'step0_errors' in st.session_state:
                    del st.session_state.step0_errors
                st.session_state.builder_step = min(len(steps) - 1, current_step + 1)
                st.rerun()
        else:
            st.session_state.builder_step = min(len(steps) - 1, current_step + 1)
            st.rerun()
