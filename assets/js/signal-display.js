/* Public fixture replay. Context from separate investigations is never merged. */
(function(root){
 'use strict';
 const fixture=root.PortfolioTechnicalFixtures.authentication, evaluate=root.PortfolioDetection.evaluateAuthentication;
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const panel=document.querySelector('[data-signal-display]');
 if(panel){
  const scenario=panel.querySelector('[data-signal-scenario]');let replay;
  function render(index,running){
   panel.dataset.running=String(running);panel.dataset.stage=String(index);
   panel.querySelector('[data-signal-play]').textContent=running?'Pause':'Play';panel.querySelector('[data-signal-step]').disabled=index===3;
   panel.querySelectorAll('[data-signal-stage]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.signalStage)===index)));
   const events=fixture.events.filter(e=>e.scenario===scenario.value),r=evaluate(events),d=r.decisions.at(-1),hit=d&&d.triggered;
   panel.querySelector('[data-signal-chart]').innerHTML='<path class="signal-route" d="M30 40H570"/>'+events.map((e,i)=>`<circle class="signal-data-dot ${index>0&&d.contributingIds.includes(e.id)?'contributes':''}" cx="${30+i*540/(events.length-1)}" cy="40" r="${e.event_type==='login_success'?10:6}"/><text class="signal-chart-label" x="${30+i*540/(events.length-1)}" y="75" text-anchor="middle">${esc(e.timestamp.slice(11,16))}</text>`).join('');
   const content=[['Preserve the source events',`${events.length} timestamped events. ${esc(events[0].username)} · ${esc(events[0].source_ip)}. Source fields remain attached to this sequence.`],['Evaluate the relationship',`${d.count} failures in the inclusive 0–600 s window. Same username + source IP; every success resets the streak. ${hit?'Threshold reached.':'Threshold not reached.'}`],['Ask for the missing context','MFA/session evidence and endpoint context are not supplied in this authentication fixture. <a href="projects/network-traffic-analysis.html">Packet work</a> and <a href="projects/windows-process-triage.html">Windows triage</a> are independent investigations.'],['Document a bounded disposition',hit?'Investigate: suspicious authentication sequence; compromise not established. Review MFA outcome, account history, and related endpoint activity.':'Rule not triggered. Absence of a finding does not establish benign activity. Keep the sequence available for review.']];
   panel.querySelector('[data-signal-detail]').innerHTML=`<h3>${content[index][0]}</h3><p>${content[index][1]}</p><details><summary>Inspect source event IDs</summary><p class="signal-event-ids">${events.map(e=>esc(e.id)).join(' · ')}</p><a href="projects/01-authentication-detection/validation_events.csv">Open canonical events ↗</a></details>`;
  }
  replay=root.PortfolioReplay.createReplay({count:4,intervalMs:2200,onChange:render,element:panel});
  panel.querySelector('[data-signal-stages]').addEventListener('click',e=>{const b=e.target.closest('[data-signal-stage]');if(b)replay.select(Number(b.dataset.signalStage));});
  panel.querySelector('[data-signal-play]').addEventListener('click',()=>panel.dataset.running==='true'?replay.pause():replay.play());
  panel.querySelector('[data-signal-step]').addEventListener('click',()=>replay.step());panel.querySelector('[data-signal-reset]').addEventListener('click',()=>replay.reset());scenario.addEventListener('change',()=>replay.reset());panel.querySelectorAll('[data-enhanced]').forEach(e=>e.hidden=false);
 }
 document.querySelectorAll('[data-auth-preview]').forEach(panel=>{
  const events=fixture.events.filter(e=>e.scenario==='ten_minute_boundary');
  const replay=root.PortfolioReplay.createReplay({count:events.length,intervalMs:900,element:panel,onChange:(index,running)=>{
   panel.dataset.running=String(running);panel.querySelector('[data-preview-play]').textContent=running?'Pause sequence':'Play sequence';
   panel.querySelector('[data-preview-chart]').innerHTML='<path class="axis-line" d="M20 55H380"/>'+events.map((e,i)=>`<circle class="event-dot ${i===index?'selected-dot':''}" cx="${20+(e.epochMs-events[0].epochMs)/600000*360}" cy="55" r="${i===index?9:5}"/><text x="${20+(e.epochMs-events[0].epochMs)/600000*360}" y="${i%2?100:82}" class="chart-time">${e.timestamp.slice(11,16)}</text>`).join('');
   panel.querySelector('[data-preview-caption]').textContent=index===events.length-1?'Success at 13:10 includes the failure at 13:00.':'Inspect '+events[index].id+' · '+events[index].timestamp.slice(11,19)+' UTC';
  }});
  const button=panel.querySelector('[data-preview-play]');button.hidden=false;button.addEventListener('click',()=>panel.dataset.running==='true'?replay.pause():replay.play());
 });
})(globalThis);
