## 29.10. 監控 [#](#LOGICAL-REPLICATION-MONITORING)

由於邏輯複寫的架構與[實體串流複寫](../high-availability/warm-standby.md#STREAMING-REPLICATION)相近，發佈節點的監控方式也類似於實體複寫主要伺服器的監控（請參閱[第 26.2.5.2 節](../high-availability/warm-standby.md#STREAMING-REPLICATION-MONITORING)）。

訂閱的監控資訊可在 [`pg_stat_subscription`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION)中查看。此檢視表會為每個訂閱工作者包含一個資料列。訂閱可依其狀態有零個或多個作用中的訂閱工作者。

一般而言，已啟用的訂閱會有一個套用程序執行。已停用或當機的訂閱在此檢視表中沒有資料列。若任何資料表正在進行初始資料同步，則會有額外工作者處理同步中的資料表。此外，若[`streaming`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING)交易以平行方式套用，可能還會有額外的平行套用工作者。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-monitoring.html)（原文版本：18.6；核對日期：2026-09-10）
