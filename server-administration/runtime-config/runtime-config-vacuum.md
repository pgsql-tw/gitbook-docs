## 19.10. Vacuuming [#](#RUNTIME-CONFIG-VACUUM)

[19.10.1. Automatic Vacuuming](runtime-config-vacuum.md#RUNTIME-CONFIG-AUTOVACUUM)

[19.10.2. Cost-based Vacuum Delay](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)

[19.10.3. Default Behavior](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-DEFAULT)

[19.10.4. Freezing](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-FREEZING)

<a id="id-1.6.6.13.2"></a>

These parameters control vacuuming behavior. For more information on the
purpose and responsibilities of vacuum, see [Section 24.1](../maintenance/routine-vacuuming.md).

<a id="RUNTIME-CONFIG-AUTOVACUUM"></a>

### 19.10.1. Automatic Vacuuming [#](#RUNTIME-CONFIG-AUTOVACUUM)

These settings control the behavior of the *autovacuum*
feature. Refer to [Section 24.1.6](../maintenance/routine-vacuuming.md#AUTOVACUUM) for more information.
Note that many of these settings can be overridden on a per-table
basis; see [Storage Parameters](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS).

<a id="GUC-AUTOVACUUM"></a>

`autovacuum` (`boolean`) <a id="id-1.6.6.13.4.3.1.1.3"></a> [#](#GUC-AUTOVACUUM)
:   Controls whether the server should run the
    autovacuum launcher daemon. This is on by default; however,
    [track_counts](runtime-config-statistics.md#GUC-TRACK-COUNTS) must also be enabled for
    autovacuum to work.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line; however, autovacuuming can be
    disabled for individual tables by changing table storage parameters.

    Note that even when this parameter is disabled, the system
    will launch autovacuum processes if necessary to
    prevent transaction ID wraparound. See [Section 24.1.5](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND) for more information.
<a id="GUC-AUTOVACUUM-WORKER-SLOTS"></a>

`autovacuum_worker_slots` (`integer`) <a id="id-1.6.6.13.4.3.2.1.3"></a> [#](#GUC-AUTOVACUUM-WORKER-SLOTS)
:   Specifies the number of backend slots to reserve for autovacuum worker
    processes. The default is typically 16 slots, but might be less if
    your kernel settings will not support it (as determined during initdb).
    This parameter can only be set at server start.

    When changing this value, consider also adjusting
    [autovacuum_max_workers](runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS).
<a id="GUC-AUTOVACUUM-MAX-WORKERS"></a>

`autovacuum_max_workers` (`integer`) <a id="id-1.6.6.13.4.3.3.1.3"></a> [#](#GUC-AUTOVACUUM-MAX-WORKERS)
:   Specifies the maximum number of autovacuum processes (other than the
    autovacuum launcher) that may be running at any one time. The default
    is `3`. This parameter can only be set in the
    `postgresql.conf` file or on the server command line.

    Note that a setting for this value which is higher than
    [autovacuum_worker_slots](runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS) will have no effect,
    since autovacuum workers are taken from the pool of slots established
    by that setting.
<a id="GUC-AUTOVACUUM-NAPTIME"></a>

`autovacuum_naptime` (`integer`) <a id="id-1.6.6.13.4.3.4.1.3"></a> [#](#GUC-AUTOVACUUM-NAPTIME)
:   Specifies the minimum delay between autovacuum runs on any given
    database. In each round the daemon examines the
    database and issues `VACUUM` and `ANALYZE` commands
    as needed for tables in that database.
    If this value is specified without units, it is taken as seconds.
    The default is one minute (`1min`).
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-AUTOVACUUM-VACUUM-THRESHOLD"></a>

`autovacuum_vacuum_threshold` (`integer`) <a id="id-1.6.6.13.4.3.5.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-THRESHOLD)
:   Specifies the minimum number of updated or deleted tuples needed
    to trigger a `VACUUM` in any one table.
    The default is 50 tuples.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line;
    but the setting can be overridden for individual tables by
    changing table storage parameters.
<a id="GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD"></a>

`autovacuum_vacuum_insert_threshold` (`integer`) <a id="id-1.6.6.13.4.3.6.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD)
:   Specifies the number of inserted tuples needed to trigger a
    `VACUUM` in any one table.
    The default is 1000 tuples. If -1 is specified, autovacuum will not
    trigger a `VACUUM` operation on any tables based on
    the number of inserts.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line;
    but the setting can be overridden for individual tables by
    changing table storage parameters.
<a id="GUC-AUTOVACUUM-ANALYZE-THRESHOLD"></a>

`autovacuum_analyze_threshold` (`integer`) <a id="id-1.6.6.13.4.3.7.1.3"></a> [#](#GUC-AUTOVACUUM-ANALYZE-THRESHOLD)
:   Specifies the minimum number of inserted, updated or deleted tuples
    needed to trigger an `ANALYZE` in any one table.
    The default is 50 tuples.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line;
    but the setting can be overridden for individual tables by
    changing table storage parameters.
<a id="GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR"></a>

`autovacuum_vacuum_scale_factor` (`floating point`) <a id="id-1.6.6.13.4.3.8.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR)
:   Specifies a fraction of the table size to add to
    `autovacuum_vacuum_threshold`
    when deciding whether to trigger a `VACUUM`.
    The default is `0.2` (20% of table size).
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line;
    but the setting can be overridden for individual tables by
    changing table storage parameters.
<a id="GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR"></a>

`autovacuum_vacuum_insert_scale_factor` (`floating point`) <a id="id-1.6.6.13.4.3.9.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR)
:   Specifies a fraction of the unfrozen pages in the table to add to
    `autovacuum_vacuum_insert_threshold` when deciding
    whether to trigger a `VACUUM`. The default is
    `0.2` (20% of unfrozen pages in table). This
    parameter can only be set in the `postgresql.conf`
    file or on the server command line; but the setting can be overridden
    for individual tables by changing table storage parameters.
<a id="GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR"></a>

`autovacuum_analyze_scale_factor` (`floating point`) <a id="id-1.6.6.13.4.3.10.1.3"></a> [#](#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR)
:   Specifies a fraction of the table size to add to
    `autovacuum_analyze_threshold`
    when deciding whether to trigger an `ANALYZE`.
    The default is `0.1` (10% of table size).
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line;
    but the setting can be overridden for individual tables by
    changing table storage parameters.
<a id="GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD"></a>

`autovacuum_vacuum_max_threshold` (`integer`) <a id="id-1.6.6.13.4.3.11.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD)
:   Specifies the maximum number of updated or deleted tuples needed to
    trigger a `VACUUM` in any one table, i.e., a limit on
    the value calculated with
    `autovacuum_vacuum_threshold` and
    `autovacuum_vacuum_scale_factor`. The default is
    100,000,000 tuples. If -1 is specified, autovacuum will not enforce a
    maximum number of updated or deleted tuples that will trigger a
    `VACUUM` operation. This parameter can only be set
    in the `postgresql.conf` file or on the server
    command line; but the setting can be overridden for individual tables
    by changing storage parameters.
<a id="GUC-AUTOVACUUM-FREEZE-MAX-AGE"></a>

`autovacuum_freeze_max_age` (`integer`) <a id="id-1.6.6.13.4.3.12.1.3"></a> [#](#GUC-AUTOVACUUM-FREEZE-MAX-AGE)
:   Specifies the maximum age (in transactions) that a table's
    `pg_class`.`relfrozenxid` field can
    attain before a `VACUUM` operation is forced
    to prevent transaction ID wraparound within the table.
    Note that the system will launch autovacuum processes to
    prevent wraparound even when autovacuum is otherwise disabled.

    Vacuum also allows removal of old files from the
    `pg_xact` subdirectory, which is why the default
    is a relatively low 200 million transactions.
    This parameter can only be set at server start, but the setting
    can be reduced for individual tables by
    changing table storage parameters.
    For more information see [Section 24.1.5](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND).
<a id="GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE"></a>

`autovacuum_multixact_freeze_max_age` (`integer`) <a id="id-1.6.6.13.4.3.13.1.3"></a> [#](#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE)
:   Specifies the maximum age (in multixacts) that a table's
    `pg_class`.`relminmxid` field can
    attain before a `VACUUM` operation is forced to
    prevent multixact ID wraparound within the table.
    Note that the system will launch autovacuum processes to
    prevent wraparound even when autovacuum is otherwise disabled.

    Vacuuming multixacts also allows removal of old files from the
    `pg_multixact/members` and `pg_multixact/offsets`
    subdirectories, which is why the default is a relatively low
    400 million multixacts.
    This parameter can only be set at server start, but the setting can
    be reduced for individual tables by changing table storage parameters.
    For more information see [Section 24.1.5.1](../maintenance/routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND).
<a id="GUC-AUTOVACUUM-VACUUM-COST-DELAY"></a>

`autovacuum_vacuum_cost_delay` (`floating point`) <a id="id-1.6.6.13.4.3.14.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-COST-DELAY)
:   Specifies the cost delay value that will be used in automatic
    `VACUUM` operations. If -1 is specified, the regular
    [vacuum_cost_delay](runtime-config-vacuum.md#GUC-VACUUM-COST-DELAY) value will be used.
    If this value is specified without units, it is taken as milliseconds.
    The default value is 2 milliseconds.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line;
    but the setting can be overridden for individual tables by
    changing table storage parameters.
<a id="GUC-AUTOVACUUM-VACUUM-COST-LIMIT"></a>

`autovacuum_vacuum_cost_limit` (`integer`) <a id="id-1.6.6.13.4.3.15.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-COST-LIMIT)
:   Specifies the cost limit value that will be used in automatic
    `VACUUM` operations. If `-1`
    is specified (which is the default), the regular
    [vacuum_cost_limit](runtime-config-vacuum.md#GUC-VACUUM-COST-LIMIT) value will be used. Note that
    the value is distributed proportionally among the running autovacuum
    workers, if there is more than one, so that the sum of the limits for
    each worker does not exceed the value of this variable.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line;
    but the setting can be overridden for individual tables by
    changing table storage parameters.

<a id="RUNTIME-CONFIG-RESOURCE-VACUUM-COST"></a>

### 19.10.2. Cost-based Vacuum Delay [#](#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)

During the execution of [VACUUM](../../reference/sql-commands/sql-vacuum.md)
and [ANALYZE](../../reference/sql-commands/sql-analyze.md)
commands, the system maintains an
internal counter that keeps track of the estimated cost of the
various I/O operations that are performed. When the accumulated
cost reaches a limit (specified by
`vacuum_cost_limit`), the process performing
the operation will sleep for a short period of time, as specified by
`vacuum_cost_delay`. Then it will reset the
counter and continue execution.

The intent of this feature is to allow administrators to reduce
the I/O impact of these commands on concurrent database
activity. There are many situations where it is not
important that maintenance commands like
`VACUUM` and `ANALYZE` finish
quickly; however, it is usually very important that these
commands do not significantly interfere with the ability of the
system to perform other database operations. Cost-based vacuum
delay provides a way for administrators to achieve this.

This feature is disabled by default for manually issued
`VACUUM` commands. To enable it, set the
`vacuum_cost_delay` variable to a nonzero
value.

<a id="GUC-VACUUM-COST-DELAY"></a>

`vacuum_cost_delay` (`floating point`) <a id="id-1.6.6.13.5.5.1.1.3"></a> [#](#GUC-VACUUM-COST-DELAY)
:   The amount of time that the process will sleep when the cost
    limit has been exceeded. If this value is specified without
    units, it is taken as milliseconds. The default value is
    `0`, which disables the cost-based vacuum delay
    feature. Positive values enable cost-based vacuuming.

    When using cost-based vacuuming, appropriate values for
    `vacuum_cost_delay` are usually quite small, perhaps
    less than 1 millisecond. While `vacuum_cost_delay`
    can be set to fractional-millisecond values, such delays may not be
    measured accurately on older platforms. On such platforms,
    increasing `VACUUM`'s throttled resource consumption
    above what you get at 1ms will require changing the other vacuum cost
    parameters. You should, nonetheless,
    keep `vacuum_cost_delay` as small as your platform
    will consistently measure; large delays are not helpful.
<a id="GUC-VACUUM-COST-PAGE-HIT"></a>

`vacuum_cost_page_hit` (`integer`) <a id="id-1.6.6.13.5.5.2.1.3"></a> [#](#GUC-VACUUM-COST-PAGE-HIT)
:   The estimated cost for vacuuming a buffer found in the shared
    buffer cache. It represents the cost to lock the buffer pool,
    lookup the shared hash table and scan the content of the page.
    The default value is `1`.
<a id="GUC-VACUUM-COST-PAGE-MISS"></a>

`vacuum_cost_page_miss` (`integer`) <a id="id-1.6.6.13.5.5.3.1.3"></a> [#](#GUC-VACUUM-COST-PAGE-MISS)
:   The estimated cost for vacuuming a buffer that has to be read from
    disk. This represents the effort to lock the buffer pool,
    lookup the shared hash table, read the desired block in from
    the disk and scan its content. The default value is
    `2`.
<a id="GUC-VACUUM-COST-PAGE-DIRTY"></a>

`vacuum_cost_page_dirty` (`integer`) <a id="id-1.6.6.13.5.5.4.1.3"></a> [#](#GUC-VACUUM-COST-PAGE-DIRTY)
:   The estimated cost charged when vacuum modifies a block that was
    previously clean. It represents the extra I/O required to
    flush the dirty block out to disk again. The default value is
    `20`.
<a id="GUC-VACUUM-COST-LIMIT"></a>

`vacuum_cost_limit` (`integer`) <a id="id-1.6.6.13.5.5.5.1.3"></a> [#](#GUC-VACUUM-COST-LIMIT)
:   This is the accumulated cost that will cause the vacuuming
    process to sleep for `vacuum_cost_delay`. The
    default is `200`.

### Note

There are certain operations that hold critical locks and should
therefore complete as quickly as possible. Cost-based vacuum
delays do not occur during such operations. Therefore it is
possible that the cost accumulates far higher than the specified
limit. To avoid uselessly long delays in such cases, the actual
delay is calculated as `vacuum_cost_delay` \*
`accumulated_balance` /
`vacuum_cost_limit` with a maximum of
`vacuum_cost_delay` \* 4.

<a id="RUNTIME-CONFIG-VACUUM-DEFAULT"></a>

### 19.10.3. Default Behavior [#](#RUNTIME-CONFIG-VACUUM-DEFAULT)

<a id="GUC-VACUUM-TRUNCATE"></a>

`vacuum_truncate` (`boolean`) <a id="id-1.6.6.13.6.2.1.1.3"></a> [#](#GUC-VACUUM-TRUNCATE)
:   Enables or disables vacuum to try to truncate off any empty pages at
    the end of the table. The default value is `true`.
    If `true`, `VACUUM` and autovacuum
    do the truncation and the disk space for the truncated pages is
    returned to the operating system. Note that the truncation requires
    an `ACCESS EXCLUSIVE` lock on the table. The
    `TRUNCATE` parameter of
    [`VACUUM`](../../reference/sql-commands/sql-vacuum.md), if
    specified, overrides the value of this parameter. The setting can
    also be overridden for individual tables by changing table storage
    parameters.

<a id="RUNTIME-CONFIG-VACUUM-FREEZING"></a>

### 19.10.4. Freezing [#](#RUNTIME-CONFIG-VACUUM-FREEZING)

To maintain correctness even after transaction IDs wrap around,
PostgreSQL marks rows that are sufficiently
old as *frozen*. These rows are visible to everyone;
other transactions do not need to examine their inserting XID to
determine visibility. `VACUUM` is responsible for
marking rows as frozen. The following settings control
`VACUUM`'s freezing behavior and should be tuned based
on the XID consumption rate of the system and data access patterns of the
dominant workloads. See [Section 24.1.5](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND) for more
information on transaction ID wraparound and tuning these parameters.

<a id="GUC-VACUUM-FREEZE-TABLE-AGE"></a>

`vacuum_freeze_table_age` (`integer`) <a id="id-1.6.6.13.7.3.1.1.3"></a> [#](#GUC-VACUUM-FREEZE-TABLE-AGE)
:   `VACUUM` performs an aggressive scan if the table's
    `pg_class`.`relfrozenxid` field has reached
    the age specified by this setting. An aggressive scan differs from
    a regular `VACUUM` in that it visits every page that might
    contain unfrozen XIDs or MXIDs, not just those that might contain dead
    tuples. The default is 150 million transactions. Although users can
    set this value anywhere from zero to two billion, `VACUUM`
    will silently limit the effective value to 95% of
    [autovacuum_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE), so that a
    periodic manual `VACUUM` has a chance to run before an
    anti-wraparound autovacuum is launched for the table. For more
    information see
    [Section 24.1.5](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND).
<a id="GUC-VACUUM-FREEZE-MIN-AGE"></a>

`vacuum_freeze_min_age` (`integer`) <a id="id-1.6.6.13.7.3.2.1.3"></a> [#](#GUC-VACUUM-FREEZE-MIN-AGE)
:   Specifies the cutoff age (in transactions) that
    `VACUUM` should use to decide whether to
    trigger freezing of pages that have an older XID.
    The default is 50 million transactions. Although
    users can set this value anywhere from zero to one billion,
    `VACUUM` will silently limit the effective value to half
    the value of [autovacuum_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE), so
    that there is not an unreasonably short time between forced
    autovacuums. For more information see [Section 24.1.5](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND).
<a id="GUC-VACUUM-FAILSAFE-AGE"></a>

`vacuum_failsafe_age` (`integer`) <a id="id-1.6.6.13.7.3.3.1.3"></a> [#](#GUC-VACUUM-FAILSAFE-AGE)
:   Specifies the maximum age (in transactions) that a table's
    `pg_class`.`relfrozenxid`
    field can attain before `VACUUM` takes
    extraordinary measures to avoid system-wide transaction ID
    wraparound failure. This is `VACUUM`'s
    strategy of last resort. The failsafe typically triggers
    when an autovacuum to prevent transaction ID wraparound has
    already been running for some time, though it's possible for
    the failsafe to trigger during any `VACUUM`.

    When the failsafe is triggered, any cost-based delay that is
    in effect will no longer be applied, further non-essential
    maintenance tasks (such as index vacuuming) are bypassed, and any
    [*[Buffer Access Strategy](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)*](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)
    in use will be disabled resulting in `VACUUM` being
    free to make use of all of
    [*[shared buffers](../../appendixes/glossary/README.md#GLOSSARY-SHARED-MEMORY)*](../../appendixes/glossary/README.md#GLOSSARY-SHARED-MEMORY).

    The default is 1.6 billion transactions. Although users can
    set this value anywhere from zero to 2.1 billion,
    `VACUUM` will silently adjust the effective
    value to no less than 105% of [autovacuum_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE).
<a id="GUC-VACUUM-MULTIXACT-FREEZE-TABLE-AGE"></a>

`vacuum_multixact_freeze_table_age` (`integer`) <a id="id-1.6.6.13.7.3.4.1.3"></a> [#](#GUC-VACUUM-MULTIXACT-FREEZE-TABLE-AGE)
:   `VACUUM` performs an aggressive scan if the table's
    `pg_class`.`relminmxid` field has reached
    the age specified by this setting. An aggressive scan differs from
    a regular `VACUUM` in that it visits every page that might
    contain unfrozen XIDs or MXIDs, not just those that might contain dead
    tuples. The default is 150 million multixacts.
    Although users can set this value anywhere from zero to two billion,
    `VACUUM` will silently limit the effective value to 95% of
    [autovacuum_multixact_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE), so that a
    periodic manual `VACUUM` has a chance to run before an
    anti-wraparound is launched for the table.
    For more information see [Section 24.1.5.1](../maintenance/routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND).
<a id="GUC-VACUUM-MULTIXACT-FREEZE-MIN-AGE"></a>

`vacuum_multixact_freeze_min_age` (`integer`) <a id="id-1.6.6.13.7.3.5.1.3"></a> [#](#GUC-VACUUM-MULTIXACT-FREEZE-MIN-AGE)
:   Specifies the cutoff age (in multixacts) that `VACUUM`
    should use to decide whether to trigger freezing of pages with
    an older multixact ID. The default is 5 million multixacts.
    Although users can set this value anywhere from zero to one billion,
    `VACUUM` will silently limit the effective value to half
    the value of [autovacuum_multixact_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE),
    so that there is not an unreasonably short time between forced
    autovacuums.
    For more information see [Section 24.1.5.1](../maintenance/routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND).
<a id="GUC-VACUUM-MULTIXACT-FAILSAFE-AGE"></a>

`vacuum_multixact_failsafe_age` (`integer`) <a id="id-1.6.6.13.7.3.6.1.3"></a> [#](#GUC-VACUUM-MULTIXACT-FAILSAFE-AGE)
:   Specifies the maximum age (in multixacts) that a table's
    `pg_class`.`relminmxid`
    field can attain before `VACUUM` takes
    extraordinary measures to avoid system-wide multixact ID
    wraparound failure. This is `VACUUM`'s
    strategy of last resort. The failsafe typically triggers when
    an autovacuum to prevent transaction ID wraparound has already
    been running for some time, though it's possible for the
    failsafe to trigger during any `VACUUM`.

    When the failsafe is triggered, any cost-based delay that is
    in effect will no longer be applied, and further non-essential
    maintenance tasks (such as index vacuuming) are bypassed.

    The default is 1.6 billion multixacts. Although users can set
    this value anywhere from zero to 2.1 billion,
    `VACUUM` will silently adjust the effective
    value to no less than 105% of [autovacuum_multixact_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE).
<a id="GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE"></a>

`vacuum_max_eager_freeze_failure_rate` (`floating point`) <a id="id-1.6.6.13.7.3.7.1.3"></a> [#](#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE)
:   Specifies the maximum number of pages (as a fraction of total pages in
    the relation) that `VACUUM` may scan and
    *fail* to set all-frozen in the visibility map
    before disabling eager scanning. A value of `0`
    disables eager scanning altogether. The default is
    `0.03` (3%).

    Note that when eager scanning is enabled, only freeze failures
    count against the cap, not successful freezing. Successful page
    freezes are capped internally at 20% of the all-visible but not
    all-frozen pages in the relation. Capping successful page freezes helps
    amortize the overhead across multiple normal vacuums and limits the
    potential downside of wasted eager freezes of pages that are modified
    again before the next aggressive vacuum.

    This parameter can only be set in the
    `postgresql.conf` file or on the server command
    line; but the setting can be overridden for individual tables by
    changing the
    [corresponding table storage parameter](../../reference/sql-commands/sql-createtable.md#RELOPTION-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE).
    For more information on tuning vacuum's freezing behavior,
    see [Section 24.1.5](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-vacuum.html)（英文原文，待翻譯）
