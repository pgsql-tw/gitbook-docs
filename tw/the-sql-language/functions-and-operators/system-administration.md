# 9.27. 系統管理函式

The functions described in this section are used to control and monitor a PostgreSQL installation.

## 9.27.1. Configuration Settings Functions

[Table 9.83](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-SET-TABLE) shows the functions available to query and alter run-time configuration parameters.

#### **Table 9.83. Configuration Settings Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
        <p>Example(s)</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>current_setting</code> ( <em><code>setting_name</code></em>  <code>text</code> [, <em><code>missing_ok</code></em>  <code>boolean</code> ]
          ) &#x2192; <code>text</code>
        </p>
        <p>Returns the current value of the setting <em><code>setting_name</code></em>.
          If there is no such setting, <code>current_setting</code> throws an error
          unless <em><code>missing_ok</code></em> is supplied and is <code>true</code>.
          This function corresponds to the SQL command <code>SHOW</code>.</p>
        <p><code>current_setting(&apos;datestyle&apos;)</code> &#x2192; <code>ISO, MDY</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>set_config</code> ( <em><code>setting_name</code></em>  <code>text</code>, <em><code>new_value</code></em>  <code>text</code>, <em><code>is_local</code></em>  <code>boolean</code> )
          &#x2192; <code>text</code>
        </p>
        <p>Sets the parameter <em><code>setting_name</code></em> to <em><code>new_value</code></em>,
          and returns that value. If <em><code>is_local</code></em> is <code>true</code>,
          the new value will only apply for the current transaction. If you want
          the new value to apply for the current session, use <code>false</code> instead.
          This function corresponds to the SQL command <code>SET</code>.</p>
        <p><code>set_config(&apos;log_statement_stats&apos;, &apos;off&apos;, false)</code> &#x2192; <code>off</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

## 9.27.2. Server Signaling Functions

The functions shown in [Table 9.84](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL-TABLE) send control signals to other server processes. Use of these functions is restricted to superusers by default but access may be granted to others using `GRANT`, with noted exceptions.

Each of these functions returns `true` if successful and `false` otherwise.

