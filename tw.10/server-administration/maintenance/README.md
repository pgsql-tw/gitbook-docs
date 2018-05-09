# 24. 例行性資料庫維護工作

像任何資料庫軟體一樣，PostgreSQL 要求定期執行某些任務以維持最佳性能。這裡討論的任務是必須的，但它們本質上是重複性的，並且可以使用標準工具（如 cron 腳本或 Windows 的「Task Scheduler」）輕鬆實現自動化。資料庫管理員有責任設置適當的腳本，並檢查它們是否成功執行。

一項明顯的維護任務是定期建立資料的備份副本。如果沒有最近的備份，在災難發生後（磁碟故障、火災、錯誤地刪除關鍵資料表等），您將無法恢復。PostgreSQL 中的備份和還原機制將在[第 25 章](../backup-and-restore/)中詳細討論。

The other main category of maintenance task is periodic “vacuuming” of the database. This activity is discussed in [Section 24.1](https://www.postgresql.org/docs/10/static/routine-vacuuming.html). Closely related to this is updating the statistics that will be used by the query planner, as discussed in [Section 24.1.3](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-STATISTICS).

Another task that might need periodic attention is log file management. This is discussed in [Section 24.3](https://www.postgresql.org/docs/10/static/logfile-maintenance.html).

[check\_postgres](https://bucardo.org/check_postgres/) is available for monitoring database health and reporting unusual conditions. check\_postgres integrates with Nagios and MRTG, but can be run standalone too.

PostgreSQL is low-maintenance compared to some other database management systems. Nonetheless, appropriate attention to these tasks will go far towards ensuring a pleasant and productive experience with the system.

