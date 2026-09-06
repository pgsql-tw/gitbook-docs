<a id="SQL-COMMIT"></a><a id="id-1.9.3.53.1"></a>

# COMMIT

COMMIT — commit the current transaction

## Synopsis

```

COMMIT [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

<a id="id-1.9.3.53.5"></a>

## Description

`COMMIT` commits the current transaction. All changes made by the transaction become visible to others and are guaranteed to be durable if a crash occurs.

<a id="id-1.9.3.53.6"></a>

## Parameters

<a id="id-1.9.3.53.6.2"></a>

`WORK`<br>`TRANSACTION`

Optional key words. They have no effect.

<a id="SQL-COMMIT-CHAIN"></a>

`AND CHAIN`

If `AND CHAIN` is specified, a new transaction is immediately started with the same transaction characteristics (see [SET TRANSACTION](set-transaction.md)) as the just finished one. Otherwise, no new transaction is started.

<a id="id-1.9.3.53.7"></a>

## Notes

Use [ROLLBACK](rollback.md) to abort a transaction.

Issuing `COMMIT` when not inside a transaction does no harm, but it will provoke a warning message. `COMMIT AND CHAIN` when not inside a transaction is an error.

<a id="id-1.9.3.53.8"></a>

## Examples

To commit the current transaction and make all changes permanent:

```

COMMIT;
```

<a id="id-1.9.3.53.9"></a>

## Compatibility

The command `COMMIT` conforms to the SQL standard. The form `COMMIT TRANSACTION` is a PostgreSQL extension.

<a id="id-1.9.3.53.10"></a>

## See Also

[BEGIN](begin.md), [ROLLBACK](rollback.md)

---

原文：[PostgreSQL 15.19 Documentation](commit.md)（英文原文，待翻譯）
