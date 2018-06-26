# CREATE SUBSCRIPTION

CREATE SUBSCRIPTION — define a new subscription

### Synopsis

```text
CREATE SUBSCRIPTION subscription_name
    CONNECTION 'conninfo'
    PUBLICATION publication_name [, ...]
    [ WITH ( subscription_parameter [= value] [, ... ] ) ]
```

### Description

`CREATE SUBSCRIPTION` adds a new subscription for the current database. The subscription name must be distinct from the name of any existing subscription in the database.

The subscription represents a replication connection to the publisher. As such this command does not only add definitions in the local catalogs but also creates a replication slot on the publisher.

A logical replication worker will be started to replicate data for the new subscription at the commit of the transaction where this command is run.

Additional info about subscriptions and logical replication as a whole can is available at [Section 31.2](https://www.postgresql.org/docs/10/static/logical-replication-subscription.html) and [Chapter 31](https://www.postgresql.org/docs/10/static/logical-replication.html).

### Parameters

_`subscription_name`_

The name of the new subscription.`CONNECTION '`_`conninfo`_'

The connection string to the publisher. For details see [Section 33.1.1](https://www.postgresql.org/docs/10/static/libpq-connect.html#LIBPQ-CONNSTRING).`PUBLICATION` _`publication_name`_

Names of the publications on the publisher to subscribe to.`WITH (` _`subscription_parameter`_ \[= _`value`_\] \[, ... \] \)

This clause specifies optional parameters for a subscription. The following parameters are supported:`copy_data` \(`boolean`\)

Specifies whether the existing data in the publications that are being subscribed to should be copied once the replication starts. The default is `true`.`create_slot` \(`boolean`\)

Specifies whether the command should create the replication slot on the publisher. The default is `true`.`enabled` \(`boolean`\)

Specifies whether the subscription should be actively replicating, or whether it should be just setup but not started yet. The default is `true`.`slot_name` \(`string`\)

Name of the replication slot to use. The default behavior is to use the name of the subscription for the slot name.

When `slot_name` is set to `NONE`, there will be no replication slot associated with the subscription. This can be used if the replication slot will be created later manually. Such subscriptions must also have both `enabled` and `create_slot` set to `false`.`synchronous_commit` \(`enum`\)

The value of this parameter overrides the [synchronous\_commit](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT) setting. The default value is `off`.

It is safe to use `off` for logical replication: If the subscriber loses transactions because of missing synchronization, the data will be resent from the publisher.

A different setting might be appropriate when doing synchronous logical replication. The logical replication workers report the positions of writes and flushes to the publisher, and when using synchronous replication, the publisher will wait for the actual flush. This means that setting `synchronous_commit` for the subscriber to `off` when the subscription is used for synchronous replication might increase the latency for `COMMIT` on the publisher. In this scenario, it can be advantageous to set `synchronous_commit` to `local` or higher.`connect` \(`boolean`\)

Specifies whether the `CREATE SUBSCRIPTION` should connect to the publisher at all. Setting this to `false` will change default values of `enabled`, `create_slot` and `copy_data` to `false`.

It is not allowed to combine `connect` set to `false` and `enabled`, `create_slot`, or `copy_data` set to `true`.

Since no connection is made when this option is set to `false`, the tables are not subscribed, and so after you enable the subscription nothing will be replicated. It is required to run `ALTER SUBSCRIPTION ... REFRESH PUBLICATION` in order for tables to be subscribed.

### Notes

See [Section 31.7](https://www.postgresql.org/docs/10/static/logical-replication-security.html) for details on how to configure access control between the subscription and the publication instance.

When creating a replication slot \(the default behavior\), `CREATE SUBSCRIPTION` cannot be executed inside a transaction block.

Creating a subscription that connects to the same database cluster \(for example, to replicate between databases in the same cluster or to replicate within the same database\) will only succeed if the replication slot is not created as part of the same command. Otherwise, the `CREATE SUBSCRIPTION` call will hang. To make this work, create the replication slot separately \(using the function `pg_create_logical_replication_slot` with the plugin name `pgoutput`\) and create the subscription using the parameter `create_slot = false`. This is an implementation restriction that might be lifted in a future release.

### Examples

Create a subscription to a remote server that replicates tables in the publications `mypublication` and `insert_only` and starts replicating immediately on commit:

```text
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION mypublication, insert_only;
```

Create a subscription to a remote server that replicates tables in the `insert_only` publication and does not start replicating until enabled at a later time.

```text
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION insert_only
               WITH (enabled = false);
```

### Compatibility

`CREATE SUBSCRIPTION` is a PostgreSQL extension.

### See Also

[ALTER SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-altersubscription.html), [DROP SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-dropsubscription.html), [CREATE PUBLICATION](https://www.postgresql.org/docs/10/static/sql-createpublication.html), [ALTER PUBLICATION](https://www.postgresql.org/docs/10/static/sql-alterpublication.html)

