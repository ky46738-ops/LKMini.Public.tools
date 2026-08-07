"use strict";
const setText=(selector,value)=>{const node=document.querySelector(selector);if(node)node.textContent=String(value);};
async function boot(){
  const response=await fetch("./animation-data.json",{cache:"no-store"});
  if(!response.ok)throw new Error("animation-data "+response.status);
  const data=await response.json();
  setText("#state",data.status+"｜"+data.edition+"｜端點缺口 "+data.metrics.current_errors);
  setText("#repo-count",data.metrics.repositories);
  setText("#branch-count",data.metrics.branches);
  setText("#change-count",data.metrics.changed_repositories);
  setText("#workflow-count",data.metrics.workflow_definitions);
  setText("#gate-count",data.current.mirror_gate_status);
  setText("#source-sha-count",data.metrics.source_hashes_verified+"/7");
  setText("#error-count",data.metrics.current_errors);
  setText("#notify-count",data.metrics.external_notifications);
  setText("#writeback",data.current.writeback);
  setText("#captured-at","巡檢快照："+data.captured_at+"｜永久刪除 0");
  const projection=document.querySelector("#projection");projection.href=data.current.web_projection;
  const commit=document.querySelector("#canonical-commit");commit.href=data.current.canonical_commit_url;commit.querySelector("code").textContent=data.current.canonical_commit.slice(0,12)+"…";
  const changes=document.querySelector("#changes");
  data.changes.forEach(item=>{const row=document.createElement("div");row.className="change";const link=document.createElement("a");link.href="https://github.com/"+item.repository+"/commit/"+item.commit;link.textContent=item.repository+" @ "+item.commit.slice(0,8);const detail=document.createElement("small");detail.textContent="｜"+item.message+"｜"+item.path;row.append(link,detail);changes.append(row);});
}
boot().catch(error=>setText("#state","錯誤｜"+error.message));
