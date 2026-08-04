# ↩反向回推鏈｜ReverseChain

> 🥃錨點｜版本=v1.0｜更新=2026-08-05 01:28 (Asia/Taipei)

`Repository → Commit → Tree → Path → Blob → Identity → Manifest → Locator → Snapshot → ReverseChain → 🥃老K系統 → 🧩LKMINI → A=A`

## 回推規則
1. Projection 先讀取 MANIFEST。
2. MANIFEST 以 LOCATOR 找到 GitHub Repository／Branch／Path。
3. Path 以 Blob SHA 回到 Commit 與 Repository。
4. Snapshot 保存寫入前狀態；GITHUB_READBACK 保存寫入後證據。
5. 最終回到 `LKMINI://`、`🪞幻影膠囊`、`🧩LKMINI` 與 `A=A`。
