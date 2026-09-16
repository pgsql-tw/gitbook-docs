# 補審單頁退件隔離

修正 `process_deferred()` 將單頁語意退件拋成 GlobalFailure，導致整個控制器退出的問題。

- 語意退件與 reviewer 的 PageFailure：持久化為 `review_exception`，保留錯誤、來源與審查證據，繼續下一頁。
- 相同輸入的既有退件：不再次呼叫模型、不重複送出退件事件。sync 不再將此狀態改回一般待補審。
- 權限／額度、輸入被修改、來源或提交雜湊不一致等 GlobalFailure：繼續向外拋出，不能掩蓋資料完整性問題。
- 批次達到 100 個新增頁面但仍有補審例外時：停止新增，狀態為 `batch_target_reached_review_incomplete`，不是完成。全站結束檢查亦會計入補審例外。

這次修改不會自動修正或核准 functions-admin，也沒有刪除其退件。後續仍須在隔離稿修正、重審與明確對帳；不能把「主佇列繼續」解讀為「退件已解決」。

新增／調整測試：退件不能完成且不重試、退件不阻擋下一頁、PageFailure 與 GlobalFailure 分流、批次達標不能隱藏退件。deferred 測試共 7 項通過。
