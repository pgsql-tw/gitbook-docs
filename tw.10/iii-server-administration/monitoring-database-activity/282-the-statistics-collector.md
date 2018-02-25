# 28.2. 統計資訊收集器

[28.2.1. Statistics Collection Configuration](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-SETUP)

[28.2.2. Viewing Statistics](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-VIEWS)

[28.2.3. Statistics Functions](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-FUNCTIONS)

PostgreSQL's\_statistics collector\_is a subsystem that supports collection and reporting of information about server activity. Presently, the collector can count accesses to tables and indexes in both disk-block and individual-row terms. It also tracks the total number of rows in each table, and information about vacuum and analyze actions for each table. It can also count calls to user-defined functions and the total time spent in each one.

PostgreSQLalso supports reporting dynamic information about exactly what is going on in the system right now, such as the exact command currently being executed by other server processes, and which other connections exist in the system. This facility is independent of the collector process.

### 28.2.1. Statistics Collection Configuration

Since collection of statistics adds some overhead to query execution, the system can be configured to collect or not collect information. This is controlled by configuration parameters that are normally set in`postgresql.conf`. \(See[Chapter 19](https://www.postgresql.org/docs/10/static/runtime-config.html)for details about setting configuration parameters.\)

The parameter[track\_activities](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-ACTIVITIES)enables monitoring of the current command being executed by any server process.

The parameter[track\_counts](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-COUNTS)controls whether statistics are collected about table and index accesses.

The parameter[track\_functions](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-FUNCTIONS)enables tracking of usage of user-defined functions.

The parameter[track\_io\_timing](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-IO-TIMING)enables monitoring of block read and write times.

Normally these parameters are set in`postgresql.conf`so that they apply to all server processes, but it is possible to turn them on or off in individual sessions using the[SET](https://www.postgresql.org/docs/10/static/sql-set.html)command. \(To prevent ordinary users from hiding their activity from the administrator, only superusers are allowed to change these parameters with`SET`.\)

The statistics collector transmits the collected information to otherPostgreSQLprocesses through temporary files. These files are stored in the directory named by the[stats\_temp\_directory](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-STATS-TEMP-DIRECTORY)parameter,`pg_stat_tmp`by default. For better performance,`stats_temp_directory`can be pointed at a RAM-based file system, decreasing physical I/O requirements. When the server shuts down cleanly, a permanent copy of the statistics data is stored in the`pg_stat`subdirectory, so that statistics can be retained across server restarts. When recovery is performed at server start \(e.g. after immediate shutdown, server crash, and point-in-time recovery\), all statistics counters are reset.

### 28.2.2. Viewing Statistics

Several predefined views, listed in[Table 28.1](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-DYNAMIC-VIEWS-TABLE), are available to show the current state of the system. There are also several other views, listed in[Table 28.2](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-VIEWS-TABLE), available to show the results of statistics collection. Alternatively, one can build custom views using the underlying statistics functions, as discussed in[Section 28.2.3](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-FUNCTIONS).

When using the statistics to monitor collected data, it is important to realize that the information does not update instantaneously. Each individual server process transmits new statistical counts to the collector just before going idle; so a query or transaction still in progress does not affect the displayed totals. Also, the collector itself emits a new report at most once per`PGSTAT_STAT_INTERVAL`milliseconds \(500 ms unless altered while building the server\). So the displayed information lags behind actual activity. However, current-query information collected by`track_activities`is always up-to-date.

Another important point is that when a server process is asked to display any of these statistics, it first fetches the most recent report emitted by the collector process and then continues to use this snapshot for all statistical views and functions until the end of its current transaction. So the statistics will show static information as long as you continue the current transaction. Similarly, information about the current queries of all sessions is collected when any such information is first requested within a transaction, and the same information will be displayed throughout the transaction. This is a feature, not a bug, because it allows you to perform several queries on the statistics and correlate the results without worrying that the numbers are changing underneath you. But if you want to see new results with each query, be sure to do the queries outside any transaction block. Alternatively, you can invoke`pg_stat_clear_snapshot`\(\), which will discard the current transaction's statistics snapshot \(if any\). The next use of statistical information will cause a new snapshot to be fetched.

A transaction can also see its own statistics \(as yet untransmitted to the collector\) in the views`pg_stat_xact_all_tables`,`pg_stat_xact_sys_tables`,`pg_stat_xact_user_tables`, and`pg_stat_xact_user_functions`. These numbers do not act as stated above; instead they update continuously throughout the transaction.

**Table 28.1. Dynamic Statistics Views**

| View Name | Description |
| :--- | :--- |
| `pg_stat_activity` | One row per server process, showing information related to the current activity of that process, such as state and current query. See[pg\_stat\_activity](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-ACTIVITY-VIEW)for details. |
| `pg_stat_replication` | One row per WAL sender process, showing statistics about replication to that sender's connected standby server. See[pg\_stat\_replication](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-REPLICATION-VIEW)for details. |
| `pg_stat_wal_receiver` | Only one row, showing statistics about the WAL receiver from that receiver's connected server. See[pg\_stat\_wal\_receiver](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-WAL-RECEIVER-VIEW)for details. |
| `pg_stat_subscription` | At least one row per subscription, showing information about the subscription workers. See[pg\_stat\_subscription](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-SUBSCRIPTION)for details. |
| `pg_stat_ssl` | One row per connection \(regular and replication\), showing information about SSL used on this connection. See[pg\_stat\_ssl](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-SSL-VIEW)for details. |
| `pg_stat_progress_vacuum` | One row for each backend \(including autovacuum worker processes\) running`VACUUM`, showing current progress. See[Section 28.4.1](https://www.postgresql.org/docs/10/static/progress-reporting.html#VACUUM-PROGRESS-REPORTING). |

  


**Table 28.2. Collected Statistics Views**

| View Name | Description |
| :--- | :--- |
| `pg_stat_archiver` | One row only, showing statistics about the WAL archiver process's activity. See[pg\_stat\_archiver](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-ARCHIVER-VIEW)for details. |
| `pg_stat_bgwriter` | One row only, showing statistics about the background writer process's activity. See[pg\_stat\_bgwriter](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-BGWRITER-VIEW)for details. |
| `pg_stat_database` | One row per database, showing database-wide statistics. See[pg\_stat\_database](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-DATABASE-VIEW)for details. |
| `pg_stat_database_conflicts` | One row per database, showing database-wide statistics about query cancels due to conflict with recovery on standby servers. See[pg\_stat\_database\_conflicts](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-DATABASE-CONFLICTS-VIEW)for details. |
| `pg_stat_all_tables` | One row for each table in the current database, showing statistics about accesses to that specific table. See[pg\_stat\_all\_tables](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-ALL-TABLES-VIEW)for details. |
| `pg_stat_sys_tables` | Same as`pg_stat_all_tables`, except that only system tables are shown. |
| `pg_stat_user_tables` | Same as`pg_stat_all_tables`, except that only user tables are shown. |
| `pg_stat_xact_all_tables` | Similar to`pg_stat_all_tables`, but counts actions taken so far within the current transaction \(which are_not_yet included in`pg_stat_all_tables`and related views\). The columns for numbers of live and dead rows and vacuum and analyze actions are not present in this view. |
| `pg_stat_xact_sys_tables` | Same as`pg_stat_xact_all_tables`, except that only system tables are shown. |
| `pg_stat_xact_user_tables` | Same as`pg_stat_xact_all_tables`, except that only user tables are shown. |
| `pg_stat_all_indexes` | One row for each index in the current database, showing statistics about accesses to that specific index. See[pg\_stat\_all\_indexes](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-ALL-INDEXES-VIEW)for details. |
| `pg_stat_sys_indexes` | Same as`pg_stat_all_indexes`, except that only indexes on system tables are shown. |
| `pg_stat_user_indexes` | Same as`pg_stat_all_indexes`, except that only indexes on user tables are shown. |
| `pg_statio_all_tables` | One row for each table in the current database, showing statistics about I/O on that specific table. See[pg\_statio\_all\_tables](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STATIO-ALL-TABLES-VIEW)for details. |
| `pg_statio_sys_tables` | Same as`pg_statio_all_tables`, except that only system tables are shown. |
| `pg_statio_user_tables` | Same as`pg_statio_all_tables`, except that only user tables are shown. |
| `pg_statio_all_indexes` | One row for each index in the current database, showing statistics about I/O on that specific index. See[pg\_statio\_all\_indexes](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STATIO-ALL-INDEXES-VIEW)for details. |
| `pg_statio_sys_indexes` | Same as`pg_statio_all_indexes`, except that only indexes on system tables are shown. |
| `pg_statio_user_indexes` | Same as`pg_statio_all_indexes`, except that only indexes on user tables are shown. |
| `pg_statio_all_sequences` | One row for each sequence in the current database, showing statistics about I/O on that specific sequence. See[pg\_statio\_all\_sequences](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STATIO-ALL-SEQUENCES-VIEW)for details. |
| `pg_statio_sys_sequences` | Same as`pg_statio_all_sequences`, except that only system sequences are shown. \(Presently, no system sequences are defined, so this view is always empty.\) |
| `pg_statio_user_sequences` | Same as`pg_statio_all_sequences`, except that only user sequences are shown. |
| `pg_stat_user_functions` | One row for each tracked function, showing statistics about executions of that function. See[pg\_stat\_user\_functions](https://www.postgresql.org/docs/10/static/monitoring-stats.html#PG-STAT-USER-FUNCTIONS-VIEW)for details. |
| `pg_stat_xact_user_functions` | Similar to`pg_stat_user_functions`, but counts only calls during the current transaction \(which are_not_yet included in`pg_stat_user_functions`\). |

  


The per-index statistics are particularly useful to determine which indexes are being used and how effective they are.

The`pg_statio_`views are primarily useful to determine the effectiveness of the buffer cache. When the number of actual disk reads is much smaller than the number of buffer hits, then the cache is satisfying most read requests without invoking a kernel call. However, these statistics do not give the entire story: due to the way in whichPostgreSQLhandles disk I/O, data that is not in thePostgreSQLbuffer cache might still reside in the kernel's I/O cache, and might therefore still be fetched without requiring a physical read. Users interested in obtaining more detailed information onPostgreSQLI/O behavior are advised to use thePostgreSQLstatistics collector in combination with operating system utilities that allow insight into the kernel's handling of I/O.

**Table 28.3. `pg_stat_activity`View**

| Column | Type | Description |
| :--- | :--- | :--- |
| `datid` | `oid` | OID of the database this backend is connected to |
| `datname` | `name` | Name of the database this backend is connected to |
| `pid` | `integer` | Process ID of this backend |
| `usesysid` | `oid` | OID of the user logged into this backend |
| `usename` | `name` | Name of the user logged into this backend |
| `application_name` | `text` | Name of the application that is connected to this backend |
| `client_addr` | `inet` | IP address of the client connected to this backend. If this field is null, it indicates either that the client is connected via a Unix socket on the server machine or that this is an internal process such as autovacuum. |
| `client_hostname` | `text` | Host name of the connected client, as reported by a reverse DNS lookup of`client_addr`. This field will only be non-null for IP connections, and only when[log\_hostname](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#GUC-LOG-HOSTNAME)is enabled. |
| `client_port` | `integer` | TCP port number that the client is using for communication with this backend, or`-1`if a Unix socket is used |
| `backend_start` | `timestamp with time zone` | Time when this process was started. For client backends, this is the time the client connected to the server. |
| `xact_start` | `timestamp with time zone` | Time when this process' current transaction was started, or null if no transaction is active. If the current query is the first of its transaction, this column is equal to the`query_start`column. |
| `query_start` | `timestamp with time zone` | Time when the currently active query was started, or if`state`is not`active`, when the last query was started |
| `state_change` | `timestamp with time zone` | Time when the`state`was last changed |
| `wait_event_type` | `text` | The type of event for which the backend is waiting, if any; otherwise NULL. Possible values are:`LWLock`: The backend is waiting for a lightweight lock. Each such lock protects a particular data structure in shared memory.`wait_event`will contain a name identifying the purpose of the lightweight lock. \(Some locks have specific names; others are part of a group of locks each with a similar purpose.\)`Lock`: The backend is waiting for a heavyweight lock. Heavyweight locks, also known as lock manager locks or simply locks, primarily protect SQL-visible objects such as tables. However, they are also used to ensure mutual exclusion for certain internal operations such as relation extension.`wait_event`will identify the type of lock awaited.`BufferPin`: The server process is waiting to access to a data buffer during a period when no other process can be examining that buffer. Buffer pin waits can be protracted if another process holds an open cursor which last read data from the buffer in question.`Activity`: The server process is idle. This is used by system processes waiting for activity in their main processing loop.`wait_event`will identify the specific wait point.`Extension`: The server process is waiting for activity in an extension module. This category is useful for modules to track custom waiting points.`Client`: The server process is waiting for some activity on a socket from user applications, and that the server expects something to happen that is independent from its internal processes.`wait_event`will identify the specific wait point.`IPC`: The server process is waiting for some activity from another process in the server.`wait_event`will identify the specific wait point.`Timeout`: The server process is waiting for a timeout to expire.`wait_event`will identify the specific wait point.`IO`: The server process is waiting for a IO to complete.`wait_event`will identify the specific wait point. |
| `wait_event` | `text` | Wait event name if backend is currently waiting, otherwise NULL. See[Table 28.4](https://www.postgresql.org/docs/10/static/monitoring-stats.html#WAIT-EVENT-TABLE)for details. |
| `state` | `text` | Current overall state of this backend. Possible values are:`active`: The backend is executing a query.`idle`: The backend is waiting for a new client command.`idle in transaction`: The backend is in a transaction, but is not currently executing a query.`idle in transaction (aborted)`: This state is similar to`idle in transaction`, except one of the statements in the transaction caused an error.`fastpath function call`: The backend is executing a fast-path function.`disabled`: This state is reported if[track\_activities](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-ACTIVITIES)is disabled in this backend. |
| `backend_xid` | `xid` | Top-level transaction identifier of this backend, if any. |
| `backend_xmin` | `xid` | The current backend's`xmin`horizon. |
| `query` | `text` | Text of this backend's most recent query. If`state`is`active`this field shows the currently executing query. In all other states, it shows the last query that was executed. By default the query text is truncated at 1024 characters; this value can be changed via the parameter[track\_activity\_query\_size](https://www.postgresql.org/docs/10/static/runtime-config-statistics.html#GUC-TRACK-ACTIVITY-QUERY-SIZE). |
| `backend_type` | `text` | Type of current backend. Possible types are`autovacuum launcher`,`autovacuum worker`,`background worker`,`background writer`,`client backend`,`checkpointer`,`startup`,`walreceiver`,`walsender`and`walwriter`. |

  


The`pg_stat_activity`view will have one row per server process, showing information related to the current activity of that process.

### Note

The`wait_event`and`state`columns are independent. If a backend is in the`active`state, it may or may not be`waiting`on some event. If the state is`active`and`wait_event`is non-null, it means that a query is being executed, but is being blocked somewhere in the system.

