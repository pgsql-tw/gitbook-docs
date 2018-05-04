# 9.26. 系統管理函式

The functions described in this section are used to control and monitor aPostgreSQLinstallation.

## 9.26.1. Configuration Settings Functions

[Table 9.77](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-set-table)shows the functions available to query and alter run-time configuration parameters.

**Table 9.77. Configuration Settings Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `current_setting(setting_name`\[,`missing_ok`\]\) | `text` | get current value of setting |
| `set_config(setting_name`,`new_value`,`is_local`\) | `text` | set parameter and return new value |

The function`current_setting`yields the current value of the setting`setting_name`. It corresponds to theSQLcommand`SHOW`. An example:

```text
SELECT current_setting('datestyle');

 current_setting
-----------------
 ISO, MDY
(1 row)
```

If there is no setting named`setting_name`,`current_setting`throws an error unless\_`missing_ok`\_is supplied and is`true`.

`set_config`sets the parameter`setting_name`_\_to_`new_value`_. If_`is_local`\_is`true`, the new value will only apply to the current transaction. If you want the new value to apply for the current session, use`false`instead. The function corresponds to the SQL command`SET`. An example:

```text
SELECT set_config('log_statement_stats', 'off', false);

 set_config
------------
 off
(1 row)
```

## 9.26.2. Server Signaling Functions

The functions shown in[Table 9.78](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-signal-table)send control signals to other server processes. Use of these functions is restricted to superusers by default but access may be granted to others using`GRANT`, with noted exceptions.

