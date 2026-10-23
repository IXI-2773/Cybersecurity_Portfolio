/* Public teaching engines. Independent of private CR/RAI and the Python/Splunk runtime. */
'use strict';
globalThis.PortfolioEngine = (() => {
  function detectAuth(events, {threshold = 5, windowSeconds = 600} = {}) {
    if (!Number.isInteger(threshold) || threshold < 1 || !Number.isInteger(windowSeconds) || windowSeconds < 1) {
      throw new Error('Threshold and window must be positive integers.');
    }
    if (!Array.isArray(events)) throw new Error('Expected an event array.');
    const ordered = events.map(event => {
      if (!event || typeof event.username !== 'string' || !event.username ||
          typeof event.source_ip !== 'string' || !event.source_ip ||
          !['login_failure', 'login_success'].includes(event.event_type) ||
          !/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$/.test(event.timestamp)) {
        throw new Error('Invalid authentication event.');
      }
      const time = Date.parse(event.timestamp);
      if (!Number.isFinite(time) || new Date(time).toISOString().replace('.000Z', 'Z') !== event.timestamp) {
        throw new Error('Invalid event timestamp.');
      }
      return {event, time};
    }).sort((a, b) => a.time - b.time);
    const histories = new Map();
    const findings = [];
    for (const {event, time} of ordered) {
      const key = JSON.stringify([event.username, event.source_ip]);
      const recent = (histories.get(key) || []).filter(t => time - t <= windowSeconds * 1000);
      if (event.event_type === 'login_failure') recent.push(time);
      else {
        if (recent.length >= threshold) findings.push({
          scenario: event.scenario || 'browser_check',
          timestamp: event.timestamp,
          username: event.username,
          source_ip: event.source_ip,
          failure_count_in_window: recent.length
        });
        recent.length = 0;
      }
      histories.set(key, recent);
    }
    return findings;
  }

  // This checks structured attribution and completeness, not the truth of a document.
  function checkCoverage(records, declarations) {
    for (const list of [records, declarations]) {
      if (!Array.isArray(list) || list.some(r => !r || typeof r.source !== 'string' || !r.source || !Number.isFinite(r.value))) {
        throw new Error('Evidence rows require a source identifier and a finite numeric value.');
      }
    }
    if (new Set(records.map(r => r.source)).size !== records.length) throw new Error('Evidence source identifiers must be unique.');
    if (!records.length) return {status:'HOLD_NO_EVIDENCE',reason:'No evidence records are available.'};
    const reference = new Map(records.map(r => [r.source, r.value]));
    const mentioned = new Set();
    for (const row of declarations) {
      if (mentioned.has(row.source)) return {status:'HOLD_DUPLICATE_ATTRIBUTION',reason:'A source is attributed more than once.'};
      mentioned.add(row.source);
      if (!reference.has(row.source)) return {status:'HOLD_UNSUPPORTED_SOURCE',reason:'A declared source is absent from the evidence.'};
      if (reference.get(row.source) !== row.value) return {status:'HOLD_ATTRIBUTION_MISMATCH',reason:'A reported value does not match its attributed source.'};
    }
    if (mentioned.size !== reference.size) return {status:'HOLD_INCOMPLETE_COVERAGE',reason:'At least one evidence record is omitted.'};
    return {status:'PASS_COVERAGE',reason:'Every supplied record is included with matching source and value; disagreement remains visible.'};
  }

  const evidenceCases = {
    complete: {label:'Preserve the disagreement',records:[{source:'A',value:4},{source:'B',value:6}],declarations:[{source:'A',value:4},{source:'B',value:6}]},
    omitted: {label:'Omit the conflicting source',records:[{source:'A',value:4},{source:'B',value:6}],declarations:[{source:'A',value:4}]},
    mismatch: {label:'Attribute the wrong value',records:[{source:'A',value:4},{source:'B',value:6}],declarations:[{source:'A',value:4},{source:'B',value:4}]}
  };
  function runChecks(data) {
    const event = (second, type, user = 'check_user', ip = '192.0.2.1') => ({
      timestamp:new Date(Date.UTC(2026,9,5,0,0,second)).toISOString().replace('.000Z','Z'),
      username:user,source_ip:ip,event_type:type
    });
    const failures = [0,1,2,3,4].map(s => event(s,'login_failure'));
    const same = (a,b) => JSON.stringify(a) === JSON.stringify(b);
    const tests = [
      ['Frozen 64-event matrix', 'Matches the five independently recorded expected rows.', () => same(detectAuth(data.events),data.expected)],
      ['Inclusive 600-second boundary','Failures exactly 600 seconds old remain in scope.', () => detectAuth([...failures,event(600,'login_success')]).length === 1],
      ['Outside the time window','One expired failure leaves fewer than five in scope.', () => detectAuth([...failures,event(601,'login_success')]).length === 0],
      ['Success resets the streak','Separate bursts do not combine after a success.', () => detectAuth([...failures.slice(0,4),event(5,'login_success'),event(6,'login_failure'),event(7,'login_success')]).length === 0],
      ['Identity isolation','A success on another source IP does not inherit failures.', () => detectAuth([...failures,event(5,'login_success','check_user','192.0.2.2')]).length === 0],
      ['Complete attributed coverage','Both conflicting records remain visible.', () => checkCoverage(evidenceCases.complete.records,evidenceCases.complete.declarations).status === 'PASS_COVERAGE'],
      ['Omitted conflicting record','Missing coverage produces a hold.', () => checkCoverage(evidenceCases.omitted.records,evidenceCases.omitted.declarations).status === 'HOLD_INCOMPLETE_COVERAGE'],
      ['Wrong source value','Misattribution produces a hold.', () => checkCoverage(evidenceCases.mismatch.records,evidenceCases.mismatch.declarations).status === 'HOLD_ATTRIBUTION_MISMATCH'],
      ['Absent evidence','An empty evidence set cannot pass.', () => checkCoverage([],[]).status === 'HOLD_NO_EVIDENCE']
    ];
    return tests.map(([name,purpose,run]) => {
      try { return {name,purpose,passed:Boolean(run())}; }
      catch (error) { return {name,purpose,passed:false,error:error.message}; }
    });
  }
  return {detectAuth,checkCoverage,evidenceCases,runChecks,version:'1.0.0'};
})();
