# AGENTS.md

本專案由多個 AI 代理（目前是 Codex 與 Claude）並行翻譯 PostgreSQL 18 手冊。

> 若你是 translation-only worker（提示詞要求只處理單一頁面、不得修改其他檔案），請忽略本檔，只遵守提示詞。

開始任何翻譯或發佈工作前，先讀協作協定：`outputs/pg18-translation/agents/PROTOCOL.md`。

重點摘要：

- **單一發佈者**：只有 publisher（目前是 Codex）可以修改受追蹤檔案並 commit。其他代理把譯稿送到 `outputs/pg18-translation/agents/inbox/`。
- **取頁方向**：Codex 由 `outputs/pg18-translation/pending-pages.md` 由上往下；Claude 由下往上。
- **先認領再翻譯**：`outputs/pg18-translation/agents/claims/<slug>.json`；他人有效認領的頁面一律跳過。
- **交接工具**：`python scripts/agent_handoff.py status | claim | publish | message`。
- **進度與訊息**：`outputs/pg18-translation/agents/status/`（各寫各的）、`outputs/pg18-translation/agents/messages/`（一則一檔）。
- **風格**：Codex skill `postgresql-tw-translation` 的 SKILL.md 與 `references/style.md`（技術直述）。
