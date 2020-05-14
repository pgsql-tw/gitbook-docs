# 9.26. 系統管理函式

## 9.26.1. 組態設定函式

[Table 9.82](system-administration.md#table-9-82-configuration-settings-functions) 列出了可用於查詢和變更執行階段組態參數的函式。

#### **Table 9.82. Configuration Settings Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `current_setting(`_`setting_name`_ \[, _`missing_ok`_ \]\) | `text` | get current value of setting |
| `set_config(`_`setting_name`_, _`new_value`_, _`is_local`_\) | `text` | set parameter and return new value |

函數 current\_setting 會回傳 setting\_name 目前的設定值。它對應於 SQL 指令 SHOW。範例如下：

```text
SELECT current_setting('datestyle');

 current_setting
-----------------
 ISO, MDY
(1 row)
```

如果沒有名為 setting\_name 的設定，也沒有設定 missing\_ok 為 true，則 current\_setting 會引發執行錯誤訊息。

set\_config 將參數 setting\_name 設定為 new\_value。如果 is\_local 為 true，則新值將僅套用於目前交易事務之中。如果您希望新值套用於目前連線，請讓 is\_local 為 false。此功能對應的 SQL 命令為 SET。範例如下：

```text
SELECT set_config('log_statement_stats', 'off', false);

 set_config
------------
 off
(1 row)
```

## 9.26.2. 伺服器系統信號函數

[Table 9.83](system-administration.md#table-9-83-server-signaling-functions) 中列出的功能將系統控制信號發送到其他伺服器程序。預設情況下，這些功能僅限於超級使用者使用，可以在例外情況使用 GRANT 授予其他人存取權限。

#### **Table 9.83. Server Signaling Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_cancel_backend(`_`pid`_ `int`\) | `boolean` | 從後端服務取消正在執行的查詢。如果呼叫的角色是其後端被取消的角色的成員或已授予呼叫角色 pg\_signal\_backend 的角色，則也允許進行這個動作，但是只有超級使用者才能取消超級使用者後端行程。 |
| `pg_reload_conf()` | `boolean` | 使伺服器程序重新載入其組態配置檔案 |
| `pg_rotate_logfile()` | `boolean` | 輪流使用下一個伺服器的日誌檔案 |
| `pg_terminate_backend(`_`pid`_ `int`\) | `boolean` | 終止整個後端程序。如果呼叫的角色是其後端被終止的角色的成員或已授予呼叫角色 pg\_signal\_backend 的角色，則也允許進行這個動作，但是只有超級使用者才能終止超級使用者的後端程序。 |

如果成功，這些函數均回傳 true，否則回傳 false。

pg\_cancel\_backend 和 pg\_terminate\_backend 發送信號（分別為SIGINT 或 SIGTERM）到由程序 ID 指示的後端程序。正在運作中的後端程序 ID 可以從 pg\_stat\_activity 檢視表的 pid 欄位中找到，或者透過列出伺服器上的 postgres 程序（在 Unix 上使用 ps 或在 Windows 上使用工作管理員）找到。正在執行的後端角色可以在 pg\_stat\_activity 檢視表的 usename 欄位中找到。

pg\_reload\_conf 向伺服器發送 SIGHUP 信號，會使所有伺服器程序重新載入組態檔案。

pg\_rotate\_logfile 指示日誌檔案管理器立即切換到新的輸出檔案。僅當內建的日誌收集器正在運行時，此函數才有作用，因為沒有日誌檔案管理器的子程序可以操作。

## 9.26.3. Backup Control Functions

The functions shown in [Table 9.84](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADMIN-BACKUP-TABLE) assist in making on-line backups. These functions cannot be executed during recovery \(except non-exclusive `pg_start_backup`, non-exclusive `pg_stop_backup`, `pg_is_in_backup`, `pg_backup_start_time` and `pg_wal_lsn_diff`\).

