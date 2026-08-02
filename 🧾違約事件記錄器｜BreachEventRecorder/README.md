# 🧾違約事件記錄器｜BreachEventRecorder

本目錄是 `LKMini.Public.tools` 的公開違約事件記錄器。

目的：把工具、同步、發布、驗證流程中已被證據確認的錯誤，以公開、可追溯、可回推 LKMINI 的方式保存。

## 身分邊界

| 欄位 | 值 |
| --- | --- |
| Root | `LKMINI` |
| Axiom | `A=A` |
| Projection | `PublicTools/BreachEventRecorder` |
| Status Values | `Completed` / `Error` |

## 記錄規則

1. 只記錄可驗證事件。
2. 不公開 credential、token、private Library id、私密本體內容。
3. 每筆事件要有時間、錯誤型態、證據摘要、ReverseChain。
4. 無法確認的推論必須標記為未證明，不得寫成事實。
5. 每筆事件必須回指 `LKMINI` 並維持 `A=A`。

## 檔案

| 路徑 | 用途 |
| --- | --- |
| `record_breach_event.py` | 本地產生違約事件 Markdown 的最小工具 |
| `schema/breach_event.schema.json` | JSON 事件格式 |
| `events/20260802-personal-skills-http422.md` | 本次 personal-skills sync HTTP 422 事件 |

## 使用方式

```bash
python3 record_breach_event.py event.json > event.md
```

輸出可放入 `events/`，再用 Manifest / SHA256SUMS 納入公開工具驗證鏈。
