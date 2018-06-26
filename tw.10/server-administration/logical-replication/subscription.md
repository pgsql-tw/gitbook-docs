---
description: 版本：10
---

# 31.2. Subscription

A _subscription_ is the downstream side of logical replication. The node where a subscription is defined is referred to as the _subscriber_. A subscription defines the connection to another database and set of publications \(one or more\) to which it wants to subscribe.

The subscriber database behaves in the same way as any other PostgreSQL instance and can be used as a publisher for other databases by defining its own publications.

A subscriber node may have multiple subscriptions if desired. It is possible to define multiple subscriptions between a single publisher-subscriber pair, in which case care must be taken to ensure that the subscribed publication objects don't overlap.

Each subscription will receive changes via one replication slot \(see [Section 26.2.6](https://www.postgresql.org/docs/10/static/warm-standby.html#STREAMING-REPLICATION-SLOTS)\). Additional temporary replication slots may be required for the initial data synchronization of pre-existing table data.

A logical replication subscription can be a standby for synchronous replication \(see [Section 26.2.8](https://www.postgresql.org/docs/10/static/warm-standby.html#SYNCHRONOUS-REPLICATION)\). The standby name is by default the subscription name. An alternative name can be specified as `application_name` in the connection information of the subscription.

Subscriptions are dumped by `pg_dump` if the current user is a superuser. Otherwise a warning is written and subscriptions are skipped, because non-superusers cannot read all subscription information from the `pg_subscription` catalog.

The subscription is added using [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-createsubscription.html) and can be stopped/resumed at any time using the [ALTER SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-altersubscription.html) command and removed using [DROP SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-dropsubscription.html).

When a subscription is dropped and recreated, the synchronization information is lost. This means that the data has to be resynchronized afterwards.

The schema definitions are not replicated, and the published tables must exist on the subscriber. Only regular tables may be the target of replication. For example, you can't replicate to a view.

The tables are matched between the publisher and the subscriber using the fully qualified table name. Replication to differently-named tables on the subscriber is not supported.

Columns of a table are also matched by name. A different order of columns in the target table is allowed, but the column types have to match. The target table can have additional columns not provided by the published table. Those will be filled with their default values.

#### 31.2.1. Replication Slot Management

As mentioned earlier, each \(active\) subscription receives changes from a replication slot on the remote \(publishing\) side. Normally, the remote replication slot is created automatically when the subscription is created using `CREATE SUBSCRIPTION` and it is dropped automatically when the subscription is dropped using `DROP SUBSCRIPTION`. In some situations, however, it can be useful or necessary to manipulate the subscription and the underlying replication slot separately. Here are some scenarios:

* When creating a subscription, the replication slot already exists. In that case, the subscription can be created using the `create_slot = false` option to associate with the existing slot.
* When creating a subscription, the remote host is not reachable or in an unclear state. In that case, the subscription can be created using the `connect = false` option. The remote host will then not be contacted at all. This is what pg\_dump uses. The remote replication slot will then have to be created manually before the subscription can be activated.
* When dropping a subscription, the replication slot should be kept. This could be useful when the subscriber database is being moved to a different host and will be activated from there. In that case, disassociate the slot from the subscription using `ALTER SUBSCRIPTION` before attempting to drop the subscription.
* When dropping a subscription, the remote host is not reachable. In that case, disassociate the slot from the subscription using `ALTER SUBSCRIPTION` before attempting to drop the subscription. If the remote database instance no longer exists, no further action is then necessary. If, however, the remote database instance is just unreachable, the replication slot should then be dropped manually; otherwise it would continue to reserve WAL and might eventually cause the disk to fill up. Such cases should be carefully investigated.

