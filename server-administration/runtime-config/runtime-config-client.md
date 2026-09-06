## 19.11. Client Connection Defaults [#](#RUNTIME-CONFIG-CLIENT)

[19.11.1. Statement Behavior](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-STATEMENT)

[19.11.2. Locale and Formatting](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-FORMAT)

[19.11.3. Shared Library Preloading](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-PRELOAD)

[19.11.4. Other Defaults](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-OTHER)

<a id="RUNTIME-CONFIG-CLIENT-STATEMENT"></a>

### 19.11.1. Statement Behavior [#](#RUNTIME-CONFIG-CLIENT-STATEMENT)

<a id="GUC-CLIENT-MIN-MESSAGES"></a>

`client_min_messages` (`enum`) <a id="id-1.6.6.14.2.2.1.1.3"></a> [#](#GUC-CLIENT-MIN-MESSAGES)
:   Controls which
    [message levels](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS)
    are sent to the client.
    Valid values are `DEBUG5`,
    `DEBUG4`, `DEBUG3`, `DEBUG2`,
    `DEBUG1`, `LOG`, `NOTICE`,
    `WARNING`, and `ERROR`.
    Each level includes all the levels that follow it. The later the level,
    the fewer messages are sent. The default is
    `NOTICE`. Note that `LOG` has a different
    rank here than in [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES).

    `INFO` level messages are always sent to the client.
<a id="GUC-SEARCH-PATH"></a>

`search_path` (`string`) <a id="id-1.6.6.14.2.2.2.1.3"></a> <a id="id-1.6.6.14.2.2.2.1.4"></a> [#](#GUC-SEARCH-PATH)
:   This variable specifies the order in which schemas are searched
    when an object (table, data type, function, etc.) is referenced by a
    simple name with no schema specified. When there are objects of
    identical names in different schemas, the one found first
    in the search path is used. An object that is not in any of the
    schemas in the search path can only be referenced by specifying
    its containing schema with a qualified (dotted) name.

    The value for `search_path` must be a comma-separated
    list of schema names. Any name that is not an existing schema, or is
    a schema for which the user does not have `USAGE`
    permission, is silently ignored.

    If one of the list items is the special name
    `$user`, then the schema having the name returned by
    `CURRENT_USER` is substituted, if there is such a schema
    and the user has `USAGE` permission for it.
    (If not, `$user` is ignored.)

    The system catalog schema, `pg_catalog`, is always
    searched, whether it is mentioned in the path or not. If it is
    mentioned in the path then it will be searched in the specified
    order. If `pg_catalog` is not in the path then it will
    be searched *before* searching any of the path items.

    Likewise, the current session's temporary-table schema,
    `pg_temp_nnn`, is always searched if it
    exists. It can be explicitly listed in the path by using the
    alias `pg_temp`<a id="id-1.6.6.14.2.2.2.2.5.3"></a>. If it is not listed in the path then
    it is searched first (even before `pg_catalog`). However,
    the temporary schema is only searched for relation (table, view,
    sequence, etc.) and data type names. It is never searched for
    function or operator names.

    When objects are created without specifying a particular target
    schema, they will be placed in the first valid schema named in
    `search_path`. An error is reported if the search
    path is empty.

    The default value for this parameter is
    `"$user", public`.
    This setting supports shared use of a database (where no users
    have private schemas, and all share use of `public`),
    private per-user schemas, and combinations of these. Other
    effects can be obtained by altering the default search path
    setting, either globally or per-user.

    For more information on schema handling, see
    [Section 5.10](../../the-sql-language/ddl/ddl-schemas.md). In particular, the default
    configuration is suitable only when the database has a single user or
    a few mutually-trusting users.

    The current effective value of the search path can be examined
    via the SQL function
    `current_schemas`
    (see [Section 9.27](../../the-sql-language/functions/functions-info.md)).
    This is not quite the same as
    examining the value of `search_path`, since
    `current_schemas` shows how the items
    appearing in `search_path` were resolved.
<a id="GUC-ROW-SECURITY"></a>

`row_security` (`boolean`) <a id="id-1.6.6.14.2.2.3.1.3"></a> [#](#GUC-ROW-SECURITY)
:   This variable controls whether to raise an error in lieu of applying a
    row security policy. When set to `on`, policies apply
    normally. When set to `off`, queries fail which would
    otherwise apply at least one policy. The default is `on`.
    Change to `off` where limited row visibility could cause
    incorrect results; for example, pg_dump makes that
    change by default. This variable has no effect on roles which bypass
    every row security policy, to wit, superusers and roles with
    the `BYPASSRLS` attribute.

    For more information on row security policies,
    see [CREATE POLICY](../../reference/sql-commands/sql-createpolicy.md).
<a id="GUC-DEFAULT-TABLE-ACCESS-METHOD"></a>

`default_table_access_method` (`string`) <a id="id-1.6.6.14.2.2.4.1.3"></a> [#](#GUC-DEFAULT-TABLE-ACCESS-METHOD)
:   This parameter specifies the default table access method to use when
    creating tables or materialized views if the `CREATE`
    command does not explicitly specify an access method, or when
    `SELECT ... INTO` is used, which does not allow
    specifying a table access method. The default is `heap`.
<a id="GUC-DEFAULT-TABLESPACE"></a>

`default_tablespace` (`string`) <a id="id-1.6.6.14.2.2.5.1.3"></a> <a id="id-1.6.6.14.2.2.5.1.4"></a> [#](#GUC-DEFAULT-TABLESPACE)
:   This variable specifies the default tablespace in which to create
    objects (tables and indexes) when a `CREATE` command does
    not explicitly specify a tablespace.

    The value is either the name of a tablespace, or an empty string
    to specify using the default tablespace of the current database.
    If the value does not match the name of any existing tablespace,
    PostgreSQL will automatically use the default
    tablespace of the current database. If a nondefault tablespace
    is specified, the user must have `CREATE` privilege
    for it, or creation attempts will fail.

    This variable is not used for temporary tables; for them,
    [temp_tablespaces](runtime-config-client.md#GUC-TEMP-TABLESPACES) is consulted instead.

    This variable is also not used when creating databases.
    By default, a new database inherits its tablespace setting from
    the template database it is copied from.

    If this parameter is set to a value other than the empty string
    when a partitioned table is created, the partitioned table's
    tablespace will be set to that value, which will be used as
    the default tablespace for partitions created in the future,
    even if `default_tablespace` has changed since then.

    For more information on tablespaces,
    see [Section 22.6](../managing-databases/manage-ag-tablespaces.md).
<a id="GUC-DEFAULT-TOAST-COMPRESSION"></a>

`default_toast_compression` (`enum`) <a id="id-1.6.6.14.2.2.6.1.3"></a> [#](#GUC-DEFAULT-TOAST-COMPRESSION)
:   This variable sets the default
    [TOAST](../../internals/storage/storage-toast.md)
    compression method for values of compressible columns.
    (This can be overridden for individual columns by setting
    the `COMPRESSION` column option in
    `CREATE TABLE` or
    `ALTER TABLE`.)
    The supported compression methods are `pglz` and
    (if PostgreSQL was compiled with
    `--with-lz4`) `lz4`.
    The default is `pglz`.
<a id="GUC-TEMP-TABLESPACES"></a>

`temp_tablespaces` (`string`) <a id="id-1.6.6.14.2.2.7.1.3"></a> <a id="id-1.6.6.14.2.2.7.1.4"></a> [#](#GUC-TEMP-TABLESPACES)
:   This variable specifies tablespaces in which to create temporary
    objects (temp tables and indexes on temp tables) when a
    `CREATE` command does not explicitly specify a tablespace.
    Temporary files for purposes such as sorting large data sets
    are also created in these tablespaces.

    The value is a list of names of tablespaces. When there is more than
    one name in the list, PostgreSQL chooses a random
    member of the list each time a temporary object is to be created;
    except that within a transaction, successively created temporary
    objects are placed in successive tablespaces from the list.
    If the selected element of the list is an empty string,
    PostgreSQL will automatically use the default
    tablespace of the current database instead.

    When `temp_tablespaces` is set interactively, specifying a
    nonexistent tablespace is an error, as is specifying a tablespace for
    which the user does not have `CREATE` privilege. However,
    when using a previously set value, nonexistent tablespaces are
    ignored, as are tablespaces for which the user lacks
    `CREATE` privilege. In particular, this rule applies when
    using a value set in `postgresql.conf`.

    The default value is an empty string, which results in all temporary
    objects being created in the default tablespace of the current
    database.

    See also [default_tablespace](runtime-config-client.md#GUC-DEFAULT-TABLESPACE).
<a id="GUC-CHECK-FUNCTION-BODIES"></a>

`check_function_bodies` (`boolean`) <a id="id-1.6.6.14.2.2.8.1.3"></a> [#](#GUC-CHECK-FUNCTION-BODIES)
:   This parameter is normally on. When set to `off`, it
    disables validation of the routine body string during [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md) and [CREATE PROCEDURE](../../reference/sql-commands/sql-createprocedure.md). Disabling validation avoids side
    effects of the validation process, in particular preventing false
    positives due to problems such as forward references.
    Set this parameter
    to `off` before loading functions on behalf of other
    users; pg_dump does so automatically.
<a id="GUC-DEFAULT-TRANSACTION-ISOLATION"></a>

`default_transaction_isolation` (`enum`) <a id="id-1.6.6.14.2.2.9.1.3"></a> <a id="id-1.6.6.14.2.2.9.1.4"></a> [#](#GUC-DEFAULT-TRANSACTION-ISOLATION)
:   Each SQL transaction has an isolation level, which can be
    either “read uncommitted”, “read
    committed”, “repeatable read”, or
    “serializable”. This parameter controls the
    default isolation level of each new transaction. The default
    is “read committed”.

    Consult [Chapter 13](../../the-sql-language/mvcc/README.md) and [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) for more information.
<a id="GUC-DEFAULT-TRANSACTION-READ-ONLY"></a>

`default_transaction_read_only` (`boolean`) <a id="id-1.6.6.14.2.2.10.1.3"></a> <a id="id-1.6.6.14.2.2.10.1.4"></a> [#](#GUC-DEFAULT-TRANSACTION-READ-ONLY)
:   A read-only SQL transaction cannot alter non-temporary tables.
    This parameter controls the default read-only status of each new
    transaction. The default is `off` (read/write).

    Consult [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) for more information.
<a id="GUC-DEFAULT-TRANSACTION-DEFERRABLE"></a>

`default_transaction_deferrable` (`boolean`) <a id="id-1.6.6.14.2.2.11.1.3"></a> <a id="id-1.6.6.14.2.2.11.1.4"></a> [#](#GUC-DEFAULT-TRANSACTION-DEFERRABLE)
:   When running at the `serializable` isolation level,
    a deferrable read-only SQL transaction may be delayed before
    it is allowed to proceed. However, once it begins executing
    it does not incur any of the overhead required to ensure
    serializability; so serialization code will have no reason to
    force it to abort because of concurrent updates, making this
    option suitable for long-running read-only transactions.

    This parameter controls the default deferrable status of each
    new transaction. It currently has no effect on read-write
    transactions or those operating at isolation levels lower
    than `serializable`. The default is `off`.

    Consult [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) for more information.
<a id="GUC-TRANSACTION-ISOLATION"></a>

`transaction_isolation` (`enum`) <a id="id-1.6.6.14.2.2.12.1.3"></a> <a id="id-1.6.6.14.2.2.12.1.4"></a> [#](#GUC-TRANSACTION-ISOLATION)
:   This parameter reflects the current transaction's isolation level.
    At the beginning of each transaction, it is set to the current value
    of [default_transaction_isolation](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-ISOLATION).
    Any subsequent attempt to change it is equivalent to a [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) command.
<a id="GUC-TRANSACTION-READ-ONLY"></a>

`transaction_read_only` (`boolean`) <a id="id-1.6.6.14.2.2.13.1.3"></a> <a id="id-1.6.6.14.2.2.13.1.4"></a> [#](#GUC-TRANSACTION-READ-ONLY)
:   This parameter reflects the current transaction's read-only status.
    At the beginning of each transaction, it is set to the current value
    of [default_transaction_read_only](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-READ-ONLY).
    Any subsequent attempt to change it is equivalent to a [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) command.
<a id="GUC-TRANSACTION-DEFERRABLE"></a>

`transaction_deferrable` (`boolean`) <a id="id-1.6.6.14.2.2.14.1.3"></a> <a id="id-1.6.6.14.2.2.14.1.4"></a> [#](#GUC-TRANSACTION-DEFERRABLE)
:   This parameter reflects the current transaction's deferrability status.
    At the beginning of each transaction, it is set to the current value
    of [default_transaction_deferrable](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-DEFERRABLE).
    Any subsequent attempt to change it is equivalent to a [SET TRANSACTION](../../reference/sql-commands/sql-set-transaction.md) command.
<a id="GUC-SESSION-REPLICATION-ROLE"></a>

`session_replication_role` (`enum`) <a id="id-1.6.6.14.2.2.15.1.3"></a> [#](#GUC-SESSION-REPLICATION-ROLE)
:   Controls firing of replication-related triggers and rules for the
    current session.
    Possible values are `origin` (the default),
    `replica` and `local`.
    Setting this parameter results in discarding any previously cached
    query plans.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.

    The intended use of this setting is that logical replication systems
    set it to `replica` when they are applying replicated
    changes. The effect of that will be that triggers and rules (that
    have not been altered from their default configuration) will not fire
    on the replica. See the [`ALTER TABLE`](../../reference/sql-commands/sql-altertable.md) clauses
    `ENABLE TRIGGER` and `ENABLE RULE`
    for more information.

    PostgreSQL treats the settings `origin` and
    `local` the same internally. Third-party replication
    systems may use these two values for their internal purposes, for
    example using `local` to designate a session whose
    changes should not be replicated.

    Since foreign keys are implemented as triggers, setting this parameter
    to `replica` also disables all foreign key checks,
    which can leave data in an inconsistent state if improperly used.
<a id="GUC-STATEMENT-TIMEOUT"></a>

`statement_timeout` (`integer`) <a id="id-1.6.6.14.2.2.16.1.3"></a> [#](#GUC-STATEMENT-TIMEOUT)
:   Abort any statement that takes more than the specified amount of time.
    If `log_min_error_statement` is set
    to `ERROR` or lower, the statement that timed out
    will also be logged.
    If this value is specified without units, it is taken as milliseconds.
    A value of zero (the default) disables the timeout.

    The timeout is measured from the time a command arrives at the
    server until it is completed by the server. If multiple SQL
    statements appear in a single simple-query message, the timeout
    is applied to each statement separately.
    (PostgreSQL versions before 13 usually
    treated the timeout as applying to the whole query string.)
    In extended query protocol, the timeout starts running when any
    query-related message (Parse, Bind, Execute, Describe) arrives, and
    it is canceled by completion of an Execute or Sync message.

    Setting `statement_timeout` in
    `postgresql.conf` is not recommended because it would
    affect all sessions.
<a id="GUC-TRANSACTION-TIMEOUT"></a>

`transaction_timeout` (`integer`) <a id="id-1.6.6.14.2.2.17.1.3"></a> [#](#GUC-TRANSACTION-TIMEOUT)
:   Terminate any session that spans longer than the specified amount of
    time in a transaction. The limit applies both to explicit transactions
    (started with `BEGIN`) and to an implicitly started
    transaction corresponding to a single statement.
    If this value is specified without units, it is taken as milliseconds.
    A value of zero (the default) disables the timeout.

    If `transaction_timeout` is shorter or equal to
    `idle_in_transaction_session_timeout` or `statement_timeout`
    then the longer timeout is ignored.

    Setting `transaction_timeout` in
    `postgresql.conf` is not recommended because it would
    affect all sessions.

    ### Note

    Prepared transactions are not subject to this timeout.
<a id="GUC-LOCK-TIMEOUT"></a>

`lock_timeout` (`integer`) <a id="id-1.6.6.14.2.2.18.1.3"></a> [#](#GUC-LOCK-TIMEOUT)
:   Abort any statement that waits longer than the specified amount of
    time while attempting to acquire a lock on a table, index,
    row, or other database object. The time limit applies separately to
    each lock acquisition attempt. The limit applies both to explicit
    locking requests (such as `LOCK TABLE`, or `SELECT
    FOR UPDATE` without `NOWAIT`) and to implicitly-acquired
    locks.
    If this value is specified without units, it is taken as milliseconds.
    A value of zero (the default) disables the timeout.

    Unlike `statement_timeout`, this timeout can only occur
    while waiting for locks. Note that if `statement_timeout`
    is nonzero, it is rather pointless to set `lock_timeout` to
    the same or larger value, since the statement timeout would always
    trigger first. If `log_min_error_statement` is set to
    `ERROR` or lower, the statement that timed out will be
    logged.

    Setting `lock_timeout` in
    `postgresql.conf` is not recommended because it would
    affect all sessions.
<a id="GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT"></a>

`idle_in_transaction_session_timeout` (`integer`) <a id="id-1.6.6.14.2.2.19.1.3"></a> [#](#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT)
:   Terminate any session that has been idle (that is, waiting for a
    client query) within an open transaction for longer than the
    specified amount of time.
    If this value is specified without units, it is taken as milliseconds.
    A value of zero (the default) disables the timeout.

    This option can be used to ensure that idle sessions do not hold
    locks for an unreasonable amount of time. Even when no significant
    locks are held, an open transaction prevents vacuuming away
    recently-dead tuples that may be visible only to this transaction;
    so remaining idle for a long time can contribute to table bloat.
    See [Section 24.1](../maintenance/routine-vacuuming.md) for more details.
<a id="GUC-IDLE-SESSION-TIMEOUT"></a>

`idle_session_timeout` (`integer`) <a id="id-1.6.6.14.2.2.20.1.3"></a> [#](#GUC-IDLE-SESSION-TIMEOUT)
:   Terminate any session that has been idle (that is, waiting for a
    client query), but not within an open transaction, for longer than
    the specified amount of time.
    If this value is specified without units, it is taken as milliseconds.
    A value of zero (the default) disables the timeout.

    Unlike the case with an open transaction, an idle session without a
    transaction imposes no large costs on the server, so there is less
    need to enable this timeout
    than `idle_in_transaction_session_timeout`.

    Be wary of enforcing this timeout on connections made through
    connection-pooling software or other middleware, as such a layer
    may not react well to unexpected connection closure. It may be
    helpful to enable this timeout only for interactive sessions,
    perhaps by applying it only to particular users.
<a id="GUC-BYTEA-OUTPUT"></a>

`bytea_output` (`enum`) <a id="id-1.6.6.14.2.2.21.1.3"></a> [#](#GUC-BYTEA-OUTPUT)
:   Sets the output format for values of type `bytea`.
    Valid values are `hex` (the default)
    and `escape` (the traditional PostgreSQL
    format). See [Section 8.4](../../the-sql-language/datatype/datatype-binary.md) for more
    information. The `bytea` type always
    accepts both formats on input, regardless of this setting.
<a id="GUC-XMLBINARY"></a>

`xmlbinary` (`enum`) <a id="id-1.6.6.14.2.2.22.1.3"></a> [#](#GUC-XMLBINARY)
:   Sets how binary values are to be encoded in XML. This applies
    for example when `bytea` values are converted to
    XML by the functions `xmlelement` or
    `xmlforest`. Possible values are
    `base64` and `hex`, which
    are both defined in the XML Schema standard. The default is
    `base64`. For further information about
    XML-related functions, see [Section 9.15](../../the-sql-language/functions/functions-xml.md).

    The actual choice here is mostly a matter of taste,
    constrained only by possible restrictions in client
    applications. Both methods support all possible values,
    although the hex encoding will be somewhat larger than the
    base64 encoding.
<a id="GUC-XMLOPTION"></a>

`xmloption` (`enum`) <a id="id-1.6.6.14.2.2.23.1.3"></a> <a id="id-1.6.6.14.2.2.23.1.4"></a> <a id="id-1.6.6.14.2.2.23.1.5"></a> [#](#GUC-XMLOPTION)
:   Sets whether `DOCUMENT` or
    `CONTENT` is implicit when converting between
    XML and character string values. See [Section 8.13](../../the-sql-language/datatype/datatype-xml.md) for a description of this. Valid
    values are `DOCUMENT` and
    `CONTENT`. The default is
    `CONTENT`.

    According to the SQL standard, the command to set this option is

    ```

    SET XML OPTION { DOCUMENT | CONTENT };
    ```

    This syntax is also available in PostgreSQL.
<a id="GUC-GIN-PENDING-LIST-LIMIT"></a>

`gin_pending_list_limit` (`integer`) <a id="id-1.6.6.14.2.2.24.1.3"></a> [#](#GUC-GIN-PENDING-LIST-LIMIT)
:   Sets the maximum size of a GIN index's pending list, which is used
    when `fastupdate` is enabled. If the list grows
    larger than this maximum size, it is cleaned up by moving
    the entries in it to the index's main GIN data structure in bulk.
    If this value is specified without units, it is taken as kilobytes.
    The default is four megabytes (`4MB`). This setting
    can be overridden for individual GIN indexes by changing
    index storage parameters.
    See [Section 65.4.4.1](../../internals/indextypes/gin.md#GIN-FAST-UPDATE) and [Section 65.4.5](../../internals/indextypes/gin.md#GIN-TIPS)
    for more information.
<a id="GUC-CREATEROLE-SELF-GRANT"></a>

`createrole_self_grant` (`string`) <a id="id-1.6.6.14.2.2.25.1.3"></a> [#](#GUC-CREATEROLE-SELF-GRANT)
:   If a user who has `CREATEROLE` but not
    `SUPERUSER` creates a role, and if this
    is set to a non-empty value, the newly-created role will be granted
    to the creating user with the options specified. The value must be
    `set`, `inherit`, or a
    comma-separated list of these. The default value is an empty string,
    which disables the feature.

    The purpose of this option is to allow a `CREATEROLE`
    user who is not a superuser to automatically inherit, or automatically
    gain the ability to `SET ROLE` to, any created users.
    Since a `CREATEROLE` user is always implicitly granted
    `ADMIN OPTION` on created roles, that user could
    always execute a `GRANT` statement that would achieve
    the same effect as this setting. However, it can be convenient for
    usability reasons if the grant happens automatically. A superuser
    automatically inherits the privileges of every role and can always
    `SET ROLE` to any role, and this setting can be used
    to produce a similar behavior for `CREATEROLE` users
    for users which they create.
<a id="GUC-EVENT-TRIGGERS"></a>

`event_triggers` (`boolean`) <a id="id-1.6.6.14.2.2.26.1.3"></a> [#](#GUC-EVENT-TRIGGERS)
:   Allow temporarily disabling execution of event triggers in order to
    troubleshoot and repair faulty event triggers. All event triggers will
    be disabled by setting it to `false`. Setting the value
    to `true` allows all event triggers to fire, this
    is the default value. Only superusers and users with the appropriate
    `SET` privilege can change this setting.
<a id="GUC-RESTRICT-NONSYSTEM-RELATION-KIND"></a>

`restrict_nonsystem_relation_kind` (`string`) <a id="id-1.6.6.14.2.2.27.1.3"></a> [#](#GUC-RESTRICT-NONSYSTEM-RELATION-KIND)
:   Set relation kinds for which access to non-system relations is prohibited.
    The value takes the form of a comma-separated list of relation kinds.
    Currently, the supported relation kinds are `view` and
    `foreign-table`.

<a id="RUNTIME-CONFIG-CLIENT-FORMAT"></a>

### 19.11.2. Locale and Formatting [#](#RUNTIME-CONFIG-CLIENT-FORMAT)

<a id="GUC-DATESTYLE"></a>

`DateStyle` (`string`) <a id="id-1.6.6.14.3.2.1.1.3"></a> [#](#GUC-DATESTYLE)
:   Sets the display format for date and time values, as well as the
    rules for interpreting ambiguous date input values. For
    historical reasons, this variable contains two independent
    components: the output format specification (`ISO`,
    `Postgres`, `SQL`, or `German`)
    and the input/output specification for year/month/day ordering
    (`DMY`, `MDY`, or `YMD`). These
    can be set separately or together. The keywords `Euro`
    and `European` are synonyms for `DMY`; the
    keywords `US`, `NonEuro`, and
    `NonEuropean` are synonyms for `MDY`. See
    [Section 8.5](../../the-sql-language/datatype/datatype-datetime.md) for more information. The
    built-in default is `ISO, MDY`, but
    initdb will initialize the
    configuration file with a setting that corresponds to the
    behavior of the chosen `lc_time` locale.
<a id="GUC-INTERVALSTYLE"></a>

`IntervalStyle` (`enum`) <a id="id-1.6.6.14.3.2.2.1.3"></a> [#](#GUC-INTERVALSTYLE)
:   Sets the display format for interval values.
    The value `sql_standard` will produce
    output matching SQL standard interval literals.
    The value `postgres` (which is the default) will produce
    output matching PostgreSQL releases prior to 8.4
    when the [DateStyle](runtime-config-client.md#GUC-DATESTYLE)
    parameter was set to `ISO`.
    The value `postgres_verbose` will produce output
    matching PostgreSQL releases prior to 8.4
    when the `DateStyle`
    parameter was set to non-`ISO` output.
    The value `iso_8601` will produce output matching the time
    interval “format with designators” defined in section
    4.4.3.2 of ISO 8601.

    The `IntervalStyle` parameter also affects the
    interpretation of ambiguous interval input. See
    [Section 8.5.4](../../the-sql-language/datatype/datatype-datetime.md#DATATYPE-INTERVAL-INPUT) for more information.
<a id="GUC-TIMEZONE"></a>

`TimeZone` (`string`) <a id="id-1.6.6.14.3.2.3.1.3"></a> <a id="id-1.6.6.14.3.2.3.1.4"></a> [#](#GUC-TIMEZONE)
:   Sets the time zone for displaying and interpreting time stamps.
    The built-in default is `GMT`, but that is typically
    overridden in `postgresql.conf`; initdb
    will install a setting there corresponding to its system environment.
    See [Section 8.5.3](../../the-sql-language/datatype/datatype-datetime.md#DATATYPE-TIMEZONES) for more information.
<a id="GUC-TIMEZONE-ABBREVIATIONS"></a>

`timezone_abbreviations` (`string`) <a id="id-1.6.6.14.3.2.4.1.3"></a> <a id="id-1.6.6.14.3.2.4.1.4"></a> [#](#GUC-TIMEZONE-ABBREVIATIONS)
:   Sets the collection of additional time zone abbreviations that
    will be accepted by the server for datetime input (beyond any
    abbreviations defined by the current `TimeZone`
    setting). The default is `'Default'`,
    which is a collection that works in most of the world; there are
    also `'Australia'` and `'India'`,
    and other collections can be defined for a particular installation.
    See [Section B.4](../../appendixes/datetime-appendix/datetime-config-files.md) for more information.
<a id="GUC-EXTRA-FLOAT-DIGITS"></a>

`extra_float_digits` (`integer`) <a id="id-1.6.6.14.3.2.5.1.3"></a> <a id="id-1.6.6.14.3.2.5.1.4"></a> <a id="id-1.6.6.14.3.2.5.1.5"></a> [#](#GUC-EXTRA-FLOAT-DIGITS)
:   This parameter adjusts the number of digits used for textual output of
    floating-point values, including `float4`, `float8`,
    and geometric data types.

    If the value is 1 (the default) or above, float values are output in
    shortest-precise format; see [Section 8.1.3](../../the-sql-language/datatype/datatype-numeric.md#DATATYPE-FLOAT). The
    actual number of digits generated depends only on the value being
    output, not on the value of this parameter. At most 17 digits are
    required for `float8` values, and 9 for `float4`
    values. This format is both fast and precise, preserving the original
    binary float value exactly when correctly read. For historical
    compatibility, values up to 3 are permitted.

    If the value is zero or negative, then the output is rounded to a
    given decimal precision. The precision used is the standard number of
    digits for the type (`FLT_DIG`
    or `DBL_DIG` as appropriate) reduced according to the
    value of this parameter. (For example, specifying -1 will cause
    `float4` values to be output rounded to 5 significant
    digits, and `float8` values
    rounded to 14 digits.) This format is slower and does not preserve all
    the bits of the binary float value, but may be more human-readable.

    ### Note

    The meaning of this parameter, and its default value, changed
    in PostgreSQL 12;
    see [Section 8.1.3](../../the-sql-language/datatype/datatype-numeric.md#DATATYPE-FLOAT) for further discussion.
<a id="GUC-CLIENT-ENCODING"></a>

`client_encoding` (`string`) <a id="id-1.6.6.14.3.2.6.1.3"></a> <a id="id-1.6.6.14.3.2.6.1.4"></a> [#](#GUC-CLIENT-ENCODING)
:   Sets the client-side encoding (character set).
    The default is to use the database encoding.
    The character sets supported by the PostgreSQL
    server are described in [Section 23.3.1](../charset/multibyte.md#MULTIBYTE-CHARSET-SUPPORTED).
<a id="GUC-LC-MESSAGES"></a>

`lc_messages` (`string`) <a id="id-1.6.6.14.3.2.7.1.3"></a> [#](#GUC-LC-MESSAGES)
:   Sets the language in which messages are displayed. Acceptable
    values are system-dependent; see [Section 23.1](../charset/locale.md) for
    more information. If this variable is set to the empty string
    (which is the default) then the value is inherited from the
    execution environment of the server in a system-dependent way.

    On some systems, this locale category does not exist. Setting
    this variable will still work, but there will be no effect.
    Also, there is a chance that no translated messages for the
    desired language exist. In that case you will continue to see
    the English messages.

    Only superusers and users with the appropriate `SET`
    privilege can change this setting.
<a id="GUC-LC-MONETARY"></a>

`lc_monetary` (`string`) <a id="id-1.6.6.14.3.2.8.1.3"></a> [#](#GUC-LC-MONETARY)
:   Sets the locale to use for formatting monetary amounts, for
    example with the `to_char` family of
    functions. Acceptable values are system-dependent; see [Section 23.1](../charset/locale.md) for more information. If this variable is
    set to the empty string (which is the default) then the value
    is inherited from the execution environment of the server in a
    system-dependent way.
<a id="GUC-LC-NUMERIC"></a>

`lc_numeric` (`string`) <a id="id-1.6.6.14.3.2.9.1.3"></a> [#](#GUC-LC-NUMERIC)
:   Sets the locale to use for formatting numbers, for example
    with the `to_char` family of
    functions. Acceptable values are system-dependent; see [Section 23.1](../charset/locale.md) for more information. If this variable is
    set to the empty string (which is the default) then the value
    is inherited from the execution environment of the server in a
    system-dependent way.
<a id="GUC-LC-TIME"></a>

`lc_time` (`string`) <a id="id-1.6.6.14.3.2.10.1.3"></a> [#](#GUC-LC-TIME)
:   Sets the locale to use for formatting dates and times, for example
    with the `to_char` family of
    functions. Acceptable values are system-dependent; see [Section 23.1](../charset/locale.md) for more information. If this variable is
    set to the empty string (which is the default) then the value
    is inherited from the execution environment of the server in a
    system-dependent way.
<a id="GUC-ICU-VALIDATION-LEVEL"></a>

`icu_validation_level` (`enum`) <a id="id-1.6.6.14.3.2.11.1.3"></a> [#](#GUC-ICU-VALIDATION-LEVEL)
:   When ICU locale validation problems are encountered, controls which
    [message level](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS) is
    used to report the problem. Valid values are
    `DISABLED`, `DEBUG5`,
    `DEBUG4`, `DEBUG3`,
    `DEBUG2`, `DEBUG1`,
    `INFO`, `NOTICE`,
    `WARNING`, `ERROR`, and
    `LOG`.

    If set to `DISABLED`, does not report validation
    problems at all. Otherwise reports problems at the given message
    level. The default is `WARNING`.
<a id="GUC-DEFAULT-TEXT-SEARCH-CONFIG"></a>

`default_text_search_config` (`string`) <a id="id-1.6.6.14.3.2.12.1.3"></a> [#](#GUC-DEFAULT-TEXT-SEARCH-CONFIG)
:   Selects the text search configuration that is used by those variants
    of the text search functions that do not have an explicit argument
    specifying the configuration.
    See [Chapter 12](../../the-sql-language/textsearch/README.md) for further information.
    The built-in default is `pg_catalog.simple`, but
    initdb will initialize the
    configuration file with a setting that corresponds to the
    chosen `lc_ctype` locale, if a configuration
    matching that locale can be identified.

<a id="RUNTIME-CONFIG-CLIENT-PRELOAD"></a>

### 19.11.3. Shared Library Preloading [#](#RUNTIME-CONFIG-CLIENT-PRELOAD)

Several settings are available for preloading shared libraries into the
server, in order to load additional functionality or achieve performance
benefits. For example, a setting of
`'$libdir/mylib'` would cause
`mylib.so` (or on some platforms,
`mylib.sl`) to be preloaded from the installation's standard
library directory. The differences between the settings are when they
take effect and what privileges are required to change them.

PostgreSQL procedural language libraries can
be preloaded in this way, typically by using the
syntax `'$libdir/plXXX'` where
`XXX` is `pgsql`, `perl`,
`tcl`, or `python`.

Only shared libraries specifically intended to be used with PostgreSQL
can be loaded this way. Every PostgreSQL-supported library has
a “magic block” that is checked to guarantee compatibility. For
this reason, non-PostgreSQL libraries cannot be loaded in this way. You
might be able to use operating-system facilities such
as `LD_PRELOAD` for that.

In general, refer to the documentation of a specific module for the
recommended way to load that module.

<a id="GUC-LOCAL-PRELOAD-LIBRARIES"></a>

`local_preload_libraries` (`string`) <a id="id-1.6.6.14.4.6.1.1.3"></a> <a id="id-1.6.6.14.4.6.1.1.4"></a> [#](#GUC-LOCAL-PRELOAD-LIBRARIES)
:   This variable specifies one or more shared libraries that are to be
    preloaded at connection start.
    It contains a comma-separated list of library names, where each name
    is interpreted as for the [`LOAD`](../../reference/sql-commands/sql-load.md) command.
    Whitespace between entries is ignored; surround a library name with
    double quotes if you need to include whitespace or commas in the name.
    The parameter value only takes effect at the start of the connection.
    Subsequent changes have no effect. If a specified library is not
    found, the connection attempt will fail.

    This option can be set by any user. Because of that, the libraries
    that can be loaded are restricted to those appearing in the
    `plugins` subdirectory of the installation's
    standard library directory. (It is the database administrator's
    responsibility to ensure that only “safe” libraries
    are installed there.) Entries in `local_preload_libraries`
    can specify this directory explicitly, for example
    `$libdir/plugins/mylib`, or just specify
    the library name — `mylib` would have
    the same effect as `$libdir/plugins/mylib`.

    The intent of this feature is to allow unprivileged users to load
    debugging or performance-measurement libraries into specific sessions
    without requiring an explicit `LOAD` command. To that end,
    it would be typical to set this parameter using
    the `PGOPTIONS` environment variable on the client or by
    using
    `ALTER ROLE SET`.

    However, unless a module is specifically designed to be used in this way by
    non-superusers, this is usually not the right setting to use. Look
    at [session_preload_libraries](runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES) instead.
<a id="GUC-SESSION-PRELOAD-LIBRARIES"></a>

`session_preload_libraries` (`string`) <a id="id-1.6.6.14.4.6.2.1.3"></a> [#](#GUC-SESSION-PRELOAD-LIBRARIES)
:   This variable specifies one or more shared libraries that are to be
    preloaded at connection start.
    It contains a comma-separated list of library names, where each name
    is interpreted as for the [`LOAD`](../../reference/sql-commands/sql-load.md) command.
    Whitespace between entries is ignored; surround a library name with
    double quotes if you need to include whitespace or commas in the name.
    The parameter value only takes effect at the start of the connection.
    Subsequent changes have no effect. If a specified library is not
    found, the connection attempt will fail.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.

    The intent of this feature is to allow debugging or
    performance-measurement libraries to be loaded into specific sessions
    without an explicit
    `LOAD` command being given. For
    example, [auto_explain](../../appendixes/contrib/auto-explain.md) could be enabled for all
    sessions under a given user name by setting this parameter
    with `ALTER ROLE SET`. Also, this parameter can be changed
    without restarting the server (but changes only take effect when a new
    session is started), so it is easier to add new modules this way, even
    if they should apply to all sessions.

    Unlike [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES), there is no large
    performance advantage to loading a library at session start rather than
    when it is first used. There is some advantage, however, when
    connection pooling is used.
<a id="GUC-SHARED-PRELOAD-LIBRARIES"></a>

`shared_preload_libraries` (`string`) <a id="id-1.6.6.14.4.6.3.1.3"></a> [#](#GUC-SHARED-PRELOAD-LIBRARIES)
:   This variable specifies one or more shared libraries to be preloaded at
    server start.
    It contains a comma-separated list of library names, where each name
    is interpreted as for the [`LOAD`](../../reference/sql-commands/sql-load.md) command.
    Whitespace between entries is ignored; surround a library name with
    double quotes if you need to include whitespace or commas in the name.
    This parameter can only be set at server start. If a specified
    library is not found, the server will fail to start.

    Some libraries need to perform certain operations that can only take
    place at postmaster start, such as allocating shared memory, reserving
    light-weight locks, or starting background workers. Those libraries
    must be loaded at server start through this parameter. See the
    documentation of each library for details.

    Other libraries can also be preloaded. By preloading a shared library,
    the library startup time is avoided when the library is first used.
    However, the time to start each new server process might increase
    slightly, even if that process never uses the library. So this
    parameter is recommended only for libraries that will be used in most
    sessions. Also, changing this parameter requires a server restart, so
    this is not the right setting to use for short-term debugging tasks,
    say. Use [session_preload_libraries](runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES) for that
    instead.

    ### Note

    On Windows hosts, preloading a library at server start will not reduce
    the time required to start each new server process; each server process
    will re-load all preload libraries. However, `shared_preload_libraries` is still useful on Windows hosts for libraries that need to
    perform operations at postmaster start time.
<a id="GUC-JIT-PROVIDER"></a>

`jit_provider` (`string`) <a id="id-1.6.6.14.4.6.4.1.3"></a> [#](#GUC-JIT-PROVIDER)
:   This variable is the name of the JIT provider library to be used
    (see [Section 30.4.2](../jit/jit-extensibility.md#JIT-PLUGGABLE)).
    The default is `llvmjit`.
    This parameter can only be set at server start.

    If set to a non-existent library, JIT will not be
    available, but no error will be raised. This allows JIT support to be
    installed separately from the main
    PostgreSQL package.

<a id="RUNTIME-CONFIG-CLIENT-OTHER"></a>

### 19.11.4. Other Defaults [#](#RUNTIME-CONFIG-CLIENT-OTHER)

<a id="GUC-DYNAMIC-LIBRARY-PATH"></a>

`dynamic_library_path` (`string`) <a id="id-1.6.6.14.5.2.1.1.3"></a> <a id="id-1.6.6.14.5.2.1.1.4"></a> [#](#GUC-DYNAMIC-LIBRARY-PATH)
:   If a dynamically loadable module needs to be opened and the
    file name specified in the `CREATE FUNCTION` or
    `LOAD` command
    does not have a directory component (i.e., the
    name does not contain a slash), the system will search this
    path for the required file.

    The value for `dynamic_library_path` must be a
    list of absolute directory paths separated by colons (or semi-colons
    on Windows). If a list element starts
    with the special string `$libdir`, the
    compiled-in PostgreSQL package
    library directory is substituted for `$libdir`; this
    is where the modules provided by the standard
    PostgreSQL distribution are installed.
    (Use `pg_config --pkglibdir` to find out the name of
    this directory.) For example:

    ```

    dynamic_library_path = '/usr/local/lib/postgresql:/home/my_project/lib:$libdir'
    ```

    or, in a Windows environment:

    ```

    dynamic_library_path = 'C:\tools\postgresql;H:\my_project\lib;$libdir'
    ```

    The default value for this parameter is
    `'$libdir'`. If the value is set to an empty
    string, the automatic path search is turned off.

    This parameter can be changed at run time by superusers and users
    with the appropriate `SET` privilege, but a
    setting done that way will only persist until the end of the
    client connection, so this method should be reserved for
    development purposes. The recommended way to set this parameter
    is in the `postgresql.conf` configuration
    file.
<a id="GUC-EXTENSION-CONTROL-PATH"></a>

`extension_control_path` (`string`) <a id="id-1.6.6.14.5.2.2.1.3"></a> [#](#GUC-EXTENSION-CONTROL-PATH)
:   A path to search for extensions, specifically extension control files
    (`name.control`). The
    remaining extension script and secondary control files are then loaded
    from the same directory where the primary control file was found.
    See [Section 36.17.1](../../server-programming/extend/extend-extensions.md#EXTEND-EXTENSIONS-FILES) for details.

    The value for `extension_control_path` must be a
    list of absolute directory paths separated by colons (or semi-colons
    on Windows). If a list element starts
    with the special string `$system`, the
    compiled-in PostgreSQL extension
    directory is substituted for `$system`; this
    is where the extensions provided by the standard
    PostgreSQL distribution are installed.
    (Use `pg_config --sharedir` to find out the name of
    this directory.) For example:

    ```

    extension_control_path = '/usr/local/share/postgresql:/home/my_project/share:$system'
    ```

    or, in a Windows environment:

    ```

    extension_control_path = 'C:\tools\postgresql;H:\my_project\share;$system'
    ```

    Note that the specified paths elements are expected to have a
    subdirectory `extension` which will contain the
    `.control` and `.sql` files; the
    `extension` suffix is automatically appended to
    each path element.

    The default value for this parameter is
    `'$system'`. If the value is set to an empty
    string, the default `'$system'` is also assumed.

    If extensions with equal names are present in multiple directories in
    the configured path, only the instance found first in the path will be
    used.

    This parameter can be changed at run time by superusers and users
    with the appropriate `SET` privilege, but a
    setting done that way will only persist until the end of the
    client connection, so this method should be reserved for
    development purposes. The recommended way to set this parameter
    is in the `postgresql.conf` configuration
    file.

    Note that if you set this parameter to be able to load extensions from
    nonstandard locations, you will most likely also need to set [dynamic_library_path](runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH) to a correspondent location, for
    example,

    ```

    extension_control_path = '/usr/local/share/postgresql:$system'
    dynamic_library_path = '/usr/local/lib/postgresql:$libdir'
    ```
<a id="GUC-GIN-FUZZY-SEARCH-LIMIT"></a>

`gin_fuzzy_search_limit` (`integer`) <a id="id-1.6.6.14.5.2.3.1.3"></a> [#](#GUC-GIN-FUZZY-SEARCH-LIMIT)
:   Soft upper limit of the size of the set returned by GIN index scans. For more
    information see [Section 65.4.5](../../internals/indextypes/gin.md#GIN-TIPS).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-client.html)（英文原文，待翻譯）
