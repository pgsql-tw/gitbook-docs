# AGENTS.md

本專案由多個 AI 代理（目前是 Codex 與 Claude）並行翻譯 PostgreSQL 手冊，目標版本以目前分支或明確的專案設定為準。

> 若你是 translation-only worker（提示詞要求只處理單一頁面、不得修改其他檔案），請忽略本檔，只遵守提示詞。

工具共用名稱採 `pg`；先執行 `python scripts/pg_project.py` 確認目標版本及實際資料根目錄。以下 `outputs/pg-translation` 是新專案預設；既有版本目錄由工具自動辨識，勿直接搬動審查存檔或另建競爭佇列。

開始任何翻譯或發佈工作前，先讀協作協定：`outputs/pg-translation/agents/PROTOCOL.md`。

重點摘要：

- **單一發佈者**：只有 publisher（目前是 Codex）可以修改受追蹤檔案並 commit。其他代理把譯稿送到 `outputs/pg-translation/agents/inbox/`。
- **取頁方向**：Codex 由 `outputs/pg-translation/pending-pages.md` 由上往下；Claude 由下往上。
- **先認領再翻譯**：`outputs/pg-translation/agents/claims/<slug>.json`；他人有效認領的頁面一律跳過。
- **交接工具**：`python scripts/agent_handoff.py status | claim | publish | message`。
- **進度與訊息**：`outputs/pg-translation/agents/status/`（各寫各的）、`outputs/pg-translation/agents/messages/`（一則一檔）。
- **專案 skill**：`.agents/skills/postgresql-tw-translation/SKILL.md`；風格見其 `references/style.md`（技術直述），修訂複審依入口載入 `references/review-workflow.md`。
- **目前發佈標的**：GitBook；格式、導航修繕與公開驗收依 skill 入口載入 `references/gitbook-maintenance.md`。未來若加入其他標的，另確認其建置與驗收規則，不直接套用 GitBook 行為。

## 自動本地提交範圍（2026-11-07 使用者授權）

- 除暫存及機敏性檔案外，所有專案成果均納入自動 commit 範圍，包括手冊、程式、測試、skill、設定、協作文件，以及需長期保留的報告、清單、修補檔、截圖與驗證證據；不得只因檔案位於 `outputs/` 而排除。
- 每次工作完成後，publisher 檢查實際差異、機敏資訊及適用驗證，將該次已完成的成果一併本地提交；不必再逐次要求 commit 授權。既有尚未驗證或其他代理仍在編輯的檔案，核對完成後再提交，不盲目執行 `git add -A`。
- 排除可重建暫存、瀏覽器個人資料與快取、模型下載、執行期鎖與檢查點、巢狀測試 repository，以及密碼、私鑰、權杖、cookie 或登入工作階段資料。持久證據如含機敏資訊，先產生可公開的遮蔽版本；不刪除或改寫原始審查歷史。
- 保留既有協作執行期目錄的忽略規則及單一 publisher 分工，不直接提交他人未完成的工作或修改他人看板。提交訊息使用正體中文；push 仍由使用者處理，本授權不包含自動 push 或新的外部 AI 送審。
