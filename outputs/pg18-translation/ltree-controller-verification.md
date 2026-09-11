# ltree 續跑控制器驗證

日期：2026-09-11。測試範圍僅為 `appendixes/contrib/ltree.md`，不是剩餘所有頁面的無人值守部署。

## 結果

- 翻譯 commit：`bd42ec86c5aeb0fbafb37f2b9dc771abf7b5f74a`。
- 頁面 SHA-256：`e6e5fde4c3915e673ea349ba39ee21213f4d1eac8522ec118af96c1ee1cc9951`（UTF-8，LF 換行）。
- 完成 F.22.1 至 F.22.6，依既有「技術直述」skill；保留原有部分翻譯並補齊漏譯。
- 原文基準：[PostgreSQL 18.6 ltree](https://www.postgresql.org/docs/18/ltree.html)，2026-09-11 核對。
- 實際待譯清單由 916 減為 915；原頁首過期數字 923 已修正。
- 真實儲存庫再次執行 finalize 回傳同一筆 commit，事件為 `reconciled`，未新增翻譯 commit。
- `git diff --check` 通過。提交僅包括頁面、SUMMARY、待譯清單與續跑狀態。

## 故障注入：22 項全部通過

重現：`python -m unittest discover -s scripts -p test_translation_controller.py -v`。最後一次結果：Ran 22 tests in 6.514s / OK。
測試使用臨時 Git repository，不改動正式譯文或使用者未追蹤目錄。

1. 連續兩次無頁面變化標記 failed_no_progress。
2. 只改檢查點不算翻譯進展。
3. 重新建立控制器保留部分譯文與連續無進展計數。
4. 未經語意審查不能提交。
5. 審查後檔案變更不能提交。
6. 過期審查雜湊不能核准。
7. SQL 範例變更被攔截。
8. 行內識別字變更被攔截。
9. 語法範例的說明文字允許翻譯。
10. 行內識別字允許依中文語序調整次序，但保留內容與數量。
11. 遺失錨點被攔截。
12. 使用者已暫存的其他檔案被保留，拒絕混入提交。
13. 模擬 commit 已完成、狀態尚未保存即中斷；重啟後對帳，不重複提交。
14. 待譯數字不一致時拒絕提交。
15. 登入失敗狀態持久保存。
16. 第二個寫入者無法取得鎖；子程序以 os._exit 中斷後可重新取得鎖。
17. 模擬 CLI 宣稱完成但無檔案變更：重試兩次後失敗。
18. 模擬 CLI 部分完成：立即執行下一次；完成候選仍須另外審查，沒有自行 commit。
19. 模擬 CLI 結構化回覆無效：明確記錄失敗。
20. 模擬完成候選結構不合格：立即回饋並重試，通過後仍需語意審查。
21. 允許翻譯 HTML table 的 summary 說明，但表格結構變動仍被攔截。
22. 事件檔無寫入權限時仍向 stdout 回報原始錯誤，不因記錄錯誤再次崩潰。

## 全頁語意核對

核對標籤的 1000 字元與 65535 標籤上限、量詞預設與 NOT 群組、`%` 與 `*` 的逐字行為、ltxtquery 位置無關及空白規則、16 項運算子描述、10 項函式簽章與範例、負 offset/len、8 引數限制、siglen 的 8/28 預設值與 2024 上限、GiST 有損警告、SQL 查詢輸出，以及 PL/Python 不支援反向轉換。

程式檢查比對初始化時的 HTML code、表格標記、錨點、連結、行內程式碼與程式碼區塊；前三個區塊包含可翻譯的語法說明，因此只機械保護各列語法首欄，其餘說明由語意審查核對。修正原本缺失的 LTREE 頁面錨點。沒有資料庫變更，也沒有宣稱執行 SQL 範例。

## 實際發現的阻礙與尚未驗證事項

- 沙箱內 `codex login status` 顯示 Not logged in；該環境的 CLI worker 在登入預檢即失敗。經核准在沙箱外檢查卻顯示 Logged in using ChatGPT；這是執行環境可見性差異，不能直接推論帳號未登入。後續以隔離儲存庫進行真實 CLI 測試。
- 正式儲存庫的翻譯與語意審查由目前對話執行，控制器記錄兩次候選內容變更、雜湊核准並執行提交。另有隔離 CLI 實測，見下節。
- 初次 Git 寫入遇到 `.git/index.lock: Permission denied`，經工具核准後成功。未關閉沙箱或繞過權限。
- 尚未測試真實 worker 超時、模型額度限制或網路中斷。worker 有整次執行 timeout 與事件檔，但尚未實作逐事件活性監控。
- 核准是審查流程，不是安全隔離；不能讓翻譯 worker 自己執行 approve。工作者修改範圍仍依賴指令與沙箱，提交範圍另由程式白名單限制。
- 尚未部署跨頁佇列、自動語意審查或通知轉送。heartbeat `postgresql-18` 已暫停，避免舊提示詞與控制器同時寫入。
- 需在能存取既有登入的核准執行環境驗證真實模型，並通過連續三頁測試，才可擴大部署。此 pilot 固定 ltree，不可直接當成通用全量 runner。

## 真實 CLI 隔離重播

由 `scripts/live_translation_probe.py` 將本次初始化保存的未完成 ltree 快照放入獨立 Git repository；正式頁面不受影響。既有 ChatGPT 登入在經核准的執行環境可用，工作者仍採 workspace-write 沙箱，未使用繞過沙箱選項。

- 位置：`outputs/pg18-translation/controller-runtime/live-ltree-9zhyh71v/`。
- 20:16:14（台北）啟動真實工作者，20:18:52 回傳候選；讀取 skill、查官方原文、實際修改譯文均有 JSONL 事件。
- 首次候選缺少 LTREE 頁面錨點；未核准提交，於 20:19:13 續跑修復。
- 修復後的候選被當時過嚴的 HTML summary 檢查拒絕；20:20:20 控制器在同一次 run 中立即啟動第二次工作者，無需等待排程或使用者再次說「繼續」。
- 20:22:15 返回 `review_required`；最後候選雜湊 `cda2cfddfdf0c40ef1e6171d208156ced936869f628f26051220ac955ac76456`。最終機械檢查通過。
- 已將 summary 說明允許翻譯、表格結構仍受保護的規則修正並加回歸測試，避免日後誤報。運行中的程序使用啟動時程式碼，該次仍要求工作者還原 summary，事件如實保留。
- 此隔離候選未取得語意核准，故沒有自動提交；只有建立測試基線的那一筆 commit。正式通過全頁核對並提交的是本報告開頭的 `bd42ec86`。隔離候選仍有「符合符合」等既有語病，以及 lossy 譯為「有失真」等待修訂詞句，不能用機械檢查代替語意審查。
- 實際驗證了真實 CLI 翻譯、結構化結果、程式驗收與立即修復續跑。未宣稱全自動語意驗收、跨頁排程或不間斷服務已部署。

## 操作

`python scripts/translation_controller.py status` 查看狀態。

`python scripts/translation_controller.py check` 唯讀檢查結構；這兩個命令不取得寫入鎖，適合觀察權限受限的 runtime。

`init` 只初始化一次，保留已有 checkpoint；`observe` 只在一次實際工作嘗試結束後呼叫，不用作輪詢。`run` 嘗試 CLI 翻譯（預設最多兩次、每次上限 900 秒；此上限是自訂程式設定，不是產品時限）。`approve --sha256 HASH --note "核對依據"` 在人工／審查者全頁核對後使用。`finalize` 提交或對帳。已完成的 ltree 拒絕再次 run。

runtime 狀態與事件位於 `outputs/pg18-translation/controller-runtime/`，由 .gitignore 排除；其中 state.json 含初始譯文快照。不要在作業中刪除此目錄。狀態寫入採同目錄暫存檔加原子更名；鎖由作業系統管理，中斷後不需手動刪鎖。

如果中斷發生在 git add 之後、commit 之前，控制器會因索引非空而保守停止，需要核對暫存內容；不會自行清除使用者索引。已 commit 的中斷可自動對帳恢復。

CLI 介面依據：[官方非互動模式說明](https://learn.chatgpt.com/docs/non-interactive-mode)。未安裝替代 cron 或 Windows 排程。
