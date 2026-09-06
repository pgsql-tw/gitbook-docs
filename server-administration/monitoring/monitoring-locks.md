## 27.3. 檢視鎖定 [#](#MONITORING-LOCKS)

<a id="id-1.6.14.8.2"></a>

另一個監控資料庫活動的實用工具是 `pg_locks` 系統資料表。它讓資料庫管理者能查看鎖定管理器中尚未解除之鎖定的資訊。例如，可以用來：

* 查看目前所有尚未解除的鎖定、特定資料庫中所有關聯上的鎖定、特定關聯上的所有鎖定，或特定 PostgreSQL 工作階段持有的所有鎖定。
* 找出目前資料庫中尚未獲准之鎖定最多的關聯（這可能是資料庫用戶端之間競爭的來源）。
* 判斷鎖定競爭對整體資料庫效能的影響，以及競爭程度如何隨整體資料庫流量改變。

`pg_locks` 檢視表的詳細資訊見[第 53.13 節](../../internals/views/view-pg-locks.md)。關於 PostgreSQL 鎖定與並行管理的更多資訊，請參閱[第 13 章](../../the-sql-language/mvcc/README.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-locks.html)（原文版本：18.6；核對日期：2026-09-07）