#### **Table 9.84. Backup Control Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_create_restore_point(`_`name`_ `text`\) | `pg_lsn` | Create a named point for performing restore \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_current_wal_flush_lsn()` | `pg_lsn` | Get current write-ahead log flush location |
| `pg_current_wal_insert_lsn()` | `pg_lsn` | Get current write-ahead log insert location |
| `pg_current_wal_lsn()` | `pg_lsn` | Get current write-ahead log write location |
| `pg_start_backup(`_`label`_ `text` \[, _`fast`_ `boolean` \[, _`exclusive`_ `boolean` \]\]\) | `pg_lsn` | Prepare for performing on-line backup \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_stop_backup()` | `pg_lsn` | Finish performing exclusive on-line backup \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_stop_backup(`_`exclusive`_ `boolean` \[, _`wait_for_archive`_ `boolean` \]\) | `setof record` | Finish performing exclusive or non-exclusive on-line backup \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_is_in_backup()` | `bool` | True if an on-line exclusive backup is still in progress. |
| `pg_backup_start_time()` | `timestamp with time zone` | Get start time of an on-line exclusive backup in progress. |
| `pg_switch_wal()` | `pg_lsn` | Force switch to a new write-ahead log file \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\) |
| `pg_walfile_name(`_`lsn`_ `pg_lsn`\) | `text` | Convert write-ahead log location to file name |
| `pg_walfile_name_offset(`_`lsn`_ `pg_lsn`\) | `text`, `integer` | Convert write-ahead log location to file name and decimal byte offset within file |
| `pg_wal_lsn_diff(`_`lsn`_ `pg_lsn`, _`lsn`_ `pg_lsn`\) | `numeric` | Calculate the difference between two write-ahead log locations |

`pg_start_backup` accepts an arbitrary user-defined label for the backup. \(Typically this would be the name under which the backup dump file will be stored.\) When used in exclusive mode, the function writes a backup label file \(`backup_label`\) and, if there are any links in the `pg_tblspc/` directory, a tablespace map file \(`tablespace_map`\) into the database cluster's data directory, performs a checkpoint, and then returns the backup's starting write-ahead log location as text. The user can ignore this result value, but it is provided in case it is useful. When used in non-exclusive mode, the contents of these files are instead returned by the `pg_stop_backup` function, and should be written to the backup by the caller.

```text
postgres=# select pg_start_backup('label_goes_here');
 pg_start_backup
-----------------
 0/D4445B8
(1 row)
```

There is an optional second parameter of type `boolean`. If `true`, it specifies executing `pg_start_backup` as quickly as possible. This forces an immediate checkpoint which will cause a spike in I/O operations, slowing any concurrently executing queries.

In an exclusive backup, `pg_stop_backup` removes the label file and, if it exists, the `tablespace_map` file created by `pg_start_backup`. In a non-exclusive backup, the contents of the `backup_label` and `tablespace_map` are returned in the result of the function, and should be written to files in the backup \(and not in the data directory\). There is an optional second parameter of type `boolean`. If false, the `pg_stop_backup` will return immediately after the backup is completed without waiting for WAL to be archived. This behavior is only useful for backup software which independently monitors WAL archiving. Otherwise, WAL required to make the backup consistent might be missing and make the backup useless. When this parameter is set to true, `pg_stop_backup` will wait for WAL to be archived when archiving is enabled; on the standby, this means that it will wait only when `archive_mode = always`. If write activity on the primary is low, it may be useful to run `pg_switch_wal` on the primary in order to trigger an immediate segment switch.

When executed on a primary, the function also creates a backup history file in the write-ahead log archive area. The history file includes the label given to `pg_start_backup`, the starting and ending write-ahead log locations for the backup, and the starting and ending times of the backup. The return value is the backup's ending write-ahead log location \(which again can be ignored\). After recording the ending location, the current write-ahead log insertion point is automatically advanced to the next write-ahead log file, so that the ending write-ahead log file can be archived immediately to complete the backup.

`pg_switch_wal` moves to the next write-ahead log file, allowing the current file to be archived \(assuming you are using continuous archiving\). The return value is the ending write-ahead log location + 1 within the just-completed write-ahead log file. If there has been no write-ahead log activity since the last write-ahead log switch, `pg_switch_wal` does nothing and returns the start location of the write-ahead log file currently in use.

`pg_create_restore_point` creates a named write-ahead log record that can be used as recovery target, and returns the corresponding write-ahead log location. The given name can then be used with [recovery\_target\_name](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-RECOVERY-TARGET-NAME) to specify the point up to which recovery will proceed. Avoid creating multiple restore points with the same name, since recovery will stop at the first one whose name matches the recovery target.

`pg_current_wal_lsn` displays the current write-ahead log write location in the same format used by the above functions. Similarly, `pg_current_wal_insert_lsn` displays the current write-ahead log insertion location and `pg_current_wal_flush_lsn` displays the current write-ahead log flush location. The insertion location is the “logical” end of the write-ahead log at any instant, while the write location is the end of what has actually been written out from the server's internal buffers and flush location is the location guaranteed to be written to durable storage. The write location is the end of what can be examined from outside the server, and is usually what you want if you are interested in archiving partially-complete write-ahead log files. The insertion and flush locations are made available primarily for server debugging purposes. These are both read-only operations and do not require superuser permissions.

You can use `pg_walfile_name_offset` to extract the corresponding write-ahead log file name and byte offset from the results of any of the above functions. For example:

```text
postgres=# SELECT * FROM pg_walfile_name_offset(pg_stop_backup());
        file_name         | file_offset 
--------------------------+-------------
 00000001000000000000000D |     4039624
(1 row)
```

Similarly, `pg_walfile_name` extracts just the write-ahead log file name. When the given write-ahead log location is exactly at a write-ahead log file boundary, both these functions return the name of the preceding write-ahead log file. This is usually the desired behavior for managing write-ahead log archiving behavior, since the preceding file is the last one that currently needs to be archived.

`pg_wal_lsn_diff` calculates the difference in bytes between two write-ahead log locations. It can be used with `pg_stat_replication` or some functions shown in [Table 9.84](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADMIN-BACKUP-TABLE) to get the replication lag.

For details about proper usage of these functions, see [Section 25.3](https://www.postgresql.org/docs/12/continuous-archiving.html).

## 9.26.4. Recovery Control Functions

The functions shown in [Table 9.85](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-RECOVERY-INFO-TABLE) provide information about the current status of the standby. These functions may be executed both during recovery and in normal running.

#### **Table 9.85. Recovery Information Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_is_in_recovery()` | `bool` | True if recovery is still in progress. |
| `pg_last_wal_receive_lsn()` | `pg_lsn` | Get last write-ahead log location received and synced to disk by streaming replication. While streaming replication is in progress this will increase monotonically. If recovery has completed this will remain static at the value of the last WAL record received and synced to disk during recovery. If streaming replication is disabled, or if it has not yet started, the function returns NULL. |
| `pg_last_wal_replay_lsn()` | `pg_lsn` | Get last write-ahead log location replayed during recovery. If recovery is still in progress this will increase monotonically. If recovery has completed then this value will remain static at the value of the last WAL record applied during that recovery. When the server has been started normally without recovery the function returns NULL. |
| `pg_last_xact_replay_timestamp()` | `timestamp with time zone` | Get time stamp of last transaction replayed during recovery. This is the time at which the commit or abort WAL record for that transaction was generated on the primary. If no transactions have been replayed during recovery, this function returns NULL. Otherwise, if recovery is still in progress this will increase monotonically. If recovery has completed then this value will remain static at the value of the last transaction applied during that recovery. When the server has been started normally without recovery the function returns NULL. |

The functions shown in [Table 9.86](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL-TABLE) control the progress of recovery. These functions may be executed only during recovery.

#### **Table 9.86. Recovery Control Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_is_wal_replay_paused()` | `bool` | True if recovery is paused. |
| `pg_promote(`_`wait`_ `boolean` DEFAULT true, _`wait_seconds`_ `integer` DEFAULT 60\) | `boolean` | Promotes a physical standby server. With _`wait`_ set to `true` \(the default\), the function waits until promotion is completed or _`wait_seconds`_ seconds have passed, and returns `true` if promotion is successful and `false` otherwise. If _`wait`_ is set to `false`, the function returns `true` immediately after sending `SIGUSR1` to the postmaster to trigger the promotion. This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function. |
| `pg_wal_replay_pause()` | `void` | Pauses recovery immediately \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\). |
| `pg_wal_replay_resume()` | `void` | Restarts recovery if it was paused \(restricted to superusers by default, but other users can be granted EXECUTE to run the function\). |

While recovery is paused no further database changes are applied. If in hot standby, all new queries will see the same consistent snapshot of the database, and no further query conflicts will be generated until recovery is resumed.

If streaming replication is disabled, the paused state may continue indefinitely without problem. While streaming replication is in progress WAL records will continue to be received, which will eventually fill available disk space, depending upon the duration of the pause, the rate of WAL generation and available disk space.

## 9.26.5. Snapshot Synchronization Functions

PostgreSQL allows database sessions to synchronize their snapshots. A _snapshot_ determines which data is visible to the transaction that is using the snapshot. Synchronized snapshots are necessary when two or more sessions need to see identical content in the database. If two sessions just start their transactions independently, there is always a possibility that some third transaction commits between the executions of the two `START TRANSACTION` commands, so that one session sees the effects of that transaction and the other does not.

To solve this problem, PostgreSQL allows a transaction to _export_ the snapshot it is using. As long as the exporting transaction remains open, other transactions can _import_ its snapshot, and thereby be guaranteed that they see exactly the same view of the database that the first transaction sees. But note that any database changes made by any one of these transactions remain invisible to the other transactions, as is usual for changes made by uncommitted transactions. So the transactions are synchronized with respect to pre-existing data, but act normally for changes they make themselves.

Snapshots are exported with the `pg_export_snapshot` function, shown in [Table 9.87](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION-TABLE), and imported with the [SET TRANSACTION](https://www.postgresql.org/docs/12/sql-set-transaction.html) command.

#### **Table 9.87. Snapshot Synchronization Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_export_snapshot()` | `text` | Save the current snapshot and return its identifier |

The function `pg_export_snapshot` saves the current snapshot and returns a `text` string identifying the snapshot. This string must be passed \(outside the database\) to clients that want to import the snapshot. The snapshot is available for import only until the end of the transaction that exported it. A transaction can export more than one snapshot, if needed. Note that doing so is only useful in `READ COMMITTED` transactions, since in `REPEATABLE READ` and higher isolation levels, transactions use the same snapshot throughout their lifetime. Once a transaction has exported any snapshots, it cannot be prepared with [PREPARE TRANSACTION](https://www.postgresql.org/docs/12/sql-prepare-transaction.html).

See [SET TRANSACTION](https://www.postgresql.org/docs/12/sql-set-transaction.html) for details of how to use an exported snapshot.

## 9.26.6. Replication Functions

The functions shown in [Table 9.88](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-REPLICATION-TABLE) are for controlling and interacting with replication features. See [Section 26.2.5](https://www.postgresql.org/docs/12/warm-standby.html#STREAMING-REPLICATION), [Section 26.2.6](https://www.postgresql.org/docs/12/warm-standby.html#STREAMING-REPLICATION-SLOTS), and [Chapter 49](https://www.postgresql.org/docs/12/replication-origins.html) for information about the underlying features. Use of functions for replication origin is restricted to superusers. Use of functions for replication slot is restricted to superusers and users having `REPLICATION` privilege.

Many of these functions have equivalent commands in the replication protocol; see [Section 52.4](https://www.postgresql.org/docs/12/protocol-replication.html).

The functions described in [Section 9.26.3](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADMIN-BACKUP), [Section 9.26.4](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL), and [Section 9.26.5](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION) are also relevant for replication.

#### **Table 9.88. Replication SQL Functions**

| Function | Return Type | Description |
| :--- | :--- | :--- |
| `pg_create_physical_replication_slot(`_`slot_name`_ `name` \[, _`immediately_reserve`_ `boolean`, _`temporary`_ `boolean`\]\) | \(_`slot_name`_ `name`, _`lsn`_ `pg_lsn`\) | Creates a new physical replication slot named _`slot_name`_. The optional second parameter, when `true`, specifies that the LSN for this replication slot be reserved immediately; otherwise the LSN is reserved on first connection from a streaming replication client. Streaming changes from a physical slot is only possible with the streaming-replication protocol — see [Section 52.4](https://www.postgresql.org/docs/12/protocol-replication.html). The optional third parameter, _`temporary`_, when set to true, specifies that the slot should not be permanently stored to disk and is only meant for use by current session. Temporary slots are also released upon any error. This function corresponds to the replication protocol command `CREATE_REPLICATION_SLOT ... PHYSICAL`. |
| `pg_drop_replication_slot(`_`slot_name`_ `name`\) | `void` | Drops the physical or logical replication slot named _`slot_name`_. Same as replication protocol command `DROP_REPLICATION_SLOT`. For logical slots, this must be called when connected to the same database the slot was created on. |
| `pg_create_logical_replication_slot(`_`slot_name`_ `name`, _`plugin`_ `name` \[, _`temporary`_ `boolean`\]\) | \(_`slot_name`_ `name`, _`lsn`_ `pg_lsn`\) | Creates a new logical \(decoding\) replication slot named _`slot_name`_ using the output plugin _`plugin`_. The optional third parameter, _`temporary`_, when set to true, specifies that the slot should not be permanently stored to disk and is only meant for use by current session. Temporary slots are also released upon any error. A call to this function has the same effect as the replication protocol command `CREATE_REPLICATION_SLOT ... LOGICAL`. |
| `pg_copy_physical_replication_slot(`_`src_slot_name`_ `name`, _`dst_slot_name`_ `name` \[, _`temporary`_ `boolean`\]\) | \(_`slot_name`_ `name`, _`lsn`_ `pg_lsn`\) | Copies an existing physical replication slot named _`src_slot_name`_ to a physical replication slot named _`dst_slot_name`_. The copied physical slot starts to reserve WAL from the same LSN as the source slot. _`temporary`_ is optional. If _`temporary`_ is omitted, the same value as the source slot is used. |
| `pg_copy_logical_replication_slot(`_`src_slot_name`_ `name`, _`dst_slot_name`_ `name` \[, _`temporary`_ `boolean` \[, _`plugin`_ `name`\]\]\) | \(_`slot_name`_ `name`, _`lsn`_ `pg_lsn`\) | Copies an existing logical replication slot named _`src_slot_name`_ to a logical replication slot named _`dst_slot_name`_ while changing the output plugin and persistence. The copied logical slot starts from the same LSN as the source logical slot. Both _`temporary`_ and _`plugin`_ are optional. If _`temporary`_ or _`plugin`_ are omitted, the same values as the source logical slot are used. |
| `pg_logical_slot_get_changes(`_`slot_name`_ `name`, _`upto_lsn`_ `pg_lsn`, _`upto_nchanges`_ `int`, VARIADIC _`options`_ `text[]`\) | \(_`lsn`_ `pg_lsn`, _`xid`_ `xid`, _`data`_ `text`\) | Returns changes in the slot _`slot_name`_, starting from the point at which since changes have been consumed last. If _`upto_lsn`_ and _`upto_nchanges`_ are NULL, logical decoding will continue until end of WAL. If _`upto_lsn`_ is non-NULL, decoding will include only those transactions which commit prior to the specified LSN. If _`upto_nchanges`_ is non-NULL, decoding will stop when the number of rows produced by decoding exceeds the specified value. Note, however, that the actual number of rows returned may be larger, since this limit is only checked after adding the rows produced when decoding each new transaction commit. |
| `pg_logical_slot_peek_changes(`_`slot_name`_ `name`, _`upto_lsn`_ `pg_lsn`, _`upto_nchanges`_ `int`, VARIADIC _`options`_ `text[]`\) | \(_`lsn`_ `pg_lsn`, _`xid`_ `xid`, _`data`_ `text`\) | Behaves just like the `pg_logical_slot_get_changes()` function, except that changes are not consumed; that is, they will be returned again on future calls. |
| `pg_logical_slot_get_binary_changes(`_`slot_name`_ `name`, _`upto_lsn`_ `pg_lsn`, _`upto_nchanges`_ `int`, VARIADIC _`options`_ `text[]`\) | \(_`lsn`_ `pg_lsn`, _`xid`_ `xid`, _`data`_ `bytea`\) | Behaves just like the `pg_logical_slot_get_changes()` function, except that changes are returned as `bytea`. |
| `pg_logical_slot_peek_binary_changes(`_`slot_name`_ `name`, _`upto_lsn`_ `pg_lsn`, _`upto_nchanges`_ `int`, VARIADIC _`options`_ `text[]`\) | \(_`lsn`_ `pg_lsn`, _`xid`_ `xid`, _`data`_ `bytea`\) | Behaves just like the `pg_logical_slot_get_changes()` function, except that changes are returned as `bytea` and that changes are not consumed; that is, they will be returned again on future calls. |
| `pg_replication_slot_advance(`_`slot_name`_ `name`, _`upto_lsn`_ `pg_lsn`\) | \(_`slot_name`_ `name`, _`end_lsn`_ `pg_lsn`\) `bool` | Advances the current confirmed position of a replication slot named _`slot_name`_. The slot will not be moved backwards, and it will not be moved beyond the current insert location. Returns the name of the slot and the real position to which it was advanced to. The information of the updated slot is written out at the follow-up checkpoint if any advancing is done. In the event of a crash, the slot may return to an earlier position. |
| `pg_replication_origin_create(`_`node_name`_ `text`\) | `oid` | Create a replication origin with the given external name, and return the internal id assigned to it. |
| `pg_replication_origin_drop(`_`node_name`_ `text`\) | `void` | Delete a previously created replication origin, including any associated replay progress. |
| `pg_replication_origin_oid(`_`node_name`_ `text`\) | `oid` | Lookup a replication origin by name and return the internal id. If no corresponding replication origin is found an error is thrown. |
| `pg_replication_origin_session_setup(`_`node_name`_ `text`\) | `void` | Mark the current session as replaying from the given origin, allowing replay progress to be tracked. Use `pg_replication_origin_session_reset` to revert. Can only be used if no previous origin is configured. |
| `pg_replication_origin_session_reset()` | `void` | Cancel the effects of `pg_replication_origin_session_setup()`. |
| `pg_replication_origin_session_is_setup()` | `bool` | Has a replication origin been configured in the current session? |
| `pg_replication_origin_session_progress(`_`flush`_ `bool`\) | `pg_lsn` | Return the replay location for the replication origin configured in the current session. The parameter _`flush`_ determines whether the corresponding local transaction will be guaranteed to have been flushed to disk or not. |
| `pg_replication_origin_xact_setup(`_`origin_lsn`_ `pg_lsn`, _`origin_timestamp`_ `timestamptz`\) | `void` | Mark the current transaction as replaying a transaction that has committed at the given LSN and timestamp. Can only be called when a replication origin has previously been configured using `pg_replication_origin_session_setup()`. |
| `pg_replication_origin_xact_reset()` | `void` | Cancel the effects of `pg_replication_origin_xact_setup()`. |
| `pg_replication_origin_advance(`_`node_name`_ `text`, _`lsn`_ `pg_lsn`\) | `void` | Set replication progress for the given node to the given location. This primarily is useful for setting up the initial location or a new location after configuration changes and similar. Be aware that careless use of this function can lead to inconsistently replicated data. |
| `pg_replication_origin_progress(`_`node_name`_ `text`, _`flush`_ `bool`\) | `pg_lsn` | Return the replay location for the given replication origin. The parameter _`flush`_ determines whether the corresponding local transaction will be guaranteed to have been flushed to disk or not. |
| `pg_logical_emit_message(`_`transactional`_ `bool`, _`prefix`_ `text`, _`content`_ `text`\) | `pg_lsn` | Emit text logical decoding message. This can be used to pass generic messages to logical decoding plugins through WAL. The parameter _`transactional`_ specifies if the message should be part of current transaction or if it should be written immediately and decoded as soon as the logical decoding reads the record. The _`prefix`_ is textual prefix used by the logical decoding plugins to easily recognize interesting messages for them. The _`content`_ is the text of the message. |
| `pg_logical_emit_message(`_`transactional`_ `bool`, _`prefix`_ `text`, _`content`_ `bytea`\) | `pg_lsn` | Emit binary logical decoding message. This can be used to pass generic messages to logical decoding plugins through WAL. The parameter _`transactional`_ specifies if the message should be part of current transaction or if it should be written immediately and decoded as soon as the logical decoding reads the record. The _`prefix`_ is textual prefix used by the logical decoding plugins to easily recognize interesting messages for them. The _`content`_ is the binary content of the message. |

