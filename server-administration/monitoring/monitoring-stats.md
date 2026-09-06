## 27.2. The Cumulative Statistics System [#](#MONITORING-STATS)

[27.2.1. Statistics Collection Configuration](monitoring-stats.md#MONITORING-STATS-SETUP)

[27.2.2. Viewing Statistics](monitoring-stats.md#MONITORING-STATS-VIEWS)

[27.2.3. `pg_stat_activity`](monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW)

[27.2.4. `pg_stat_replication`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW)

[27.2.5. `pg_stat_replication_slots`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW)

[27.2.6. `pg_stat_wal_receiver`](monitoring-stats.md#MONITORING-PG-STAT-WAL-RECEIVER-VIEW)

[27.2.7. `pg_stat_recovery_prefetch`](monitoring-stats.md#MONITORING-PG-STAT-RECOVERY-PREFETCH)

[27.2.8. `pg_stat_subscription`](monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION)

[27.2.9. `pg_stat_subscription_stats`](monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS)

[27.2.10. `pg_stat_ssl`](monitoring-stats.md#MONITORING-PG-STAT-SSL-VIEW)

[27.2.11. `pg_stat_gssapi`](monitoring-stats.md#MONITORING-PG-STAT-GSSAPI-VIEW)

[27.2.12. `pg_stat_archiver`](monitoring-stats.md#MONITORING-PG-STAT-ARCHIVER-VIEW)

[27.2.13. `pg_stat_io`](monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW)

[27.2.14. `pg_stat_bgwriter`](monitoring-stats.md#MONITORING-PG-STAT-BGWRITER-VIEW)

[27.2.15. `pg_stat_checkpointer`](monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW)

[27.2.16. `pg_stat_wal`](monitoring-stats.md#MONITORING-PG-STAT-WAL-VIEW)

[27.2.17. `pg_stat_database`](monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW)

[27.2.18. `pg_stat_database_conflicts`](monitoring-stats.md#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW)

[27.2.19. `pg_stat_all_tables`](monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW)

[27.2.20. `pg_stat_all_indexes`](monitoring-stats.md#MONITORING-PG-STAT-ALL-INDEXES-VIEW)

[27.2.21. `pg_statio_all_tables`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-TABLES-VIEW)

[27.2.22. `pg_statio_all_indexes`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-INDEXES-VIEW)

[27.2.23. `pg_statio_all_sequences`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW)

[27.2.24. `pg_stat_user_functions`](monitoring-stats.md#MONITORING-PG-STAT-USER-FUNCTIONS-VIEW)

[27.2.25. `pg_stat_slru`](monitoring-stats.md#MONITORING-PG-STAT-SLRU-VIEW)

[27.2.26. Statistics Functions](monitoring-stats.md#MONITORING-STATS-FUNCTIONS)

<a id="id-1.6.14.7.2"></a>

PostgreSQL's *cumulative statistics
system* supports collection and reporting of information about
server activity. Presently, accesses to tables and indexes in both
disk-block and individual-row terms are counted. The total number of rows
in each table, and information about vacuum and analyze actions for each
table are also counted. If enabled, calls to user-defined functions and
the total time spent in each one are counted as well.

PostgreSQL also supports reporting dynamic
information about exactly what is going on in the system right now, such as
the exact command currently being executed by other server processes, and
which other connections exist in the system. This facility is independent
of the cumulative statistics system.

<a id="MONITORING-STATS-SETUP"></a>

### 27.2.1. Statistics Collection Configuration [#](#MONITORING-STATS-SETUP)

Since collection of statistics adds some overhead to query execution,
the system can be configured to collect or not collect information.
This is controlled by configuration parameters that are normally set in
`postgresql.conf`. (See [Chapter 19](../runtime-config/README.md) for
details about setting configuration parameters.)

The parameter [track_activities](../runtime-config/runtime-config-statistics.md#GUC-TRACK-ACTIVITIES) enables monitoring
of the current command being executed by any server process.

The parameter [track_cost_delay_timing](../runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING) enables
monitoring of cost-based vacuum delay.

The parameter [track_counts](../runtime-config/runtime-config-statistics.md#GUC-TRACK-COUNTS) controls whether
cumulative statistics are collected about table and index accesses.

The parameter [track_functions](../runtime-config/runtime-config-statistics.md#GUC-TRACK-FUNCTIONS) enables tracking of
usage of user-defined functions.

The parameter [track_io_timing](../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING) enables monitoring
of block read, write, extend, and fsync times.

The parameter [track_wal_io_timing](../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING) enables monitoring
of WAL read, write and fsync times.

Normally these parameters are set in `postgresql.conf` so
that they apply to all server processes, but it is possible to turn
them on or off in individual sessions using the [SET](../../reference/sql-commands/sql-set.md) command. (To prevent
ordinary users from hiding their activity from the administrator,
only superusers are allowed to change these parameters with
`SET`.)

Cumulative statistics are collected in shared memory. Every
PostgreSQL process collects statistics locally,
then updates the shared data at appropriate intervals. When a server,
including a physical replica, shuts down cleanly, a permanent copy of the
statistics data is stored in the `pg_stat` subdirectory,
so that statistics can be retained across server restarts. In contrast,
when starting from an unclean shutdown (e.g., after an immediate shutdown,
a server crash, starting from a base backup, and point-in-time recovery),
all statistics counters are reset.

<a id="MONITORING-STATS-VIEWS"></a>

### 27.2.2. Viewing Statistics [#](#MONITORING-STATS-VIEWS)

Several predefined views, listed in [Table 27.1](monitoring-stats.md#MONITORING-STATS-DYNAMIC-VIEWS-TABLE), are available to show
the current state of the system. There are also several other
views, listed in [Table 27.2](monitoring-stats.md#MONITORING-STATS-VIEWS-TABLE), available to show the accumulated
statistics. Alternatively, one can
build custom views using the underlying cumulative statistics functions, as
discussed in [Section 27.2.26](monitoring-stats.md#MONITORING-STATS-FUNCTIONS).

When using the cumulative statistics views and functions to monitor
collected data, it is important to realize that the information does not
update instantaneously. Each individual server process flushes out
accumulated statistics to shared memory just before going idle, but not
more frequently than once per `PGSTAT_MIN_INTERVAL`
milliseconds (1 second unless altered while building the server); so a
query or transaction still in progress does not affect the displayed totals
and the displayed information lags behind actual activity. However,
current-query information collected by `track_activities`
is always up-to-date.

Another important point is that when a server process is asked to display
any of the accumulated statistics, accessed values are cached until the end
of its current transaction in the default configuration. So the statistics
will show static information as long as you continue the current
transaction. Similarly, information about the current queries of all
sessions is collected when any such information is first requested within a
transaction, and the same information will be displayed throughout the
transaction. This is a feature, not a bug, because it allows you to perform
several queries on the statistics and correlate the results without
worrying that the numbers are changing underneath you.
When analyzing statistics interactively, or with expensive queries, the
time delta between accesses to individual statistics can lead to
significant skew in the cached statistics. To minimize skew,
`stats_fetch_consistency` can be set to
`snapshot`, at the price of increased memory usage for
caching not-needed statistics data. Conversely, if it's known that
statistics are only accessed once, caching accessed statistics is
unnecessary and can be avoided by setting
`stats_fetch_consistency` to `none`.
You can invoke `pg_stat_clear_snapshot()` to discard the
current transaction's statistics snapshot or cached values (if any). The
next use of statistical information will (when in snapshot mode) cause a
new snapshot to be built or (when in cache mode) accessed statistics to be
cached.

A transaction can also see its own statistics (not yet flushed out to the
shared memory statistics) in the views
`pg_stat_xact_all_tables`,
`pg_stat_xact_sys_tables`,
`pg_stat_xact_user_tables`, and
`pg_stat_xact_user_functions`. These numbers do not act as
stated above; instead they update continuously throughout the transaction.

Some of the information in the dynamic statistics views shown in [Table 27.1](monitoring-stats.md#MONITORING-STATS-DYNAMIC-VIEWS-TABLE) is security restricted.
Ordinary users can only see all the information about their own sessions
(sessions belonging to a role that they are a member of). In rows about
other sessions, many columns will be null. Note, however, that the
existence of a session and its general properties such as its sessions user
and database are visible to all users. Superusers and roles with privileges of
built-in role [`pg_read_all_stats`](../user-manag/predefined-roles.md#PREDEFINED-ROLE-PG-MONITOR)
can see all the information about all sessions.

<a id="MONITORING-STATS-DYNAMIC-VIEWS-TABLE"></a>

**Table 27.1. Dynamic Statistics Views**

<table border="1" class="table" summary="Dynamic Statistics Views"><colgroup><col/><col/></colgroup><thead><tr><th>View Name</th><th>Description</th></tr></thead><tbody><tr><td>
<code class="structname">pg_stat_activity</code>
<a class="indexterm" id="id-1.6.14.7.6.7.2.2.1.1.2"></a>
</td><td>
       One row per server process, showing information related to
       the current activity of that process, such as state and current query.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW">
<code class="structname">pg_stat_activity</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_replication</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.2.1.2"></a></td><td>One row per WAL sender process, showing statistics about
       replication to that sender's connected standby server.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW">
<code class="structname">pg_stat_replication</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_wal_receiver</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.3.1.2"></a></td><td>Only one row, showing statistics about the WAL receiver from
       that receiver's connected server.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-WAL-RECEIVER-VIEW">
<code class="structname">pg_stat_wal_receiver</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_recovery_prefetch</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.4.1.2"></a></td><td>Only one row, showing statistics about blocks prefetched during recovery.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-RECOVERY-PREFETCH">
<code class="structname">pg_stat_recovery_prefetch</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_subscription</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.5.1.2"></a></td><td>At least one row per subscription, showing information about
       the subscription workers.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION">
<code class="structname">pg_stat_subscription</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_ssl</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.6.1.2"></a></td><td>One row per connection (regular and replication), showing information about
       SSL used on this connection.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-SSL-VIEW">
<code class="structname">pg_stat_ssl</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_gssapi</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.7.1.2"></a></td><td>One row per connection (regular and replication), showing information about
       GSSAPI authentication and encryption used on this connection.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-GSSAPI-VIEW">
<code class="structname">pg_stat_gssapi</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_progress_analyze</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.8.1.2"></a></td><td>One row for each backend (including autovacuum worker processes) running
       <code class="command">ANALYZE</code>, showing current progress.
       See <a class="xref" href="progress-reporting.md#ANALYZE-PROGRESS-REPORTING">Section 27.4.1</a>.
      </td></tr><tr><td><code class="structname">pg_stat_progress_create_index</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.9.1.2"></a></td><td>One row for each backend running <code class="command">CREATE INDEX</code> or <code class="command">REINDEX</code>, showing
      current progress.
      See <a class="xref" href="progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING">Section 27.4.4</a>.
     </td></tr><tr><td><code class="structname">pg_stat_progress_vacuum</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.10.1.2"></a></td><td>One row for each backend (including autovacuum worker processes) running
       <code class="command">VACUUM</code>, showing current progress.
       See <a class="xref" href="progress-reporting.md#VACUUM-PROGRESS-REPORTING">Section 27.4.5</a>.
      </td></tr><tr><td><code class="structname">pg_stat_progress_cluster</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.11.1.2"></a></td><td>One row for each backend running
       <code class="command">CLUSTER</code> or <code class="command">VACUUM FULL</code>, showing current progress.
       See <a class="xref" href="progress-reporting.md#CLUSTER-PROGRESS-REPORTING">Section 27.4.2</a>.
      </td></tr><tr><td><code class="structname">pg_stat_progress_basebackup</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.12.1.2"></a></td><td>One row for each WAL sender process streaming a base backup,
       showing current progress.
       See <a class="xref" href="progress-reporting.md#BASEBACKUP-PROGRESS-REPORTING">Section 27.4.6</a>.
      </td></tr><tr><td><code class="structname">pg_stat_progress_copy</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.13.1.2"></a></td><td>One row for each backend running <code class="command">COPY</code>, showing current progress.
       See <a class="xref" href="progress-reporting.md#COPY-PROGRESS-REPORTING">Section 27.4.3</a>.
      </td></tr></tbody></table>

<br><a id="MONITORING-STATS-VIEWS-TABLE"></a>

**Table 27.2. Collected Statistics Views**

<table border="1" class="table" summary="Collected Statistics Views"><colgroup><col/><col/></colgroup><thead><tr><th>View Name</th><th>Description</th></tr></thead><tbody><tr><td><code class="structname">pg_stat_archiver</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.1.1.2"></a></td><td>One row only, showing statistics about the
       WAL archiver process's activity. See
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ARCHIVER-VIEW">
<code class="structname">pg_stat_archiver</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_bgwriter</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.2.1.2"></a></td><td>One row only, showing statistics about the
       background writer process's activity. See
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-BGWRITER-VIEW">
<code class="structname">pg_stat_bgwriter</code></a> for details.
     </td></tr><tr><td><code class="structname">pg_stat_checkpointer</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.3.1.2"></a></td><td>One row only, showing statistics about the
       checkpointer process's activity. See
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW">
<code class="structname">pg_stat_checkpointer</code></a> for details.
     </td></tr><tr><td><code class="structname">pg_stat_database</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.4.1.2"></a></td><td>One row per database, showing database-wide statistics. See
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW">
<code class="structname">pg_stat_database</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_database_conflicts</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.5.1.2"></a></td><td>
       One row per database, showing database-wide statistics about
       query cancels due to conflict with recovery on standby servers.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW">
<code class="structname">pg_stat_database_conflicts</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_io</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.6.1.2"></a></td><td>
       One row for each combination of backend type, context, and target object
       containing cluster-wide I/O statistics.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW">
<code class="structname">pg_stat_io</code></a> for details.
     </td></tr><tr><td><code class="structname">pg_stat_replication_slots</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.7.1.2"></a></td><td>One row per replication slot, showing statistics about the
       replication slot's usage. See
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW">
<code class="structname">pg_stat_replication_slots</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_slru</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.8.1.2"></a></td><td>One row per SLRU, showing statistics of operations. See
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-SLRU-VIEW">
<code class="structname">pg_stat_slru</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_subscription_stats</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.9.1.2"></a></td><td>One row per subscription, showing statistics about errors and conflicts.
      See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS">
<code class="structname">pg_stat_subscription_stats</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_wal</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.10.1.2"></a></td><td>One row only, showing statistics about WAL activity. See
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-WAL-VIEW">
<code class="structname">pg_stat_wal</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_all_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.11.1.2"></a></td><td>
       One row for each table in the current database, showing statistics
       about accesses to that specific table.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW">
<code class="structname">pg_stat_all_tables</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_sys_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.12.1.2"></a></td><td>Same as <code class="structname">pg_stat_all_tables</code>, except that only
      system tables are shown.</td></tr><tr><td><code class="structname">pg_stat_user_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.13.1.2"></a></td><td>Same as <code class="structname">pg_stat_all_tables</code>, except that only user
      tables are shown.</td></tr><tr><td><code class="structname">pg_stat_xact_all_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.14.1.2"></a></td><td>Similar to <code class="structname">pg_stat_all_tables</code>, but counts actions
      taken so far within the current transaction (which are <span class="emphasis"><em>not</em></span>
      yet included in <code class="structname">pg_stat_all_tables</code> and related views).
      The columns for numbers of live and dead rows and vacuum and
      analyze actions are not present in this view.</td></tr><tr><td><code class="structname">pg_stat_xact_sys_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.15.1.2"></a></td><td>Same as <code class="structname">pg_stat_xact_all_tables</code>, except that only
      system tables are shown.</td></tr><tr><td><code class="structname">pg_stat_xact_user_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.16.1.2"></a></td><td>Same as <code class="structname">pg_stat_xact_all_tables</code>, except that only
      user tables are shown.</td></tr><tr><td><code class="structname">pg_stat_all_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.17.1.2"></a></td><td>
       One row for each index in the current database, showing statistics
       about accesses to that specific index.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ALL-INDEXES-VIEW">
<code class="structname">pg_stat_all_indexes</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_sys_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.18.1.2"></a></td><td>Same as <code class="structname">pg_stat_all_indexes</code>, except that only
      indexes on system tables are shown.</td></tr><tr><td><code class="structname">pg_stat_user_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.19.1.2"></a></td><td>Same as <code class="structname">pg_stat_all_indexes</code>, except that only
      indexes on user tables are shown.</td></tr><tr><td><code class="structname">pg_stat_user_functions</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.20.1.2"></a></td><td>
       One row for each tracked function, showing statistics
       about executions of that function. See
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-USER-FUNCTIONS-VIEW">
<code class="structname">pg_stat_user_functions</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_stat_xact_user_functions</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.21.1.2"></a></td><td>Similar to <code class="structname">pg_stat_user_functions</code>, but counts only
      calls during the current transaction (which are <span class="emphasis"><em>not</em></span>
      yet included in <code class="structname">pg_stat_user_functions</code>).</td></tr><tr><td><code class="structname">pg_statio_all_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.22.1.2"></a></td><td>
       One row for each table in the current database, showing statistics
       about I/O on that specific table.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STATIO-ALL-TABLES-VIEW">
<code class="structname">pg_statio_all_tables</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_statio_sys_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.23.1.2"></a></td><td>Same as <code class="structname">pg_statio_all_tables</code>, except that only
      system tables are shown.</td></tr><tr><td><code class="structname">pg_statio_user_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.24.1.2"></a></td><td>Same as <code class="structname">pg_statio_all_tables</code>, except that only
      user tables are shown.</td></tr><tr><td><code class="structname">pg_statio_all_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.25.1.2"></a></td><td>
       One row for each index in the current database,
       showing statistics about I/O on that specific index.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STATIO-ALL-INDEXES-VIEW">
<code class="structname">pg_statio_all_indexes</code></a> for details.
      </td></tr><tr><td><code class="structname">pg_statio_sys_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.26.1.2"></a></td><td>Same as <code class="structname">pg_statio_all_indexes</code>, except that only
      indexes on system tables are shown.</td></tr><tr><td><code class="structname">pg_statio_user_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.27.1.2"></a></td><td>Same as <code class="structname">pg_statio_all_indexes</code>, except that only
      indexes on user tables are shown.</td></tr><tr><td><code class="structname">pg_statio_all_sequences</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.28.1.2"></a></td><td>
       One row for each sequence in the current database,
       showing statistics about I/O on that specific sequence.
       See <a class="link" href="monitoring-stats.md#MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW">
<code class="structname">pg_statio_all_sequences</code></a> for details.
     </td></tr><tr><td><code class="structname">pg_statio_sys_sequences</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.29.1.2"></a></td><td>Same as <code class="structname">pg_statio_all_sequences</code>, except that only
      system sequences are shown.  (Presently, no system sequences are defined,
      so this view is always empty.)</td></tr><tr><td><code class="structname">pg_statio_user_sequences</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.30.1.2"></a></td><td>Same as <code class="structname">pg_statio_all_sequences</code>, except that only
      user sequences are shown.</td></tr></tbody></table>

<br>

The per-index statistics are particularly useful to determine which
indexes are being used and how effective they are.

The `pg_stat_io` and
`pg_statio_` set of views are useful for determining
the effectiveness of the buffer cache. They can be used to calculate a cache
hit ratio. Note that while PostgreSQL's I/O
statistics capture most instances in which the kernel was invoked in order
to perform I/O, they do not differentiate between data which had to be
fetched from disk and that which already resided in the kernel page cache.
Users are advised to use the PostgreSQL
statistics views in combination with operating system utilities for a more
complete picture of their database's I/O performance.

<a id="MONITORING-PG-STAT-ACTIVITY-VIEW"></a>

### 27.2.3. `pg_stat_activity` [#](#MONITORING-PG-STAT-ACTIVITY-VIEW)

<a id="id-1.6.14.7.7.2"></a>

The `pg_stat_activity` view will have one row
per server process, showing information related to
the current activity of that process.

<a id="PG-STAT-ACTIVITY-VIEW"></a>

**Table 27.3. `pg_stat_activity` View**

<table border="1" class="table" summary="pg_stat_activity View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       OID of the database this backend is connected to
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       Name of the database this backend is connected to
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of this backend
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">leader_pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of the parallel group leader if this process is a parallel
       query worker, or process ID of the leader apply worker if this process
       is a parallel apply worker.  <code class="literal">NULL</code> indicates that this
       process is a parallel group leader or leader apply worker, or does not
       participate in any parallel operation.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesysid</code> <code class="type">oid</code>
</p>
<p>
       OID of the user logged into this backend
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usename</code> <code class="type">name</code>
</p>
<p>
       Name of the user logged into this backend
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">application_name</code> <code class="type">text</code>
</p>
<p>
       Name of the application that is connected
       to this backend
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_addr</code> <code class="type">inet</code>
</p>
<p>
       IP address of the client connected to this backend.
       If this field is null, it indicates either that the client is
       connected via a Unix socket on the server machine or that this is an
       internal process such as autovacuum.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_hostname</code> <code class="type">text</code>
</p>
<p>
       Host name of the connected client, as reported by a
       reverse DNS lookup of <code class="structfield">client_addr</code>. This field will
       only be non-null for IP connections, and only when <a class="xref" href="../runtime-config/runtime-config-logging.md#GUC-LOG-HOSTNAME">log_hostname</a> is enabled.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_port</code> <code class="type">integer</code>
</p>
<p>
       TCP port number that the client is using for communication
       with this backend, or <code class="literal">-1</code> if a Unix socket is used.
       If this field is null, it indicates that this is an internal server process.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_start</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time when this process was started.  For client backends,
       this is the time the client connected to the server.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">xact_start</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time when this process' current transaction was started, or null
       if no transaction is active. If the current
       query is the first of its transaction, this column is equal to the
       <code class="structfield">query_start</code> column.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">query_start</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time when the currently active query was started, or if
       <code class="structfield">state</code> is not <code class="literal">active</code>, when the last query
       was started
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">state_change</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time when the <code class="structfield">state</code> was last changed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wait_event_type</code> <code class="type">text</code>
</p>
<p>
       The type of event for which the backend is waiting, if any;
       otherwise NULL.  See <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TABLE">Table 27.4</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wait_event</code> <code class="type">text</code>
</p>
<p>
       Wait event name if backend is currently waiting, otherwise NULL.
       See <a class="xref" href="monitoring-stats.md#WAIT-EVENT-ACTIVITY-TABLE">Table 27.5</a> through
       <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TIMEOUT-TABLE">Table 27.13</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">state</code> <code class="type">text</code>
</p>
<p>
       Current overall state of this backend.
       Possible values are:
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">starting</code>: The backend is in initial startup. Client
          authentication is performed during this phase.
         </p></li><li class="listitem"><p>
<code class="literal">active</code>: The backend is executing a query.
         </p></li><li class="listitem"><p>
<code class="literal">idle</code>: The backend is waiting for a new client command.
         </p></li><li class="listitem"><p>
<code class="literal">idle in transaction</code>: The backend is in a transaction,
          but is not currently executing a query.
         </p></li><li class="listitem"><p>
<code class="literal">idle in transaction (aborted)</code>: This state is similar to
          <code class="literal">idle in transaction</code>, except one of the statements in
          the transaction caused an error.
         </p></li><li class="listitem"><p>
<code class="literal">fastpath function call</code>: The backend is executing a
          fast-path function.
         </p></li><li class="listitem"><p>
<code class="literal">disabled</code>: This state is reported if <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-ACTIVITIES">track_activities</a> is disabled in this backend.
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_xid</code> <code class="type">xid</code>
</p>
<p>
       Top-level transaction identifier of this backend, if any;  see
       <a class="xref" href="../../internals/transactions/transaction-id.md">Section 67.1</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_xmin</code> <code class="type">xid</code>
</p>
<p>
       The current backend's <code class="literal">xmin</code> horizon.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">query_id</code> <code class="type">bigint</code>
</p>
<p>
      Identifier of this backend's most recent query. If
      <code class="structfield">state</code> is <code class="literal">active</code> this
      field shows the identifier of the currently executing query. In
      all other states, it shows the identifier of last query that was
      executed.  Query identifiers are not computed by default so this
      field will be null unless <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID">compute_query_id</a>
      parameter is enabled or a third-party module that computes query
      identifiers is configured.
     </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">query</code> <code class="type">text</code>
</p>
<p>
       Text of this backend's most recent query. If
       <code class="structfield">state</code> is <code class="literal">active</code> this field shows the
       currently executing query. In all other states, it shows the last query
       that was executed. By default the query text is truncated at 1024
       bytes; this value can be changed via the parameter
       <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-ACTIVITY-QUERY-SIZE">track_activity_query_size</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_type</code> <code class="type">text</code>
</p>
<p>
       Type of current backend. Possible types are
       <code class="literal">autovacuum launcher</code>, <code class="literal">autovacuum worker</code>,
       <code class="literal">logical replication launcher</code>,
       <code class="literal">logical replication worker</code>,
       <code class="literal">parallel worker</code>, <code class="literal">background writer</code>,
       <code class="literal">client backend</code>, <code class="literal">checkpointer</code>,
       <code class="literal">archiver</code>, <code class="literal">standalone backend</code>,
       <code class="literal">startup</code>, <code class="literal">walreceiver</code>,
       <code class="literal">walsender</code>, <code class="literal">walwriter</code> and
       <code class="literal">walsummarizer</code>.
       In addition, background workers registered by extensions may have
       additional types.
      </p></td></tr></tbody></table>

<br>

### Note

The `wait_event` and `state` columns are
independent. If a backend is in the `active` state,
it may or may not be `waiting` on some event. If the state
is `active` and `wait_event` is non-null, it
means that a query is being executed, but is being blocked somewhere
in the system. To keep the reporting overhead low, the system does not
attempt to synchronize different aspects of activity data for a backend.
As a result, ephemeral discrepancies may exist between the view's columns.

<a id="WAIT-EVENT-TABLE"></a>

**Table 27.4. Wait Event Types**

<table border="1" class="table" summary="Wait Event Types"><colgroup><col/><col/></colgroup><thead><tr><th>Wait Event Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">Activity</code></td><td>The server process is idle.  This event type indicates a process
       waiting for activity in its main processing loop.
       <code class="literal">wait_event</code> will identify the specific wait point;
       see <a class="xref" href="monitoring-stats.md#WAIT-EVENT-ACTIVITY-TABLE">Table 27.5</a>.
      </td></tr><tr><td><code class="literal">BufferPin</code></td><td>The server process is waiting for exclusive access to
       a data buffer.  Buffer pin waits can be protracted if
       another process holds an open cursor that last read data from the
       buffer in question. See <a class="xref" href="monitoring-stats.md#WAIT-EVENT-BUFFERPIN-TABLE">Table 27.6</a>.
      </td></tr><tr><td><code class="literal">Client</code></td><td>The server process is waiting for activity on a socket
       connected to a user application.  Thus, the server expects something
       to happen that is independent of its internal processes.
       <code class="literal">wait_event</code> will identify the specific wait point;
       see <a class="xref" href="monitoring-stats.md#WAIT-EVENT-CLIENT-TABLE">Table 27.7</a>.
      </td></tr><tr><td><code class="literal">Extension</code></td><td>The server process is waiting for some condition defined by an
       extension module.
       See <a class="xref" href="monitoring-stats.md#WAIT-EVENT-EXTENSION-TABLE">Table 27.8</a>.
      </td></tr><tr><td><code class="literal">InjectionPoint</code></td><td>The server process is waiting for an injection point to reach an
       outcome defined in a test.  See
       <a class="xref" href="../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS">Section 36.10.14</a> for more details.  This
       type has no predefined wait points.
      </td></tr><tr><td><code class="literal">IO</code></td><td>The server process is waiting for an I/O operation to complete.
       <code class="literal">wait_event</code> will identify the specific wait point;
       see <a class="xref" href="monitoring-stats.md#WAIT-EVENT-IO-TABLE">Table 27.9</a>.
      </td></tr><tr><td><code class="literal">IPC</code></td><td>The server process is waiting for some interaction with
       another server process.  <code class="literal">wait_event</code> will
       identify the specific wait point;
       see <a class="xref" href="monitoring-stats.md#WAIT-EVENT-IPC-TABLE">Table 27.10</a>.
      </td></tr><tr><td><code class="literal">Lock</code></td><td>The server process is waiting for a heavyweight lock.
       Heavyweight locks, also known as lock manager locks or simply locks,
       primarily protect SQL-visible objects such as tables.  However,
       they are also used to ensure mutual exclusion for certain internal
       operations such as relation extension.  <code class="literal">wait_event</code>
       will identify the type of lock awaited;
       see <a class="xref" href="monitoring-stats.md#WAIT-EVENT-LOCK-TABLE">Table 27.11</a>.
      </td></tr><tr><td><code class="literal">LWLock</code></td><td> The server process is waiting for a lightweight lock.
       Most such locks protect a particular data structure in shared memory.
       <code class="literal">wait_event</code> will contain a name identifying the purpose
       of the lightweight lock.  (Some locks have specific names; others
       are part of a group of locks each with a similar purpose.)
       See <a class="xref" href="monitoring-stats.md#WAIT-EVENT-LWLOCK-TABLE">Table 27.12</a>.
      </td></tr><tr><td><code class="literal">Timeout</code></td><td>The server process is waiting for a timeout
       to expire.  <code class="literal">wait_event</code> will identify the specific wait
       point; see <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TIMEOUT-TABLE">Table 27.13</a>.
      </td></tr></tbody></table>

<br><a id="WAIT-EVENT-ACTIVITY-TABLE"></a>

**Table 27.5. Wait Events of Type `Activity`**

<table border="1" class="table" summary="Wait Events of Type Activity"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Activity</code> Wait Event</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">ArchiverMain</code></td><td>Waiting in main loop of archiver process.</td></tr><tr><td><code class="literal">AutovacuumMain</code></td><td>Waiting in main loop of autovacuum launcher process.</td></tr><tr><td><code class="literal">BgwriterHibernate</code></td><td>Waiting in background writer process, hibernating.</td></tr><tr><td><code class="literal">BgwriterMain</code></td><td>Waiting in main loop of background writer process.</td></tr><tr><td><code class="literal">CheckpointerMain</code></td><td>Waiting in main loop of checkpointer process.</td></tr><tr><td><code class="literal">CheckpointerShutdown</code></td><td>Waiting for checkpointer process to be terminated.</td></tr><tr><td><code class="literal">IoWorkerMain</code></td><td>Waiting in main loop of IO Worker process.</td></tr><tr><td><code class="literal">LogicalApplyMain</code></td><td>Waiting in main loop of logical replication apply process.</td></tr><tr><td><code class="literal">LogicalLauncherMain</code></td><td>Waiting in main loop of logical replication launcher process.</td></tr><tr><td><code class="literal">LogicalParallelApplyMain</code></td><td>Waiting in main loop of logical replication parallel apply process.</td></tr><tr><td><code class="literal">RecoveryWalStream</code></td><td>Waiting in main loop of startup process for WAL to arrive, during streaming recovery.</td></tr><tr><td><code class="literal">ReplicationSlotsyncMain</code></td><td>Waiting in main loop of slot sync worker.</td></tr><tr><td><code class="literal">ReplicationSlotsyncShutdown</code></td><td>Waiting for slot sync worker to shut down.</td></tr><tr><td><code class="literal">SysloggerMain</code></td><td>Waiting in main loop of syslogger process.</td></tr><tr><td><code class="literal">WalReceiverMain</code></td><td>Waiting in main loop of WAL receiver process.</td></tr><tr><td><code class="literal">WalSenderMain</code></td><td>Waiting in main loop of WAL sender process.</td></tr><tr><td><code class="literal">WalSummarizerWal</code></td><td>Waiting in WAL summarizer for more WAL to be generated.</td></tr><tr><td><code class="literal">WalWriterMain</code></td><td>Waiting in main loop of WAL writer process.</td></tr></tbody></table>

<br><a id="WAIT-EVENT-BUFFERPIN-TABLE"></a>

**Table 27.6. Wait Events of Type `Bufferpin`**

<table border="1" class="table" summary="Wait Events of Type Bufferpin"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">BufferPin</code> Wait Event</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">BufferPin</code></td><td>Waiting to acquire an exclusive pin on a buffer.</td></tr></tbody></table>

<br><a id="WAIT-EVENT-CLIENT-TABLE"></a>

**Table 27.7. Wait Events of Type `Client`**

<table border="1" class="table" summary="Wait Events of Type Client"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Client</code> Wait Event</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">ClientRead</code></td><td>Waiting to read data from the client.</td></tr><tr><td><code class="literal">ClientWrite</code></td><td>Waiting to write data to the client.</td></tr><tr><td><code class="literal">GssOpenServer</code></td><td>Waiting to read data from the client while establishing a GSSAPI session.</td></tr><tr><td><code class="literal">LibpqwalreceiverConnect</code></td><td>Waiting in WAL receiver to establish connection to remote server.</td></tr><tr><td><code class="literal">LibpqwalreceiverReceive</code></td><td>Waiting in WAL receiver to receive data from remote server.</td></tr><tr><td><code class="literal">SslOpenServer</code></td><td>Waiting for SSL while attempting connection.</td></tr><tr><td><code class="literal">WaitForStandbyConfirmation</code></td><td>Waiting for WAL to be received and flushed by the physical standby.</td></tr><tr><td><code class="literal">WalSenderWaitForWal</code></td><td>Waiting for WAL to be flushed in WAL sender process.</td></tr><tr><td><code class="literal">WalSenderWriteData</code></td><td>Waiting for any activity when processing replies from WAL receiver in WAL sender process.</td></tr></tbody></table>

<br><a id="WAIT-EVENT-EXTENSION-TABLE"></a>

**Table 27.8. Wait Events of Type `Extension`**

<table border="1" class="table" summary="Wait Events of Type Extension"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Extension</code> Wait Event</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">Extension</code></td><td>Waiting in an extension.</td></tr></tbody></table>

<br><a id="WAIT-EVENT-IO-TABLE"></a>

**Table 27.9. Wait Events of Type `Io`**

<table border="1" class="table" summary="Wait Events of Type Io"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">IO</code> Wait Event</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">AioIoCompletion</code></td><td>Waiting for another process to complete IO.</td></tr><tr><td><code class="literal">AioIoUringExecution</code></td><td>Waiting for IO execution via io_uring.</td></tr><tr><td><code class="literal">AioIoUringSubmit</code></td><td>Waiting for IO submission via io_uring.</td></tr><tr><td><code class="literal">BasebackupRead</code></td><td>Waiting for base backup to read from a file.</td></tr><tr><td><code class="literal">BasebackupSync</code></td><td>Waiting for data written by a base backup to reach durable storage.</td></tr><tr><td><code class="literal">BasebackupWrite</code></td><td>Waiting for base backup to write to a file.</td></tr><tr><td><code class="literal">BuffileRead</code></td><td>Waiting for a read from a buffered file.</td></tr><tr><td><code class="literal">BuffileTruncate</code></td><td>Waiting for a buffered file to be truncated.</td></tr><tr><td><code class="literal">BuffileWrite</code></td><td>Waiting for a write to a buffered file.</td></tr><tr><td><code class="literal">ControlFileRead</code></td><td>Waiting for a read from the <code class="filename">pg_control</code> file.</td></tr><tr><td><code class="literal">ControlFileSync</code></td><td>Waiting for the <code class="filename">pg_control</code> file to reach durable storage.</td></tr><tr><td><code class="literal">ControlFileSyncUpdate</code></td><td>Waiting for an update to the <code class="filename">pg_control</code> file to reach durable storage.</td></tr><tr><td><code class="literal">ControlFileWrite</code></td><td>Waiting for a write to the <code class="filename">pg_control</code> file.</td></tr><tr><td><code class="literal">ControlFileWriteUpdate</code></td><td>Waiting for a write to update the <code class="filename">pg_control</code> file.</td></tr><tr><td><code class="literal">CopyFileCopy</code></td><td>Waiting for a file copy operation.</td></tr><tr><td><code class="literal">CopyFileRead</code></td><td>Waiting for a read during a file copy operation.</td></tr><tr><td><code class="literal">CopyFileWrite</code></td><td>Waiting for a write during a file copy operation.</td></tr><tr><td><code class="literal">DataFileExtend</code></td><td>Waiting for a relation data file to be extended.</td></tr><tr><td><code class="literal">DataFileFlush</code></td><td>Waiting for a relation data file to reach durable storage.</td></tr><tr><td><code class="literal">DataFileImmediateSync</code></td><td>Waiting for an immediate synchronization of a relation data file to durable storage.</td></tr><tr><td><code class="literal">DataFilePrefetch</code></td><td>Waiting for an asynchronous prefetch from a relation data file.</td></tr><tr><td><code class="literal">DataFileRead</code></td><td>Waiting for a read from a relation data file.</td></tr><tr><td><code class="literal">DataFileSync</code></td><td>Waiting for changes to a relation data file to reach durable storage.</td></tr><tr><td><code class="literal">DataFileTruncate</code></td><td>Waiting for a relation data file to be truncated.</td></tr><tr><td><code class="literal">DataFileWrite</code></td><td>Waiting for a write to a relation data file.</td></tr><tr><td><code class="literal">DsmAllocate</code></td><td>Waiting for a dynamic shared memory segment to be allocated.</td></tr><tr><td><code class="literal">DsmFillZeroWrite</code></td><td>Waiting to fill a dynamic shared memory backing file with zeroes.</td></tr><tr><td><code class="literal">LockFileAddtodatadirRead</code></td><td>Waiting for a read while adding a line to the data directory lock file.</td></tr><tr><td><code class="literal">LockFileAddtodatadirSync</code></td><td>Waiting for data to reach durable storage while adding a line to the data directory lock file.</td></tr><tr><td><code class="literal">LockFileAddtodatadirWrite</code></td><td>Waiting for a write while adding a line to the data directory lock file.</td></tr><tr><td><code class="literal">LockFileCreateRead</code></td><td>Waiting to read while creating the data directory lock file.</td></tr><tr><td><code class="literal">LockFileCreateSync</code></td><td>Waiting for data to reach durable storage while creating the data directory lock file.</td></tr><tr><td><code class="literal">LockFileCreateWrite</code></td><td>Waiting for a write while creating the data directory lock file.</td></tr><tr><td><code class="literal">LockFileRecheckdatadirRead</code></td><td>Waiting for a read during recheck of the data directory lock file.</td></tr><tr><td><code class="literal">LogicalRewriteCheckpointSync</code></td><td>Waiting for logical rewrite mappings to reach durable storage during a checkpoint.</td></tr><tr><td><code class="literal">LogicalRewriteMappingSync</code></td><td>Waiting for mapping data to reach durable storage during a logical rewrite.</td></tr><tr><td><code class="literal">LogicalRewriteMappingWrite</code></td><td>Waiting for a write of mapping data during a logical rewrite.</td></tr><tr><td><code class="literal">LogicalRewriteSync</code></td><td>Waiting for logical rewrite mappings to reach durable storage.</td></tr><tr><td><code class="literal">LogicalRewriteTruncate</code></td><td>Waiting for truncate of mapping data during a logical rewrite.</td></tr><tr><td><code class="literal">LogicalRewriteWrite</code></td><td>Waiting for a write of logical rewrite mappings.</td></tr><tr><td><code class="literal">RelationMapRead</code></td><td>Waiting for a read of the relation map file.</td></tr><tr><td><code class="literal">RelationMapReplace</code></td><td>Waiting for durable replacement of a relation map file.</td></tr><tr><td><code class="literal">RelationMapWrite</code></td><td>Waiting for a write to the relation map file.</td></tr><tr><td><code class="literal">ReorderBufferRead</code></td><td>Waiting for a read during reorder buffer management.</td></tr><tr><td><code class="literal">ReorderBufferWrite</code></td><td>Waiting for a write during reorder buffer management.</td></tr><tr><td><code class="literal">ReorderLogicalMappingRead</code></td><td>Waiting for a read of a logical mapping during reorder buffer management.</td></tr><tr><td><code class="literal">ReplicationSlotRead</code></td><td>Waiting for a read from a replication slot control file.</td></tr><tr><td><code class="literal">ReplicationSlotRestoreSync</code></td><td>Waiting for a replication slot control file to reach durable storage while restoring it to memory.</td></tr><tr><td><code class="literal">ReplicationSlotSync</code></td><td>Waiting for a replication slot control file to reach durable storage.</td></tr><tr><td><code class="literal">ReplicationSlotWrite</code></td><td>Waiting for a write to a replication slot control file.</td></tr><tr><td><code class="literal">SlruFlushSync</code></td><td>Waiting for SLRU data to reach durable storage during a checkpoint or database shutdown.</td></tr><tr><td><code class="literal">SlruRead</code></td><td>Waiting for a read of an SLRU page.</td></tr><tr><td><code class="literal">SlruSync</code></td><td>Waiting for SLRU data to reach durable storage following a page write.</td></tr><tr><td><code class="literal">SlruWrite</code></td><td>Waiting for a write of an SLRU page.</td></tr><tr><td><code class="literal">SnapbuildRead</code></td><td>Waiting for a read of a serialized historical catalog snapshot.</td></tr><tr><td><code class="literal">SnapbuildSync</code></td><td>Waiting for a serialized historical catalog snapshot to reach durable storage.</td></tr><tr><td><code class="literal">SnapbuildWrite</code></td><td>Waiting for a write of a serialized historical catalog snapshot.</td></tr><tr><td><code class="literal">TimelineHistoryFileSync</code></td><td>Waiting for a timeline history file received via streaming replication to reach durable storage.</td></tr><tr><td><code class="literal">TimelineHistoryFileWrite</code></td><td>Waiting for a write of a timeline history file received via streaming replication.</td></tr><tr><td><code class="literal">TimelineHistoryRead</code></td><td>Waiting for a read of a timeline history file.</td></tr><tr><td><code class="literal">TimelineHistorySync</code></td><td>Waiting for a newly created timeline history file to reach durable storage.</td></tr><tr><td><code class="literal">TimelineHistoryWrite</code></td><td>Waiting for a write of a newly created timeline history file.</td></tr><tr><td><code class="literal">TwophaseFileRead</code></td><td>Waiting for a read of a two phase state file.</td></tr><tr><td><code class="literal">TwophaseFileSync</code></td><td>Waiting for a two phase state file to reach durable storage.</td></tr><tr><td><code class="literal">TwophaseFileWrite</code></td><td>Waiting for a write of a two phase state file.</td></tr><tr><td><code class="literal">VersionFileSync</code></td><td>Waiting for the version file to reach durable storage while creating a database.</td></tr><tr><td><code class="literal">VersionFileWrite</code></td><td>Waiting for the version file to be written while creating a database.</td></tr><tr><td><code class="literal">WalsenderTimelineHistoryRead</code></td><td>Waiting for a read from a timeline history file during a walsender timeline command.</td></tr><tr><td><code class="literal">WalBootstrapSync</code></td><td>Waiting for WAL to reach durable storage during bootstrapping.</td></tr><tr><td><code class="literal">WalBootstrapWrite</code></td><td>Waiting for a write of a WAL page during bootstrapping.</td></tr><tr><td><code class="literal">WalCopyRead</code></td><td>Waiting for a read when creating a new WAL segment by copying an existing one.</td></tr><tr><td><code class="literal">WalCopySync</code></td><td>Waiting for a new WAL segment created by copying an existing one to reach durable storage.</td></tr><tr><td><code class="literal">WalCopyWrite</code></td><td>Waiting for a write when creating a new WAL segment by copying an existing one.</td></tr><tr><td><code class="literal">WalInitSync</code></td><td>Waiting for a newly initialized WAL file to reach durable storage.</td></tr><tr><td><code class="literal">WalInitWrite</code></td><td>Waiting for a write while initializing a new WAL file.</td></tr><tr><td><code class="literal">WalRead</code></td><td>Waiting for a read from a WAL file.</td></tr><tr><td><code class="literal">WalSummaryRead</code></td><td>Waiting for a read from a WAL summary file.</td></tr><tr><td><code class="literal">WalSummaryWrite</code></td><td>Waiting for a write to a WAL summary file.</td></tr><tr><td><code class="literal">WalSync</code></td><td>Waiting for a WAL file to reach durable storage.</td></tr><tr><td><code class="literal">WalSyncMethodAssign</code></td><td>Waiting for data to reach durable storage while assigning a new WAL sync method.</td></tr><tr><td><code class="literal">WalWrite</code></td><td>Waiting for a write to a WAL file.</td></tr></tbody></table>

<br><a id="WAIT-EVENT-IPC-TABLE"></a>

**Table 27.10. Wait Events of Type `Ipc`**

<table border="1" class="table" summary="Wait Events of Type Ipc"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">IPC</code> Wait Event</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">AppendReady</code></td><td>Waiting for subplan nodes of an <code class="literal">Append</code> plan node to be ready.</td></tr><tr><td><code class="literal">ArchiveCleanupCommand</code></td><td>Waiting for <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND">archive_cleanup_command</a> to complete.</td></tr><tr><td><code class="literal">ArchiveCommand</code></td><td>Waiting for <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-ARCHIVE-COMMAND">archive_command</a> to complete.</td></tr><tr><td><code class="literal">BackendTermination</code></td><td>Waiting for the termination of another backend.</td></tr><tr><td><code class="literal">BackupWaitWalArchive</code></td><td>Waiting for WAL files required for a backup to be successfully archived.</td></tr><tr><td><code class="literal">BgworkerShutdown</code></td><td>Waiting for background worker to shut down.</td></tr><tr><td><code class="literal">BgworkerStartup</code></td><td>Waiting for background worker to start up.</td></tr><tr><td><code class="literal">BtreePage</code></td><td>Waiting for the page number needed to continue a parallel B-tree scan to become available.</td></tr><tr><td><code class="literal">BufferIo</code></td><td>Waiting for buffer I/O to complete.</td></tr><tr><td><code class="literal">CheckpointDelayComplete</code></td><td>Waiting for a backend that blocks a checkpoint from completing.</td></tr><tr><td><code class="literal">CheckpointDelayStart</code></td><td>Waiting for a backend that blocks a checkpoint from starting.</td></tr><tr><td><code class="literal">CheckpointDone</code></td><td>Waiting for a checkpoint to complete.</td></tr><tr><td><code class="literal">CheckpointStart</code></td><td>Waiting for a checkpoint to start.</td></tr><tr><td><code class="literal">ExecuteGather</code></td><td>Waiting for activity from a child process while executing a <code class="literal">Gather</code> plan node.</td></tr><tr><td><code class="literal">HashBatchAllocate</code></td><td>Waiting for an elected Parallel Hash participant to allocate a hash table.</td></tr><tr><td><code class="literal">HashBatchElect</code></td><td>Waiting to elect a Parallel Hash participant to allocate a hash table.</td></tr><tr><td><code class="literal">HashBatchLoad</code></td><td>Waiting for other Parallel Hash participants to finish loading a hash table.</td></tr><tr><td><code class="literal">HashBuildAllocate</code></td><td>Waiting for an elected Parallel Hash participant to allocate the initial hash table.</td></tr><tr><td><code class="literal">HashBuildElect</code></td><td>Waiting to elect a Parallel Hash participant to allocate the initial hash table.</td></tr><tr><td><code class="literal">HashBuildHashInner</code></td><td>Waiting for other Parallel Hash participants to finish hashing the inner relation.</td></tr><tr><td><code class="literal">HashBuildHashOuter</code></td><td>Waiting for other Parallel Hash participants to finish partitioning the outer relation.</td></tr><tr><td><code class="literal">HashGrowBatchesDecide</code></td><td>Waiting to elect a Parallel Hash participant to decide on future batch growth.</td></tr><tr><td><code class="literal">HashGrowBatchesElect</code></td><td>Waiting to elect a Parallel Hash participant to allocate more batches.</td></tr><tr><td><code class="literal">HashGrowBatchesFinish</code></td><td>Waiting for an elected Parallel Hash participant to decide on future batch growth.</td></tr><tr><td><code class="literal">HashGrowBatchesReallocate</code></td><td>Waiting for an elected Parallel Hash participant to allocate more batches.</td></tr><tr><td><code class="literal">HashGrowBatchesRepartition</code></td><td>Waiting for other Parallel Hash participants to finish repartitioning.</td></tr><tr><td><code class="literal">HashGrowBucketsElect</code></td><td>Waiting to elect a Parallel Hash participant to allocate more buckets.</td></tr><tr><td><code class="literal">HashGrowBucketsReallocate</code></td><td>Waiting for an elected Parallel Hash participant to finish allocating more buckets.</td></tr><tr><td><code class="literal">HashGrowBucketsReinsert</code></td><td>Waiting for other Parallel Hash participants to finish inserting tuples into new buckets.</td></tr><tr><td><code class="literal">LogicalApplySendData</code></td><td>Waiting for a logical replication leader apply process to send data to a parallel apply process.</td></tr><tr><td><code class="literal">LogicalParallelApplyStateChange</code></td><td>Waiting for a logical replication parallel apply process to change state.</td></tr><tr><td><code class="literal">LogicalSyncData</code></td><td>Waiting for a logical replication remote server to send data for initial table synchronization.</td></tr><tr><td><code class="literal">LogicalSyncStateChange</code></td><td>Waiting for a logical replication remote server to change state.</td></tr><tr><td><code class="literal">MessageQueueInternal</code></td><td>Waiting for another process to be attached to a shared message queue.</td></tr><tr><td><code class="literal">MessageQueuePutMessage</code></td><td>Waiting to write a protocol message to a shared message queue.</td></tr><tr><td><code class="literal">MessageQueueReceive</code></td><td>Waiting to receive bytes from a shared message queue.</td></tr><tr><td><code class="literal">MessageQueueSend</code></td><td>Waiting to send bytes to a shared message queue.</td></tr><tr><td><code class="literal">MultixactCreation</code></td><td>Waiting for a multixact creation to complete.</td></tr><tr><td><code class="literal">ParallelBitmapScan</code></td><td>Waiting for parallel bitmap scan to become initialized.</td></tr><tr><td><code class="literal">ParallelCreateIndexScan</code></td><td>Waiting for parallel <code class="command">CREATE INDEX</code> workers to finish heap scan.</td></tr><tr><td><code class="literal">ParallelFinish</code></td><td>Waiting for parallel workers to finish computing.</td></tr><tr><td><code class="literal">ProcarrayGroupUpdate</code></td><td>Waiting for the group leader to clear the transaction ID at transaction end.</td></tr><tr><td><code class="literal">ProcSignalBarrier</code></td><td>Waiting for a barrier event to be processed by all backends.</td></tr><tr><td><code class="literal">Promote</code></td><td>Waiting for standby promotion.</td></tr><tr><td><code class="literal">RecoveryConflictSnapshot</code></td><td>Waiting for recovery conflict resolution for a vacuum cleanup.</td></tr><tr><td><code class="literal">RecoveryConflictTablespace</code></td><td>Waiting for recovery conflict resolution for dropping a tablespace.</td></tr><tr><td><code class="literal">RecoveryEndCommand</code></td><td>Waiting for <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-RECOVERY-END-COMMAND">recovery_end_command</a> to complete.</td></tr><tr><td><code class="literal">RecoveryPause</code></td><td>Waiting for recovery to be resumed.</td></tr><tr><td><code class="literal">ReplicationOriginDrop</code></td><td>Waiting for a replication origin to become inactive so it can be dropped.</td></tr><tr><td><code class="literal">ReplicationSlotDrop</code></td><td>Waiting for a replication slot to become inactive so it can be dropped.</td></tr><tr><td><code class="literal">RestoreCommand</code></td><td>Waiting for <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-RESTORE-COMMAND">restore_command</a> to complete.</td></tr><tr><td><code class="literal">SafeSnapshot</code></td><td>Waiting to obtain a valid snapshot for a <code class="literal">READ ONLY DEFERRABLE</code> transaction.</td></tr><tr><td><code class="literal">SyncRep</code></td><td>Waiting for confirmation from a remote server during synchronous replication.</td></tr><tr><td><code class="literal">WalReceiverExit</code></td><td>Waiting for the WAL receiver to exit.</td></tr><tr><td><code class="literal">WalReceiverUpstreamCatchup</code></td><td>Waiting for upstream server WAL flush position to catch up to requested start point.</td></tr><tr><td><code class="literal">WalReceiverWaitStart</code></td><td>Waiting for startup process to send initial data for streaming replication.</td></tr><tr><td><code class="literal">WalSummaryReady</code></td><td>Waiting for a new WAL summary to be generated.</td></tr><tr><td><code class="literal">XactGroupUpdate</code></td><td>Waiting for the group leader to update transaction status at transaction end.</td></tr></tbody></table>

<br><a id="WAIT-EVENT-LOCK-TABLE"></a>

**Table 27.11. Wait Events of Type `Lock`**

<table border="1" class="table" summary="Wait Events of Type Lock"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Lock</code> Wait Event</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">advisory</code></td><td>Waiting to acquire an advisory user lock.</td></tr><tr><td><code class="literal">applytransaction</code></td><td>Waiting to acquire a lock on a remote transaction being applied by a logical replication subscriber.</td></tr><tr><td><code class="literal">extend</code></td><td>Waiting to extend a relation.</td></tr><tr><td><code class="literal">frozenid</code></td><td>Waiting to update <code class="structname">pg_database</code>.<code class="structfield">datfrozenxid</code> and <code class="structname">pg_database</code>.<code class="structfield">datminmxid</code>.</td></tr><tr><td><code class="literal">object</code></td><td>Waiting to acquire a lock on a non-relation database object.</td></tr><tr><td><code class="literal">page</code></td><td>Waiting to acquire a lock on a page of a relation.</td></tr><tr><td><code class="literal">relation</code></td><td>Waiting to acquire a lock on a relation.</td></tr><tr><td><code class="literal">spectoken</code></td><td>Waiting to acquire a speculative insertion lock.</td></tr><tr><td><code class="literal">transactionid</code></td><td>Waiting for a transaction to finish.</td></tr><tr><td><code class="literal">tuple</code></td><td>Waiting to acquire a lock on a tuple.</td></tr><tr><td><code class="literal">userlock</code></td><td>Waiting to acquire a user lock.</td></tr><tr><td><code class="literal">virtualxid</code></td><td>Waiting to acquire a virtual transaction ID lock; see <a class="xref" href="../../internals/transactions/transaction-id.md">Section 67.1</a>.</td></tr></tbody></table>

<br><a id="WAIT-EVENT-LWLOCK-TABLE"></a>

**Table 27.12. Wait Events of Type `Lwlock`**

<table border="1" class="table" summary="Wait Events of Type Lwlock"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">LWLock</code> Wait Event</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">AddinShmemInit</code></td><td>Waiting to manage an extension's space allocation in shared memory.</td></tr><tr><td><code class="literal">AioUringCompletion</code></td><td>Waiting for another process to complete IO via io_uring.</td></tr><tr><td><code class="literal">AioWorkerSubmissionQueue</code></td><td>Waiting to access AIO worker submission queue.</td></tr><tr><td><code class="literal">AutoFile</code></td><td>Waiting to update the <code class="filename">postgresql.auto.conf</code> file.</td></tr><tr><td><code class="literal">Autovacuum</code></td><td>Waiting to read or update the current state of autovacuum workers.</td></tr><tr><td><code class="literal">AutovacuumSchedule</code></td><td>Waiting to ensure that a table selected for autovacuum still needs vacuuming.</td></tr><tr><td><code class="literal">BackgroundWorker</code></td><td>Waiting to read or update background worker state.</td></tr><tr><td><code class="literal">BtreeVacuum</code></td><td>Waiting to read or update vacuum-related information for a B-tree index.</td></tr><tr><td><code class="literal">BufferContent</code></td><td>Waiting to access a data page in memory.</td></tr><tr><td><code class="literal">BufferMapping</code></td><td>Waiting to associate a data block with a buffer in the buffer pool.</td></tr><tr><td><code class="literal">CheckpointerComm</code></td><td>Waiting to manage fsync requests.</td></tr><tr><td><code class="literal">CommitTs</code></td><td>Waiting to read or update the last value set for a transaction commit timestamp.</td></tr><tr><td><code class="literal">CommitTsBuffer</code></td><td>Waiting for I/O on a commit timestamp SLRU buffer.</td></tr><tr><td><code class="literal">CommitTsSLRU</code></td><td>Waiting to access the commit timestamp SLRU cache.</td></tr><tr><td><code class="literal">ControlFile</code></td><td>Waiting to read or update the <code class="filename">pg_control</code> file or create a new WAL file.</td></tr><tr><td><code class="literal">DSMRegistry</code></td><td>Waiting to read or update the dynamic shared memory registry.</td></tr><tr><td><code class="literal">DSMRegistryDSA</code></td><td>Waiting to access dynamic shared memory registry's dynamic shared memory allocator.</td></tr><tr><td><code class="literal">DSMRegistryHash</code></td><td>Waiting to access dynamic shared memory registry's shared hash table.</td></tr><tr><td><code class="literal">DynamicSharedMemoryControl</code></td><td>Waiting to read or update dynamic shared memory allocation information.</td></tr><tr><td><code class="literal">InjectionPoint</code></td><td>Waiting to read or update information related to injection points.</td></tr><tr><td><code class="literal">LockFastPath</code></td><td>Waiting to read or update a process' fast-path lock information.</td></tr><tr><td><code class="literal">LockManager</code></td><td>Waiting to read or update information about <span class="quote">“<span class="quote">heavyweight</span>”</span> locks.</td></tr><tr><td><code class="literal">LogicalRepLauncherDSA</code></td><td>Waiting to access logical replication launcher's dynamic shared memory allocator.</td></tr><tr><td><code class="literal">LogicalRepLauncherHash</code></td><td>Waiting to access logical replication launcher's shared hash table.</td></tr><tr><td><code class="literal">LogicalRepWorker</code></td><td>Waiting to read or update the state of logical replication workers.</td></tr><tr><td><code class="literal">MultiXactGen</code></td><td>Waiting to read or update shared multixact state.</td></tr><tr><td><code class="literal">MultiXactMemberBuffer</code></td><td>Waiting for I/O on a multixact member SLRU buffer.</td></tr><tr><td><code class="literal">MultiXactMemberSLRU</code></td><td>Waiting to access the multixact member SLRU cache.</td></tr><tr><td><code class="literal">MultiXactOffsetBuffer</code></td><td>Waiting for I/O on a multixact offset SLRU buffer.</td></tr><tr><td><code class="literal">MultiXactOffsetSLRU</code></td><td>Waiting to access the multixact offset SLRU cache.</td></tr><tr><td><code class="literal">MultiXactTruncation</code></td><td>Waiting to read or truncate multixact information.</td></tr><tr><td><code class="literal">NotifyBuffer</code></td><td>Waiting for I/O on a <code class="command">NOTIFY</code> message SLRU buffer.</td></tr><tr><td><code class="literal">NotifyQueue</code></td><td>Waiting to read or update <code class="command">NOTIFY</code> messages.</td></tr><tr><td><code class="literal">NotifyQueueTail</code></td><td>Waiting to update limit on <code class="command">NOTIFY</code> message storage.</td></tr><tr><td><code class="literal">NotifySLRU</code></td><td>Waiting to access the <code class="command">NOTIFY</code> message SLRU cache.</td></tr><tr><td><code class="literal">OidGen</code></td><td>Waiting to allocate a new OID.</td></tr><tr><td><code class="literal">ParallelAppend</code></td><td>Waiting to choose the next subplan during Parallel Append plan execution.</td></tr><tr><td><code class="literal">ParallelBtreeScan</code></td><td>Waiting to synchronize workers during Parallel B-tree scan plan execution.</td></tr><tr><td><code class="literal">ParallelHashJoin</code></td><td>Waiting to synchronize workers during Parallel Hash Join plan execution.</td></tr><tr><td><code class="literal">ParallelQueryDSA</code></td><td>Waiting for parallel query dynamic shared memory allocation.</td></tr><tr><td><code class="literal">ParallelVacuumDSA</code></td><td>Waiting for parallel vacuum dynamic shared memory allocation.</td></tr><tr><td><code class="literal">PerSessionDSA</code></td><td>Waiting for parallel query dynamic shared memory allocation.</td></tr><tr><td><code class="literal">PerSessionRecordType</code></td><td>Waiting to access a parallel query's information about composite types.</td></tr><tr><td><code class="literal">PerSessionRecordTypmod</code></td><td>Waiting to access a parallel query's information about type modifiers that identify anonymous record types.</td></tr><tr><td><code class="literal">PerXactPredicateList</code></td><td>Waiting to access the list of predicate locks held by the current serializable transaction during a parallel query.</td></tr><tr><td><code class="literal">PgStatsData</code></td><td>Waiting for shared memory stats data access.</td></tr><tr><td><code class="literal">PgStatsDSA</code></td><td>Waiting for stats dynamic shared memory allocator access.</td></tr><tr><td><code class="literal">PgStatsHash</code></td><td>Waiting for stats shared memory hash table access.</td></tr><tr><td><code class="literal">PredicateLockManager</code></td><td>Waiting to access predicate lock information used by serializable transactions.</td></tr><tr><td><code class="literal">ProcArray</code></td><td>Waiting to access the shared per-process data structures (typically, to get a snapshot or report a session's transaction ID).</td></tr><tr><td><code class="literal">RelationMapping</code></td><td>Waiting to read or update a <code class="filename">pg_filenode.map</code> file (used to track the filenode assignments of certain system catalogs).</td></tr><tr><td><code class="literal">RelCacheInit</code></td><td>Waiting to read or update a <code class="filename">pg_internal.init</code> relation cache initialization file.</td></tr><tr><td><code class="literal">ReplicationOrigin</code></td><td>Waiting to create, drop or use a replication origin.</td></tr><tr><td><code class="literal">ReplicationOriginState</code></td><td>Waiting to read or update the progress of one replication origin.</td></tr><tr><td><code class="literal">ReplicationSlotAllocation</code></td><td>Waiting to allocate or free a replication slot.</td></tr><tr><td><code class="literal">ReplicationSlotControl</code></td><td>Waiting to read or update replication slot state.</td></tr><tr><td><code class="literal">ReplicationSlotIO</code></td><td>Waiting for I/O on a replication slot.</td></tr><tr><td><code class="literal">SerialBuffer</code></td><td>Waiting for I/O on a serializable transaction conflict SLRU buffer.</td></tr><tr><td><code class="literal">SerialControl</code></td><td>Waiting to read or update shared <code class="filename">pg_serial</code> state.</td></tr><tr><td><code class="literal">SerializableFinishedList</code></td><td>Waiting to access the list of finished serializable transactions.</td></tr><tr><td><code class="literal">SerializablePredicateList</code></td><td>Waiting to access the list of predicate locks held by serializable transactions.</td></tr><tr><td><code class="literal">SerializableXactHash</code></td><td>Waiting to read or update information about serializable transactions.</td></tr><tr><td><code class="literal">SerialSLRU</code></td><td>Waiting to access the serializable transaction conflict SLRU cache.</td></tr><tr><td><code class="literal">SharedTidBitmap</code></td><td>Waiting to access a shared TID bitmap during a parallel bitmap index scan.</td></tr><tr><td><code class="literal">SharedTupleStore</code></td><td>Waiting to access a shared tuple store during parallel query.</td></tr><tr><td><code class="literal">ShmemIndex</code></td><td>Waiting to find or allocate space in shared memory.</td></tr><tr><td><code class="literal">SInvalRead</code></td><td>Waiting to retrieve messages from the shared catalog invalidation queue.</td></tr><tr><td><code class="literal">SInvalWrite</code></td><td>Waiting to add a message to the shared catalog invalidation queue.</td></tr><tr><td><code class="literal">SubtransBuffer</code></td><td>Waiting for I/O on a sub-transaction SLRU buffer.</td></tr><tr><td><code class="literal">SubtransSLRU</code></td><td>Waiting to access the sub-transaction SLRU cache.</td></tr><tr><td><code class="literal">SyncRep</code></td><td>Waiting to read or update information about the state of synchronous replication.</td></tr><tr><td><code class="literal">SyncScan</code></td><td>Waiting to select the starting location of a synchronized table scan.</td></tr><tr><td><code class="literal">TablespaceCreate</code></td><td>Waiting to create or drop a tablespace.</td></tr><tr><td><code class="literal">TwoPhaseState</code></td><td>Waiting to read or update the state of prepared transactions.</td></tr><tr><td><code class="literal">WaitEventCustom</code></td><td>Waiting to read or update custom wait events information.</td></tr><tr><td><code class="literal">WALBufMapping</code></td><td>Waiting to replace a page in WAL buffers.</td></tr><tr><td><code class="literal">WALInsert</code></td><td>Waiting to insert WAL data into a memory buffer.</td></tr><tr><td><code class="literal">WALSummarizer</code></td><td>Waiting to read or update WAL summarization state.</td></tr><tr><td><code class="literal">WALWrite</code></td><td>Waiting for WAL buffers to be written to disk.</td></tr><tr><td><code class="literal">WrapLimitsVacuum</code></td><td>Waiting to update limits on transaction id and multixact consumption.</td></tr><tr><td><code class="literal">XactBuffer</code></td><td>Waiting for I/O on a transaction status SLRU buffer.</td></tr><tr><td><code class="literal">XactSLRU</code></td><td>Waiting to access the transaction status SLRU cache.</td></tr><tr><td><code class="literal">XactTruncation</code></td><td>Waiting to execute <code class="function">pg_xact_status</code> or update the oldest transaction ID available to it.</td></tr><tr><td><code class="literal">XidGen</code></td><td>Waiting to allocate a new transaction ID.</td></tr></tbody></table>

<br><a id="WAIT-EVENT-TIMEOUT-TABLE"></a>

**Table 27.13. Wait Events of Type `Timeout`**

<table border="1" class="table" summary="Wait Events of Type Timeout"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Timeout</code> Wait Event</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">BaseBackupThrottle</code></td><td>Waiting during base backup when throttling activity.</td></tr><tr><td><code class="literal">CheckpointWriteDelay</code></td><td>Waiting between writes while performing a checkpoint.</td></tr><tr><td><code class="literal">PgSleep</code></td><td>Waiting due to a call to <code class="function">pg_sleep</code> or a sibling function.</td></tr><tr><td><code class="literal">RecoveryApplyDelay</code></td><td>Waiting to apply WAL during recovery because of a delay setting.</td></tr><tr><td><code class="literal">RecoveryRetrieveRetryInterval</code></td><td>Waiting during recovery when WAL data is not available from any source (<code class="filename">pg_wal</code>, archive or stream).</td></tr><tr><td><code class="literal">RegisterSyncRequest</code></td><td>Waiting while sending synchronization requests to the checkpointer, because the request queue is full.</td></tr><tr><td><code class="literal">SpinDelay</code></td><td>Waiting while acquiring a contended spinlock.</td></tr><tr><td><code class="literal">VacuumDelay</code></td><td>Waiting in a cost-based vacuum delay point.</td></tr><tr><td><code class="literal">VacuumTruncate</code></td><td>Waiting to acquire an exclusive lock to truncate off any empty pages at the end of a table vacuumed.</td></tr><tr><td><code class="literal">WalSummarizerError</code></td><td>Waiting after a WAL summarizer error.</td></tr></tbody></table>

<br>

Here are examples of how wait events can be viewed:

```

SELECT pid, wait_event_type, wait_event FROM pg_stat_activity WHERE wait_event is NOT NULL;
 pid  | wait_event_type | wait_event
------+-----------------+------------
 2540 | Lock            | relation
 6644 | LWLock          | ProcArray
(2 rows)
```

```

SELECT a.pid, a.wait_event, w.description
  FROM pg_stat_activity a JOIN
       pg_wait_events w ON (a.wait_event_type = w.type AND
                            a.wait_event = w.name)
  WHERE a.wait_event is NOT NULL and a.state = 'active';
-[ RECORD 1 ]------------------------------------------------------​------------
pid         | 686674
wait_event  | WALInitSync
description | Waiting for a newly initialized WAL file to reach durable storage
```

### Note

Extensions can add `Extension`,
`InjectionPoint`, and `LWLock` events
to the lists shown in [Table 27.8](monitoring-stats.md#WAIT-EVENT-EXTENSION-TABLE) and
[Table 27.12](monitoring-stats.md#WAIT-EVENT-LWLOCK-TABLE). In some cases, the name
of an `LWLock` assigned by an extension will not be
available in all server processes. It might be reported as just
“`extension`” rather than the
extension-assigned name.

<a id="MONITORING-PG-STAT-REPLICATION-VIEW"></a>

### 27.2.4. `pg_stat_replication` [#](#MONITORING-PG-STAT-REPLICATION-VIEW)

<a id="id-1.6.14.7.8.2"></a>

The `pg_stat_replication` view will contain one row
per WAL sender process, showing statistics about replication to that
sender's connected standby server. Only directly connected standbys are
listed; no information is available about downstream standby servers.

<a id="PG-STAT-REPLICATION-VIEW"></a>

**Table 27.14. `pg_stat_replication` View**

<table border="1" class="table" summary="pg_stat_replication View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of a WAL sender process
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesysid</code> <code class="type">oid</code>
</p>
<p>
       OID of the user logged into this WAL sender process
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usename</code> <code class="type">name</code>
</p>
<p>
       Name of the user logged into this WAL sender process
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">application_name</code> <code class="type">text</code>
</p>
<p>
       Name of the application that is connected
       to this WAL sender
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_addr</code> <code class="type">inet</code>
</p>
<p>
       IP address of the client connected to this WAL sender.
       If this field is null, it indicates that the client is
       connected via a Unix socket on the server machine.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_hostname</code> <code class="type">text</code>
</p>
<p>
       Host name of the connected client, as reported by a
       reverse DNS lookup of <code class="structfield">client_addr</code>. This field will
       only be non-null for IP connections, and only when <a class="xref" href="../runtime-config/runtime-config-logging.md#GUC-LOG-HOSTNAME">log_hostname</a> is enabled.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_port</code> <code class="type">integer</code>
</p>
<p>
       TCP port number that the client is using for communication
       with this WAL sender, or <code class="literal">-1</code> if a Unix socket is used
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_start</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time when this process was started, i.e., when the
       client connected to this WAL sender
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_xmin</code> <code class="type">xid</code>
</p>
<p>
       This standby's <code class="literal">xmin</code> horizon reported
       by <a class="xref" href="../runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK">hot_standby_feedback</a>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">state</code> <code class="type">text</code>
</p>
<p>
       Current WAL sender state.
       Possible values are:
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">startup</code>: This WAL sender is starting up.
         </p></li><li class="listitem"><p>
<code class="literal">catchup</code>: This WAL sender's connected standby is
          catching up with the primary.
         </p></li><li class="listitem"><p>
<code class="literal">streaming</code>: This WAL sender is streaming changes
          after its connected standby server has caught up with the primary.
         </p></li><li class="listitem"><p>
<code class="literal">backup</code>: This WAL sender is sending a backup.
         </p></li><li class="listitem"><p>
<code class="literal">stopping</code>: This WAL sender is stopping.
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sent_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Last write-ahead log location sent on this connection
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">write_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Last write-ahead log location written to disk by this standby
       server
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">flush_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Last write-ahead log location flushed to disk by this standby
       server
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">replay_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Last write-ahead log location replayed into the database on this
       standby server
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">write_lag</code> <code class="type">interval</code>
</p>
<p>
       Time elapsed between flushing recent WAL locally and receiving
       notification that this standby server has written it (but not yet
       flushed it or applied it).  This can be used to gauge the delay that
       <code class="literal">synchronous_commit</code> level
       <code class="literal">remote_write</code> incurred while committing if this
       server was configured as a synchronous standby.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">flush_lag</code> <code class="type">interval</code>
</p>
<p>
       Time elapsed between flushing recent WAL locally and receiving
       notification that this standby server has written and flushed it
       (but not yet applied it).  This can be used to gauge the delay that
       <code class="literal">synchronous_commit</code> level
       <code class="literal">on</code> incurred while committing if this
       server was configured as a synchronous standby.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">replay_lag</code> <code class="type">interval</code>
</p>
<p>
       Time elapsed between flushing recent WAL locally and receiving
       notification that this standby server has written, flushed and
       applied it.  This can be used to gauge the delay that
       <code class="literal">synchronous_commit</code> level
       <code class="literal">remote_apply</code> incurred while committing if this
       server was configured as a synchronous standby.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sync_priority</code> <code class="type">integer</code>
</p>
<p>
       Priority of this standby server for being chosen as the
       synchronous standby in a priority-based synchronous replication.
       This has no effect in a quorum-based synchronous replication.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sync_state</code> <code class="type">text</code>
</p>
<p>
       Synchronous state of this standby server.
       Possible values are:
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">async</code>: This standby server is asynchronous.
         </p></li><li class="listitem"><p>
<code class="literal">potential</code>: This standby server is now asynchronous,
          but can potentially become synchronous if one of current
          synchronous ones fails.
         </p></li><li class="listitem"><p>
<code class="literal">sync</code>: This standby server is synchronous.
         </p></li><li class="listitem"><p>
<code class="literal">quorum</code>: This standby server is considered as a candidate
          for quorum standbys.
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reply_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Send time of last reply message received from standby server
      </p></td></tr></tbody></table>

<br>

The lag times reported in the `pg_stat_replication`
view are measurements of the time taken for recent WAL to be written,
flushed and replayed and for the sender to know about it. These times
represent the commit delay that was (or would have been) introduced by each
synchronous commit level, if the remote server was configured as a
synchronous standby. For an asynchronous standby, the
`replay_lag` column approximates the delay
before recent transactions became visible to queries. If the standby
server has entirely caught up with the sending server and there is no more
WAL activity, the most recently measured lag times will continue to be
displayed for a short time and then show NULL.

Lag times work automatically for physical replication. Logical decoding
plugins may optionally emit tracking messages; if they do not, the tracking
mechanism will simply display NULL lag.

### Note

The reported lag times are not predictions of how long it will take for
the standby to catch up with the sending server assuming the current
rate of replay. Such a system would show similar times while new WAL is
being generated, but would differ when the sender becomes idle. In
particular, when the standby has caught up completely,
`pg_stat_replication` shows the time taken to
write, flush and replay the most recent reported WAL location rather than
zero as some users might expect. This is consistent with the goal of
measuring synchronous commit and transaction visibility delays for
recent write transactions.
To reduce confusion for users expecting a different model of lag, the
lag columns revert to NULL after a short time on a fully replayed idle
system. Monitoring systems should choose whether to represent this
as missing data, zero or continue to display the last known value.

<a id="MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW"></a>

### 27.2.5. `pg_stat_replication_slots` [#](#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW)

<a id="id-1.6.14.7.9.2"></a>

The `pg_stat_replication_slots` view will contain
one row per logical replication slot, showing statistics about its usage.

<a id="PG-STAT-REPLICATION-SLOTS-VIEW"></a>

**Table 27.15. `pg_stat_replication_slots` View**

<table border="1" class="table" summary="pg_stat_replication_slots View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
        Column Type
       </p>
<p>
        Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slot_name</code> <code class="type">text</code>
</p>
<p>
        A unique, cluster-wide identifier for the replication slot
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spill_txns</code> <code class="type">bigint</code>
</p>
<p>
        Number of transactions spilled to disk once the memory used by
        logical decoding to decode changes from WAL has exceeded
        <code class="literal">logical_decoding_work_mem</code>. The counter gets
        incremented for both top-level transactions and subtransactions.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spill_count</code> <code class="type">bigint</code>
</p>
<p>
        Number of times transactions were spilled to disk while decoding
        changes from WAL for this slot. This counter is incremented each time
        a transaction is spilled, and the same transaction may be spilled
        multiple times.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spill_bytes</code> <code class="type">bigint</code>
</p>
<p>
        Amount of decoded transaction data spilled to disk while performing
        decoding of changes from WAL for this slot. This and other spill
        counters can be used to gauge the I/O which occurred during logical
        decoding and allow tuning <code class="literal">logical_decoding_work_mem</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stream_txns</code> <code class="type">bigint</code>
</p>
<p>
        Number of in-progress transactions streamed to the decoding output
        plugin after the memory used by logical decoding to decode changes
        from WAL for this slot has exceeded
        <code class="literal">logical_decoding_work_mem</code>. Streaming only
        works with top-level transactions (subtransactions can't be streamed
        independently), so the counter is not incremented for subtransactions.
       </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stream_count</code><code class="type">bigint</code>
</p>
<p>
        Number of times in-progress transactions were streamed to the decoding
        output plugin while decoding changes from WAL for this slot. This
        counter is incremented each time a transaction is streamed, and the
        same transaction may be streamed multiple times.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stream_bytes</code><code class="type">bigint</code>
</p>
<p>
        Amount of transaction data decoded for streaming in-progress
        transactions to the decoding output plugin while decoding changes from
        WAL for this slot. This and other streaming counters for this slot can
        be used to tune <code class="literal">logical_decoding_work_mem</code>.
       </p>
</td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_txns</code> <code class="type">bigint</code>
</p>
<p>
        Number of decoded transactions sent to the decoding output plugin for
        this slot. This counts top-level transactions only, and is not incremented
        for subtransactions. Note that this includes the transactions that are
        streamed and/or spilled.
       </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_bytes</code><code class="type">bigint</code>
</p>
<p>
        Amount of transaction data decoded for sending transactions to the
        decoding output plugin while decoding changes from WAL for this slot.
        Note that this includes data that is streamed and/or spilled.
       </p>
</td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
        Time at which these statistics were last reset
       </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-WAL-RECEIVER-VIEW"></a>

### 27.2.6. `pg_stat_wal_receiver` [#](#MONITORING-PG-STAT-WAL-RECEIVER-VIEW)

<a id="id-1.6.14.7.10.2"></a>

The `pg_stat_wal_receiver` view will contain only
one row, showing statistics about the WAL receiver from that receiver's
connected server.

<a id="PG-STAT-WAL-RECEIVER-VIEW"></a>

**Table 27.16. `pg_stat_wal_receiver` View**

<table border="1" class="table" summary="pg_stat_wal_receiver View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of the WAL receiver process
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">status</code> <code class="type">text</code>
</p>
<p>
       Activity status of the WAL receiver process
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">receive_start_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       First write-ahead log location used when WAL receiver is
       started
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">receive_start_tli</code> <code class="type">integer</code>
</p>
<p>
       First timeline number used when WAL receiver is started
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">written_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Last write-ahead log location already received and written to disk,
       but not flushed. This should not be used for data integrity checks.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">flushed_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Last write-ahead log location already received and flushed to
       disk, the initial value of this field being the first log location used
       when WAL receiver is started
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">received_tli</code> <code class="type">integer</code>
</p>
<p>
       Timeline number of last write-ahead log location received and
       flushed to disk, the initial value of this field being the timeline
       number of the first log location used when WAL receiver is started
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_msg_send_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Send time of last message received from origin WAL sender
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_msg_receipt_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Receipt time of last message received from origin WAL sender
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">latest_end_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Last write-ahead log location reported to origin WAL sender
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">latest_end_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time of last write-ahead log location reported to origin WAL sender
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slot_name</code> <code class="type">text</code>
</p>
<p>
       Replication slot name used by this WAL receiver
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sender_host</code> <code class="type">text</code>
</p>
<p>
       Host of the <span class="productname">PostgreSQL</span> instance
       this WAL receiver is connected to. This can be a host name,
       an IP address, or a directory path if the connection is via
       Unix socket.  (The path case can be distinguished because it
       will always be an absolute path, beginning with <code class="literal">/</code>.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sender_port</code> <code class="type">integer</code>
</p>
<p>
       Port number of the <span class="productname">PostgreSQL</span> instance
       this WAL receiver is connected to.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conninfo</code> <code class="type">text</code>
</p>
<p>
       Connection string used by this WAL receiver,
       with security-sensitive fields obfuscated.
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-RECOVERY-PREFETCH"></a>

### 27.2.7. `pg_stat_recovery_prefetch` [#](#MONITORING-PG-STAT-RECOVERY-PREFETCH)

<a id="id-1.6.14.7.11.2"></a>

The `pg_stat_recovery_prefetch` view will contain
only one row. The columns `wal_distance`,
`block_distance` and
`io_depth` show current values, and the
other columns show cumulative counters that can be reset
with the `pg_stat_reset_shared` function.

<a id="PG-STAT-RECOVERY-PREFETCH-VIEW"></a>

**Table 27.17. `pg_stat_recovery_prefetch` View**

<table border="1" class="table" summary="pg_stat_recovery_prefetch View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
        Time at which these statistics were last reset
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">prefetch</code> <code class="type">bigint</code>
</p>
<p>
        Number of blocks prefetched because they were not in the buffer pool
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">hit</code> <code class="type">bigint</code>
</p>
<p>
        Number of blocks not prefetched because they were already in the buffer pool
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">skip_init</code> <code class="type">bigint</code>
</p>
<p>
        Number of blocks not prefetched because they would be zero-initialized
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">skip_new</code> <code class="type">bigint</code>
</p>
<p>
        Number of blocks not prefetched because they didn't exist yet
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">skip_fpw</code> <code class="type">bigint</code>
</p>
<p>
        Number of blocks not prefetched because a full page image was included in the WAL
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">skip_rep</code> <code class="type">bigint</code>
</p>
<p>
        Number of blocks not prefetched because they were already recently prefetched
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">wal_distance</code> <code class="type">int</code>
</p>
<p>
        How many bytes ahead the prefetcher is looking
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">block_distance</code> <code class="type">int</code>
</p>
<p>
        How many blocks ahead the prefetcher is looking
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">io_depth</code> <code class="type">int</code>
</p>
<p>
        How many prefetches have been initiated but are not yet known to have completed
       </p>
</td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-SUBSCRIPTION"></a>

### 27.2.8. `pg_stat_subscription` [#](#MONITORING-PG-STAT-SUBSCRIPTION)

<a id="id-1.6.14.7.12.2"></a><a id="PG-STAT-SUBSCRIPTION"></a>

**Table 27.18. `pg_stat_subscription` View**

<table border="1" class="table" summary="pg_stat_subscription View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subid</code> <code class="type">oid</code>
</p>
<p>
       OID of the subscription
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subname</code> <code class="type">name</code>
</p>
<p>
       Name of the subscription
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">worker_type</code> <code class="type">text</code>
</p>
<p>
       Type of the subscription worker process.  Possible types are
       <code class="literal">apply</code>, <code class="literal">parallel apply</code>, and
       <code class="literal">table synchronization</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of the subscription worker process
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">leader_pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of the leader apply worker if this process is a parallel
       apply worker; NULL if this process is a leader apply worker or a table
       synchronization worker
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the relation that the worker is synchronizing; NULL for the
       leader apply worker and parallel apply workers
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">received_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Last write-ahead log location received, the initial value of
       this field being 0; NULL for parallel apply workers
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_msg_send_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Send time of last message received from origin WAL sender; NULL for
       parallel apply workers
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_msg_receipt_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Receipt time of last message received from origin WAL sender; NULL for
       parallel apply workers
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">latest_end_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       Last write-ahead log location reported to origin WAL sender; NULL for
       parallel apply workers
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">latest_end_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time of last write-ahead log location reported to origin WAL
       sender; NULL for parallel apply workers
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-SUBSCRIPTION-STATS"></a>

### 27.2.9. `pg_stat_subscription_stats` [#](#MONITORING-PG-STAT-SUBSCRIPTION-STATS)

<a id="id-1.6.14.7.13.2"></a>

The `pg_stat_subscription_stats` view will contain
one row per subscription.

<a id="PG-STAT-SUBSCRIPTION-STATS"></a>

**Table 27.19. `pg_stat_subscription_stats` View**

<table border="1" class="table" summary="pg_stat_subscription_stats View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subid</code> <code class="type">oid</code>
</p>
<p>
       OID of the subscription
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subname</code> <code class="type">name</code>
</p>
<p>
       Name of the subscription
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">apply_error_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of times an error occurred while applying changes. Note that any
       conflict resulting in an apply error will be counted in both
       <code class="literal">apply_error_count</code> and the corresponding conflict
       count (e.g., <code class="literal">confl_*</code>).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sync_error_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of times an error occurred during the initial table
       synchronization
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_insert_exists</code> <code class="type">bigint</code>
</p>
<p>
       Number of times a row insertion violated a
       <code class="literal">NOT DEFERRABLE</code> unique constraint during the
       application of changes. See <a class="xref" href="../logical-replication/logical-replication-conflicts.md#CONFLICT-INSERT-EXISTS">insert_exists</a>
       for details about this conflict.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_update_origin_differs</code> <code class="type">bigint</code>
</p>
<p>
       Number of times an update was applied to a row that had been previously
       modified by another source during the application of changes. See
       <a class="xref" href="../logical-replication/logical-replication-conflicts.md#CONFLICT-UPDATE-ORIGIN-DIFFERS">update_origin_differs</a> for details about this
       conflict.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_update_exists</code> <code class="type">bigint</code>
</p>
<p>
       Number of times that an updated row value violated a
       <code class="literal">NOT DEFERRABLE</code> unique constraint during the
       application of changes. See <a class="xref" href="../logical-replication/logical-replication-conflicts.md#CONFLICT-UPDATE-EXISTS">update_exists</a>
       for details about this conflict.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_update_missing</code> <code class="type">bigint</code>
</p>
<p>
       Number of times the tuple to be updated was not found during the
       application of changes. See <a class="xref" href="../logical-replication/logical-replication-conflicts.md#CONFLICT-UPDATE-MISSING">update_missing</a>
       for details about this conflict.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_delete_origin_differs</code> <code class="type">bigint</code>
</p>
<p>
       Number of times a delete operation was applied to row that had been
       previously modified by another source during the application of changes.
       See <a class="xref" href="../logical-replication/logical-replication-conflicts.md#CONFLICT-DELETE-ORIGIN-DIFFERS">delete_origin_differs</a> for details about
       this conflict.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_delete_missing</code> <code class="type">bigint</code>
</p>
<p>
       Number of times the tuple to be deleted was not found during the application
       of changes. See <a class="xref" href="../logical-replication/logical-replication-conflicts.md#CONFLICT-DELETE-MISSING">delete_missing</a> for details
       about this conflict.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_multiple_unique_conflicts</code> <code class="type">bigint</code>
</p>
<p>
       Number of times a row insertion or an updated row values violated multiple
       <code class="literal">NOT DEFERRABLE</code> unique constraints during the
       application of changes. See <a class="xref" href="../logical-replication/logical-replication-conflicts.md#CONFLICT-MULTIPLE-UNIQUE-CONFLICTS">multiple_unique_conflicts</a>
       for details about this conflict.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which these statistics were last reset
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-SSL-VIEW"></a>

### 27.2.10. `pg_stat_ssl` [#](#MONITORING-PG-STAT-SSL-VIEW)

<a id="id-1.6.14.7.14.2"></a>

The `pg_stat_ssl` view will contain one row per
backend or WAL sender process, showing statistics about SSL usage on
this connection. It can be joined to `pg_stat_activity`
or `pg_stat_replication` on the
`pid` column to get more details about the
connection.

<a id="PG-STAT-SSL-VIEW"></a>

**Table 27.20. `pg_stat_ssl` View**

<table border="1" class="table" summary="pg_stat_ssl View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of a backend or WAL sender process
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ssl</code> <code class="type">boolean</code>
</p>
<p>
       True if SSL is used on this connection
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">version</code> <code class="type">text</code>
</p>
<p>
       Version of SSL in use, or NULL if SSL is not in use
       on this connection
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cipher</code> <code class="type">text</code>
</p>
<p>
       Name of SSL cipher in use, or NULL if SSL is not in use
       on this connection
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bits</code> <code class="type">integer</code>
</p>
<p>
       Number of bits in the encryption algorithm used, or NULL
       if SSL is not used on this connection
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_dn</code> <code class="type">text</code>
</p>
<p>
       Distinguished Name (DN) field from the client certificate
       used, or NULL if no client certificate was supplied or if SSL
       is not in use on this connection. This field is truncated if the
       DN field is longer than <code class="symbol">NAMEDATALEN</code> (64 characters
       in a standard build).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_serial</code> <code class="type">numeric</code>
</p>
<p>
       Serial number of the client certificate, or NULL if no client
       certificate was supplied or if SSL is not in use on this connection.  The
       combination of certificate serial number and certificate issuer uniquely
       identifies a certificate (unless the issuer erroneously reuses serial
       numbers).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">issuer_dn</code> <code class="type">text</code>
</p>
<p>
       DN of the issuer of the client certificate, or NULL if no client
       certificate was supplied or if SSL is not in use on this connection.
       This field is truncated like <code class="structfield">client_dn</code>.
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-GSSAPI-VIEW"></a>

### 27.2.11. `pg_stat_gssapi` [#](#MONITORING-PG-STAT-GSSAPI-VIEW)

<a id="id-1.6.14.7.15.2"></a>

The `pg_stat_gssapi` view will contain one row per
backend, showing information about GSSAPI usage on this connection. It can
be joined to `pg_stat_activity` or
`pg_stat_replication` on the
`pid` column to get more details about the
connection.

<a id="PG-STAT-GSSAPI-VIEW"></a>

**Table 27.21. `pg_stat_gssapi` View**

<table border="1" class="table" summary="pg_stat_gssapi View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       Process ID of a backend
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">gss_authenticated</code> <code class="type">boolean</code>
</p>
<p>
       True if GSSAPI authentication was used for this connection
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">principal</code> <code class="type">text</code>
</p>
<p>
       Principal used to authenticate this connection, or NULL
       if GSSAPI was not used to authenticate this connection.  This
       field is truncated if the principal is longer than
       <code class="symbol">NAMEDATALEN</code> (64 characters in a standard build).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">encrypted</code> <code class="type">boolean</code>
</p>
<p>
       True if GSSAPI encryption is in use on this connection
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">credentials_delegated</code> <code class="type">boolean</code>
</p>
<p>
       True if GSSAPI credentials were delegated on this connection.
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-ARCHIVER-VIEW"></a>

### 27.2.12. `pg_stat_archiver` [#](#MONITORING-PG-STAT-ARCHIVER-VIEW)

<a id="id-1.6.14.7.16.2"></a>

The `pg_stat_archiver` view will always have a
single row, containing data about the archiver process of the cluster.

<a id="PG-STAT-ARCHIVER-VIEW"></a>

**Table 27.22. `pg_stat_archiver` View**

<table border="1" class="table" summary="pg_stat_archiver View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">archived_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of WAL files that have been successfully archived
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_archived_wal</code> <code class="type">text</code>
</p>
<p>
       Name of the WAL file most recently successfully archived
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_archived_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time of the most recent successful archive operation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">failed_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of failed attempts for archiving WAL files
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_failed_wal</code> <code class="type">text</code>
</p>
<p>
       Name of the WAL file of the most recent failed archival operation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_failed_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time of the most recent failed archival operation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which these statistics were last reset
      </p></td></tr></tbody></table>

<br>

Normally, WAL files are archived in order, oldest to newest, but that is
not guaranteed, and does not hold under special circumstances like when
promoting a standby or after crash recovery. Therefore it is not safe to
assume that all files older than
`last_archived_wal` have also been successfully
archived.

<a id="MONITORING-PG-STAT-IO-VIEW"></a>

### 27.2.13. `pg_stat_io` [#](#MONITORING-PG-STAT-IO-VIEW)

<a id="id-1.6.14.7.17.2"></a>

The `pg_stat_io` view will contain one row for each
combination of backend type, target I/O object, and I/O context, showing
cluster-wide I/O statistics. Combinations which do not make sense are
omitted.

Currently, I/O on relations (e.g. tables, indexes) and WAL activity are
tracked. However, relation I/O which bypasses shared buffers
(e.g. when moving a table from one tablespace to another) is currently
not tracked.

<a id="PG-STAT-IO-VIEW"></a>

**Table 27.23. `pg_stat_io` View**

<table border="1" class="table" summary="pg_stat_io View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry">
<p class="column_definition">
        Column Type
       </p>
<p>
        Description
       </p>
</th></tr></thead><tbody><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">backend_type</code> <code class="type">text</code>
</p>
<p>
        Type of backend (e.g. background worker, autovacuum worker). See <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW">
<code class="structname">pg_stat_activity</code></a> for more information
        on <code class="varname">backend_type</code>s. Some
        <code class="varname">backend_type</code>s do not accumulate I/O operation
        statistics and will not be included in the view.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">object</code> <code class="type">text</code>
</p>
<p>
        Target object of an I/O operation. Possible values are:
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">relation</code>: Permanent relations.
         </p></li><li class="listitem"><p>
<code class="literal">temp relation</code>: Temporary relations.
         </p></li><li class="listitem"><p>
<code class="literal">wal</code>: Write Ahead Logs.
         </p></li></ul></div><p>
</p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">context</code> <code class="type">text</code>
</p>
<p>
        The context of an I/O operation. Possible values are:
       </p>
<div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">normal</code>: The default or standard
          <code class="varname">context</code> for a type of I/O operation. For
          example, by default, relation data is read into and written out from
          shared buffers. Thus, reads and writes of relation data to and from
          shared buffers are tracked in <code class="varname">context</code>
<code class="literal">normal</code>.
         </p></li><li class="listitem"><p>
<code class="literal">init</code>: I/O operations performed while creating the
          WAL segments are tracked in <code class="varname">context</code>
<code class="literal">init</code>.
         </p></li><li class="listitem"><p>
<code class="literal">vacuum</code>: I/O operations performed outside of shared
          buffers while vacuuming and analyzing permanent relations. Temporary
          table vacuums use the same local buffer pool as other temporary table
          I/O operations and are tracked in <code class="varname">context</code>
<code class="literal">normal</code>.
         </p></li><li class="listitem"><p>
<code class="literal">bulkread</code>: Certain large read I/O operations
          done outside of shared buffers, for example, a sequential scan of a
          large table.
         </p></li><li class="listitem"><p>
<code class="literal">bulkwrite</code>: Certain large write I/O operations
          done outside of shared buffers, such as <code class="command">COPY</code>.
         </p></li></ul></div>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">reads</code> <code class="type">bigint</code>
</p>
<p>
        Number of read operations.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">read_bytes</code> <code class="type">numeric</code>
</p>
<p>
        The total size of read operations in bytes.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">read_time</code> <code class="type">double precision</code>
</p>
<p>
        Time spent waiting for read operations in milliseconds (if
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled and
        <code class="varname">object</code> is not <code class="literal">wal</code>,
        or if <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">track_wal_io_timing</a> is enabled
        and <code class="varname">object</code> is <code class="literal">wal</code>,
        otherwise zero)
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">writes</code> <code class="type">bigint</code>
</p>
<p>
        Number of write operations.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">write_bytes</code> <code class="type">numeric</code>
</p>
<p>
        The total size of write operations in bytes.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">write_time</code> <code class="type">double precision</code>
</p>
<p>
        Time spent waiting for write operations in milliseconds (if
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled and
        <code class="varname">object</code> is not <code class="literal">wal</code>,
        or if <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">track_wal_io_timing</a> is enabled
        and <code class="varname">object</code> is <code class="literal">wal</code>,
        otherwise zero)
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">writebacks</code> <code class="type">bigint</code>
</p>
<p>
        Number of units of size <code class="symbol">BLCKSZ</code> (typically 8kB) which
        the process requested the kernel write out to permanent storage.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">writeback_time</code> <code class="type">double precision</code>
</p>
<p>
        Time spent waiting for writeback operations in milliseconds (if
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled, otherwise zero). This
        includes the time spent queueing write-out requests and, potentially,
        the time spent to write out the dirty data.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">extends</code> <code class="type">bigint</code>
</p>
<p>
        Number of relation extend operations.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">extend_bytes</code> <code class="type">numeric</code>
</p>
<p>
        The total size of relation extend operations in bytes.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">extend_time</code> <code class="type">double precision</code>
</p>
<p>
        Time spent waiting for extend operations in milliseconds. (if
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled and
        <code class="varname">object</code> is not <code class="literal">wal</code>,
        or if <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">track_wal_io_timing</a> is enabled
        and <code class="varname">object</code> is <code class="literal">wal</code>,
        otherwise zero)
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">hits</code> <code class="type">bigint</code>
</p>
<p>
        The number of times a desired block was found in a shared buffer.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">evictions</code> <code class="type">bigint</code>
</p>
<p>
        Number of times a block has been written out from a shared or local
        buffer in order to make it available for another use.
       </p>
<p>
        In <code class="varname">context</code> <code class="literal">normal</code>, this counts
        the number of times a block was evicted from a buffer and replaced with
        another block. In <code class="varname">context</code>s
        <code class="literal">bulkwrite</code>, <code class="literal">bulkread</code>, and
        <code class="literal">vacuum</code>, this counts the number of times a block was
        evicted from shared buffers in order to add the shared buffer to a
        separate, size-limited ring buffer for use in a bulk I/O operation.
        </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">reuses</code> <code class="type">bigint</code>
</p>
<p>
        The number of times an existing buffer in a size-limited ring buffer
        outside of shared buffers was reused as part of an I/O operation in the
        <code class="literal">bulkread</code>, <code class="literal">bulkwrite</code>, or
        <code class="literal">vacuum</code> <code class="varname">context</code>s.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">fsyncs</code> <code class="type">bigint</code>
</p>
<p>
        Number of <code class="literal">fsync</code> calls. These are only tracked in
        <code class="varname">context</code> <code class="literal">normal</code>.
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">fsync_time</code> <code class="type">double precision</code>
</p>
<p>
        Time spent waiting for fsync operations in milliseconds (if
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled and
        <code class="varname">object</code> is not <code class="literal">wal</code>,
        or if <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">track_wal_io_timing</a> is enabled
        and <code class="varname">object</code> is <code class="literal">wal</code>,
        otherwise zero)
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
        Time at which these statistics were last reset.
       </p>
</td></tr></tbody></table>

<br>

Some backend types never perform I/O operations on some I/O objects and/or
in some I/O contexts. These rows are omitted from the view. For example, the
checkpointer does not checkpoint temporary tables, so there will be no rows
for `backend_type` `checkpointer` and
`object` `temp relation`.

In addition, some I/O operations will never be performed either by certain
backend types or on certain I/O objects and/or in certain I/O contexts.
These cells will be NULL. For example, temporary tables are not
`fsync`ed, so `fsyncs` will be NULL for
`object` `temp relation`. Also, the
background writer does not perform reads, so `reads` will
be NULL in rows for `backend_type` `background
writer`.

For the `object` `wal`,
`fsyncs` and `fsync_time` track the
fsync activity of WAL files done in `issue_xlog_fsync`.
`writes` and `write_time`
track the write activity of WAL files done in
`XLogWrite`.
See [Section 28.5](../wal/wal-configuration.md) for more information.

`pg_stat_io` can be used to inform database tuning.
For example:

* A high `evictions` count can indicate that shared
  buffers should be increased.
* Client backends rely on the checkpointer to ensure data is persisted to
  permanent storage. Large numbers of `fsyncs` by
  `client backend`s could indicate a misconfiguration of
  shared buffers or of the checkpointer. More information on configuring
  the checkpointer can be found in [Section 28.5](../wal/wal-configuration.md).
* Normally, client backends should be able to rely on auxiliary processes
  like the checkpointer and the background writer to write out dirty data
  as much as possible. Large numbers of writes by client backends could
  indicate a misconfiguration of shared buffers or of the checkpointer.
  More information on configuring the checkpointer can be found in [Section 28.5](../wal/wal-configuration.md).

### Note

Columns tracking I/O wait time will only be non-zero when
[track_io_timing](../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING) is enabled. The user should be
careful when referencing these columns in combination with their
corresponding I/O operations in case `track_io_timing`
was not enabled for the entire time since the last stats reset.

<a id="MONITORING-PG-STAT-BGWRITER-VIEW"></a>

### 27.2.14. `pg_stat_bgwriter` [#](#MONITORING-PG-STAT-BGWRITER-VIEW)

<a id="id-1.6.14.7.18.2"></a>

The `pg_stat_bgwriter` view will always have a
single row, containing data about the background writer of the cluster.

<a id="PG-STAT-BGWRITER-VIEW"></a>

**Table 27.24. `pg_stat_bgwriter` View**

<table border="1" class="table" summary="pg_stat_bgwriter View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_clean</code> <code class="type">bigint</code>
</p>
<p>
       Number of buffers written by the background writer
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">maxwritten_clean</code> <code class="type">bigint</code>
</p>
<p>
       Number of times the background writer stopped a cleaning
       scan because it had written too many buffers
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_alloc</code> <code class="type">bigint</code>
</p>
<p>
       Number of buffers allocated
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which these statistics were last reset
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-CHECKPOINTER-VIEW"></a>

### 27.2.15. `pg_stat_checkpointer` [#](#MONITORING-PG-STAT-CHECKPOINTER-VIEW)

<a id="id-1.6.14.7.19.2"></a>

The `pg_stat_checkpointer` view will always have a
single row, containing data about the checkpointer process of the cluster.

<a id="PG-STAT-CHECKPOINTER-VIEW"></a>

**Table 27.25. `pg_stat_checkpointer` View**

<table border="1" class="table" summary="pg_stat_checkpointer View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">num_timed</code> <code class="type">bigint</code>
</p>
<p>
       Number of scheduled checkpoints due to timeout
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">num_requested</code> <code class="type">bigint</code>
</p>
<p>
       Number of requested checkpoints
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">num_done</code> <code class="type">bigint</code>
</p>
<p>
       Number of checkpoints that have been performed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">restartpoints_timed</code> <code class="type">bigint</code>
</p>
<p>
       Number of scheduled restartpoints due to timeout or after a failed attempt to perform it
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">restartpoints_req</code> <code class="type">bigint</code>
</p>
<p>
       Number of requested restartpoints
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">restartpoints_done</code> <code class="type">bigint</code>
</p>
<p>
       Number of restartpoints that have been performed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">write_time</code> <code class="type">double precision</code>
</p>
<p>
       Total amount of time that has been spent in the portion of
       processing checkpoints and restartpoints where files are written to disk,
       in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sync_time</code> <code class="type">double precision</code>
</p>
<p>
       Total amount of time that has been spent in the portion of
       processing checkpoints and restartpoints where files are synchronized to
       disk, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_written</code> <code class="type">bigint</code>
</p>
<p>
       Number of shared buffers written during checkpoints and restartpoints
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slru_written</code> <code class="type">bigint</code>
</p>
<p>
        Number of SLRU buffers written during checkpoints and restartpoints
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which these statistics were last reset
      </p></td></tr></tbody></table>

<br>

Checkpoints may be skipped if the server has been idle since the last one.
`num_timed` and
`num_requested` count both completed and skipped
checkpoints, while `num_done` tracks only
the completed ones. Similarly, restartpoints may be skipped
if the last replayed checkpoint record is already the last restartpoint.
`restartpoints_timed` and
`restartpoints_req` count both completed and
skipped restartpoints, while `restartpoints_done`
tracks only the completed ones.

<a id="MONITORING-PG-STAT-WAL-VIEW"></a>

### 27.2.16. `pg_stat_wal` [#](#MONITORING-PG-STAT-WAL-VIEW)

<a id="id-1.6.14.7.20.2"></a>

The `pg_stat_wal` view will always have a
single row, containing data about WAL activity of the cluster.

<a id="PG-STAT-WAL-VIEW"></a>

**Table 27.26. `pg_stat_wal` View**

<table border="1" class="table" summary="pg_stat_wal View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_records</code> <code class="type">bigint</code>
</p>
<p>
       Total number of WAL records generated
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_fpi</code> <code class="type">bigint</code>
</p>
<p>
       Total number of WAL full page images generated
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_bytes</code> <code class="type">numeric</code>
</p>
<p>
       Total amount of WAL generated in bytes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_buffers_full</code> <code class="type">bigint</code>
</p>
<p>
       Number of times WAL data was written to disk because WAL buffers became full
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which these statistics were last reset
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-DATABASE-VIEW"></a>

### 27.2.17. `pg_stat_database` [#](#MONITORING-PG-STAT-DATABASE-VIEW)

<a id="id-1.6.14.7.21.2"></a>

The `pg_stat_database` view will contain one row
for each database in the cluster, plus one for shared objects, showing
database-wide statistics.

<a id="PG-STAT-DATABASE-VIEW"></a>

**Table 27.27. `pg_stat_database` View**

<table border="1" class="table" summary="pg_stat_database View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       OID of this database, or 0 for objects belonging to a shared
       relation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       Name of this database, or <code class="literal">NULL</code> for shared
       objects.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numbackends</code> <code class="type">integer</code>
</p>
<p>
       Number of backends currently connected to this database, or
       <code class="literal">NULL</code> for shared objects.  This is the only column
       in this view that returns a value reflecting current state; all other
       columns return the accumulated values since the last reset.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">xact_commit</code> <code class="type">bigint</code>
</p>
<p>
       Number of transactions in this database that have been
       committed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">xact_rollback</code> <code class="type">bigint</code>
</p>
<p>
       Number of transactions in this database that have been
       rolled back
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of disk blocks read in this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Number of times disk blocks were found already in the buffer
       cache, so that a read was not necessary (this only includes hits in the
       PostgreSQL buffer cache, not the operating system's file system cache)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_returned</code> <code class="type">bigint</code>
</p>
<p>
       Number of live rows fetched by sequential scans and index entries returned by index scans in this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_fetched</code> <code class="type">bigint</code>
</p>
<p>
       Number of live rows fetched by index scans in this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_inserted</code> <code class="type">bigint</code>
</p>
<p>
       Number of rows inserted by queries in this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_updated</code> <code class="type">bigint</code>
</p>
<p>
       Number of rows updated by queries in this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_deleted</code> <code class="type">bigint</code>
</p>
<p>
       Number of rows deleted by queries in this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conflicts</code> <code class="type">bigint</code>
</p>
<p>
       Number of queries canceled due to conflicts with recovery
       in this database. (Conflicts occur only on standby servers; see
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW">
<code class="structname">pg_stat_database_conflicts</code></a> for details.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_files</code> <code class="type">bigint</code>
</p>
<p>
       Number of temporary files created by queries in this database.
       All temporary files are counted, regardless of why the temporary file
       was created (e.g., sorting or hashing), and regardless of the
       <a class="xref" href="../runtime-config/runtime-config-logging.md#GUC-LOG-TEMP-FILES">log_temp_files</a> setting.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_bytes</code> <code class="type">bigint</code>
</p>
<p>
       Total amount of data written to temporary files by queries in
       this database. All temporary files are counted, regardless of why
       the temporary file was created, and
       regardless of the <a class="xref" href="../runtime-config/runtime-config-logging.md#GUC-LOG-TEMP-FILES">log_temp_files</a> setting.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">deadlocks</code> <code class="type">bigint</code>
</p>
<p>
       Number of deadlocks detected in this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">checksum_failures</code> <code class="type">bigint</code>
</p>
<p>
       Number of data page checksum failures detected in this
       database (or on a shared object), or NULL if data checksums are
       disabled.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">checksum_last_failure</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which the last data page checksum failure was detected in
       this database (or on a shared object), or NULL if data checksums are
       disabled.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       Time spent reading data file blocks by backends in this database,
       in milliseconds (if <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled,
       otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       Time spent writing data file blocks by backends in this database,
       in milliseconds (if <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> is enabled,
       otherwise zero)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">session_time</code> <code class="type">double precision</code>
</p>
<p>
       Time spent by database sessions in this database, in milliseconds
       (note that statistics are only updated when the state of a session
       changes, so if sessions have been idle for a long time, this idle time
       won't be included)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">active_time</code> <code class="type">double precision</code>
</p>
<p>
       Time spent executing SQL statements in this database, in milliseconds
       (this corresponds to the states <code class="literal">active</code> and
       <code class="literal">fastpath function call</code> in
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW">
<code class="structname">pg_stat_activity</code></a>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idle_in_transaction_time</code> <code class="type">double precision</code>
</p>
<p>
       Time spent idling while in a transaction in this database, in milliseconds
       (this corresponds to the states <code class="literal">idle in transaction</code> and
       <code class="literal">idle in transaction (aborted)</code> in
       <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW">
<code class="structname">pg_stat_activity</code></a>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sessions</code> <code class="type">bigint</code>
</p>
<p>
       Total number of sessions established to this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sessions_abandoned</code> <code class="type">bigint</code>
</p>
<p>
       Number of database sessions to this database that were terminated
       because connection to the client was lost
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sessions_fatal</code> <code class="type">bigint</code>
</p>
<p>
       Number of database sessions to this database that were terminated
       by fatal errors
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sessions_killed</code> <code class="type">bigint</code>
</p>
<p>
       Number of database sessions to this database that were terminated
       by operator intervention
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parallel_workers_to_launch</code> <code class="type">bigint</code>
</p>
<p>
       Number of parallel workers planned to be launched by queries on this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parallel_workers_launched</code> <code class="type">bigint</code>
</p>
<p>
       Number of parallel workers launched by queries on this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which these statistics were last reset
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW"></a>

### 27.2.18. `pg_stat_database_conflicts` [#](#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW)

<a id="id-1.6.14.7.22.2"></a>

The `pg_stat_database_conflicts` view will contain
one row per database, showing database-wide statistics about
query cancels occurring due to conflicts with recovery on standby servers.
This view will only contain information on standby servers, since
conflicts do not occur on primary servers.

<a id="PG-STAT-DATABASE-CONFLICTS-VIEW"></a>

**Table 27.28. `pg_stat_database_conflicts` View**

<table border="1" class="table" summary="pg_stat_database_conflicts View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       OID of a database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       Name of this database
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_tablespace</code> <code class="type">bigint</code>
</p>
<p>
       Number of queries in this database that have been canceled due to
       dropped tablespaces
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_lock</code> <code class="type">bigint</code>
</p>
<p>
       Number of queries in this database that have been canceled due to
       lock timeouts
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_snapshot</code> <code class="type">bigint</code>
</p>
<p>
       Number of queries in this database that have been canceled due to
       old snapshots
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_bufferpin</code> <code class="type">bigint</code>
</p>
<p>
       Number of queries in this database that have been canceled due to
       pinned buffers
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_deadlock</code> <code class="type">bigint</code>
</p>
<p>
       Number of queries in this database that have been canceled due to
       deadlocks
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_active_logicalslot</code> <code class="type">bigint</code>
</p>
<p>
       Number of uses of logical slots in this database that have been
       canceled due to old snapshots or too low a <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL">wal_level</a>
       on the primary
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-ALL-TABLES-VIEW"></a>

### 27.2.19. `pg_stat_all_tables` [#](#MONITORING-PG-STAT-ALL-TABLES-VIEW)

<a id="id-1.6.14.7.23.2"></a>

The `pg_stat_all_tables` view will contain
one row for each table in the current database (including TOAST
tables), showing statistics about accesses to that specific table. The
`pg_stat_user_tables` and
`pg_stat_sys_tables` views
contain the same information,
but filtered to only show user and system tables respectively.

<a id="PG-STAT-ALL-TABLES-VIEW"></a>

**Table 27.29. `pg_stat_all_tables` View**

<table border="1" class="table" summary="pg_stat_all_tables View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of a table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       Name of the schema that this table is in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       Name of this table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seq_scan</code> <code class="type">bigint</code>
</p>
<p>
       Number of sequential scans initiated on this table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_seq_scan</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       The time of the last sequential scan on this table, based on the
       most recent transaction stop time
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seq_tup_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of live rows fetched by sequential scans
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_scan</code> <code class="type">bigint</code>
</p>
<p>
       Number of index scans initiated on this table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_idx_scan</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       The time of the last index scan on this table, based on the
       most recent transaction stop time
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_tup_fetch</code> <code class="type">bigint</code>
</p>
<p>
       Number of live rows fetched by index scans
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_ins</code> <code class="type">bigint</code>
</p>
<p>
       Total number of rows inserted
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_upd</code> <code class="type">bigint</code>
</p>
<p>
       Total number of rows updated.  (This includes row updates
       counted in <code class="structfield">n_tup_hot_upd</code> and
       <code class="structfield">n_tup_newpage_upd</code>, and remaining
       non-<acronym class="acronym">HOT</acronym> updates.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_del</code> <code class="type">bigint</code>
</p>
<p>
       Total number of rows deleted
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_hot_upd</code> <code class="type">bigint</code>
</p>
<p>
       Number of rows <a class="link" href="../../internals/storage/storage-hot.md">HOT updated</a>.
       These are updates where no successor versions are required in
       indexes.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_newpage_upd</code> <code class="type">bigint</code>
</p>
<p>
       Number of rows updated where the successor version goes onto a
       <span class="emphasis"><em>new</em></span> heap page, leaving behind an original
       version with a
       <a class="link" href="../../internals/storage/storage-page-layout.md#STORAGE-TUPLE-LAYOUT"><code class="structfield">t_ctid</code>
        field</a> that points to a different heap page.  These are
       always non-<acronym class="acronym">HOT</acronym> updates.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_live_tup</code> <code class="type">bigint</code>
</p>
<p>
       Estimated number of live rows
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_dead_tup</code> <code class="type">bigint</code>
</p>
<p>
       Estimated number of dead rows
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_mod_since_analyze</code> <code class="type">bigint</code>
</p>
<p>
       Estimated number of rows modified since this table was last analyzed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_ins_since_vacuum</code> <code class="type">bigint</code>
</p>
<p>
       Estimated number of rows inserted since this table was last vacuumed
       (not counting <code class="command">VACUUM FULL</code>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_vacuum</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Last time at which this table was manually vacuumed
       (not counting <code class="command">VACUUM FULL</code>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_autovacuum</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Last time at which this table was vacuumed by the autovacuum
       daemon
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_analyze</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Last time at which this table was manually analyzed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_autoanalyze</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Last time at which this table was analyzed by the autovacuum
       daemon
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">vacuum_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of times this table has been manually vacuumed
       (not counting <code class="command">VACUUM FULL</code>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">autovacuum_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of times this table has been vacuumed by the autovacuum
       daemon
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">analyze_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of times this table has been manually analyzed
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">autoanalyze_count</code> <code class="type">bigint</code>
</p>
<p>
       Number of times this table has been analyzed by the autovacuum
       daemon
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_vacuum_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time this table has been manually vacuumed, in milliseconds
       (not counting <code class="command">VACUUM FULL</code>).
       (This includes the time spent sleeping due to cost-based delays.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_autovacuum_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time this table has been vacuumed by the autovacuum daemon,
       in milliseconds. (This includes the time spent sleeping due to
       cost-based delays.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_analyze_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time this table has been manually analyzed, in milliseconds.
       (This includes the time spent sleeping due to cost-based delays.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_autoanalyze_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time this table has been analyzed by the autovacuum daemon,
       in milliseconds. (This includes the time spent sleeping due to
       cost-based delays.)
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-ALL-INDEXES-VIEW"></a>

### 27.2.20. `pg_stat_all_indexes` [#](#MONITORING-PG-STAT-ALL-INDEXES-VIEW)

<a id="id-1.6.14.7.24.2"></a>

The `pg_stat_all_indexes` view will contain
one row for each index in the current database,
showing statistics about accesses to that specific index. The
`pg_stat_user_indexes` and
`pg_stat_sys_indexes` views
contain the same information,
but filtered to only show user and system indexes respectively.

<a id="PG-STAT-ALL-INDEXES-VIEW"></a>

**Table 27.30. `pg_stat_all_indexes` View**

<table border="1" class="table" summary="pg_stat_all_indexes View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the table for this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelid</code> <code class="type">oid</code>
</p>
<p>
       OID of this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       Name of the schema this index is in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       Name of the table for this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelname</code> <code class="type">name</code>
</p>
<p>
       Name of this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_scan</code> <code class="type">bigint</code>
</p>
<p>
       Number of index scans initiated on this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_idx_scan</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       The time of the last scan on this index, based on the
       most recent transaction stop time
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_tup_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of index entries returned by scans on this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_tup_fetch</code> <code class="type">bigint</code>
</p>
<p>
       Number of live table rows fetched by simple index scans using this
       index
      </p></td></tr></tbody></table>

<br>

Indexes can be used by simple index scans, “bitmap” index scans,
and the optimizer. In a bitmap scan
the output of several indexes can be combined via AND or OR rules,
so it is difficult to associate individual heap row fetches
with specific indexes when a bitmap scan is used. Therefore, a bitmap
scan increments the
`pg_stat_all_indexes`.`idx_tup_read`
count(s) for the index(es) it uses, and it increments the
`pg_stat_all_tables`.`idx_tup_fetch`
count for the table, but it does not affect
`pg_stat_all_indexes`.`idx_tup_fetch`.
The optimizer also accesses indexes to check for supplied constants
whose values are outside the recorded range of the optimizer statistics
because the optimizer statistics might be stale.

### Note

The `idx_tup_read` and `idx_tup_fetch` counts
can be different even without any use of bitmap scans,
because `idx_tup_read` counts
index entries retrieved from the index while `idx_tup_fetch`
counts live rows fetched from the table. The latter will be less if any
dead or not-yet-committed rows are fetched using the index, or if any
heap fetches are avoided by means of an index-only scan.

### Note

Index scans may sometimes perform multiple index searches per execution.
Each index search increments `pg_stat_all_indexes`.`idx_scan`,
so it's possible for the count of index scans to significantly exceed the
total number of index scan executor node executions.

This can happen with queries that use certain SQL
constructs to search for rows matching any value out of a list or array of
multiple scalar values (see [Section 9.25](../../the-sql-language/functions/functions-comparisons.md)). It
can also happen to queries with a
`column_name =
value1 OR
column_name =
value2 ...` construct, though only
when the optimizer transforms the construct into an equivalent
multi-valued array representation. Similarly, when B-tree index scans use
the skip scan optimization, an index search is performed each time the
scan is repositioned to the next index leaf page that might have matching
tuples (see [Section 11.3](../../the-sql-language/indexes/indexes-multicolumn.md)).

### Tip

`EXPLAIN ANALYZE` outputs the total number of index
searches performed by each index scan node. See
[Section 14.1.2](../../the-sql-language/performance-tips/using-explain.md#USING-EXPLAIN-ANALYZE) for an example demonstrating how
this works.

<a id="MONITORING-PG-STATIO-ALL-TABLES-VIEW"></a>

### 27.2.21. `pg_statio_all_tables` [#](#MONITORING-PG-STATIO-ALL-TABLES-VIEW)

<a id="id-1.6.14.7.25.2"></a>

The `pg_statio_all_tables` view will contain
one row for each table in the current database (including TOAST
tables), showing statistics about I/O on that specific table. The
`pg_statio_user_tables` and
`pg_statio_sys_tables` views
contain the same information,
but filtered to only show user and system tables respectively.

<a id="PG-STATIO-ALL-TABLES-VIEW"></a>

**Table 27.31. `pg_statio_all_tables` View**

<table border="1" class="table" summary="pg_statio_all_tables View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of a table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       Name of the schema that this table is in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       Name of this table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of disk blocks read from this table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Number of buffer hits in this table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of disk blocks read from all indexes on this table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Number of buffer hits in all indexes on this table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">toast_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of disk blocks read from this table's TOAST table (if any)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">toast_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Number of buffer hits in this table's TOAST table (if any)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tidx_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of disk blocks read from this table's TOAST table indexes (if any)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tidx_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Number of buffer hits in this table's TOAST table indexes (if any)
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STATIO-ALL-INDEXES-VIEW"></a>

### 27.2.22. `pg_statio_all_indexes` [#](#MONITORING-PG-STATIO-ALL-INDEXES-VIEW)

<a id="id-1.6.14.7.26.2"></a>

The `pg_statio_all_indexes` view will contain
one row for each index in the current database,
showing statistics about I/O on that specific index. The
`pg_statio_user_indexes` and
`pg_statio_sys_indexes` views
contain the same information,
but filtered to only show user and system indexes respectively.

<a id="PG-STATIO-ALL-INDEXES-VIEW"></a>

**Table 27.32. `pg_statio_all_indexes` View**

<table border="1" class="table" summary="pg_statio_all_indexes View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of the table for this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelid</code> <code class="type">oid</code>
</p>
<p>
       OID of this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       Name of the schema this index is in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       Name of the table for this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelname</code> <code class="type">name</code>
</p>
<p>
       Name of this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of disk blocks read from this index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Number of buffer hits in this index
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW"></a>

### 27.2.23. `pg_statio_all_sequences` [#](#MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW)

<a id="id-1.6.14.7.27.2"></a>

The `pg_statio_all_sequences` view will contain
one row for each sequence in the current database,
showing statistics about I/O on that specific sequence.

<a id="PG-STATIO-ALL-SEQUENCES-VIEW"></a>

**Table 27.33. `pg_statio_all_sequences` View**

<table border="1" class="table" summary="pg_statio_all_sequences View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       OID of a sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       Name of the schema this sequence is in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       Name of this sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of disk blocks read from this sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Number of buffer hits in this sequence
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-USER-FUNCTIONS-VIEW"></a>

### 27.2.24. `pg_stat_user_functions` [#](#MONITORING-PG-STAT-USER-FUNCTIONS-VIEW)

<a id="id-1.6.14.7.28.2"></a>

The `pg_stat_user_functions` view will contain
one row for each tracked function, showing statistics about executions of
that function. The [track_functions](../runtime-config/runtime-config-statistics.md#GUC-TRACK-FUNCTIONS) parameter
controls exactly which functions are tracked.

<a id="PG-STAT-USER-FUNCTIONS-VIEW"></a>

**Table 27.34. `pg_stat_user_functions` View**

<table border="1" class="table" summary="pg_stat_user_functions View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">funcid</code> <code class="type">oid</code>
</p>
<p>
       OID of a function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       Name of the schema this function is in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">funcname</code> <code class="type">name</code>
</p>
<p>
       Name of this function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">calls</code> <code class="type">bigint</code>
</p>
<p>
       Number of times this function has been called
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent in this function and all other functions
       called by it, in milliseconds
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">self_time</code> <code class="type">double precision</code>
</p>
<p>
       Total time spent in this function itself, not including
       other functions called by it, in milliseconds
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-PG-STAT-SLRU-VIEW"></a>

### 27.2.25. `pg_stat_slru` [#](#MONITORING-PG-STAT-SLRU-VIEW)

<a id="id-1.6.14.7.29.2"></a><a id="id-1.6.14.7.29.3"></a>

PostgreSQL accesses certain on-disk information
via `SLRU` (*simple least-recently-used*)
caches.
The `pg_stat_slru` view will contain
one row for each tracked SLRU cache, showing statistics about access
to cached pages.

For each `SLRU` cache that's part of the core server,
there is a configuration parameter that controls its size, with the suffix
`_buffers` appended.

<a id="PG-STAT-SLRU-VIEW"></a>

**Table 27.35. `pg_stat_slru` View**

<table border="1" class="table" summary="pg_stat_slru View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       Name of the SLRU
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_zeroed</code> <code class="type">bigint</code>
</p>
<p>
       Number of blocks zeroed during initializations
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       Number of times disk blocks were found already in the SLRU,
       so that a read was not necessary (this only includes hits in the
       SLRU, not the operating system's file system cache)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_read</code> <code class="type">bigint</code>
</p>
<p>
       Number of disk blocks read for this SLRU
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_written</code> <code class="type">bigint</code>
</p>
<p>
       Number of disk blocks written for this SLRU
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_exists</code> <code class="type">bigint</code>
</p>
<p>
       Number of blocks checked for existence for this SLRU
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">flushes</code> <code class="type">bigint</code>
</p>
<p>
       Number of flushes of dirty data for this SLRU
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">truncates</code> <code class="type">bigint</code>
</p>
<p>
       Number of truncates for this SLRU
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       Time at which these statistics were last reset
      </p></td></tr></tbody></table>

<br>

<a id="MONITORING-STATS-FUNCTIONS"></a>

### 27.2.26. Statistics Functions [#](#MONITORING-STATS-FUNCTIONS)

Other ways of looking at the statistics can be set up by writing
queries that use the same underlying statistics access functions used by
the standard views shown above. For details such as the functions' names,
consult the definitions of the standard views. (For example, in
psql you could issue `\d+ pg_stat_activity`.)
The access functions for per-database statistics take a database OID as an
argument to identify which database to report on.
The per-table and per-index functions take a table or index OID.
The functions for per-function statistics take a function OID.
Note that only tables, indexes, and functions in the current database
can be seen with these functions.

Additional functions related to the cumulative statistics system are listed
in [Table 27.36](monitoring-stats.md#MONITORING-STATS-FUNCS-TABLE).

<a id="MONITORING-STATS-FUNCS-TABLE"></a>

**Table 27.36. Additional Statistics Functions**

<table border="1" class="table" summary="Additional Statistics Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">pg_backend_pid</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the process ID of the server process attached to the current
        session.
       </p></td></tr><tr><td class="func_table_entry" id="PG-STAT-GET-BACKEND-IO"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.2.1.1.1"></a>
<code class="function">pg_stat_get_backend_io</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        Returns I/O statistics about the backend with the specified
        process ID. The output fields are exactly the same as the ones in the
        <code class="structname">pg_stat_io</code> view.
       </p>
<p>
        The function does not return I/O statistics for the checkpointer,
        the background writer, the startup process and the autovacuum launcher
        as they are already visible in the <code class="structname">pg_stat_io</code>
        view and there is only one of each.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.3.1.1.1"></a>
<code class="function">pg_stat_get_activity</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        Returns a record of information about the backend with the specified
        process ID, or one record for each active backend in the system
        if <code class="literal">NULL</code> is specified.  The fields returned are a
        subset of those in the <code class="structname">pg_stat_activity</code> view.
       </p></td></tr><tr><td class="func_table_entry" id="PG-STAT-GET-BACKEND-WAL"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.4.1.1.1"></a>
<code class="function">pg_stat_get_backend_wal</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
</p>
<p>
        Returns WAL statistics about the backend with the specified
        process ID. The output fields are exactly the same as the ones in the
        <code class="structname">pg_stat_wal</code> view.
       </p>
<p>
        The function does not return WAL statistics for the checkpointer,
        the background writer, the startup process and the autovacuum launcher.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.5.1.1.1"></a>
<code class="function">pg_stat_get_snapshot_timestamp</code> ()
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        Returns the timestamp of the current statistics snapshot, or NULL if
        no statistics snapshot has been taken. A snapshot is taken the first
        time cumulative statistics are accessed in a transaction if
        <code class="varname">stats_fetch_consistency</code> is set to
        <code class="literal">snapshot</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.6.1.1.1"></a>
<code class="function">pg_stat_get_xact_blocks_fetched</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        Returns the number of block read requests for table or index, in the
        current transaction. This number minus
        <code class="function">pg_stat_get_xact_blocks_hit</code> gives the number of
        kernel <code class="function">read()</code> calls; the number of actual
        physical reads is usually lower due to kernel-level buffering.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.7.1.1.1"></a>
<code class="function">pg_stat_get_xact_blocks_hit</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        Returns the number of block read requests for table or index, in the
        current transaction, found in cache (not triggering kernel
        <code class="function">read()</code> calls).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.8.1.1.1"></a>
<code class="function">pg_stat_clear_snapshot</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        Discards the current statistics snapshot or cached information.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.9.1.1.1"></a>
<code class="function">pg_stat_reset</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        Resets all statistics counters for the current database to zero.
       </p>
<p>
        This function is restricted to superusers by default, but other users
        can be granted EXECUTE to run the function.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.10.1.1.1"></a>
<code class="function">pg_stat_reset_shared</code> ( [ <em class="parameter"><code>target</code></em> <code class="type">text</code> <code class="literal">DEFAULT</code> <code class="literal">NULL</code> ] )
        → <code class="returnvalue">void</code>
</p>
<p>
        Resets some cluster-wide statistics counters to zero, depending on the
        argument. <em class="parameter"><code>target</code></em> can be:
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">archiver</code>: Reset all the counters shown in the
          <code class="structname">pg_stat_archiver</code> view.
         </p></li><li class="listitem"><p>
<code class="literal">bgwriter</code>: Reset all the counters shown in the
           <code class="structname">pg_stat_bgwriter</code> view.
         </p></li><li class="listitem"><p>
<code class="literal">checkpointer</code>: Reset all the counters shown in the
          <code class="structname">pg_stat_checkpointer</code> view.
         </p></li><li class="listitem"><p>
<code class="literal">io</code>: Reset all the counters shown in the
          <code class="structname">pg_stat_io</code> view.
         </p></li><li class="listitem"><p>
<code class="literal">recovery_prefetch</code>: Reset all the counters shown in
          the <code class="structname">pg_stat_recovery_prefetch</code> view.
         </p></li><li class="listitem"><p>
<code class="literal">slru</code>: Reset all the counters shown in the
          <code class="structname">pg_stat_slru</code> view.
         </p></li><li class="listitem"><p>
<code class="literal">wal</code>: Reset all the counters shown in the
          <code class="structname">pg_stat_wal</code> view.
         </p></li><li class="listitem"><p>
<code class="literal">NULL</code> or not specified: All the counters from the
          views listed above are reset.
         </p></li></ul></div><p>
</p>
<p>
        This function is restricted to superusers by default, but other users
        can be granted EXECUTE to run the function.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.11.1.1.1"></a>
<code class="function">pg_stat_reset_single_table_counters</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        Resets statistics for a single table or index in the current database
        or shared across all databases in the cluster to zero.
       </p>
<p>
        This function is restricted to superusers by default, but other users
        can be granted EXECUTE to run the function.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.12.1.1.1"></a>
<code class="function">pg_stat_reset_backend_stats</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        Resets statistics for a single backend with the specified process ID
        to zero.
       </p>
<p>
        This function is restricted to superusers by default, but other users
        can be granted EXECUTE to run the function.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.13.1.1.1"></a>
<code class="function">pg_stat_reset_single_function_counters</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        Resets statistics for a single function in the current database to
        zero.
       </p>
<p>
        This function is restricted to superusers by default, but other users
        can be granted EXECUTE to run the function.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.14.1.1.1"></a>
<code class="function">pg_stat_reset_slru</code> ( [ <em class="parameter"><code>target</code></em> <code class="type">text</code> <code class="literal">DEFAULT</code> <code class="literal">NULL</code> ] )
        → <code class="returnvalue">void</code>
</p>
<p>
        Resets statistics to zero for a single SLRU cache, or for all SLRUs in
        the cluster. If <em class="parameter"><code>target</code></em> is
        <code class="literal">NULL</code> or is not specified, all the counters shown in
        the <code class="structname">pg_stat_slru</code> view for all SLRU caches are
        reset. The argument can be one of
        <code class="literal">commit_timestamp</code>,
        <code class="literal">multixact_member</code>,
        <code class="literal">multixact_offset</code>,
        <code class="literal">notify</code>,
        <code class="literal">serializable</code>,
        <code class="literal">subtransaction</code>, or
        <code class="literal">transaction</code>
        to reset the counters for only that entry.
        If the argument is <code class="literal">other</code> (or indeed, any
        unrecognized name), then the counters for all other SLRU caches, such
        as extension-defined caches, are reset.
       </p>
<p>
        This function is restricted to superusers by default, but other users
        can be granted EXECUTE to run the function.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.15.1.1.1"></a>
<code class="function">pg_stat_reset_replication_slot</code> ( <code class="type">text</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        Resets statistics of the replication slot defined by the argument. If
        the argument is <code class="literal">NULL</code>, resets statistics for all
        the replication slots.
       </p>
<p>
         This function is restricted to superusers by default, but other users
         can be granted EXECUTE to run the function.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.16.1.1.1"></a>
<code class="function">pg_stat_reset_subscription_stats</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        Resets statistics for a single subscription shown in the
        <code class="structname">pg_stat_subscription_stats</code> view to zero. If
        the argument is <code class="literal">NULL</code>, reset statistics for all
        subscriptions.
       </p>
<p>
        This function is restricted to superusers by default, but other users
        can be granted EXECUTE to run the function.
       </p></td></tr></tbody></table>

<br>

### Warning

Using `pg_stat_reset()` also resets counters that
autovacuum uses to determine when to trigger a vacuum or an analyze.
Resetting these counters can cause autovacuum to not perform necessary
work, which can cause problems such as table bloat or out-dated
table statistics. A database-wide `ANALYZE` is
recommended after the statistics have been reset.

`pg_stat_get_activity`, the underlying function of
the `pg_stat_activity` view, returns a set of records
containing all the available information about each backend process.
Sometimes it may be more convenient to obtain just a subset of this
information. In such cases, another set of per-backend statistics
access functions can be used; these are shown in [Table 27.37](monitoring-stats.md#MONITORING-STATS-BACKEND-FUNCS-TABLE).
These access functions use the session's backend ID number, which is a
small integer (>= 0) that is distinct from the backend ID of any
concurrent session, although a session's ID can be recycled as soon as
it exits. The backend ID is used, among other things, to identify the
session's temporary schema if it has one.
The function `pg_stat_get_backend_idset` provides a
convenient way to list all the active backends' ID numbers for
invoking these functions. For example, to show the PIDs and
current queries of all backends:

```

SELECT pg_stat_get_backend_pid(backendid) AS pid,
       pg_stat_get_backend_activity(backendid) AS query
FROM pg_stat_get_backend_idset() AS backendid;
```

<a id="MONITORING-STATS-BACKEND-FUNCS-TABLE"></a>

**Table 27.37. Per-Backend Statistics Functions**

<table border="1" class="table" summary="Per-Backend Statistics Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.1.1.1.1"></a>
<code class="function">pg_stat_get_backend_activity</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the text of this backend's most recent query.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.2.1.1.1"></a>
<code class="function">pg_stat_get_backend_activity_start</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        Returns the time when the backend's most recent query was started.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.3.1.1.1"></a>
<code class="function">pg_stat_get_backend_client_addr</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        Returns the IP address of the client connected to this backend.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.4.1.1.1"></a>
<code class="function">pg_stat_get_backend_client_port</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the TCP port number that the client is using for communication.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.5.1.1.1"></a>
<code class="function">pg_stat_get_backend_dbid</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        Returns the OID of the database this backend is connected to.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.6.1.1.1"></a>
<code class="function">pg_stat_get_backend_idset</code> ()
        → <code class="returnvalue">setof integer</code>
</p>
<p>
        Returns the set of currently active backend ID numbers.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.7.1.1.1"></a>
<code class="function">pg_stat_get_backend_pid</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the process ID of this backend.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.8.1.1.1"></a>
<code class="function">pg_stat_get_backend_start</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        Returns the time when this process was started.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.9.1.1.1"></a>
<code class="function">pg_stat_get_backend_subxact</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
</p>
<p>
        Returns a record of information about the subtransactions of the
        backend with the specified ID.
        The fields returned are <em class="parameter"><code>subxact_count</code></em>, which
        is the number of subtransactions in the backend's subtransaction cache,
        and <em class="parameter"><code>subxact_overflow</code></em>, which indicates whether
        the backend's subtransaction cache is overflowed or not.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.10.1.1.1"></a>
<code class="function">pg_stat_get_backend_userid</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        Returns the OID of the user logged into this backend.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.11.1.1.1"></a>
<code class="function">pg_stat_get_backend_wait_event</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the wait event name if this backend is currently waiting,
        otherwise NULL. See <a class="xref" href="monitoring-stats.md#WAIT-EVENT-ACTIVITY-TABLE">Table 27.5</a> through
        <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TIMEOUT-TABLE">Table 27.13</a>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.12.1.1.1"></a>
<code class="function">pg_stat_get_backend_wait_event_type</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the wait event type name if this backend is currently waiting,
        otherwise NULL.  See <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TABLE">Table 27.4</a> for details.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.13.1.1.1"></a>
<code class="function">pg_stat_get_backend_xact_start</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        Returns the time when the backend's current transaction was started.
       </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（英文原文，待翻譯）
