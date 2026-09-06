<a id="id-1.9.3.146.1"></a>

## END

END — commit the current transaction

## Synopsis

```

END [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

<a id="id-1.9.3.146.5"></a>

## Description

`END` commits the current transaction. All changes
made by the transaction become visible to others and are guaranteed
to be durable if a crash occurs. This command is a
PostgreSQL extension
that is equivalent to [`COMMIT`](sql-commit.md).

<a id="id-1.9.3.146.6"></a>

## Parameters

`WORK`<br>`TRANSACTION`
:   Optional key words. They have no effect.

`AND CHAIN`
:   If `AND CHAIN` is specified, a new transaction is
    immediately started with the same transaction characteristics (see [SET TRANSACTION](sql-set-transaction.md)) as the just finished one. Otherwise,
    no new transaction is started.

<a id="id-1.9.3.146.7"></a>

## Notes

Use [`ROLLBACK`](sql-rollback.md) to
abort a transaction.

Issuing `END` when not inside a transaction does
no harm, but it will provoke a warning message.

<a id="id-1.9.3.146.8"></a>

## Examples

To commit the current transaction and make all changes permanent:

```

END;
```

<a id="id-1.9.3.146.9"></a>

## Compatibility

`END` is a PostgreSQL
extension that provides functionality equivalent to [`COMMIT`](sql-commit.md), which is
specified in the SQL standard.

<a id="id-1.9.3.146.10"></a>

## See Also

[BEGIN](sql-begin.md), [COMMIT](sql-commit.md), [ROLLBACK](sql-rollback.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-end.html)（英文原文，待翻譯）
