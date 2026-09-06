<a id="id-1.9.3.160.1"></a>

## PREPARE TRANSACTION

PREPARE TRANSACTION — prepare the current transaction for two-phase commit

## Synopsis

```

PREPARE TRANSACTION transaction_id
```

<a id="id-1.9.3.160.5"></a>

## Description

`PREPARE TRANSACTION` prepares the current transaction
for two-phase commit. After this command, the transaction is no longer
associated with the current session; instead, its state is fully stored on
disk, and there is a very high probability that it can be committed
successfully, even if a database crash occurs before the commit is
requested.

Once prepared, a transaction can later be committed or rolled back
with [`COMMIT PREPARED`](sql-commit-prepared.md)
or [`ROLLBACK PREPARED`](sql-rollback-prepared.md),
respectively. Those commands can be issued from any session, not
only the one that executed the original transaction.

From the point of view of the issuing session, `PREPARE
TRANSACTION` is not unlike a `ROLLBACK` command:
after executing it, there is no active current transaction, and the
effects of the prepared transaction are no longer visible. (The effects
will become visible again if the transaction is committed.)

If the `PREPARE TRANSACTION` command fails for any
reason, it becomes a `ROLLBACK`: the current transaction
is canceled.

<a id="id-1.9.3.160.6"></a>

## Parameters

*`transaction_id`*
:   An arbitrary identifier that later identifies this transaction for
    `COMMIT PREPARED` or `ROLLBACK PREPARED`.
    The identifier must be written as a string literal, and must be
    less than 200 bytes long. It must not be the same as the identifier
    used for any currently prepared transaction.

<a id="id-1.9.3.160.7"></a>

## Notes

`PREPARE TRANSACTION` is not intended for use in applications
or interactive sessions. Its purpose is to allow an external
transaction manager to perform atomic global transactions across multiple
databases or other transactional resources. Unless you're writing a
transaction manager, you probably shouldn't be using `PREPARE
TRANSACTION`.

This command must be used inside a transaction block. Use [`BEGIN`](sql-begin.md) to start one.

It is not currently allowed to `PREPARE` a transaction that
has executed any operations involving temporary tables or the session's
temporary namespace, created any cursors `WITH HOLD`, or
executed `LISTEN`, `UNLISTEN`, or
`NOTIFY`.
Those features are too tightly
tied to the current session to be useful in a transaction to be prepared.

If the transaction modified any run-time parameters with `SET`
(without the `LOCAL` option),
those effects persist after `PREPARE TRANSACTION`, and will not
be affected by any later `COMMIT PREPARED` or
`ROLLBACK PREPARED`. Thus, in this one respect
`PREPARE TRANSACTION` acts more like `COMMIT` than
`ROLLBACK`.

All currently available prepared transactions are listed in the
[`pg_prepared_xacts`](../../internals/views/view-pg-prepared-xacts.md)
system view.

### Caution

It is unwise to leave transactions in the prepared state for a long time.
This will interfere with the ability of `VACUUM` to reclaim
storage, and in extreme cases could cause the database to shut down
to prevent transaction ID wraparound (see [Section 24.1.5](../../server-administration/maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)). Keep in mind also that the transaction
continues to hold whatever locks it held. The intended usage of the
feature is that a prepared transaction will normally be committed or
rolled back as soon as an external transaction manager has verified that
other databases are also prepared to commit.

If you have not set up an external transaction manager to track prepared
transactions and ensure they get closed out promptly, it is best to keep
the prepared-transaction feature disabled by setting
[max_prepared_transactions](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PREPARED-TRANSACTIONS) to zero. This will
prevent accidental creation of prepared transactions that might then
be forgotten and eventually cause problems.

<a id="SQL-PREPARE-TRANSACTION-EXAMPLES"></a>

## Examples

Prepare the current transaction for two-phase commit, using
`foobar` as the transaction identifier:

```

PREPARE TRANSACTION 'foobar';
```

<a id="id-1.9.3.160.9"></a>

## Compatibility

`PREPARE TRANSACTION` is a
PostgreSQL extension. It is intended for use by
external transaction management systems, some of which are covered by
standards (such as X/Open XA), but the SQL side of those systems is not
standardized.

<a id="id-1.9.3.160.10"></a>

## See Also

[COMMIT PREPARED](sql-commit-prepared.md), [ROLLBACK PREPARED](sql-rollback-prepared.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-prepare-transaction.html)（英文原文，待翻譯）
