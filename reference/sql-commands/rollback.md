<a id="SQL-ROLLBACK"></a><a id="id-1.9.3.167.1"></a>

# ROLLBACK

ROLLBACK — abort the current transaction

## Synopsis

```

ROLLBACK [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

<a id="id-1.9.3.167.5"></a>

## Description

`ROLLBACK` rolls back the current transaction and causes all the updates made by the transaction to be discarded.

<a id="id-1.9.3.167.6"></a>

## Parameters

<a id="id-1.9.3.167.6.2"></a>

`WORK`<br>`TRANSACTION`

Optional key words. They have no effect.

<a id="SQL-ROLLBACK-CHAIN"></a>

`AND CHAIN`

If `AND CHAIN` is specified, a new transaction is immediately started with the same transaction characteristics (see [SET TRANSACTION](set-transaction.md)) as the just finished one. Otherwise, no new transaction is started.

<a id="id-1.9.3.167.7"></a>

## Notes

Use [`COMMIT`](commit.md) to successfully terminate a transaction.

Issuing `ROLLBACK` outside of a transaction block emits a warning and otherwise has no effect. `ROLLBACK AND CHAIN` outside of a transaction block is an error.

<a id="id-1.9.3.167.8"></a>

## Examples

To abort all changes:

```

ROLLBACK;
```

<a id="id-1.9.3.167.9"></a>

## Compatibility

The command `ROLLBACK` conforms to the SQL standard. The form `ROLLBACK TRANSACTION` is a PostgreSQL extension.

<a id="id-1.9.3.167.10"></a>

## See Also

[BEGIN](begin.md), [COMMIT](commit.md), [ROLLBACK TO SAVEPOINT](rollback-to-savepoint.md)

---

原文：[PostgreSQL 15.19 Documentation](rollback.md)（英文原文，待翻譯）
