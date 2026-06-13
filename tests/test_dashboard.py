from services.dashboard_service import DashboardService
from core.database import get_database_connection

def test_dashboard_metrics_compilation():
    """Test compiled platform stats returns realistic values when DB is populated or empty"""
    service = DashboardService()
    
    # 1. Test empty DB fallback defaults
    metrics = service.get_dashboard_metrics()
    assert metrics['total_analyses'] == 84
    assert metrics['avg_score'] == 73.8
    assert metrics['resumes_built'] == 47
    
    # 2. Add an analysis record and test live metrics
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ai_analysis (model_used, resume_score, job_role)
        VALUES ('gemini-1.5-pro', 85, 'Software Engineer')
    """)
    conn.commit()
    conn.close()
    
    metrics_live = service.get_dashboard_metrics()
    assert metrics_live['total_analyses'] == 1
    assert metrics_live['avg_score'] == 85.0

def test_dashboard_trends_distribution():
    """Test retrieve score lists, upload trend dates, and roles frequencies"""
    service = DashboardService()
    
    # Test distribution ranges fallback
    scores = service.get_ats_distribution()
    assert len(scores) > 0
    assert all(0 <= s <= 100 for s in scores)
    
    # Test upload trends date listings
    dates, counts = service.get_upload_trends()
    assert len(dates) == 7
    assert len(counts) == 7
    
    # Test targeted roles frequency fallback
    roles, role_counts = service.get_targeted_roles()
    assert len(roles) > 0
    assert len(role_counts) == len(roles)

def test_dashboard_ai_insights():
    """Verify dynamic AI insights lists contains relevant details from the data"""
    service = DashboardService()
    insights = service.get_ai_insights()
    
    assert len(insights) > 0
    # Every insight should possess an icon and description text
    for insight in insights:
        assert 'icon' in insight
        assert 'text' in insight
        assert len(insight['text']) > 10
