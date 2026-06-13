# Smart Resume AI

Professional AI-powered Resume Analysis and Resume Building Platform.

Smart Resume AI is a modern SaaS platform designed to optimize resumes for Applicant Tracking Systems (ATS) and align candidates with their target job roles. Built with a dark glassmorphic design and modular Python services, the platform provides deep parsing analytics, automated resume builders, and job portals integration.

---

## 🚀 Overview

Smart Resume AI bridges the gap between candidate resumes and job postings:
* **Resume Analyzer**: Scans uploaded PDF/Word resumes, checks structure, formatting constraints, and matches keywords.
* **Resume Builder**: Step-by-step wizard to dynamically compile resumes and export formatted Word (`.docx`) files.
* **ATS Score Analysis**: Rates candidate resumes against target job description requirements.
* **Dashboard Analytics**: Renders metrics trends, score distributions, and dynamic AI insights.
* **Job Search**: Assembles direct search links for Naukri, LinkedIn, Foundit, and Indeed, alongside a LinkedIn automated web scraper.
* **Feedback System**: Category-based interface for user bug reports and suggestions.
* **Admin Features**: Session audit logs, submissions records, and direct Excel database exports.

---

## ✨ Features

* 🔍 **ATS Resume Analysis**: Granular formatting, structure, and keyword compatibility scorecard.
* 🤖 **AI Resume Evaluation**: Deep suggestions utilizing LLM (Google Gemini) integration.
* 📝 **Resume Builder**: Professional templates (Modern, Professional, Minimal, Creative) with multi-step workflows.
* 📊 **Dashboard Analytics**: High-performance Plotly charts mapping score spreads and upload traffic.
* 🧩 **Skill Gap Detection**: Pinpoints exact missing qualifications between target roles and profiles.
* 🔗 **Job Recommendations**: Direct queries compilation and search list matching.
* 💬 **Feedback Management**: Easy-to-use form to collect and save user suggestions.
* 🔐 **Admin Dashboard**: Audits login session logs, exports data spreadsheets, and monitors traffic.

---

## 🛠️ Tech Stack

* **Frontend & Shell**: Streamlit, HTML5, custom Vanilla HSL CSS variables
* **Backend Processing**: Python 3.12, Pandas, SQLite3
* **Interactive Visualizations**: Plotly Express & Plotly Graph Objects
* **Document Services**: Python-docx, PyPDF2
* **NLP & Scraping**: NLTK, Google Generative AI (Gemini SDK), Selenium WebDriver

---

## 📐 Project Architecture

```
Smart-AI-Resume-Analyzer/
├── app.py                  # Main routing entry point
├── Dockerfile              # Docker container settings
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Testing / development dependencies
├── resume_data.db          # Unified database storage
│
├── assets/                 # Custom HSL stylesheets, animations, and logos
│   ├── css/
│   │   └── style.css       # Unified SaaS CSS variables
│   ├── screenshots/        # Application UI screenshot files
│   └── videos/             # Product video records
│
├── core/                   # Configurations, constants, session, and DB managers
│   ├── config.py
│   ├── constants.py
│   ├── database.py
│   └── session.py
│
├── database/               # Database tables schemas and migrations
│   ├── schema.py
│   └── migrations.py
│
├── components/             # Reusable UI widgets and Plotly graphs
│   ├── cards.py
│   ├── charts.py
│   ├── metrics.py
│   └── navbar.py
│
├── services/               # Parsers, builders, scrapers, and AI logic
│   ├── resume_service.py
│   ├── ai_analysis_service.py
│   ├── dashboard_service.py
│   ├── feedback_service.py
│   └── job_service.py
│
└── tests/                  # Automated pytest testing files
    ├── conftest.py
    ├── test_analyzer.py
    ├── test_database.py
    └── test_dashboard.py
```

---

## 📸 Screenshots

To help you navigate the system, visual screenshots are configured in the repository:

* **Home Landing**: `assets/screenshots/home.png`
* **Scorecard Analyzer**: `assets/screenshots/analyzer.png`
* **Wizard Builder**: `assets/screenshots/builder.png`
* **Metrics Dashboard**: `assets/screenshots/dashboard.png`
* **Feedback Page**: `assets/screenshots/feedback.png`
* **About Page**: `assets/screenshots/about.png`
* **Admin Auth Panel**: `assets/screenshots/admin.png`

*(Refer to the [SCREENSHOT_GUIDE.md](SCREENSHOT_GUIDE.md) file for instructions on updating these files.)*

---

## 🎥 Demo Video

Watch the complete project demo:
* **Product Walkthrough Video**: `assets/videos/demo.mp4`

*(Refer to the [VIDEO_GUIDE.md](VIDEO_GUIDE.md) file for instructions on recording walkthrough segments.)*

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/IamNamanSingh/Smart-AI-Resume-Analyzer.git
cd Smart-AI-Resume-Analyzer
```

### 2. Set up virtual environment
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install packages
```bash
pip install -r requirements.txt
```

---

## 🚀 Running Locally

### 1. Configure Secrets
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your_secure_password_here
```

### 2. Boot Streamlit Server
```bash
python -m streamlit run app.py
```
Open your browser to [http://localhost:8501](http://localhost:8501).

---

## 🌐 Deployment

### Streamlit Cloud
1. Push your repository to GitHub.
2. Link your account to [Streamlit Share](https://share.streamlit.io/).
3. Create a **New App**, selecting the repository and `app.py` as entrypoint.
4. Set environment secrets inside settings.

### Docker Support
Build and run via Docker:
```bash
docker build -t smart-resume-ai .
docker run -d -p 8501:8501 -e GOOGLE_API_KEY="key" smart-resume-ai
```

---

## 🗺️ Future Roadmap

* **Asynchronous Scrapers**: Shift scraping jobs to celery task pipelines.
* **Interactive AI Chat**: Let candidates talk directly with the AI about resume improvements.
* **Granular Skills Progressions**: Render line graphs monitoring skills gains over multiple updates.

---

## 👤 Author

* **Naman Singh**
* **GitHub**: [IamNamanSingh](https://github.com/IamNamanSingh)
* **LinkedIn**: [Naman Singh](https://www.linkedin.com/in/namansingh2405/)
* **Email**: namansingh2475@gmail.com