**Table 9.78. Server Signaling Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_cancel_backend(pidint`\) | `boolean` | Cancel a backend's current query. This is also allowed if the calling role is a member of the role whose backend is being canceled or the calling role has been granted`pg_signal_backend`, however only superusers can cancel superuser backends. |
| `pg_reload_conf()` | `boolean` | Cause server processes to reload their configuration files |
| `pg_rotate_logfile()` | `boolean` | Rotate server's log file |
| `pg_terminate_backend(pidint`\) | `boolean` | Terminate a backend. This is also allowed if the calling role is a member of the role whose backend is being terminated or the calling role has been granted`pg_signal_backend`, however only superusers can terminate superuser backends. |

Each of these functions returns`true`if successful and`false`otherwise.

`pg_cancel_backend`and`pg_terminate_backend`send signals \(SIGINTorSIGTERMrespectively\) to backend processes identified by process ID. The process ID of an active backend can be found from the`pid`column of the`pg_stat_activity`view, or by listing the`postgres`processes on the server \(usingpson Unix or theTask ManageronWindows\). The role of an active backend can be found from the`usename`column of the`pg_stat_activity`view.

`pg_reload_conf`sends aSIGHUPsignal to the server, causing configuration files to be reloaded by all server processes.

`pg_rotate_logfile`signals the log-file manager to switch to a new output file immediately. This works only when the built-in log collector is running, since otherwise there is no log-file manager subprocess.

## 9.26.3. Backup Control Functions

The functions shown in[Table 9.79](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-backup-table)assist in making on-line backups. These functions cannot be executed during recovery \(except`pg_is_in_backup`,`pg_backup_start_time`and`pg_wal_lsn_diff`\).

**Table 9.79. Backup Control Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_create_restore_point(nametext`\) | `pg_lsn` | Create a named point for performing restore \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_current_wal_flush_lsn()` | `pg_lsn` | Get current write-ahead log flush location |
| `pg_current_wal_insert_lsn()` | `pg_lsn` | Get current write-ahead log insert location |
| `pg_current_wal_lsn()` | `pg_lsn` | Get current write-ahead log write location |
| `pg_start_backup(labeltext`\[,`fastboolean`\[,`exclusiveboolean`\]\]\) | `pg_lsn` | Prepare for performing on-line backup \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_stop_backup()` | `pg_lsn` | Finish performing exclusive on-line backup \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_stop_backup(exclusiveboolean`\[,`wait_for_archiveboolean`\]\) | `setof record` | Finish performing exclusive or non-exclusive on-line backup \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_is_in_backup()` | `bool` | True if an on-line exclusive backup is still in progress. |
| `pg_backup_start_time()` | `timestamp with time zone` | Get start time of an on-line exclusive backup in progress. |
| `pg_switch_wal()` | `pg_lsn` | Force switch to a new write-ahead log file \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_walfile_name(lsnpg_lsn`\) | `text` | Convert write-ahead log location to file name |
| `pg_walfile_name_offset(lsnpg_lsn`\) | `text`,`integer` | Convert write-ahead log location to file name and decimal byte offset within file |
| `pg_wal_lsn_diff(lsnpg_lsn`,`lsnpg_lsn`\) | `numeric` | Calculate the difference between two write-ahead log locations |

`pg_start_backup`accepts an arbitrary user-defined label for the backup. \(Typically this would be the name under which the backup dump file will be stored.\) When used in exclusive mode, the function writes a backup label file \(`backup_label`\) and, if there are any links in the`pg_tblspc/`directory, a tablespace map file \(`tablespace_map`\) into the database cluster's data directory, performs a checkpoint, and then returns the backup's starting write-ahead log location as text. The user can ignore this result value, but it is provided in case it is useful. When used in non-exclusive mode, the contents of these files are instead returned by the`pg_stop_backup`function, and should be written to the backup by the caller.

```text
postgres=# select pg_start_backup('label_goes_here');
 pg_start_backup
-----------------
 0/D4445B8
(1 row)
```

There is an optional second parameter of type`boolean`. If`true`, it specifies executing`pg_start_backup`as quickly as possible. This forces an immediate checkpoint which will cause a spike in I/O operations, slowing any concurrently executing queries.

In an exclusive backup,`pg_stop_backup`removes the label file and, if it exists, the`tablespace_map`file created by`pg_start_backup`. In a non-exclusive backup, the contents of the`backup_label`and`tablespace_map`are returned in the result of the function, and should be written to files in the backup \(and not in the data directory\). There is an optional second parameter of type boolean. If false, the`pg_stop_backup`will return immediately after the backup is completed without waiting for WAL to be archived. This behavior is only useful for backup software which independently monitors WAL archiving. Otherwise, WAL required to make the backup consistent might be missing and make the backup useless.

The function also creates a backup history file in the write-ahead log archive area. The history file includes the label given to`pg_start_backup`, the starting and ending write-ahead log locations for the backup, and the starting and ending times of the backup. The return value is the backup's ending write-ahead log location \(which again can be ignored\). After recording the ending location, the current write-ahead log insertion point is automatically advanced to the next write-ahead log file, so that the ending write-ahead log file can be archived immediately to complete the backup.

`pg_switch_wal`moves to the next write-ahead log file, allowing the current file to be archived \(assuming you are using continuous archiving\). The return value is the ending write-ahead log location + 1 within the just-completed write-ahead log file. If there has been no write-ahead log activity since the last write-ahead log switch,`pg_switch_wal`does nothing and returns the start location of the write-ahead log file currently in use.

`pg_create_restore_point`creates a named write-ahead log record that can be used as recovery target, and returns the corresponding write-ahead log location. The given name can then be used with[recovery\_target\_name](https://www.postgresql.org/docs/10/static/recovery-target-settings.html#recovery-target-name)to specify the point up to which recovery will proceed. Avoid creating multiple restore points with the same name, since recovery will stop at the first one whose name matches the recovery target.

`pg_current_wal_lsn`displays the current write-ahead log write location in the same format used by the above functions. Similarly,`pg_current_wal_insert_lsn`displays the current write-ahead log insertion location and`pg_current_wal_flush_lsn`displays the current write-ahead log flush location. The insertion location is the“logical”end of the write-ahead log at any instant, while the write location is the end of what has actually been written out from the server's internal buffers and flush location is the location guaranteed to be written to durable storage. The write location is the end of what can be examined from outside the server, and is usually what you want if you are interested in archiving partially-complete write-ahead log files. The insertion and flush locations are made available primarily for server debugging purposes. These are both read-only operations and do not require superuser permissions.

You can use`pg_walfile_name_offset`to extract the corresponding write-ahead log file name and byte offset from the results of any of the above functions. For example:

```text
postgres=# SELECT * FROM pg_walfile_name_offset(pg_stop_backup());
        file_name         | file_offset 
--------------------------+-------------
 00000001000000000000000D |     4039624
(1 row)
```

Similarly,`pg_walfile_name`extracts just the write-ahead log file name. When the given write-ahead log location is exactly at a write-ahead log file boundary, both these functions return the name of the preceding write-ahead log file. This is usually the desired behavior for managing write-ahead log archiving behavior, since the preceding file is the last one that currently needs to be archived.

`pg_wal_lsn_diff`calculates the difference in bytes between two write-ahead log locations. It can be used with`pg_stat_replication`or some functions shown in[Table 9.79](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-backup-table)to get the replication lag.

For details about proper usage of these functions, see[Section 25.3](https://www.postgresql.org/docs/10/static/continuous-archiving.html).

## 9.26.4. Recovery Control Functions

The functions shown in[Table 9.80](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-recovery-info-table)provide information about the current status of the standby. These functions may be executed both during recovery and in normal running.

**Table 9.80. Recovery Information Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_is_in_recovery()` | `bool` | True if recovery is still in progress. |
| `pg_last_wal_receive_lsn()` | `pg_lsn` | Get last write-ahead log location received and synced to disk by streaming replication. While streaming replication is in progress this will increase monotonically. If recovery has completed this will remain static at the value of the last WAL record received and synced to disk during recovery. If streaming replication is disabled, or if it has not yet started, the function returns NULL. |
| `pg_last_wal_replay_lsn()` | `pg_lsn` | Get last write-ahead log location replayed during recovery. If recovery is still in progress this will increase monotonically. If recovery has completed then this value will remain static at the value of the last WAL record applied during that recovery. When the server has been started normally without recovery the function returns NULL. |
| `pg_last_xact_replay_timestamp()` | `timestamp with time zone` | Get time stamp of last transaction replayed during recovery. This is the time at which the commit or abort WAL record for that transaction was generated on the primary. If no transactions have been replayed during recovery, this function returns NULL. Otherwise, if recovery is still in progress this will increase monotonically. If recovery has completed then this value will remain static at the value of the last transaction applied during that recovery. When the server has been started normally without recovery the function returns NULL. |

The functions shown in[Table 9.81](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-recovery-control-table)control the progress of recovery. These functions may be executed only during recovery.

**Table 9.81. Recovery Control Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_is_wal_replay_paused()` | `bool` | True if recovery is paused. |
| `pg_wal_replay_pause()` | `void` | Pauses recovery immediately \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\). |
| `pg_wal_replay_resume()` | `void` | Restarts recovery if it was paused \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\). |

While recovery is paused no further database changes are applied. If in hot standby, all new queries will see the same consistent snapshot of the database, and no further query conflicts will be generated until recovery is resumed.

If streaming replication is disabled, the paused state may continue indefinitely without problem. While streaming replication is in progress WAL records will continue to be received, which will eventually fill available disk space, depending upon the duration of the pause, the rate of WAL generation and available disk space.

## 9.26.5. Snapshot Synchronization Functions

PostgreSQLallows database sessions to synchronize their snapshots. A\_snapshot\_determines which data is visible to the transaction that is using the snapshot. Synchronized snapshots are necessary when two or more sessions need to see identical content in the database. If two sessions just start their transactions independently, there is always a possibility that some third transaction commits between the executions of the two`START TRANSACTION`commands, so that one session sees the effects of that transaction and the other does not.

To solve this problem,PostgreSQLallows a transaction to\_export\_the snapshot it is using. As long as the exporting transaction remains open, other transactions can\_import\_its snapshot, and thereby be guaranteed that they see exactly the same view of the database that the first transaction sees. But note that any database changes made by any one of these transactions remain invisible to the other transactions, as is usual for changes made by uncommitted transactions. So the transactions are synchronized with respect to pre-existing data, but act normally for changes they make themselves.

Snapshots are exported with the`pg_export_snapshot`function, shown in[Table 9.82](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-snapshot-synchronization-table), and imported with the[SET TRANSACTION](https://www.postgresql.org/docs/10/static/sql-set-transaction.html)command.

**Table 9.82. Snapshot Synchronization Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_export_snapshot()` | `text` | Save the current snapshot and return its identifier |

The function`pg_export_snapshot`saves the current snapshot and returns a`text`string identifying the snapshot. This string must be passed \(outside the database\) to clients that want to import the snapshot. The snapshot is available for import only until the end of the transaction that exported it. A transaction can export more than one snapshot, if needed. Note that doing so is only useful in`READ COMMITTED`transactions, since in`REPEATABLE READ`and higher isolation levels, transactions use the same snapshot throughout their lifetime. Once a transaction has exported any snapshots, it cannot be prepared with[PREPARE TRANSACTION](https://www.postgresql.org/docs/10/static/sql-prepare-transaction.html).

See[SET TRANSACTION](https://www.postgresql.org/docs/10/static/sql-set-transaction.html)for details of how to use an exported snapshot.

## 9.26.6. Replication Functions

The functions shown in[Table 9.83](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-replication-table)are for controlling and interacting with replication features. See[Section 26.2.5](https://www.postgresql.org/docs/10/static/warm-standby.html#streaming-replication),[Section 26.2.6](https://www.postgresql.org/docs/10/static/warm-standby.html#streaming-replication-slots), and[Chapter 49](https://www.postgresql.org/docs/10/static/replication-origins.html)for information about the underlying features. Use of these functions is restricted to superusers.

Many of these functions have equivalent commands in the replication protocol; see[Section 52.4](https://www.postgresql.org/docs/10/static/protocol-replication.html).

The functions described in[Section 9.26.3](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-backup),[Section 9.26.4](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-recovery-control), and[Section 9.26.5](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-snapshot-synchronization)are also relevant for replication.

**Table 9.83. ReplicationSQLFunctions**

| Function | Return Type | Description |
| :--- | :--- | :--- |
| `pg_create_physical_replication_slot(slot_namename`\[,`immediately_reserveboolean`,`temporaryboolean`\]\) | \(`slot_namename`,`lsnpg_lsn`\) | Creates a new physical replication slot named`slot_name`. The optional second parameter, when`true`, specifies that theLSNfor this replication slot be reserved immediately; otherwise theLSNis reserved on first connection from a streaming replication client. Streaming changes from a physical slot is only possible with the streaming-replication protocol — see[Section 52.4](https://www.postgresql.org/docs/10/static/protocol-replication.html). The optional third parameter,`temporary`, when set to true, specifies that the slot should not be permanently stored to disk and is only meant for use by current session. Temporary slots are also released upon any error. This function corresponds to the replication protocol command`CREATE_REPLICATION_SLOT ... PHYSICAL`. |
| `pg_drop_replication_slot(slot_namename`\) | `void` | Drops the physical or logical replication slot named`slot_name`. Same as replication protocol command`DROP_REPLICATION_SLOT`. For logical slots, this must be called when connected to the same database the slot was created on. |
| `pg_create_logical_replication_slot(slot_namename`,`pluginname`\[,`temporaryboolean`\]\) | \(`slot_namename`,`lsnpg_lsn`\) | Creates a new logical \(decoding\) replication slot named`slot_name`_\_using the output plugin_`plugin`_. The optional third parameter,_`temporary`\_, when set to true, specifies that the slot should not be permanently stored to disk and is only meant for use by current session. Temporary slots are also released upon any error. A call to this function has the same effect as the replication protocol command`CREATE_REPLICATION_SLOT ... LOGICAL`. |
| `pg_logical_slot_get_changes(slot_namename`,`upto_lsnpg_lsn`,`upto_nchangesint`, VARIADIC`optionstext[]`\) | \(`lsnpg_lsn`,`xidxid`,`datatext`\) | Returns changes in the slot`slot_name`, starting from the point at which since changes have been consumed last. If`upto_lsn`_\_and_`upto_nchanges`_are NULL, logical decoding will continue until end of WAL. If_`upto_lsn`_is non-NULL, decoding will include only those transactions which commit prior to the specified LSN. If_`upto_nchanges`\_is non-NULL, decoding will stop when the number of rows produced by decoding exceeds the specified value. Note, however, that the actual number of rows returned may be larger, since this limit is only checked after adding the rows produced when decoding each new transaction commit. |
| `pg_logical_slot_peek_changes(slot_namename`,`upto_lsnpg_lsn`,`upto_nchangesint`, VARIADIC`optionstext[]`\) | \(`lsnpg_lsn`,`xidxid`,`datatext`\) | Behaves just like the`pg_logical_slot_get_changes()`function, except that changes are not consumed; that is, they will be returned again on future calls. |
| `pg_logical_slot_get_binary_changes(slot_namename`,`upto_lsnpg_lsn`,`upto_nchangesint`, VARIADIC`optionstext[]`\) | \(`lsnpg_lsn`,`xidxid`,`databytea`\) | Behaves just like the`pg_logical_slot_get_changes()`function, except that changes are returned as`bytea`. |
| `pg_logical_slot_peek_binary_changes(slot_namename`,`upto_lsnpg_lsn`,`upto_nchangesint`, VARIADIC`optionstext[]`\) | \(`lsnpg_lsn`,`xidxid`,`databytea`\) | Behaves just like the`pg_logical_slot_get_changes()`function, except that changes are returned as`bytea`and that changes are not consumed; that is, they will be returned again on future calls. |
| `pg_replication_origin_create(node_nametext`\) | `oid` | Create a replication origin with the given external name, and return the internal id assigned to it. |
| `pg_replication_origin_drop(node_nametext`\) | `void` | Delete a previously created replication origin, including any associated replay progress. |
| `pg_replication_origin_oid(node_nametext`\) | `oid` | Lookup a replication origin by name and return the internal id. If no corresponding replication origin is found an error is thrown. |
| `pg_replication_origin_session_setup(node_nametext`\) | `void` | Mark the current session as replaying from the given origin, allowing replay progress to be tracked. Use`pg_replication_origin_session_reset`to revert. Can only be used if no previous origin is configured. |
| `pg_replication_origin_session_reset()` | `void` | Cancel the effects of`pg_replication_origin_session_setup()`. |
| `pg_replication_origin_session_is_setup()` | `bool` | Has a replication origin been configured in the current session? |
| `pg_replication_origin_session_progress(flushbool`\) | `pg_lsn` | Return the replay location for the replication origin configured in the current session. The parameter\_`flush`\_determines whether the corresponding local transaction will be guaranteed to have been flushed to disk or not. |
| `pg_replication_origin_xact_setup(origin_lsnpg_lsn`,`origin_timestamptimestamptz`\) | `void` | Mark the current transaction as replaying a transaction that has committed at the givenLSNand timestamp. Can only be called when a replication origin has previously been configured using`pg_replication_origin_session_setup()`. |
| `pg_replication_origin_xact_reset()` | `void` | Cancel the effects of`pg_replication_origin_xact_setup()`. |
| `pg_replication_origin_advance(node_nametext`,`lsnpg_lsn`\) | `void` | Set replication progress for the given node to the given location. This primarily is useful for setting up the initial location or a new location after configuration changes and similar. Be aware that careless use of this function can lead to inconsistently replicated data. |
| `pg_replication_origin_progress(node_nametext`,`flushbool`\) | `pg_lsn` | Return the replay location for the given replication origin. The parameter\_`flush`\_determines whether the corresponding local transaction will be guaranteed to have been flushed to disk or not. |
| `pg_logical_emit_message(transactionalbool`,`prefixtext`,`contenttext`\) | `pg_lsn` | Emit text logical decoding message. This can be used to pass generic messages to logical decoding plugins through WAL. The parameter`transactional`_\_specifies if the message should be part of current transaction or if it should be written immediately and decoded as soon as the logical decoding reads the record. The_`prefix`_is textual prefix used by the logical decoding plugins to easily recognize interesting messages for them. The_`content`\_is the text of the message. |
| `pg_logical_emit_message(transactionalbool`,`prefixtext`,`contentbytea`\) | `pg_lsn` | Emit binary logical decoding message. This can be used to pass generic messages to logical decoding plugins through WAL. The parameter`transactional`_\_specifies if the message should be part of current transaction or if it should be written immediately and decoded as soon as the logical decoding reads the record. The_`prefix`_is textual prefix used by the logical decoding plugins to easily recognize interesting messages for them. The_`content`\_is the binary content of the message. |

