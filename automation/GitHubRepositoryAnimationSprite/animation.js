const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const card=(title,body,meta='',cls='')=>`<article class="card searchable ${cls}" data-search="${esc(title+' '+body+' '+meta)}"><h3>${esc(title)}</h3><p>${esc(body)}</p><small>${meta}</small></article>`;
async function boot(){
 const d=await fetch('./animation-data.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('animation-data '+r.status);return r.json()});
 $('#repo').textContent=d.metrics.repositories;$('#branch').textContent=d.metrics.branches;$('#external').textContent=d.metrics.external_content_changes;$('#asset').textContent=d.metrics.visual_assets;
 $('#changeCards').innerHTML=card(d.change.original_message,d.change.summary_zh_tw,`Commit ${d.change.commit_sha}<br>Path ${esc(d.change.path)}<br>Blob ${d.change.blob_sha}<br>Workflow ${esc(d.change.workflow)}<br>風險 ${esc(d.change.risk)}<br>回退 ${d.change.rollback_commit}`);
 $('#repoCards').innerHTML=d.repository_heads.map(r=>card(r.repository,r.path,`Commit ${r.head}<br>Blob ${r.blob_sha}`)).join('');
 $('#assetCards').innerHTML=`<article class="card"><h3>素材基線</h3><p>SVG 3／HTML 20／JPEG 2</p><small>正式 Snapshot Blob 33155c2024203659fb25156b51c07b0ef3c23be0</small></article>`;
 $('#stepCards').innerHTML=d.steps.map(s=>card(`${s.id}｜${s.name}`,s.status,'',s.status==='錯誤'?'bad':'ok')).join('');
 $('#errorCards').innerHTML=d.tool_gaps.map(e=>card(`錯誤｜${e.item}`,e.evidence,`A：${esc(e.repair_a)}<br>B：${esc(e.repair_b)}`,'bad')).join('');
 $('#q').oninput=e=>{const q=e.target.value.toLowerCase();$$('.searchable').forEach(x=>x.hidden=!x.dataset.search.toLowerCase().includes(q))};
}
function show(id){$$('.view').forEach(v=>v.hidden=v.id!==id);$$('[data-v]').forEach(b=>b.classList.toggle('on',b.dataset.v===id))}
$$('[data-v]').forEach(b=>b.onclick=()=>show(b.dataset.v));show('overview');boot().catch(e=>{$('#state').innerHTML='<b>錯誤</b>｜'+esc(e.message)});
