'use strict';
(() => {
  const engine = globalThis.PortfolioEngine;
  const fixture = globalThis.PortfolioLabData;
  if (!engine || !fixture) return;
  const byId = id => document.getElementById(id);
  const receipt = {schema:'portfolio.browser-run.v1',engine:engine.version,scope:'Independent public teaching engines; synthetic fixtures; not private CR/RAI or Splunk execution',sources:fixture.sources};
  function rows(target, values) {
    const fragment = document.createDocumentFragment();
    for (const value of values) {
      const tr = document.createElement('tr');
      for (const cell of value) {const td=document.createElement('td');td.textContent=String(cell);tr.append(td);}
      fragment.append(tr);
    }
    target.replaceChildren(fragment);
  }
  const stamp = () => new Date().toISOString();
  byId('run-checks').disabled = false;
  byId('replay-submit').disabled = false;
  byId('coverage-submit').disabled = false;
  byId('run-checks').addEventListener('click',() => {
    const checks=engine.runChecks(fixture);
    const passed=checks.filter(check => check.passed).length;
    rows(byId('check-rows'),checks.map(check => [check.passed?'PASS':'FAIL',check.name,check.purpose]));
    byId('checks-status').textContent=`${passed} / ${checks.length} checks passed in this browser run.`;
    byId('checks-status').dataset.result=passed===checks.length?'pass':'hold';
    receipt.baseline={run_at:stamp(),settings:{threshold:5,window_seconds:600},checks};
    byId('download-run').disabled=false;
  });
  byId('replay-form').addEventListener('submit',event => {
    event.preventDefault();
    const form=event.currentTarget;
    if (!form.reportValidity()) return;
    try {
      const threshold=Number(byId('auth-threshold').value);
      const windowSeconds=Number(byId('auth-window').value);
      const findings=engine.detectAuth(fixture.events,{threshold,windowSeconds});
      const key=row => JSON.stringify([row.timestamp,row.username,row.source_ip,row.failure_count_in_window]);
      const expected=new Set(fixture.expected.map(key));
      const actual=new Set(findings.map(key));
      const missing=[...expected].filter(row => !actual.has(row)).length;
      const additional=[...actual].filter(row => !expected.has(row)).length;
      rows(byId('replay-rows'),findings.map(row => [row.timestamp.slice(11,19),row.username,row.source_ip,row.failure_count_in_window]));
      byId('replay-empty').hidden=findings.length>0;
      byId('replay-status').textContent=`${findings.length} findings · ${missing} baseline rows missing · ${additional} additional rows. ${threshold===5 && windowSeconds===600?'Frozen baseline settings.':'Modified rule settings.'}`;
      receipt.replay={run_at:stamp(),settings:{threshold,window_seconds:windowSeconds},findings,baseline_comparison:{missing,additional}};
    } catch(error) {byId('replay-status').textContent=error.message;}
  });
  byId('coverage-form').addEventListener('submit',event => {
    event.preventDefault();
    const sample=engine.evidenceCases[byId('coverage-case').value];
    if (!sample) return;
    const result=engine.checkCoverage(sample.records,sample.declarations);
    byId('coverage-input').textContent=JSON.stringify({evidence:sample.records,reported:sample.declarations},null,2);
    byId('coverage-status').textContent=result.status;
    byId('coverage-status').dataset.result=result.status==='PASS_COVERAGE'?'pass':'hold';
    byId('coverage-reason').textContent=result.reason;
    receipt.coverage={run_at:stamp(),scenario:byId('coverage-case').value,input:sample,result};
  });
  byId('download-run').addEventListener('click',() => {
    if (!receipt.baseline) return;
    const blob=new Blob([JSON.stringify(receipt,null,2)+'\n'],{type:'application/json'});
    const url=URL.createObjectURL(blob);
    const anchor=document.createElement('a');anchor.href=url;anchor.download='Don_Lopez_Public_Engine_Run.json';
    document.body.append(anchor);anchor.click();anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url),1000);
  });
})();
