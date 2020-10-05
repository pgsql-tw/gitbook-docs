# 24. 例行性資料庫維護工作

像任何資料庫軟體一樣，PostgreSQL 要求定期執行某些任務以維持最佳性能。這裡討論的任務是必須的，但它們本質上是重複性的，並且可以使用標準工具（如 cron 腳本或 Windows 的「Task Scheduler」）輕鬆實現自動化。資料庫管理員有責任設置適當的腳本，並檢查它們是否成功執行。

一項明顯的維護任務是定期建立資料的備份副本。如果沒有最近的備份，在災難發生後（磁碟故障、火災、錯誤地刪除關鍵資料表等），您將無法恢復。PostgreSQL 中的備份和還原機制將在[第 25 章](../25.-bei-fen-ji-huan-yuan/)中詳細討論。

另一個主要類別的維護任務是定期「清理」資料庫。這個活動在[第 24.1 節](routine-vacuuming.md)中討論。與此密切相關的是更新查詢規劃器所使用的統計信息，如[第 24.1.3 節](routine-vacuuming.md#24-1-3-updating-planner-statistics)所述。

另一個需要定期關注的任務是日誌檔案管理。這在[第 24.3 節](log-file-maintenance.md)中討論。

[check\_postgres](https://bucardo.org/check_postgres/) 可用於監控資料庫執行狀況並回報異常情況。check\_postgres 能與 Nagios 和 MRTG 共同運作，但也可以獨立運行。

與其他一些資料庫管理系統相比，PostgreSQL 維護費用較低。儘管如此，對這些任務的適當關注將能有效地確保系統的使用上愉快且富有成效的體驗。

