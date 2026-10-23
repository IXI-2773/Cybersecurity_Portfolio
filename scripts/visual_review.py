"""Focused actual Chrome viewport checks, screenshot capture, and navigation QA.

Run only in the dedicated visual-review GitHub Actions workflow. Uses Chrome,
Selenium and LOCAL file:// portfolio pages; no login or external page requests.
"""
from __future__ import annotations

import base64
import json
import re
import subprocess
from pathlib import Path
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "visual-review-screenshots"
PAGES = {
    "home": "index.html",
    "explorer": "explore.html",
    "evidence-review": "verify.html",
    "role-paths": "roles.html",
    "test-workbench": "test-lab.html",
    "synthetic-soc-preview": "projects/splunk-synthetic-preview.html",
    "soc-analyst-evidence": "projects/soc-analyst-evidence.html",
    "recruiter-profile": "recruiter.html",
    "application-toolkit": "apply.html",
    "celestial-resonance": "projects/celestial-resonance.html",
    "network": "projects/network-traffic-analysis.html",
    "vulnerability": "projects/vulnerability-remediation.html",
    "authentication": "projects/authentication-detection.html",
    "windows": "projects/windows-process-triage.html",
    "research-ai": "projects/research-ai-infrastructure.html",
    "analyst-workflow": "projects/soc-analyst-workflow.html",
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
    downloads = SCREENSHOTS / "downloads"
    downloads.mkdir(exist_ok=True)
    opts.add_experimental_option("prefs", {"download.default_directory": str(downloads), "download.prompt_for_download": False})
    results = []
    failures = []
    print_review = {"status": "NOT_RUN", "pages": None}

    with webdriver.Chrome(service=Service(executable_path=driver_exe), options=opts) as driver:
        driver.set_page_load_timeout(20)
        # Native WebDriver scrolling must settle before clicking offscreen controls.
        # Exercise the site's reduced-motion mode instead of racing smooth scroll.
        driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {
            "features": [{"name": "prefers-reduced-motion", "value": "reduce"}]
        })
        def click_control(element):
            # A native nearest-edge scroll can leave a target behind the sticky header.
            # Center the real control first, then use WebDriver's normal pointer click.
            driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", element)
            element.click()

        for name, relative in PAGES.items():
            url = (ROOT / relative).resolve().as_uri()
            for viewport, (width, height) in VIEWPORTS.items():
                # Check six rewritten cases at 320px as well as mobile/desktop.
                case_pages = {"authentication", "windows", "network", "vulnerability",
                              "celestial-resonance", "research-ai", "explorer", "test-workbench", "evidence-review", "role-paths"}
                if name != "home" and viewport not in ("mobile", "desktop"):
                    if name not in case_pages or viewport != "small-mobile":
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
                if dimensions["viewport"] != width:
                    failures.append(f"{name}/{viewport}: requested {width}px but observed {dimensions['viewport']}px")
                if dimensions["scrollWidth"] > dimensions["viewport"] + 2:
                    failures.append(f"{name}/{viewport}: document horizontal overflow: {dimensions}")
                if name in {"authentication", "windows", "network", "vulnerability",
                            "celestial-resonance", "research-ai"}:
                    bar = driver.find_element(By.CSS_SELECTOR, ".case-review-strip")
                    scope_type = bar.get_attribute("data-case-scope")
                    expected_scope = "private-summary" if name in {"celestial-resonance", "research-ai"} else "public-lab"
                    if scope_type != expected_scope:
                        failures.append(f"{name}/{viewport}: wrong evidence scope in case review bar")
                    actions = bar.find_elements(By.CSS_SELECTOR, ".case-review-actions a")
                    if len(actions) != 3:
                        failures.append(f"{name}/{viewport}: expected three reviewer shortcuts")
                    else:
                        for anchor in (actions[0], actions[2]):
                            dest = anchor.get_attribute("href").split("#")[-1]
                            if not driver.find_elements(By.ID, dest):
                                failures.append(f"{name}/{viewport}: broken case-section shortcut #{dest}")
                        click_control(actions[2])
                        if driver.execute_script("return location.hash") != "#" + actions[2].get_attribute("href").split("#")[-1]:
                            failures.append(f"{name}/{viewport}: evidence-limit shortcut did not navigate")
                        body.send_keys(Keys.CONTROL, Keys.HOME)
                    if not bar.is_displayed():
                        failures.append(f"{name}/{viewport}: review shortcuts hidden")
                if name == "role-paths":
                    sections = ("soc-analyst", "security-analyst", "security-automation")
                    if len(driver.find_elements(By.CSS_SELECTOR, ".role-route-card")) != 3:
                        failures.append(f"{name}/{viewport}: expected exactly three role links")
                    if len(driver.find_elements(By.CSS_SELECTOR, ".role-interview-question summary")) != 3:
                        failures.append(f"{name}/{viewport}: every role needs an interview disclosure")
                    for role_id in sections:
                        anchor = driver.find_element(By.CSS_SELECTOR, f'.role-route-card[href="#{role_id}"]')
                        click_control(anchor)
                        if driver.execute_script("return window.location.hash") != f"#{role_id}":
                            failures.append(f"{name}/{viewport}: role link did not navigate to {role_id}")
                        target = driver.find_element(By.ID, role_id)
                        if not target.is_displayed() or not target.find_element(By.TAG_NAME, "h2").is_displayed():
                            failures.append(f"{name}/{viewport}: hidden role section {role_id}")
                    first = driver.find_element(By.CSS_SELECTOR, "#soc-analyst .role-interview-question")
                    summary = first.find_element(By.TAG_NAME, "summary")
                    click_control(summary)
                    if first.get_attribute("open") is None:
                        failures.append(f"{name}/{viewport}: interview question did not expand")
                    click_control(summary)
                    if first.get_attribute("open") is not None:
                        failures.append(f"{name}/{viewport}: interview question did not collapse")
                    body.send_keys(Keys.CONTROL, Keys.HOME)
                if name in {"explorer", "test-workbench", "evidence-review"}:
                    shell = driver.find_element(By.CSS_SELECTOR, ".toolkit-masthead")
                    pipeline = driver.find_elements(By.CSS_SELECTOR, ".toolkit-pipeline a")
                    if not shell.is_displayed() or len(pipeline) != 3:
                        failures.append(f"{name}/{viewport}: missing common review navigation")
                    active = [a for a in pipeline if a.get_attribute("aria-current") == "page"]
                    if len(active) != 1 or not active[0].is_displayed():
                        failures.append(f"{name}/{viewport}: active review step not discoverable")
                if name == "evidence-review":
                    if len(driver.find_elements(By.CSS_SELECTOR, "[data-evidence-card]")) != 7:
                        failures.append(f"{name}/{viewport}: expected seven claim-to-source cards")
                    if len(driver.find_elements(By.CSS_SELECTOR, ".verification-limit")) != 7:
                        failures.append(f"{name}/{viewport}: every evidence item must state its limit")
                    jump_links = driver.find_elements(By.CSS_SELECTOR, ".verification-jump a")
                    if len(jump_links) != 3:
                        failures.append(f"{name}/{viewport}: evidence category anchors missing")
                    for link in jump_links:
                        anchor = link.get_attribute("href").split("#")[-1]
                        if not driver.find_elements(By.ID, anchor):
                            failures.append(f"{name}/{viewport}: evidence category anchor {anchor} not found")
                    if len(jump_links) == 3:
                        click_control(jump_links[2])
                        if driver.execute_script("return location.hash") != "#browser-title":
                            failures.append(f"{name}/{viewport}: public browser evidence jump failed")
                    if not driver.find_element(By.CSS_SELECTOR, 'a[href="https://github.com/IXI-2773/Cybersecurity_Portfolio/blob/main/splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md"]').is_displayed():
                        failures.append(f"{name}/{viewport}: missing native Splunk observation")
                if name == "explorer":
                    def shown_cards():
                        return [el for el in driver.find_elements(By.CSS_SELECTOR, "[data-project-entry]") if el.is_displayed()]
                    query = driver.find_element(By.ID, "project-search")
                    role = Select(driver.find_element(By.ID, "role-filter"))
                    quick_roles = driver.find_elements(By.CSS_SELECTOR, "[data-quick-role]")
                    if len(quick_roles) != 4:
                        failures.append(f"{name}/{viewport}: missing accessible role shortcuts")
                    else:
                        for focus, expected in (("soc", 4), ("automation", 4), ("security", 6), ("all", 7)):
                            click_control(driver.find_element(By.CSS_SELECTOR, f'[data-quick-role="{focus}"]'))
                            if role.first_selected_option.get_attribute("value") != focus:
                                failures.append(f"{name}/{viewport}: quick filter {focus} did not update select")
                            if driver.find_element(By.CSS_SELECTOR, f'[data-quick-role="{focus}"]').get_attribute("aria-pressed") != "true":
                                failures.append(f"{name}/{viewport}: quick filter {focus} not announced selected")
                            if len(shown_cards()) != expected:
                                failures.append(f"{name}/{viewport}: quick filter {focus} returned {len(shown_cards())}, expected {expected}")
                    if len(shown_cards()) != 7:
                        failures.append(f"{name}/{viewport}: all seven entries must be discoverable")
                    for acronym in ("CR", "RAI"):
                        query.clear()
                        query.send_keys(acronym)
                        if len(shown_cards()) != 1 or acronym not in shown_cards()[0].text:
                            failures.append(f"{name}/{viewport}: acronym {acronym} should find its engineering project")
                    role.select_by_value("soc")
                    if len(shown_cards()) != 0:
                        failures.append(f"{name}/{viewport}: role and keyword filters must combine")
                    click_control(driver.find_element(By.CSS_SELECTOR, "#project-filters button[type=reset]"))
                    query.send_keys("unmatched-portfolio-query")
                    if shown_cards() or not driver.find_element(By.ID, "filter-empty").is_displayed():
                        failures.append(f"{name}/{viewport}: missing zero-result feedback")
                    click_control(driver.find_element(By.CSS_SELECTOR, "#project-filters button[type=reset]"))
                    if len(shown_cards()) != 7:
                        failures.append(f"{name}/{viewport}: clear filters failed")
                    if viewport == "desktop":
                        try:
                            driver.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": True})
                            driver.get(url)
                            if len(shown_cards()) != 7 or driver.find_element(By.CSS_SELECTOR,"#project-filters fieldset").is_displayed():
                                failures.append("explorer/no-js: entries must remain visible and inert controls hidden")
                        finally:
                            driver.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": False})
                            driver.get(url)
                            body = driver.find_element(By.TAG_NAME, "body")
                    body.send_keys(Keys.CONTROL, Keys.HOME)
                if name == "test-workbench":
                    click_control(driver.find_element(By.ID, "run-checks"))
                    if "9 / 9" not in driver.find_element(By.ID,"checks-status").text:
                        failures.append(f"{name}/{viewport}: real baseline checks did not pass")
                    for seconds, count in ((599, 3), (600, 5)):
                        preset = driver.find_element(By.CSS_SELECTOR, f'[data-window-preset="{seconds}"]')
                        if preset.get_attribute("disabled") is not None:
                            failures.append(f"{name}/{viewport}: {seconds}s preset did not initialize")
                            continue
                        click_control(preset)
                        if (len(driver.find_elements(By.CSS_SELECTOR, "#replay-rows tr")) != count or
                                driver.find_element(By.ID, "auth-window").get_attribute("value") != str(seconds) or
                                preset.get_attribute("aria-pressed") != "true"):
                            failures.append(f"{name}/{viewport}: {seconds}s preset did not compute expected source rows")
                    window = driver.find_element(By.ID,"auth-window")
                    for seconds, count in ((599,3),(600,5)):
                        window.clear()
                        window.send_keys(str(seconds))
                        click_control(driver.find_element(By.ID,"replay-submit"))
                        if len(driver.find_elements(By.CSS_SELECTOR,"#replay-rows tr")) != count:
                            failures.append(f"{name}/{viewport}: {seconds}s must replay {count} fixture findings")
                    for sample, expected in (("complete","PASS_COVERAGE"),("omitted","HOLD_INCOMPLETE_COVERAGE"),("mismatch","HOLD_ATTRIBUTION_MISMATCH")):
                        Select(driver.find_element(By.ID,"coverage-case")).select_by_value(sample)
                        click_control(driver.find_element(By.ID,"coverage-submit"))
                        if driver.find_element(By.ID,"coverage-status").text != expected:
                            failures.append(f"{name}/{viewport}: incorrect structured coverage result for {sample}")
                    receipt_path = downloads / "Don_Lopez_Public_Engine_Run.json"
                    receipt_path.unlink(missing_ok=True)
                    click_control(driver.find_element(By.ID,"download-run"))
                    WebDriverWait(driver, 5).until(lambda _: receipt_path.is_file())
                    receipt = json.loads(receipt_path.read_text())
                    if (len(receipt["baseline"]["checks"]) != 9 or
                        not all(check["passed"] for check in receipt["baseline"]["checks"]) or
                        len(receipt["replay"]["findings"]) != 5 or
                        receipt["coverage"]["result"]["status"] != "HOLD_ATTRIBUTION_MISMATCH" or
                        len(receipt["sources"]) != 2):
                        failures.append(f"{name}/{viewport}: downloaded receipt differs from actual completed runs")
                    body.send_keys(Keys.CONTROL, Keys.HOME)
                if name == "application-toolkit":
                    role_cards = driver.find_elements(By.CSS_SELECTOR, ".application-role-card")
                    downloads = driver.find_elements(By.CSS_SELECTOR, ".application-role-actions a[download]")
                    if len(role_cards) != 2 or len(downloads) != 2:
                        failures.append(f"{name}/{viewport}: expected two role cards and downloads")
                    for link in downloads:
                        relative_resume = link.get_attribute("href")
                        if not relative_resume or not relative_resume.endswith(".txt"):
                            failures.append(f"{name}/{viewport}: missing real text resume link")
                if name == "recruiter-profile" and viewport == "desktop":
                    # A profile is not itself an ATS text résumé; follow the actual choice.
                    download_choice = driver.find_element(By.CSS_SELECTOR, '.recruiter-actions a[href="apply.html"]')
                    if "Choose ATS résumé" not in download_choice.text:
                        failures.append("recruiter/profile: résumé choice is labeled as an immediate download")
                    click_control(download_choice)
                    if not driver.current_url.endswith("/apply.html") or len(
                            driver.find_elements(By.CSS_SELECTOR, ".application-role-actions a[download]")) != 2:
                        failures.append("recruiter/profile: choice does not reach both résumé downloads")
                    driver.get(url)
                    body = driver.find_element(By.TAG_NAME, "body")
                if name == "home":
                    replay = driver.find_element(By.ID, "boundary-replay")
                    replay_buttons = replay.find_elements(By.CSS_SELECTOR, "[data-replay-window]")
                    if len(replay_buttons) != 2 or any(b.get_attribute("disabled") is not None for b in replay_buttons):
                        failures.append(f"{name}/{viewport}: replay did not initialize from source fixtures")
                    if len(replay.find_elements(By.CSS_SELECTOR, "[data-replay-username]")) != 5:
                        failures.append(f"{name}/{viewport}: frozen reference rows missing")
                    for seconds, expected_count, expected_missing in ((599, "3 / 5", 2), (600, "5 / 5", 0)):
                        click_control(replay.find_element(By.CSS_SELECTOR, f'[data-replay-window="{seconds}"]'))
                        actual_count = replay.find_element(By.ID, "home-replay-count").text.strip()
                        missing_count = len(replay.find_elements(By.CSS_SELECTOR, '[data-replay-status="missing"]'))
                        if actual_count != expected_count or missing_count != expected_missing:
                            failures.append(f"{name}/{viewport}: {seconds}s replay calculated {actual_count}, {missing_count} missing")
                        if replay.find_element(By.CSS_SELECTOR, f'[data-replay-window="{seconds}"]').get_attribute("aria-pressed") != "true":
                            failures.append(f"{name}/{viewport}: {seconds}s replay not announced as selected")
                    if viewport == "desktop":
                        # JS-free rendering must not pretend the training rule executed.
                        try:
                            driver.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": True})
                            driver.get(url)
                            replay = driver.find_element(By.ID, "boundary-replay")
                            if not all(btn.get_attribute("disabled") is not None for btn in replay.find_elements(By.CSS_SELECTOR, "[data-replay-window]")):
                                failures.append("home/no-js: replay controls should remain disabled")
                            if replay.find_element(By.ID, "home-replay-count").text.strip() != "— / 5":
                                failures.append("home/no-js: dynamic finding count must remain uncalculated")
                        finally:
                            driver.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": False})
                            driver.get(url)
                            body = driver.find_element(By.TAG_NAME, "body")
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
                    # Both concise evidence disclosures must expose their content by keyboard.
                    for selector, content_selector in (
                        (".result-details", ".splunk-evidence-table"),
                        (".evidence-details", ".evidence-table"),
                    ):
                        disclosure = driver.find_element(By.CSS_SELECTOR, selector)
                        summary = disclosure.find_element(By.TAG_NAME, "summary")
                        summary.send_keys(Keys.ENTER)
                        if disclosure.get_attribute("open") is None or not disclosure.find_element(By.CSS_SELECTOR, content_selector).is_displayed():
                            failures.append(f"{name}/{viewport}: {selector} failed to open by keyboard")
                        summary.send_keys(Keys.ENTER)
                        if disclosure.get_attribute("open") is not None:
                            failures.append(f"{name}/{viewport}: {selector} failed to close by keyboard")
                    # Restore the top after keyboard disclosure checks scroll the page.
                    body.send_keys(Keys.CONTROL, Keys.HOME)
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
                    if viewport == "desktop":
                        # Follow the real recruiter route across pages, not merely its href.
                        path_link = driver.find_element(By.CSS_SELECTOR, '.hiring-route[href="roles.html"]')
                        click_control(path_link)
                        # file:// navigation can complete asynchronously in a busy headless
                        # runner; inspect the destination after its own DOM has loaded.
                        try:
                            WebDriverWait(driver, 5).until(
                                lambda d: d.current_url.endswith("/roles.html")
                                and len(d.find_elements(By.CSS_SELECTOR, ".role-route-card")) == 3)
                        except Exception:
                            failures.append(
                                "home/recruiter: expected roles.html and 3 role cards; got "
                                f"{driver.current_url} with {len(driver.find_elements(By.CSS_SELECTOR, '.role-route-card'))} cards")
                        else:
                            soc = driver.find_element(By.CSS_SELECTOR, '.role-route-card[href="#soc-analyst"]')
                            click_control(soc)
                            if driver.execute_script("return location.hash") != "#soc-analyst":
                                failures.append("home/recruiter: SOC evidence anchor did not open")
                        driver.get(url)
                        body = driver.find_element(By.TAG_NAME, "body")
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
                # Preserve an actual top-of-page capture, not the scroll position
                # left behind by interaction tests (a prior review-artifact defect).
                driver.get(url)
                driver.execute_script("window.scrollTo({top:0,left:0,behavior:'instant'})")
                out = SCREENSHOTS / f"{name}-{viewport}.png"
                driver.save_screenshot(str(out))
                if viewport == "desktop" and name in {
                        "home", "explorer", "test-workbench", "evidence-review",
                        "recruiter-profile", "role-paths"}:
                    # Reviewer can inspect complete page hierarchy, not only the
                    # top viewport. This is still a raw Chrome screenshot.
                    metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
                    content_size = metrics.get("cssContentSize", metrics["contentSize"])
                    full = driver.execute_cdp_cmd("Page.captureScreenshot", {
                        "format": "png", "captureBeyondViewport": True,
                        "clip": {"x": 0, "y": 0,
                                 "width": min(1280, content_size["width"]),
                                 "height": min(12000, content_size["height"]),
                                 "scale": 1}})
                    (SCREENSHOTS / f"{name}-full-desktop.png").write_bytes(
                        base64.b64decode(full["data"]))
                if name == "recruiter-profile" and viewport == "desktop":
                    pdf_path = SCREENSHOTS / "recruiter-print.pdf"
                    try:
                        pdf = driver.execute_cdp_cmd("Page.printToPDF", {
                            "printBackground": True, "displayHeaderFooter": False,
                            "preferCSSPageSize": True})
                        pdf_path.write_bytes(base64.b64decode(pdf["data"]))
                        info = subprocess.run(
                            ["pdfinfo", str(pdf_path)], capture_output=True,
                            text=True, check=True, timeout=10)
                        match = re.search(r"^Pages:\\s+(\\d+)", info.stdout, re.M)
                        pages = int(match.group(1)) if match else None
                        print_review = {"status": "PASS" if pages == 1 else "FAIL",
                                        "pages": pages, "filename": "recruiter-print.pdf"}
                        if pages != 1:
                            failures.append(f"recruiter/print: expected one US-letter page, got {pages}")
                    except (OSError, ValueError, subprocess.SubprocessError, KeyError) as error:
                        print_review = {"status": "FAIL", "pages": None,
                                        "reason": type(error).__name__}
                        failures.append("recruiter/print: could not inspect generated PDF")
                results.append({"page": relative, "viewport": viewport, "requested_width": width,
                                "observed_width": dimensions["viewport"],
                                "observed_height": dimensions["viewportHeight"],
                                "scroll_width": dimensions["scrollWidth"],
                                "screenshot": out.relative_to(ROOT).as_posix()})

    report = {"schema": "portfolio.chrome-responsive-review.v1",
              "browser": "Google Chrome or Chromium headless",
              "motion_preference": "reduce",
              "pages": len(PAGES),
              "viewports_reviewed": len(results),
              "screenshots": results, "print_review": print_review, "failures": failures,
              "status": "PASS" if not failures else "FAIL",
              "limitations": "Checks keyboard nav and horizontal overflow; screenshots still need human visual review. Not a WCAG or screen-reader audit."}
    (SCREENSHOTS / "review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "viewports_reviewed": len(results),
                      "failures": failures, "screenshots": str(SCREENSHOTS)}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
