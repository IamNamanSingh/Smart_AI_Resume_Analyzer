import streamlit as st
from components.cards import page_header

def render_about_page():
    """Render the About Page with Creator credentials"""
    page_header(
        "About Smart Resume AI",
        "A professional AI platform built to help job seekers optimize resumes with smart guidance."
    )
    st.markdown(
        """
        <div class='panel-card' style='max-width: 800px; margin: 0 auto; padding: 2.5rem; border: 1px solid var(--surface-border); border-radius: 20px; background: var(--surface-soft);'>
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h3 style='color: var(--accent); font-size: 1.6rem; margin-top: 0; margin-bottom: 1rem;'>About the Platform</h3>
                <p style='color: var(--text-primary); font-size: 1.05rem; line-height: 1.7; max-width: 700px; margin: 0 auto;'>
                    Smart Resume AI combines advanced resume parsing, role-based job alignment, automated ATS scoring, and personalized AI recommendations into a unified, modern interface. The platform helps job seekers optimize their resumes to pass automated screening filters and stand out to recruiters.
                </p>
            </div>
            <hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin: 2rem 0;'>
            <div style='text-align: center;'>
                <h3 style='color: var(--accent); font-size: 1.4rem; margin-top: 0; margin-bottom: 0.5rem;'>Creator Information</h3>
                <h2 style='font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem; color: var(--text-primary);'>Naman Singh</h2>
                <p style='color: var(--text-secondary); font-size: 1rem; margin-bottom: 1.5rem; font-weight: 500;'>
                    AI & ML Developer | Full Stack Developer | Tech Enthusiast
                </p>
                <p style='color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; max-width: 600px; margin: 0 auto 2rem auto;'>
                    Passionate about building intelligent, human-centric software that empowers job seekers and enhances career development.
                </p>
                <div style='display: flex; justify-content: center; gap: 2rem; font-size: 2rem;'>
                    <a href="https://github.com/IamNamanSingh/" target="_blank" style="color: var(--text-primary); text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text-primary)'">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="https://www.linkedin.com/in/namansingh2405/" target="_blank" style="color: var(--text-primary); text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text-primary)'">
                        <i class="fab fa-linkedin"></i>
                    </a>
                    <a href="mailto:namansingh2475@gmail.com" target="_blank" style="color: var(--text-primary); text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text-primary)'">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
