(function(root){
 'use strict';
 const utc=s=>typeof s==='string'&&/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$/.test(s)&&Number.isFinite(Date.parse(s))&&new Date(s).toISOString().replace('.000Z','Z')===s;
 function resolveVintage(records,decisionTime){
  const invalid={state:'invalid',selectedId:null,exclusions:[]},seen=new Set();
  if(!Array.isArray(records)||!utc(decisionTime))return invalid;
  for(const r of records){if(!r||typeof r.record_id!=='string'||!r.record_id||seen.has(r.record_id)||!utc(r.observation_time)||!utc(r.available_at)||typeof r.vintage_id!=='string'||!r.vintage_id||!Number.isFinite(r.value)||!(/^[0-9a-f]{64}$/).test(r.source_hash))return invalid;seen.add(r.record_id);}
  const exclusions=[],eligible=[];
  for(const r of records){const reason=r.observation_time>decisionTime?'future observation':r.available_at>decisionTime?'not yet available':null;if(reason)exclusions.push({record_id:r.record_id,reason});else eligible.push(r);}
  if(!eligible.length)return {state:'unavailable',selectedId:null,exclusions};
  eligible.sort((a,b)=>b.available_at.localeCompare(a.available_at)||a.record_id.localeCompare(b.record_id));
  const latest=eligible.filter(x=>x.available_at===eligible[0].available_at);
  if(latest.some(x=>x.value!==latest[0].value||x.vintage_id!==latest[0].vintage_id||x.observation_time!==latest[0].observation_time))return {state:'ambiguous',selectedId:null,exclusions:[...exclusions,...eligible.map(x=>({record_id:x.record_id,reason:latest.includes(x)?'ambiguous latest vintage':'superseded'}))]};
  return {state:'selected',selectedId:eligible[0].record_id,exclusions:[...exclusions,...eligible.slice(1).map(x=>({record_id:x.record_id,reason:x.available_at===eligible[0].available_at?'equivalent vintage':'superseded'}))]};
 }
 function traceClaim(scenario){
  const passages=[];const outcome=(state,explanation)=>({state,passageIds:passages,explanation});
  if(!scenario||!Array.isArray(scenario.sources)||!Array.isArray(scenario.citations)||!Array.isArray(scenario.requiredSourceIds)||scenario.requiredSourceIds.length<2)return outcome('missing','Required source coverage is missing. Narrow the claim or retrieve the missing evidence.');
  const {sources,citations,requiredSourceIds}=scenario;
  if(new Set(sources.map(x=>x.source_id)).size!==sources.length||new Set(sources.map(x=>x.passage_id)).size!==sources.length)return outcome('attribution','Source or passage identities are ambiguous. Repair the record before tracing the claim.');
  for(const c of citations){const p=sources.find(x=>x.passage_id===c.passage_id);if(!p||p.source_id!==c.source_id)return outcome('attribution','The cited passage belongs to a different source. Correct its attribution before assessing support.');passages.push(p.passage_id);}
  if(requiredSourceIds.some(id=>!sources.some(x=>x.source_id===id)||!citations.some(x=>x.source_id===id)))return outcome('missing','Only part of the required evidence is present. Source A alone cannot establish what both sources indicate.');
  const cited=sources.filter(x=>passages.includes(x.passage_id));
  if(cited.some(x=>!x.scope||!x.period||!x.text||!x.observation))return outcome('missing','A cited record lacks its scope, period, passage, or structured observation.');
  if(cited.some(x=>x.scope!==cited[0].scope||x.period!==cited[0].period))return outcome('not-comparable','The observations cover different measurements or periods. Report them separately; this does not establish consensus or resolve a contradiction.');
  if(cited.some(x=>x.observation!==cited[0].observation))return outcome('conflict','Comparable observations disagree. Preserve both passages and investigate their methods before making a joint claim.');
  if(cited[0].observation!=='tightening')return outcome('conflict','The structured observations do not support the proposed tightening claim. Revise its wording.');
  return outcome('supported','Both cited passages report tighter business credit for the same period. This supports the authored example claim; source truth has not been independently verified.');
 }
 const api={resolveVintage,traceClaim};root.PortfolioResearch=api;if(typeof module!=='undefined')module.exports=api;
 if(!root.document)return;
 const f=root.PortfolioResearchFixtures,esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function wirePlayback(panel,count,render){let replay;replay=root.PortfolioReplay.createReplay({count,element:panel,intervalMs:1500,onChange:(i,running)=>{panel.dataset.running=String(running);panel.querySelector('[data-replay-play]').textContent=running?'Pause':'Play';panel.querySelector('[data-replay-step]').disabled=i===count-1;render(i);}});panel.querySelector('[data-replay-play]').addEventListener('click',()=>panel.dataset.running==='true'?replay.pause():replay.play());panel.querySelector('[data-replay-step]').addEventListener('click',()=>replay.step());panel.querySelector('[data-replay-reset]').addEventListener('click',()=>replay.reset());panel.querySelectorAll('[data-enhanced]').forEach(x=>x.hidden=false);return replay;}
 document.querySelectorAll('[data-vintage-workbench]').forEach(panel=>{
  const cutoff=panel.querySelector('[data-vintage-cutoff]'),mode=panel.querySelector('[data-vintage-mode]');let selected='release-v1',step=0,replay;
  const records=()=>mode.value==='ambiguous'?[...f.versions,{...f.versions[1],record_id:'conflicting-v2',value:9}]:f.versions;
  function render(){const rows=records(),r=resolveVintage(rows,cutoff.value),record=rows.find(x=>x.record_id===selected)||rows[0];panel.dataset.result=r.state;
   panel.querySelector('[data-vintage-records]').innerHTML=rows.map(x=>{const reason=x.record_id===r.selectedId?'selected':r.exclusions.find(e=>e.record_id===x.record_id)?.reason||r.state;return `<button type="button" data-record-id="${esc(x.record_id)}" aria-pressed="${x.record_id===selected}"><span>${esc(x.vintage_id)} · ${x.value}</span><strong>${esc(reason)}</strong><span>${esc(x.available_at.slice(0,10))}</span></button>`;}).join('');
   panel.querySelector('[data-vintage-inspector]').innerHTML=`<h3>${esc(record.record_id)}</h3><dl class="field-list">${Object.entries(record).map(([k,v])=>`<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>`;
   const captions=['Validate the record schema and retain its identity.','Check observation time and version availability against the cutoff.','Choose the latest eligible vintage; hold conflicting latest ties.','Record the selected ID and every exclusion without overwriting earlier inputs.'];
   panel.querySelector('[data-vintage-caption]').textContent=captions[step];
   panel.querySelector('[data-vintage-outcome]').textContent=r.selectedId?`Dataset includes ${r.selectedId}. Other records retain their exclusion reasons.`:r.state==='ambiguous'?'Hold: conflicting latest vintages. No record is selected.':'Hold: no eligible record at this cutoff.';
   panel.querySelector('[data-vintage-receipt]').textContent=JSON.stringify({fixture:'public-research-examples.v1',fixture_sha256:f.sourceHash,decision_time:cutoff.value,selected_ids:r.selectedId?[r.selectedId]:[],exclusions:r.exclusions},null,2);
   const day=s=>(Date.parse(s)-Date.parse('2026-02-25T00:00:00Z'))/86400000, x=s=>70+day(s)*9;
   panel.querySelector('[data-vintage-timeline]').innerHTML=`<text x="5" y="40" class="chart-note">observed</text><text x="5" y="120" class="chart-note">available</text><path class="axis-line" d="M70 45H660M70 125H660"/><line class="cutoff-line" x1="${x(cutoff.value)}" x2="${x(cutoff.value)}" y1="15" y2="160"/><text x="${Math.min(x(cutoff.value)+5,580)}" y="17" class="chart-note">cutoff</text>`+rows.map((q,i)=>`<path class="vintage-wire ${q.record_id===r.selectedId?'admitted':''}" d="M${x(q.observation_time)} 45L${x(q.available_at)} 125"/><circle class="event-dot ${q.record_id===selected?'selected-dot':''}" cx="${x(q.available_at)}" cy="125" r="6"/><text x="${x(q.available_at)}" y="${145+(i%2)*17}" class="chart-time">${esc(q.vintage_id)}</text>`).join('');
  }
  replay=wirePlayback(panel,4,i=>{step=i;render();});[cutoff,mode].forEach(x=>x.addEventListener('change',()=>{replay.reset();render();}));panel.querySelector('[data-vintage-records]').addEventListener('click',e=>{const b=e.target.closest('[data-record-id]');if(b){selected=b.dataset.recordId;replay.pause();render();}});
 });
 document.querySelectorAll('[data-claim-workbench]').forEach(panel=>{
  const select=panel.querySelector('[data-claim-scenario]');select.innerHTML=f.claims.map(s=>`<option value="${s.id}">${esc(s.title)}</option>`).join('');select.value='scope';let selected='A:p1',stage=0,replay;
  function render(){const scenario=f.claims.find(x=>x.id===select.value),r=traceClaim(scenario),source=scenario.sources.find(x=>x.passage_id===selected)||scenario.sources[0];selected=source.passage_id;
   panel.dataset.result=r.state;panel.dataset.traceStage=String(stage);panel.querySelector('[data-claim-text]').textContent=scenario.claim;
   panel.querySelector('[data-claim-sources]').innerHTML=scenario.sources.map(x=>`<button type="button" data-passage-id="${esc(x.passage_id)}" aria-pressed="${x.passage_id===selected}"><span>${esc(x.source_id)} · ${esc(x.period)}</span><strong>${esc(x.scope)}</strong><span>${esc(x.observation)}</span></button>`).join('');
   panel.querySelector('[data-claim-inspector]').innerHTML=`<h3>${esc(source.title)}</h3><p class="passage-id">${esc(source.passage_id)} · ${esc(source.period)} · ${esc(source.scope)}</p><blockquote>${esc(source.text)}</blockquote><p>Recorded citations: ${scenario.citations.map(x=>esc(x.passage_id)+' → '+esc(x.source_id)).join('; ')}</p>`;
   const stateLabels={supported:'Supported within this example',conflict:'Preserve the disagreement',missing:'Hold: missing source coverage',attribution:'Hold: citation attribution mismatch','not-comparable':'Not directly comparable'};
   panel.querySelector('[data-claim-outcome]').textContent=stateLabels[r.state];panel.querySelector('[data-claim-explanation]').textContent=r.explanation;
   const captions=['Retrieve candidates; do not treat retrieval as proof.','Trace each citation to an exact source passage.','Compare scope, period, and structured observations.','Write an answer bounded by this evidence.'];panel.querySelector('[data-claim-caption]').textContent=captions[stage];
   const answer=r.state==='supported'?'Both sources report tighter business credit in February.':r.state==='not-comparable'?`Source A describes ${scenario.sources[0].scope} in ${scenario.sources[0].period}; source B describes ${scenario.sources[1].scope} in ${scenario.sources[1].period}. These observations do not establish a joint trend.`:r.explanation;
   panel.querySelector('[data-claim-answer]').textContent=answer;
   panel.querySelectorAll('[data-trace-node]').forEach((x,i)=>x.dataset.active=String(i<=stage));
  }
  replay=wirePlayback(panel,4,i=>{stage=i;render();});panel.querySelector('.claim-graph').addEventListener('click',e=>{const b=e.target.closest('[data-trace-step]');if(b)replay.select(Number(b.dataset.traceStep));});select.addEventListener('change',()=>{selected='A:p1';replay.reset();});panel.querySelector('[data-claim-sources]').addEventListener('click',e=>{const b=e.target.closest('[data-passage-id]');if(b){selected=b.dataset.passageId;replay.pause();render();}});
 });
 document.querySelectorAll('[data-research-preview]').forEach(panel=>{const type=panel.dataset.researchPreview;const captions=type==='cr'?['Preserve every release','Reject unavailable revisions','Select the eligible vintage','Record lineage + exclusions']:['Retrieve source passages','Trace exact citations','Compare scope + period','Keep the answer bounded'];const replay=root.PortfolioReplay.createReplay({count:4,element:panel,onChange:(i,running)=>{panel.dataset.running=String(running);panel.dataset.previewStage=String(i);panel.querySelector('[data-preview-caption]').textContent=captions[i];panel.querySelector('[data-preview-play]').textContent=running?'Pause trace':'Play trace';panel.querySelectorAll('[data-trace-node]').forEach((n,j)=>n.dataset.active=String(j<=i));}});const b=panel.querySelector('[data-preview-play]');b.hidden=false;b.addEventListener('click',()=>panel.dataset.running==='true'?replay.pause():replay.play());});
})(globalThis);
