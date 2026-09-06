<a id="SQL-ABORT"></a><a id="id-1.9.3.3.1"></a>

# ABORT

ABORT — abort the current transaction

## Synopsis

```

ABORT [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

<a id="id-1.9.3.3.5"></a>

## Description

`ABORT` rolls back the current transaction and causes all the updates made by the transaction to be discarded. This command is identical in behavior to the standard SQL command [`ROLLBACK`](rollback.md), and is present only for historical reasons.

<a id="id-1.9.3.3.6"></a>

## Parameters

`WORK`<br>`TRANSACTION`

Optional key words. They have no effect.

`AND CHAIN`

If `AND CHAIN` is specified, a new transaction is immediately started with the same transaction characteristics (see [`SET TRANSACTION`](set-transaction.md)) as the just finished one. Otherwise, no new transaction is started.

<a id="id-1.9.3.3.7"></a>

## Notes

Use [`COMMIT`](commit.md) to successfully terminate a transaction.

Issuing `ABORT` outside of a transaction block emits a warning and otherwise has no effect.

<a id="id-1.9.3.3.8"></a>

## Examples

To abort all changes:

```

ABORT;
```

<a id="id-1.9.3.3.9"></a>

## Compatibility

This command is a PostgreSQL extension present for historical reasons. `ROLLBACK` is the equivalent standard SQL command.

<a id="id-1.9.3.3.10"></a>

## See Also

[BEGIN](begin.md), [COMMIT](commit.md), [ROLLBACK](rollback.md)

---

原文：[PostgreSQL 15.19 Documentation](abort.md)（英文原文，待翻譯）
