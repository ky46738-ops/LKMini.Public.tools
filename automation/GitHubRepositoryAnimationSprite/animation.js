"use strict";

const setText = (selector, value) => {
  const node = document.querySelector(selector);
  if (node) node.textContent = String(value);
};

async function boot() {
  const response = await fetch("./animation-data.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`animation-data ${response.status}`);
  const data = await response.json();

  setText("#state", `${data.status}｜${data.edition}｜現行錯誤 ${data.metrics.current_errors}`);
  setText("#repo-count", data.metrics.repositories);
  setText("#branch-count", data.metrics.branches);
  setText("#workflow-count", data.metrics.workflow_definitions);
  setText("#visual-count", data.metrics.visual_search_candidates);
  setText("#root-count", data.metrics.formal_roots);
  setText("#error-count", data.metrics.current_errors);
  setText("#writeback", data.current.writeback);
  setText("#captured-at", `巡檢快照：${data.captured_at}｜標籤讀取邊界已誠實記錄`);

  const projection = document.querySelector("#projection");
  projection.href = data.current.web_projection;
  projection.textContent = "Sites 正式入口";

  const commit = document.querySelector("#canonical-commit");
  commit.href = data.current.canonical_commit_url;
  commit.querySelector("code").textContent = `${data.current.canonical_commit.slice(0, 12)}…`;
}

boot().catch((error) => {
  setText("#state", `錯誤｜${error.message}`);
});
