# PostgreSQL 18 全量翻譯續跑狀態

- 建立日期：2026-09-11
- 範圍：`outputs/pg18-translation/pending-pages.md` 中所有未完成（`[ ]`）頁面。
- 起始待譯頁數：950
- 已選風格：技術直述；依 `postgresql-tw-translation` skill 及其 `references/style.md` 執行。
- 提交規則：每完成一個 Markdown 頁面，連同必要的 `SUMMARY.md` 與待譯清單更新，各自建立一筆 Git commit。
- 續跑任務：`postgresql-18`（目前對話的 heartbeat，自動每 5 分鐘續跑）。

## 續跑規則

每次續跑都先讀取本檔、`outputs/pg18-translation/pending-pages.md` 與 Git 狀態，從清單中的第一個 `[ ]` 頁面繼續。翻譯前核對 PostgreSQL 18 官方文件；保留語法、識別字、範例、錨點、表格與相對連結。完成頁面後將清單標記為 `[x]` 並更新頁數。

不得因單次執行完成數量、發出進度訊息或建立 commit 而結束全量工作。只有待譯頁數為 0、所有頁面均已逐頁提交、且 Git 格式檢查通過時，才可停止 heartbeat 並回報完成。
