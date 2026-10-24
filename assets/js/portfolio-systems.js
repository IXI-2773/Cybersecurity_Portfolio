/* Independent, fictional-data explainers. No private CR/RAI execution or IO. */
(function (root) {
  'use strict';
  function validDate(value) {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
    const parsed = new Date(value + 'T00:00:00Z');
    return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
  }
  function evaluateCR({asOf, revision} = {}) {
    const available = revision === true ? '2026-03-20' : '2026-03-04';
    const value = revision === true ? '2.7' : '2.4';
    const eligible = validDate(asOf) && typeof revision === 'boolean' && asOf >= available;
    return {eligible, value, available, state: eligible ? 'eligible' : 'hold'};
  }
  function evaluateRAI({includeB, attributionValid, agrees} = {}) {
    if (includeB !== true) return {state:'missing', title:'Hold: a source is missing', detail:'Source B belongs to this two-record example. Leaving it out does not establish agreement.'};
    if (attributionValid !== true) return {state:'attribution', title:'Hold: attribution does not match', detail:'The cited source and recorded observation disagree. Correct the attribution before assessing the claim.'};
    if (agrees !== true) return {state:'conflict', title:'Conflict: preserve both observations', detail:'Source A suggests tightening; source B suggests easing. Report the disagreement rather than claiming consensus.'};
    return {state:'supported', title:'Supported within this example', detail:'Both cited records indicate tightening. Coverage and attribution pass; the real-world truth of either source has not been assessed.'};
  }
  const api = {evaluateCR, evaluateRAI};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.PortfolioSystems = api;
  if (typeof document === 'undefined') return;

  const reduce = root.matchMedia('(prefers-reduced-motion: reduce)');
  const initializers = {cr: initCR, rai: initRAI};
  document.querySelectorAll('[data-system-demo]').forEach(panel => {
    const initialize = initializers[panel.dataset.systemDemo];
    if (initialize) initialize(panel);
  });
  function onPause(panel, pause) {
    document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });
    if (reduce.addEventListener) reduce.addEventListener('change', () => { if (reduce.matches) pause(); });
    if ('IntersectionObserver' in root) {
      new IntersectionObserver(entries => { if (!entries[0].isIntersecting) pause(); }).observe(panel);
    }
  }
  function initCR(panel) {
    const date = panel.querySelector('[data-cr-date]');
    const revision = panel.querySelector('[data-cr-revision]');
    const play = panel.querySelector('[data-cr-play]');
    const next = panel.querySelector('[data-cr-step]');
    const status = panel.querySelector('[data-demo-status]');
    const steps = [...panel.querySelectorAll('[data-cr-stage]')];
    const captions = [
      'Read the source record and its release date.',
      'Preserve this exact version rather than overwriting earlier evidence.',
      'Check that the record was available by the research date.',
      'Carry the admitted version into a comparable research dataset.',
      'Record the research decision and keep the input traceable. No forecast is calculated.'
    ];
    let step = 0, timer = null;
    const result = () => evaluateCR({asOf:date.value, revision:revision.checked});
    function pause() { if (timer !== null) root.clearInterval(timer); timer = null; play.textContent = 'Play'; play.setAttribute('aria-pressed','false'); }
    function render() {
      const r = result(), last = r.eligible ? 4 : 2;
      panel.dataset.result = r.state;
      panel.querySelector('[data-cr-value]').textContent = r.value;
      panel.querySelector('[data-cr-release]').textContent = r.available;
      status.textContent = r.eligible ? 'Eligible research input' : 'Hold: not available at this research date';
      panel.querySelector('[data-cr-caption]').textContent = step === 2 && !r.eligible
        ? 'Stop here. This version was released after the research date. Preserve it for a later run.' : captions[step];
      steps.forEach((item, index) => { item.dataset.state = index === step ? 'current' : index < step ? 'complete' : 'waiting'; });
      panel.querySelector('[data-cr-token]').setAttribute('cx', String(30 + step * 175));
      panel.querySelector('[data-cr-progress]').setAttribute('x2', String(30 + step * 175));
      next.disabled = step >= last;
      if (step >= last) pause();
    }
    function advance() { step = Math.min(step + 1, result().eligible ? 4 : 2); render(); }
    function reset() { pause(); step = 0; render(); }
    play.addEventListener('click', () => {
      if (timer !== null) { pause(); return; }
      if (step >= (result().eligible ? 4 : 2)) step = 0;
      if (reduce.matches) { advance(); return; }
      play.textContent = 'Pause'; play.setAttribute('aria-pressed','true');
      timer = root.setInterval(advance, 1100); advance();
    });
    next.addEventListener('click', () => { pause(); advance(); });
    panel.querySelector('[data-cr-reset]').addEventListener('click', reset);
    date.addEventListener('change', reset); revision.addEventListener('change', reset);
    panel.querySelectorAll('[data-demo-controls]').forEach(el => { el.hidden = false; });
    onPause(panel, pause); render();
  }
  function initRAI(panel) {
    const include = panel.querySelector('[data-rai-include]');
    const attribution = panel.querySelector('[data-rai-attribution]');
    const observation = panel.querySelector('[data-rai-observation]');
    const trace = panel.querySelector('[data-rai-trace]');
    let timer = null, stage = 0;
    function pause() { if (timer !== null) root.clearInterval(timer); timer = null; panel.dataset.tracing = 'false'; }
    function render() {
      const r = evaluateRAI({includeB:include.checked, attributionValid:attribution.checked, agrees:observation.value === 'tightening'});
      panel.dataset.result = r.state;
      panel.querySelector('[data-demo-status]').textContent = r.title;
      panel.querySelector('[data-rai-detail]').textContent = r.detail;
      panel.querySelector('[data-rai-b-text]').textContent = observation.value === 'tightening' ? 'Tightening' : 'Easing';
      panel.querySelector('[data-rai-b]').dataset.included = String(include.checked);
      panel.querySelector('[data-rai-citation]').textContent = attribution.checked ? 'B → Source B' : 'B → Source A (mismatch)';
    }
    [include, attribution, observation].forEach(el => el.addEventListener('change', () => { pause(); render(); }));
    trace.addEventListener('click', () => {
      pause(); stage = 0; panel.dataset.traceStage = '0';
      if (reduce.matches) { panel.dataset.traceStage = '2'; return; }
      panel.dataset.tracing = 'true';
      timer = root.setInterval(() => { stage++; panel.dataset.traceStage = String(stage); if (stage >= 2) pause(); }, 650);
    });
    panel.querySelector('[data-rai-reset]').addEventListener('click', () => {
      pause(); include.checked = true; attribution.checked = true; observation.value = 'easing'; panel.dataset.traceStage = ''; render();
    });
    panel.querySelectorAll('[data-demo-controls]').forEach(el => { el.hidden = false; });
    onPause(panel, pause); render();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
