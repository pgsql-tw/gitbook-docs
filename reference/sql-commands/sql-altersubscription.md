<a id="id-1.9.3.33.1"></a>

## ALTER SUBSCRIPTION

ALTER SUBSCRIPTION — change the definition of a subscription

## Synopsis

```

ALTER SUBSCRIPTION name CONNECTION 'conninfo'
ALTER SUBSCRIPTION name SET PUBLICATION publication_name [, ...] [ WITH ( publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name ADD PUBLICATION publication_name [, ...] [ WITH ( publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name DROP PUBLICATION publication_name [, ...] [ WITH ( publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name REFRESH PUBLICATION [ WITH ( refresh_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name ENABLE
ALTER SUBSCRIPTION name DISABLE
ALTER SUBSCRIPTION name SET ( subscription_parameter [= value] [, ... ] )
ALTER SUBSCRIPTION name SKIP ( skip_option = value )
ALTER SUBSCRIPTION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER SUBSCRIPTION name RENAME TO new_name
```

<a id="id-1.9.3.33.5"></a>

## Description

`ALTER SUBSCRIPTION` can change most of the subscription
properties that can be specified
in [CREATE SUBSCRIPTION](sql-createsubscription.md).

You must own the subscription to use `ALTER SUBSCRIPTION`.
To rename a subscription or alter the owner, you must have
`CREATE` permission on the database. In addition,
to alter the owner, you must be able to `SET ROLE` to the
new owning role. If the subscription has
`password_required=false`, only superusers can modify it.

When refreshing a publication we remove the relations that are no longer
part of the publication and we also remove the table synchronization slots
if there are any. It is necessary to remove these slots so that the resources
allocated for the subscription on the remote host are released. If due to
network breakdown or some other error, PostgreSQL
is unable to remove the slots, an error will be reported. To proceed in this
situation, the user either needs to retry the operation or disassociate the
slot from the subscription and drop the subscription as explained in
[DROP SUBSCRIPTION](sql-dropsubscription.md).

Commands `ALTER SUBSCRIPTION ... REFRESH PUBLICATION`,
`ALTER SUBSCRIPTION ... {SET|ADD|DROP} PUBLICATION ...`
with `refresh` option as `true`,
`ALTER SUBSCRIPTION ... SET (failover = true|false)` and
`ALTER SUBSCRIPTION ... SET (two_phase = false)`
cannot be executed inside a transaction block.

Commands `ALTER SUBSCRIPTION ... REFRESH PUBLICATION` and
`ALTER SUBSCRIPTION ... {SET|ADD|DROP} PUBLICATION ...`
with `refresh` option as `true` also cannot
be executed when the subscription has
[`two_phase`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE)
commit enabled, unless
[`copy_data`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-COPY-DATA)
is `false`. See column `subtwophasestate`
of [`pg_subscription`](../../internals/catalogs/catalog-pg-subscription.md)
to know the actual two-phase state.

<a id="id-1.9.3.33.6"></a>

## Parameters

<a id="SQL-ALTERSUBSCRIPTION-PARAMS-NAME"></a>

*`name`* [#](#SQL-ALTERSUBSCRIPTION-PARAMS-NAME)
:   The name of a subscription whose properties are to be altered.
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-CONNECTION"></a>

`CONNECTION 'conninfo'` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-CONNECTION)
:   This clause replaces the connection string originally set by
    [CREATE SUBSCRIPTION](sql-createsubscription.md). See there for more
    information.
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-SETADDDROP-PUBLICATION"></a>

`SET PUBLICATION publication_name`<br>`ADD PUBLICATION publication_name`<br>`DROP PUBLICATION publication_name` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-SETADDDROP-PUBLICATION)
:   These forms change the list of subscribed publications.
    `SET`
    replaces the entire list of publications with a new list,
    `ADD` adds additional publications to the list of
    publications, and `DROP` removes the publications from
    the list of publications. We allow non-existent publications to be
    specified in `ADD` and `SET` variants
    so that users can add those later. See [CREATE SUBSCRIPTION](sql-createsubscription.md)
    for more information. By default, this command will also act like
    `REFRESH PUBLICATION`.

    *`publication_option`* specifies additional
    options for this operation. The supported options are:

    `refresh` (`boolean`)
    :   When false, the command will not try to refresh table information.
        `REFRESH PUBLICATION` should then be executed separately.
        The default is `true`.

    Additionally, the options described under
    `REFRESH PUBLICATION` may be specified, to control the
    implicit refresh operation.
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION"></a>

`REFRESH PUBLICATION` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION)
:   Fetch missing table information from publisher. This will start
    replication of tables that were added to the subscribed-to publications
    since [`CREATE SUBSCRIPTION`](sql-createsubscription.md) or
    the last invocation of `REFRESH PUBLICATION`.

    *`refresh_option`* specifies additional options for the
    refresh operation. The supported options are:

    `copy_data` (`boolean`)
    :   Specifies whether to copy pre-existing data in the publications
        that are being subscribed to when the replication starts.
        The default is `true`.

        Previously subscribed tables are not copied, even if a table's row
        filter `WHERE` clause has since been modified.

        See [Notes](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES) for details of
        how `copy_data = true` can interact with the
        [`origin`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-ORIGIN)
        parameter.

        See the
        [`binary`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY)
        parameter of `CREATE SUBSCRIPTION` for details about
        copying pre-existing data in binary format.
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE"></a>

