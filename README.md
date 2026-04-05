<div align="center">

# 🐝 Beeline

**Straight to the job. No detours.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-pdflatex-008080?style=flat-square&logo=latex&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-API-8E75B2?style=flat-square&logo=google&logoColor=white)
![ATS](https://img.shields.io/badge/ATS%20Score-%E2%89%A590-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

*No fluff. No ATS headaches. No wasted afternoons copy-pasting your resume into broken forms.*
*Just you, your resume, and the job — straight line, no detours.*

</div>

---

## What is Beeline?

Remember when job hunting meant printing your resume, walking in, and talking to someone? No keyword stuffing. No 47-step applications. No getting filtered out by a bot before a human ever sees your name.

**Beeline brings that back.**

Like a bee flying straight back to the hive — no zigzagging, no wasted energy — Beeline cuts straight through the noise. It scrapes fresh listings from **Indeed** and **LinkedIn**, tailors your resume to each role using **Gemini AI**, iterates until the ATS score hits **≥ 90**, compiles a clean PDF, and submits the application — all while you do something better with your time.

One confirmation prompt. That's the only thing it asks of you.

---

## Features

| | |
|---|---|
| 🔍 **Job Discovery** | Scrapes live listings from Indeed & LinkedIn on a schedule you set |
| 📄 **Resume Tailoring** | Generates 3 templates per job — Corporate, NIT, and ZeroNoise |
| 🎯 **ATS Optimization** | Iterates with Gemini until every template scores ≥ 90 |
| 📦 **PDF Compilation** | Compiles the best-scoring version via `pdflatex` |
| ✅ **Human-in-the-Loop** | One confirmation prompt before anything is submitted |
| 🌿 **Git Branching** | Each company gets its own branch: `<company>_resume` |
| 📝 **Audit Log** | Every result — applied, skipped, scores — logged to `jobs_applied.json` |

---

## How It Works

```
Scrape Indeed + LinkedIn
        │
        ▼
  Deduplicate & Queue New Listings
        │
        ▼
  For each job:
  ├── git checkout -b <company>_resume
  ├── Tailor 3 resume templates:
  │     ├── Corporate
  │     ├── NIT
  │     └── ZeroNoise
  ├── ATS Optimization Loop:
  │     └── Gemini rewrites → score → repeat until ≥ 90
  ├── Compile PDFs via pdflatex
  ├── Select best resume (highest ATS score)
  └── Commit: resumes + scores + job metadata
        │
        ▼
  🐝 Apply to Senior Engineer @ Stripe? [ATS: 94] (ZeroNoise) [y/n]
  ├── y → Playwright submits the application
  └── n → Logged & skipped
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core orchestration & scripting |
| **Playwright** | Browser automation for submissions |
| **pdflatex / LaTeX** | Resume PDF compilation |
| **Gemini API** | Resume tailoring & ATS optimization |
| **BeautifulSoup + Requests** | Scraping Indeed & LinkedIn |
| **APScheduler** | Recurring scrape scheduling |

---

## Quickstart

### Prerequisites

- Python 3.10+
- A LaTeX distribution — [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/)
- A [Gemini API key](https://aistudio.google.com/app/apikey)

### Installation

```bash
# 1. Clone
git clone https://github.com/your-username/beeline
cd beeline

# 2. Virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / Mac
.venv\Scripts\activate           # Windows

# 3. Install
pip install -r requirements.txt
playwright install chromium

# 4. Configure
cp .env.example .env
# Fill in your credentials

# 5. Run
python main.py
```

---

## Environment Variables

```env
# Gemini
GEMINI_API_KEY=your_gemini_api_key

# LinkedIn
LINKEDIN_EMAIL=you@example.com
LINKEDIN_PASSWORD=your_password

# Indeed
INDEED_EMAIL=you@example.com
INDEED_PASSWORD=your_password

# Search config
JOB_TITLES=Software Engineer,Backend Developer
LOCATIONS=Remote,San Francisco CA
ATS_THRESHOLD=90

# Schedule
SCRAPE_INTERVAL_HOURS=6
```

> ⚠️ Never commit `.env`. It is already in `.gitignore`.

---

## Project Structure

```
beeline/
│
├── scraper/
│   ├── indeed.py          # Indeed scraping
│   ├── linkedin.py        # LinkedIn scraping
│   └── dedup.py           # Deduplication logic
│
├── resume/
│   ├── templates/
│   │   ├── corporate.tex
│   │   ├── nit.tex
│   │   └── zeronoise.tex
│   └── tailor.py          # Gemini tailoring
│
├── ats/
│   ├── scorer.py          # ATS scoring
│   └── optimizer.py       # Optimization loop
│
├── apply/
│   ├── indeed_apply.py    # Playwright — Indeed
│   └── linkedin_apply.py  # Playwright — LinkedIn
│
├── data/                  # git-ignored
│   └── jobs_applied.json  # Audit log
│
├── main.py                # Entry point
├── scheduler.py           # Cron config
├── config.py              # Settings from .env
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Confirmation Prompt

```
🐝 Apply to Senior Backend Engineer @ Stripe? [ATS: 94] (ZeroNoise) [y/n]: _
```

- **`y`** — Playwright submits the application.
- **`n`** — Logged as skipped. Nothing is sent.

---

## Logs

```json
[
  {
    "company": "Stripe",
    "role": "Senior Backend Engineer",
    "platform": "LinkedIn",
    "ats_score": 94,
    "template": "ZeroNoise",
    "status": "applied",
    "applied_at": "2025-08-14T10:32:00Z"
  },
  {
    "company": "Notion",
    "role": "Platform Engineer",
    "platform": "Indeed",
    "ats_score": 91,
    "template": "Corporate",
    "status": "skipped",
    "applied_at": "2025-08-14T10:35:00Z"
  }
]
```

---

## Important Notes

- **`.env` is required** — Beeline won't run without it.
- **Use responsibly** — respect each platform's Terms of Service.
- **LaTeX must be installed** — `pdflatex` must be available in your PATH.
- **Generated files are git-ignored** — PDFs, scores, and logs stay local.

---

## Contributing

PRs are welcome. Open an issue first for major changes.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add some feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

<div align="center">
  <sub>🐝 Beeline · Straight to the job. No detours.</sub>
</div>
