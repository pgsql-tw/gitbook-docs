# PostgreSQL 18 全量翻譯續跑狀態

- 建立日期：2026-09-11
- 範圍：`outputs/pg18-translation/pending-pages.md` 中所有未完成（`[ ]`）頁面。
- 起始待譯頁數：950
- 已選風格：技術直述；依 `postgresql-tw-translation` skill 及其 `references/style.md` 執行。
- 提交規則：每完成一個 Markdown 頁面，連同必要的 `SUMMARY.md` 與待譯清單更新，各自建立一筆 Git commit。
- 續跑任務：`postgresql-18`（heartbeat 已暫停，避免與控制器重複寫入）。
- 權限差異：2026-09-11 沙箱內 `codex login status` 顯示 Not logged in，但經核准在沙箱外顯示 Logged in using ChatGPT；不能直接判定帳號未登入。

## 續跑規則

每次續跑都先讀取本檔、`outputs/pg18-translation/pending-pages.md` 與 Git 狀態。若下列「進行中頁面」存在，必須從其未完成段落接續；只有沒有進行中頁面時，才從清單中的第一個 `[ ]` 頁面開始。翻譯前核對 PostgreSQL 18 官方文件；保留語法、識別字、範例、錨點、表格與相對連結。完成頁面後將清單標記為 `[x]` 並更新頁數。

## 本次測試頁面

- 路徑：`appendixes/contrib/ltree.md`
- 標題：F.22. `ltree` — 階層式樹狀資料型別
- 已完成：F.22.1 至 F.22.6 全頁翻譯與 PostgreSQL 18.6 原文核對；補齊語法範例說明、函式表格、頁面錨點與目錄。
- 審查雜湊：`e6e5fde4c3915e673ea349ba39ee21213f4d1eac8522ec118af96c1ee1cc9951`（UTF-8、換行正規化為 LF）。
- 提交由 `scripts/translation_controller.py finalize` 執行；以 Git 中的 `Translation-Page-SHA256` trailer 及 runtime 狀態確認，不以此文字宣告代替 commit。
- 全量待譯：915 頁；本次只測試 ltree，不自動領取下一頁。
- 驗證：22 項故障注入通過；真實 CLI 隔離重播已走過候選、驗收攔截與立即修復續跑，詳見 `ltree-controller-verification.md`。隔離候選未經語意核准，沒有自動提交。

## 控制器規則（取代原提示詞看門狗）

- 頁面雜湊變化只代表候選進展；檢查點、時間戳與狀態回覆不算翻譯。
- 連續兩次沒有頁面變化即記錄 failed_no_progress；登入失敗則直接記錄 failed_auth。
- 同一頁採 OS 單寫入者鎖及原子狀態保存。長頁部分完成可立即接續；嘗試次數耗盡明確回報，不當成成功。
- 完整語意核對與結構檢查後，以頁面 SHA-256 核准；檔案再變動即使核准失效。
- 每頁只提交頁面及必要追蹤檔。commit 後狀態尚未保存就中斷時，以 trailer 對帳，避免重複提交。
- 尚未部署跨頁佇列、自動語意審查或背景通知轉送；不得宣稱全量自動翻譯正在運作。

恢復全量執行前，先在可使用既有登入的核准執行環境完成真實工作者端到端驗證，再測試連續三頁。本次暫停是執行環境與測試範圍限制，不是全量完成。
