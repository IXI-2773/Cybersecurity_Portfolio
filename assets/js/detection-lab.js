(function(root){
  'use strict';
  function evaluateAuthentication(events,{windowSeconds=600,threshold=5}={}){
    if(!Array.isArray(events)||!Number.isFinite(windowSeconds)||windowSeconds<0||!Number.isInteger(threshold)||threshold<1)throw new TypeError('Invalid detector inputs');
    const seen=new Set();
    const ordered=events.map((event,index)=>{
      for(const k of ['id','timestamp','username','source_ip','host','scenario'])if(typeof event[k]!=='string'||!event[k].trim())throw new TypeError('Missing '+k);
      const time=Date.parse(event.timestamp);
      if(!Number.isFinite(time)||!/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$/.test(event.timestamp)||new Date(time).toISOString().replace('.000Z','Z')!==event.timestamp)throw new TypeError('Invalid UTC timestamp');
      if('epochMs' in event&&event.epochMs!==time)throw new TypeError('Inconsistent epoch');
      if(seen.has(event.id)||!['login_failure','login_success'].includes(event.event_type))throw new TypeError('Invalid event');seen.add(event.id);
      return {event,index,time};
    }).sort((a,b)=>a.time-b.time||a.index-b.index);
    const findings=[],decisions=[],history=[],resetAt=new Map();
    for(const row of ordered){
      const e=row.event,key=JSON.stringify([e.username,e.source_ip]);
      if(e.event_type==='login_success'){
        const contributingIds=[],exclusions=[];
        for(const prior of history){
          if(prior.event.event_type!=='login_failure')continue;
          const p=prior.event,ageSeconds=(row.time-prior.time)/1000;
          let reason=null;
          if(p.username!==e.username)reason='different account';
          else if(p.source_ip!==e.source_ip)reason='different source IP';
          else if(resetAt.has(key)&&prior.sequence<=resetAt.get(key))reason='before intervening success';
          else if(ageSeconds>windowSeconds)reason='outside window';
          if(reason)exclusions.push({id:p.id,reason,ageSeconds});else contributingIds.push(p.id);
        }
        const triggered=contributingIds.length>=threshold;
        decisions.push({successId:e.id,contributingIds,exclusions,count:contributingIds.length,triggered});
        if(triggered)findings.push({scenario:e.scenario,timestamp:e.timestamp,username:e.username,source_ip:e.source_ip,failure_count_in_window:contributingIds.length});
        resetAt.set(key,history.length);
      }
      history.push({...row,sequence:history.length});
    }
    return {findings,decisions};
  }
  const api={evaluateAuthentication};root.PortfolioDetection=api;if(typeof module!=='undefined')module.exports=api;
  if(!root.document)return;
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fixture=root.PortfolioTechnicalFixtures.authentication;
  const labels={threshold:'Threshold reached',below:'Below threshold',intervening_success:'Success interrupts streak',post_success_burst:'New streak after success',expired:'Expired window',other_user:'Different accounts',other_ip:'Different source IPs',ten_minute_boundary:'Exact 600-second boundary',interleaved_users:'Interleaved accounts'};
  root.document.querySelectorAll('[data-detection-lab]').forEach(panel=>{
    const select=panel.querySelector('[data-auth-scenario]');
    const scenarios=[...new Set(fixture.events.map(x=>x.scenario))];
    select.innerHTML=scenarios.map(s=>`<option value="${s}">${esc(labels[s])}</option>`).join('');select.value='ten_minute_boundary';
    const result=evaluateAuthentication(fixture.events);
    panel.querySelector('[data-auth-validation]').textContent=`${result.findings.length} of ${fixture.expectedFindings.length} expected findings match in this browser replay · ${fixture.events.length} source events · ${scenarios.length} scenarios`;
    panel.querySelector('[data-auth-spl]').textContent=fixture.splExcerpt;
    panel.querySelector('[data-auth-hash]').textContent=fixture.sourceHash;
    let replay=null,events=[],decision=null;
    function render(index,running){
      panel.dataset.running=String(running);
      panel.querySelector('[data-replay-play]').textContent=running?'Pause':'Play';
      const current=events[index];
      const end=events.find(x=>x.id===(decision&&decision.successId))||events[events.length-1];
      const min=Math.min(...events.map(e=>e.epochMs),end.epochMs-600000),span=Math.max(end.epochMs-min,1000);
      const x=e=>45+((e.epochMs-min)/span)*610;
      const cutoff=45+((end.epochMs-600000-min)/span)*610;
      panel.querySelector('[data-auth-timeline]').innerHTML=`<rect class="window-zone" x="${cutoff}" y="16" width="${655-cutoff}" height="90" rx="4"/><text x="${cutoff+8}" y="34" class="chart-note">inclusive 600 s window</text><path class="axis-line" d="M40 75H665"/>`+events.map((e,i)=>`<circle class="event-dot ${e.event_type==='login_success'?'success-dot':''} ${i===index?'selected-dot':''} ${i>index?'pending-dot':''}" cx="${x(e)}" cy="75" r="${i===index?9:6}"/><text x="${x(e)}" y="${i%2?130:112}" class="chart-time">${esc(e.timestamp.slice(11,19))}</text>`).join('');
      panel.querySelector('[data-auth-events]').innerHTML=events.map((e,i)=>`<button type="button" data-event-index="${i}" aria-pressed="${i===index}"><span>${esc(e.timestamp.slice(11,19))}</span><strong>${e.event_type==='login_failure'?'Failure':'Success'}</strong><span>${esc(e.username)}</span></button>`).join('');
      const excluded=decision&&decision.exclusions.find(e=>e.id===current.id);
      const included=decision&&decision.contributingIds.includes(current.id);
      const reason=included?'Included: same account/IP, since previous success, age ≤ 600 s':excluded?'Excluded: '+excluded.reason:current.event_type==='login_success'?'Success event: evaluates and then resets this account/IP streak':'Not a preceding failure for this decision';
      panel.querySelector('[data-auth-inspector]').innerHTML=`<h3>${esc(current.id)} · ${esc(current.event_type)}</h3><dl class="field-list">${Object.entries({timestamp:current.timestamp,username:current.username,source_ip:current.source_ip,host:current.host,age_at_success:((end.epochMs-current.epochMs)/1000)+' s',scenario:current.scenario}).map(([k,v])=>`<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl><p class="decision-reason">${esc(reason)}</p>`;
      panel.querySelector('[data-auth-outcome]').textContent=decision&&decision.triggered?`${decision.count} qualifying failures → investigate. Compromise is not established.`:'Rule not triggered. Absence of a match does not establish benign activity.';
      panel.querySelector('[data-replay-step]').disabled=index===events.length-1;
    }
    function load(){if(replay)replay.dispose();events=fixture.events.filter(e=>e.scenario===select.value);const evaluation=evaluateAuthentication(events);decision=evaluation.decisions.at(-1);replay=root.PortfolioReplay.createReplay({count:events.length,onChange:render,element:panel,intervalMs:950});}
    panel.querySelector('[data-auth-events]').addEventListener('click',e=>{const b=e.target.closest('[data-event-index]');if(b)replay.select(Number(b.dataset.eventIndex));});
    panel.querySelector('[data-replay-play]').addEventListener('click',()=>panel.dataset.running==='true'?replay.pause():replay.play());
    panel.querySelector('[data-replay-step]').addEventListener('click',()=>replay.step());panel.querySelector('[data-replay-reset]').addEventListener('click',()=>replay.reset());select.addEventListener('change',load);
    panel.querySelectorAll('[data-enhanced]').forEach(e=>e.hidden=false);load();
  });
})(globalThis);
