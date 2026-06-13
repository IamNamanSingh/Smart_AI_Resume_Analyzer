import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# App settings
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# Database settings
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resume_data.db"))

# Google & Gemini API settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Static assets settings
CSS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "css", "style.css")
IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "images")
ANIMATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "animations")
