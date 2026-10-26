"""Chrome review of the current employer journey and master-derived public resume.

The unchanged lab engines have their own fixture and executable checks. This
review covers readable layouts, no-script links, image loading and menus.
"""
from __future__ import annotations

import base64
from io import BytesIO
import json
import re
from pathlib import Path
import shutil

from pypdf import PdfReader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "visual-review-screenshots"
CASES = ("ad-attack-chain", "authentication-detection", "windows-process-triage", "network-traffic-analysis",
         "vulnerability-remediation", "celestial-resonance", "research-ai-infrastructure",
         "certification-learning-engine", "detection-engineering", "splunk-siem-investigation",
         "network-intrusion-lab", "phishing-investigation", "identity-mfa-investigation",
         "soc-triage-automation", "e3-digital-forensics", "offensive-security-vm-labs",
         "kali-defender-visibility", "splunk-threat-hunting", "splunk-execution-workflow")
PAGES = {"home": "index.html", "choice": "explore.html", "role-paths": "roles.html", "evidence":"verify.html", "application":"apply.html", "recruiter":"recruiter.html", "workbench":"test-lab.html", "awards": "awards.html", "education":"education.html", "image-credits":"visual-credits.html",
         **{slug: f"projects/{slug}.html" for slug in CASES}}
VIEWPORTS = {"desktop": (1280, 1000), "mobile": (390, 844), "small-mobile": (320, 720)}


