# COMMIT PREPARED

COMMIT PREPARED — commit a transaction that was earlier prepared for two-phase commit

### Synopsis

```
COMMIT PREPARED transaction_id
```

### Description

`COMMIT PREPARED` commits a transaction that is in prepared state.

### Parameters

_`transaction_id`_

The transaction identifier of the transaction that is to be committed.

### Notes

To commit a prepared transaction, you must be either the same user that executed the transaction originally, or a superuser. But you do not have to be in the same session that executed the transaction.

This command cannot be executed inside a transaction block. The prepared transaction is committed immediately.

All currently available prepared transactions are listed in the [`pg_prepared_xacts`](../../internals/system-catalogs/pg_prepared_xacts.md) system view.

### Examples

Commit the transaction identified by the transaction identifier `foobar`:

```
COMMIT PREPARED 'foobar';
```

### Compatibility

`COMMIT PREPARED` is a PostgreSQL extension. It is intended for use by external transaction management systems, some of which are covered by standards (such as X/Open XA), but the SQL side of those systems is not standardized.

### See Also

[PREPARE TRANSACTION](prepare-transaction.md), [ROLLBACK PREPARED](rollback-prepared.md)
