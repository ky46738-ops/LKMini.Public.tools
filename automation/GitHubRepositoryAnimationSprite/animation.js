const data=window.ANIMATION_DATA;
const stage=document.querySelector('#stage'),progress=document.querySelector('#progress'),caption=document.querySelector('#caption');
let current=0,timer;
function esc(v){return v.replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}
function render(i){const s=data.scenes[i];stage.innerHTML=`<article class="repo-card"><div class="eyebrow">Scene ${String(i+1).padStart(2,'0')} / ${data.scenes.length}</div><h2>${esc(s.repo)}</h2><div class="chain"><span>Repository</span><b>→</b><span>${esc(s.branch)}</span><b>→</b><span>${s.commit.slice(0,8)}</span><b>→</b><span class="path">${esc(s.path)}</span><b>→</b><span>${s.blob.slice(0,8)}</span></div><p>${esc(s.summary)}</p><small>${esc(s.change)}｜${esc(s.workflow)}</small></article>`;caption.textContent=s.summary;progress.style.width=`${((i+1)/data.scenes.length)*100}%`;}
function play(){clearInterval(timer);render(current);timer=setInterval(()=>{current=(current+1)%data.scenes.length;render(current)},6500);}
document.querySelector('#prev').onclick=()=>{current=(current-1+data.scenes.length)%data.scenes.length;render(current)};
document.querySelector('#next').onclick=()=>{current=(current+1)%data.scenes.length;render(current)};
document.querySelector('#play').onclick=play;document.querySelector('#pause').onclick=()=>clearInterval(timer);play();