## 9.26.7. Database Object Management Functions

The functions shown in [Table 9.89](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADMIN-DBSIZE) calculate the disk space usage of database objects.

#### **Table 9.89. Database Object Size Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_column_size(any`\) | `int` | Number of bytes used to store a particular value \(possibly compressed\) |
| `pg_database_size(oid`\) | `bigint` | Disk space used by the database with the specified OID |
| `pg_database_size(name`\) | `bigint` | Disk space used by the database with the specified name |
| `pg_indexes_size(regclass`\) | `bigint` | Total disk space used by indexes attached to the specified table |
| `pg_relation_size(`_`relation`_ `regclass`, _`fork`_ `text`\) | `bigint` | Disk space used by the specified fork \(`'main'`, `'fsm'`, `'vm'`, or `'init'`\) of the specified table or index |
| `pg_relation_size(`_`relation`_ `regclass`\) | `bigint` | Shorthand for `pg_relation_size(..., 'main')` |
| `pg_size_bytes(text`\) | `bigint` | Converts a size in human-readable format with size units into bytes |
| `pg_size_pretty(bigint`\) | `text` | Converts a size in bytes expressed as a 64-bit integer into a human-readable format with size units |
| `pg_size_pretty(numeric`\) | `text` | Converts a size in bytes expressed as a numeric value into a human-readable format with size units |
| `pg_table_size(regclass`\) | `bigint` | Disk space used by the specified table, excluding indexes \(but including TOAST, free space map, and visibility map\) |
| `pg_tablespace_size(oid`\) | `bigint` | Disk space used by the tablespace with the specified OID |
| `pg_tablespace_size(name`\) | `bigint` | Disk space used by the tablespace with the specified name |
| `pg_total_relation_size(regclass`\) | `bigint` | Total disk space used by the specified table, including all indexes and TOAST data |

