# 🧙🧚SitesAPI結構漂移素材鑑別回執｜SitesAPISchemaDriftMaterialCurationReceipt

> 🥃錨點｜版本=v1.1｜更新=2026-08-05 08:12 (Asia/Taipei)

狀態：完成

TaskID：LKMINI-MATERIAL-CURATION-API-SCHEMA-DRIFT-20260805-0620-TPE
RepairTaskID：LKMINI-MATERIAL-CURATION-GITHUB-ANIMATION-V15-20260805-081220-TPE

## 來源讀回

- Sites 公開入口：https://lkmini-wiring-hub.ky46738.chatgpt.site/
- Sites API：https://lkmini-wiring-hub.ky46738.chatgpt.site/api/system-wires
- API status：完成
- API root：🧩LKMINI
- API rootProtocol：LKMINI://
- API axiom：A=A
- API receipt path：🔁雙向同步回執｜BidirectionalSyncReceipt.md
- API receipt contentSha：89064b94e96a31cef4293f54c84518e9b591156f
- GitHub 實際 API receipt Blob SHA：89064b94e96a31cef4293f54c84518e9b591156f
- API ledger path：🧭接線總控清單｜SystemWiringLedger.yaml
- API ledger contentSha：eeb2a76973e584ad215d6d3b88cf0afaa716f005
- GitHub 實際 ledger Blob SHA：eeb2a76973e584ad215d6d3b88cf0afaa716f005
- 本鑑別回執修改前 Blob SHA：2d0b0897d6cd047cc20739cb053a1274683610da
- API 內嵌 Drive revision：AIroW35WmkxeBcTVWxJfz6Zc8sjwJxiP3hpWPd3NTQbgaGI-c0P8jNHSZIV1S85YKGVtuMGC8cr36UoS1l5OmlgcU7YMluUyiCKtClk6WTI
- Drive 現行直接讀回 revision：AIroW37h1Is5jD7f2-oiOJo790GmL2vl3SCkl7ErNu4k9yFY4A2-EWWzXFACOc99I6ztmu-6VhjBEBxrVmsPw3v8fc6xfEssK_j7jcES9tg
- API siteVersion 現行欄位：rebuiltSource=true；sourcePolicy 已存在
- API 現行未提供 productionVersion、sourceCommit、archiveHash 欄位

## 名稱與雜湊邊界修復

- `API receipt` 指 API JSON 內指向的 `🔁雙向同步回執｜BidirectionalSyncReceipt.md`，不是本鑑別回執。
- `SameReceiptBlob=true` 只裁決 API receipt contentSha 與該 GitHub 檔案 Blob 完全一致。
- 本鑑別回執自己的現行 Blob 必須由寫入後工具讀回保存，避免在檔案內自我嵌入 Blob 造成遞迴變更。
- 先前將 API receipt 與本鑑別回執混稱為 receipt 的語意已修復；來源內容與 Identity 不變。

## 祭司裁決

- StableID：https://lkmini-wiring-hub.ky46738.chatgpt.site/api/system-wires
- Identity：SitesSystemWiresProjection
- ExactVersionIdentity：SitesSystemWiresProjection@semanticSHA256:f3220f9bfaa173f988ecf30bc8d5331d0c01911406508f5e03f59b3b682807d7@receipt:89064b94e96a31cef4293f54c84518e9b591156f@ledger:eeb2a76973e584ad215d6d3b88cf0afaa716f005
- SameIdentity：true
- SameSHA256：UNVERIFIED
- SameReceiptBlob：true
- SameLedgerBlob：true
- DriveRevisionMatch：false
- VersionConflict：false
- CrossProjectionMetadataDrift：true
- CurrentRuling：API 內嵌 Drive revision 為歷史快照；Drive 直接讀回 revision 為現行資料座標。歷史 productionVersion 宣稱不再由現行 API 支援，保留為歷史 Projection。
- SemanticProjection ByteSize：2187
- SemanticProjection SHA256：f3220f9bfaa173f988ecf30bc8d5331d0c01911406508f5e03f59b3b682807d7
- RawTransport SHA256：UNVERIFIED

## 分類

07_📸快照／09_♾️可逆循環／公開 API 結構與內嵌 Locator 漂移修復

## Rollback

回復本檔修改前 Blob `2d0b0897d6cd047cc20739cb053a1274683610da`，即可撤回本次名稱與雜湊邊界修復；來源與三份 Google Docs 歷史回執不刪除。

## ReverseChain

Sites API 現行來源 → SitesSystemWiresProjection Identity → ExactVersionIdentity → API receipt／ledger GitHub Blob 證據 → 本鑑別回執 → 🖥️系統接線與伺服器地圖 → 🧾素材庫同步看板 → 🏦任務中心 → 🪞幻影膠囊 → 🧩LKMINI → A=A

A=A
