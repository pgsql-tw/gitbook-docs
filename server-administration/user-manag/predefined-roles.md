## 21.5. Predefined Roles [#](#PREDEFINED-ROLES)

<a id="id-1.6.8.9.2"></a>

PostgreSQL provides a set of predefined roles
that provide access to certain, commonly needed, privileged capabilities
and information. Administrators (including roles that have the
`CREATEROLE` privilege) can `GRANT` these
roles to users and/or other roles in their environment, providing those
users with access to the specified capabilities and information. For
example:

```

GRANT pg_signal_backend TO admin_user;
```

### Warning

Care should be taken when granting these roles to ensure they are only used
where needed and with the understanding that these roles grant access to
privileged information.

The predefined roles are described below.
Note that the specific permissions for each of the roles may change in
the future as additional capabilities are added. Administrators
should monitor the release notes for changes.

<a id="PREDEFINED-ROLE-PG-CHECKPOINT"></a>

`pg_checkpoint` [#](#PREDEFINED-ROLE-PG-CHECKPOINT)
:   `pg_checkpoint` allows executing the
    [`CHECKPOINT`](../../reference/sql-commands/sql-checkpoint.md) command.
<a id="PREDEFINED-ROLE-PG-CREATE-SUBSCRIPTION"></a>

`pg_create_subscription` [#](#PREDEFINED-ROLE-PG-CREATE-SUBSCRIPTION)
:   `pg_create_subscription` allows users with
    `CREATE` permission on the database to issue
    [`CREATE SUBSCRIPTION`](../../reference/sql-commands/sql-createsubscription.md).
<a id="PREDEFINED-ROLE-PG-DATABASE-OWNER"></a>

`pg_database_owner` [#](#PREDEFINED-ROLE-PG-DATABASE-OWNER)
:   `pg_database_owner` always has exactly one implicit
    member: the current database owner. It cannot be granted membership in
    any role, and no role can be granted membership in
    `pg_database_owner`. However, like any other role, it
    can own objects and receive grants of access privileges. Consequently,
    once `pg_database_owner` has rights within a template
    database, each owner of a database instantiated from that template will
    possess those rights. Initially, this role owns the
    `public` schema, so each database owner governs local
    use of that schema.
<a id="PREDEFINED-ROLE-PG-MAINTAIN"></a>

`pg_maintain` [#](#PREDEFINED-ROLE-PG-MAINTAIN)
:   `pg_maintain` allows executing
    [`VACUUM`](../../reference/sql-commands/sql-vacuum.md),
    [`ANALYZE`](../../reference/sql-commands/sql-analyze.md),
    [`CLUSTER`](../../reference/sql-commands/sql-cluster.md),
    [`REFRESH MATERIALIZED VIEW`](../../reference/sql-commands/sql-refreshmaterializedview.md),
    [`REINDEX`](../../reference/sql-commands/sql-reindex.md),
    and [`LOCK TABLE`](../../reference/sql-commands/sql-lock.md) on all
    relations, as if having `MAINTAIN` rights on those
    objects.
<a id="PREDEFINED-ROLE-PG-MONITOR"></a>

`pg_monitor`<br>`pg_read_all_settings`<br>`pg_read_all_stats`<br>`pg_stat_scan_tables` [#](#PREDEFINED-ROLE-PG-MONITOR)
:   These roles are intended to allow administrators to easily configure a
    role for the purpose of monitoring the database server. They grant a
    set of common privileges allowing the role to read various useful
    configuration settings, statistics, and other system information
    normally restricted to superusers.

    `pg_monitor` allows reading/executing various
    monitoring views and functions. This role is a member of
    `pg_read_all_settings`,
    `pg_read_all_stats` and
    `pg_stat_scan_tables`.

    `pg_read_all_settings` allows reading all configuration
    variables, even those normally visible only to superusers.

    `pg_read_all_stats` allows reading all pg_stat_\* views
    and use various statistics related extensions, even those normally
    visible only to superusers.

    `pg_stat_scan_tables` allows executing monitoring
    functions that may take `ACCESS SHARE` locks on tables,
    potentially for a long time (e.g., `pgrowlocks(text)`
    in the [pgrowlocks](../../appendixes/contrib/pgrowlocks.md) extension).
<a id="PREDEFINED-ROLE-PG-READ-ALL-DATA"></a>

`pg_read_all_data`<br>`pg_write_all_data` [#](#PREDEFINED-ROLE-PG-READ-ALL-DATA)
:   `pg_read_all_data` allows reading all data (tables,
    views, sequences), as if having `SELECT` rights on
    those objects and `USAGE` rights on all schemas. This
    role does not bypass row-level security (RLS) policies. If RLS is being
    used, an administrator may wish to set `BYPASSRLS` on
    roles which this role is granted to.

    `pg_write_all_data` allows writing all data (tables,
    views, sequences), as if having `INSERT`,
    `UPDATE`, and `DELETE` rights on those
    objects and `USAGE` rights on all schemas. This role
    does not bypass row-level security (RLS) policies. If RLS is being
    used, an administrator may wish to set `BYPASSRLS` on
    roles which this role is granted to.
<a id="PREDEFINED-ROLE-PG-READ-SERVER-FILES"></a>

`pg_read_server_files`<br>`pg_write_server_files`<br>`pg_execute_server_program` [#](#PREDEFINED-ROLE-PG-READ-SERVER-FILES)
:   These roles are intended to allow administrators to have trusted, but
    non-superuser, roles which are able to access files and run programs on
    the database server as the user the database runs as. They bypass all
    database-level permission checks when accessing files directly and they
    could be used to gain superuser-level access. Therefore, great care
    should be taken when granting these roles to users.

    `pg_read_server_files` allows reading files from any
    location the database can access on the server using
    `COPY` and other file-access functions.

    `pg_write_server_files` allows writing to files in any
    location the database can access on the server using
    `COPY` and other file-access functions.

    `pg_execute_server_program` allows executing programs
    on the database server as the user the database runs as using
    `COPY` and other functions which allow executing a
    server-side program.
<a id="PREDEFINED-ROLE-PG-SIGNAL-AUTOVACUUM-WORKER"></a>

`pg_signal_autovacuum_worker` [#](#PREDEFINED-ROLE-PG-SIGNAL-AUTOVACUUM-WORKER)
:   `pg_signal_autovacuum_worker` allows signaling
    autovacuum workers to cancel the current table's vacuum or terminate its
    session. See [Section 9.28.2](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL).
<a id="PREDEFINED-ROLE-PG-SIGNAL-BACKEND"></a>

`pg_signal_backend` [#](#PREDEFINED-ROLE-PG-SIGNAL-BACKEND)
:   `pg_signal_backend` allows signaling another backend to
    cancel a query or terminate its session. Note that this role does not
    permit signaling backends owned by a superuser. See
    [Section 9.28.2](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL).
<a id="PREDEFINED-ROLE-PG-USE-RESERVED-CONNECTIONS"></a>

`pg_use_reserved_connections` [#](#PREDEFINED-ROLE-PG-USE-RESERVED-CONNECTIONS)
:   `pg_use_reserved_connections` allows use of connection
    slots reserved via [reserved_connections](../runtime-config/runtime-config-connection.md#GUC-RESERVED-CONNECTIONS).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/predefined-roles.html)（英文原文，待翻譯）
