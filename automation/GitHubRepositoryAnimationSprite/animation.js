const DATA_URL='./animation-data.json';
async function boot(){
 const d=await fetch(DATA_URL).then(r=>r.json());
 repoCount.textContent=d.repository_count; changeCount.textContent=d.change_count; sourceCount.textContent=d.external_sources_to_import;
 d.changes.forEach((c,i)=>{const b=document.createElement('button');b.innerHTML=`<b>${i+1}. ${c.original_message}</b><span>${c.path}</span><small>${c.summary}</small>`;b.onclick=()=>detail.innerHTML=`<h3>${c.path}</h3><p><b>Commit</b> ${c.commit_sha}</p><p><b>Blob</b> ${c.blob_sha}</p><p><b>ByteSize</b> ${c.byte_size}</p><p><b>SHA256</b> ${c.sha256}</p><p><b>Workflow</b> ${c.workflow}</p><p><b>風險</b> ${c.risk}</p><p><b>回退</b> ${c.rollback_commit}</p>`;changes.appendChild(b);});
 d.eleven_actions.forEach(s=>{const b=document.createElement('button');b.textContent=`S${s.index} ${s.name}｜${s.status}`;steps.appendChild(b);});
} boot();