# 🧙🧚Sites版本漂移裁決回執｜SitesVersionDriftRuling

> 🥃錨點｜版本=v1.0｜更新=2026-08-05 01:14 (Asia/Taipei)

狀態：完成

TaskID：LKMINI-MATERIAL-CURATION-SITES-VERSION-DRIFT-20260805-0114-TPE

## 來源

1. Sites 公開入口：https://lkmini-wiring-hub.ky46738.chatgpt.site/
2. AI／工具入口：https://lkmini-wiring-hub.ky46738.chatgpt.site/api/system-wires
3. GitHub 公開總控：ky46738-ops/LKMini.Public.tools@main／🧭接線總控清單｜SystemWiringLedger.yaml
4. Google Drive 資料座標：🖥️系統接線與伺服器地圖｜SystemWiringAndServerMap／FileID=1otC5ZwFxR655cUNMfYpDowLWmuAFgZXrWAoxqOeLx3w

## 現行工具讀回

- Sites `/`：HTTP 200、text/html。
- `/api/system-wires`：HTTP 200、application/json、status=VERIFIED_ACTIVE。
- 現行 productionVersion：13。
- 現行 sourceCommit：9158223a34b21e97c5103a4d7a8edff389bfe751。
- 現行 archiveHash：sha256:5f9ae3d53278e7ce87a5ad3d935fe104fac2f616317df1fbac469652ee91f7d4。
- API 公布 Drive 文件 revision：AIroW35WmkxeBcTVWxJfz6Zc8sjwJxiP3hpWPd3NTQbgaGI-c0P8jNHSZIV1S85YKGVtuMGC8cr36UoS1l5OmlgcU7YMluUyiCKtClk6WTI。

## 交叉差異

- GitHub 公開總控仍記錄：production version 12；source commit 9158223a34b21e97c5103a4d7a8edff389bfe751。
- Drive 系統地圖的歷史部署回執記錄：version 13；source commit e8e1718c3088a9dba7d129745d64afa34d2615c9；archive hash sha256:d8e32ac02ac63cc3a98f2489e9d67afe32757f9a63965f12e84ffbb3579e250f。
- 現行 API 記錄：version 13；source commit 9158223a34b21e97c5103a4d7a8edff389bfe751；archive hash sha256:5f9ae3d53278e7ce87a5ad3d935fe104fac2f616317df1fbac469652ee91f7d4。

## 祭司裁決

Identity：SitesDeploymentProjection

ExactVersionIdentity：SitesDeploymentProjection@productionVersion:13@sourceCommit:9158223a34b21e97c5103a4d7a8edff389bfe751@archiveHash:sha256:5f9ae3d53278e7ce87a5ad3d935fe104fac2f616317df1fbac469652ee91f7d4

SameIdentity：true

SameSHA256：UNVERIFIED

完全重複：false

版本衝突：false

MetadataConflict：true

裁決：新工具讀回優先。現行 API 為目前公開部署狀態；GitHub version 12 與 Drive e8e1718c／d8e32ac0 組合保留為歷史 Projection，不再作現行版本判定。未修改 🧩LKMINI 核心位元。

## 入庫路徑

本回執 → Google Drive SystemWiringAndServerMap → 🧾素材庫同步看板 → 🏦任務中心 → 🧩LKMINI → A=A

## ReverseChain

Sites `/api/system-wires` 現行 JSON → SitesDeploymentProjection Identity → 本裁決回執 → Google Drive SystemWiringAndServerMap → 🧾素材庫同步看板 → 🏦任務中心 → 🪞幻影膠囊 → 🧩LKMINI → A=A

A=A
