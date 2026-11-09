"""Central configuration — loads .env once, exposes all settings.

Every module should import from here instead of reading os.environ directly.
This ensures .env is loaded exactly once and all defaults are in one place.
"""

import os
from pathlib import Path

# ── Load .env file ──────────────────────────────────────────────────────
# python-dotenv reads the .env file and populates os.environ.
# If python-dotenv is not installed, we fall back to os.environ only.
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(_env_path)
except ImportError:
    pass  # python-dotenv not installed; rely on environment variables


# ── MongoDB ─────────────────────────────────────────────────────────────
MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "sarta_db")

# ── Judge0 CE Sandbox ──────────────────────────────────────────────────
JUDGE0_URL: str = os.getenv("JUDGE0_URL", "http://127.0.0.1:2358").rstrip("/")
JUDGE0_API_KEY: str = os.getenv("JUDGE0_API_KEY", "").strip()
JUDGE0_API_HOST: str = os.getenv("JUDGE0_API_HOST", "judge0-ce.p.rapidapi.com").strip()

# ── LLM Question Generator (for dynamic JD topics) ─────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "").strip()
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()
OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")

# ── SQLite Session Store ───────────────────────────────────────────────
SARTA_ASSESSMENT_DB: str = os.getenv(
    "SARTA_ASSESSMENT_DB",
    str(Path(__file__).resolve().parent / "assessment_sessions.sqlite3"),
)

# ── Server ─────────────────────────────────────────────────────────────
SARTA_HOST: str = os.getenv("SARTA_HOST", "0.0.0.0")
SARTA_PORT: int = int(os.getenv("SARTA_PORT", "8000"))

