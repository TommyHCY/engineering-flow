# 本地配置

此配置由 Agent 透過 `resolve_config.py` 讀取，使用 Python 3.9 以上標準函式庫，不需安裝套件。它不會執行配置內的命令、讀取憑證或呼叫外部服務。

## 開始使用

複製 `engineering-flow.example.json` 為目標專案根目錄的 `engineering-flow.local.json`，填入公司、框架與工具資料。若希望跨專案共用，可放在使用者家目錄的 `.config/engineering-flow/config.json`，並列出適用的 repo。

```text
python /path/to/engineering-flow/resolve_config.py --root /path/to/project --repository example/service
python /path/to/engineering-flow/resolve_config.py --root /path/to/project --repository example/service --config /path/to/private/config.json
```

Windows 可使用 `C:/path/to/project`。路徑包含空白時加上引號。

## 載入順序

只選一份配置，不跨檔案合併，優先順序如下：

1. `--config` 指定的路徑。
2. `ENGINEERING_FLOW_CONFIG` 環境變數。
3. `--root` 下的 `engineering-flow.local.json`。
4. 使用者家目錄的 `.config/engineering-flow/config.json`。
5. 都沒有則使用通用預設。

明確指定的相對路徑以 `--root` 為基準；`~` 展開為使用者家目錄。檔案內的 `context.rules_file` 以配置檔所在目錄為基準，可使用絕對路徑。讀取器只解析此路徑，由 Agent 在需要時讀取。

選定檔案不存在、無法讀取、JSON 無效、重複鍵、版本不支援、未知欄位或型別錯誤時，退出碼為 `2`，不退回另一份設定。錯誤訊息不輸出欄位內容。無關的本機調查仍可繼續。

## 欄位契約

| 欄位 | 型別與用途 | 未提供時 |
|---|---|---|
| `version` | 必填整數 `1` | 報錯 |
| `context.organization` | 公司或團隊名稱字串 | 空字串 |
| `context.repositories` | 精確的 `owner/repository` 字串陣列，不支援萬用字元 | 空陣列；不套用 |
| `context.frameworks` | 框架名稱字串陣列 | 空陣列 |
| `context.services` | 服務名稱字串陣列 | 空陣列 |
| `context.rules_file` | 本地補充規則檔路徑字串 | 空字串 |
| `tools.tracker` | 外部問題追蹤 Skill 名稱 | 空字串；不啟用 |
| `tools.logs` | 日誌調查 Skill 名稱 | 空字串；不啟用 |
| `tools.ci` | CI 調查 Skill 名稱 | 空字串；不啟用 |
| `tools.issue_conventions` | Issue 慣例 Skill 名稱 | 空字串；使用通用規則 |
| `logs.environments` | 環境名稱對應物件，每筆必須包含非空字串 `profile`、`index`、`trace_field` | 空物件 |
| `workflows` | 工作流名稱對應 Skill 字串，可用空字串停用綁定 | 通用 `mattpocock-skills` 綁定 |
| `verification` | 驗證規則陣列，每筆包含非空字串陣列 `patterns`、`command` | 空陣列 |

`workflows` 的合法名稱為 `diagnosing-bugs`、`codebase-design`、`research`、`tdd`、`code-review`、`resolving-merge-conflicts`、`domain-modeling`、`prototype`、`grilling`、`writing-for-agents`。

選定配置中省略的欄位會補上預設；物件依欄位補值，陣列完整取代。`logs.environments` 不額外補入任何環境。空字串可清除選用 Skill；`null` 不合法。

## 適用範圍與執行

Agent 先從使用者與實際 remote 確認目標，再傳入 `--repository`。只有精確命中 `context.repositories` 才套用配置；未提供或未命中則回傳 `generic`，不輸出該公司的資料。不要由公司名稱、資料夾名或框架關鍵字推定適用範圍。

框架規則、專用查詢時間窗、報表規則與跨服務資料鏈可寫在 `team-rules.local.md`，再由 `context.rules_file` 指向它。需要的規則檔或工具缺失時，說明受限的步驟，保留獨立工作；不猜測替代索引。

CI 診斷若已配置 `tools.ci`，載入該 Skill 讀取對應版本的建置證據。日誌環境由問題證據決定，查詢時間窗由使用者或已確認事件時間決定；配置中的索引與 trace 欄位仍需現場驗證。

驗證規則範例：

```json
{"patterns": ["*.py"], "command": ["python", "-m", "unittest", "discover"]}
```

`patterns` 使用 Python `fnmatch.fnmatchcase` 語意，對 `/` 分隔的 repo 相對路徑比對；`*` 可跨 `/`。任一修改路徑命中任一 pattern 即需該驗證。Agent 必須先檢查命令與範圍，再以參數陣列從目標根目錄執行；不得把字串拼接為 shell 指令。配置只描述驗證，讀取器不執行。空規則也不免除 repo 本身要求的測試。

## 私密資料與更新

本 repo 已忽略 `engineering-flow.local.json`、`*.local.json`、`*.local.md` 與 `.local/`。若配置放在其他專案，需在該專案的 `.git/info/exclude` 加入相同本地路徑，並用 `git check-ignore` 確認。已追蹤的檔案不會因 ignore 自動移除。

不要把 Token、密碼或 Cookie 寫入配置。只指定工具名稱與其非機密 profile；憑證沿用工具既有的安全儲存方式。解析輸出可能有公司與內部索引，僅供本機使用，不要直接貼入 Issue 或上傳。發布時只包含 example 範本，不包含本地設定與規則。

更新 Skill 時保留本地檔案。移轉既有設定時，將原公司與服務資料填入 context、外部工具填入 tools、環境與索引填入 logs，其餘團隊規則放入 rules_file；重新執行配置驗證後才使用。
