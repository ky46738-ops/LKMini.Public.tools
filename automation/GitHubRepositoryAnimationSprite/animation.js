"use strict";

async function boot() {
  const response = await fetch("./animation-data.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`animation-data ${response.status}`);
  const data = await response.json();
  document.querySelector("#state").textContent = `${data.status}｜v${data.metrics.sites_version}｜現行錯誤 ${data.metrics.current_errors}`;
  document.querySelector("#root-count").textContent = String(data.metrics.formal_roots);
  document.querySelector("#container-count").textContent = String(data.metrics.formal_containers);
  document.querySelector("#test-count").textContent = `${data.metrics.public_tests_passed}/${data.metrics.public_tests_total}`;
  document.querySelector("#error-count").textContent = String(data.metrics.current_errors);
  document.querySelector("#projection").textContent = data.current.web_projection;
  document.querySelector("#projection").href = data.current.web_projection;
  document.querySelector("#writeback").textContent = data.current.writeback;
}

boot().catch((error) => {
  document.querySelector("#state").textContent = `錯誤｜${error.message}`;
});
