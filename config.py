import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ─── Gemini ────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ─── Repo & Templates ──────────────────────────────────────
RESUMES_REPO_PATH = os.path.expanduser("~/Resumes")

TEMPLATES = {
    "Corporate":  os.path.join(RESUMES_REPO_PATH, "Corporate",  "Resume.tex"),
    "NIT":        os.path.join(RESUMES_REPO_PATH, "NIT",        "Resume.tex"),
    "ZeroNoise":  os.path.join(RESUMES_REPO_PATH, "ZeroNoise",  "Resume.tex"),
}

# ─── Job Search ────────────────────────────────────────────
JOB_SEARCH = {
    "keywords": "software engineer fresher",
    "location": "India",
    "max_jobs": 10,
}

# ─── ATS ───────────────────────────────────────────────────
ATS_TARGET_SCORE = 90
MAX_ATS_RETRIES  = 5

# ─── Your Info ─────────────────────────────────────────────
YOUR_INFO = {
    "name":     os.getenv("USER_NAME"),
    "email":    os.getenv("USER_EMAIL"),
    "phone":    os.getenv("USER_PHONE"),
    "linkedin": os.getenv("USER_LINKEDIN"),
    "github":   os.getenv("USER_GITHUB"),
}

# ─── Credentials ───────────────────────────────────────────
INDEED_CREDENTIALS = {
    "email":    os.getenv("INDEED_EMAIL"),
    "password": os.getenv("INDEED_PASSWORD"),
}

LINKEDIN_CREDENTIALS = {
    "email":    os.getenv("LINKEDIN_EMAIL"),
    "password": os.getenv("LINKEDIN_PASSWORD"),
}

# ─── Safety Checks (VERY IMPORTANT) ─────────────────────────
required_vars = [
    "GEMINI_API_KEY",
    "INDEED_EMAIL", "INDEED_PASSWORD",
    "LINKEDIN_EMAIL", "LINKEDIN_PASSWORD",
    "USER_NAME", "USER_EMAIL", "USER_PHONE"
]

for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing environment variable: {var}")