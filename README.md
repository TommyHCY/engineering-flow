# Engineering Flow

通用工程協作 Skill：以 **Issue／Map → 證據 → 決策 → 授權 → 修改 → 驗證 → 審查 → 交付** 串起需求、研究、診斷與實作。

核心流程不綁定公司、框架或內部系統。團隊資料由本地 JSON 與規則檔提供；未配置時直接使用通用流程。

## 保留的流程

- 小而明確的工作使用單一追蹤紀錄；多個未知決策使用 Wayfinding Map。
- 未授權發布 Issue 時，使用本機 Tracking pending 草稿。
- 修改前完成 Implementation-ready：目標、範圍、設計、驗收、驗證、風險六項內容。
- 先查證程式與實際證據，再區分已驗證、推論、尚未確認。
- 依階段選擇一個主要工作流；需要的 Skill 未安裝時明確說明，再採相同方法處理。
- 本地配置與追蹤紀錄都不代表 commit、push、PR 或遠端寫入授權。

## 安裝與配置

將整份 repo 放在工具支援的 Skills 目錄下，資料夾名稱使用 `engineering-flow`。保留 `SKILL.md` 與同層的配置文件、讀取器。若舊版技能仍啟用，請在使用的工具中選定要用的版本，避免重複套用。

複製 `engineering-flow.example.json` 為目標專案根目錄的 `engineering-flow.local.json`，填入適用的 repo、公司、框架、環境與 Skill 綁定。也可使用個人配置路徑或環境變數，詳見 [配置說明](CONFIGURATION.md)。

```text
python /path/to/engineering-flow/resolve_config.py --root /path/to/project --repository example/service
```

輸出 `generic` 表示未套用公司資料；`configured` 表示已載入且精確命中目標。設定檔有錯會報錯，不會默默換用另一份配置。

## 檔案

| 檔案 | 用途 |
|---|---|
| `SKILL.md` | 英文 Agent 工作流程與載入規則 |
| `CONFIGURATION.md` | 繁體中文配置契約與遷移方式 |
| `engineering-flow.example.json` | 可分享的通用配置範本 |
| `resolve_config.py` | Python 標準函式庫配置讀取與驗證 |
| `test_config.py` | 直接相關的配置回歸測試 |
| `evals.json` | 通用化的原有情境與新增配置情境 |

## 驗證

從 repo 根目錄執行：

```text
python -m unittest -v test_config
```

`evals.json` 是供 Agent 情境評估的輸入與預期行為，並非上述單元測試的執行結果。兩者分別驗證流程指令與配置解析，回報時應分開。

## 資料邊界

本地公司設定與內部規則不納入 Git；憑證保留在外部工具既有的安全配置。只提交通用範本。追蹤紀錄只保留最小必要的去敏感摘要；原始附件與完整 log 不發布。公開發布仍需明確授權。
