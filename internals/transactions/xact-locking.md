## 67.2. Transactions and Locking [#](#XACT-LOCKING)

The transaction IDs of currently executing transactions are shown in
[`pg_locks`](../views/view-pg-locks.md)
in columns `virtualxid` and
`transactionid`. Read-only transactions
will have `virtualxid`s but NULL
`transactionid`s, while both columns will be
set in read-write transactions.

Some lock types wait on `virtualxid`,
while other types wait on `transactionid`.
Row-level read and write locks are recorded directly in the locked
rows and can be inspected using the [pgrowlocks](../../appendixes/contrib/pgrowlocks.md)
extension. Row-level read locks might also require the assignment
of multixact IDs (`mxid`; see [Section 24.1.5.1](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND)).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xact-locking.html)（英文原文，待翻譯）