#### **Table 9.84. Server Signaling Functions**

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
        <p><code>pg_cancel_backend</code> ( <em><code>pid</code></em>  <code>integer</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p>Cancels the current query of the session whose backend process has the
          specified process ID. This is also allowed if the calling role is a member
          of the role whose backend is being canceled or the calling role has been
          granted <code>pg_signal_backend</code>, however only superusers can cancel
          superuser backends.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_reload_conf</code> () &#x2192; <code>boolean</code>
        </p>
        <p>Causes all processes of the PostgreSQL server to reload their configuration
          files. (This is initiated by sending a SIGHUP signal to the postmaster
          process, which in turn sends SIGHUP to each of its children.)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_rotate_logfile</code> () &#x2192; <code>boolean</code>
        </p>
        <p>Signals the log-file manager to switch to a new output file immediately.
          This works only when the built-in log collector is running, since otherwise
          there is no log-file manager subprocess.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_terminate_backend</code> ( <em><code>pid</code></em>  <code>integer</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p>Terminates the session whose backend process has the specified process
          ID. This is also allowed if the calling role is a member of the role whose
          backend is being terminated or the calling role has been granted <code>pg_signal_backend</code>,
          however only superusers can terminate superuser backends.</p>
      </td>
    </tr>
  </tbody>
</table>

`pg_cancel_backend` and `pg_terminate_backend` send signals \(SIGINT or SIGTERM respectively\) to backend processes identified by process ID. The process ID of an active backend can be found from the `pid` column of the `pg_stat_activity` view, or by listing the `postgres` processes on the server \(using ps on Unix or the Task Manager on Windows\). The role of an active backend can be found from the `usename` column of the `pg_stat_activity` view.

## 9.27.3. Backup Control Functions

The functions shown in [Table 9.85](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-BACKUP-TABLE) assist in making on-line backups. These functions cannot be executed during recovery \(except non-exclusive `pg_start_backup`, non-exclusive `pg_stop_backup`, `pg_is_in_backup`, `pg_backup_start_time` and `pg_wal_lsn_diff`\).

For details about proper usage of these functions, see [Section 25.3](https://www.postgresql.org/docs/13/continuous-archiving.html).

#### **Table 9.85. Backup Control Functions**

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
        <p><code>pg_create_restore_point</code> ( <em><code>name</code></em>  <code>text</code> )
          &#x2192; <code>pg_lsn</code>
        </p>
        <p>Creates a named marker record in the write-ahead log that can later be
          used as a recovery target, and returns the corresponding write-ahead log
          location. The given name can then be used with <a href="https://www.postgresql.org/docs/13/runtime-config-wal.html#GUC-RECOVERY-TARGET-NAME">recovery_target_name</a> to
          specify the point up to which recovery will proceed. Avoid creating multiple
          restore points with the same name, since recovery will stop at the first
          one whose name matches the recovery target.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_current_wal_flush_lsn</code> () &#x2192; <code>pg_lsn</code>
        </p>
        <p>Returns the current write-ahead log flush location (see notes below).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_current_wal_insert_lsn</code> () &#x2192; <code>pg_lsn</code>
        </p>
        <p>Returns the current write-ahead log insert location (see notes below).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_current_wal_lsn</code> () &#x2192; <code>pg_lsn</code>
        </p>
        <p>Returns the current write-ahead log write location (see notes below).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_start_backup</code> ( <em><code>label</code></em>  <code>text</code> [, <em><code>fast</code></em>  <code>boolean</code> [, <em><code>exclusive</code></em>  <code>boolean</code> ]]
          ) &#x2192; <code>pg_lsn</code>
        </p>
        <p>Prepares the server to begin an on-line backup. The only required parameter
          is an arbitrary user-defined label for the backup. (Typically this would
          be the name under which the backup dump file will be stored.) If the optional
          second parameter is given as <code>true</code>, it specifies executing <code>pg_start_backup</code> as
          quickly as possible. This forces an immediate checkpoint which will cause
          a spike in I/O operations, slowing any concurrently executing queries.
          The optional third parameter specifies whether to perform an exclusive
          or non-exclusive backup (default is exclusive).</p>
        <p>When used in exclusive mode, this function writes a backup label file
          (<code>backup_label</code>) and, if there are any links in the <code>pg_tblspc/</code> directory,
          a tablespace map file (<code>tablespace_map</code>) into the database cluster&apos;s
          data directory, then performs a checkpoint, and then returns the backup&apos;s
          starting write-ahead log location. (The user can ignore this result value,
          but it is provided in case it is useful.) When used in non-exclusive mode,
          the contents of these files are instead returned by the <code>pg_stop_backup</code> function,
          and should be copied to the backup area by the user.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stop_backup</code> ( <em><code>exclusive</code></em>  <code>boolean</code> [, <em><code>wait_for_archive</code></em>  <code>boolean</code> ]
          ) &#x2192; <code>setof record</code> ( <em><code>lsn</code></em>  <code>pg_lsn</code>, <em><code>labelfile</code></em>  <code>text</code>, <em><code>spcmapfile</code></em>  <code>text</code> )</p>
        <p>Finishes performing an exclusive or non-exclusive on-line backup. The <em><code>exclusive</code></em> parameter
          must match the previous <code>pg_start_backup</code> call. In an exclusive
          backup, <code>pg_stop_backup</code> removes the backup label file and, if
          it exists, the tablespace map file created by <code>pg_start_backup</code>.
          In a non-exclusive backup, the desired contents of these files are returned
          as part of the result of the function, and should be written to files in
          the backup area (not in the data directory).</p>
        <p>There is an optional second parameter of type <code>boolean</code>. If
          false, the function will return immediately after the backup is completed,
          without waiting for WAL to be archived. This behavior is only useful with
          backup software that independently monitors WAL archiving. Otherwise, WAL
          required to make the backup consistent might be missing and make the backup
          useless. By default or when this parameter is true, <code>pg_stop_backup</code> will
          wait for WAL to be archived when archiving is enabled. (On a standby, this
          means that it will wait only when <code>archive_mode</code> = <code>always</code>.
          If write activity on the primary is low, it may be useful to run <code>pg_switch_wal</code> on
          the primary in order to trigger an immediate segment switch.)</p>
        <p>When executed on a primary, this function also creates a backup history
          file in the write-ahead log archive area. The history file includes the
          label given to <code>pg_start_backup</code>, the starting and ending write-ahead
          log locations for the backup, and the starting and ending times of the
          backup. After recording the ending location, the current write-ahead log
          insertion point is automatically advanced to the next write-ahead log file,
          so that the ending write-ahead log file can be archived immediately to
          complete the backup.</p>
        <p>The result of the function is a single record. The <em><code>lsn</code></em> column
          holds the backup&apos;s ending write-ahead log location (which again can
          be ignored). The second and third columns are <code>NULL</code> when ending
          an exclusive backup; after a non-exclusive backup they hold the desired
          contents of the label and tablespace map files.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stop_backup</code> () &#x2192; <code>pg_lsn</code>
        </p>
        <p>Finishes performing an exclusive on-line backup. This simplified version
          is equivalent to <code>pg_stop_backup(true, true)</code>, except that it
          only returns the <code>pg_lsn</code> result.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_is_in_backup</code> () &#x2192; <code>boolean</code>
        </p>
        <p>Returns true if an on-line exclusive backup is in progress.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_backup_start_time</code> () &#x2192; <code>timestamp with time zone</code>
        </p>
        <p>Returns the start time of the current on-line exclusive backup if one
          is in progress, otherwise <code>NULL</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_switch_wal</code> () &#x2192; <code>pg_lsn</code>
        </p>
        <p>Forces the server to switch to a new write-ahead log file, which allows
          the current file to be archived (assuming you are using continuous archiving).
          The result is the ending write-ahead log location plus 1 within the just-completed
          write-ahead log file. If there has been no write-ahead log activity since
          the last write-ahead log switch, <code>pg_switch_wal</code> does nothing
          and returns the start location of the write-ahead log file currently in
          use.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_walfile_name</code> ( <em><code>lsn</code></em>  <code>pg_lsn</code> )
          &#x2192; <code>text</code>
        </p>
        <p>Converts a write-ahead log location to the name of the WAL file holding
          that location.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_walfile_name_offset</code> ( <em><code>lsn</code></em>  <code>pg_lsn</code> )
          &#x2192; <code>record</code> ( <em><code>file_name</code></em>  <code>text</code>, <em><code>file_offset</code></em>  <code>integer</code> )</p>
        <p>Converts a write-ahead log location to a WAL file name and byte offset
          within that file.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_wal_lsn_diff</code> ( <em><code>lsn</code></em>  <code>pg_lsn</code>, <em><code>lsn</code></em>  <code>pg_lsn</code> )
          &#x2192; <code>numeric</code>
        </p>
        <p>Calculates the difference in bytes between two write-ahead log locations.
          This can be used with <code>pg_stat_replication</code> or some of the functions
          shown in <a href="https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-BACKUP-TABLE">Table 9.85</a> to
          get the replication lag.</p>
      </td>
    </tr>
  </tbody>
</table>

`pg_current_wal_lsn` displays the current write-ahead log write location in the same format used by the above functions. Similarly, `pg_current_wal_insert_lsn` displays the current write-ahead log insertion location and `pg_current_wal_flush_lsn` displays the current write-ahead log flush location. The insertion location is the “logical” end of the write-ahead log at any instant, while the write location is the end of what has actually been written out from the server's internal buffers, and the flush location is the last location known to be written to durable storage. The write location is the end of what can be examined from outside the server, and is usually what you want if you are interested in archiving partially-complete write-ahead log files. The insertion and flush locations are made available primarily for server debugging purposes. These are all read-only operations and do not require superuser permissions.

You can use `pg_walfile_name_offset` to extract the corresponding write-ahead log file name and byte offset from a `pg_lsn` value. For example:

```text
postgres=# SELECT * FROM pg_walfile_name_offset(pg_stop_backup());
        file_name         | file_offset
--------------------------+-------------
 00000001000000000000000D |     4039624
(1 row)
```

Similarly, `pg_walfile_name` extracts just the write-ahead log file name. When the given write-ahead log location is exactly at a write-ahead log file boundary, both these functions return the name of the preceding write-ahead log file. This is usually the desired behavior for managing write-ahead log archiving behavior, since the preceding file is the last one that currently needs to be archived.

## 9.27.4. Recovery Control Functions

The functions shown in [Table 9.86](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-RECOVERY-INFO-TABLE) provide information about the current status of a standby server. These functions may be executed both during recovery and in normal running.

#### **Table 9.86. Recovery Information Functions**

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
        <p><code>pg_is_in_recovery</code> () &#x2192; <code>boolean</code>
        </p>
        <p>Returns true if recovery is still in progress.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_last_wal_receive_lsn</code> () &#x2192; <code>pg_lsn</code>
        </p>
        <p>Returns the last write-ahead log location that has been received and synced
          to disk by streaming replication. While streaming replication is in progress
          this will increase monotonically. If recovery has completed then this will
          remain static at the location of the last WAL record received and synced
          to disk during recovery. If streaming replication is disabled, or if it
          has not yet started, the function returns <code>NULL</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_last_wal_replay_lsn</code> () &#x2192; <code>pg_lsn</code>
        </p>
        <p>Returns the last write-ahead log location that has been replayed during
          recovery. If recovery is still in progress this will increase monotonically.
          If recovery has completed then this will remain static at the location
          of the last WAL record applied during recovery. When the server has been
          started normally without recovery, the function returns <code>NULL</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_last_xact_replay_timestamp</code> () &#x2192; <code>timestamp with time zone</code>
        </p>
        <p>Returns the time stamp of the last transaction replayed during recovery.
          This is the time at which the commit or abort WAL record for that transaction
          was generated on the primary. If no transactions have been replayed during
          recovery, the function returns <code>NULL</code>. Otherwise, if recovery
          is still in progress this will increase monotonically. If recovery has
          completed then this will remain static at the time of the last transaction
          applied during recovery. When the server has been started normally without
          recovery, the function returns <code>NULL</code>.</p>
      </td>
    </tr>
  </tbody>
</table>

The functions shown in [Table 9.87](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL-TABLE) control the progress of recovery. These functions may be executed only during recovery.

#### **Table 9.87. Recovery Control Functions**

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
        <p><code>pg_is_wal_replay_paused</code> () &#x2192; <code>boolean</code>
        </p>
        <p>Returns true if recovery is paused.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_promote</code> ( <em><code>wait</code></em>  <code>boolean</code>  <code>DEFAULT</code>  <code>true</code>, <em><code>wait_seconds</code></em>  <code>integer</code>  <code>DEFAULT</code>  <code>60</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p>Promotes a standby server to primary status. With <em><code>wait</code></em> set
          to <code>true</code> (the default), the function waits until promotion is
          completed or <em><code>wait_seconds</code></em> seconds have passed, and
          returns <code>true</code> if promotion is successful and <code>false</code> otherwise.
          If <em><code>wait</code></em> is set to <code>false</code>, the function returns <code>true</code> immediately
          after sending a <code>SIGUSR1</code> signal to the postmaster to trigger
          promotion.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_wal_replay_pause</code> () &#x2192; <code>void</code>
        </p>
        <p>Pauses recovery. While recovery is paused, no further database changes
          are applied. If hot standby is active, all new queries will see the same
          consistent snapshot of the database, and no further query conflicts will
          be generated until recovery is resumed.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_wal_replay_resume</code> () &#x2192; <code>void</code>
        </p>
        <p>Restarts recovery if it was paused.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
  </tbody>
</table>

`pg_wal_replay_pause` and `pg_wal_replay_resume` cannot be executed while a promotion is ongoing. If a promotion is triggered while recovery is paused, the paused state ends and promotion continues.

If streaming replication is disabled, the paused state may continue indefinitely without a problem. If streaming replication is in progress then WAL records will continue to be received, which will eventually fill available disk space, depending upon the duration of the pause, the rate of WAL generation and available disk space.

## 9.27.5. Snapshot Synchronization Functions

PostgreSQL allows database sessions to synchronize their snapshots. A _snapshot_ determines which data is visible to the transaction that is using the snapshot. Synchronized snapshots are necessary when two or more sessions need to see identical content in the database. If two sessions just start their transactions independently, there is always a possibility that some third transaction commits between the executions of the two `START TRANSACTION` commands, so that one session sees the effects of that transaction and the other does not.

To solve this problem, PostgreSQL allows a transaction to _export_ the snapshot it is using. As long as the exporting transaction remains open, other transactions can _import_ its snapshot, and thereby be guaranteed that they see exactly the same view of the database that the first transaction sees. But note that any database changes made by any one of these transactions remain invisible to the other transactions, as is usual for changes made by uncommitted transactions. So the transactions are synchronized with respect to pre-existing data, but act normally for changes they make themselves.

Snapshots are exported with the `pg_export_snapshot` function, shown in [Table 9.88](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION-TABLE), and imported with the [SET TRANSACTION](https://www.postgresql.org/docs/13/sql-set-transaction.html) command.

#### **Table 9.88. Snapshot Synchronization Functions**

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
        <p><code>pg_export_snapshot</code> () &#x2192; <code>text</code>
        </p>
        <p>Saves the transaction&apos;s current snapshot and returns a <code>text</code> string
          identifying the snapshot. This string must be passed (outside the database)
          to clients that want to import the snapshot. The snapshot is available
          for import only until the end of the transaction that exported it.</p>
        <p>A transaction can export more than one snapshot, if needed. Note that
          doing so is only useful in <code>READ COMMITTED</code> transactions, since
          in <code>REPEATABLE READ</code> and higher isolation levels, transactions
          use the same snapshot throughout their lifetime. Once a transaction has
          exported any snapshots, it cannot be prepared with <a href="https://www.postgresql.org/docs/13/sql-prepare-transaction.html">PREPARE TRANSACTION</a>.</p>
      </td>
    </tr>
  </tbody>
</table>

## 9.27.6. Replication Management Functions

The functions shown in [Table 9.89](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-REPLICATION-TABLE) are for controlling and interacting with replication features. See [Section 26.2.5](https://www.postgresql.org/docs/13/warm-standby.html#STREAMING-REPLICATION), [Section 26.2.6](https://www.postgresql.org/docs/13/warm-standby.html#STREAMING-REPLICATION-SLOTS), and [Chapter 49](https://www.postgresql.org/docs/13/replication-origins.html) for information about the underlying features. Use of functions for replication origin is restricted to superusers. Use of functions for replication slots is restricted to superusers and users having `REPLICATION` privilege.

Many of these functions have equivalent commands in the replication protocol; see [Section 52.4](https://www.postgresql.org/docs/13/protocol-replication.html).

The functions described in [Section 9.27.3](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-BACKUP), [Section 9.27.4](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL), and [Section 9.27.5](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION) are also relevant for replication.

#### **Table 9.89. Replication Management Functions**

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
        <p><code>pg_create_physical_replication_slot</code> ( <em><code>slot_name</code></em>  <code>name</code> [, <em><code>immediately_reserve</code></em>  <code>boolean</code>, <em><code>temporary</code></em>  <code>boolean</code> ]
          ) &#x2192; <code>record</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>lsn</code></em>  <code>pg_lsn</code> )</p>
        <p>Creates a new physical replication slot named <em><code>slot_name</code></em>.
          The optional second parameter, when <code>true</code>, specifies that the
          LSN for this replication slot be reserved immediately; otherwise the LSN
          is reserved on first connection from a streaming replication client. Streaming
          changes from a physical slot is only possible with the streaming-replication
          protocol &#x2014; see <a href="https://www.postgresql.org/docs/13/protocol-replication.html">Section 52.4</a>.
          The optional third parameter, <em><code>temporary</code></em>, when set
          to true, specifies that the slot should not be permanently stored to disk
          and is only meant for use by the current session. Temporary slots are also
          released upon any error. This function corresponds to the replication protocol
          command <code>CREATE_REPLICATION_SLOT ... PHYSICAL</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_drop_replication_slot</code> ( <em><code>slot_name</code></em>  <code>name</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Drops the physical or logical replication slot named <em><code>slot_name</code></em>.
          Same as replication protocol command <code>DROP_REPLICATION_SLOT</code>.
          For logical slots, this must be called while connected to the same database
          the slot was created on.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_create_logical_replication_slot</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>plugin</code></em>  <code>name</code> [, <em><code>temporary</code></em>  <code>boolean</code> ]
          ) &#x2192; <code>record</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>lsn</code></em>  <code>pg_lsn</code> )</p>
        <p>Creates a new logical (decoding) replication slot named <em><code>slot_name</code></em> using
          the output plugin <em><code>plugin</code></em>. The optional third parameter, <em><code>temporary</code></em>,
          when set to true, specifies that the slot should not be permanently stored
          to disk and is only meant for use by the current session. Temporary slots
          are also released upon any error. A call to this function has the same
          effect as the replication protocol command <code>CREATE_REPLICATION_SLOT ... LOGICAL</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_copy_physical_replication_slot</code> ( <em><code>src_slot_name</code></em>  <code>name</code>, <em><code>dst_slot_name</code></em>  <code>name</code> [, <em><code>temporary</code></em>  <code>boolean</code> ]
          ) &#x2192; <code>record</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>lsn</code></em>  <code>pg_lsn</code> )</p>
        <p>Copies an existing physical replication slot named <em><code>src_slot_name</code></em> to
          a physical replication slot named <em><code>dst_slot_name</code></em>. The
          copied physical slot starts to reserve WAL from the same LSN as the source
          slot. <em><code>temporary</code></em> is optional. If <em><code>temporary</code></em> is
          omitted, the same value as the source slot is used.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_copy_logical_replication_slot</code> ( <em><code>src_slot_name</code></em>  <code>name</code>, <em><code>dst_slot_name</code></em>  <code>name</code> [, <em><code>temporary</code></em>  <code>boolean</code> [, <em><code>plugin</code></em>  <code>name</code> ]]
          ) &#x2192; <code>record</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>lsn</code></em>  <code>pg_lsn</code> )</p>
        <p>Copies an existing logical replication slot named <em><code>src_slot_name</code></em> to
          a logical replication slot named <em><code>dst_slot_name</code></em>, optionally
          changing the output plugin and persistence. The copied logical slot starts
          from the same LSN as the source logical slot. Both <em><code>temporary</code></em> and <em><code>plugin</code></em> are
          optional; if they are omitted, the values of the source slot are used.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_logical_slot_get_changes</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>upto_lsn</code></em>  <code>pg_lsn</code>, <em><code>upto_nchanges</code></em>  <code>integer</code>, <code>VARIADIC</code>  <em><code>options</code></em>  <code>text[]</code> )
          &#x2192; <code>setof record</code> ( <em><code>lsn</code></em>  <code>pg_lsn</code>, <em><code>xid</code></em>  <code>xid</code>, <em><code>data</code></em>  <code>text</code> )</p>
        <p>Returns changes in the slot <em><code>slot_name</code></em>, starting from
          the point from which changes have been consumed last. If <em><code>upto_lsn</code></em> and <em><code>upto_nchanges</code></em> are
          NULL, logical decoding will continue until end of WAL. If <em><code>upto_lsn</code></em> is
          non-NULL, decoding will include only those transactions which commit prior
          to the specified LSN. If <em><code>upto_nchanges</code></em> is non-NULL,
          decoding will stop when the number of rows produced by decoding exceeds
          the specified value. Note, however, that the actual number of rows returned
          may be larger, since this limit is only checked after adding the rows produced
          when decoding each new transaction commit.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_logical_slot_peek_changes</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>upto_lsn</code></em>  <code>pg_lsn</code>, <em><code>upto_nchanges</code></em>  <code>integer</code>, <code>VARIADIC</code>  <em><code>options</code></em>  <code>text[]</code> )
          &#x2192; <code>setof record</code> ( <em><code>lsn</code></em>  <code>pg_lsn</code>, <em><code>xid</code></em>  <code>xid</code>, <em><code>data</code></em>  <code>text</code> )</p>
        <p>Behaves just like the <code>pg_logical_slot_get_changes()</code> function,
          except that changes are not consumed; that is, they will be returned again
          on future calls.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_logical_slot_get_binary_changes</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>upto_lsn</code></em>  <code>pg_lsn</code>, <em><code>upto_nchanges</code></em>  <code>integer</code>, <code>VARIADIC</code>  <em><code>options</code></em>  <code>text[]</code> )
          &#x2192; <code>setof record</code> ( <em><code>lsn</code></em>  <code>pg_lsn</code>, <em><code>xid</code></em>  <code>xid</code>, <em><code>data</code></em>  <code>bytea</code> )</p>
        <p>Behaves just like the <code>pg_logical_slot_get_changes()</code> function,
          except that changes are returned as <code>bytea</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_logical_slot_peek_binary_changes</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>upto_lsn</code></em>  <code>pg_lsn</code>, <em><code>upto_nchanges</code></em>  <code>integer</code>, <code>VARIADIC</code>  <em><code>options</code></em>  <code>text[]</code> )
          &#x2192; <code>setof record</code> ( <em><code>lsn</code></em>  <code>pg_lsn</code>, <em><code>xid</code></em>  <code>xid</code>, <em><code>data</code></em>  <code>bytea</code> )</p>
        <p>Behaves just like the <code>pg_logical_slot_peek_changes()</code> function,
          except that changes are returned as <code>bytea</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_slot_advance</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>upto_lsn</code></em>  <code>pg_lsn</code> )
          &#x2192; <code>record</code> ( <em><code>slot_name</code></em>  <code>name</code>, <em><code>end_lsn</code></em>  <code>pg_lsn</code> )</p>
        <p>Advances the current confirmed position of a replication slot named <em><code>slot_name</code></em>.
          The slot will not be moved backwards, and it will not be moved beyond the
          current insert location. Returns the name of the slot and the actual position
          that it was advanced to. The updated slot position information is written
          out at the next checkpoint if any advancing is done. So in the event of
          a crash, the slot may return to an earlier position.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_create</code> ( <em><code>node_name</code></em>  <code>text</code> )
          &#x2192; <code>oid</code>
        </p>
        <p>Creates a replication origin with the given external name, and returns
          the internal ID assigned to it.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_drop</code> ( <em><code>node_name</code></em>  <code>text</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Deletes a previously-created replication origin, including any associated
          replay progress.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_oid</code> ( <em><code>node_name</code></em>  <code>text</code> )
          &#x2192; <code>oid</code>
        </p>
        <p>Looks up a replication origin by name and returns the internal ID. If
          no such replication origin is found an error is thrown.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_session_setup</code> ( <em><code>node_name</code></em>  <code>text</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Marks the current session as replaying from the given origin, allowing
          replay progress to be tracked. Can only be used if no origin is currently
          selected. Use <code>pg_replication_origin_session_reset</code> to undo.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_session_reset</code> () &#x2192; <code>void</code>
        </p>
        <p>Cancels the effects of <code>pg_replication_origin_session_setup()</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_session_is_setup</code> () &#x2192; <code>boolean</code>
        </p>
        <p>Returns true if a replication origin has been selected in the current
          session.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_session_progress</code> ( <em><code>flush</code></em>  <code>boolean</code> )
          &#x2192; <code>pg_lsn</code>
        </p>
        <p>Returns the replay location for the replication origin selected in the
          current session. The parameter <em><code>flush</code></em> determines whether
          the corresponding local transaction will be guaranteed to have been flushed
          to disk or not.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_xact_setup</code> ( <em><code>origin_lsn</code></em>  <code>pg_lsn</code>, <em><code>origin_timestamp</code></em>  <code>timestamp with time zone</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Marks the current transaction as replaying a transaction that has committed
          at the given LSN and timestamp. Can only be called when a replication origin
          has been selected using <code>pg_replication_origin_session_setup</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_xact_reset</code> () &#x2192; <code>void</code>
        </p>
        <p>Cancels the effects of <code>pg_replication_origin_xact_setup()</code>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_advance</code> ( <em><code>node_name</code></em>  <code>text</code>, <em><code>lsn</code></em>  <code>pg_lsn</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Sets replication progress for the given node to the given location. This
          is primarily useful for setting up the initial location, or setting a new
          location after configuration changes and similar. Be aware that careless
          use of this function can lead to inconsistently replicated data.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_replication_origin_progress</code> ( <em><code>node_name</code></em>  <code>text</code>, <em><code>flush</code></em>  <code>boolean</code> )
          &#x2192; <code>pg_lsn</code>
        </p>
        <p>Returns the replay location for the given replication origin. The parameter <em><code>flush</code></em> determines
          whether the corresponding local transaction will be guaranteed to have
          been flushed to disk or not.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_logical_emit_message</code> ( <em><code>transactional</code></em>  <code>boolean</code>, <em><code>prefix</code></em>  <code>text</code>, <em><code>content</code></em>  <code>text</code> )
          &#x2192; <code>pg_lsn</code>
        </p>
        <p><code>pg_logical_emit_message</code> ( <em><code>transactional</code></em>  <code>boolean</code>, <em><code>prefix</code></em>  <code>text</code>, <em><code>content</code></em>  <code>bytea</code> )
          &#x2192; <code>pg_lsn</code>
        </p>
        <p>Emits a logical decoding message. This can be used to pass generic messages
          to logical decoding plugins through WAL. The <em><code>transactional</code></em> parameter
          specifies if the message should be part of the current transaction, or
          if it should be written immediately and decoded as soon as the logical
          decoder reads the record. The <em><code>prefix</code></em> parameter is a
          textual prefix that can be used by logical decoding plugins to easily recognize
          messages that are interesting for them. The <em><code>content</code></em> parameter
          is the content of the message, given either in text or binary form.</p>
      </td>
    </tr>
  </tbody>
</table>

## 9.27.7. Database Object Management Functions

The functions shown in [Table 9.90](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-DBSIZE) calculate the disk space usage of database objects, or assist in presentation of usage results. All these functions return sizes measured in bytes. If an OID that does not represent an existing object is passed to one of these functions, `NULL` is returned.

#### **Table 9.90. Database Object Size Functions**

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
        <p><code>pg_column_size</code> ( <code>&quot;any&quot;</code> ) &#x2192; <code>integer</code>
        </p>
        <p>Shows the number of bytes used to store any individual data value. If
          applied directly to a table column value, this reflects any compression
          that was done.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_database_size</code> ( <code>name</code> ) &#x2192; <code>bigint</code>
        </p>
        <p><code>pg_database_size</code> ( <code>oid</code> ) &#x2192; <code>bigint</code>
        </p>
        <p>Computes the total disk space used by the database with the specified
          name or OID. To use this function, you must have <code>CONNECT</code> privilege
          on the specified database (which is granted by default) or be a member
          of the <code>pg_read_all_stats</code> role.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_indexes_size</code> ( <code>regclass</code> ) &#x2192; <code>bigint</code>
        </p>
        <p>Computes the total disk space used by indexes attached to the specified
          table.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_relation_size</code> ( <em><code>relation</code></em>  <code>regclass</code> [, <em><code>fork</code></em>  <code>text</code> ]
          ) &#x2192; <code>bigint</code>
        </p>
        <p>Computes the disk space used by one &#x201C;fork&#x201D; of the specified
          relation. (Note that for most purposes it is more convenient to use the
          higher-level functions <code>pg_total_relation_size</code> or <code>pg_table_size</code>,
          which sum the sizes of all forks.) With one argument, this returns the
          size of the main data fork of the relation. The second argument can be
          provided to specify which fork to examine:</p>
        <ul>
          <li><code>main</code> returns the size of the main data fork of the relation.</li>
          <li><code>fsm</code> returns the size of the Free Space Map (see <a href="https://www.postgresql.org/docs/13/storage-fsm.html">Section 68.3</a>)
            associated with the relation.</li>
          <li><code>vm</code> returns the size of the Visibility Map (see <a href="https://www.postgresql.org/docs/13/storage-vm.html">Section 68.4</a>)
            associated with the relation.</li>
          <li><code>init</code> returns the size of the initialization fork, if any,
            associated with the relation.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_size_bytes</code> ( <code>text</code> ) &#x2192; <code>bigint</code>
        </p>
        <p>Converts a size in human-readable format (as returned by <code>pg_size_pretty</code>)
          into bytes.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_size_pretty</code> ( <code>bigint</code> ) &#x2192; <code>text</code>
        </p>
        <p><code>pg_size_pretty</code> ( <code>numeric</code> ) &#x2192; <code>text</code>
        </p>
        <p>Converts a size in bytes into a more easily human-readable format with
          size units (bytes, kB, MB, GB or TB as appropriate). Note that the units
          are powers of 2 rather than powers of 10, so 1kB is 1024 bytes, 1MB is
          10242 = 1048576 bytes, and so on.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_table_size</code> ( <code>regclass</code> ) &#x2192; <code>bigint</code>
        </p>
        <p>Computes the disk space used by the specified table, excluding indexes
          (but including its TOAST table if any, free space map, and visibility map).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_tablespace_size</code> ( <code>name</code> ) &#x2192; <code>bigint</code>
        </p>
        <p><code>pg_tablespace_size</code> ( <code>oid</code> ) &#x2192; <code>bigint</code>
        </p>
        <p>Computes the total disk space used in the tablespace with the specified
          name or OID. To use this function, you must have <code>CREATE</code> privilege
          on the specified tablespace or be a member of the <code>pg_read_all_stats</code> role,
          unless it is the default tablespace for the current database.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_total_relation_size</code> ( <code>regclass</code> ) &#x2192; <code>bigint</code>
        </p>
        <p>Computes the total disk space used by the specified table, including all
          indexes and TOAST data. The result is equivalent to <code>pg_table_size</code>  <code>+</code>  <code>pg_indexes_size</code>.</p>
      </td>
    </tr>
  </tbody>
</table>

The functions above that operate on tables or indexes accept a `regclass` argument, which is simply the OID of the table or index in the `pg_class` system catalog. You do not have to look up the OID by hand, however, since the `regclass` data type's input converter will do the work for you. Just write the table name enclosed in single quotes so that it looks like a literal constant. For compatibility with the handling of ordinary SQL names, the string will be converted to lower case unless it contains double quotes around the table name.

The functions shown in [Table 9.91](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-DBLOCATION) assist in identifying the specific disk files associated with database objects.

## **Table 9.91. Database Object Location Functions**

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
        <p><code>pg_relation_filenode</code> ( <em><code>relation</code></em>  <code>regclass</code> )
          &#x2192; <code>oid</code>
        </p>
        <p>Returns the &#x201C;filenode&#x201D; number currently assigned to the
          specified relation. The filenode is the base component of the file name(s)
          used for the relation (see <a href="https://www.postgresql.org/docs/13/storage-file-layout.html">Section 68.1</a> for
          more information). For most relations the result is the same as <code>pg_class</code>.<code>relfilenode</code>,
          but for certain system catalogs <code>relfilenode</code> is zero and this
          function must be used to get the correct value. The function returns NULL
          if passed a relation that does not have storage, such as a view.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_relation_filepath</code> ( <em><code>relation</code></em>  <code>regclass</code> )
          &#x2192; <code>text</code>
        </p>
        <p>Returns the entire file path name (relative to the database cluster&apos;s
          data directory, <code>PGDATA</code>) of the relation.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_filenode_relation</code> ( <em><code>tablespace</code></em>  <code>oid</code>, <em><code>filenode</code></em>  <code>oid</code> )
          &#x2192; <code>regclass</code>
        </p>
        <p>Returns a relation&apos;s OID given the tablespace OID and filenode it
          is stored under. This is essentially the inverse mapping of <code>pg_relation_filepath</code>.
          For a relation in the database&apos;s default tablespace, the tablespace
          can be specified as zero. Returns <code>NULL</code> if no relation in the
          current database is associated with the given values.</p>
      </td>
    </tr>
  </tbody>
</table>

[Table 9.92](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-COLLATION) lists functions used to manage collations.

#### **Table 9.92. Collation Management Functions**

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
        <p><code>pg_collation_actual_version</code> ( <code>oid</code> ) &#x2192; <code>text</code>
        </p>
        <p>Returns the actual version of the collation object as it is currently
          installed in the operating system. If this is different from the value
          in <code>pg_collation</code>.<code>collversion</code>, then objects depending
          on the collation might need to be rebuilt. See also <a href="https://www.postgresql.org/docs/13/sql-altercollation.html">ALTER COLLATION</a>.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_import_system_collations</code> ( <em><code>schema</code></em>  <code>regnamespace</code> )
          &#x2192; <code>integer</code>
        </p>
        <p>Adds collations to the system catalog <code>pg_collation</code> based on
          all the locales it finds in the operating system. This is what <code>initdb</code> uses;
          see <a href="https://www.postgresql.org/docs/13/collation.html#COLLATION-MANAGING">Section 23.2.2</a> for
          more details. If additional locales are installed into the operating system
          later on, this function can be run again to add collations for the new
          locales. Locales that match existing entries in <code>pg_collation</code> will
          be skipped. (But collation objects based on locales that are no longer
          present in the operating system are not removed by this function.) The <em><code>schema</code></em> parameter
          would typically be <code>pg_catalog</code>, but that is not a requirement;
          the collations could be installed into some other schema as well. The function
          returns the number of new collation objects it created.</p>
      </td>
    </tr>
  </tbody>
</table>

[Table 9.93](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-INFO-PARTITION) lists functions that provide information about the structure of partitioned tables.

#### **Table 9.93. Partitioning Information Functions**

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
        <p><code>pg_partition_tree</code> ( <code>regclass</code> ) &#x2192; <code>setof record</code> ( <em><code>relid</code></em>  <code>regclass</code>, <em><code>parentrelid</code></em>  <code>regclass</code>, <em><code>isleaf</code></em>  <code>boolean</code>, <em><code>level</code></em>  <code>integer</code> )</p>
        <p>Lists the tables or indexes in the partition tree of the given partitioned
          table or partitioned index, with one row for each partition. Information
          provided includes the OID of the partition, the OID of its immediate parent,
          a boolean value telling if the partition is a leaf, and an integer telling
          its level in the hierarchy. The level value is 0 for the input table or
          index, 1 for its immediate child partitions, 2 for their partitions, and
          so on. Returns no rows if the relation does not exist or is not a partition
          or partitioned table.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_partition_ancestors</code> ( <code>regclass</code> ) &#x2192; <code>setof regclass</code>
        </p>
        <p>Lists the ancestor relations of the given partition, including the relation
          itself. Returns no rows if the relation does not exist or is not a partition
          or partitioned table.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_partition_root</code> ( <code>regclass</code> ) &#x2192; <code>regclass</code>
        </p>
        <p>Returns the top-most parent of the partition tree to which the given relation
          belongs. Returns <code>NULL</code> if the relation does not exist or is not
          a partition or partitioned table.</p>
      </td>
    </tr>
  </tbody>
</table>

For example, to check the total size of the data contained in a partitioned table `measurement`, one could use the following query:

```text
SELECT pg_size_pretty(sum(pg_relation_size(relid))) AS total_size
  FROM pg_partition_tree('measurement');
```

## 9.27.8. Index Maintenance Functions

[Table 9.94](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-INDEX-TABLE) shows the functions available for index maintenance tasks. \(Note that these maintenance tasks are normally done automatically by autovacuum; use of these functions is only required in special cases.\) These functions cannot be executed during recovery. Use of these functions is restricted to superusers and the owner of the given index.

#### **Table 9.94. Index Maintenance Functions**

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
        <p><code>brin_summarize_new_values</code> ( <em><code>index</code></em>  <code>regclass</code> )
          &#x2192; <code>integer</code>
        </p>
        <p>Scans the specified BRIN index to find page ranges in the base table that
          are not currently summarized by the index; for any such range it creates
          a new summary index tuple by scanning those table pages. Returns the number
          of new page range summaries that were inserted into the index.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>brin_summarize_range</code> ( <em><code>index</code></em>  <code>regclass</code>, <em><code>blockNumber</code></em>  <code>bigint</code> )
          &#x2192; <code>integer</code>
        </p>
        <p>Summarizes the page range covering the given block, if not already summarized.
          This is like <code>brin_summarize_new_values</code> except that it only processes
          the page range that covers the given table block number.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>brin_desummarize_range</code> ( <em><code>index</code></em>  <code>regclass</code>, <em><code>blockNumber</code></em>  <code>bigint</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Removes the BRIN index tuple that summarizes the page range covering the
          given table block, if there is one.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>gin_clean_pending_list</code> ( <em><code>index</code></em>  <code>regclass</code> )
          &#x2192; <code>bigint</code>
        </p>
        <p>Cleans up the &#x201C;pending&#x201D; list of the specified GIN index
          by moving entries in it, in bulk, to the main GIN data structure. Returns
          the number of pages removed from the pending list. If the argument is a
          GIN index built with the <code>fastupdate</code> option disabled, no cleanup
          happens and the result is zero, because the index doesn&apos;t have a pending
          list. See <a href="https://www.postgresql.org/docs/13/gin-implementation.html#GIN-FAST-UPDATE">Section 66.4.1</a> and
          <a
          href="https://www.postgresql.org/docs/13/gin-tips.html">Section 66.5</a>for details about the pending list and <code>fastupdate</code> option.</p>
      </td>
    </tr>
  </tbody>
</table>

## 9.27.9. Generic File Access Functions

The functions shown in [Table 9.95](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADMIN-GENFILE-TABLE) provide native access to files on the machine hosting the server. Only files within the database cluster directory and the `log_directory` can be accessed, unless the user is a superuser or is granted the role `pg_read_server_files`. Use a relative path for files in the cluster directory, and a path matching the `log_directory` configuration setting for log files.

Note that granting users the EXECUTE privilege on `pg_read_file()`, or related functions, allows them the ability to read any file on the server that the database server process can read; these functions bypass all in-database privilege checks. This means that, for example, a user with such access is able to read the contents of the `pg_authid` table where authentication information is stored, as well as read any table data in the database. Therefore, granting access to these functions should be carefully considered.

Some of these functions take an optional _`missing_ok`_ parameter, which specifies the behavior when the file or directory does not exist. If `true`, the function returns `NULL` or an empty result set, as appropriate. If `false`, an error is raised. The default is `false`.

#### **Table 9.95. Generic File Access Functions**

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
        <p><code>pg_ls_dir</code> ( <em><code>dirname</code></em>  <code>text</code> [, <em><code>missing_ok</code></em>  <code>boolean</code>, <em><code>include_dot_dirs</code></em>  <code>boolean</code> ]
          ) &#x2192; <code>setof text</code>
        </p>
        <p>Returns the names of all files (and directories and other special files)
          in the specified directory. The <em><code>include_dot_dirs</code></em> parameter
          indicates whether &#x201C;.&#x201D; and &#x201C;..&#x201D; are to be included
          in the result set; the default is to exclude them. Including them can be
          useful when <em><code>missing_ok</code></em> is <code>true</code>, to distinguish
          an empty directory from a non-existent directory.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_ls_logdir</code> () &#x2192; <code>setof record</code> ( <em><code>name</code></em>  <code>text</code>, <em><code>size</code></em>  <code>bigint</code>, <em><code>modification</code></em>  <code>timestamp with time zone</code> )</p>
        <p>Returns the name, size, and last modification time (mtime) of each ordinary
          file in the server&apos;s log directory. Filenames beginning with a dot,
          directories, and other special files are excluded.</p>
        <p>This function is restricted to superusers and members of the <code>pg_monitor</code> role
          by default, but other users can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_ls_waldir</code> () &#x2192; <code>setof record</code> ( <em><code>name</code></em>  <code>text</code>, <em><code>size</code></em>  <code>bigint</code>, <em><code>modification</code></em>  <code>timestamp with time zone</code> )</p>
        <p>Returns the name, size, and last modification time (mtime) of each ordinary
          file in the server&apos;s write-ahead log (WAL) directory. Filenames beginning
          with a dot, directories, and other special files are excluded.</p>
        <p>This function is restricted to superusers and members of the <code>pg_monitor</code> role
          by default, but other users can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_ls_archive_statusdir</code> () &#x2192; <code>setof record</code> ( <em><code>name</code></em>  <code>text</code>, <em><code>size</code></em>  <code>bigint</code>, <em><code>modification</code></em>  <code>timestamp with time zone</code> )</p>
        <p>Returns the name, size, and last modification time (mtime) of each ordinary
          file in the server&apos;s WAL archive status directory (<code>pg_wal/archive_status</code>).
          Filenames beginning with a dot, directories, and other special files are
          excluded.</p>
        <p>This function is restricted to superusers and members of the <code>pg_monitor</code> role
          by default, but other users can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_ls_tmpdir</code> ( [ <em><code>tablespace</code></em>  <code>oid</code> ]
          ) &#x2192; <code>setof record</code> ( <em><code>name</code></em>  <code>text</code>, <em><code>size</code></em>  <code>bigint</code>, <em><code>modification</code></em>  <code>timestamp with time zone</code> )</p>
        <p>Returns the name, size, and last modification time (mtime) of each ordinary
          file in the temporary file directory for the specified <em><code>tablespace</code></em>.
          If <em><code>tablespace</code></em> is not provided, the <code>pg_default</code> tablespace
          is examined. Filenames beginning with a dot, directories, and other special
          files are excluded.</p>
        <p>This function is restricted to superusers and members of the <code>pg_monitor</code> role
          by default, but other users can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_read_file</code> ( <em><code>filename</code></em>  <code>text</code> [, <em><code>offset</code></em>  <code>bigint</code>, <em><code>length</code></em>  <code>bigint</code> [, <em><code>missing_ok</code></em>  <code>boolean</code> ]]
          ) &#x2192; <code>text</code>
        </p>
        <p>Returns all or part of a text file, starting at the given byte <em><code>offset</code></em>,
          returning at most <em><code>length</code></em> bytes (less if the end of
          file is reached first). If <em><code>offset</code></em> is negative, it is
          relative to the end of the file. If <em><code>offset</code></em> and <em><code>length</code></em> are
          omitted, the entire file is returned. The bytes read from the file are
          interpreted as a string in the database&apos;s encoding; an error is thrown
          if they are not valid in that encoding.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_read_binary_file</code> ( <em><code>filename</code></em>  <code>text</code> [, <em><code>offset</code></em>  <code>bigint</code>, <em><code>length</code></em>  <code>bigint</code> [, <em><code>missing_ok</code></em>  <code>boolean</code> ]]
          ) &#x2192; <code>bytea</code>
        </p>
        <p>Returns all or part of a file. This function is identical to <code>pg_read_file</code> except
          that it can read arbitrary binary data, returning the result as <code>bytea</code> not <code>text</code>;
          accordingly, no encoding checks are performed.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
        <p>In combination with the <code>convert_from</code> function, this function
          can be used to read a text file in a specified encoding and convert to
          the database&apos;s encoding:</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_stat_file</code> ( <em><code>filename</code></em>  <code>text</code> [, <em><code>missing_ok</code></em>  <code>boolean</code> ]
          ) &#x2192; <code>record</code> ( <em><code>size</code></em>  <code>bigint</code>, <em><code>access</code></em>  <code>timestamp with time zone</code>, <em><code>modification</code></em>  <code>timestamp with time zone</code>, <em><code>change</code></em>  <code>timestamp with time zone</code>, <em><code>creation</code></em>  <code>timestamp with time zone</code>, <em><code>isdir</code></em>  <code>boolean</code> )</p>
        <p>Returns a record containing the file&apos;s size, last access time stamp,
          last modification time stamp, last file status change time stamp (Unix
          platforms only), file creation time stamp (Windows only), and a flag indicating
          if it is a directory.</p>
        <p>This function is restricted to superusers by default, but other users
          can be granted EXECUTE to run the function.</p>
      </td>
    </tr>
  </tbody>
</table>

## 9.27.10. Advisory Lock Functions

The functions shown in [Table 9.96](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-ADVISORY-LOCKS-TABLE) manage advisory locks. For details about proper use of these functions, see [Section 13.3.5](https://www.postgresql.org/docs/13/explicit-locking.html#ADVISORY-LOCKS).

All these functions are intended to be used to lock application-defined resources, which can be identified either by a single 64-bit key value or two 32-bit key values \(note that these two key spaces do not overlap\). If another session already holds a conflicting lock on the same resource identifier, the functions will either wait until the resource becomes available, or return a `false` result, as appropriate for the function. Locks can be either shared or exclusive: a shared lock does not conflict with other shared locks on the same resource, only with exclusive locks. Locks can be taken at session level \(so that they are held until released or the session ends\) or at transaction level \(so that they are held until the current transaction ends; there is no provision for manual release\). Multiple session-level lock requests stack, so that if the same resource identifier is locked three times there must then be three unlock requests to release the resource in advance of session end.

#### **Table 9.96. Advisory Lock Functions**

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
        <p><code>pg_advisory_lock</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>void</code>
        </p>
        <p><code>pg_advisory_lock</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Obtains an exclusive session-level advisory lock, waiting if necessary.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_advisory_lock_shared</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>void</code>
        </p>
        <p><code>pg_advisory_lock_shared</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Obtains a shared session-level advisory lock, waiting if necessary.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_advisory_unlock</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p><code>pg_advisory_unlock</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p>Releases a previously-acquired exclusive session-level advisory lock.
          Returns <code>true</code> if the lock is successfully released. If the lock
          was not held, <code>false</code> is returned, and in addition, an SQL warning
          will be reported by the server.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_advisory_unlock_all</code> () &#x2192; <code>void</code>
        </p>
        <p>Releases all session-level advisory locks held by the current session.
          (This function is implicitly invoked at session end, even if the client
          disconnects ungracefully.)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_advisory_unlock_shared</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p><code>pg_advisory_unlock_shared</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p>Releases a previously-acquired shared session-level advisory lock. Returns <code>true</code> if
          the lock is successfully released. If the lock was not held, <code>false</code> is
          returned, and in addition, an SQL warning will be reported by the server.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_advisory_xact_lock</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>void</code>
        </p>
        <p><code>pg_advisory_xact_lock</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Obtains an exclusive transaction-level advisory lock, waiting if necessary.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_advisory_xact_lock_shared</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>void</code>
        </p>
        <p><code>pg_advisory_xact_lock_shared</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>void</code>
        </p>
        <p>Obtains a shared transaction-level advisory lock, waiting if necessary.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_try_advisory_lock</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p><code>pg_try_advisory_lock</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p>Obtains an exclusive session-level advisory lock if available. This will
          either obtain the lock immediately and return <code>true</code>, or return <code>false</code> without
          waiting if the lock cannot be acquired immediately.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_try_advisory_lock_shared</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p><code>pg_try_advisory_lock_shared</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p>Obtains a shared session-level advisory lock if available. This will either
          obtain the lock immediately and return <code>true</code>, or return <code>false</code> without
          waiting if the lock cannot be acquired immediately.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_try_advisory_xact_lock</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p><code>pg_try_advisory_xact_lock</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p>Obtains an exclusive transaction-level advisory lock if available. This
          will either obtain the lock immediately and return <code>true</code>, or
          return <code>false</code> without waiting if the lock cannot be acquired
          immediately.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pg_try_advisory_xact_lock_shared</code> ( <em><code>key</code></em>  <code>bigint</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p><code>pg_try_advisory_xact_lock_shared</code> ( <em><code>key1</code></em>  <code>integer</code>, <em><code>key2</code></em>  <code>integer</code> )
          &#x2192; <code>boolean</code>
        </p>
        <p>Obtains a shared transaction-level advisory lock if available. This will
          either obtain the lock immediately and return <code>true</code>, or return <code>false</code> without
          waiting if the lock cannot be acquired immediately.</p>
      </td>
    </tr>
  </tbody>
</table>

