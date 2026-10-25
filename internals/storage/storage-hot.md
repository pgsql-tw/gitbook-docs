<a id="STORAGE-HOT"></a>

## 66.7. 僅堆積元組（HOT） [#](#storage-hot) <a href="#storage-hot" id="storage-hot"></a>

為了支援高度並行，PostgreSQL 使用[多版本並行控制](../../the-sql-language/mvcc/mvcc-intro.md)（MVCC）來儲存資料列。然而，MVCC 對於更新查詢有一些缺點。具體來說，更新需要將資料列的新版本加入資料表。這也可能需要為每個被更新的資料列建立新的索引項目，而移除資料列的舊版本及其索引項目的成本可能很高。

為了協助降低更新的負擔，PostgreSQL 提供一項稱為僅堆積元組（heap-only tuple，HOT）的最佳化。此最佳化在下列情況下可行：

* 此更新沒有修改資料表索引所參照的任何欄位（摘要型索引除外）。核心 PostgreSQL 發行版本中唯一的摘要型索引方法是 [BRIN](../indextypes/brin.md)。
* 包含舊資料列的頁面上有足夠的可用空間容納更新後的資料列。

在這些情況下，僅堆積元組提供兩項最佳化：

* 不需要新的索引項目來表示被更新的資料列；不過，摘要型索引可能仍需要更新。
* 當一個資料列被多次更新時，除了最舊與最新的版本以外，其他資料列版本都可以在正常操作期間（包括 `SELECT`）完全移除，而不需要定期執行清理（vacuum）操作。（索引一律參照原始資料列版本的[頁面項目識別碼](storage-page-layout.md)。與該資料列版本相關聯的元組資料會被移除，其項目識別碼則會轉換為重新導向（redirect），指向可能仍對某些並行交易可見的最舊版本。不再對任何人可見的中間資料列版本會被完全移除，相關的頁面項目識別碼也會變得可供重複使用。）

你可以藉由降低資料表的 [`fillfactor`](../../reference/sql-commands/sql-createtable.md#RELOPTION-FILLFACTOR) 來提高頁面有足夠空間進行 HOT 更新的可能性。即使不這麼做，HOT 更新仍會發生，因為新的資料列自然會遷移到新頁面，以及有足夠可用空間容納新資料列版本的既有頁面。系統檢視表 [pg_stat_all_tables](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW) 可以用來監控 HOT 與非 HOT 更新的發生情況。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-hot.html)（原文版本：18.6；核對日期：2026-10-12）
