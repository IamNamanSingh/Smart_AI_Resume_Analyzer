import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

# Standard colors compatible with SaaS theme
THEME_COLORS = {
    'primary': '#10A37F',      # Accent green
    'secondary': '#22C55E',    # Light green
    'warning': '#F97316',      # Orange
    'danger': '#EF4444',       # Red
    'grid': 'rgba(255, 255, 255, 0.08)',
    'text': '#F8FAFC',
    'text_muted': 'rgba(255, 255, 255, 0.6)'
}

def apply_chart_theme(fig):
    """Apply the default dark SaaS theme to a Plotly figure"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME_COLORS['text'], family="Inter, system-ui, sans-serif"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            gridcolor=THEME_COLORS['grid'],
            zerolinecolor=THEME_COLORS['grid'],
            tickfont=dict(color=THEME_COLORS['text_muted'])
        ),
        yaxis=dict(
            gridcolor=THEME_COLORS['grid'],
            zerolinecolor=THEME_COLORS['grid'],
            tickfont=dict(color=THEME_COLORS['text_muted'])
        )
    )
    return fig

def render_ats_score_distribution(scores):
    """Render a distribution bar chart or histogram of ATS scores"""
    if not scores:
        scores = [65, 70, 75, 80, 82, 85, 90]
        
    df = pd.DataFrame({'ATS Score': scores})
    fig = px.histogram(
        df, 
        x='ATS Score', 
        nbins=10, 
        title='ATS Score Distribution',
        color_discrete_sequence=[THEME_COLORS['primary']]
    )
    fig.update_layout(
        bargap=0.1,
        yaxis_title="Count",
        xaxis_title="Score Range"
    )
    apply_chart_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_resume_upload_trends(dates, counts):
    """Render a timeline trend chart of resume uploads"""
    if not dates:
        dates = ['2026-06-06', '2026-06-07', '2026-06-08', '2026-06-09', '2026-06-10', '2026-06-11', '2026-06-12']
        counts = [12, 18, 15, 25, 30, 28, 35]
        
    df = pd.DataFrame({'Date': dates, 'Uploads': counts})
    fig = px.line(
        df, 
        x='Date', 
        y='Uploads', 
        title='Resume Upload Trends',
        markers=True,
        color_discrete_sequence=[THEME_COLORS['primary']]
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    apply_chart_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_most_targeted_roles(roles_list, counts_list):
    """Render a horizontal bar chart of targeted job roles"""
    if not roles_list:
        roles_list = ['Frontend Developer', 'Backend Developer', 'Data Scientist', 'DevOps Engineer', 'UI Designer']
        counts_list = [45, 38, 29, 22, 15]
        
    df = pd.DataFrame({'Role': roles_list, 'Count': counts_list}).sort_values(by='Count')
    fig = px.bar(
        df, 
        y='Role', 
        x='Count', 
        orientation='h',
        title='Most Targeted Job Roles',
        color_discrete_sequence=[THEME_COLORS['primary']]
    )
    apply_chart_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_top_skills(skills_list, counts_list):
    """Render a bar chart of top extracted skills"""
    if not skills_list:
        skills_list = ['Python', 'React', 'SQL', 'Docker', 'AWS', 'JavaScript', 'Git']
        counts_list = [55, 42, 38, 30, 28, 25, 20]
        
    df = pd.DataFrame({'Skill': skills_list, 'Usage': counts_list}).sort_values(by='Usage', ascending=False)
    fig = px.bar(
        df, 
        x='Skill', 
        y='Usage', 
        title='Top Core Skills Identified',
        color='Usage',
        color_continuous_scale=[[0, '#0f3c2b'], [1, THEME_COLORS['primary']]]
    )
    fig.update_layout(coloraxis_showscale=False)
    apply_chart_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_success_rate(success_score):
    """Render a Gauge chart for resume success rating"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = success_score if success_score else 72.5,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Average Platform Match Rate"},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': THEME_COLORS['text']},
            'bar': {'color': THEME_COLORS['primary']},
            'bgcolor': 'rgba(255,255,255,0.05)',
            'borderwidth': 1,
            'bordercolor': THEME_COLORS['grid'],
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.1)'},
                {'range': [50, 75], 'color': 'rgba(249, 115, 22, 0.1)'},
                {'range': [75, 100], 'color': 'rgba(16, 163, 127, 0.1)'}
            ]
        }
    ))
    fig.update_layout(height=260)
    apply_chart_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
