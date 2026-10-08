import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# Base Workspace Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Sessions Directory (Restricted to workspace folder to comply with guidelines)
SESSIONS_DIR = os.path.join(BASE_DIR, "backend", "sessions")

# Ensure sessions directory exists
os.makedirs(SESSIONS_DIR, exist_ok=True)

# Session configurations
SESSION_TTL_MINUTES = int(os.getenv("SESSION_TTL_MINUTES", "60"))
MAX_SESSIONS = int(os.getenv("MAX_SESSIONS", "50"))

# Piston Code Execution Sandbox API
PISTON_API_URL = os.getenv("PISTON_API_URL", "https://emkc.org/api/v2/piston/execute")

# LLM Spaces Configs (Gradio API Client endpoints)
LLM_PRIMARY_SPACE = os.getenv("LLM_PRIMARY_SPACE", "Qwen/Qwen3-VL-Demo")
LLM_FALLBACK_SPACE = os.getenv("LLM_FALLBACK_SPACE", "Qwen/Qwen2.5-VL-Demo")

# Gmail Alert settings (smtplib)
EMAIL_FROM = os.getenv("GMAIL_FROM", "")
EMAIL_TO = os.getenv("GMAIL_TO", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# Supported languages list and Piston integration mappings
SUPPORTED_LANGUAGES = {
    "python": "python",
    "javascript": "javascript",
    "typescript": "typescript",
    "java": "java",
    "cpp": "cpp",
    "c": "c",
    "go": "go",
    "rust": "rust",
    "bash": "bash"
}

# CORS settings
CORS_ORIGINS = ["*"]
