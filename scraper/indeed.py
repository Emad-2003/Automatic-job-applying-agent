# scraper/indeed.py

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth


def scrape_indeed(keywords: str, location: str, max_jobs: int, applied_urls: list[str]) -> list[dict]:
    url = f"https://in.indeed.com/jobs?q={keywords.replace(' ', '+')}&l={location}"
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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

        print(f"[Indeed] Navigating to search page...")
        page.goto(url)
        page.wait_for_timeout(3000)

        # Cloudflare check
        if "challenge" in page.url or "captcha" in page.content().lower():
            print("[Indeed] ⚠️  Cloudflare detected — you have 30s to solve it manually...")
            page.wait_for_timeout(30000)

        # Scroll to load more cards
        for _ in range(3):
            page.keyboard.press("End")
            page.wait_for_timeout(1000)

        job_cards = page.query_selector_all("div.job_seen_beacon")
        print(f"[Indeed] Found {len(job_cards)} cards, processing up to {max_jobs}...")

        for card in job_cards[:max_jobs]:
            try:
                title_el    = card.query_selector("h2.jobTitle span")
                company_el  = card.query_selector("[data-testid='company-name']")
                location_el = card.query_selector("[data-testid='text-location']")
                link_el     = card.query_selector("a[data-jk]")

                title    = title_el.inner_text().strip()    if title_el    else "N/A"
                company  = company_el.inner_text().strip()  if company_el  else "N/A"
                loc      = location_el.inner_text().strip() if location_el else "N/A"
                href     = link_el.get_attribute("href")    if link_el     else ""
                job_url  = "https://in.indeed.com" + href   if href        else ""

                if not job_url or job_url in applied_urls:
                    continue

                # Click to load job description panel
                card.click()
                page.wait_for_timeout(2000)

                desc_el     = page.query_selector("#jobDescriptionText")
                description = desc_el.inner_text().strip() if desc_el else "N/A"
                easy_apply  = page.query_selector("button[id*='indeedApplyButton']") is not None

                jobs.append({
                    "title":       title,
                    "company":     company,
                    "location":    loc,
                    "url":         job_url,
                    "description": description,
                    "easy_apply":  easy_apply,
                    "source":      "indeed",
                })
                print(f"[Indeed] ✅ {title} @ {company}  |  Easy Apply: {easy_apply}")

            except Exception as e:
                print(f"[Indeed] ⚠️  Skipped card — {e}")
                continue

        browser.close()

    return jobs
