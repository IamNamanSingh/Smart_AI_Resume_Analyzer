# SQLite Database Schemas for Smart Resume AI

CREATE_RESUME_DATA_TABLE = '''
CREATE TABLE IF NOT EXISTS resume_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    linkedin TEXT,
    github TEXT,
    portfolio TEXT,
    summary TEXT,
    target_role TEXT,
    target_category TEXT,
    education TEXT,
    experience TEXT,
    projects TEXT,
    skills TEXT,
    template TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

CREATE_RESUME_SKILLS_TABLE = '''
CREATE TABLE IF NOT EXISTS resume_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER,
    skill_name TEXT NOT NULL,
    skill_category TEXT NOT NULL,
    proficiency_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resume_data (id)
);
'''

CREATE_RESUME_ANALYSIS_TABLE = '''
CREATE TABLE IF NOT EXISTS resume_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER,
    ats_score REAL,
    keyword_match_score REAL,
    format_score REAL,
    section_score REAL,
    missing_skills TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resume_data (id)
);
'''

CREATE_ADMIN_LOGS_TABLE = '''
CREATE TABLE IF NOT EXISTS admin_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_email TEXT NOT NULL,
    action TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

CREATE_ADMIN_TABLE = '''
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

CREATE_AI_ANALYSIS_TABLE = '''
CREATE TABLE IF NOT EXISTS ai_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER,
    model_used TEXT,
    resume_score INTEGER,
    job_role TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resume_data (id)
);
'''

CREATE_FEEDBACK_TABLE = '''
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER,
    usability_score INTEGER,
    feature_satisfaction INTEGER,
    missing_features TEXT,
    improvement_suggestions TEXT,
    user_experience TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    name TEXT,
    email TEXT,
    category TEXT,
    feedback_text TEXT
);
'''
