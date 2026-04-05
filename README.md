# Automatic-job-applying-agent

1. Scrape job listings from:
   - Indeed
   - LinkedIn

2. Process each new job:
   ├── Create or checkout branch: <company>_resume
   ├── Tailor all 3 resume templates using Gemini:
   │     - Corporate
   │     - NIT
   │     - ZeroNoise
   │
   ├── Run ATS optimization loop:
   │     - Iterate until score ≥ 90
   │
   ├── Generate PDFs:
   │     - Compile all templates using pdflatex
   │
   ├── Select best resume:
   │     - Choose highest ATS scoring PDF
   │
   └── Commit results:
         - All 3 resumes
         - ATS scores
         - Job metadata
         - Commit message includes job title + scores

3. User Confirmation Step:
   Prompt:
   "Apply to <Role> @ <Company>? [ATS: XX] (<Template Name>) [y/n]"

   ├── If YES:
   │     - Apply automatically using Playwright
   │     - Upload best-scoring resume
   │
   └── If NO:
         - Skip job
         - Mark as skipped in jobs_applied.json