def main() -> None:
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    driver_exe = shutil.which("chromedriver")
    if not chrome or not driver_exe:
        raise SystemExit("Chrome/ChromeDriver missing; browser validation not performed")
    opts = webdriver.ChromeOptions()
    opts.binary_location = chrome
    for arg in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars",
                "--disable-background-networking", "--blink-settings=scriptEnabled=false"):
        opts.add_argument(arg)
    OUT.mkdir(exist_ok=True)
    failures, captures = [], []
    with webdriver.Chrome(service=Service(driver_exe), options=opts) as driver:
        driver.set_page_load_timeout(20)
        for name, relative in PAGES.items():
            for viewport, (width, height) in VIEWPORTS.items():
                driver.set_window_size(width, height)
                driver.get((ROOT / relative).resolve().as_uri())
                if not driver.find_element(By.CSS_SELECTOR, "main h1").is_displayed():
                    failures.append(f"{name}/{viewport}: heading hidden")
                dims = driver.execute_script("return {width:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}")
                if dims["scroll"] > dims["width"] + 1:
                    failures.append(f"{name}/{viewport}: horizontal overflow {dims}")
                if dims["width"] != width:
                    failures.append(f"{name}/{viewport}: expected {width}px viewport, got {dims['width']}")
                for image in driver.find_elements(By.CSS_SELECTOR, "img"):
                    loaded = driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth>0", image)
                    if not loaded:
                        # Force below-fold lazy images into the browser's load area.
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'})", image)
                        from selenium.webdriver.support.ui import WebDriverWait
                        WebDriverWait(driver, 5).until(lambda d: d.execute_script("return arguments[0].complete && arguments[0].naturalWidth>0", image))
                if width <= 390:
                    summary = driver.find_element(By.CSS_SELECTOR, ".mobile-nav summary")
                    summary.send_keys(Keys.ENTER)
                    menu = driver.find_element(By.CSS_SELECTOR, '.mobile-nav nav')
                    if not menu.is_displayed():
                        failures.append(f"{name}/{viewport}: keyboard menu failed")
                    for link in menu.find_elements(By.TAG_NAME, 'a'):
                        if not link.is_displayed():
                            failures.append(f"{name}/{viewport}: menu destination hidden")
                    summary.send_keys(Keys.ENTER)
                driver.execute_script("window.scrollTo({top:0,left:0,behavior:'instant'})")
                layout = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})["cssContentSize"]
                shot = driver.execute_cdp_cmd("Page.captureScreenshot", {"format":"png","captureBeyondViewport":True,
                       "clip":{"x":0,"y":0,"width":width,"height":layout["height"],"scale":1}})
                path = OUT / f"{name}-{viewport}.png"
                path.write_bytes(base64.b64decode(shot["data"]))
                captures.append({"page":relative,"viewport":viewport,"screenshot":path.name})
        # Each skill must lead directly to its supporting case without scripts.
        driver.set_window_size(1280,1000)
        for relative in ('projects/detection-engineering.html','projects/ad-attack-chain.html','projects/network-traffic-analysis.html','projects/splunk-execution-workflow.html'):
            driver.get((ROOT/'index.html').resolve().as_uri())
            skill = driver.find_element(By.CSS_SELECTOR, f'#skills a[href="{relative}"]')
            driver.execute_script("arguments[0].scrollIntoView({behavior:'instant',block:'center'})",skill)
            skill.click()
            if not driver.current_url.endswith('/'+relative) or not driver.find_element(By.CSS_SELECTOR,'main h1').is_displayed():
                failures.append('Skill evidence destination unavailable: '+relative)
        for relative in ('roles.html','verify.html','apply.html','recruiter.html','test-lab.html'):
            driver.get((ROOT/relative).resolve().as_uri())
            current = driver.find_elements(By.CSS_SELECTOR,'.employer-nav a[aria-current="page"]')
            if len(current)!=1 or not current[0].get_attribute('href').endswith('/'+relative):
                failures.append('Employer navigation current-page mismatch: '+relative)
        # Follow the strongest case, then the full directory, without JavaScript.
        driver.get((ROOT/'index.html').resolve().as_uri())
        driver.find_element(By.CSS_SELECTOR,'.actions .button').click()
        if not driver.current_url.endswith('/projects/ad-attack-chain.html'):
            failures.append('Primary employer action did not open the AD investigation')
        driver.get((ROOT/'index.html').resolve().as_uri())
        all_work = driver.find_element(By.CSS_SELECTOR, '.more-investigations a[href="explore.html"]')
        # Finish scrolling before the native click; CSS smooth scrolling can leave
        # Selenium's automatically scrolled target outside the viewport.
        driver.execute_script("arguments[0].scrollIntoView({behavior:'instant',block:'center'})", all_work)
        all_work.click()
        if not driver.current_url.endswith('/explore.html'):
            failures.append('All-work action did not open the choice page')
        for slug in CASES:
            links = driver.find_elements(By.CSS_SELECTOR,f'a[href="projects/{slug}.html"]')
            if not links or not any(link.is_displayed() for link in links):
                failures.append('Case choice unavailable without scripts: '+slug)
        # PDF source is independent of browser print and must preserve the master content.
        pdf = PdfReader(ROOT/'resumes/Don_Lopez_Cybersecurity_Resume.pdf')
        content = '\n'.join(page.extract_text() for page in pdf.pages)
        if len(pdf.pages)!=1:
            failures.append('Public resume is not one page')
        for term in ('Don Lopez','Allied Universal','Security Officer','CySA+','SCCDA','Planned','5+','30%','5,000+'):
            if term not in content:
                failures.append('Public resume missing master content: '+term)
        if 'Brandon' in content or '(760)' in content:
            failures.append('Private master identity or phone exposed in public resume')
        driver.get((ROOT/'recruiter.html').resolve().as_uri())
        printed=driver.execute_cdp_cmd('Page.printToPDF',{'printBackground':True,'preferCSSPageSize':True})
        printed_bytes=base64.b64decode(printed['data'])
        (OUT/'recruiter-print.pdf').write_bytes(printed_bytes)
        profile=PdfReader(BytesIO(printed_bytes))
        profile_text='\n'.join(page.extract_text() for page in profile.pages)
        if len(profile.pages)!=1:
            failures.append('Recruiter profile print is not one page')
        for term in ('Don Lopez','Allied Universal','CySA+','25,993'):
            if term not in profile_text:
                failures.append('Recruiter print missing content: '+term)
        if not re.search(r'5\s*/\s*5',profile_text):
            failures.append('Recruiter print missing five-of-five result')
    # Technical playback and inspector behavior live in test_technical_workbenches_browser.py.
    summary = {"status":"PASS" if not failures else "FAIL","captures":captures,
               "interactive_review":"covered by separate technical workbench browser check",
               "javascript":"disabled for employer navigation review","failures":failures}
    (OUT/'review-summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps({"status":summary['status'],"captures":len(captures),"failures":failures},indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
