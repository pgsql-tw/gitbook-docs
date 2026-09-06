## 19.9. Run-time Statistics [#](#RUNTIME-CONFIG-STATISTICS)

[19.9.1. Cumulative Query and Index Statistics](runtime-config-statistics.md#RUNTIME-CONFIG-CUMULATIVE-STATISTICS)

[19.9.2. Statistics Monitoring](runtime-config-statistics.md#RUNTIME-CONFIG-STATISTICS-MONITOR)

<a id="RUNTIME-CONFIG-CUMULATIVE-STATISTICS"></a>

### 19.9.1. Cumulative Query and Index Statistics [#](#RUNTIME-CONFIG-CUMULATIVE-STATISTICS)

These parameters control the server-wide cumulative statistics system.
When enabled, the data that is collected can be accessed via the
`pg_stat` and `pg_statio`
family of system views. Refer to [Chapter 27](../monitoring/README.md) for more
information.

<a id="GUC-TRACK-ACTIVITIES"></a>

`track_activities` (`boolean`) <a id="id-1.6.6.12.2.3.1.1.3"></a> [#](#GUC-TRACK-ACTIVITIES)
:   Enables the collection of information on the currently
    executing command of each session, along with its identifier and the
    time when that command began execution. This parameter is on by
    default. Note that even when enabled, this information is only
    visible to superusers, roles with privileges of the
    `pg_read_all_stats` role and the user owning the
    sessions being reported on (including sessions belonging to a role they
    have the privileges of), so it should not represent a security risk.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.
<a id="GUC-TRACK-ACTIVITY-QUERY-SIZE"></a>

`track_activity_query_size` (`integer`) <a id="id-1.6.6.12.2.3.2.1.3"></a> [#](#GUC-TRACK-ACTIVITY-QUERY-SIZE)
:   Specifies the amount of memory reserved to store the text of the
    currently executing command for each active session, for the
    `pg_stat_activity`.`query` field.
    If this value is specified without units, it is taken as bytes.
    The default value is 1024 bytes.
    This parameter can only be set at server start.
<a id="GUC-TRACK-COUNTS"></a>

`track_counts` (`boolean`) <a id="id-1.6.6.12.2.3.3.1.3"></a> [#](#GUC-TRACK-COUNTS)
:   Enables collection of statistics on database activity.
    This parameter is on by default, because the autovacuum
    daemon needs the collected information.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.
<a id="GUC-TRACK-COST-DELAY-TIMING"></a>

`track_cost_delay_timing` (`boolean`) <a id="id-1.6.6.12.2.3.4.1.3"></a> [#](#GUC-TRACK-COST-DELAY-TIMING)
:   Enables timing of cost-based vacuum delay (see
    [Section 19.10.2](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)). This parameter
    is off by default, as it will repeatedly query the operating system for
    the current time, which may cause significant overhead on some
    platforms. You can use the [pg_test_timing](../../reference/reference-server/pgtesttiming.md) tool to
    measure the overhead of timing on your system. Cost-based vacuum delay
    timing information is displayed in
    [`pg_stat_progress_vacuum`](../monitoring/progress-reporting.md#VACUUM-PROGRESS-REPORTING),
    [`pg_stat_progress_analyze`](../monitoring/progress-reporting.md#ANALYZE-PROGRESS-REPORTING),
    in the output of [VACUUM](../../reference/sql-commands/sql-vacuum.md) and
    [ANALYZE](../../reference/sql-commands/sql-analyze.md) when the
    `VERBOSE` option is used, and by autovacuum for
    auto-vacuums and auto-analyzes when
    [log_autovacuum_min_duration](runtime-config-logging.md#GUC-LOG-AUTOVACUUM-MIN-DURATION) is set.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.
<a id="GUC-TRACK-IO-TIMING"></a>

`track_io_timing` (`boolean`) <a id="id-1.6.6.12.2.3.5.1.3"></a> [#](#GUC-TRACK-IO-TIMING)
:   Enables timing of database I/O waits. This parameter is off by
    default, as it will repeatedly query the operating system for
    the current time, which may cause significant overhead on some
    platforms. You can use the [pg_test_timing](../../reference/reference-server/pgtesttiming.md) tool to
    measure the overhead of timing on your system.
    I/O timing information is
    displayed in [`pg_stat_database`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW),
    [`pg_stat_io`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW) (if `object`
    is not `wal`), in the output of the
    [`pg_stat_get_backend_io()`](../monitoring/monitoring-stats.md#PG-STAT-GET-BACKEND-IO) function (if
    `object` is not `wal`), in the
    output of [EXPLAIN](../../reference/sql-commands/sql-explain.md) when the `BUFFERS`
    option is used, in the output of [VACUUM](../../reference/sql-commands/sql-vacuum.md) when
    the `VERBOSE` option is used, by autovacuum
    for auto-vacuums and auto-analyzes, when [log_autovacuum_min_duration](runtime-config-logging.md#GUC-LOG-AUTOVACUUM-MIN-DURATION) is set and by
    [pg_stat_statements](../../appendixes/contrib/pgstatstatements.md).
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.
<a id="GUC-TRACK-WAL-IO-TIMING"></a>

`track_wal_io_timing` (`boolean`) <a id="id-1.6.6.12.2.3.6.1.3"></a> [#](#GUC-TRACK-WAL-IO-TIMING)
:   Enables timing of WAL I/O waits. This parameter is off by default,
    as it will repeatedly query the operating system for the current time,
    which may cause significant overhead on some platforms.
    You can use the pg_test_timing tool to
    measure the overhead of timing on your system.
    I/O timing information is displayed in
    [`pg_stat_io`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW) for the
    `object` `wal` and in the output of
    the [`pg_stat_get_backend_io()`](../monitoring/monitoring-stats.md#PG-STAT-GET-BACKEND-IO) function for the
    `object` `wal`.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.
<a id="GUC-TRACK-FUNCTIONS"></a>

`track_functions` (`enum`) <a id="id-1.6.6.12.2.3.7.1.3"></a> [#](#GUC-TRACK-FUNCTIONS)
:   Enables tracking of function call counts and time used. Specify
    `pl` to track only procedural-language functions,
    `all` to also track SQL and C language functions.
    The default is `none`, which disables function
    statistics tracking.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.

    ### Note

    SQL-language functions that are simple enough to be “inlined”
    into the calling query will not be tracked, regardless of this
    setting.
<a id="GUC-STATS-FETCH-CONSISTENCY"></a>

`stats_fetch_consistency` (`enum`) <a id="id-1.6.6.12.2.3.8.1.3"></a> [#](#GUC-STATS-FETCH-CONSISTENCY)
:   Determines the behavior when cumulative statistics are accessed
    multiple times within a transaction. When set to
    `none`, each access re-fetches counters from shared
    memory. When set to `cache`, the first access to
    statistics for an object caches those statistics until the end of the
    transaction unless `pg_stat_clear_snapshot()` is
    called. When set to `snapshot`, the first statistics
    access caches all statistics accessible in the current database, until
    the end of the transaction unless
    `pg_stat_clear_snapshot()` is called. Changing this
    parameter in a transaction discards the statistics snapshot.
    The default is `cache`.

    ### Note

    `none` is most suitable for monitoring systems. If
    values are only accessed once, it is the most
    efficient. `cache` ensures repeat accesses yield the
    same values, which is important for queries involving
    e.g. self-joins. `snapshot` can be useful when
    interactively inspecting statistics, but has higher overhead,
    particularly if many database objects exist.

<a id="RUNTIME-CONFIG-STATISTICS-MONITOR"></a>

### 19.9.2. Statistics Monitoring [#](#RUNTIME-CONFIG-STATISTICS-MONITOR)

<a id="GUC-COMPUTE-QUERY-ID"></a>

`compute_query_id` (`enum`) <a id="id-1.6.6.12.3.2.1.1.3"></a> [#](#GUC-COMPUTE-QUERY-ID)
:   Enables in-core computation of a query identifier.
    Query identifiers can be displayed in the [`pg_stat_activity`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW)
    view, using `EXPLAIN`, or emitted in the log if
    configured via the [log_line_prefix](runtime-config-logging.md#GUC-LOG-LINE-PREFIX) parameter.
    The [pg_stat_statements](../../appendixes/contrib/pgstatstatements.md) extension also requires a query
    identifier to be computed. Note that an external module can
    alternatively be used if the in-core query identifier computation
    method is not acceptable. In this case, in-core computation
    must be always disabled.
    Valid values are `off` (always disabled),
    `on` (always enabled), `auto`,
    which lets modules such as [pg_stat_statements](../../appendixes/contrib/pgstatstatements.md)
    automatically enable it, and `regress` which
    has the same effect as `auto`, except that the
    query identifier is not shown in the `EXPLAIN` output
    in order to facilitate automated regression testing.
    The default is `auto`.

    ### Note

    To ensure that only one query identifier is calculated and
    displayed, extensions that calculate query identifiers should
    throw an error if a query identifier has already been computed.
<a id="GUC-LOG-STATEMENT-STATS"></a>

`log_statement_stats` (`boolean`) <a id="id-1.6.6.12.3.2.2.1.3"></a> <br>`log_parser_stats` (`boolean`) <a id="id-1.6.6.12.3.2.2.2.3"></a> <br>`log_planner_stats` (`boolean`) <a id="id-1.6.6.12.3.2.2.3.3"></a> <br>`log_executor_stats` (`boolean`) <a id="id-1.6.6.12.3.2.2.4.3"></a> [#](#GUC-LOG-STATEMENT-STATS)
:   For each query, output performance statistics of the respective
    module to the server log. This is a crude profiling
    instrument, similar to the Unix `getrusage()` operating
    system facility. `log_statement_stats` reports total
    statement statistics, while the others report per-module statistics.
    `log_statement_stats` cannot be enabled together with
    any of the per-module options. All of these options are disabled by
    default.
    Only superusers and users with the appropriate `SET`
    privilege can change these settings.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-statistics.html)（英文原文，待翻譯）
