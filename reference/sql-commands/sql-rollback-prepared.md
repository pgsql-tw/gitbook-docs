<a id="id-1.9.3.168.1"></a>

## ROLLBACK PREPARED

ROLLBACK PREPARED — cancel a transaction that was earlier prepared for two-phase commit

## Synopsis

```

ROLLBACK PREPARED transaction_id
```

<a id="id-1.9.3.168.5"></a>

## Description

`ROLLBACK PREPARED` rolls back a transaction that is in
prepared state.

<a id="id-1.9.3.168.6"></a>

## Parameters

*`transaction_id`*
:   The transaction identifier of the transaction that is to be
    rolled back.

<a id="id-1.9.3.168.7"></a>

## Notes

To roll back a prepared transaction, you must be either the same user that
executed the transaction originally, or a superuser. But you do not
have to be in the same session that executed the transaction.

This command cannot be executed inside a transaction block. The prepared
transaction is rolled back immediately.

All currently available prepared transactions are listed in the
[`pg_prepared_xacts`](../../internals/views/view-pg-prepared-xacts.md)
system view.

<a id="SQL-ROLLBACK-PREPARED-EXAMPLES"></a>

## Examples

Roll back the transaction identified by the transaction
identifier `foobar`:

```

ROLLBACK PREPARED 'foobar';
```

<a id="id-1.9.3.168.9"></a>

## Compatibility

`ROLLBACK PREPARED` is a
PostgreSQL extension. It is intended for use by
external transaction management systems, some of which are covered by
standards (such as X/Open XA), but the SQL side of those systems is not
standardized.

<a id="id-1.9.3.168.10"></a>

## See Also

[PREPARE TRANSACTION](sql-prepare-transaction.md), [COMMIT PREPARED](sql-commit-prepared.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-rollback-prepared.html)（英文原文，待翻譯）
