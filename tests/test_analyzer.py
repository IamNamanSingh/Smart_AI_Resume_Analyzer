from services.resume_service import ResumeAnalyzer

def test_resume_document_type_detection():
    """Verify that the parser correctly classifies documents based on keyword density"""
    analyzer = ResumeAnalyzer()
    
    resume_text = "John Doe\nExperience: Software Developer at XYZ.\nEducation: B.S. Computer Science.\nSkills: Python, Go."
    marksheet_text = "Grade Sheet\nSemester 1 marks: 85, Semester 2: 90\nSGPA: 8.8, CGPA: 9.0"
    
    assert analyzer.detect_document_type(resume_text) == 'resume'
    assert analyzer.detect_document_type(marksheet_text) == 'marksheet'

def test_resume_personal_info_extraction():
    """Test standard regex extraction of contact metadata from raw text"""
    analyzer = ResumeAnalyzer()
    sample_text = (
        "Naman Singh\n"
        "Email: candidate@example.com\n"
        "Phone: 9876543210\n"
        "LinkedIn: linkedin.com/in/namansingh2405\n"
        "GitHub: github.com/IamNamanSingh"
    )
    
    info = analyzer.extract_personal_info(sample_text)
    assert info['name'] == "Naman Singh"
    assert info['email'].strip() == "candidate@example.com"
    assert info['phone'].strip() == "9876543210"
    assert "namansingh2405" in info['linkedin']
    assert "IamNamanSingh" in info['github']

def test_resume_keyword_matching():
    """Verify keyword alignment checks between resume skills and job requirements"""
    analyzer = ResumeAnalyzer()
    resume_text = "Experienced in Python programming, React frontend, and SQL databases."
    required_skills = ["Python", "React", "Docker", "SQL"]
    
    match_result = analyzer.calculate_keyword_match(resume_text, required_skills)
    assert match_result['score'] == 75.0
    assert "Python" in match_result['found_skills']
    assert "Docker" in match_result['missing_skills']

def test_resume_sections_and_formatting():
    """Test check_formatting and check_resume_sections logic for scoring checks"""
    analyzer = ResumeAnalyzer()
    
    # Enrich text to cover multiple keywords per section
    resume_text = (
        "JOHN DOE\n"
        "Email: john.doe@example.com\n"
        "Phone: 123-456-7890\n"
        "Address: 123 Main St\n"
        "LinkedIn: linkedin.com/in/johndoe\n\n"
        "SUMMARY\n"
        "Detail-oriented developer.\n\n"
        "EDUCATION\n"
        "BS degree in CS at University of Tech college, academic studies\n\n"
        "EXPERIENCE\n"
        "work employment history: job developer internship\n"
        "- Developed backend apps in Python\n"
        "- Maintained cloud servers\n\n"
        "SKILLS\n"
        "technologies and tools expertise and proficiencies\n"
        "Python, JavaScript, SQL\n"
    )
    
    section_score = analyzer.check_resume_sections(resume_text)
    # Check that contact, education, experience, and skills sections are detected
    assert section_score > 50
    
    format_score, deductions = analyzer.check_formatting(resume_text)
    assert format_score > 0
    # No bullet point deduction since we included '-' bullets
    assert not any("bullet points" in d.lower() for d in deductions)
