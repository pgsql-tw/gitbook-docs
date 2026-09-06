## 67.1. Transactions and Identifiers [#](#TRANSACTION-ID)

Transactions can be created explicitly using `BEGIN`
or `START TRANSACTION` and ended using
`COMMIT` or `ROLLBACK`. SQL
statements outside of explicit transactions automatically use
single-statement transactions.

Every transaction is identified by a unique
`VirtualTransactionId` (also called
`virtualXID` or `vxid`), which
is comprised of a backend's process number (or `procNumber`)
and a sequentially-assigned number local to each backend, known as
`localXID`. For example, the virtual transaction
ID `4/12532` has a `procNumber`
of `4` and a `localXID` of
`12532`.

Non-virtual `TransactionId`s (or `xid`),
e.g., `278394`, are assigned sequentially to
transactions from a global counter used by all databases within
the PostgreSQL cluster. This assignment
happens when a transaction first writes to the database. This means
lower-numbered xids started writing before higher-numbered xids.
Note that the order in which transactions perform their first database
write might be different from the order in which the transactions
started, particularly if the transaction started with statements that
only performed database reads.

The internal transaction ID type `xid` is 32 bits wide
and [wraps around](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND) every
4 billion transactions. A 32-bit epoch is incremented during each
wraparound. There is also a 64-bit type `xid8` which
includes this epoch and therefore does not wrap around during the
life of an installation; it can be converted to xid by casting.
The functions in [Table 9.84](../../the-sql-language/functions/functions-info.md#FUNCTIONS-PG-SNAPSHOT)
return `xid8` values. Xids are used as the
basis for PostgreSQL's [MVCC](../../the-sql-language/mvcc/README.md) concurrency mechanism and streaming
replication.

When a top-level transaction with a (non-virtual) xid commits,
it is marked as committed in the `pg_xact`
directory. Additional information is recorded in the
`pg_commit_ts` directory if [track_commit_timestamp](../../server-administration/runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP) is enabled.

In addition to `vxid` and `xid`,
prepared transactions are also assigned Global Transaction
Identifiers (GID). GIDs are string literals up
to 200 bytes long, which must be unique amongst other currently
prepared transactions. The mapping of GID to xid is shown in [`pg_prepared_xacts`](../views/view-pg-prepared-xacts.md).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/transaction-id.html)（英文原文，待翻譯）
