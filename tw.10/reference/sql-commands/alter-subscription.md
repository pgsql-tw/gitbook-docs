# ALTER SUBSCRIPTION

ALTER SUBSCRIPTION — change the definition of a subscription

### Synopsis

```text
ALTER SUBSCRIPTION name CONNECTION 'conninfo'
ALTER SUBSCRIPTION name SET PUBLICATION publication_name [, ...] [ WITH ( set_publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name REFRESH PUBLICATION [ WITH ( refresh_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name ENABLE
ALTER SUBSCRIPTION name DISABLE
ALTER SUBSCRIPTION name SET ( subscription_parameter [= value] [, ... ] )
ALTER SUBSCRIPTION name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER SUBSCRIPTION name RENAME TO new_name
```

### Description

`ALTER SUBSCRIPTION` can change most of the subscription properties that can be specified in [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-createsubscription.html).

You must own the subscription to use `ALTER SUBSCRIPTION`. To alter the owner, you must also be a direct or indirect member of the new owning role. The new owner has to be a superuser. \(Currently, all subscription owners must be superusers, so the owner checks will be bypassed in practice. But this might change in the future.\)

### Parameters

_`name`_

The name of a subscription whose properties are to be altered.`CONNECTION '`_`conninfo`_'

This clause alters the connection property originally set by [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-createsubscription.html). See there for more information.`SET PUBLICATION` _`publication_name`_

Changes list of subscribed publications. See [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-createsubscription.html) for more information. By default this command will also act like `REFRESH PUBLICATION`.

_`set_publication_option`_ specifies additional options for this operation. The supported options are:`refresh` \(`boolean`\)

When false, the command will not try to refresh table information. `REFRESH PUBLICATION` should then be executed separately. The default is `true`.

Additionally, refresh options as described under `REFRESH PUBLICATION` may be specified.`REFRESH PUBLICATION`

Fetch missing table information from publisher. This will start replication of tables that were added to the subscribed-to publications since the last invocation of `REFRESH PUBLICATION` or since `CREATE SUBSCRIPTION`.

_`refresh_option`_ specifies additional options for the refresh operation. The supported options are:`copy_data` \(`boolean`\)

Specifies whether the existing data in the publications that are being subscribed to should be copied once the replication starts. The default is `true`.`ENABLE`

Enables the previously disabled subscription, starting the logical replication worker at the end of transaction.`DISABLE`

Disables the running subscription, stopping the logical replication worker at the end of transaction.`SET (` _`subscription_parameter`_ \[= _`value`_\] \[, ... \] \)

This clause alters parameters originally set by [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-createsubscription.html). See there for more information. The allowed options are `slot_name` and `synchronous_commit`_`new_owner`_

The user name of the new owner of the subscription._`new_name`_

The new name for the subscription.

### Examples

Change the publication subscribed by a subscription to `insert_only`:

```text
ALTER SUBSCRIPTION mysub SET PUBLICATION insert_only;
```

Disable \(stop\) the subscription:

```text
ALTER SUBSCRIPTION mysub DISABLE;
```

### Compatibility

`ALTER SUBSCRIPTION` is a PostgreSQL extension.

### See Also

[CREATE SUBSCRIPTION](create-subscription.md), [DROP SUBSCRIPTION](https://www.postgresql.org/docs/10/static/sql-dropsubscription.html), [CREATE PUBLICATION](create-publication.md), [ALTER PUBLICATION](alter-publication.md)

