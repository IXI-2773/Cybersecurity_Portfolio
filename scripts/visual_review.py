"""Focused actual Chrome viewport checks, screenshot capture, and navigation QA.

Run only in the dedicated visual-review GitHub Actions workflow. Uses Chrome,
Selenium and LOCAL file:// portfolio pages; no login or external page requests.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "visual-review-screenshots"
PAGES = {
    "home": "index.html",
    "synthetic-soc-preview": "projects/splunk-synthetic-preview.html",
    "soc-analyst-evidence": "projects/soc-analyst-evidence.html",
    "recruiter-profile": "recruiter.html",
    "application-toolkit": "apply.html",
    "celestial-resonance": "projects/celestial-resonance.html",
    "network": "projects/network-traffic-analysis.html",
    "vulnerability": "projects/vulnerability-remediation.html",
}
VIEWPORTS = {"mobile": (390, 844), "small-mobile": (320, 720),
             "tablet": (768, 900), "desktop": (1280, 900)}


def main() -> None:
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    driver_exe = shutil.which("chromedriver")
    if not chrome or not driver_exe:
        raise SystemExit("Chrome/ChromeDriver missing from runner; cannot claim browser validation")
    opts = webdriver.ChromeOptions()
    opts.binary_location = chrome
    for arg in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage",
                "--disable-gpu", "--hide-scrollbars", "--disable-background-networking"):
        opts.add_argument(arg)
    opts.add_argument("--window-size=1280,900")
    SCREENSHOTS.mkdir(exist_ok=True)
    results = []
    failures = []

    with webdriver.Chrome(service=Service(executable_path=driver_exe), options=opts) as driver:
        driver.set_page_load_timeout(20)
        for name, relative in PAGES.items():
            url = (ROOT / relative).resolve().as_uri()
            for viewport, (width, height) in VIEWPORTS.items():
                # Review 4 widths on homepage; 390 and 1280 on other pages.
                if name != "home" and viewport not in ("mobile", "desktop"):
                    continue
                driver.set_window_size(width, height)
                driver.get(url)
                body = driver.find_element(By.TAG_NAME, "body")
                h1 = driver.find_element(By.CSS_SELECTOR, "main#main h1")
                if not h1.is_displayed():
                    failures.append(f"{name}/{viewport}: main heading not displayed")
                dimensions = driver.execute_script("""
                    return {
                      viewport: document.documentElement.clientWidth,
                      viewportHeight: window.innerHeight,
                      scrollWidth: document.documentElement.scrollWidth,
                      mainWidth: document.querySelector('main').getBoundingClientRect().width
                    };
                """)
                if dimensions["scrollWidth"] > dimensions["viewport"] + 2:
                    failures.append(f"{name}/{viewport}: document horizontal overflow: {dimensions}")
                if name == "application-toolkit":
                    role_cards = driver.find_elements(By.CSS_SELECTOR, ".application-role-card")
                    downloads = driver.find_elements(By.CSS_SELECTOR, ".application-role-actions a[download]")
                    if len(role_cards) != 2 or len(downloads) != 2:
                        failures.append(f"{name}/{viewport}: expected two role cards and downloads")
                    for link in downloads:
                        relative_resume = link.get_attribute("href")
                        if not relative_resume or not relative_resume.endswith(".txt"):
                            failures.append(f"{name}/{viewport}: missing real text resume link")
                if name == "home":
                    featured = driver.find_element(By.ID, "featured-splunk")
                    if not featured.is_displayed() or len(featured.find_elements(By.CSS_SELECTOR, ".splunk-evidence-table tbody tr")) != 5:
                        failures.append(f"{name}/{viewport}: missing featured five-row Splunk evidence section")
                    proof_image = featured.find_element(By.CSS_SELECTOR, ".splunk-real-proof img")
                    if driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0;", proof_image) is not True:
                        failures.append(f"{name}/{viewport}: genuine Splunk screenshot failed to load")
                    quick_view = driver.find_element(By.ID, "soc-evidence")
                    if not quick_view.is_displayed():
                        failures.append(f"{name}/{viewport}: recruiter section hidden")
                    if len(quick_view.find_elements(By.CSS_SELECTOR, ".soc-proof-card")) != 4:
                        failures.append(f"{name}/{viewport}: expected four SOC evidence cards")
                    main_link = quick_view.find_element(By.CSS_SELECTOR, "a[href='projects/soc-analyst-evidence.html']")
                    if not main_link.is_displayed():
                        failures.append(f"{name}/{viewport}: SOC evidence detail link missing")
                    # The last line of the synthetic terminal must not be clipped.
                    status_box = driver.find_element(By.CSS_SELECTOR, ".terminal-result")
                    box_info = driver.execute_script("""
                        const el = arguments[0];
                        return {width: el.clientWidth, content_width: el.scrollWidth,
                                white_space: getComputedStyle(el).whiteSpace};
                    """, status_box)
                    if box_info["content_width"] > box_info["width"] + 2:
                        failures.append(f"{name}/{viewport}: terminal result clipped: {box_info}")
                    if viewport == "small-mobile":
                        cta = driver.find_element(By.CSS_SELECTOR, ".hero .actions .button.primary")
                        cta_bottom = driver.execute_script(
                            "return arguments[0].getBoundingClientRect().bottom", cta)
                        if cta_bottom > dimensions["viewportHeight"] - 1:
                            failures.append(
                                f"{name}/{viewport}: CTA bottom {cta_bottom:.1f}px exceeds "
                                f"actual visible height {dimensions['viewportHeight']}px")
                desktop_nav = driver.find_element(By.CSS_SELECTOR, ".nav > nav")
                menu = driver.find_element(By.CSS_SELECTOR, ".nav > details.mobile-nav")
                if dimensions["viewport"] <= 800:
                    if desktop_nav.is_displayed() or not menu.is_displayed():
                        failures.append(f"{name}/{viewport}: incorrect compact navigation visibility")
                    else:
                        summary = menu.find_element(By.TAG_NAME, "summary")
                        summary.send_keys(Keys.ENTER)
                        if menu.get_attribute("open") is None:
                            failures.append(f"{name}/{viewport}: keyboard Enter did not open native menu")
                        else:
                            first = menu.find_element(By.CSS_SELECTOR, "nav a")
                            if not first.is_displayed():
                                failures.append(f"{name}/{viewport}: opened navigation links not visible")
                        summary.send_keys(Keys.ENTER)
                        if menu.get_attribute("open") is not None:
                            failures.append(f"{name}/{viewport}: keyboard Enter did not close menu")
                elif not desktop_nav.is_displayed() or menu.is_displayed():
                    failures.append(f"{name}/{viewport}: desktop nav visibility incorrect")
                out = SCREENSHOTS / f"{name}-{viewport}.png"
                driver.save_screenshot(str(out))
                results.append({"page": relative, "viewport": viewport, "requested_width": width,
                                "observed_width": dimensions["viewport"],
                                "observed_height": dimensions["viewportHeight"],
                                "scroll_width": dimensions["scrollWidth"],
                                "screenshot": out.relative_to(ROOT).as_posix()})

    report = {"schema": "portfolio.chrome-responsive-review.v1",
              "browser": "Google Chrome or Chromium headless",
              "pages": len(PAGES),
              "viewports_reviewed": len(results),
              "screenshots": results, "failures": failures,
              "status": "PASS" if not failures else "FAIL",
              "limitations": "Checks keyboard nav and horizontal overflow; screenshots still need human visual review. Not a WCAG or screen-reader audit."}
    (SCREENSHOTS / "review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "viewports_reviewed": len(results),
                      "failures": failures, "screenshots": str(SCREENSHOTS)}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
