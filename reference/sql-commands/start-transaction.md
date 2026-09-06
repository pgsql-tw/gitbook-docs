<a id="SQL-START-TRANSACTION"></a><a id="id-1.9.3.180.1"></a>

# START TRANSACTION

START TRANSACTION — start a transaction block

## Synopsis

```

START TRANSACTION [ transaction_mode [, ...] ]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

<a id="id-1.9.3.180.5"></a>

## Description

This command begins a new transaction block. If the isolation level, read/write mode, or deferrable mode is specified, the new transaction has those characteristics, as if [`SET TRANSACTION`](set-transaction.md) was executed. This is the same as the [`BEGIN`](begin.md) command.

<a id="id-1.9.3.180.6"></a>

## Parameters

Refer to [SET TRANSACTION](set-transaction.md) for information on the meaning of the parameters to this statement.

<a id="id-1.9.3.180.7"></a>

## Compatibility

In the standard, it is not necessary to issue `START TRANSACTION` to start a transaction block: any SQL command implicitly begins a block. PostgreSQL's behavior can be seen as implicitly issuing a `COMMIT` after each command that does not follow `START TRANSACTION` (or `BEGIN`), and it is therefore often called “autocommit”. Other relational database systems might offer an autocommit feature as a convenience.

The `DEFERRABLE` <em class="replaceable"><code>transaction&#95;mode</code></em> is a PostgreSQL language extension.

The SQL standard requires commas between successive <em class="replaceable"><code>transaction&#95;modes</code></em>, but for historical reasons PostgreSQL allows the commas to be omitted.

See also the compatibility section of [SET TRANSACTION](set-transaction.md).

<a id="id-1.9.3.180.8"></a>

## See Also

[BEGIN](begin.md), [COMMIT](commit.md), [ROLLBACK](rollback.md), [SAVEPOINT](savepoint.md), [SET TRANSACTION](set-transaction.md)

---

原文：[PostgreSQL 15.19 Documentation](start-transaction.md)（英文原文，待翻譯）
