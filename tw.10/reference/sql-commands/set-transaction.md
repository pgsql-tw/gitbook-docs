# SET TRANSACTION

SET TRANSACTION — 設定目前交易事務的模式

## 語法

```text
SET TRANSACTION transaction_mode [, ...]
SET TRANSACTION SNAPSHOT snapshot_id
SET SESSION CHARACTERISTICS AS TRANSACTION transaction_mode [, ...]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

## 說明

SET TRANSACTION 指令設定目前交易事務的模式。它對任何後續的交易都沒有影響。SET SESSION CHARACTERISTICS 設定連線後續交易事務的預設的交易模式。 對於單個交易，這些預設值可以由 SET TRANSACTION 所覆寫。

可用的事務模式是事務隔離級別、事務存取模式（讀/寫或唯讀）以及可延遲模式。另外，可以選擇一個快照，但僅限於目前事務，而不是連線預設值。

事務的隔離級別確定了其他事務同時運行時事務可以看到的資料：

`READ COMMITTED`

A statement can only see rows committed before it began. This is the default.

`REPEATABLE READ`

All statements of the current transaction can only see rows committed before the first query or data-modification statement was executed in this transaction.

`SERIALIZABLE`

All statements of the current transaction can only see rows committed before the first query or data-modification statement was executed in this transaction. If a pattern of reads and writes among concurrent serializable transactions would create a situation which could not have occurred for any serial \(one-at-a-time\) execution of those transactions, one of them will be rolled back with a`serialization_failure`error.

The SQL standard defines one additional level,`READ UNCOMMITTED`. InPostgreSQL`READ UNCOMMITTED`is treated as`READ COMMITTED`.

The transaction isolation level cannot be changed after the first query or data-modification statement \(`SELECT`,`INSERT`,`DELETE`,`UPDATE`,`FETCH`, or`COPY`\) of a transaction has been executed. See[Chapter 13](https://www.postgresql.org/docs/10/static/mvcc.html)for more information about transaction isolation and concurrency control.

The transaction access mode determines whether the transaction is read/write or read-only. Read/write is the default. When a transaction is read-only, the following SQL commands are disallowed:`INSERT`,`UPDATE`,`DELETE`, and`COPY FROM`if the table they would write to is not a temporary table; all`CREATE`,`ALTER`, and`DROP`commands;`COMMENT`,`GRANT`,`REVOKE`,`TRUNCATE`; and`EXPLAIN ANALYZE`and`EXECUTE`if the command they would execute is among those listed. This is a high-level notion of read-only that does not prevent all writes to disk.

The`DEFERRABLE`transaction property has no effect unless the transaction is also`SERIALIZABLE`and`READ ONLY`. When all three of these properties are selected for a transaction, the transaction may block when first acquiring its snapshot, after which it is able to run without the normal overhead of a`SERIALIZABLE`transaction and without any risk of contributing to or being canceled by a serialization failure. This mode is well suited for long-running reports or backups.

The`SET TRANSACTION SNAPSHOT`command allows a new transaction to run with the same\_snapshot\_as an existing transaction. The pre-existing transaction must have exported its snapshot with the`pg_export_snapshot`function \(see[Section 9.26.5](https://www.postgresql.org/docs/10/static/functions-admin.html#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)\). That function returns a snapshot identifier, which must be given to`SET TRANSACTION SNAPSHOT`to specify which snapshot is to be imported. The identifier must be written as a string literal in this command, for example`'000003A1-1'`.`SET TRANSACTION SNAPSHOT`can only be executed at the start of a transaction, before the first query or data-modification statement \(`SELECT`,`INSERT`,`DELETE`,`UPDATE`,`FETCH`, or`COPY`\) of the transaction. Furthermore, the transaction must already be set to`SERIALIZABLE`or`REPEATABLE READ`isolation level \(otherwise, the snapshot would be discarded immediately, since`READ COMMITTED`mode takes a new snapshot for each command\). If the importing transaction uses`SERIALIZABLE`isolation level, then the transaction that exported the snapshot must also use that isolation level. Also, a non-read-only serializable transaction cannot import a snapshot from a read-only transaction.

## Notes

If`SET TRANSACTION`is executed without a prior`START TRANSACTION`or`BEGIN`, it emits a warning and otherwise has no effect.

It is possible to dispense with`SET TRANSACTION`by instead specifying the desired\_`transaction_modes`\_in`BEGIN`or`START TRANSACTION`. But that option is not available for`SET TRANSACTION SNAPSHOT`.

The session default transaction modes can also be set by setting the configuration parameters[default\_transaction\_isolation](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-ISOLATION),[default\_transaction\_read\_only](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-READ-ONLY), and[default\_transaction\_deferrable](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-DEFERRABLE). \(In fact`SET SESSION CHARACTERISTICS`is just a verbose equivalent for setting these variables with`SET`.\) This means the defaults can be set in the configuration file, via`ALTER DATABASE`, etc. Consult[Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html)for more information.

## Examples

To begin a new transaction with the same snapshot as an already existing transaction, first export the snapshot from the existing transaction. That will return the snapshot identifier, for example:

```text
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT pg_export_snapshot();
 pg_export_snapshot
---------------------
 00000003-0000001B-1
(1 row)
```

Then give the snapshot identifier in a`SET TRANSACTION SNAPSHOT`command at the beginning of the newly opened transaction:

```text
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION SNAPSHOT '00000003-0000001B-1';
```

## Compatibility

These commands are defined in theSQLstandard, except for the`DEFERRABLE`transaction mode and the`SET TRANSACTION SNAPSHOT`form, which arePostgreSQLextensions.

`SERIALIZABLE`is the default transaction isolation level in the standard. InPostgreSQLthe default is ordinarily`READ COMMITTED`, but you can change it as mentioned above.

In the SQL standard, there is one other transaction characteristic that can be set with these commands: the size of the diagnostics area. This concept is specific to embedded SQL, and therefore is not implemented in thePostgreSQLserver.

The SQL standard requires commas between successive`transaction_modes`, but for historical reasonsPostgreSQLallows the commas to be omitted.

