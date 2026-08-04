const DATA_URL = './animation-data.json';
async function boot() {
  const data = await fetch(DATA_URL).then(r => r.json());
  document.querySelector('#repoCount').textContent = data.repository_count;
  document.querySelector('#changeCount').textContent = data.external_change_count;
  const list = document.querySelector('#scenes');
  data.scenes.forEach((scene, index) => {
    const item = document.createElement('button');
    item.className = 'scene';
    item.innerHTML = `<span>${index}</span><b>${scene.title}</b><small>${scene.value}</small>`;
    item.onclick = () => {
      document.querySelectorAll('.scene').forEach(x => x.classList.remove('active'));
      item.classList.add('active');
      document.querySelector('#detail').textContent = `${scene.title}｜${scene.value}`;
    };
    list.appendChild(item);
  });
  list.firstElementChild?.click();
}
boot();
