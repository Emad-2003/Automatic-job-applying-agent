
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from config import LINKEDIN_CREDENTIALS
import urllib.parse
import time


def scrape_linkedin(keywords: str, location: str, max_jobs: int, applied_urls: list[str]) -> list[dict]:
    search_url = (
        f"https://www.linkedin.com/jobs/search/?"
        f"keywords={keywords.replace(' ', '%20')}&location={location}"
    )

    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )

        page = context.new_page()

        stealth = Stealth()
        stealth.apply_stealth_sync(page)

        # ── Login ─────────────────────────────
        print("[LinkedIn] Logging in...")
        page.goto("https://www.linkedin.com/login")
        page.wait_for_timeout(2000)

        page.fill("#username", LINKEDIN_CREDENTIALS["email"])
        page.fill("#password", LINKEDIN_CREDENTIALS["password"])
        page.click("button[type='submit']")
        page.wait_for_timeout(5000)

        if "checkpoint" in page.url or "challenge" in page.url:
            print("[LinkedIn] ⚠️ Solve captcha manually (30s)...")
            page.wait_for_timeout(30000)

        # ── Search ────────────────────────────
        print("[LinkedIn] Searching jobs...")
        page.goto(search_url, wait_until="domcontentloaded", timeout=60000)

        page.wait_for_selector("div.job-card-container", timeout=20000)

        for _ in range(5):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        print("[LinkedIn] Collecting jobs...")

        total_cards = len(page.query_selector_all("div.job-card-container"))

        for i in range(min(max_jobs, total_cards)):
            try:
                # 🔥 Fix stale DOM
                job_cards = page.query_selector_all("div.job-card-container")
                card = job_cards[i]

                card.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                card.click()

                page.wait_for_selector("h1", timeout=10000)

                # ── Extract basic details ─────────
                title_el = page.query_selector("h1")

                company_el = page.query_selector(
                    "div.job-details-jobs-unified-top-card__company-name a"
                )
                if not company_el:
                    company_el = page.query_selector("span.tvm__text")

                location_el = page.query_selector("span.tvm__text--low-emphasis")

                title = title_el.inner_text().strip() if title_el else "N/A"
                company = company_el.inner_text().strip() if company_el else "N/A"
                loc = location_el.inner_text().strip() if location_el else "N/A"

                job_url = None
                easy_apply = False

                # ── 1. Hidden offsite link ───────
                offsite_link = page.query_selector("a[href*='offsite']")
                if offsite_link:
                    job_url = offsite_link.get_attribute("href")

                    if job_url:
                        parsed = urllib.parse.urlparse(job_url)
                        if "url=" in parsed.query:
                            job_url = urllib.parse.parse_qs(parsed.query)["url"][0]

                # ── 2. Apply button → new tab ────
                if not job_url:
                    apply_btn = page.query_selector("button.jobs-apply-button")

                    if apply_btn:
                        btn_text = apply_btn.inner_text().lower()

                        if "easy apply" in btn_text:
                            easy_apply = True
                        else:
                            try:
                                with context.expect_page(timeout=10000) as new_page_info:
                                    apply_btn.click()

                                new_page = new_page_info.value

                                # ⚡ FAST URL capture (handles slow loading)
                                for _ in range(10):
                                    current_url = new_page.url
                                    if current_url and current_url != "about:blank":
                                        job_url = current_url
                                        break
                                    time.sleep(0.5)

                                if not job_url:
                                    job_url = new_page.url

                                new_page.close()

                            except Exception as e:
                                print(f"[LinkedIn] New tab failed: {e}")

                # ── 3. Same tab fallback ─────────
                if not job_url:
                    page.wait_for_timeout(3000)
                    current_url = page.url

                    if "linkedin.com" not in current_url:
                        job_url = current_url
                        print("[LinkedIn] Captured same-tab external URL")

                # ❌ Skip invalid
                if not job_url or job_url in applied_urls:
                    continue

                print(f"[DEBUG] URL: {job_url}")

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": loc,
                    "url": job_url,
                    "description": "",
                    "easy_apply": easy_apply,
                    "source": "linkedin",
                })

                print(f"[LinkedIn] ✅ {title} @ {company}")

            except Exception as e:
                print(f"[LinkedIn] ⚠️ Skipped card — {e}")
                continue

        browser.close()

    return jobs