`pg_column_size` shows the space used to store any individual data value.

`pg_total_relation_size` accepts the OID or name of a table or toast table, and returns the total on-disk space used for that table, including all associated indexes. This function is equivalent to `pg_table_size` `+` `pg_indexes_size`.

`pg_table_size` accepts the OID or name of a table and returns the disk space needed for that table, exclusive of indexes. \(TOAST space, free space map, and visibility map are included.\)

`pg_indexes_size` accepts the OID or name of a table and returns the total disk space used by all the indexes attached to that table.

`pg_database_size` and `pg_tablespace_size` accept the OID or name of a database or tablespace, and return the total disk space used therein. To use `pg_database_size`, you must have `CONNECT` permission on the specified database \(which is granted by default\), or be a member of the `pg_read_all_stats` role. To use `pg_tablespace_size`, you must have `CREATE` permission on the specified tablespace, or be a member of the `pg_read_all_stats` role unless it is the default tablespace for the current database.

`pg_relation_size` accepts the OID or name of a table, index or toast table, and returns the on-disk size in bytes of one fork of that relation. \(Note that for most purposes it is more convenient to use the higher-level functions `pg_total_relation_size` or `pg_table_size`, which sum the sizes of all forks.\) With one argument, it returns the size of the main data fork of the relation. The second argument can be provided to specify which fork to examine:

