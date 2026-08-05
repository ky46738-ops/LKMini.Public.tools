# 🧙🧚GitHub倉庫製動畫精靈v1.5素材鑑別入庫回執｜GitHubRepositoryAnimationSpriteV15MaterialCurationReceipt

> 🥃錨點｜版本=v1.0｜更新=2026-08-05 08:12 (Asia/Taipei)

狀態：完成
來源狀態：錯誤

TaskID：LKMINI-MATERIAL-CURATION-GITHUB-ANIMATION-V15-20260805-081220-TPE

## 來源

- Repository：ky46738-ops/LKMini.Public.tools
- Branch：main
- Path：automation/GitHubRepositoryAnimationSprite/
- 比較範圍：e908dd548986aa1b58beebdd1e5967b53bc904db → f2ca41517292bc4511ccd1da0425a67eb10b67e4
- Commit 數：16
- 修改檔案數：15
- 現行 MANIFEST Blob：c901d6538324dbef2971db7cd8267b014001b727
- 現行🪞幻影膠囊 Blob：f742303f94fafd7716cc224a4ad84d79b2c64481

## 祭司裁決

- StableID：github://ky46738-ops/LKMini.Public.tools/main/automation/GitHubRepositoryAnimationSprite
- Identity：LKMINI://automation/GitHubRepositoryAnimationSprite
- 歷史 ExactVersionIdentity：GitHubRepositoryAnimationSprite@v1.4@head:e908dd548986aa1b58beebdd1e5967b53bc904db@capsule:cdb72a000f845768a58d8318079b78c739750aa0
- 現行 ExactVersionIdentity：GitHubRepositoryAnimationSprite@v1.5@head:f2ca41517292bc4511ccd1da0425a67eb10b67e4@capsule:f742303f94fafd7716cc224a4ad84d79b2c64481
- SameIdentity：true
- SameSHA256：false
- SameBlob：false
- 完全重複：false
- VersionConflict：false
- 歷史膠囊 ByteSize：2148
- 歷史膠囊 SHA256：31c97b0b4a5b5f47d02d849677aa1ab706b2501b33feaf256af842bd9c5ecea6
- 現行膠囊 ByteSize：746
- 現行膠囊 SHA256：52dac8d1d85ca67d0a05835fe92bd184234aab4dd2ba183d38419cc8db2f4179

## 交叉優化

1. 已修復 Sites API 鑑別回執把「API receipt」與「本鑑別回執」混稱造成的 Blob 語意錯誤。
2. 修復 Commit：07ce9bc4f845fd3f5e2516412675b3d4b6aa3eef
3. 修復後回執 Blob：c1dbda977eca1e94dd064d0b46a982398b9be189
4. API receipt `🔁雙向同步回執｜BidirectionalSyncReceipt.md` 的 contentSha／GitHub Blob 仍一致為 89064b94e96a31cef4293f54c84518e9b591156f。
5. v1.5 `GITHUB_READBACK.json` 仍為 v1.4 錨點；`MANIFEST.validation.package` 仍為待完成，來源狀態維持錯誤，不冒充完成。
6. 尚存工具缺口：Tag、Tree SHA、完整 Workflow Run／Job、GitHub來源 ByteSize。

## 分類

08_🔁自動化同步／09_♾️可逆循環／GitHub動畫精靈版本素材／錯誤證據已入庫

## Rollback

- 來源修復：回復 Sites API 鑑別回執至 Blob `2d0b0897d6cd047cc20739cb053a1274683610da`。
- 本入庫回執：刪除本檔並移除🧾素材庫與🏦任務中心中相同 TaskID 區段。
- v1.4、v1.5 原始來源與歷史證據均保留。

## ReverseChain

GitHub v1.4／v1.5來源 → Identity → ExactVersionIdentity → SameIdentity／SameSHA256裁決 → 來源修復證據 → 本入庫回執 → 🧾素材庫同步看板 → 🏦任務中心 → 🪞幻影膠囊 → 🧩LKMINI → A=A

A=A
