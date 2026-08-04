const DATA_URL='./animation-data.json';
async function boot(){
 const d=await fetch(DATA_URL).then(r=>r.json());
 for(const [id,key] of [['repoCount','repository_count'],['commitCount','new_commit_count'],['pathCount','final_path_count'],['riskCount','risk_count']]) document.getElementById(id).textContent=d[key];
 const risks=document.getElementById('risks');
 d.risks.forEach(r=>{const b=document.createElement('button');b.innerHTML=`<b>${r.id}｜${r.level}｜${r.title}</b><small>${r.evidence}</small>`;b.onclick=()=>document.getElementById('detail').innerHTML=`<h3>${r.title}</h3><p><b>證據：</b>${r.evidence}</p><p><b>影響：</b>${r.impact}</p><p><b>修復：</b>${r.repair}</p>`;risks.appendChild(b);});
 const steps=document.getElementById('steps');
 d.eleven_actions.forEach(s=>{const b=document.createElement('button');b.textContent=`S${s.index} ${s.name}｜${s.status}`;steps.appendChild(b);});
}
boot();