* `'main'` returns the size of the main data fork of the relation.
* `'fsm'` returns the size of the Free Space Map \(see [Section 68.3](https://www.postgresql.org/docs/12/storage-fsm.html)\) associated with the relation.
* `'vm'` returns the size of the Visibility Map \(see [Section 68.4](https://www.postgresql.org/docs/12/storage-vm.html)\) associated with the relation.
* `'init'` returns the size of the initialization fork, if any, associated with the relation.

`pg_size_pretty` can be used to format the result of one of the other functions in a human-readable way, using bytes, kB, MB, GB or TB as appropriate.

`pg_size_bytes` can be used to get the size in bytes from a string in human-readable format. The input may have units of bytes, kB, MB, GB or TB, and is parsed case-insensitively. If no units are specified, bytes are assumed.

#### Note

The units kB, MB, GB and TB used by the functions `pg_size_pretty` and `pg_size_bytes` are defined using powers of 2 rather than powers of 10, so 1kB is 1024 bytes, 1MB is 10242 = 1048576 bytes, and so on.

The functions above that operate on tables or indexes accept a `regclass` argument, which is simply the OID of the table or index in the `pg_class` system catalog. You do not have to look up the OID by hand, however, since the `regclass` data type's input converter will do the work for you. Just write the table name enclosed in single quotes so that it looks like a literal constant. For compatibility with the handling of ordinary SQL names, the string will be converted to lower case unless it contains double quotes around the table name.

If an OID that does not represent an existing object is passed as argument to one of the above functions, NULL is returned.

The functions shown in [Table 9.90](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADMIN-DBLOCATION) assist in identifying the specific disk files associated with database objects.

#### **Table 9.90. Database Object Location Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_relation_filenode(`_`relation`_ `regclass`\) | `oid` | Filenode number of the specified relation |
| `pg_relation_filepath(`_`relation`_ `regclass`\) | `text` | File path name of the specified relation |
| `pg_filenode_relation(`_`tablespace`_ `oid`, _`filenode`_ `oid`\) | `regclass` | Find the relation associated with a given tablespace and filenode |

`pg_relation_filenode` accepts the OID or name of a table, index, sequence, or toast table, and returns the “filenode” number currently assigned to it. The filenode is the base component of the file name\(s\) used for the relation \(see [Section 68.1](https://www.postgresql.org/docs/12/storage-file-layout.html) for more information\). For most tables the result is the same as `pg_class`.`relfilenode`, but for certain system catalogs `relfilenode` is zero and this function must be used to get the correct value. The function returns NULL if passed a relation that does not have storage, such as a view.

`pg_relation_filepath` is similar to `pg_relation_filenode`, but it returns the entire file path name \(relative to the database cluster's data directory `PGDATA`\) of the relation.

`pg_filenode_relation` is the reverse of `pg_relation_filenode`. Given a “tablespace” OID and a “filenode”, it returns the associated relation's OID. For a table in the database's default tablespace, the tablespace can be specified as 0.

[Table 9.91](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADMIN-COLLATION) lists functions used to manage collations.

#### **Table 9.91. Collation Management Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_collation_actual_version(oid`\) | `text` | Return actual version of collation from operating system |
| `pg_import_system_collations(`_`schema`_ `regnamespace`\) | `integer` | Import operating system collations |

`pg_collation_actual_version` returns the actual version of the collation object as it is currently installed in the operating system. If this is different from the value in `pg_collation.collversion`, then objects depending on the collation might need to be rebuilt. See also [ALTER COLLATION](https://www.postgresql.org/docs/12/sql-altercollation.html).

`pg_import_system_collations` adds collations to the system catalog `pg_collation` based on all the locales it finds in the operating system. This is what `initdb` uses; see [Section 23.2.2](https://www.postgresql.org/docs/12/collation.html#COLLATION-MANAGING) for more details. If additional locales are installed into the operating system later on, this function can be run again to add collations for the new locales. Locales that match existing entries in `pg_collation` will be skipped. \(But collation objects based on locales that are no longer present in the operating system are not removed by this function.\) The _`schema`_ parameter would typically be `pg_catalog`, but that is not a requirement; the collations could be installed into some other schema as well. The function returns the number of new collation objects it created.

#### **Table 9.92. Partitioning Information Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_partition_tree(regclass`\) | `setof record` | List information about tables or indexes in a partition tree for a given partitioned table or partitioned index, with one row for each partition. Information provided includes the name of the partition, the name of its immediate parent, a boolean value telling if the partition is a leaf, and an integer telling its level in the hierarchy. The value of level begins at `0` for the input table or index in its role as the root of the partition tree, `1` for its partitions, `2` for their partitions, and so on. |
| `pg_partition_ancestors(regclass`\) | `setof regclass` | List the ancestor relations of the given partition, including the partition itself. |
| `pg_partition_root(regclass`\) | `regclass` | Return the top-most parent of a partition tree to which the given relation belongs. |

To check the total size of the data contained in `measurement` table described in [Section 5.11.2.1](https://www.postgresql.org/docs/12/ddl-partitioning.html#DDL-PARTITIONING-DECLARATIVE-EXAMPLE), one could use the following query:

```text
=# SELECT pg_size_pretty(sum(pg_relation_size(relid))) AS total_size
     FROM pg_partition_tree('measurement');
 total_size 
------------
 24 kB
(1 row)
```

## 9.26.8. Index Maintenance Functions

[Table 9.93](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADMIN-INDEX-TABLE) shows the functions available for index maintenance tasks. These functions cannot be executed during recovery. Use of these functions is restricted to superusers and the owner of the given index.

#### **Table 9.93. Index Maintenance Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `brin_summarize_new_values(`_`index`_ `regclass`\) | `integer` | summarize page ranges not already summarized |
| `brin_summarize_range(`_`index`_ `regclass`, _`blockNumber`_ `bigint`\) | `integer` | summarize the page range covering the given block, if not already summarized |
| `brin_desummarize_range(`_`index`_ `regclass`, _`blockNumber`_ `bigint`\) | `integer` | de-summarize the page range covering the given block, if summarized |
| `gin_clean_pending_list(`_`index`_ `regclass`\) | `bigint` | move GIN pending list entries into main index structure |

`brin_summarize_new_values` accepts the OID or name of a BRIN index and inspects the index to find page ranges in the base table that are not currently summarized by the index; for any such range it creates a new summary index tuple by scanning the table pages. It returns the number of new page range summaries that were inserted into the index. `brin_summarize_range` does the same, except it only summarizes the range that covers the given block number.

`gin_clean_pending_list` accepts the OID or name of a GIN index and cleans up the pending list of the specified index by moving entries in it to the main GIN data structure in bulk. It returns the number of pages removed from the pending list. Note that if the argument is a GIN index built with the `fastupdate` option disabled, no cleanup happens and the return value is 0, because the index doesn't have a pending list. Please see [Section 66.4.1](https://www.postgresql.org/docs/12/gin-implementation.html#GIN-FAST-UPDATE) and [Section 66.5](https://www.postgresql.org/docs/12/gin-tips.html) for details of the pending list and `fastupdate` option.

## 9.26.9. Generic File Access Functions

The functions shown in [Table 9.94](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADMIN-GENFILE-TABLE) provide native access to files on the machine hosting the server. Only files within the database cluster directory and the `log_directory` can be accessed unless the user is granted the role `pg_read_server_files`. Use a relative path for files in the cluster directory, and a path matching the `log_directory` configuration setting for log files.

Note that granting users the EXECUTE privilege on `pg_read_file()`, or related functions, allows them the ability to read any file on the server which the database can read and that those reads bypass all in-database privilege checks. This means that, among other things, a user with this access is able to read the contents of the `pg_authid` table where authentication information is contained, as well as read any file in the database. Therefore, granting access to these functions should be carefully considered.

#### **Table 9.94. Generic File Access Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_ls_dir(`_`dirname`_ `text` \[, _`missing_ok`_ `boolean`, _`include_dot_dirs`_ `boolean`\]\) | `setof text` | List the contents of a directory. Restricted to superusers by default, but other users can be granted EXECUTE to run the function. |
| `pg_ls_logdir()` | `setof record` | List the name, size, and last modification time of files in the log directory. Access is granted to members of the `pg_monitor` role and may be granted to other non-superuser roles. |
| `pg_ls_waldir()` | `setof record` | List the name, size, and last modification time of files in the WAL directory. Access is granted to members of the `pg_monitor` role and may be granted to other non-superuser roles. |
| `pg_ls_archive_statusdir()` | `setof record` | List the name, size, and last modification time of files in the WAL archive status directory. Access is granted to members of the `pg_monitor` role and may be granted to other non-superuser roles. |
| `pg_ls_tmpdir([`_`tablespace`_ `oid`\]\) | `setof record` | List the name, size, and last modification time of files in the temporary directory for _`tablespace`_. If _`tablespace`_ is not provided, the `pg_default` tablespace is used. Access is granted to members of the `pg_monitor` role and may be granted to other non-superuser roles. |
| `pg_read_file(`_`filename`_ `text` \[, _`offset`_ `bigint`, _`length`_ `bigint` \[, _`missing_ok`_ `boolean`\] \]\) | `text` | Return the contents of a text file. Restricted to superusers by default, but other users can be granted EXECUTE to run the function. |
| `pg_read_binary_file(`_`filename`_ `text` \[, _`offset`_ `bigint`, _`length`_ `bigint` \[, _`missing_ok`_ `boolean`\] \]\) | `bytea` | Return the contents of a file. Restricted to superusers by default, but other users can be granted EXECUTE to run the function. |
| `pg_stat_file(`_`filename`_ `text`\[, _`missing_ok`_ `boolean`\]\) | `record` | Return information about a file. Restricted to superusers by default, but other users can be granted EXECUTE to run the function. |

