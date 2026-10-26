"""Bounded Chrome verification of the technical portfolio routes."""
import base64
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
ROUTES=['index.html','projects/detection-engineering.html','projects/celestial-resonance.html','projects/research-ai-infrastructure.html','projects/ad-attack-chain.html']
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
        def click(css):
            target=el(css)
            d.execute_script('arguments[0].scrollIntoView({block:"center",behavior:"instant"})',target)
            wait.until(lambda _:d.execute_script('const r=arguments[0].getBoundingClientRect();return r.top>=0 && r.bottom<=innerHeight',target))
            target.click()
        def capture_panel(panel,name):
            d.execute_script('window.scrollTo({top:0,left:0,behavior:"instant"})')
            box=d.execute_script('const r=arguments[0].getBoundingClientRect();return {x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height,scale:1}',panel)
            shot=d.execute_cdp_cmd('Page.captureScreenshot',{'format':'png','captureBeyondViewport':True,'clip':box})
            (OUT/name).write_bytes(base64.b64decode(shot['data']))

        def open_page(path):
            d.get((ROOT/path).as_uri())
            if 'ad-attack-chain' in path:wait.until(lambda _:len(d.find_elements(By.CSS_SELECTOR,'[data-ad-record]'))>0)
            elif 'detection-engineering' in path:wait.until(lambda _:len(d.find_elements(By.CSS_SELECTOR,'[data-event-index]'))>0)
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
                if 'ad-attack-chain' in path:
                    label_height=d.execute_script('return document.querySelector("[data-ad-timeline] .chart-note").getBoundingClientRect().height')
                    assert label_height>=10,(path,width,'timeline labels below readable rendered size',label_height)
                    if width<=390:
                        chart=el('.ad-chart-scroll')
                        assert chart.get_attribute('tabindex')=='0'
                        assert d.execute_script('return arguments[0].scrollWidth>arguments[0].clientWidth',chart),'Timeline must retain readable width inside its scroll region'
                for image in d.find_elements(By.CSS_SELECTOR,'img'):
                    d.execute_script('arguments[0].scrollIntoView({block:"center"})',image)
                    wait.until(lambda _:d.execute_script('return arguments[0].complete && arguments[0].naturalWidth>0',image))
                if width<=390:
                    for select in d.find_elements(By.CSS_SELECTOR,'.technical-workbench .workbench-toolbar select'):
                        panel=select.find_element(By.XPATH,'ancestor::section[1]')
                        assert select.rect['width']>=panel.rect['width']-50,(path,width,'selector too narrow')
                if width in [1280,390]:
                    d.execute_script('window.scrollTo(0,0)')
                    d.save_screenshot(str(OUT/(Path(path).stem+f'-technical-{width}.png')))
                    panels=d.find_elements(By.CSS_SELECTOR,'.technical-workbench')
                    if panels:capture_panel(panels[0],Path(path).stem+f'-inspector-{width}.png')
                    if path=='index.html':capture_panel(el('[data-signal-display]'),f'signal-film-{width}.png')
                checks.append(f'{path}/{width}: images, no overflow, no JS errors')
        d.set_window_size(1280,1100)
        d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',{'width':1280,'height':950,'deviceScaleFactor':1,'mobile':False})
        open_page('projects/detection-engineering.html')
        b=el('[data-event-index="5"]');b.send_keys(Keys.ENTER)
        assert 'login_success' in el('[data-auth-inspector]').text
        assert d.execute_script('return document.activeElement.dataset.eventIndex')=='5','Event selection must retain keyboard focus'
        assert '5 qualifying failures' in el('[data-auth-outcome]').text
        Select(el('[data-auth-scenario]')).select_by_value('post_success_burst')
        early=d.find_elements(By.CSS_SELECTOR,'[data-event-index]')[3];early.send_keys(Keys.ENTER)
        assert 'Rule not triggered' in el('[data-auth-outcome]').text
        assert 'auth-022' in el('[data-auth-inspector]').text
        Select(el('[data-auth-scenario]')).select_by_value('below')
        assert 'Rule not triggered' in el('[data-auth-outcome]').text
        click('[data-replay-play]');wait.until(lambda _:el('[data-detection-lab]').get_attribute('data-running')=='true')
        d.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        wait.until(lambda _:el('[data-detection-lab]').get_attribute('data-running')=='false')
        d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
        open_page('projects/detection-engineering.html');click('[data-replay-play]')
        assert el('[data-detection-lab]').get_attribute('data-running')=='false'
        assert el('[data-event-index="1"]').get_attribute('aria-pressed')=='true'
        d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[]})
        open_page('projects/celestial-resonance.html')
        Select(el('[data-vintage-cutoff]')).select_by_value('2026-03-20T00:00:00Z')
        assert 'release-v2' in el('[data-vintage-outcome]').text
        Select(el('[data-vintage-mode]')).select_by_value('ambiguous')
        assert 'Hold: conflicting' in el('[data-vintage-outcome]').text
        el('[data-record-id="release-v2"]').send_keys(Keys.ENTER)
        assert d.execute_script('return document.activeElement.dataset.recordId')=='release-v2'
        capture_panel(el('[data-vintage-workbench]'),'cr-held-inspector.png')
        open_page('projects/research-ai-infrastructure.html')
        el('[data-passage-id="B:p1"]').send_keys(Keys.ENTER)
        assert 'mortgage' in el('[data-claim-inspector]').text
        assert d.execute_script('return document.activeElement.dataset.passageId')=='B:p1','Passage selection must retain focus'
        assert 'Not directly comparable' in el('[data-claim-outcome]').text
        Select(el('[data-claim-scenario]')).select_by_value('attribution')
        assert 'attribution mismatch' in el('[data-claim-outcome]').text
        capture_panel(el('[data-claim-workbench]'),'rai-attribution-inspector.png')
        open_page('index.html')
        assert not d.find_elements(By.CSS_SELECTOR,'.intro-content a[href="projects/ad-attack-chain.html"]')
        assert el('.actions a[download]').get_attribute('href').endswith('/resumes/Don_Lopez_Cybersecurity_Resume.pdf')
        assert el('[data-signal-display]').get_attribute('data-visual')=='film'
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-film-running')=='true')
        d.execute_async_script('const done=arguments[0];setTimeout(done,5100)')
        assert el('[data-signal-display]').get_attribute('data-film-running')=='true','GIF must keep running past one cycle'
        assert el('[data-signal-film]').get_attribute('src').endswith('signal-to-case.gif')
        click('[data-film-play]')
        assert el('[data-signal-film]').get_attribute('src').endswith('signal-to-case-still.png')
        d.execute_script('window.scrollTo({top:document.body.scrollHeight,behavior:"instant"})')
        d.execute_async_script('const done=arguments[0];requestAnimationFrame(()=>requestAnimationFrame(done))')
        d.execute_script('window.scrollTo({top:0,behavior:"instant"})')
        d.execute_async_script('const done=arguments[0];requestAnimationFrame(()=>requestAnimationFrame(done))')
        assert el('[data-signal-display]').get_attribute('data-film-running')=='false','Manual stop must persist'
        click('[data-film-play]')
        assert el('[data-signal-display]').get_attribute('data-film-running')=='true'
        click('.signal-inspection > summary')
        click('[data-signal-detail] summary')
        click('[data-signal-event]')
        assert el('[data-signal-display]').get_attribute('data-visual')=='events'
        assert el('[data-signal-display]').get_attribute('data-film-running')=='false'
        click('[data-film-play]')
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-film-running')=='true')
        assert el('[data-signal-display]').get_attribute('data-visual')=='film'
        click('[data-signal-step]')
        assert el('[data-signal-display]').get_attribute('data-visual')=='events'
        assert el('[data-signal-display]').get_attribute('data-film-running')=='false'
        click('[data-signal-detail] summary')
        click('[data-signal-event]')
        assert el('[data-signal-detail] details').get_attribute('open') is not None
        assert el('[data-signal-event-inspector]').is_displayed()
        Select(el('[data-signal-scenario]')).select_by_value('below')
        assert not el('.signal-film-caption span').is_displayed()
        click('[data-film-play]')
        assert el('[data-signal-display]').get_attribute('data-visual')=='film'
        assert el('[data-signal-display]').get_attribute('data-running')=='false'
        assert Select(el('[data-signal-scenario]')).first_selected_option.get_attribute('value')=='ten_minute_boundary'
        assert '6 timestamped events' in el('[data-signal-detail]').text
        d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
        wait.until(lambda _:el('[data-film-play]').get_attribute('disabled'))
        assert d.execute_script('return arguments[0].currentSrc',el('[data-signal-film]')).endswith('signal-to-case-still.png')
        d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[]})
        wait.until(lambda _:not el('[data-film-play]').get_attribute('disabled'))
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-film-running')=='true')
        d.execute_script('window.scrollTo({top:document.body.scrollHeight,behavior:"instant"})')
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-film-running')=='false')
        d.execute_script('window.scrollTo({top:0,behavior:"instant"})')
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-film-running')=='true')
        d.execute_script("window.filmVisibility=[];document.addEventListener('visibilitychange',()=>window.filmVisibility.push({hidden:document.hidden,running:document.querySelector('[data-signal-display]').dataset.filmRunning}))")
        old=d.current_window_handle;d.switch_to.new_window('tab');d.switch_to.window(old)
        wait.until(lambda _:d.execute_script("return window.filmVisibility.some(s=>s.hidden&&s.running==='false') && window.filmVisibility.some(s=>!s.hidden&&s.running==='true')"))
        d.switch_to.window(d.window_handles[-1]);d.close();d.switch_to.window(old)
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-film-running')=='true')
        checks.append('looping GIF past one cycle, persistent manual stop, inspector handoff, hidden/offscreen pause/resume and reduced-motion poster passed')
        open_page('index.html');click('.signal-inspection > summary');click('[data-signal-play]')
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-running')=='true')
        old=d.current_window_handle;d.switch_to.new_window('tab');d.switch_to.window(old)
        wait.until(lambda _:el('[data-signal-display]').get_attribute('data-running')=='false')
        open_page('projects/ad-attack-chain.html')
        click('[data-ad-phase="3"]')
        Select(el('[data-ad-target]')).select_by_value('mordordc.theshire.local')
        assert 'H24051' in el('[data-ad-inspector]').text
        assert '39.812' in el('[data-ad-inspector]').text
        before=el('[data-ad-point="5"]').get_attribute('style')
        Select(el('[data-ad-clock]')).select_by_value('collection_time')
        assert before!=el('[data-ad-point="5"]').get_attribute('style'),'Clock change must move DC dot'
        assert 'Collection time' in el('[data-ad-clock-label]').text
        click('[data-ad-record="H23781"]')
        assert d.execute_script('return document.activeElement.dataset.adRecord')=='H23781'
        assert 'fddc55f3-4305' in el('[data-ad-inspector]').text
        click('[data-ad-record="P00843"]')
        assert '58215' in el('[data-ad-inspector]').text
        assert 'POST /wsman' in el('[data-ad-inspector]').text
        Select(el('[data-ad-view]')).select_by_value('controls')
        assert len(d.find_elements(By.CSS_SELECTOR,'[data-ad-record]'))==12
        assert '12 nonmatching' in el('[data-ad-outcome]').text
        click('[data-ad-record]')
        assert 'Security 4769' in el('[data-ad-inspector]').text
        capture_panel(el('[data-ad-case]'),'ad-controls-inspector.png')
        click('[data-ad-reset]')
        click('[data-ad-play]')
        wait.until(lambda _:el('[data-ad-case]').get_attribute('data-running')=='true')
        d.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        wait.until(lambda _:el('[data-ad-case]').get_attribute('data-running')=='false')
        d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
        open_page('projects/ad-attack-chain.html');click('[data-ad-play]')
        assert el('[data-ad-case]').get_attribute('data-running')=='false'
        assert el('[data-ad-phase="1"]').get_attribute('aria-pressed')=='true'
        checks.append('AD source selection, target session, two clocks, PCAP tuple, negative controls, offscreen pause and reduced motion passed')
        checks.append('keyboard, selected evidence, scope/attribution, hidden/offscreen pause, reduced motion passed')
        d.execute_cdp_cmd('Emulation.setEmulatedMedia',{'features':[]})
        d.get((ROOT/'test-lab.html').as_uri())
        wait.until(lambda _:el('#run-checks').is_enabled())
        click('#run-checks')
        assert '9 / 9 checks passed' in el('#checks-status').text
        assert el('#download-run').is_enabled()
        click('[data-window-preset="599"]')
        assert '2 baseline rows missing' in el('#replay-status').text
        click('[data-window-preset="600"]')
        assert '0 baseline rows missing' in el('#replay-status').text
        Select(el('#coverage-case')).select_by_value('omitted')
        click('#coverage-submit')
        assert el('#coverage-status').get_attribute('data-result')=='hold'
        checks.append('restyled public workbench: nine baseline checks, window boundary, receipt availability and evidence hold passed')
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
            if 'ad-attack-chain' in path:assert 'both clocks' in el('[data-ad-inspector]').text
            if path=='index.html':
                assert el('[data-signal-film]').get_attribute('src').endswith('signal-to-case-still.png')
                assert not el('[data-film-play]').is_displayed()
        checks.append('no-JavaScript representative explanations, image, and source links retained')
    (OUT/'technical-review.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2))
    print('PASS:',len(checks),'technical browser check groups')
if __name__=='__main__':main()
