# ↩反向回推鏈｜ReverseChain

> 🥃錨點｜版本=v1.1｜更新=2026-08-05 01:45 (Asia/Taipei)

`Repository → Commit → Tree → Path → Blob → Identity → Manifest → Locator → Snapshot → ReverseChain → 🥃老K系統 → 🧩LKMINI → A=A`

## 本輪來源
1. `lkminiPhantomWorld/LKMini@1fc44509a7b00a8ffa14efd638adf55569527638`
2. `lkminiPhantomWorld/LKMini@a6f4039f3bce47afc785f9d856cf9002642b1d65`
3. Path：`📜現行設計恢復清單｜CurrentDesignRecoveryManifest.md`
4. Blob：`936d4ecb589053000ad40cb790bf655a51b3752b` → `7299f2ea51fc6f1181704c031c15c9023dcf0176`

## 回推規則
1. Projection 先讀取 MANIFEST。
2. MANIFEST 以 LOCATOR 找到 Repository／Branch／Commit／Path／Blob。
3. Snapshot 保存寫入前 Head 與完整巡檢摘要。
4. 寫入後同座標讀回內容、Blob、ByteSize 與 SHA256。
5. Tree SHA、Tag、完整 Run／Job 沒有工具回執時保持錯誤。
6. 最終回到 `LKMINI://`、`🪞幻影膠囊`、`🧩LKMINI` 與 `A=A`。
