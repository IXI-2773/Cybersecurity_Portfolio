/* Homepage preview of the independent public authentication training replay.
   This is not Splunk execution, private CR/RAI execution, or live telemetry. */
'use strict';
(() => {
  const root = document.querySelector('#boundary-replay');
  const engine = globalThis.PortfolioEngine;
  const fixture = globalThis.PortfolioLabData;
  if (!root || !engine || !fixture) return;
  const buttons = [...root.querySelectorAll('[data-replay-window]')];
  const cases = [...root.querySelectorAll('[data-replay-username]')];
  const count = root.querySelector('#home-replay-count');
  const status = root.querySelector('#home-replay-status');
  if (buttons.length !== 2 || cases.length !== fixture.expected.length ||
      !fixture.expected.every(row => cases.some(item => item.dataset.replayUsername === row.username))) return;
  const key = row => JSON.stringify([row.timestamp, row.username, row.source_ip, row.failure_count_in_window]);
  const expected = new Set(fixture.expected.map(key));
  function render(seconds) {
    try {
      const findings = engine.detectAuth(fixture.events, {threshold:5, windowSeconds:seconds});
      const actual = new Set(findings.map(key));
      const missing = fixture.expected.filter(row => !actual.has(key(row)));
      const unexpected = findings.filter(row => !expected.has(key(row)));
      count.textContent = `${findings.length} / ${fixture.expected.length}`;
      status.textContent = `${missing.length} baseline findings missing · ${unexpected.length} additional or mismatched. ${seconds}-second inclusive window; computed from frozen synthetic inputs.`;
      root.dataset.replayResult = missing.length || unexpected.length ? 'difference' : 'match';
      for (const cell of cases) {
        const reference = fixture.expected.find(row => row.username === cell.dataset.replayUsername);
        const found = actual.has(key(reference));
        cell.dataset.replayStatus = found ? 'match' : 'missing';
        cell.querySelector('[data-replay-verdict]').textContent = found ? 'MATCH' : 'MISSING';
      }
      for (const button of buttons) button.setAttribute('aria-pressed', String(Number(button.dataset.replayWindow) === seconds));
    } catch (error) {
      status.textContent = 'Replay could not be calculated. Open the full workbench to inspect the source and controls.';
      root.dataset.replayResult = 'error';
    }
  }
  render(600);
  for (const button of buttons) {
    button.disabled = false;
    button.addEventListener('click', () => render(Number(button.dataset.replayWindow)));
  }
})();