`ENABLE` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE)
:   Enables a previously disabled subscription, starting the logical
    replication worker at the end of the transaction.
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE"></a>

`DISABLE` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE)
:   Disables a running subscription, stopping the logical replication
    worker at the end of the transaction.
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-SET"></a>

`SET ( subscription_parameter [= value] [, ... ] )` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-SET)
:   This clause alters parameters originally set by
    [CREATE SUBSCRIPTION](sql-createsubscription.md). See there for more
    information. The parameters that can be altered are
    [`slot_name`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME),
    [`synchronous_commit`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SYNCHRONOUS-COMMIT),
    [`binary`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY),
    [`streaming`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING),
    [`disable_on_error`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-DISABLE-ON-ERROR),
    [`password_required`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-PASSWORD-REQUIRED),
    [`run_as_owner`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-RUN-AS-OWNER),
    [`origin`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-ORIGIN),
    [`failover`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER), and
    [`two_phase`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE).
    Only a superuser can set `password_required = false`.

    When altering the
    [`slot_name`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME),
    the `failover` and `two_phase` property
    values of the named slot may differ from the counterpart
    [`failover`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER)
    and [`two_phase`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE)
    parameters specified in the subscription. When creating the slot, ensure
    the slot properties `failover` and `two_phase`
    match their counterpart parameters of the subscription.
    Otherwise, the slot on the publisher may behave differently from what these
    subscription options say: for example, the slot on the publisher could either be
    synced to the standbys even when the subscription's
    [`failover`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER)
    option is disabled or could be disabled for sync
    even when the subscription's
    [`failover`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER)
    option is enabled.

    The [`failover`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER)
    and [`two_phase`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE)
    parameters can only be altered when the subscription is disabled.

    When altering [`two_phase`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE)
    from `true` to `false`, the backend
    process reports an error if any prepared transactions done by the
    logical replication worker (from when `two_phase`
    parameter was still `true`) are found. You can resolve
    prepared transactions on the publisher node, or manually roll them back
    on the subscriber, and then try again. The transactions prepared by
    logical replication worker corresponding to a particular subscription have
    the following pattern: “`pg_gid_%u_%u`”
    (parameters: subscription *`oid`*, remote transaction id *`xid`*).
    To resolve such transactions manually, you need to roll back all
    the prepared transactions with corresponding subscription IDs in their
    names. Applications can check
    [`pg_prepared_xacts`](../../internals/views/view-pg-prepared-xacts.md)
    to find the required prepared transactions. After the `two_phase`
    option is changed from `true` to `false`,
    the publisher will replicate the transactions again when they are committed.
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-SKIP"></a>

`SKIP ( skip_option = value )` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-SKIP)
:   Skips applying all changes of the remote transaction. If incoming data
    violates any constraints, logical replication will stop until it is
    resolved. By using the `ALTER SUBSCRIPTION ... SKIP` command,
    the logical replication worker skips all data modification changes within
    the transaction. This option has no effect on the transactions that are
    already prepared by enabling
    [`two_phase`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE)
    on the subscriber.
    After the logical replication worker successfully skips the transaction or
    finishes a transaction, the LSN (stored in
    `pg_subscription`.`subskiplsn`)
    is cleared. See [Section 29.7](../../server-administration/logical-replication/logical-replication-conflicts.md) for
    the details of logical replication conflicts.

    *`skip_option`* specifies options for this operation.
    The supported option is:

    `lsn` (`pg_lsn`)
    :   Specifies the finish LSN of the remote transaction whose changes
        are to be skipped by the logical replication worker. The finish LSN
        is the LSN at which the transaction is either committed or prepared.
        Skipping individual subtransactions is not supported. Setting
        `NONE` resets the LSN.
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-NEW-OWNER"></a>

*`new_owner`* [#](#SQL-ALTERSUBSCRIPTION-PARAMS-NEW-OWNER)
:   The user name of the new owner of the subscription.
<a id="SQL-ALTERSUBSCRIPTION-PARAMS-NEW-NAME"></a>

*`new_name`* [#](#SQL-ALTERSUBSCRIPTION-PARAMS-NEW-NAME)
:   The new name for the subscription.

When specifying a parameter of type `boolean`, the
`=` *`value`*
part can be omitted, which is equivalent to
specifying `TRUE`.

<a id="id-1.9.3.33.7"></a>

## Examples

Change the publication subscribed by a subscription to
`insert_only`:

```

ALTER SUBSCRIPTION mysub SET PUBLICATION insert_only;
```

Disable (stop) the subscription:

```

ALTER SUBSCRIPTION mysub DISABLE;
```

<a id="id-1.9.3.33.8"></a>

## Compatibility

`ALTER SUBSCRIPTION` is a PostgreSQL
extension.

<a id="id-1.9.3.33.9"></a>

## See Also

[CREATE SUBSCRIPTION](sql-createsubscription.md), [DROP SUBSCRIPTION](sql-dropsubscription.md), [CREATE PUBLICATION](sql-createpublication.md), [ALTER PUBLICATION](sql-alterpublication.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altersubscription.html)（英文原文，待翻譯）
