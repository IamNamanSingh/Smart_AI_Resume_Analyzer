import sqlite3
import os
from core.database import (
    get_database_connection,
    save_resume_data,
    save_analysis_data,
    get_resume_stats,
    log_admin_action,
    get_admin_logs,
    verify_admin
)

def test_database_tables_exist():
    """Verify that all required tables are successfully created upon initialization"""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    assert "resume_data" in tables
    assert "resume_skills" in tables
    assert "resume_analysis" in tables
    assert "admin_logs" in tables
    assert "admin" in tables
    assert "ai_analysis" in tables
    assert "feedback" in tables

def test_save_and_retrieve_resume_data():
    """Test saving resume details to the database and checking that statistics are updated"""
    resume_payload = {
        'personal_info': {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'linkedin': 'linkedin.com/in/test',
            'github': 'github.com/test',
            'portfolio': 'test.com'
        },
        'summary': 'A qualified software engineering professional.',
        'target_role': 'Software Engineer',
        'target_category': 'Development',
        'education': [{'school': 'Test University', 'degree': 'B.S.', 'field': 'CS', 'graduation_date': '2026', 'gpa': '4.0'}],
        'experience': [{'company': 'Test Corp', 'position': 'Dev', 'start_date': '2024', 'end_date': '2026', 'description': 'coding'}],
        'projects': [{'name': 'Test Project', 'technologies': 'Python', 'description': 'built a tool'}],
        'skills': {'technical': ['Python', 'SQL'], 'soft': ['Communication']},
        'template': 'Modern'
    }
    
    # Save the resume
    resume_id = save_resume_data(resume_payload)
    assert resume_id is not None
    assert resume_id > 0
    
    # Save analysis data
    analysis_payload = {
        'ats_score': 85.0,
        'keyword_match_score': 90.0,
        'format_score': 80.0,
        'section_score': 100.0,
        'missing_skills': 'Docker, AWS',
        'recommendations': 'Add cloud experience.'
    }
    save_analysis_data(resume_id, analysis_payload)
    
    # Verify stats
    stats = get_resume_stats()
    assert stats is not None
    assert stats['total_resumes'] == 1
    assert stats['avg_ats_score'] == 85.0
    assert len(stats['recent_activity']) == 1
    assert stats['recent_activity'][0][0] == 'Test User'
    assert stats['recent_activity'][0][1] == 'Software Engineer'

def test_admin_logging_and_verification(monkeypatch):
    """Verify administrator action logging and authentication verification functions"""
    # Test logging
    log_admin_action("admin@example.com", "login")
    logs = get_admin_logs()
    
    assert len(logs) == 1
    assert logs[0][0] == "admin@example.com"
    assert logs[0][1] == "login"
    
    # Test verify_admin environment settings
    monkeypatch.setenv("ADMIN_EMAIL", "testadmin@test.com")
    monkeypatch.setenv("ADMIN_PASSWORD", "secret123")
    
    assert verify_admin("testadmin@test.com", "secret123") is True
    assert verify_admin("testadmin@test.com", "wrongpass") is False
    assert verify_admin("wrongadmin@test.com", "secret123") is False
