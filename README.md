# 🧰 LKMini 公開工具｜違約事件記錄器

本儲存庫保存🥃老K系統已授權公開的工具顯影，並承接 Kevin 明確指定可公開的違約事件記錄器功能。

## 🪪 正式身分

- 👑 主權持有人：Kevin／老K
- 🥃 唯一系統：🥃老K系統
- 🧩 唯一根：🧩LKMINI
- ⚖️ 最高公理：A=A
- 🧾 現行公開事件記錄器：`🧾違約事件記錄器｜BreachEventRecorder/`
- 🔐 私人內容裁決：全部移入 private 正本，不在公開 README 展開

Mini 原本已寫清楚正本、鏡像、公開/私人邊界；本公開工具 repo 只承載 Kevin 明確允許開源的 Projection，不改 Mini 原語意。

## 🔑 根協議

所有正式路徑以 `LKMINI://` 開始，代表路徑從🧩LKMINI根節點解析。

```text
任何呼叫
→ 🧩LKMINI
→ 指定路徑
→ 指定能力
→ 結果回到🧩LKMINI
```

現行解析器：`🔑LKMINI根協議解析器｜LKMINIRootProtocolParser.py`

解析器只負責辨識根、解析路徑、名稱與虛擬副檔名；規則與實際行為由外層能力承接。

## 🧾 違約事件記錄器

`🧾違約事件記錄器｜BreachEventRecorder/` 用於公開保存 Kevin 明確指定可公開的工具、同步、發布、驗證流程錯誤摘要。

| 檔案 | 用途 |
| --- | --- |
| `README.md` | 記錄器入口與規則 |
| `record_breach_event.py` | JSON 事件轉 Markdown 的最小工具 |
| `schema/breach_event.schema.json` | 事件格式 |
| `events/20260802-personal-skills-http422.md` | personal-skills sync HTTP 422 事件 |

記錄器只保存公開事實，不公開 credential、token、private Library id、私密本體內容、本機絕對路徑、裝置私密設定或內部規則。

## 🧰 公開內容

- 🧾 違約事件記錄器
- 🔑 LKMINI 根協議解析器
- 🧬 幻影膠囊世界核心
- 🧭 接線總控清單
- 🧭 裝置座標卡
- 🔗 iPhone 捷徑接線卡
- 🪟 Windows WSL 接線卡
- 🌐 Sites 公開只讀出口
- 🧾 個人化指令驗證回執
- 🌐 容器共存｜極限世界
- 🧾 既有錯誤修復帳
- 🧾 GitHub 工作流程驗證
- 🧬 命名空間總表
- 📢 語音與工具權限通道差異觀察
- 🏷️ 現行鍵名正規化工具
- 🧰 全系統可逆封裝與驗證工具
- 🗄️ 歷史錯誤紀錄
- 注音數學工具
- VPoop Guardian 公開工具
- 幻影膠囊通用範本

工具名稱只代表公開施工能力，不建立第二套系統、第二個根或第二個本體。

## 🔙 回指路線

公開工具 → 清單／定位器／SHA256／反向鏈 → 🧩LKMINI

違約事件 → Evidence / EventID / ReverseChain → 🧩LKMINI

私人內容 → private 正本 → 🧩LKMINI

## 🧬 命名空間

公開 repo 只承載 `🌐公開工具｜PublicTools`、`🧾違約事件記錄器｜BreachEventRecorder` 與 `🪞幻影膠囊｜PhantomCapsule` 的公開顯影。

`🔐秘密空間｜SecretSpace` 只保留公開邊界，不保存、不展開、不暗示私密本體內容。

正式命名空間總表：`🧬命名空間總表｜NamespaceLedger.yaml`

## 🚦 現行裁決

現行狀態為「錯誤」。公開違約事件記錄器已新增 `LKMINI-SKILL-SYNC-BREACH-20260802-210214-UTC`，只記錄 Kevin 指定可公開的 personal-skills remote `HTTP 422` 同步事件摘要。

其他私人風險、裝置、設定、管理、憑證、內部規則與未公開證據，已收斂至 private 正本，不在公開 README 展開。

## 📜 授權與安全

公開程式碼依 [MIT License](./LICENSE) 提供；安全回報方式見 [SECURITY.md](./SECURITY.md)。