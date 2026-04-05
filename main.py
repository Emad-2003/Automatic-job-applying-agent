# main.py

import os
import json

from config import RESUMES_REPO_PATH, TEMPLATES, JOB_SEARCH
from scraper.indeed   import scrape_indeed
from scraper.linkedin import scrape_linkedin
# from resume.rewriter  import rewrite_latex
# from resume.ats_scorer import optimize_template
# from resume.compiler  import compile_with_autofix
# from git_manager.branch import get_or_create_company_branch, commit_job_resume
# from applier.indeed_apply   import apply_indeed
# from applier.linkedin_apply import apply_linkedin

APPLIED_FILE = os.path.join(os.path.dirname(__file__), "jobs_applied.json")


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_applied() -> list[dict]:
    if os.path.exists(APPLIED_FILE):
        with open(APPLIED_FILE) as f:
            return json.load(f)
    return []

def save_applied(data: list[dict]):
    with open(APPLIED_FILE, "w") as f:
        json.dump(data, f, indent=2)

def confirm(prompt: str) -> bool:
    """Simple y/n prompt."""
    while True:
        ans = input(f"\n{prompt} [y/n] > ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False


# ── Core pipeline for a single job ───────────────────────────────────────────

def process_job(job: dict, applied: list[dict]) -> dict | None:
    """
    Runs the full resume pipeline for one job.
    Returns an entry to add to jobs_applied.json, or None on failure.
    """
    print(f"\n{'═'*64}")
    print(f"  📌  {job['title']}  @  {job['company']}")
    print(f"  🔗  {job['url']}")
    print(f"{'═'*64}")

    # ── Step 1: Git branch ────────────────────────────────────────────────────
    repo, branch_name = get_or_create_company_branch(job["company"])

    # ── Step 2: Process all 3 templates ──────────────────────────────────────
    results     = {}   # { template_name: (final_latex, ats_score) }
    best_name   = None
    best_score  = -1

    for template_name, template_path in TEMPLATES.items():
        print(f"\n  ── Template: {template_name} ──────────────────────────────")

        # Read base template
        with open(template_path, "r", encoding="utf-8") as f:
            base_latex = f.read()

        # Initial rewrite
        print(f"    [Rewriter] Tailoring for {job['company']}...")
        rewritten = rewrite_latex(base_latex, job)

        # ATS optimization loop
        print(f"    [ATS] Optimizing (target: 90+)...")
        final_latex, ats_score = optimize_template(rewritten, job, template_name)

        # Compile to PDF (with auto-fix on error)
        tex_path = template_path   # write back to same file on branch
        print(f"    [Compiler] Compiling PDF...")
        success, final_latex = compile_with_autofix(tex_path, final_latex)

        if not success:
            print(f"    ❌ Compilation failed for {template_name}, skipping template")
            continue

        results[template_name] = (final_latex, ats_score)

        if ats_score > best_score:
            best_score = ats_score
            best_name  = template_name

    if not results:
        print("  ❌ All templates failed — skipping this job")
        return None

    # ── Step 3: Commit all tailored templates ─────────────────────────────────
    commit_job_resume(repo, job, results, best_name)

    # ── Step 4: Confirmation prompt ───────────────────────────────────────────
    best_pdf = os.path.join(RESUMES_REPO_PATH, best_name, "Resume.pdf")
    scores   = "  |  ".join(f"{t}: {s}/100" for t, (_, s) in results.items())

    print(f"\n  📊 ATS Scores  : {scores}")
    print(f"  🏆 Best Template: {best_name}  ({best_score}/100)")
    print(f"  📄 PDF          : {best_pdf}")

    should_apply = confirm(
        f"Apply to '{job['title']}' @ {job['company']} "
        f"using {best_name} template (ATS: {best_score}/100)?"
    )

    if not should_apply:
        print("  ⏭️  Skipped by user.")
        return {
            "title":         job["title"],
            "company":       job["company"],
            "url":           job["url"],
            "source":        job["source"],
            "branch":        branch_name,
            "best_template": best_name,
            "best_score":    best_score,
            "all_scores":    {t: s for t, (_, s) in results.items()},
            "pdf_path":      best_pdf,
            "applied":       False,
            "skipped":       True,
        }

    # ── Step 5: Auto-apply ────────────────────────────────────────────────────
    if job["source"] == "indeed":
        success = apply_indeed(job, best_pdf)
    else:
        success = apply_linkedin(job, best_pdf)

    status = "✅ Applied" if success else "❌ Apply failed"
    print(f"  {status}")

    return {
        "title":         job["title"],
        "company":       job["company"],
        "url":           job["url"],
        "source":        job["source"],
        "branch":        branch_name,
        "best_template": best_name,
        "best_score":    best_score,
        "all_scores":    {t: s for t, (_, s) in results.items()},
        "pdf_path":      best_pdf,
        "applied":       success,
        "skipped":       False,
    }


# ── Main run ──────────────────────────────────────────────────────────────────

def run():
    print("\n🚀  Resume Agent Starting...\n")

    applied = load_applied()
    applied_urls = {j["url"] for j in applied}

    # ── Scrape ────────────────────────────────────────────────────────────────
    # indeed_jobs   = scrape_indeed(
    #     JOB_SEARCH["keywords"], JOB_SEARCH["location"],
    #     JOB_SEARCH["max_jobs"], applied_urls
    # )


    linkedin_jobs = scrape_linkedin(
        JOB_SEARCH["keywords"], JOB_SEARCH["location"],
        JOB_SEARCH["max_jobs"], applied_urls
    )
    


    # all_jobs = indeed_jobs + linkedin_jobs
    # print(f"\n📋  New jobs found: {len(all_jobs)}\n")

    # if not all_jobs:
    #     print("No new jobs to process.")
    #     return

    # # ── Process each job ──────────────────────────────────────────────────────
    # for job in all_jobs:
    #     entry = process_job(job, applied)
    #     if entry:
    #         applied.append(entry)
    #         save_applied(applied)   # save after every job so progress is not lost

    # # Return to master when done
    # import git
    # git.Repo(RESUMES_REPO_PATH).git.checkout("master")

    # applied_count = sum(1 for j in applied if j.get("applied"))
    # print(f"\n\n✅  Run complete! Total applied so far: {applied_count}")
    # print(f"📁  Log: {APPLIED_FILE}\n")


if __name__ == "__main__":
    run()
