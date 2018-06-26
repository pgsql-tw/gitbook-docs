# DROP SUBSCRIPTION

DROP SUBSCRIPTION — remove a subscription

### Synopsis

```text
DROP SUBSCRIPTION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

### Description

`DROP SUBSCRIPTION` removes a subscription from the database cluster.

A subscription can only be dropped by a superuser.

`DROP SUBSCRIPTION` cannot be executed inside a transaction block if the subscription is associated with a replication slot. \(You can use `ALTER SUBSCRIPTION` to unset the slot.\)

### Parameters

_`name`_

The name of a subscription to be dropped.`CASCADE`  
`RESTRICT`

These key words do not have any effect, since there are no dependencies on subscriptions.

### Notes

When dropping a subscription that is associated with a replication slot on the remote host \(the normal state\), `DROP SUBSCRIPTION` will connect to the remote host and try to drop the replication slot as part of its operation. This is necessary so that the resources allocated for the subscription on the remote host are released. If this fails, either because the remote host is not reachable or because the remote replication slot cannot be dropped or does not exist or never existed, the `DROP SUBSCRIPTION` command will fail. To proceed in this situation, disassociate the subscription from the replication slot by executing `ALTER SUBSCRIPTION ... SET (slot_name = NONE)`. After that, `DROP SUBSCRIPTION` will no longer attempt any actions on a remote host. Note that if the remote replication slot still exists, it should then be dropped manually; otherwise it will continue to reserve WAL and might eventually cause the disk to fill up. See also [Section 31.2.1](https://www.postgresql.org/docs/10/static/logical-replication-subscription.html#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT).

If a subscription is associated with a replication slot, then `DROP SUBSCRIPTION` cannot be executed inside a transaction block.

### Examples

Drop a subscription:

```text
DROP SUBSCRIPTION mysub;
```

### Compatibility

`DROP SUBSCRIPTION` is a PostgreSQL extension.

### See Also

[CREATE SUBSCRIPTION](create-subscription.md), [ALTER SUBSCRIPTION](alter-subscription.md)

