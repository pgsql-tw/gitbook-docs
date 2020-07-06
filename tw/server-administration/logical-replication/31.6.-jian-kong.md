# 30.6. 監控

由於邏輯複寫基於與[物理性的串流複寫](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-5-streaming-replication)相似的體系結構，因此發佈節點上的監控與監控物理式串流複寫主節點類似（請參閱[第 26.2.5.2 節](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-5-streaming-replication)）。

有關訂閱的監控訊息可以在 [pg\_stat\_subscription](../monitoring-database-activity/the-statistics-collector.md#28-2-2-viewing-statistics) 中找到。該檢視表對每個訂閱程序都有一個資料列。根據訂閱的狀態，訂閱可以有零個或多個活動訂閱程序。

一般而言，每一個啟用的訂閱會有單個 apply 程序運行。此檢視表中禁用的訂閱或當掉的訂閱將不會看到資料。如果任何資料表的初始資料同步正在進行，則會有額外的程序表示正在同步資料表。

