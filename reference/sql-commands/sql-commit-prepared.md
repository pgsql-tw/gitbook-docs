<a id="id-1.9.3.54.1"></a>

## COMMIT PREPARED

COMMIT PREPARED — commit a transaction that was earlier prepared for two-phase commit

## Synopsis

```

COMMIT PREPARED transaction_id
```

<a id="id-1.9.3.54.5"></a>

## Description

`COMMIT PREPARED` commits a transaction that is in
prepared state.

<a id="id-1.9.3.54.6"></a>

## Parameters

*`transaction_id`*
:   The transaction identifier of the transaction that is to be
    committed.

<a id="id-1.9.3.54.7"></a>

## Notes

To commit a prepared transaction, you must be either the same user that
executed the transaction originally, or a superuser. But you do not
have to be in the same session that executed the transaction.

This command cannot be executed inside a transaction block. The prepared
transaction is committed immediately.

All currently available prepared transactions are listed in the
[`pg_prepared_xacts`](../../internals/views/view-pg-prepared-xacts.md)
system view.

<a id="SQL-COMMIT-PREPARED-EXAMPLES"></a>

## Examples

Commit the transaction identified by the transaction
identifier `foobar`:

```

COMMIT PREPARED 'foobar';
```

<a id="id-1.9.3.54.9"></a>

## Compatibility

`COMMIT PREPARED` is a
PostgreSQL extension. It is intended for use by
external transaction management systems, some of which are covered by
standards (such as X/Open XA), but the SQL side of those systems is not
standardized.

<a id="id-1.9.3.54.10"></a>

## See Also

[PREPARE TRANSACTION](sql-prepare-transaction.md), [ROLLBACK PREPARED](sql-rollback-prepared.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-commit-prepared.html)（英文原文，待翻譯）