## 9.26.7. Database Object Management Functions

The functions shown in[Table 9.84](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-dbsize)calculate the disk space usage of database objects.

**Table 9.84. Database Object Size Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_column_size(any`\) | `int` | Number of bytes used to store a particular value \(possibly compressed\) |
| `pg_database_size(oid`\) | `bigint` | Disk space used by the database with the specified OID |
| `pg_database_size(name`\) | `bigint` | Disk space used by the database with the specified name |
| `pg_indexes_size(regclass`\) | `bigint` | Total disk space used by indexes attached to the specified table |
| `pg_relation_size(relationregclass`,`forktext`\) | `bigint` | Disk space used by the specified fork \(`'main'`,`'fsm'`,`'vm'`, or`'init'`\) of the specified table or index |
| `pg_relation_size(relationregclass`\) | `bigint` | Shorthand for`pg_relation_size(..., 'main')` |
| `pg_size_bytes(text`\) | `bigint` | Converts a size in human-readable format with size units into bytes |
| `pg_size_pretty(bigint`\) | `text` | Converts a size in bytes expressed as a 64-bit integer into a human-readable format with size units |
| `pg_size_pretty(numeric`\) | `text` | Converts a size in bytes expressed as a numeric value into a human-readable format with size units |
| `pg_table_size(regclass`\) | `bigint` | Disk space used by the specified table, excluding indexes \(but including TOAST, free space map, and visibility map\) |
| `pg_tablespace_size(oid`\) | `bigint` | Disk space used by the tablespace with the specified OID |
| `pg_tablespace_size(name`\) | `bigint` | Disk space used by the tablespace with the specified name |
| `pg_total_relation_size(regclass`\) | `bigint` | Total disk space used by the specified table, including all indexes andTOASTdata |

`pg_column_size`shows the space used to store any individual data value.

`pg_total_relation_size`accepts the OID or name of a table or toast table, and returns the total on-disk space used for that table, including all associated indexes. This function is equivalent to`pg_table_size+pg_indexes_size`.

`pg_table_size`accepts the OID or name of a table and returns the disk space needed for that table, exclusive of indexes. \(TOAST space, free space map, and visibility map are included.\)

`pg_indexes_size`accepts the OID or name of a table and returns the total disk space used by all the indexes attached to that table.

`pg_database_size`and`pg_tablespace_size`accept the OID or name of a database or tablespace, and return the total disk space used therein. To use`pg_database_size`, you must have`CONNECT`permission on the specified database \(which is granted by default\), or be a member of the`pg_read_all_stats`role. To use`pg_tablespace_size`, you must have`CREATE`permission on the specified tablespace, or be a member of the`pg_read_all_stats`role unless it is the default tablespace for the current database.

`pg_relation_size`accepts the OID or name of a table, index or toast table, and returns the on-disk size in bytes of one fork of that relation. \(Note that for most purposes it is more convenient to use the higher-level functions`pg_total_relation_size`or`pg_table_size`, which sum the sizes of all forks.\) With one argument, it returns the size of the main data fork of the relation. The second argument can be provided to specify which fork to examine:

* `'main'`returns the size of the main data fork of the relation.
* `'fsm'`returns the size of the Free Space Map \(see[Section 66.3](https://www.postgresql.org/docs/10/static/storage-fsm.html)\) associated with the relation.
* `'vm'`returns the size of the Visibility Map \(see[Section 66.4](https://www.postgresql.org/docs/10/static/storage-vm.html)\) associated with the relation.
* `'init'`returns the size of the initialization fork, if any, associated with the relation.

`pg_size_pretty`can be used to format the result of one of the other functions in a human-readable way, using bytes, kB, MB, GB or TB as appropriate.

`pg_size_bytes`can be used to get the size in bytes from a string in human-readable format. The input may have units of bytes, kB, MB, GB or TB, and is parsed case-insensitively. If no units are specified, bytes are assumed.

## Note

The units kB, MB, GB and TB used by the functions`pg_size_pretty`and`pg_size_bytes`are defined using powers of 2 rather than powers of 10, so 1kB is 1024 bytes, 1MB is 10242= 1048576 bytes, and so on.

The functions above that operate on tables or indexes accept a`regclass`argument, which is simply the OID of the table or index in the`pg_class`system catalog. You do not have to look up the OID by hand, however, since the`regclass`data type's input converter will do the work for you. Just write the table name enclosed in single quotes so that it looks like a literal constant. For compatibility with the handling of ordinarySQLnames, the string will be converted to lower case unless it contains double quotes around the table name.

If an OID that does not represent an existing object is passed as argument to one of the above functions, NULL is returned.

The functions shown in[Table 9.85](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-dblocation)assist in identifying the specific disk files associated with database objects.

**Table 9.85. Database Object Location Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_relation_filenode(relationregclass`\) | `oid` | Filenode number of the specified relation |
| `pg_relation_filepath(relationregclass`\) | `text` | File path name of the specified relation |
| `pg_filenode_relation(tablespaceoid`,`filenodeoid`\) | `regclass` | Find the relation associated with a given tablespace and filenode |

`pg_relation_filenode`accepts the OID or name of a table, index, sequence, or toast table, and returns the“filenode”number currently assigned to it. The filenode is the base component of the file name\(s\) used for the relation \(see[Section 66.1](https://www.postgresql.org/docs/10/static/storage-file-layout.html)for more information\). For most tables the result is the same as`pg_class`.`relfilenode`, but for certain system catalogs`relfilenode`is zero and this function must be used to get the correct value. The function returns NULL if passed a relation that does not have storage, such as a view.

`pg_relation_filepath`is similar to`pg_relation_filenode`, but it returns the entire file path name \(relative to the database cluster's data directory`PGDATA`\) of the relation.

`pg_filenode_relation`is the reverse of`pg_relation_filenode`. Given a“tablespace”OID and a“filenode”, it returns the associated relation's OID. For a table in the database's default tablespace, the tablespace can be specified as 0.

[Table 9.86](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-collation)lists functions used to manage collations.

**Table 9.86. Collation Management Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_collation_actual_version(oid`\) | `text` | Return actual version of collation from operating system |
| `pg_import_system_collations(if_not_existsboolean`,`schemaregnamespace`\) | `void` | Import operating system collations |

`pg_collation_actual_version`returns the actual version of the collation object as it is currently installed in the operating system. If this is different from the value in`pg_collation.collversion`, then objects depending on the collation might need to be rebuilt. See also[ALTER COLLATION](https://www.postgresql.org/docs/10/static/sql-altercollation.html).

`pg_import_system_collations`populates the system catalog`pg_collation`with collations based on all the locales it finds on the operating system. This is what`initdb`uses; see[Section 23.2.2](https://www.postgresql.org/docs/10/static/collation.html#collation-managing)for more details. If additional locales are installed into the operating system later on, this function can be run again to add collations for the new locales. In that case, the parameter`if_not_exists`_\_should be set to true to skip over existing collations. The_`schema`\_parameter would typically be`pg_catalog`, but that is not a requirement. \(Collation objects based on locales that are no longer present on the operating system are never removed by this function.\)

## 9.26.8. Index Maintenance Functions

[Table 9.87](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-index-table)shows the functions available for index maintenance tasks. These functions cannot be executed during recovery. Use of these functions is restricted to superusers and the owner of the given index.

**Table 9.87. Index Maintenance Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `brin_summarize_new_values(indexregclass`\) | `integer` | summarize page ranges not already summarized |
| `brin_summarize_range(indexregclass`,`blockNumberbigint`\) | `integer` | summarize the page range covering the given block, if not already summarized |
| `brin_desummarize_range(indexregclass`,`blockNumberbigint`\) | `integer` | de-summarize the page range covering the given block, if summarized |
| `gin_clean_pending_list(indexregclass`\) | `bigint` | move GIN pending list entries into main index structure |

`brin_summarize_new_values`accepts the OID or name of a BRIN index and inspects the index to find page ranges in the base table that are not currently summarized by the index; for any such range it creates a new summary index tuple by scanning the table pages. It returns the number of new page range summaries that were inserted into the index.`brin_summarize_range`does the same, except it only summarizes the range that covers the given block number.

`gin_clean_pending_list`accepts the OID or name of a GIN index and cleans up the pending list of the specified index by moving entries in it to the main GIN data structure in bulk. It returns the number of pages removed from the pending list. Note that if the argument is a GIN index built with the`fastupdate`option disabled, no cleanup happens and the return value is 0, because the index doesn't have a pending list. Please see[Section 64.4.1](https://www.postgresql.org/docs/10/static/gin-implementation.html#gin-fast-update)and[Section 64.5](https://www.postgresql.org/docs/10/static/gin-tips.html)for details of the pending list and`fastupdate`option.

## 9.26.9. Generic File Access Functions

The functions shown in[Table 9.88](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-admin-genfile-table)provide native access to files on the machine hosting the server. Only files within the database cluster directory and the`log_directory`can be accessed. Use a relative path for files in the cluster directory, and a path matching the`log_directory`configuration setting for log files. Use of these functions is restricted to superusers except where stated otherwise.

**Table 9.88. Generic File Access Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_ls_dir(dirnametext`\[,`missing_okboolean`,`include_dot_dirsboolean`\]\) | `setof text` | List the contents of a directory. |
| `pg_ls_logdir()` | `setof record` | List the name, size, and last modification time of files in the log directory. Access is granted to members of the`pg_monitor`role and may be granted to other non-superuser roles. |
| `pg_ls_waldir()` | `setof record` | List the name, size, and last modification time of files in the WAL directory. Access is granted to members of the`pg_monitor`role and may be granted to other non-superuser roles. |
| `pg_read_file(filenametext`\[,`offsetbigint`,`lengthbigint`\[,`missing_okboolean`\] \]\) | `text` | Return the contents of a text file. |
| `pg_read_binary_file(filenametext`\[,`offsetbigint`,`lengthbigint`\[,`missing_okboolean`\] \]\) | `bytea` | Return the contents of a file. |
| `pg_stat_file(filenametext`\[,`missing_okboolean`\]\) | `record` | Return information about a file. |

Some of these functions take an optional\_`missing_ok`\_parameter, which specifies the behavior when the file or directory does not exist. If`true`, the function returns NULL \(except`pg_ls_dir`, which returns an empty result set\). If`false`, an error is raised. The default is`false`.

`pg_ls_dir`returns the names of all files \(and directories and other special files\) in the specified directory. The`include_dot_dirs`_\_indicates whether“.”and“..”are included in the result set. The default is to exclude them \(_`false`_\), but including them can be useful when_`missing_ok`\_is`true`, to distinguish an empty directory from an non-existent directory.

`pg_ls_logdir`returns the name, size, and last modified time \(mtime\) of each file in the log directory. By default, only superusers and members of the`pg_monitor`role can use this function. Access may be granted to others using`GRANT`.

`pg_ls_waldir`returns the name, size, and last modified time \(mtime\) of each file in the write ahead log \(WAL\) directory. By default only superusers and members of the`pg_monitor`role can use this function. Access may be granted to others using`GRANT`.

`pg_read_file`returns part of a text file, starting at the given`offset`, returning at most`length`_\_bytes \(less if the end of file is reached first\). If_`offset`_is negative, it is relative to the end of the file. If_`offset`_and_`length`\_are omitted, the entire file is returned. The bytes read from the file are interpreted as a string in the server encoding; an error is thrown if they are not valid in that encoding.

`pg_read_binary_file`is similar to`pg_read_file`, except that the result is a`bytea`value; accordingly, no encoding checks are performed. In combination with the`convert_from`function, this function can be used to read a file in a specified encoding:

```text
SELECT convert_from(pg_read_binary_file('file_in_utf8.txt'), 'UTF8');
```

`pg_stat_file`returns a record containing the file size, last accessed time stamp, last modified time stamp, last file status change time stamp \(Unix platforms only\), file creation time stamp \(Windows only\), and a`boolean`indicating if it is a directory. Typical usages include:

```text
SELECT * FROM pg_stat_file('filename');
SELECT (pg_stat_file('filename')).modification;
```

## 9.26.10. Advisory Lock Functions

The functions shown in[Table 9.89](https://www.postgresql.org/docs/10/static/functions-admin.html#functions-advisory-locks-table)manage advisory locks. For details about proper use of these functions, see[Section 13.3.5](https://www.postgresql.org/docs/10/static/explicit-locking.html#advisory-locks).

**Table 9.89. Advisory Lock Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_advisory_lock(keybigint`\) | `void` | Obtain exclusive session level advisory lock |
| `pg_advisory_lock(key1int`,`key2int`\) | `void` | Obtain exclusive session level advisory lock |
| `pg_advisory_lock_shared(keybigint`\) | `void` | Obtain shared session level advisory lock |
| `pg_advisory_lock_shared(key1int`,`key2int`\) | `void` | Obtain shared session level advisory lock |
| `pg_advisory_unlock(keybigint`\) | `boolean` | Release an exclusive session level advisory lock |
| `pg_advisory_unlock(key1int`,`key2int`\) | `boolean` | Release an exclusive session level advisory lock |
| `pg_advisory_unlock_all()` | `void` | Release all session level advisory locks held by the current session |
| `pg_advisory_unlock_shared(keybigint`\) | `boolean` | Release a shared session level advisory lock |
| `pg_advisory_unlock_shared(key1int`,`key2int`\) | `boolean` | Release a shared session level advisory lock |
| `pg_advisory_xact_lock(keybigint`\) | `void` | Obtain exclusive transaction level advisory lock |
| `pg_advisory_xact_lock(key1int`,`key2int`\) | `void` | Obtain exclusive transaction level advisory lock |
| `pg_advisory_xact_lock_shared(keybigint`\) | `void` | Obtain shared transaction level advisory lock |
| `pg_advisory_xact_lock_shared(key1int`,`key2int`\) | `void` | Obtain shared transaction level advisory lock |
| `pg_try_advisory_lock(keybigint`\) | `boolean` | Obtain exclusive session level advisory lock if available |
| `pg_try_advisory_lock(key1int`,`key2int`\) | `boolean` | Obtain exclusive session level advisory lock if available |
| `pg_try_advisory_lock_shared(keybigint`\) | `boolean` | Obtain shared session level advisory lock if available |
| `pg_try_advisory_lock_shared(key1int`,`key2int`\) | `boolean` | Obtain shared session level advisory lock if available |
| `pg_try_advisory_xact_lock(keybigint`\) | `boolean` | Obtain exclusive transaction level advisory lock if available |
| `pg_try_advisory_xact_lock(key1int`,`key2int`\) | `boolean` | Obtain exclusive transaction level advisory lock if available |
| `pg_try_advisory_xact_lock_shared(keybigint`\) | `boolean` | Obtain shared transaction level advisory lock if available |
| `pg_try_advisory_xact_lock_shared(key1int`,`key2int`\) | `boolean` | Obtain shared transaction level advisory lock if available |

`pg_advisory_lock`locks an application-defined resource, which can be identified either by a single 64-bit key value or two 32-bit key values \(note that these two key spaces do not overlap\). If another session already holds a lock on the same resource identifier, this function will wait until the resource becomes available. The lock is exclusive. Multiple lock requests stack, so that if the same resource is locked three times it must then be unlocked three times to be released for other sessions' use.

`pg_advisory_lock_shared`works the same as`pg_advisory_lock`, except the lock can be shared with other sessions requesting shared locks. Only would-be exclusive lockers are locked out.

`pg_try_advisory_lock`is similar to`pg_advisory_lock`, except the function will not wait for the lock to become available. It will either obtain the lock immediately and return`true`, or return`false`if the lock cannot be acquired immediately.

`pg_try_advisory_lock_shared`works the same as`pg_try_advisory_lock`, except it attempts to acquire a shared rather than an exclusive lock.

`pg_advisory_unlock`will release a previously-acquired exclusive session level advisory lock. It returns`true`if the lock is successfully released. If the lock was not held, it will return`false`, and in addition, an SQL warning will be reported by the server.

`pg_advisory_unlock_shared`works the same as`pg_advisory_unlock`, except it releases a shared session level advisory lock.

`pg_advisory_unlock_all`will release all session level advisory locks held by the current session. \(This function is implicitly invoked at session end, even if the client disconnects ungracefully.\)

`pg_advisory_xact_lock`works the same as`pg_advisory_lock`, except the lock is automatically released at the end of the current transaction and cannot be released explicitly.

`pg_advisory_xact_lock_shared`works the same as`pg_advisory_lock_shared`, except the lock is automatically released at the end of the current transaction and cannot be released explicitly.

`pg_try_advisory_xact_lock`works the same as`pg_try_advisory_lock`, except the lock, if acquired, is automatically released at the end of the current transaction and cannot be released explicitly.

`pg_try_advisory_xact_lock_shared`works the same as`pg_try_advisory_lock_shared`, except the lock, if acquired, is automatically released at the end of the current transaction and cannot be released explicitly.

