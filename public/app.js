let currentReport;
const $ = id => document.getElementById(id);
const stringify = value => typeof value === 'string' ? value : JSON.stringify(value);
function render(report) {
  currentReport = report;
  $('verdict').textContent = report.verdict === 'compatible' ? 'Both clients stay compatible.' : 'Hold this rollout.';
  $('score').textContent = `${report.passed}/${report.total}`;
  $('summary').textContent = `Results for: ${report.name}. ${report.description}`;
  $('checks').replaceChildren(...report.checks.map(check => {
    const row = document.createElement('div'); row.className = `check ${check.passed ? 'pass' : 'fail'}`;
    const icon = document.createElement('span'); icon.className = 'icon'; icon.textContent = check.passed ? '✓' : '×';
    const content = document.createElement('div'); const title = document.createElement('b'); title.textContent = check.name;
    const detail = document.createElement('small'); detail.textContent = `${check.skipped ? 'Skipped. ' : ''}Expected: ${stringify(check.expected)} · Actual: ${stringify(check.actual)}`;
    content.append(title, detail); row.append(icon, content); return row;
  }));
  $('actions').hidden = false; $('repair').hidden = !report.repairScenario; $('technical').hidden = false;
  $('trace').textContent = JSON.stringify({operations:report.operations,schema:report.schema,evidenceHash:report.evidenceHash,sourceHash:report.sourceHash,commit:report.commit,pipeline:report.pipeline,runtime:report.runtime,mode:report.mode},null,2);
}
async function run(scenario) {
  $('run').disabled = true; $('repair').disabled = true; $('message').textContent = 'Executing isolated compatibility checks…';
  document.querySelectorAll('input[name=scenario]').forEach(input=>input.disabled=true);
  try {
    const response = await fetch('/api/audit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenario})});
    const report = await response.json(); if (!response.ok) throw new Error(report.error || 'Audit failed'); render(report);
    $('message').textContent = 'Checks completed. Evidence describes this fixture and migration; review your own production requirements separately.';
  } catch(error) { $('message').textContent = error.message; }
  finally { $('run').disabled = false; $('repair').disabled = false; document.querySelectorAll('input[name=scenario]').forEach(input=>input.disabled=false); }
}
$('run').addEventListener('click',()=>run(document.querySelector('input[name=scenario]:checked').value));
$('repair').addEventListener('click',()=>{ const input=document.querySelector(`input[value="${currentReport.repairScenario}"]`); input.checked=true; run(currentReport.repairScenario); });
$('export').addEventListener('click',()=>{ const url=URL.createObjectURL(new Blob([JSON.stringify(currentReport,null,2)],{type:'application/json'})); const link=document.createElement('a');link.href=url;link.download=`releasesteward-${currentReport.scenario}.json`;link.click();URL.revokeObjectURL(url); });
fetch('/api/scenarios').then(response=>{if(!response.ok)throw new Error('Could not load scenarios');return response.json();}).then(data=>{
  $('scenarios').replaceChildren(...data.scenarios.map((item,index)=>{const label=document.createElement('label');label.className='choice';const input=document.createElement('input');input.type='radio';input.name='scenario';input.value=item.id;input.checked=index===0;input.addEventListener('change',()=>{currentReport=null;$('verdict').textContent='Ready to test this migration';$('score').textContent='—';$('summary').textContent='The selected strategy changed. Run the checks to obtain current evidence.';$('checks').replaceChildren();$('actions').hidden=true;$('technical').hidden=true;$('message').textContent='Previous evidence cleared; the selected strategy has not been tested yet.';});const span=document.createElement('span');span.textContent=item.name;const detail=document.createElement('small');detail.textContent=item.description;label.append(input,span,detail);return label;}));$('run').disabled=false;
}).catch(error=>{$('message').textContent=error.message;});
