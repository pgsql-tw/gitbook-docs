---
description: 版本：11
---

# 27.2. 統計資訊收集器

PostgreSQL's _statistics collector_ is a subsystem that supports collection and reporting of information about server activity. Presently, the collector can count accesses to tables and indexes in both disk-block and individual-row terms. It also tracks the total number of rows in each table, and information about vacuum and analyze actions for each table. It can also count calls to user-defined functions and the total time spent in each one.

PostgreSQL also supports reporting dynamic information about exactly what is going on in the system right now, such as the exact command currently being executed by other server processes, and which other connections exist in the system. This facility is independent of the collector process.

## 27.2.1. Statistics Collection Configuration

Since collection of statistics adds some overhead to query execution, the system can be configured to collect or not collect information. This is controlled by configuration parameters that are normally set in `postgresql.conf`. \(See [Chapter 19](https://www.postgresql.org/docs/13/runtime-config.html) for details about setting configuration parameters.\)

The parameter [track\_activities](https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-ACTIVITIES) enables monitoring of the current command being executed by any server process.

The parameter [track\_counts](https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-COUNTS) controls whether statistics are collected about table and index accesses.

The parameter [track\_functions](https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-FUNCTIONS) enables tracking of usage of user-defined functions.

The parameter [track\_io\_timing](https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-IO-TIMING) enables monitoring of block read and write times.

Normally these parameters are set in `postgresql.conf` so that they apply to all server processes, but it is possible to turn them on or off in individual sessions using the [SET](https://www.postgresql.org/docs/13/sql-set.html) command. \(To prevent ordinary users from hiding their activity from the administrator, only superusers are allowed to change these parameters with `SET`.\)

The statistics collector transmits the collected information to other PostgreSQL processes through temporary files. These files are stored in the directory named by the [stats\_temp\_directory](https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-STATS-TEMP-DIRECTORY) parameter, `pg_stat_tmp` by default. For better performance, `stats_temp_directory` can be pointed at a RAM-based file system, decreasing physical I/O requirements. When the server shuts down cleanly, a permanent copy of the statistics data is stored in the `pg_stat` subdirectory, so that statistics can be retained across server restarts. When recovery is performed at server start \(e.g., after immediate shutdown, server crash, and point-in-time recovery\), all statistics counters are reset.

## 27.2.2. Viewing Statistics

Several predefined views, listed in [Table 27.1](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-STATS-DYNAMIC-VIEWS-TABLE), are available to show the current state of the system. There are also several other views, listed in [Table 27.2](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-STATS-VIEWS-TABLE), available to show the results of statistics collection. Alternatively, one can build custom views using the underlying statistics functions, as discussed in [Section 27.2.20](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-STATS-FUNCTIONS).

When using the statistics to monitor collected data, it is important to realize that the information does not update instantaneously. Each individual server process transmits new statistical counts to the collector just before going idle; so a query or transaction still in progress does not affect the displayed totals. Also, the collector itself emits a new report at most once per `PGSTAT_STAT_INTERVAL` milliseconds \(500 ms unless altered while building the server\). So the displayed information lags behind actual activity. However, current-query information collected by `track_activities` is always up-to-date.

Another important point is that when a server process is asked to display any of these statistics, it first fetches the most recent report emitted by the collector process and then continues to use this snapshot for all statistical views and functions until the end of its current transaction. So the statistics will show static information as long as you continue the current transaction. Similarly, information about the current queries of all sessions is collected when any such information is first requested within a transaction, and the same information will be displayed throughout the transaction. This is a feature, not a bug, because it allows you to perform several queries on the statistics and correlate the results without worrying that the numbers are changing underneath you. But if you want to see new results with each query, be sure to do the queries outside any transaction block. Alternatively, you can invoke `pg_stat_clear_snapshot`\(\), which will discard the current transaction's statistics snapshot \(if any\). The next use of statistical information will cause a new snapshot to be fetched.

A transaction can also see its own statistics \(as yet untransmitted to the collector\) in the views `pg_stat_xact_all_tables`, `pg_stat_xact_sys_tables`, `pg_stat_xact_user_tables`, and `pg_stat_xact_user_functions`. These numbers do not act as stated above; instead they update continuously throughout the transaction.

Some of the information in the dynamic statistics views shown in [Table 27.1](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-STATS-DYNAMIC-VIEWS-TABLE) is security restricted. Ordinary users can only see all the information about their own sessions \(sessions belonging to a role that they are a member of\). In rows about other sessions, many columns will be null. Note, however, that the existence of a session and its general properties such as its sessions user and database are visible to all users. Superusers and members of the built-in role `pg_read_all_stats` \(see also [Section 21.5](https://www.postgresql.org/docs/13/default-roles.html)\) can see all the information about all sessions.

#### **Table 27.1. Dynamic Statistics Views**

| View Name | Description |
| :--- | :--- |
| `pg_stat_activity` | One row per server process, showing information related to the current activity of that process, such as state and current query. See [`pg_stat_activity`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW) for details. |
| `pg_stat_replication` | One row per WAL sender process, showing statistics about replication to that sender's connected standby server. See [`pg_stat_replication`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-VIEW) for details. |
| `pg_stat_wal_receiver` | Only one row, showing statistics about the WAL receiver from that receiver's connected server. See [`pg_stat_wal_receiver`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-WAL-RECEIVER-VIEW) for details. |
| `pg_stat_subscription` | At least one row per subscription, showing information about the subscription workers. See [`pg_stat_subscription`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-SUBSCRIPTION) for details. |
| `pg_stat_ssl` | One row per connection \(regular and replication\), showing information about SSL used on this connection. See [`pg_stat_ssl`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-SSL-VIEW) for details. |
| `pg_stat_gssapi` | One row per connection \(regular and replication\), showing information about GSSAPI authentication and encryption used on this connection. See [`pg_stat_gssapi`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-GSSAPI-VIEW) for details. |
| `pg_stat_progress_analyze` | One row for each backend \(including autovacuum worker processes\) running `ANALYZE`, showing current progress. See [Section 27.4.1](https://www.postgresql.org/docs/13/progress-reporting.html#ANALYZE-PROGRESS-REPORTING). |
| `pg_stat_progress_create_index` | One row for each backend running `CREATE INDEX` or `REINDEX`, showing current progress. See [Section 27.4.2](https://www.postgresql.org/docs/13/progress-reporting.html#CREATE-INDEX-PROGRESS-REPORTING). |
| `pg_stat_progress_vacuum` | One row for each backend \(including autovacuum worker processes\) running `VACUUM`, showing current progress. See [Section 27.4.3](https://www.postgresql.org/docs/13/progress-reporting.html#VACUUM-PROGRESS-REPORTING). |
| `pg_stat_progress_cluster` | One row for each backend running `CLUSTER` or `VACUUM FULL`, showing current progress. See [Section 27.4.4](https://www.postgresql.org/docs/13/progress-reporting.html#CLUSTER-PROGRESS-REPORTING). |
| `pg_stat_progress_basebackup` | One row for each WAL sender process streaming a base backup, showing current progress. See [Section 27.4.5](https://www.postgresql.org/docs/13/progress-reporting.html#BASEBACKUP-PROGRESS-REPORTING). |

#### **Table 27.2. Collected Statistics Views**

| View Name | Description |
| :--- | :--- |
| `pg_stat_archiver` | One row only, showing statistics about the WAL archiver process's activity. See [`pg_stat_archiver`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-ARCHIVER-VIEW) for details. |
| `pg_stat_bgwriter` | One row only, showing statistics about the background writer process's activity. See [`pg_stat_bgwriter`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-BGWRITER-VIEW) for details. |
| `pg_stat_database` | One row per database, showing database-wide statistics. See [`pg_stat_database`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-DATABASE-VIEW) for details. |
| `pg_stat_database_conflicts` | One row per database, showing database-wide statistics about query cancels due to conflict with recovery on standby servers. See [`pg_stat_database_conflicts`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW) for details. |
| `pg_stat_all_tables` | 目前資料庫中每個資料表為一筆資料，顯示有關對該資料表的存取統計數據。有關詳細資訊，請參閱 [pg\_stat\_all\_tables](the-statistics-collector.md#27-2-13-pg_stat_all_tables)。 |
| `pg_stat_sys_tables` | 除了僅顯示系統資料表之外，與 pg\_stat\_all\_tables 相同。 |
| `pg_stat_user_tables` | 除了僅顯示使用者資料表之外，與 pg\_stat\_all\_tables 相同。 |
| `pg_stat_xact_all_tables` | Similar to `pg_stat_all_tables`, but counts actions taken so far within the current transaction \(which are _not_ yet included in `pg_stat_all_tables` and related views\). The columns for numbers of live and dead rows and vacuum and analyze actions are not present in this view. |
| `pg_stat_xact_sys_tables` | Same as `pg_stat_xact_all_tables`, except that only system tables are shown. |
| `pg_stat_xact_user_tables` | Same as `pg_stat_xact_all_tables`, except that only user tables are shown. |
| `pg_stat_all_indexes` | One row for each index in the current database, showing statistics about accesses to that specific index. See [`pg_stat_all_indexes`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-ALL-INDEXES-VIEW) for details. |
| `pg_stat_sys_indexes` | Same as `pg_stat_all_indexes`, except that only indexes on system tables are shown. |
| `pg_stat_user_indexes` | Same as `pg_stat_all_indexes`, except that only indexes on user tables are shown. |
| `pg_statio_all_tables` | One row for each table in the current database, showing statistics about I/O on that specific table. See [`pg_statio_all_tables`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STATIO-ALL-TABLES-VIEW) for details. |
| `pg_statio_sys_tables` | Same as `pg_statio_all_tables`, except that only system tables are shown. |
| `pg_statio_user_tables` | Same as `pg_statio_all_tables`, except that only user tables are shown. |
| `pg_statio_all_indexes` | One row for each index in the current database, showing statistics about I/O on that specific index. See [`pg_statio_all_indexes`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STATIO-ALL-INDEXES-VIEW) for details. |
| `pg_statio_sys_indexes` | Same as `pg_statio_all_indexes`, except that only indexes on system tables are shown. |
| `pg_statio_user_indexes` | Same as `pg_statio_all_indexes`, except that only indexes on user tables are shown. |
| `pg_statio_all_sequences` | One row for each sequence in the current database, showing statistics about I/O on that specific sequence. See [`pg_statio_all_sequences`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW) for details. |
| `pg_statio_sys_sequences` | Same as `pg_statio_all_sequences`, except that only system sequences are shown. \(Presently, no system sequences are defined, so this view is always empty.\) |
| `pg_statio_user_sequences` | Same as `pg_statio_all_sequences`, except that only user sequences are shown. |
| `pg_stat_user_functions` | One row for each tracked function, showing statistics about executions of that function. See [`pg_stat_user_functions`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-USER-FUNCTIONS-VIEW) for details. |
| `pg_stat_xact_user_functions` | Similar to `pg_stat_user_functions`, but counts only calls during the current transaction \(which are _not_ yet included in `pg_stat_user_functions`\). |
| `pg_stat_slru` | One row per SLRU, showing statistics of operations. See [`pg_stat_slru`](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-SLRU-VIEW) for details. |

The per-index statistics are particularly useful to determine which indexes are being used and how effective they are.

The `pg_statio_` views are primarily useful to determine the effectiveness of the buffer cache. When the number of actual disk reads is much smaller than the number of buffer hits, then the cache is satisfying most read requests without invoking a kernel call. However, these statistics do not give the entire story: due to the way in which PostgreSQL handles disk I/O, data that is not in the PostgreSQL buffer cache might still reside in the kernel's I/O cache, and might therefore still be fetched without requiring a physical read. Users interested in obtaining more detailed information on PostgreSQL I/O behavior are advised to use the PostgreSQL statistics collector in combination with operating system utilities that allow insight into the kernel's handling of I/O.

## 27.2.3. `pg_stat_activity`

The `pg_stat_activity` view will have one row per server process, showing information related to the current activity of that process.

#### **Table 27.3. `pg_stat_activity` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>datid</code>  <code>oid</code>
        </p>
        <p>OID of the database this backend is connected to</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>datname</code>  <code>name</code>
        </p>
        <p>Name of the database this backend is connected to</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pid</code>  <code>integer</code>
        </p>
        <p>Process ID of this backend</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>leader_pid</code>  <code>integer</code>
        </p>
        <p>Process ID of the parallel group leader, if this process is a parallel
          query worker. <code>NULL</code> if this process is a parallel group leader
          or does not participate in parallel query.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>usesysid</code>  <code>oid</code>
        </p>
        <p>OID of the user logged into this backend</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>usename</code>  <code>name</code>
        </p>
        <p>Name of the user logged into this backend</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>application_name</code>  <code>text</code>
        </p>
        <p>Name of the application that is connected to this backend</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>client_addr</code>  <code>inet</code>
        </p>
        <p>IP address of the client connected to this backend. If this field is null,
          it indicates either that the client is connected via a Unix socket on the
          server machine or that this is an internal process such as autovacuum.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>client_hostname</code>  <code>text</code>
        </p>
        <p>Host name of the connected client, as reported by a reverse DNS lookup
          of <code>client_addr</code>. This field will only be non-null for IP connections,
          and only when <a href="https://www.postgresql.org/docs/13/runtime-config-logging.html#GUC-LOG-HOSTNAME">log_hostname</a> is
          enabled.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>client_port</code>  <code>integer</code>
        </p>
        <p>TCP port number that the client is using for communication with this backend,
          or <code>-1</code> if a Unix socket is used. If this field is null, it indicates
          that this is an internal server process.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>backend_start</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time when this process was started. For client backends, this is the time
          the client connected to the server.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>xact_start</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time when this process&apos; current transaction was started, or null
          if no transaction is active. If the current query is the first of its transaction,
          this column is equal to the <code>query_start</code> column.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>query_start</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time when the currently active query was started, or if <code>state</code> is
          not <code>active</code>, when the last query was started</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>state_change</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time when the <code>state</code> was last changed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>wait_event_type</code>  <code>text</code>
        </p>
        <p>The type of event for which the backend is waiting, if any; otherwise
          NULL. See <a href="https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-TABLE">Table 27.4</a>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>wait_event</code>  <code>text</code>
        </p>
        <p>Wait event name if backend is currently waiting, otherwise NULL. See
          <a
          href="https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-ACTIVITY-TABLE">Table 27.5</a>through <a href="https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-TIMEOUT-TABLE">Table 27.13</a>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>state</code>  <code>text</code>
        </p>
        <p>Current overall state of this backend. Possible values are:</p>
        <ul>
          <li><code>active</code>: The backend is executing a query.</li>
          <li><code>idle</code>: The backend is waiting for a new client command.</li>
          <li><code>idle in transaction</code>: The backend is in a transaction, but
            is not currently executing a query.</li>
          <li><code>idle in transaction (aborted)</code>: This state is similar to <code>idle in transaction</code>,
            except one of the statements in the transaction caused an error.</li>
          <li><code>fastpath function call</code>: The backend is executing a fast-path
            function.</li>
          <li><code>disabled</code>: This state is reported if <a href="https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-ACTIVITIES">track_activities</a> is
            disabled in this backend.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>backend_xid</code>  <code>xid</code>
        </p>
        <p>Top-level transaction identifier of this backend, if any.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>backend_xmin</code>  <code>xid</code>
        </p>
        <p>The current backend&apos;s <code>xmin</code> horizon.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>query</code>  <code>text</code>
        </p>
        <p>Text of this backend&apos;s most recent query. If <code>state</code> is <code>active</code> this
          field shows the currently executing query. In all other states, it shows
          the last query that was executed. By default the query text is truncated
          at 1024 bytes; this value can be changed via the parameter <a href="https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-ACTIVITY-QUERY-SIZE">track_activity_query_size</a>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>backend_type</code>  <code>text</code>
        </p>
        <p>Type of current backend. Possible types are <code>autovacuum launcher</code>, <code>autovacuum worker</code>, <code>logical replication launcher</code>, <code>logical replication worker</code>, <code>parallel worker</code>, <code>background writer</code>, <code>client backend</code>, <code>checkpointer</code>, <code>startup</code>, <code>walreceiver</code>, <code>walsender</code> and <code>walwriter</code>.
          In addition, background workers registered by extensions may have additional
          types.</p>
      </td>
    </tr>
  </tbody>
</table>

#### Note

The `wait_event` and `state` columns are independent. If a backend is in the `active` state, it may or may not be `waiting` on some event. If the state is `active` and `wait_event` is non-null, it means that a query is being executed, but is being blocked somewhere in the system.

#### **Table 27.4. Wait Event Types**

| Wait Event Type | Description |
| :--- | :--- |
| `Activity` | The server process is idle. This event type indicates a process waiting for activity in its main processing loop. `wait_event` will identify the specific wait point; see [Table 27.5](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-ACTIVITY-TABLE). |
| `BufferPin` | The server process is waiting for exclusive access to a data buffer. Buffer pin waits can be protracted if another process holds an open cursor that last read data from the buffer in question. See [Table 27.6](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-BUFFERPIN-TABLE). |
| `Client` | The server process is waiting for activity on a socket connected to a user application. Thus, the server expects something to happen that is independent of its internal processes. `wait_event` will identify the specific wait point; see [Table 27.7](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-CLIENT-TABLE). |
| `Extension` | The server process is waiting for some condition defined by an extension module. See [Table 27.8](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-EXTENSION-TABLE). |
| `IO` | The server process is waiting for an I/O operation to complete. `wait_event` will identify the specific wait point; see [Table 27.9](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-IO-TABLE). |
| `IPC` | The server process is waiting for some interaction with another server process. `wait_event` will identify the specific wait point; see [Table 27.10](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-IPC-TABLE). |
| `Lock` | The server process is waiting for a heavyweight lock. Heavyweight locks, also known as lock manager locks or simply locks, primarily protect SQL-visible objects such as tables. However, they are also used to ensure mutual exclusion for certain internal operations such as relation extension. `wait_event` will identify the type of lock awaited; see [Table 27.11](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-LOCK-TABLE). |
| `LWLock` | The server process is waiting for a lightweight lock. Most such locks protect a particular data structure in shared memory. `wait_event` will contain a name identifying the purpose of the lightweight lock. \(Some locks have specific names; others are part of a group of locks each with a similar purpose.\) See [Table 27.12](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-LWLOCK-TABLE). |
| `Timeout` | The server process is waiting for a timeout to expire. `wait_event` will identify the specific wait point; see [Table 27.13](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-TIMEOUT-TABLE). |

#### **Table 27.5. Wait Events of Type `Activity`**

| `Activity` Wait Event | Description |
| :--- | :--- |
| `ArchiverMain` | Waiting in main loop of archiver process. |
| `AutoVacuumMain` | Waiting in main loop of autovacuum launcher process. |
| `BgWriterHibernate` | Waiting in background writer process, hibernating. |
| `BgWriterMain` | Waiting in main loop of background writer process. |
| `CheckpointerMain` | Waiting in main loop of checkpointer process. |
| `LogicalApplyMain` | Waiting in main loop of logical replication apply process. |
| `LogicalLauncherMain` | Waiting in main loop of logical replication launcher process. |
| `PgStatMain` | Waiting in main loop of statistics collector process. |
| `RecoveryWalStream` | Waiting in main loop of startup process for WAL to arrive, during streaming recovery. |
| `SysLoggerMain` | Waiting in main loop of syslogger process. |
| `WalReceiverMain` | Waiting in main loop of WAL receiver process. |
| `WalSenderMain` | Waiting in main loop of WAL sender process. |
| `WalWriterMain` | Waiting in main loop of WAL writer process. |

#### **Table 27.6. Wait Events of Type `BufferPin`**

| `BufferPin` Wait Event | Description |
| :--- | :--- |
| `BufferPin` | Waiting to acquire an exclusive pin on a buffer. |

#### **Table 27.7. Wait Events of Type `Client`**

| `Client` Wait Event | Description |
| :--- | :--- |
| `ClientRead` | Waiting to read data from the client. |
| `ClientWrite` | Waiting to write data to the client. |
| `GSSOpenServer` | Waiting to read data from the client while establishing a GSSAPI session. |
| `LibPQWalReceiverConnect` | Waiting in WAL receiver to establish connection to remote server. |
| `LibPQWalReceiverReceive` | Waiting in WAL receiver to receive data from remote server. |
| `SSLOpenServer` | Waiting for SSL while attempting connection. |
| `WalReceiverWaitStart` | Waiting for startup process to send initial data for streaming replication. |
| `WalSenderWaitForWAL` | Waiting for WAL to be flushed in WAL sender process. |
| `WalSenderWriteData` | Waiting for any activity when processing replies from WAL receiver in WAL sender process. |

#### **Table 27.8. Wait Events of Type `Extension`**

| `Extension` Wait Event | Description |
| :--- | :--- |
| `Extension` | Waiting in an extension. |

#### **Table 27.9. Wait Events of Type `IO`**

| `IO` Wait Event | Description |
| :--- | :--- |
| `BufFileRead` | Waiting for a read from a buffered file. |
| `BufFileWrite` | Waiting for a write to a buffered file. |
| `ControlFileRead` | Waiting for a read from the `pg_control` file. |
| `ControlFileSync` | Waiting for the `pg_control` file to reach durable storage. |
| `ControlFileSyncUpdate` | Waiting for an update to the `pg_control` file to reach durable storage. |
| `ControlFileWrite` | Waiting for a write to the `pg_control` file. |
| `ControlFileWriteUpdate` | Waiting for a write to update the `pg_control` file. |
| `CopyFileRead` | Waiting for a read during a file copy operation. |
| `CopyFileWrite` | Waiting for a write during a file copy operation. |
| `DSMFillZeroWrite` | Waiting to fill a dynamic shared memory backing file with zeroes. |
| `DataFileExtend` | Waiting for a relation data file to be extended. |
| `DataFileFlush` | Waiting for a relation data file to reach durable storage. |
| `DataFileImmediateSync` | Waiting for an immediate synchronization of a relation data file to durable storage. |
| `DataFilePrefetch` | Waiting for an asynchronous prefetch from a relation data file. |
| `DataFileRead` | Waiting for a read from a relation data file. |
| `DataFileSync` | Waiting for changes to a relation data file to reach durable storage. |
| `DataFileTruncate` | Waiting for a relation data file to be truncated. |
| `DataFileWrite` | Waiting for a write to a relation data file. |
| `LockFileAddToDataDirRead` | Waiting for a read while adding a line to the data directory lock file. |
| `LockFileAddToDataDirSync` | Waiting for data to reach durable storage while adding a line to the data directory lock file. |
| `LockFileAddToDataDirWrite` | Waiting for a write while adding a line to the data directory lock file. |
| `LockFileCreateRead` | Waiting to read while creating the data directory lock file. |
| `LockFileCreateSync` | Waiting for data to reach durable storage while creating the data directory lock file. |
| `LockFileCreateWrite` | Waiting for a write while creating the data directory lock file. |
| `LockFileReCheckDataDirRead` | Waiting for a read during recheck of the data directory lock file. |
| `LogicalRewriteCheckpointSync` | Waiting for logical rewrite mappings to reach durable storage during a checkpoint. |
| `LogicalRewriteMappingSync` | Waiting for mapping data to reach durable storage during a logical rewrite. |
| `LogicalRewriteMappingWrite` | Waiting for a write of mapping data during a logical rewrite. |
| `LogicalRewriteSync` | Waiting for logical rewrite mappings to reach durable storage. |
| `LogicalRewriteTruncate` | Waiting for truncate of mapping data during a logical rewrite. |
| `LogicalRewriteWrite` | Waiting for a write of logical rewrite mappings. |
| `RelationMapRead` | Waiting for a read of the relation map file. |
| `RelationMapSync` | Waiting for the relation map file to reach durable storage. |
| `RelationMapWrite` | Waiting for a write to the relation map file. |
| `ReorderBufferRead` | Waiting for a read during reorder buffer management. |
| `ReorderBufferWrite` | Waiting for a write during reorder buffer management. |
| `ReorderLogicalMappingRead` | Waiting for a read of a logical mapping during reorder buffer management. |
| `ReplicationSlotRead` | Waiting for a read from a replication slot control file. |
| `ReplicationSlotRestoreSync` | Waiting for a replication slot control file to reach durable storage while restoring it to memory. |
| `ReplicationSlotSync` | Waiting for a replication slot control file to reach durable storage. |
| `ReplicationSlotWrite` | Waiting for a write to a replication slot control file. |
| `SLRUFlushSync` | Waiting for SLRU data to reach durable storage during a checkpoint or database shutdown. |
| `SLRURead` | Waiting for a read of an SLRU page. |
| `SLRUSync` | Waiting for SLRU data to reach durable storage following a page write. |
| `SLRUWrite` | Waiting for a write of an SLRU page. |
| `SnapbuildRead` | Waiting for a read of a serialized historical catalog snapshot. |
| `SnapbuildSync` | Waiting for a serialized historical catalog snapshot to reach durable storage. |
| `SnapbuildWrite` | Waiting for a write of a serialized historical catalog snapshot. |
| `TimelineHistoryFileSync` | Waiting for a timeline history file received via streaming replication to reach durable storage. |
| `TimelineHistoryFileWrite` | Waiting for a write of a timeline history file received via streaming replication. |
| `TimelineHistoryRead` | Waiting for a read of a timeline history file. |
| `TimelineHistorySync` | Waiting for a newly created timeline history file to reach durable storage. |
| `TimelineHistoryWrite` | Waiting for a write of a newly created timeline history file. |
| `TwophaseFileRead` | Waiting for a read of a two phase state file. |
| `TwophaseFileSync` | Waiting for a two phase state file to reach durable storage. |
| `TwophaseFileWrite` | Waiting for a write of a two phase state file. |
| `WALBootstrapSync` | Waiting for WAL to reach durable storage during bootstrapping. |
| `WALBootstrapWrite` | Waiting for a write of a WAL page during bootstrapping. |
| `WALCopyRead` | Waiting for a read when creating a new WAL segment by copying an existing one. |
| `WALCopySync` | Waiting for a new WAL segment created by copying an existing one to reach durable storage. |
| `WALCopyWrite` | Waiting for a write when creating a new WAL segment by copying an existing one. |
| `WALInitSync` | Waiting for a newly initialized WAL file to reach durable storage. |
| `WALInitWrite` | Waiting for a write while initializing a new WAL file. |
| `WALRead` | Waiting for a read from a WAL file. |
| `WALSenderTimelineHistoryRead` | Waiting for a read from a timeline history file during a walsender timeline command. |
| `WALSync` | Waiting for a WAL file to reach durable storage. |
| `WALSyncMethodAssign` | Waiting for data to reach durable storage while assigning a new WAL sync method. |
| `WALWrite` | Waiting for a write to a WAL file. |

#### **Table 27.10. Wait Events of Type `IPC`**

| `IPC` Wait Event | Description |
| :--- | :--- |
| `BackupWaitWalArchive` | Waiting for WAL files required for a backup to be successfully archived. |
| `BgWorkerShutdown` | Waiting for background worker to shut down. |
| `BgWorkerStartup` | Waiting for background worker to start up. |
| `BtreePage` | Waiting for the page number needed to continue a parallel B-tree scan to become available. |
| `CheckpointDone` | Waiting for a checkpoint to complete. |
| `CheckpointStart` | Waiting for a checkpoint to start. |
| `ExecuteGather` | Waiting for activity from a child process while executing a `Gather` plan node. |
| `HashBatchAllocate` | Waiting for an elected Parallel Hash participant to allocate a hash table. |
| `HashBatchElect` | Waiting to elect a Parallel Hash participant to allocate a hash table. |
| `HashBatchLoad` | Waiting for other Parallel Hash participants to finish loading a hash table. |
| `HashBuildAllocate` | Waiting for an elected Parallel Hash participant to allocate the initial hash table. |
| `HashBuildElect` | Waiting to elect a Parallel Hash participant to allocate the initial hash table. |
| `HashBuildHashInner` | Waiting for other Parallel Hash participants to finish hashing the inner relation. |
| `HashBuildHashOuter` | Waiting for other Parallel Hash participants to finish partitioning the outer relation. |
| `HashGrowBatchesAllocate` | Waiting for an elected Parallel Hash participant to allocate more batches. |
| `HashGrowBatchesDecide` | Waiting to elect a Parallel Hash participant to decide on future batch growth. |
| `HashGrowBatchesElect` | Waiting to elect a Parallel Hash participant to allocate more batches. |
| `HashGrowBatchesFinish` | Waiting for an elected Parallel Hash participant to decide on future batch growth. |
| `HashGrowBatchesRepartition` | Waiting for other Parallel Hash participants to finish repartitioning. |
| `HashGrowBucketsAllocate` | Waiting for an elected Parallel Hash participant to finish allocating more buckets. |
| `HashGrowBucketsElect` | Waiting to elect a Parallel Hash participant to allocate more buckets. |
| `HashGrowBucketsReinsert` | Waiting for other Parallel Hash participants to finish inserting tuples into new buckets. |
| `LogicalSyncData` | Waiting for a logical replication remote server to send data for initial table synchronization. |
| `LogicalSyncStateChange` | Waiting for a logical replication remote server to change state. |
| `MessageQueueInternal` | Waiting for another process to be attached to a shared message queue. |
| `MessageQueuePutMessage` | Waiting to write a protocol message to a shared message queue. |
| `MessageQueueReceive` | Waiting to receive bytes from a shared message queue. |
| `MessageQueueSend` | Waiting to send bytes to a shared message queue. |
| `ParallelBitmapScan` | Waiting for parallel bitmap scan to become initialized. |
| `ParallelCreateIndexScan` | Waiting for parallel `CREATE INDEX` workers to finish heap scan. |
| `ParallelFinish` | Waiting for parallel workers to finish computing. |
| `ProcArrayGroupUpdate` | Waiting for the group leader to clear the transaction ID at end of a parallel operation. |
| `ProcSignalBarrier` | Waiting for a barrier event to be processed by all backends. |
| `Promote` | Waiting for standby promotion. |
| `RecoveryConflictSnapshot` | Waiting for recovery conflict resolution for a vacuum cleanup. |
| `RecoveryConflictTablespace` | Waiting for recovery conflict resolution for dropping a tablespace. |
| `RecoveryPause` | Waiting for recovery to be resumed. |
| `ReplicationOriginDrop` | Waiting for a replication origin to become inactive so it can be dropped. |
| `ReplicationSlotDrop` | Waiting for a replication slot to become inactive so it can be dropped. |
| `SafeSnapshot` | Waiting to obtain a valid snapshot for a `READ ONLY DEFERRABLE` transaction. |
| `SyncRep` | Waiting for confirmation from a remote server during synchronous replication. |
| `XactGroupUpdate` | Waiting for the group leader to update transaction status at end of a parallel operation. |

#### **Table 27.11. Wait Events of Type `Lock`**

| `Lock` Wait Event | Description |
| :--- | :--- |
| `advisory` | Waiting to acquire an advisory user lock. |
| `extend` | Waiting to extend a relation. |
| `frozenid` | Waiting to update `pg_database`.`datfrozenxid` and `pg_database`.`datminmxid`. |
| `object` | Waiting to acquire a lock on a non-relation database object. |
| `page` | Waiting to acquire a lock on a page of a relation. |
| `relation` | Waiting to acquire a lock on a relation. |
| `spectoken` | Waiting to acquire a speculative insertion lock. |
| `transactionid` | Waiting for a transaction to finish. |
| `tuple` | Waiting to acquire a lock on a tuple. |
| `userlock` | Waiting to acquire a user lock. |
| `virtualxid` | Waiting to acquire a virtual transaction ID lock. |

#### **Table 27.12. Wait Events of Type `LWLock`**

| `LWLock` Wait Event | Description |
| :--- | :--- |
| `AddinShmemInit` | Waiting to manage an extension's space allocation in shared memory. |
| `AutoFile` | Waiting to update the `postgresql.auto.conf` file. |
| `Autovacuum` | Waiting to read or update the current state of autovacuum workers. |
| `AutovacuumSchedule` | Waiting to ensure that a table selected for autovacuum still needs vacuuming. |
| `BackgroundWorker` | Waiting to read or update background worker state. |
| `BtreeVacuum` | Waiting to read or update vacuum-related information for a B-tree index. |
| `BufferContent` | Waiting to access a data page in memory. |
| `BufferIO` | Waiting for I/O on a data page. |
| `BufferMapping` | Waiting to associate a data block with a buffer in the buffer pool. |
| `Checkpoint` | Waiting to begin a checkpoint. |
| `CheckpointerComm` | Waiting to manage fsync requests. |
| `CommitTs` | Waiting to read or update the last value set for a transaction commit timestamp. |
| `CommitTsBuffer` | Waiting for I/O on a commit timestamp SLRU buffer. |
| `CommitTsSLRU` | Waiting to access the commit timestamp SLRU cache. |
| `ControlFile` | Waiting to read or update the `pg_control` file or create a new WAL file. |
| `DynamicSharedMemoryControl` | Waiting to read or update dynamic shared memory allocation information. |
| `LockFastPath` | Waiting to read or update a process' fast-path lock information. |
| `LockManager` | Waiting to read or update information about “heavyweight” locks. |
| `LogicalRepWorker` | Waiting to read or update the state of logical replication workers. |
| `MultiXactGen` | Waiting to read or update shared multixact state. |
| `MultiXactMemberBuffer` | Waiting for I/O on a multixact member SLRU buffer. |
| `MultiXactMemberSLRU` | Waiting to access the multixact member SLRU cache. |
| `MultiXactOffsetBuffer` | Waiting for I/O on a multixact offset SLRU buffer. |
| `MultiXactOffsetSLRU` | Waiting to access the multixact offset SLRU cache. |
| `MultiXactTruncation` | Waiting to read or truncate multixact information. |
| `NotifyBuffer` | Waiting for I/O on a `NOTIFY` message SLRU buffer. |
| `NotifyQueue` | Waiting to read or update `NOTIFY` messages. |
| `NotifyQueueTail` | Waiting to update limit on `NOTIFY` message storage. |
| `NotifySLRU` | Waiting to access the `NOTIFY` message SLRU cache. |
| `OidGen` | Waiting to allocate a new OID. |
| `OldSnapshotTimeMap` | Waiting to read or update old snapshot control information. |
| `ParallelAppend` | Waiting to choose the next subplan during Parallel Append plan execution. |
| `ParallelHashJoin` | Waiting to synchronize workers during Parallel Hash Join plan execution. |
| `ParallelQueryDSA` | Waiting for parallel query dynamic shared memory allocation. |
| `PerSessionDSA` | Waiting for parallel query dynamic shared memory allocation. |
| `PerSessionRecordType` | Waiting to access a parallel query's information about composite types. |
| `PerSessionRecordTypmod` | Waiting to access a parallel query's information about type modifiers that identify anonymous record types. |
| `PerXactPredicateList` | Waiting to access the list of predicate locks held by the current serializable transaction during a parallel query. |
| `PredicateLockManager` | Waiting to access predicate lock information used by serializable transactions. |
| `ProcArray` | Waiting to access the shared per-process data structures \(typically, to get a snapshot or report a session's transaction ID\). |
| `RelationMapping` | Waiting to read or update a `pg_filenode.map` file \(used to track the filenode assignments of certain system catalogs\). |
| `RelCacheInit` | Waiting to read or update a `pg_internal.init` relation cache initialization file. |
| `ReplicationOrigin` | Waiting to create, drop or use a replication origin. |
| `ReplicationOriginState` | Waiting to read or update the progress of one replication origin. |
| `ReplicationSlotAllocation` | Waiting to allocate or free a replication slot. |
| `ReplicationSlotControl` | Waiting to read or update replication slot state. |
| `ReplicationSlotIO` | Waiting for I/O on a replication slot. |
| `SerialBuffer` | Waiting for I/O on a serializable transaction conflict SLRU buffer. |
| `SerializableFinishedList` | Waiting to access the list of finished serializable transactions. |
| `SerializablePredicateList` | Waiting to access the list of predicate locks held by serializable transactions. |
| `SerializableXactHash` | Waiting to read or update information about serializable transactions. |
| `SerialSLRU` | Waiting to access the serializable transaction conflict SLRU cache. |
| `SharedTidBitmap` | Waiting to access a shared TID bitmap during a parallel bitmap index scan. |
| `SharedTupleStore` | Waiting to access a shared tuple store during parallel query. |
| `ShmemIndex` | Waiting to find or allocate space in shared memory. |
| `SInvalRead` | Waiting to retrieve messages from the shared catalog invalidation queue. |
| `SInvalWrite` | Waiting to add a message to the shared catalog invalidation queue. |
| `SubtransBuffer` | Waiting for I/O on a sub-transaction SLRU buffer. |
| `SubtransSLRU` | Waiting to access the sub-transaction SLRU cache. |
| `SyncRep` | Waiting to read or update information about the state of synchronous replication. |
| `SyncScan` | Waiting to select the starting location of a synchronized table scan. |
| `TablespaceCreate` | Waiting to create or drop a tablespace. |
| `TwoPhaseState` | Waiting to read or update the state of prepared transactions. |
| `WALBufMapping` | Waiting to replace a page in WAL buffers. |
| `WALInsert` | Waiting to insert WAL data into a memory buffer. |
| `WALWrite` | Waiting for WAL buffers to be written to disk. |
| `WrapLimitsVacuum` | Waiting to update limits on transaction id and multixact consumption. |
| `XactBuffer` | Waiting for I/O on a transaction status SLRU buffer. |
| `XactSLRU` | Waiting to access the transaction status SLRU cache. |
| `XactTruncation` | Waiting to execute `pg_xact_status` or update the oldest transaction ID available to it. |
| `XidGen` | Waiting to allocate a new transaction ID. |

#### Note

Extensions can add `LWLock` types to the list shown in [Table 27.12](https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-LWLOCK-TABLE). In some cases, the name assigned by an extension will not be available in all server processes; so an `LWLock` wait event might be reported as just “`extension`” rather than the extension-assigned name.

#### **Table 27.13. Wait Events of Type `Timeout`**

| `Timeout` Wait Event | Description |
| :--- | :--- |
| `BaseBackupThrottle` | Waiting during base backup when throttling activity. |
| `PgSleep` | Waiting due to a call to `pg_sleep` or a sibling function. |
| `RecoveryApplyDelay` | Waiting to apply WAL during recovery because of a delay setting. |
| `RecoveryRetrieveRetryInterval` | Waiting during recovery when WAL data is not available from any source \(`pg_wal`, archive or stream\). |
| `VacuumDelay` | Waiting in a cost-based vacuum delay point. |

Here is an example of how wait events can be viewed:

```text
SELECT pid, wait_event_type, wait_event FROM pg_stat_activity WHERE wait_event is NOT NULL;
 pid  | wait_event_type | wait_event 
------+-----------------+------------
 2540 | Lock            | relation
 6644 | LWLock          | ProcArray
(2 rows)
```

## 27.2.4. `pg_stat_replication`

The `pg_stat_replication` view will contain one row per WAL sender process, showing statistics about replication to that sender's connected standby server. Only directly connected standbys are listed; no information is available about downstream standby servers.

#### **Table 27.14. `pg_stat_replication` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>pid</code>  <code>integer</code>
        </p>
        <p>Process ID of a WAL sender process</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>usesysid</code>  <code>oid</code>
        </p>
        <p>OID of the user logged into this WAL sender process</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>usename</code>  <code>name</code>
        </p>
        <p>Name of the user logged into this WAL sender process</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>application_name</code>  <code>text</code>
        </p>
        <p>Name of the application that is connected to this WAL sender</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>client_addr</code>  <code>inet</code>
        </p>
        <p>IP address of the client connected to this WAL sender. If this field is
          null, it indicates that the client is connected via a Unix socket on the
          server machine.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>client_hostname</code>  <code>text</code>
        </p>
        <p>Host name of the connected client, as reported by a reverse DNS lookup
          of <code>client_addr</code>. This field will only be non-null for IP connections,
          and only when <a href="https://www.postgresql.org/docs/13/runtime-config-logging.html#GUC-LOG-HOSTNAME">log_hostname</a> is
          enabled.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>client_port</code>  <code>integer</code>
        </p>
        <p>TCP port number that the client is using for communication with this WAL
          sender, or <code>-1</code> if a Unix socket is used</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>backend_start</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time when this process was started, i.e., when the client connected to
          this WAL sender</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>backend_xmin</code>  <code>xid</code>
        </p>
        <p>This standby&apos;s <code>xmin</code> horizon reported by <a href="https://www.postgresql.org/docs/13/runtime-config-replication.html#GUC-HOT-STANDBY-FEEDBACK">hot_standby_feedback</a>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>state</code>  <code>text</code>
        </p>
        <p>Current WAL sender state. Possible values are:</p>
        <ul>
          <li><code>startup</code>: This WAL sender is starting up.</li>
          <li><code>catchup</code>: This WAL sender&apos;s connected standby is catching
            up with the primary.</li>
          <li><code>streaming</code>: This WAL sender is streaming changes after its
            connected standby server has caught up with the primary.</li>
          <li><code>backup</code>: This WAL sender is sending a backup.</li>
          <li><code>stopping</code>: This WAL sender is stopping.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>sent_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>Last write-ahead log location sent on this connection</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>write_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>Last write-ahead log location written to disk by this standby server</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>flush_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>Last write-ahead log location flushed to disk by this standby server</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>replay_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>Last write-ahead log location replayed into the database on this standby
          server</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>write_lag</code>  <code>interval</code>
        </p>
        <p>Time elapsed between flushing recent WAL locally and receiving notification
          that this standby server has written it (but not yet flushed it or applied
          it). This can be used to gauge the delay that <code>synchronous_commit</code> level <code>remote_write</code> incurred
          while committing if this server was configured as a synchronous standby.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>flush_lag</code>  <code>interval</code>
        </p>
        <p>Time elapsed between flushing recent WAL locally and receiving notification
          that this standby server has written and flushed it (but not yet applied
          it). This can be used to gauge the delay that <code>synchronous_commit</code> level <code>on</code> incurred
          while committing if this server was configured as a synchronous standby.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>replay_lag</code>  <code>interval</code>
        </p>
        <p>Time elapsed between flushing recent WAL locally and receiving notification
          that this standby server has written, flushed and applied it. This can
          be used to gauge the delay that <code>synchronous_commit</code> level <code>remote_apply</code> incurred
          while committing if this server was configured as a synchronous standby.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>sync_priority</code>  <code>integer</code>
        </p>
        <p>Priority of this standby server for being chosen as the synchronous standby
          in a priority-based synchronous replication. This has no effect in a quorum-based
          synchronous replication.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>sync_state</code>  <code>text</code>
        </p>
        <p>Synchronous state of this standby server. Possible values are:</p>
        <ul>
          <li><code>async</code>: This standby server is asynchronous.</li>
          <li><code>potential</code>: This standby server is now asynchronous, but can
            potentially become synchronous if one of current synchronous ones fails.</li>
          <li><code>sync</code>: This standby server is synchronous.</li>
          <li><code>quorum</code>: This standby server is considered as a candidate
            for quorum standbys.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>reply_time</code>  <code>timestamp with time zone</code>
        </p>
        <p>&#x6700;&#x5F8C;&#x5F9E;&#x5099;&#x7528;&#x4F3A;&#x670D;&#x5668;&#x6536;&#x5230;&#x56DE;&#x8986;&#x8A0A;&#x606F;&#x7684;&#x767C;&#x9001;&#x6642;&#x9593;</p>
      </td>
    </tr>
  </tbody>
</table>

The lag times reported in the `pg_stat_replication` view are measurements of the time taken for recent WAL to be written, flushed and replayed and for the sender to know about it. These times represent the commit delay that was \(or would have been\) introduced by each synchronous commit level, if the remote server was configured as a synchronous standby. For an asynchronous standby, the `replay_lag` column approximates the delay before recent transactions became visible to queries. If the standby server has entirely caught up with the sending server and there is no more WAL activity, the most recently measured lag times will continue to be displayed for a short time and then show NULL.

Lag times work automatically for physical replication. Logical decoding plugins may optionally emit tracking messages; if they do not, the tracking mechanism will simply display NULL lag.

#### Note

The reported lag times are not predictions of how long it will take for the standby to catch up with the sending server assuming the current rate of replay. Such a system would show similar times while new WAL is being generated, but would differ when the sender becomes idle. In particular, when the standby has caught up completely, `pg_stat_replication` shows the time taken to write, flush and replay the most recent reported WAL location rather than zero as some users might expect. This is consistent with the goal of measuring synchronous commit and transaction visibility delays for recent write transactions. To reduce confusion for users expecting a different model of lag, the lag columns revert to NULL after a short time on a fully replayed idle system. Monitoring systems should choose whether to represent this as missing data, zero or continue to display the last known value.

## 27.2.5. `pg_stat_wal_receiver`

The `pg_stat_wal_receiver` view will contain only one row, showing statistics about the WAL receiver from that receiver's connected server.

#### **Table 27.15. `pg_stat_wal_receiver` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>pid</code>  <code>integer</code>
        </p>
        <p>Process ID of the WAL receiver process</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>status</code>  <code>text</code>
        </p>
        <p>Activity status of the WAL receiver process</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>receive_start_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>First write-ahead log location used when WAL receiver is started</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>receive_start_tli</code>  <code>integer</code>
        </p>
        <p>First timeline number used when WAL receiver is started</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>written_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>Last write-ahead log location already received and written to disk, but
          not flushed. This should not be used for data integrity checks.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>flushed_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>Last write-ahead log location already received and flushed to disk, the
          initial value of this field being the first log location used when WAL
          receiver is started</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>received_tli</code>  <code>integer</code>
        </p>
        <p>Timeline number of last write-ahead log location received and flushed
          to disk, the initial value of this field being the timeline number of the
          first log location used when WAL receiver is started</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_msg_send_time</code>  <code>timestamp with time zone</code>
        </p>
        <p>Send time of last message received from origin WAL sender</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_msg_receipt_time</code>  <code>timestamp with time zone</code>
        </p>
        <p>Receipt time of last message received from origin WAL sender</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>latest_end_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>Last write-ahead log location reported to origin WAL sender</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>latest_end_time</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time of last write-ahead log location reported to origin WAL sender</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>slot_name</code>  <code>text</code>
        </p>
        <p>Replication slot name used by this WAL receiver</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>sender_host</code>  <code>text</code>
        </p>
        <p>Host of the PostgreSQL instance this WAL receiver is connected to. This
          can be a host name, an IP address, or a directory path if the connection
          is via Unix socket. (The path case can be distinguished because it will
          always be an absolute path, beginning with <code>/</code>.)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>sender_port</code>  <code>integer</code>
        </p>
        <p>Port number of the PostgreSQL instance this WAL receiver is connected
          to.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>conninfo</code>  <code>text</code>
        </p>
        <p>Connection string used by this WAL receiver, with security-sensitive fields
          obfuscated.</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.6. `pg_stat_subscription`

The `pg_stat_subscription` view will contain one row per subscription for main worker \(with null PID if the worker is not running\), and additional rows for workers handling the initial data copy of the subscribed tables.

#### **Table 27.16. `pg_stat_subscription` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>subid</code>  <code>oid</code>
        </p>
        <p>OID of the subscription</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>subname</code>  <code>name</code>
        </p>
        <p>Name of the subscription</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pid</code>  <code>integer</code>
        </p>
        <p>Process ID of the subscription worker process</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relid</code>  <code>oid</code>
        </p>
        <p>OID of the relation that the worker is synchronizing; null for the main
          apply worker</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>received_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>Last write-ahead log location received, the initial value of this field
          being 0</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_msg_send_time</code>  <code>timestamp with time zone</code>
        </p>
        <p>Send time of last message received from origin WAL sender</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_msg_receipt_time</code>  <code>timestamp with time zone</code>
        </p>
        <p>Receipt time of last message received from origin WAL sender</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>latest_end_lsn</code>  <code>pg_lsn</code>
        </p>
        <p>Last write-ahead log location reported to origin WAL sender</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>latest_end_time</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time of last write-ahead log location reported to origin WAL sender</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.7. `pg_stat_ssl`

The `pg_stat_ssl` view will contain one row per backend or WAL sender process, showing statistics about SSL usage on this connection. It can be joined to `pg_stat_activity` or `pg_stat_replication` on the `pid` column to get more details about the connection.

#### **Table 27.17. `pg_stat_ssl` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>pid</code>  <code>integer</code>
        </p>
        <p>Process ID of a backend or WAL sender process</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>ssl</code>  <code>boolean</code>
        </p>
        <p>True if SSL is used on this connection</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>version</code>  <code>text</code>
        </p>
        <p>Version of SSL in use, or NULL if SSL is not in use on this connection</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>cipher</code>  <code>text</code>
        </p>
        <p>Name of SSL cipher in use, or NULL if SSL is not in use on this connection</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>bits</code>  <code>integer</code>
        </p>
        <p>Number of bits in the encryption algorithm used, or NULL if SSL is not
          used on this connection</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>compression</code>  <code>boolean</code>
        </p>
        <p>True if SSL compression is in use, false if not, or NULL if SSL is not
          in use on this connection</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>client_dn</code>  <code>text</code>
        </p>
        <p>Distinguished Name (DN) field from the client certificate used, or NULL
          if no client certificate was supplied or if SSL is not in use on this connection.
          This field is truncated if the DN field is longer than <code>NAMEDATALEN</code> (64
          characters in a standard build).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>client_serial</code>  <code>numeric</code>
        </p>
        <p>Serial number of the client certificate, or NULL if no client certificate
          was supplied or if SSL is not in use on this connection. The combination
          of certificate serial number and certificate issuer uniquely identifies
          a certificate (unless the issuer erroneously reuses serial numbers).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>issuer_dn</code>  <code>text</code>
        </p>
        <p>DN of the issuer of the client certificate, or NULL if no client certificate
          was supplied or if SSL is not in use on this connection. This field is
          truncated like <code>client_dn</code>.</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.8. `pg_stat_gssapi`

The `pg_stat_gssapi` view will contain one row per backend, showing information about GSSAPI usage on this connection. It can be joined to `pg_stat_activity` or `pg_stat_replication` on the `pid` column to get more details about the connection.

#### **Table 27.18. `pg_stat_gssapi` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>pid</code>  <code>integer</code>
        </p>
        <p>Process ID of a backend</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>gss_authenticated</code>  <code>boolean</code>
        </p>
        <p>True if GSSAPI authentication was used for this connection</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>principal</code>  <code>text</code>
        </p>
        <p>Principal used to authenticate this connection, or NULL if GSSAPI was
          not used to authenticate this connection. This field is truncated if the
          principal is longer than <code>NAMEDATALEN</code> (64 characters in a standard
          build).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>encrypted</code>  <code>boolean</code>
        </p>
        <p>True if GSSAPI encryption is in use on this connection</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.9. `pg_stat_archiver`

The `pg_stat_archiver` view will always have a single row, containing data about the archiver process of the cluster.

#### **Table 27.19. `pg_stat_archiver` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>archived_count</code>  <code>bigint</code>
        </p>
        <p>Number of WAL files that have been successfully archived</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_archived_wal</code>  <code>text</code>
        </p>
        <p>Name of the last WAL file successfully archived</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_archived_time</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time of the last successful archive operation</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>failed_count</code>  <code>bigint</code>
        </p>
        <p>Number of failed attempts for archiving WAL files</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_failed_wal</code>  <code>text</code>
        </p>
        <p>Name of the WAL file of the last failed archival operation</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_failed_time</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time of the last failed archival operation</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stats_reset</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time at which these statistics were last reset</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.10. `pg_stat_bgwriter`

The `pg_stat_bgwriter` view will always have a single row, containing global data for the cluster.

#### **Table 27.20. `pg_stat_bgwriter` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>checkpoints_timed</code>  <code>bigint</code>
        </p>
        <p>Number of scheduled checkpoints that have been performed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>checkpoints_req</code>  <code>bigint</code>
        </p>
        <p>Number of requested checkpoints that have been performed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>checkpoint_write_time</code>  <code>double precision</code>
        </p>
        <p>Total amount of time that has been spent in the portion of checkpoint
          processing where files are written to disk, in milliseconds</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>checkpoint_sync_time</code>  <code>double precision</code>
        </p>
        <p>Total amount of time that has been spent in the portion of checkpoint
          processing where files are synchronized to disk, in milliseconds</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>buffers_checkpoint</code>  <code>bigint</code>
        </p>
        <p>Number of buffers written during checkpoints</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>buffers_clean</code>  <code>bigint</code>
        </p>
        <p>Number of buffers written by the background writer</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>maxwritten_clean</code>  <code>bigint</code>
        </p>
        <p>Number of times the background writer stopped a cleaning scan because
          it had written too many buffers</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>buffers_backend</code>  <code>bigint</code>
        </p>
        <p>Number of buffers written directly by a backend</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>buffers_backend_fsync</code>  <code>bigint</code>
        </p>
        <p>Number of times a backend had to execute its own <code>fsync</code> call
          (normally the background writer handles those even when the backend does
          its own write)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>buffers_alloc</code>  <code>bigint</code>
        </p>
        <p>Number of buffers allocated</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stats_reset</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time at which these statistics were last reset</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.11. `pg_stat_database`

pg\_stat\_database 檢視表將為叢集中的每個資料庫綜合為一筆資料，再加上每個共享物件，列出資料庫層級的統計資訊。

#### **Table 27.21. `pg_stat_database` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>datid</code>  <code>oid</code>
        </p>
        <p>OID of this database, or 0 for objects belonging to a shared relation</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>datname</code>  <code>name</code>
        </p>
        <p>Name of this database, or <code>NULL</code> for shared objects.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>numbackends</code>  <code>integer</code>
        </p>
        <p>Number of backends currently connected to this database, or <code>NULL</code> for
          shared objects. This is the only column in this view that returns a value
          reflecting current state; all other columns return the accumulated values
          since the last reset.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>xact_commit</code>  <code>bigint</code>
        </p>
        <p>Number of transactions in this database that have been committed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>xact_rollback</code>  <code>bigint</code>
        </p>
        <p>Number of transactions in this database that have been rolled back</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blks_read</code>  <code>bigint</code>
        </p>
        <p>Number of disk blocks read in this database</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blks_hit</code>  <code>bigint</code>
        </p>
        <p>Number of times disk blocks were found already in the buffer cache, so
          that a read was not necessary (this only includes hits in the PostgreSQL
          buffer cache, not the operating system&apos;s file system cache)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tup_returned</code>  <code>bigint</code>
        </p>
        <p>Number of rows returned by queries in this database</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tup_fetched</code>  <code>bigint</code>
        </p>
        <p>Number of rows fetched by queries in this database</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tup_inserted</code>  <code>bigint</code>
        </p>
        <p>Number of rows inserted by queries in this database</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tup_updated</code>  <code>bigint</code>
        </p>
        <p>Number of rows updated by queries in this database</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tup_deleted</code>  <code>bigint</code>
        </p>
        <p>Number of rows deleted by queries in this database</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>conflicts</code>  <code>bigint</code>
        </p>
        <p>Number of queries canceled due to conflicts with recovery in this database.
          (Conflicts occur only on standby servers; see <a href="https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW"><code>pg_stat_database_conflicts</code></a> for
          details.)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>temp_files</code>  <code>bigint</code>
        </p>
        <p>&#x7531;&#x6B64;&#x8CC7;&#x6599;&#x5EAB;&#x7684;&#x67E5;&#x8A62;&#x6240;&#x5EFA;&#x7ACB;&#x7684;&#x66AB;&#x5B58;&#x6A94;&#x6848;&#x6578;&#x91CF;&#x3002;&#x7121;&#x8AD6;&#x5EFA;&#x7ACB;&#x66AB;&#x5B58;&#x6A94;&#x6848;&#x7684;&#x539F;&#x56E0;&#xFF08;&#x4F8B;&#x5982;&#x6392;&#x5E8F;&#x6216;
          Hash&#xFF09;&#x5982;&#x4F55;&#xFF0C;&#x4EE5;&#x53CA; <a href="../server-configuration/error-reporting-and-logging.md#log_temp_files-integer">log_temp_files</a> &#x5982;&#x4F55;&#x8A2D;&#x5B9A;&#xFF0C;&#x90FD;&#x6703;&#x5C0D;&#x6240;&#x6709;&#x7684;&#x66AB;&#x5B58;&#x6A94;&#x6848;&#x9032;&#x884C;&#x8A08;&#x6578;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>temp_bytes</code>  <code>bigint</code>
        </p>
        <p>&#x6B64;&#x8CC7;&#x6599;&#x5EAB;&#x4E2D;&#x7684;&#x67E5;&#x8A62;&#x5BEB;&#x5165;&#x66AB;&#x5B58;&#x6A94;&#x6848;&#x7684;&#x8CC7;&#x6599;&#x7E3D;&#x91CF;&#x3002;&#x7121;&#x8AD6;&#x5EFA;&#x7ACB;&#x66AB;&#x6642;&#x6A94;&#x6848;&#x7684;&#x539F;&#x56E0;&#x4EE5;&#x53CA;
          <a
          href="../server-configuration/error-reporting-and-logging.md#log_temp_files-integer">log_temp_files</a>&#x8A2D;&#x5B9A;&#x70BA;&#x4F55;&#xFF0C;&#x90FD;&#x5C07;&#x5C0D;&#x6240;&#x6709;&#x7684;&#x66AB;&#x5B58;&#x6A94;&#x6848;&#x9032;&#x884C;&#x7D71;&#x8A08;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>deadlocks</code>  <code>bigint</code>
        </p>
        <p>Number of deadlocks detected in this database</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>checksum_failures</code>  <code>bigint</code>
        </p>
        <p>Number of data page checksum failures detected in this database (or on
          a shared object), or NULL if data checksums are not enabled.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>checksum_last_failure</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time at which the last data page checksum failure was detected in this
          database (or on a shared object), or NULL if data checksums are not enabled.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blk_read_time</code>  <code>double precision</code>
        </p>
        <p>Time spent reading data file blocks by backends in this database, in milliseconds
          (if <a href="https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-IO-TIMING">track_io_timing</a> is
          enabled, otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blk_write_time</code>  <code>double precision</code>
        </p>
        <p>Time spent writing data file blocks by backends in this database, in milliseconds
          (if <a href="https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-IO-TIMING">track_io_timing</a> is
          enabled, otherwise zero)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stats_reset</code>  <code>timestamp with time zone</code>
        </p>
        <p>&#x4E0A;&#x6B21;&#x91CD;&#x7F6E;&#x9019;&#x500B;&#x7D71;&#x8A08;&#x8CC7;&#x8A0A;&#x7684;&#x6642;&#x9593;</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.12. `pg_stat_database_conflicts`

The `pg_stat_database_conflicts` view will contain one row per database, showing database-wide statistics about query cancels occurring due to conflicts with recovery on standby servers. This view will only contain information on standby servers, since conflicts do not occur on master servers.

#### **Table 27.22. `pg_stat_database_conflicts` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>datid</code>  <code>oid</code>
        </p>
        <p>OID of a database</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>datname</code>  <code>name</code>
        </p>
        <p>Name of this database</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>confl_tablespace</code>  <code>bigint</code>
        </p>
        <p>Number of queries in this database that have been canceled due to dropped
          tablespaces</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>confl_lock</code>  <code>bigint</code>
        </p>
        <p>Number of queries in this database that have been canceled due to lock
          timeouts</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>confl_snapshot</code>  <code>bigint</code>
        </p>
        <p>Number of queries in this database that have been canceled due to old
          snapshots</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>confl_bufferpin</code>  <code>bigint</code>
        </p>
        <p>Number of queries in this database that have been canceled due to pinned
          buffers</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>confl_deadlock</code>  <code>bigint</code>
        </p>
        <p>Number of queries in this database that have been canceled due to deadlocks</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.13. `pg_stat_all_tables`

pg\_stat\_all\_tables 檢視表將為目前資料庫中的每個資料表（包括 TOAST 資料表）為一筆資料，顯示有關對該資料表的存取統計數據。 pg\_stat\_user\_tables 和 pg\_stat\_sys\_tables 檢視表包含相同的資訊，差別是過濾之後僅顯示使用者表和系統資料表。

#### **Table 27.23. `pg_stat_all_tables` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>relid</code>  <code>oid</code>
        </p>
        <p>OID of a table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>schemaname</code>  <code>name</code>
        </p>
        <p>Name of the schema that this table is in</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relname</code>  <code>name</code>
        </p>
        <p>Name of this table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>seq_scan</code>  <code>bigint</code>
        </p>
        <p>Number of sequential scans initiated on this table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>seq_tup_read</code>  <code>bigint</code>
        </p>
        <p>Number of live rows fetched by sequential scans</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>idx_scan</code>  <code>bigint</code>
        </p>
        <p>Number of index scans initiated on this table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>idx_tup_fetch</code>  <code>bigint</code>
        </p>
        <p>Number of live rows fetched by index scans</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>n_tup_ins</code>  <code>bigint</code>
        </p>
        <p>Number of rows inserted</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>n_tup_upd</code>  <code>bigint</code>
        </p>
        <p>Number of rows updated (includes HOT updated rows)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>n_tup_del</code>  <code>bigint</code>
        </p>
        <p>Number of rows deleted</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>n_tup_hot_upd</code>  <code>bigint</code>
        </p>
        <p>Number of rows HOT updated (i.e., with no separate index update required)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>n_live_tup</code>  <code>bigint</code>
        </p>
        <p>Estimated number of live rows</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>n_dead_tup</code>  <code>bigint</code>
        </p>
        <p>Estimated number of dead rows</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>n_mod_since_analyze</code>  <code>bigint</code>
        </p>
        <p>Estimated number of rows modified since this table was last analyzed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>n_ins_since_vacuum</code>  <code>bigint</code>
        </p>
        <p>Estimated number of rows inserted since this table was last vacuumed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_vacuum</code>  <code>timestamp with time zone</code>
        </p>
        <p>Last time at which this table was manually vacuumed (not counting <code>VACUUM FULL</code>)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_autovacuum</code>  <code>timestamp with time zone</code>
        </p>
        <p>Last time at which this table was vacuumed by the autovacuum daemon</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_analyze</code>  <code>timestamp with time zone</code>
        </p>
        <p>Last time at which this table was manually analyzed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>last_autoanalyze</code>  <code>timestamp with time zone</code>
        </p>
        <p>Last time at which this table was analyzed by the autovacuum daemon</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>vacuum_count</code>  <code>bigint</code>
        </p>
        <p>Number of times this table has been manually vacuumed (not counting <code>VACUUM FULL</code>)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>autovacuum_count</code>  <code>bigint</code>
        </p>
        <p>Number of times this table has been vacuumed by the autovacuum daemon</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>analyze_count</code>  <code>bigint</code>
        </p>
        <p>Number of times this table has been manually analyzed</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>autoanalyze_count</code>  <code>bigint</code>
        </p>
        <p>Number of times this table has been analyzed by the autovacuum daemon</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.14. `pg_stat_all_indexes`

The `pg_stat_all_indexes` view will contain one row for each index in the current database, showing statistics about accesses to that specific index. The `pg_stat_user_indexes` and `pg_stat_sys_indexes` views contain the same information, but filtered to only show user and system indexes respectively.

#### **Table 27.24. `pg_stat_all_indexes` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>relid</code>  <code>oid</code>
        </p>
        <p>OID of the table for this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>indexrelid</code>  <code>oid</code>
        </p>
        <p>OID of this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>schemaname</code>  <code>name</code>
        </p>
        <p>Name of the schema this index is in</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relname</code>  <code>name</code>
        </p>
        <p>Name of the table for this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>indexrelname</code>  <code>name</code>
        </p>
        <p>Name of this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>idx_scan</code>  <code>bigint</code>
        </p>
        <p>Number of index scans initiated on this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>idx_tup_read</code>  <code>bigint</code>
        </p>
        <p>Number of index entries returned by scans on this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>idx_tup_fetch</code>  <code>bigint</code>
        </p>
        <p>Number of live table rows fetched by simple index scans using this index</p>
      </td>
    </tr>
  </tbody>
</table>

Indexes can be used by simple index scans, “bitmap” index scans, and the optimizer. In a bitmap scan the output of several indexes can be combined via AND or OR rules, so it is difficult to associate individual heap row fetches with specific indexes when a bitmap scan is used. Therefore, a bitmap scan increments the `pg_stat_all_indexes`.`idx_tup_read` count\(s\) for the index\(es\) it uses, and it increments the `pg_stat_all_tables`.`idx_tup_fetch` count for the table, but it does not affect `pg_stat_all_indexes`.`idx_tup_fetch`. The optimizer also accesses indexes to check for supplied constants whose values are outside the recorded range of the optimizer statistics because the optimizer statistics might be stale.

#### Note

The `idx_tup_read` and `idx_tup_fetch` counts can be different even without any use of bitmap scans, because `idx_tup_read` counts index entries retrieved from the index while `idx_tup_fetch` counts live rows fetched from the table. The latter will be less if any dead or not-yet-committed rows are fetched using the index, or if any heap fetches are avoided by means of an index-only scan.

## 27.2.15. `pg_statio_all_tables`

The `pg_statio_all_tables` view will contain one row for each table in the current database \(including TOAST tables\), showing statistics about I/O on that specific table. The `pg_statio_user_tables` and `pg_statio_sys_tables` views contain the same information, but filtered to only show user and system tables respectively.

#### **Table 27.25. `pg_statio_all_tables` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>relid</code>  <code>oid</code>
        </p>
        <p>OID of a table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>schemaname</code>  <code>name</code>
        </p>
        <p>Name of the schema that this table is in</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relname</code>  <code>name</code>
        </p>
        <p>Name of this table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>heap_blks_read</code>  <code>bigint</code>
        </p>
        <p>Number of disk blocks read from this table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>heap_blks_hit</code>  <code>bigint</code>
        </p>
        <p>Number of buffer hits in this table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>idx_blks_read</code>  <code>bigint</code>
        </p>
        <p>Number of disk blocks read from all indexes on this table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>idx_blks_hit</code>  <code>bigint</code>
        </p>
        <p>Number of buffer hits in all indexes on this table</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>toast_blks_read</code>  <code>bigint</code>
        </p>
        <p>Number of disk blocks read from this table&apos;s TOAST table (if any)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>toast_blks_hit</code>  <code>bigint</code>
        </p>
        <p>Number of buffer hits in this table&apos;s TOAST table (if any)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tidx_blks_read</code>  <code>bigint</code>
        </p>
        <p>Number of disk blocks read from this table&apos;s TOAST table indexes
          (if any)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tidx_blks_hit</code>  <code>bigint</code>
        </p>
        <p>Number of buffer hits in this table&apos;s TOAST table indexes (if any)</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.16. `pg_statio_all_indexes`

The `pg_statio_all_indexes` view will contain one row for each index in the current database, showing statistics about I/O on that specific index. The `pg_statio_user_indexes` and `pg_statio_sys_indexes` views contain the same information, but filtered to only show user and system indexes respectively.

#### **Table 27.26. `pg_statio_all_indexes` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>relid</code>  <code>oid</code>
        </p>
        <p>OID of the table for this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>indexrelid</code>  <code>oid</code>
        </p>
        <p>OID of this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>schemaname</code>  <code>name</code>
        </p>
        <p>Name of the schema this index is in</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relname</code>  <code>name</code>
        </p>
        <p>Name of the table for this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>indexrelname</code>  <code>name</code>
        </p>
        <p>Name of this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>idx_blks_read</code>  <code>bigint</code>
        </p>
        <p>Number of disk blocks read from this index</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>idx_blks_hit</code>  <code>bigint</code>
        </p>
        <p>Number of buffer hits in this index</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.17. `pg_statio_all_sequences`

The `pg_statio_all_sequences` view will contain one row for each sequence in the current database, showing statistics about I/O on that specific sequence.

#### **Table 27.27. `pg_statio_all_sequences` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>relid</code>  <code>oid</code>
        </p>
        <p>OID of a sequence</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>schemaname</code>  <code>name</code>
        </p>
        <p>Name of the schema this sequence is in</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>relname</code>  <code>name</code>
        </p>
        <p>Name of this sequence</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blks_read</code>  <code>bigint</code>
        </p>
        <p>Number of disk blocks read from this sequence</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blks_hit</code>  <code>bigint</code>
        </p>
        <p>Number of buffer hits in this sequence</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.18. `pg_stat_user_functions`

The `pg_stat_user_functions` view will contain one row for each tracked function, showing statistics about executions of that function. The [track\_functions](https://www.postgresql.org/docs/13/runtime-config-statistics.html#GUC-TRACK-FUNCTIONS) parameter controls exactly which functions are tracked.

#### **Table 27.28. `pg_stat_user_functions` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>funcid</code>  <code>oid</code>
        </p>
        <p>OID of a function</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>schemaname</code>  <code>name</code>
        </p>
        <p>Name of the schema this function is in</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>funcname</code>  <code>name</code>
        </p>
        <p>Name of this function</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>calls</code>  <code>bigint</code>
        </p>
        <p>Number of times this function has been called</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>total_time</code>  <code>double precision</code>
        </p>
        <p>Total time spent in this function and all other functions called by it,
          in milliseconds</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>self_time</code>  <code>double precision</code>
        </p>
        <p>Total time spent in this function itself, not including other functions
          called by it, in milliseconds</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.19. `pg_stat_slru`

PostgreSQL accesses certain on-disk information via _SLRU_ \(simple least-recently-used\) caches. The `pg_stat_slru` view will contain one row for each tracked SLRU cache, showing statistics about access to cached pages.

#### **Table 27.29. `pg_stat_slru` View**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>name</code>  <code>text</code>
        </p>
        <p>Name of the SLRU</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blks_zeroed</code>  <code>bigint</code>
        </p>
        <p>Number of blocks zeroed during initializations</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blks_hit</code>  <code>bigint</code>
        </p>
        <p>Number of times disk blocks were found already in the SLRU, so that a
          read was not necessary (this only includes hits in the SLRU, not the operating
          system&apos;s file system cache)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blks_read</code>  <code>bigint</code>
        </p>
        <p>Number of disk blocks read for this SLRU</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blks_written</code>  <code>bigint</code>
        </p>
        <p>Number of disk blocks written for this SLRU</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>blks_exists</code>  <code>bigint</code>
        </p>
        <p>Number of blocks checked for existence for this SLRU</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>flushes</code>  <code>bigint</code>
        </p>
        <p>Number of flushes of dirty data for this SLRU</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>truncates</code>  <code>bigint</code>
        </p>
        <p>Number of truncates for this SLRU</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>stats_reset</code>  <code>timestamp with time zone</code>
        </p>
        <p>Time at which these statistics were last reset</p>
      </td>
    </tr>
  </tbody>
</table>

## 27.2.20. Statistics Functions

Other ways of looking at the statistics can be set up by writing queries that use the same underlying statistics access functions used by the standard views shown above. For details such as the functions' names, consult the definitions of the standard views. \(For example, in psql you could issue `\d+ pg_stat_activity`.\) The access functions for per-database statistics take a database OID as an argument to identify which database to report on. The per-table and per-index functions take a table or index OID. The functions for per-function statistics take a function OID. Note that only tables, indexes, and functions in the current database can be seen with these functions.

Additional functions related to statistics collection are listed in [Table 27.30](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-STATS-FUNCS-TABLE).

#### **Table 27.30. Additional Statistics Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>pg_backend_pid</code> () &#x2192; <code>integer</code>
        </p>
        <p>Returns the process ID of the server process attached to the current session.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_activity</code> ( <code>integer</code> ) &#x2192; <code>setof record</code>
        </p>
        <p>Returns a record of information about the backend with the specified process
          ID, or one record for each active backend in the system if <code>NULL</code> is
          specified. The fields returned are a subset of those in the <code>pg_stat_activity</code> view.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_snapshot_timestamp</code> () &#x2192; <code>timestamp with time zone</code>
        </p>
        <p>Returns the timestamp of the current statistics snapshot.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_clear_snapshot</code> () &#x2192; <code>void</code>
        </p>
        <p>Discards the current statistics snapshot.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_reset</code> () &#x2192; <code>void</code>
        </p>
        <p>Resets all statistics counters for the current database to zero.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_reset_shared</code> ( <code>text</code> ) &#x2192; <code>void</code>
        </p>
        <p>Resets some cluster-wide statistics counters to zero, depending on the
          argument. The argument can be <code>bgwriter</code> to reset all the counters
          shown in the <code>pg_stat_bgwriter</code> view, or <code>archiver</code> to
          reset all the counters shown in the <code>pg_stat_archiver</code> view.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_reset_single_table_counters</code> ( <code>oid</code> ) &#x2192; <code>void</code>
        </p>
        <p>Resets statistics for a single table or index in the current database
          to zero.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_reset_single_function_counters</code> ( <code>oid</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Resets statistics for a single function in the current database to zero.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_reset_slru</code> ( <code>text</code> ) &#x2192; <code>void</code>
        </p>
        <p>Resets statistics to zero for a single SLRU cache, or for all SLRUs in
          the cluster. If the argument is NULL, all counters shown in the <code>pg_stat_slru</code> view
          for all SLRU caches are reset. The argument can be one of <code>CommitTs</code>, <code>MultiXactMember</code>, <code>MultiXactOffset</code>, <code>Notify</code>, <code>Serial</code>, <code>Subtrans</code>,
          or <code>Xact</code> to reset the counters for only that entry. If the argument
          is <code>other</code> (or indeed, any unrecognized name), then the counters
          for all other SLRU caches, such as extension-defined caches, are reset.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
  </tbody>
</table>

`pg_stat_get_activity`, the underlying function of the `pg_stat_activity` view, returns a set of records containing all the available information about each backend process. Sometimes it may be more convenient to obtain just a subset of this information. In such cases, an older set of per-backend statistics access functions can be used; these are shown in [Table 27.31](https://www.postgresql.org/docs/13/monitoring-stats.html#MONITORING-STATS-BACKEND-FUNCS-TABLE). These access functions use a backend ID number, which ranges from one to the number of currently active backends. The function `pg_stat_get_backend_idset` provides a convenient way to generate one row for each active backend for invoking these functions. For example, to show the PIDs and current queries of all backends:

```text
SELECT pg_stat_get_backend_pid(s.backendid) AS pid,
       pg_stat_get_backend_activity(s.backendid) AS query
    FROM (SELECT pg_stat_get_backend_idset() AS backendid) AS s;
```

#### **Table 27.31. Per-Backend Statistics Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_idset</code> () &#x2192; <code>setof integer</code>
        </p>
        <p>Returns the set of currently active backend ID numbers (from 1 to the
          number of active backends).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_activity</code> ( <code>integer</code> ) &#x2192; <code>text</code>
        </p>
        <p>Returns the text of this backend&apos;s most recent query.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_activity_start</code> ( <code>integer</code> )
          &#x2192; <code>timestamp with time zone</code>
        </p>
        <p>Returns the time when the backend&apos;s most recent query was started.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_client_addr</code> ( <code>integer</code> ) &#x2192; <code>inet</code>
        </p>
        <p>Returns the IP address of the client connected to this backend.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_client_port</code> ( <code>integer</code> ) &#x2192; <code>integer</code>
        </p>
        <p>Returns the TCP port number that the client is using for communication.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_dbid</code> ( <code>integer</code> ) &#x2192; <code>oid</code>
        </p>
        <p>Returns the OID of the database this backend is connected to.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_pid</code> ( <code>integer</code> ) &#x2192; <code>integer</code>
        </p>
        <p>Returns the process ID of this backend.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_start</code> ( <code>integer</code> ) &#x2192; <code>timestamp with time zone</code>
        </p>
        <p>Returns the time when this process was started.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_userid</code> ( <code>integer</code> ) &#x2192; <code>oid</code>
        </p>
        <p>Returns the OID of the user logged into this backend.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_wait_event_type</code> ( <code>integer</code> )
          &#x2192; <code>text</code>
        </p>
        <p>Returns the wait event type name if this backend is currently waiting,
          otherwise NULL. See <a href="https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-TABLE">Table 27.4</a> for
          details.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_wait_event</code> ( <code>integer</code> ) &#x2192; <code>text</code>
        </p>
        <p>Returns the wait event name if this backend is currently waiting, otherwise
          NULL. See <a href="https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-ACTIVITY-TABLE">Table 27.5</a> through
          <a
          href="https://www.postgresql.org/docs/13/monitoring-stats.html#WAIT-EVENT-TIMEOUT-TABLE">Table 27.13</a>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_get_backend_xact_start</code> ( <code>integer</code> ) &#x2192; <code>timestamp with time zone</code>
        </p>
        <p>Returns the time when the backend&apos;s current transaction was started.</p>
      </td>
    </tr>
  </tbody>
</table>

