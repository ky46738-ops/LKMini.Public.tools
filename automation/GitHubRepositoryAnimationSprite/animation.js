const DATA_URL='./animation-data.json';
async function boot(){
 const d=await fetch(DATA_URL).then(r=>r.json());
 document.querySelector('#repoCount').textContent=d.repository_count;
 document.querySelector('#changeCount').textContent=d.external_change_count;
 document.querySelector('#riskCount').textContent=d.risk_count;
 const list=document.querySelector('#changes');
 d.changes.forEach((c,i)=>{
  const el=document.createElement('button');
  el.className='change';
  el.innerHTML=`<b>${i+1}. ${c.repository}</b><span>${c.original_message}</span><small>${c.summary}</small>`;
  el.onclick=()=>document.querySelector('#detail').innerHTML=
   `<h3>${c.path}</h3><p><b>Commit</b> ${c.commit_sha}</p><p><b>Blob</b> ${c.blob_sha}</p><p><b>風險</b> ${c.risk}</p><p><b>回退</b> ${c.rollback_commit}</p><p><b>接線</b> ${c.wiring_impact}</p>`;
  list.appendChild(el);
 });
 const steps=document.querySelector('#steps');
 d.eleven_actions.forEach(s=>{const b=document.createElement('button');b.textContent=`S${s.index} ${s.name}｜${s.status}`;steps.appendChild(b);});
}
boot();