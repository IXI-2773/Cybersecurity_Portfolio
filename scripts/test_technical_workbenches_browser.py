"""Bounded Chrome verification of the four technical portfolio routes."""
import json
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'visual-review-screenshots'
ROUTES=['index.html','projects/detection-engineering.html','projects/celestial-resonance.html','projects/research-ai-infrastructure.html']
def main():
    opts=Options()
    binary=shutil.which('google-chrome') or shutil.which('chromium')
    if binary:opts.binary_location=binary
    for flag in ['--headless=new','--no-sandbox','--disable-dev-shm-usage','--disable-background-networking']:opts.add_argument(flag)
    opts.set_capability('goog:loggingPrefs',{'browser':'ALL'})
    OUT.mkdir(exist_ok=True)
    checks=[]
    with webdriver.Chrome(options=opts) as d:
        wait=WebDriverWait(d,8)
        def el(css):return d.find_element(By.CSS_SELECTOR,css)
        def open_page(path):
            d.get((ROOT/path).as_uri())
            if 'detection-engineering' in path:wait.until(lambda _:len(d.find_elements(By.CSS_SELECTOR,'[data-event-index]'))>0)
            elif 'celestial-resonance' in path:wait.until(lambda _:'release-v1' in el('[data-vintage-outcome]').text)
            elif 'research-ai' in path:wait.until(lambda _:len(d.find_elements(By.CSS_SELECTOR,'[data-passage-id]'))>0)
            else:wait.until(lambda _:'auth-052' in el('[data-signal-detail]').get_attribute('innerHTML') or len(d.find_elements(By.CSS_SELECTOR,'.signal-data-dot'))>0)
            errors=[x for x in d.get_log('browser') if x['level']=='SEVERE' and 'favicon' not in x['message']]
            assert not errors,errors
        for width in [1280,390,320]:
            d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':width,'height':950,'deviceScaleFactor':1,'mobile':False})
            for path in ROUTES:
                open_page(path)
                assert d.execute_script('return document.documentElement.scrollWidth <= innerWidth + 1'),(path,width,'overflow')
                for image in d.find_elements(By.CSS_SELECTOR,'img'):
                    d.execute_script('arguments[0].scrollIntoView({block:"center"})',image)
                    wait.until(lambda _:d.execute_script('return arguments[0].complete && arguments[0].naturalWidth>0',image))
                if width in [1280,390]:
                    d.execute_script('window.scrollTo(0,0)')
                    d.save_screenshot(str(OUT/(Path(path).stem+f'-technical-{width}.png')))
                    panels=d.find_elements(By.CSS_SELECTOR,'.technical-workbench')
                    if panels:panels[0].screenshot(str(OUT/(Path(path).stem+f'-inspector-{width}.png')))
                checks.append(f'{path}/{width}: images, no overflow, no JS errors')
        d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':1280,'height':950,'deviceScaleFactor':1,'mobile':False})
        open_page('projects/detection-engineering.html')
        b=el('[data-event-index="5"]');b.send_keys(Keys.ENTER)
        assert 'login_success' in el('[data-auth-inspector]').text
        assert d.execute_script('return document.activeElement.dataset.eventIndex')=='5','Event selection must retain keyboard focus'
        assert '5 qualifying failures' in el('[data-auth-outcome]').text
        Select(el('[data-auth-scenario]')).select_by_value('below')
        assert 'Rule not triggered' in el('[data-auth-outcome]').text
        el('[data-replay-play]').click();wait.until(lambda _:el('[data-detection-lab]').get_attribute('data-running')=='true')
        d.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        wait.until(lambda _:el('[data-detection-lab]').get_attribute('data-running')=='false')
        d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
        open_page('projects/detection-engineering.html');el('[data-replay-play]').click()
        assert el('[data-detection-lab]').get_attribute('data-running')=='false'
        assert el('[data-event-index="1"]').get_attribute('aria-pressed')=='true'
        d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[]})
        open_page('projects/celestial-resonance.html')
        Select(el('[data-vintage-cutoff]')).select_by_value('2026-03-20T00:00:00Z')
        assert 'release-v2' in el('[data-vintage-outcome]').text
        Select(el('[data-vintage-mode]')).select_by_value('ambiguous')
        assert 'Hold: conflicting' in el('[data-vintage-outcome]').text
        el('[data-vintage-workbench]').screenshot(str(OUT/'cr-held-inspector.png'))
        open_page('projects/research-ai-infrastructure.html')
        el('[data-passage-id="B:p1"]').send_keys(Keys.ENTER)
        assert 'mortgage' in el('[data-claim-inspector]').text
        assert d.execute_script('return document.activeElement.dataset.passageId')=='B:p1','Passage selection must retain focus'
        assert 'Not directly comparable' in el('[data-claim-outcome]').text
        Select(el('[data-claim-scenario]')).select_by_value('attribution')
        assert 'attribution mismatch' in el('[data-claim-outcome]').text
        el('[data-claim-workbench]').screenshot(str(OUT/'rai-attribution-inspector.png'))
        open_page('index.html');el('[data-signal-play]').click()
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-running')=='true')
        old=d.current_window_handle;d.switch_to.new_window('tab');d.switch_to.window(old)
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-running')=='false')
        checks.append('keyboard, selected evidence, scope/attribution, hidden/offscreen pause, reduced motion passed')
        d.execute_cdp_cmd('Emulation.setScriptExecutionDisabled',{'value':True})
        for path in ROUTES:
            d.get((ROOT/path).as_uri())
            assert el('h1').is_displayed()
            assert d.find_elements(By.CSS_SELECTOR,'a[href]')
            if 'detection-engineering' in path:
                assert el('.genuine-capture img').is_displayed()
                assert '600 seconds' in el('[data-auth-inspector]').text
            if 'celestial-resonance' in path:assert 'release-v1' in el('[data-vintage-outcome]').text
            if 'research-ai' in path:assert 'Not directly comparable' in el('[data-claim-outcome]').text
        checks.append('no-JavaScript representative explanations, image, and source links retained')
    (OUT/'technical-review.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2))
    print('PASS:',len(checks),'technical browser check groups')
if __name__=='__main__':main()