Some of these functions take an optional _`missing_ok`_ parameter, which specifies the behavior when the file or directory does not exist. If `true`, the function returns NULL \(except `pg_ls_dir`, which returns an empty result set\). If `false`, an error is raised. The default is `false`.

`pg_ls_dir` returns the names of all files \(and directories and other special files\) in the specified directory. The _`include_dot_dirs`_ indicates whether “.” and “..” are included in the result set. The default is to exclude them \(`false`\), but including them can be useful when _`missing_ok`_ is `true`, to distinguish an empty directory from an non-existent directory.

`pg_ls_logdir` returns the name, size, and last modified time \(mtime\) of each file in the log directory. By default, only superusers and members of the `pg_monitor` role can use this function. Access may be granted to others using `GRANT`.

`pg_ls_waldir` returns the name, size, and last modified time \(mtime\) of each file in the write ahead log \(WAL\) directory. By default only superusers and members of the `pg_monitor` role can use this function. Access may be granted to others using `GRANT`.

`pg_ls_archive_statusdir` returns the name, size, and last modified time \(mtime\) of each file in the WAL archive status directory `pg_wal/archive_status`. By default only superusers and members of the `pg_monitor` role can use this function. Access may be granted to others using `GRANT`.

`pg_ls_tmpdir` returns the name, size, and last modified time \(mtime\) of each file in the temporary file directory for the specified _`tablespace`_. If _`tablespace`_ is not provided, the `pg_default` tablespace is used. By default only superusers and members of the `pg_monitor` role can use this function. Access may be granted to others using `GRANT`.

