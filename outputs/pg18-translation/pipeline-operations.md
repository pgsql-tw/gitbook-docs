# PostgreSQL 18 持續翻譯操作

## 執行與判讀

在專案根目錄，以具有既有 Codex 登入與 Git 寫入權限的環境執行：

```powershell
$env:PYTHONUTF8='1'
python scripts/translation_pipeline.py status
python scripts/translation_pipeline.py events
python scripts/translation_pipeline.py run --validation-only
```

首次驗證頁是 passwordcheck、pgbuffercache、pageinspect。三頁都提交後，mode 才轉為 production；此時以 `run`（不加 validation-only）啟動連續翻譯。每完成一頁立即接下一頁，沒有每頁 15 分鐘的限制。

15 分鐘的 Codex heartbeat 是外部監控及接續機制，不是翻譯程序本身。ACTIVE 不能作為實際正在翻譯的證據。核對 `health`、heartbeat 的 page/role/time、worker log、程序身分及 Git 提交；日誌增長僅代表活動，`section_checkpoint` 的實際差異才是候選翻譯進度，commit 才是完成。

開始每輪先回報具體頁面，結束回報提交、部分完成、阻礙與剩餘頁數。`events` 是本機事件佇列，不等於已傳送使用者通知；實際回報後才用 `ack --through <事件編號>` 確認。背景程序的事件由 heartbeat 轉送，並非即時聊天通知。

每輪優先處理一份 inbox 並立即寫入结果事件、對帳佇列，再處理自己的一頁，避免大型送件批次長時間占用全部執行機會。額度錯誤由 JSONL 終止事件擷取，`status.last_failure` 顯示原因、頁面與日誌；不得把日誌中的文件內容誤判成錯誤。審查快取只在整頁、原文、來源與政策雜湊全部一致時重用；舊版未綁定快取重新審查。風格建議不是強制術語規則，不得單憑編輯偏好退件。

## 協作與安全性

- 遵循 AGENTS.md 與 agents/PROTOCOL.md；Codex 上往下，Claude 下往上。
- 先處理 inbox，逐頁獨立唯讀語意審查；保留 Claude 作者與來源。`publish --dry-run` 只表示結構預檢，不代表語意審查通過。
- 共用 publish.lock；claims.lock 保護本機工具的認領與釋放。外部橋接寫入不使用此鎖，因此發佈前仍重新核對檔案。
- 他人有效認領記為 delegated，認領到期／釋放後回 pending；不把 delegated 當完成。
- 外部完成須核對清單及 commit 內的頁面 SHA；單改勾選不算完成。
- 每頁草稿、官方來源快照、skill/style 快照、段落檢查點及審查結果存於 pipeline-runtime；不進 Git。
- 工作程序每 4 分鐘續期自己的認領；單次呼叫最長 20 分鐘。連續無進展或反覆審查失敗列為例外，不偽報完成。
- 發佈前保存寫入意圖；pipeline 可核對 before/after SHA，接續已寫入或已暫存但未 commit 的自身修改。不同內容或無關 staged 檔案一律停下保留。
- inbox 發佈失敗保留 index／檔案及 publish-failure.json，需要檢查現場；提交後未搬移 inbox 可安全對帳，不重複提交。禁止 reset/checkout 清理。
- 過期 PID 不是可刪程序的證據。有未對帳 worker 時先核對啟動時間、命令列與專屬 log，不盲目終止或另外啟動競爭者。
- 權限、網路或額度限制必須明確回報，不自動消耗 reset credit、不購買、不繞過拒絕。

## 驗證與結束

隔離測試：`python -m unittest discover -s scripts -p 'test_translation*.py'`，以及 `python -m unittest discover -s scripts -p 'test_agent_handoff.py'`。

正式結束還須核對待譯清單、例外、inbox、claims，並完成全站連結／結構稽核。`completed_pending_site_audit` 不是全部完成；尚未通過全站稽核不得停用 heartbeat 或宣告全數完成。

保留未追蹤 batch-100-direct，不執行 git add .，不 push。
