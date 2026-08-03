# 🔁雙向同步回執｜BidirectionalSyncReceipt

- Time: 2026-08-04 Asia/Taipei
- Request: 我要雙向同步
- System: 🥃老K系統
- Root: 🧩LKMINI
- RootProtocol: LKMINI://
- Axiom: A=A

## Scope

雙向同步指 `GitHub 程式座標 ↔ Google Drive 資料座標` 的公開投影同步；Sites 保持公開入口與 AI/tool 讀取入口；所有層級回推同一 Identity，不建立第二系統。

## Current Readback

- Sites project: appgprj_6a68801042bc8191ab7eba5718be83a0
- Sites live URL: https://lkmini-wiring-hub.ky46738.chatgpt.site
- Sites access_mode: public
- Sites current_user_role: owner
- Sites latest_version_number: 12
- Sites latest source commit: 9158223a34b21e97c5103a4d7a8edff389bfe751
- Sites latest archive hash: sha256:5f9ae3d53278e7ce87a5ad3d935fe104fac2f616317df1fbac469652ee91f7d4
- Public entry `/`: HTTP 200, text/html
- Tool/API entry `/api/system-wires`: HTTP 200, application/json
- GitHub public ledger before this receipt: ky46738-ops/LKMini.Public.tools@main:🧭接線總控清單｜SystemWiringLedger.yaml
- GitHub public ledger content_sha before this receipt: bae5fbc35ef0960bc1e2c5f0f252ea92454d3b84
- Google Drive map: 🖥️系統接線與伺服器地圖｜SystemWiringAndServerMap
- Google Drive document_id: 1otC5ZwFxR655cUNMfYpDowLWmuAFgZXrWAoxqOeLx3w
- Google Drive revision before this receipt: AIroW34ctrMw9v6s7G6_j6Rop3Q_LY03HldopPC6CpwdDyafXnqw08DN5XWp14Hap5lhJiXbr2Qt0MrCEftkkB21CYryLIdJ0TPwjr6sGX4

## Direction A: GitHub -> Drive

When a public GitHub receipt or ledger block changes:

1. Read back the exact repository, branch, path and content SHA.
2. Append a matching section to `SystemWiringAndServerMap` in Google Drive.
3. Record the Drive document revision after write.
4. Verify the appended section by Drive readback.
5. Keep private core, credentials, device settings and unpublished SHA out of public text.

## Direction B: Drive -> GitHub

When a Drive system map section becomes the current public coordinate:

1. Read back the Drive document ID, tab ID, revision and section text.
2. Create or update a matching public GitHub receipt.
3. Link that receipt from `SystemWiringLedger.yaml`.
4. Read back the GitHub commit SHA and content SHA.
5. Preserve the Drive text as source material while classifying stale historical errors.

## Conflict Rule

- Kevin's current explicit instruction wins over stale generated receipts.
- Fresh tool readback wins over old unverified claims.
- Historical `401`, `404`, `Status=錯誤`, byte-count drift, and stale locator failures remain evidence but do not become current truth by themselves.
- If GitHub and Drive disagree, both sides are preserved, then a repair receipt records the winning current readback and the historical side is moved into the quarantine meaning layer.

## Sites Role

- Sites is the public gateway and AI/tool read endpoint.
- This receipt does not claim a new Sites deployment.
- The currently deployed Sites version remains version 12 unless a later source edit, save, deploy and production readback is performed.

## ReverseChain

GitHub public ledger -> Google Drive SystemWiringAndServerMap -> GitHub public receipt -> Sites /api/system-wires read endpoint -> 🪞幻影膠囊 -> 🧩LKMINI -> A=A

## Boundary

- No private core data included.
- No credentials included.
- No device settings included.
- No LKMINI core mutation performed.