`pg_read_file` returns part of a text file, starting at the given _`offset`_, returning at most _`length`_ bytes \(less if the end of file is reached first\). If _`offset`_ is negative, it is relative to the end of the file. If _`offset`_ and _`length`_ are omitted, the entire file is returned. The bytes read from the file are interpreted as a string in the server encoding; an error is thrown if they are not valid in that encoding.

`pg_read_binary_file` is similar to `pg_read_file`, except that the result is a `bytea` value; accordingly, no encoding checks are performed. In combination with the `convert_from` function, this function can be used to read a file in a specified encoding:

```text
SELECT convert_from(pg_read_binary_file('file_in_utf8.txt'), 'UTF8');
```

`pg_stat_file` returns a record containing the file size, last accessed time stamp, last modified time stamp, last file status change time stamp \(Unix platforms only\), file creation time stamp \(Windows only\), and a `boolean` indicating if it is a directory. Typical usages include:

```text
SELECT * FROM pg_stat_file('filename');
SELECT (pg_stat_file('filename')).modification;
```

## 9.26.10. Advisory Lock Functions

The functions shown in [Table 9.95](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADVISORY-LOCKS-TABLE) manage advisory locks. For details about proper use of these functions, see [Section 13.3.5](https://www.postgresql.org/docs/12/explicit-locking.html#ADVISORY-LOCKS).

#### **Table 9.95. Advisory Lock Functions**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_advisory_lock(`_`key`_ `bigint`\) | `void` | Obtain exclusive session level advisory lock |
| `pg_advisory_lock(`_`key1`_ `int`, _`key2`_ `int`\) | `void` | Obtain exclusive session level advisory lock |
| `pg_advisory_lock_shared(`_`key`_ `bigint`\) | `void` | Obtain shared session level advisory lock |
| `pg_advisory_lock_shared(`_`key1`_ `int`, _`key2`_ `int`\) | `void` | Obtain shared session level advisory lock |
| `pg_advisory_unlock(`_`key`_ `bigint`\) | `boolean` | Release an exclusive session level advisory lock |
| `pg_advisory_unlock(`_`key1`_ `int`, _`key2`_ `int`\) | `boolean` | Release an exclusive session level advisory lock |
| `pg_advisory_unlock_all()` | `void` | Release all session level advisory locks held by the current session |
| `pg_advisory_unlock_shared(`_`key`_ `bigint`\) | `boolean` | Release a shared session level advisory lock |
| `pg_advisory_unlock_shared(`_`key1`_ `int`, _`key2`_ `int`\) | `boolean` | Release a shared session level advisory lock |
| `pg_advisory_xact_lock(`_`key`_ `bigint`\) | `void` | Obtain exclusive transaction level advisory lock |
| `pg_advisory_xact_lock(`_`key1`_ `int`, _`key2`_ `int`\) | `void` | Obtain exclusive transaction level advisory lock |
| `pg_advisory_xact_lock_shared(`_`key`_ `bigint`\) | `void` | Obtain shared transaction level advisory lock |
| `pg_advisory_xact_lock_shared(`_`key1`_ `int`, _`key2`_ `int`\) | `void` | Obtain shared transaction level advisory lock |
| `pg_try_advisory_lock(`_`key`_ `bigint`\) | `boolean` | Obtain exclusive session level advisory lock if available |
| `pg_try_advisory_lock(`_`key1`_ `int`, _`key2`_ `int`\) | `boolean` | Obtain exclusive session level advisory lock if available |
| `pg_try_advisory_lock_shared(`_`key`_ `bigint`\) | `boolean` | Obtain shared session level advisory lock if available |
| `pg_try_advisory_lock_shared(`_`key1`_ `int`, _`key2`_ `int`\) | `boolean` | Obtain shared session level advisory lock if available |
| `pg_try_advisory_xact_lock(`_`key`_ `bigint`\) | `boolean` | Obtain exclusive transaction level advisory lock if available |
| `pg_try_advisory_xact_lock(`_`key1`_ `int`, _`key2`_ `int`\) | `boolean` | Obtain exclusive transaction level advisory lock if available |
| `pg_try_advisory_xact_lock_shared(`_`key`_ `bigint`\) | `boolean` | Obtain shared transaction level advisory lock if available |
| `pg_try_advisory_xact_lock_shared(`_`key1`_ `int`, _`key2`_ `int`\) | `boolean` | Obtain shared transaction level advisory lock if available |

