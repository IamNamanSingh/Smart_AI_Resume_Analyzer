from services.job_portals import JobPortal

class JobService:
    def __init__(self):
        self.portal = JobPortal()

    def get_filter_options(self):
        """Get filter configurations for job searches"""
        return {
            "experience_levels": [
                {"id": "all", "text": "All Levels"},
                {"id": "fresher", "text": "Fresher"},
                {"id": "0-1", "text": "0-1 years"},
                {"id": "1-3", "text": "1-3 years"},
                {"id": "3-5", "text": "3-5 years"},
                {"id": "5-7", "text": "5-7 years"},
                {"id": "7-10", "text": "7-10 years"},
                {"id": "10+", "text": "10+ years"}
            ],
            "salary_ranges": [
                {"id": "all", "text": "All Ranges"},
                {"id": "0-3", "text": "0-3 LPA"},
                {"id": "3-6", "text": "3-6 LPA"},
                {"id": "6-10", "text": "6-10 LPA"},
                {"id": "10-15", "text": "10-15 LPA"},
                {"id": "15+", "text": "15+ LPA"}
            ],
            "job_types": [
                {"id": "all", "text": "All Types"},
                {"id": "full-time", "text": "Full Time"},
                {"id": "part-time", "text": "Part Time"},
                {"id": "contract", "text": "Contract"},
                {"id": "remote", "text": "Remote"}
            ]
        }

    def build_search_links(self, job_title, location, experience=None):
        """Build search URLs for standard job portals"""
        return self.portal.search_jobs(job_title, location, experience)
