"""Chrome review of the current employer journey and master-derived public resume.

The unchanged lab engines have their own fixture and executable checks. This
review covers readable layouts, no-script links, image loading and menus.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
import shutil

from pypdf import PdfReader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "visual-review-screenshots"
CASES = ("authentication-detection", "windows-process-triage", "network-traffic-analysis",
         "vulnerability-remediation", "celestial-resonance", "research-ai-infrastructure",
         "certification-learning-engine", "detection-engineering", "splunk-siem-investigation",
         "network-intrusion-lab", "phishing-investigation", "identity-mfa-investigation",
         "soc-triage-automation", "e3-digital-forensics", "kali-defender-visibility", "splunk-threat-hunting")
PAGES = {"home": "index.html", "choice": "explore.html", "role-paths": "roles.html", "awards": "awards.html", "education":"education.html", "image-credits":"visual-credits.html",
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
                driver.execute_script("window.scrollTo(0,0)")
                layout = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})["cssContentSize"]
                shot = driver.execute_cdp_cmd("Page.captureScreenshot", {"format":"png","captureBeyondViewport":True,
                       "clip":{"x":0,"y":0,"width":width,"height":layout["height"],"scale":1}})
                path = OUT / f"{name}-{viewport}.png"
                path.write_bytes(base64.b64decode(shot["data"]))
                captures.append({"page":relative,"viewport":viewport,"screenshot":path.name})
        # Follow the actual employer choice action with page JavaScript disabled.
        driver.set_window_size(1280,1000)
        driver.get((ROOT/'index.html').resolve().as_uri())
        driver.find_element(By.CSS_SELECTOR,'.actions .button').click()
        if not driver.current_url.endswith('/explore.html'):
            failures.append('Primary employer action did not open the choice page')
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
    # The new explainers must also work with JavaScript enabled. Use the real
    # controls, including keyboard input, and force reduced motion before load.
    from selenium.webdriver.support.ui import Select, WebDriverWait
    enabled = webdriver.ChromeOptions()
    enabled.binary_location = chrome
    for arg in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"):
        enabled.add_argument(arg)
    with webdriver.Chrome(service=Service(driver_exe), options=enabled) as driver:
        driver.execute_cdp_cmd('Emulation.setEmulatedMedia', {'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
        for width,height in VIEWPORTS.values():
            driver.set_window_size(width,height)
            driver.get((ROOT/'projects/celestial-resonance.html').resolve().as_uri())
            panel = driver.find_element(By.CSS_SELECTOR,'[data-system-demo="cr"]')
            revision = panel.find_element(By.CSS_SELECTOR,'[data-cr-revision]')
            revision.send_keys(Keys.SPACE)
            assert 'Hold:' in panel.find_element(By.CSS_SELECTOR,'[data-demo-status]').text
            Select(panel.find_element(By.CSS_SELECTOR,'[data-cr-date]')).select_by_value('2026-03-20')
            assert 'Eligible' in panel.find_element(By.CSS_SELECTOR,'[data-demo-status]').text
            panel.find_element(By.CSS_SELECTOR,'[data-cr-play]').click()
            assert driver.execute_script("return document.querySelectorAll('[data-cr-stage]')[1].dataset.state") == 'current'
            panel.find_element(By.CSS_SELECTOR,'[data-cr-step]').click()
            assert driver.execute_script("return document.querySelectorAll('[data-cr-stage]')[2].dataset.state") == 'current'
            panel.find_element(By.CSS_SELECTOR,'[data-cr-reset]').click()
            assert driver.execute_script("return document.querySelectorAll('[data-cr-stage]')[0].dataset.state") == 'current'
            assert driver.execute_script("return getComputedStyle(document.querySelector('[data-cr-token]')).transitionDuration") == '0s'
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})",panel)
            filename=f'cr-demo-enabled-{width}.png'; driver.save_screenshot(str(OUT/filename))
            captures.append({'page':'projects/celestial-resonance.html','viewport':str(width),'screenshot':filename})
            driver.get((ROOT/'projects/research-ai-infrastructure.html').resolve().as_uri())
            panel = driver.find_element(By.CSS_SELECTOR,'[data-system-demo="rai"]')
            status = panel.find_element(By.CSS_SELECTOR,'[data-demo-status]')
            assert 'Conflict:' in status.text
            Select(panel.find_element(By.CSS_SELECTOR,'[data-rai-observation]')).select_by_value('tightening')
            assert 'Supported' in status.text
            include = panel.find_element(By.CSS_SELECTOR,'[data-rai-include]'); include.click()
            assert 'source is missing' in status.text
            include.click(); panel.find_element(By.CSS_SELECTOR,'[data-rai-attribution]').click()
            assert 'attribution does not match' in status.text
            panel.find_element(By.CSS_SELECTOR,'[data-rai-trace]').click()
            assert panel.get_attribute('data-trace-stage') == '2'
            panel.find_element(By.CSS_SELECTOR,'[data-rai-reset]').click()
            assert 'Conflict:' in status.text
            dims=driver.execute_script('return [document.documentElement.clientWidth,document.documentElement.scrollWidth]')
            assert dims[1] <= dims[0]+1
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})",panel)
            filename=f'rai-demo-enabled-{width}.png'; driver.save_screenshot(str(OUT/filename))
            captures.append({'page':'projects/research-ai-infrastructure.html','viewport':str(width),'screenshot':filename})
        # Normal-motion controls must run, pause and reset, not just jump states.
        driver.execute_cdp_cmd('Emulation.setEmulatedMedia', {'features':[{'name':'prefers-reduced-motion','value':'no-preference'}]})
        driver.get((ROOT/'projects/celestial-resonance.html').resolve().as_uri())
        play=driver.find_element(By.CSS_SELECTOR,'[data-cr-play]')
        driver.execute_script("arguments[0].scrollIntoView({block:'center',behavior:'instant'})",play)
        play.click()
        assert play.text == 'Pause'
        WebDriverWait(driver,4).until(lambda d: d.execute_script("return document.querySelectorAll('[data-cr-stage]')[2].dataset.state") == 'current')
        play.click(); assert play.text == 'Play'
        driver.find_element(By.CSS_SELECTOR,'[data-cr-reset]').click()
        assert driver.execute_script("return document.querySelectorAll('[data-cr-stage]')[0].dataset.state") == 'current'
        play.click()
        driver.execute_script("window.scrollTo({top:0,behavior:'instant'})")
        WebDriverWait(driver,3).until(lambda d: play.text == 'Play')
        # Decorative homepage animation: one profile link each, progressive
        # controls, normal pause/resume, offscreen pause and reduced-motion stop.
        driver.set_window_size(1280,1000)
        driver.get((ROOT/'index.html').resolve().as_uri())
        display=driver.find_element(By.CSS_SELECTOR,'[data-signal-display]')
        WebDriverWait(driver,3).until(lambda d: display.get_attribute('data-running') == 'true')
        toggle=display.find_element(By.TAG_NAME,'button'); toggle.click()
        assert display.get_attribute('data-running') == 'false'
        toggle.click(); assert display.get_attribute('data-running') == 'true'
        driver.execute_script("window.scrollTo({top:document.body.scrollHeight,behavior:'instant'})")
        WebDriverWait(driver,3).until(lambda d: display.get_attribute('data-running') == 'false')
        driver.execute_script("window.scrollTo({top:0,behavior:'instant'})")
        driver.execute_cdp_cmd('Emulation.setEmulatedMedia', {'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
        WebDriverWait(driver,3).until(lambda d: display.get_attribute('data-running') == 'false')
        # The panel may already be paused offscreen before the media-change
        # callback runs; wait for that callback's visible control update too.
        WebDriverWait(driver,3).until(lambda d: not toggle.is_displayed())
        assert len(driver.find_elements(By.CSS_SELECTOR,'a[href="https://github.com/IXI-2773"]')) == 1
        assert len(driver.find_elements(By.CSS_SELECTOR,'a[href="https://www.linkedin.com/in/ixi2773/"]')) == 1
    summary = {"status":"PASS" if not failures else "FAIL","captures":captures,
               "interactive_review":"CR/RAI controls, keyboard, normal and reduced motion passed",
               "javascript":"disabled for employer navigation review","failures":failures}
    (OUT/'review-summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps({"status":summary['status'],"captures":len(captures),"failures":failures},indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
