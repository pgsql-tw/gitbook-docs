<a id="SQL-BEGIN"></a><a id="id-1.9.3.47.1"></a>

# BEGIN

BEGIN — start a transaction block

## Synopsis

```

BEGIN [ WORK | TRANSACTION ] [ transaction_mode [, ...] ]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

<a id="id-1.9.3.47.5"></a>

## Description

`BEGIN` initiates a transaction block, that is, all statements after a `BEGIN` command will be executed in a single transaction until an explicit [`COMMIT`](commit.md) or [`ROLLBACK`](rollback.md) is given. By default (without `BEGIN`), PostgreSQL executes transactions in “autocommit” mode, that is, each statement is executed in its own transaction and a commit is implicitly performed at the end of the statement (if execution was successful, otherwise a rollback is done).

Statements are executed more quickly in a transaction block, because transaction start/commit requires significant CPU and disk activity. Execution of multiple statements inside a transaction is also useful to ensure consistency when making several related changes: other sessions will be unable to see the intermediate states wherein not all the related updates have been done.

If the isolation level, read/write mode, or deferrable mode is specified, the new transaction has those characteristics, as if [`SET TRANSACTION`](set-transaction.md) was executed.

<a id="id-1.9.3.47.6"></a>

## Parameters

`WORK`<br>`TRANSACTION`

Optional key words. They have no effect.

Refer to [SET TRANSACTION](set-transaction.md) for information on the meaning of the other parameters to this statement.

<a id="id-1.9.3.47.7"></a>

## Notes

[`START TRANSACTION`](start-transaction.md) has the same functionality as `BEGIN`.

Use [`COMMIT`](commit.md) or [`ROLLBACK`](rollback.md) to terminate a transaction block.

Issuing `BEGIN` when already inside a transaction block will provoke a warning message. The state of the transaction is not affected. To nest transactions within a transaction block, use savepoints (see [SAVEPOINT](savepoint.md)).

For reasons of backwards compatibility, the commas between successive <em class="replaceable"><code>transaction&#95;modes</code></em> can be omitted.

<a id="id-1.9.3.47.8"></a>

## Examples

To begin a transaction block:

```

BEGIN;
```

<a id="id-1.9.3.47.9"></a>

## Compatibility

`BEGIN` is a PostgreSQL language extension. It is equivalent to the SQL-standard command [`START TRANSACTION`](start-transaction.md), whose reference page contains additional compatibility information.

The `DEFERRABLE` <em class="replaceable"><code>transaction&#95;mode</code></em> is a PostgreSQL language extension.

Incidentally, the `BEGIN` key word is used for a different purpose in embedded SQL. You are advised to be careful about the transaction semantics when porting database applications.

<a id="id-1.9.3.47.10"></a>

## See Also

[COMMIT](commit.md), [ROLLBACK](rollback.md), [START TRANSACTION](start-transaction.md), [SAVEPOINT](savepoint.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-begin.html)（英文原文，待翻譯）
