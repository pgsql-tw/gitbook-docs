<a id="id-1.9.3.133.1"></a>

## DROP SUBSCRIPTION

DROP SUBSCRIPTION — remove a subscription

## Synopsis

```

DROP SUBSCRIPTION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.133.5"></a>

## Description

`DROP SUBSCRIPTION` removes a subscription from the
database cluster.

To execute this command the user must be the owner of the subscription.

`DROP SUBSCRIPTION` cannot be executed inside a
transaction block if the subscription is associated with a replication
slot. (You can use [`ALTER SUBSCRIPTION`](sql-altersubscription.md) to unset the
slot.)

<a id="id-1.9.3.133.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the subscription does not exist. A notice is
    issued in this case.

*`name`*
:   The name of a subscription to be dropped.

`CASCADE`<br>`RESTRICT`
:   These key words do not have any effect, since there are no dependencies
    on subscriptions.

<a id="id-1.9.3.133.7"></a>

## Notes

When dropping a subscription that is associated with a replication slot on
the remote host (the normal state), `DROP SUBSCRIPTION`
will connect to the remote host and try to drop the replication slot (and
any remaining table synchronization slots) as
part of its operation. This is necessary so that the resources allocated
for the subscription on the remote host are released. If this fails,
either because the remote host is not reachable or because the remote
replication slot cannot be dropped or does not exist or never existed,
the `DROP SUBSCRIPTION` command will fail. To proceed
in this situation, first disable the subscription by executing
[`ALTER SUBSCRIPTION ... DISABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE), and then disassociate
it from the replication slot by executing
[`ALTER SUBSCRIPTION ... SET (slot_name = NONE)`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-SET).
After that, `DROP SUBSCRIPTION` will not attempt to drop
the subscription's own replication slot. It may still connect to the publisher
to drop internally-created table synchronization slots if some table
synchronization is left unfinished; if the publisher is unreachable, those
slots (and the main slot, if it still exists) must be dropped manually. Otherwise
it/they will continue to reserve WAL and might eventually cause the disk to
fill up. See also
[Section 29.2.1](../../server-administration/logical-replication/logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT).

If a subscription is associated with a replication slot, then `DROP
SUBSCRIPTION` cannot be executed inside a transaction block.

<a id="id-1.9.3.133.8"></a>

## Examples

Drop a subscription:

```

DROP SUBSCRIPTION mysub;
```

<a id="id-1.9.3.133.9"></a>

## Compatibility

`DROP SUBSCRIPTION` is a PostgreSQL
extension.

<a id="id-1.9.3.133.10"></a>

## See Also

[CREATE SUBSCRIPTION](sql-createsubscription.md), [ALTER SUBSCRIPTION](sql-altersubscription.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropsubscription.html)（英文原文，待翻譯）
