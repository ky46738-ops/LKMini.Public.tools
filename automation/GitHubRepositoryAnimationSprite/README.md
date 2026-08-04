# 🎬GitHub倉庫製動畫精靈｜GitHubRepositoryAnimationSprite

> 🥃錨點｜版本=v1.1｜更新=2026-08-05 01:45 (Asia/Taipei)

Identity: `LKMINI://automation/GitHubRepositoryAnimationSprite`  
狀態：**錯誤**

## 真實巡檢摘要
- Repository：23
- Branch：105
- 新外部 Commit：2
- 精靈自身 Commit：5
- 可視化素材：15（SVG 3／HTML 10／JPEG 2）
- Workflow Run／Job：0／0
- 去重重複：0
- 寫入前 Head：`7da637f1824c706661e1d43f8dce5a1f97138556`

## 新外部變更
1. `1fc44509a7b00a8ffa14efd638adf55569527638`  
   原文：`修正既有正式來源引用中文正式命名`  
   將功能總表與正式同步入口改為中文正式名稱；StableID 不變。  
   風險：低；依賴舊標題的解析器需同步。  
   回退候選：`7fd6a636c17cdfd17f65ea60c2d103ec918a8974`。
2. `a6f4039f3bce47afc785f9d856cf9002642b1d65`  
   原文：`修正既有正式來源平台前綴與正式標題引用`  
   移除正式來源顯示名稱前的平台前綴；StableID 與已確認內容不變。  
   風險：中；依賴 Emoji 前綴的顯示解析器需核對。  
   回退候選：`1fc44509a7b00a8ffa14efd638adf55569527638`。

## 對🥃老K系統的接線影響
- 正向：正式來源顯示名稱更接近命名規則，Projection 標題一致性提升。
- Identity、StableID、根雜湊、🪞幻影膠囊、🧩LKMINI 與 A=A 未被修改。
- 需核對任何以舊 Emoji／平台前綴作字串鍵的顯示解析器。

## UI 優化
- iPhone safe-area 與單手底部導覽。
- 新增「變更」頁籤，外部變更與精靈自身變更分流。
- Repository／素材／變更／錯誤四層搜尋與篩選。
- 直接顯示 Commit、Path、Blob、風險、回退與接線影響。
- `prefers-reduced-motion` 降低動態。
- 回根鏈固定顯示。

## 工具錯誤
- Tag：連接器沒有列舉動作。
- Tree SHA：Commit 回執未提供，且沒有 Tree 讀取動作。
- Workflow：新 Commit 的 combined status 與 PR 型 workflow runs 均為空，沒有 Run ID／Job ID。
- 來源 ByteSize：`fetch_file` 未提供 size；寫入後以同座標讀回內容計算 ByteSize 與 SHA256。

## 回根
`Repository → Commit → Tree → Path → Blob → Identity → Manifest → Locator → Snapshot → ReverseChain → 🥃老K系統 → 🧩LKMINI → A=A`