`pg_advisory_lock` locks an application-defined resource, which can be identified either by a single 64-bit key value or two 32-bit key values \(note that these two key spaces do not overlap\). If another session already holds a lock on the same resource identifier, this function will wait until the resource becomes available. The lock is exclusive. Multiple lock requests stack, so that if the same resource is locked three times it must then be unlocked three times to be released for other sessions' use.

`pg_advisory_lock_shared` works the same as `pg_advisory_lock`, except the lock can be shared with other sessions requesting shared locks. Only would-be exclusive lockers are locked out.

`pg_try_advisory_lock` is similar to `pg_advisory_lock`, except the function will not wait for the lock to become available. It will either obtain the lock immediately and return `true`, or return `false` if the lock cannot be acquired immediately.

`pg_try_advisory_lock_shared` works the same as `pg_try_advisory_lock`, except it attempts to acquire a shared rather than an exclusive lock.

`pg_advisory_unlock` will release a previously-acquired exclusive session level advisory lock. It returns `true` if the lock is successfully released. If the lock was not held, it will return `false`, and in addition, an SQL warning will be reported by the server.

`pg_advisory_unlock_shared` works the same as `pg_advisory_unlock`, except it releases a shared session level advisory lock.

`pg_advisory_unlock_all` will release all session level advisory locks held by the current session. \(This function is implicitly invoked at session end, even if the client disconnects ungracefully.\)

`pg_advisory_xact_lock` works the same as `pg_advisory_lock`, except the lock is automatically released at the end of the current transaction and cannot be released explicitly.

`pg_advisory_xact_lock_shared` works the same as `pg_advisory_lock_shared`, except the lock is automatically released at the end of the current transaction and cannot be released explicitly.

`pg_try_advisory_xact_lock` works the same as `pg_try_advisory_lock`, except the lock, if acquired, is automatically released at the end of the current transaction and cannot be released explicitly.

`pg_try_advisory_xact_lock_shared` works the same as `pg_try_advisory_lock_shared`, except the lock, if acquired, is automatically released at the end of the current transaction and cannot be released explicitly.

