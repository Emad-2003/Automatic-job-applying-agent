# Automatic-job-applying-agent

Every 24 hours:
│
├── 1. Scrape Indeed + LinkedIn for new jobs
│
├── 2. For each new job:
│   ├── Get/create branch: company_resume
│   ├── Tailor ALL 3 templates (Corporate, NIT, ZeroNoise) with Gemini
│   ├── ATS loop each until 90+ score
│   ├── Compile all 3 → PDF via pdflatex
│   ├── Pick highest ATS scorer as "best PDF"
│   └── Commit all 3 to branch with job title + ATS scores
│
└── 3. Show confirmation prompt:
    "Apply to SDE @ Amazon? [ATS: 94] (Corporate template) [y/n]"
    ├── y → Playwright applies with best PDF
    └── n → skips, marks as skipped in jobs_applied.json
