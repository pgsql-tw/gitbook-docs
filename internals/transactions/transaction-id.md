<a id="TRANSACTION-ID"></a>

## 67.1. 交易與識別碼 [#](#transaction-id) <a href="#transaction-id" id="transaction-id"></a>

交易可以使用 `BEGIN`
或 `START TRANSACTION` 明確建立，並使用
`COMMIT` 或 `ROLLBACK` 結束。位於明確交易之外的 SQL
陳述式會自動使用單一陳述式交易。

每個交易都以唯一的
`VirtualTransactionId`（也稱為
`virtualXID` 或 `vxid`）識別，它由後端的程序編號（或稱 `procNumber`）
以及各後端本地依序分配的編號（稱為
`localXID`）組成。例如，虛擬交易
ID `4/12532` 的 `procNumber`
為 `4`，`localXID` 為
`12532`。

非虛擬的 `TransactionId`（或稱 `xid`），
例如 `278394`，是從一個全域計數器依序分配給交易的，該計數器由
PostgreSQL 叢集中的所有資料庫共用。此分配發生在交易第一次寫入資料庫時。這表示編號較小的 xid 比編號較大的 xid 更早開始寫入。請注意，交易執行第一次資料庫寫入的順序，可能與交易開始的順序不同，特別是當交易一開始執行的是只進行資料庫讀取的陳述式時。

內部交易 ID 型別 `xid` 寬 32 位元，
每 40 億個交易就會[回捲](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)一次。每次回捲時，一個 32 位元的 epoch 會遞增。另外還有一個 64 位元的型別 `xid8`，它包含此 epoch，因此在整個安裝的生命週期內都不會回捲；它可以透過型別轉換轉為 xid。
[表 9.84](../../the-sql-language/functions/functions-info.md#FUNCTIONS-PG-SNAPSHOT) 中的函式
會傳回 `xid8` 值。xid 是 PostgreSQL 的 [MVCC](../../the-sql-language/mvcc/README.md) 並行機制與串流複寫的基礎。

當具有（非虛擬）xid 的最上層交易提交時，
它會在 `pg_xact`
目錄中被標記為已提交。若啟用了 [track_commit_timestamp](../../server-administration/runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)，還會在
`pg_commit_ts` 目錄中記錄額外的資訊。

除了 `vxid` 與 `xid` 之外，
預備交易還會被分配全域交易識別碼（Global Transaction
Identifier，GID）。GID 是最長 200 位元組的字串常數，在目前其他已預備的交易之中必須是唯一的。GID 與 xid 的對應關係顯示於 [`pg_prepared_xacts`](../views/view-pg-prepared-xacts.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/transaction-id.html)（原文版本：18.6；核對日期：2026-10-12）
