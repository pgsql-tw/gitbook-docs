# 19.5. Write Ahead Log

For additional information on tuning these settings, see [Section 29.4](https://www.postgresql.org/docs/12/wal-configuration.html).

## 19.5.1. Settings

#### `wal_level` \(`enum`\)

`wal_level` determines how much information is written to the WAL. The default value is `replica`, which writes enough data to support WAL archiving and replication, including running read-only queries on a standby server. `minimal` removes all logging except the information required to recover from a crash or immediate shutdown. Finally, `logical` adds information necessary to support logical decoding. Each level includes the information logged at all lower levels. This parameter can only be set at server start.

In `minimal` level, WAL-logging of some bulk operations can be safely skipped, which can make those operations much faster \(see [Section 14.4.7](https://www.postgresql.org/docs/12/populate.html#POPULATE-PITR)\). Operations in which this optimization can be applied include:

| `CREATE TABLE AS` |
| :--- |
| `CREATE INDEX` |
| `CLUSTER` |
| `COPY` into tables that were created or truncated in the same transaction |

But minimal WAL does not contain enough information to reconstruct the data from a base backup and the WAL logs, so `replica` or higher must be used to enable WAL archiving \([archive\_mode](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-ARCHIVE-MODE)\) and streaming replication.

In `logical` level, the same information is logged as with `replica`, plus information needed to allow extracting logical change sets from the WAL. Using a level of `logical` will increase the WAL volume, particularly if many tables are configured for `REPLICA IDENTITY FULL` and many `UPDATE` and `DELETE` statements are executed.

In releases prior to 9.6, this parameter also allowed the values `archive` and `hot_standby`. These are still accepted but mapped to `replica`.

#### `fsync` \(`boolean`\)

If this parameter is on, the PostgreSQL server will try to make sure that updates are physically written to disk, by issuing `fsync()` system calls or various equivalent methods \(see [wal\_sync\_method](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-WAL-SYNC-METHOD)\). This ensures that the database cluster can recover to a consistent state after an operating system or hardware crash.

While turning off `fsync` is often a performance benefit, this can result in unrecoverable data corruption in the event of a power failure or system crash. Thus it is only advisable to turn off `fsync` if you can easily recreate your entire database from external data.

Examples of safe circumstances for turning off `fsync` include the initial loading of a new database cluster from a backup file, using a database cluster for processing a batch of data after which the database will be thrown away and recreated, or for a read-only database clone which gets recreated frequently and is not used for failover. High quality hardware alone is not a sufficient justification for turning off `fsync`.

For reliable recovery when changing `fsync` off to on, it is necessary to force all modified buffers in the kernel to durable storage. This can be done while the cluster is shutdown or while `fsync` is on by running `initdb --sync-only`, running `sync`, unmounting the file system, or rebooting the server.

In many situations, turning off [synchronous\_commit](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT) for noncritical transactions can provide much of the potential performance benefit of turning off `fsync`, without the attendant risks of data corruption.

`fsync` can only be set in the `postgresql.conf` file or on the server command line. If you turn this parameter off, also consider turning off [full\_page\_writes](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-FULL-PAGE-WRITES).

#### `synchronous_commit` \(`enum`\)

Specifies whether transaction commit will wait for WAL records to be written to disk before the command returns a “success” indication to the client. Valid values are `on`, `remote_apply`, `remote_write`, `local`, and `off`. The default, and safe, setting is `on`. When `off`, there can be a delay between when success is reported to the client and when the transaction is really guaranteed to be safe against a server crash. \(The maximum delay is three times [wal\_writer\_delay](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-WAL-WRITER-DELAY).\) Unlike [fsync](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-FSYNC), setting this parameter to `off` does not create any risk of database inconsistency: an operating system or database crash might result in some recent allegedly-committed transactions being lost, but the database state will be just the same as if those transactions had been aborted cleanly. So, turning `synchronous_commit` off can be a useful alternative when performance is more important than exact certainty about the durability of a transaction. For more discussion see [Section 29.3](https://www.postgresql.org/docs/12/wal-async-commit.html).

If [synchronous\_standby\_names](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-SYNCHRONOUS-STANDBY-NAMES) is non-empty, this parameter also controls whether or not transaction commits will wait for their WAL records to be replicated to the standby server\(s\). When set to `on`, commits will wait until replies from the current synchronous standby\(s\) indicate they have received the commit record of the transaction and flushed it to disk. This ensures the transaction will not be lost unless both the primary and all synchronous standbys suffer corruption of their database storage. When set to `remote_apply`, commits will wait until replies from the current synchronous standby\(s\) indicate they have received the commit record of the transaction and applied it, so that it has become visible to queries on the standby\(s\). When set to `remote_write`, commits will wait until replies from the current synchronous standby\(s\) indicate they have received the commit record of the transaction and written it out to their operating system. This setting is sufficient to ensure data preservation even if a standby instance of PostgreSQL were to crash, but not if the standby suffers an operating-system-level crash, since the data has not necessarily reached stable storage on the standby. Finally, the setting `local` causes commits to wait for local flush to disk, but not for replication. This is not usually desirable when synchronous replication is in use, but is provided for completeness.

If `synchronous_standby_names` is empty, the settings `on`, `remote_apply`, `remote_write` and `local` all provide the same synchronization level: transaction commits only wait for local flush to disk.

This parameter can be changed at any time; the behavior for any one transaction is determined by the setting in effect when it commits. It is therefore possible, and useful, to have some transactions commit synchronously and others asynchronously. For example, to make a single multistatement transaction commit asynchronously when the default is the opposite, issue `SET LOCAL synchronous_commit TO OFF` within the transaction.

#### `wal_sync_method` \(`enum`\)

Method used for forcing WAL updates out to disk. If `fsync` is off then this setting is irrelevant, since WAL file updates will not be forced out at all. Possible values are:

* `open_datasync` \(write WAL files with `open()` option `O_DSYNC`\)
* `fdatasync` \(call `fdatasync()` at each commit\)
* `fsync` \(call `fsync()` at each commit\)
* `fsync_writethrough` \(call `fsync()` at each commit, forcing write-through of any disk write cache\)
* `open_sync` \(write WAL files with `open()` option `O_SYNC`\)

The `open_`\* options also use `O_DIRECT` if available. Not all of these choices are available on all platforms. The default is the first method in the above list that is supported by the platform, except that `fdatasync` is the default on Linux. The default is not necessarily ideal; it might be necessary to change this setting or other aspects of your system configuration in order to create a crash-safe configuration or achieve optimal performance. These aspects are discussed in [Section 29.1](https://www.postgresql.org/docs/12/wal-reliability.html). This parameter can only be set in the `postgresql.conf` file or on the server command line.

#### `full_page_writes` \(`boolean`\)

啟用此參數後，PostgreSQL 伺服器會在檢查點之後對該頁面的首次修改期間將每個磁碟頁面的全部內容寫入 WAL。這是必要的，因為在作業系統當機期間正在進行的頁面寫入可能僅部分完成，從而導致包含新舊資料混合在磁碟頁面之中。通常在 WAL 中所儲存的資料列層級更改資料不足以在當機後還原期間完全還原此類頁面。儲存完整的頁面映像可確保還原正確的頁面，但是這樣做的代價是增加了必須寫入 WAL 的資料量。 （由於 WAL 重放總是從檢查點開始，因此在檢查點之後每頁的第一次更改期間執行此操作就足夠了。也因此，減少全頁寫入成本的一種方法是增加檢查點間隔參數。）

停用此參數可加快正常操作的速度，但在系統故障後可能會導致不可恢復的資料損壞或未知的資料損壞。風險與關閉 fsync 相似，儘管較小，但應僅根據針對該參數建議的相同情況將其關閉。

禁用此參數不會影響使用 WAL 歸檔進行時間點還原作業（PITR）（請參閱[第 25.3 節](../backup-and-restore/25.3.-continuous-archiving-and-point-in-time-recovery-pitr.md)）。

該參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設為 on。

#### `wal_log_hints` \(`boolean`\)

When this parameter is `on`, the PostgreSQL server writes the entire content of each disk page to WAL during the first modification of that page after a checkpoint, even for non-critical modifications of so-called hint bits.

If data checksums are enabled, hint bit updates are always WAL-logged and this setting is ignored. You can use this setting to test how much extra WAL-logging would occur if your database had data checksums enabled.

This parameter can only be set at server start. The default value is `off`.

#### `wal_compression` \(`boolean`\)

When this parameter is `on`, the PostgreSQL server compresses a full page image written to WAL when [full\_page\_writes](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-FULL-PAGE-WRITES) is on or during a base backup. A compressed page image will be decompressed during WAL replay. The default value is `off`. Only superusers can change this setting.

Turning this parameter on can reduce the WAL volume without increasing the risk of unrecoverable data corruption, but at the cost of some extra CPU spent on the compression during WAL logging and on the decompression during WAL replay.

#### `wal_buffers` \(`integer`\)

The amount of shared memory used for WAL data that has not yet been written to disk. The default setting of -1 selects a size equal to 1/32nd \(about 3%\) of [shared\_buffers](https://www.postgresql.org/docs/12/runtime-config-resource.html#GUC-SHARED-BUFFERS), but not less than `64kB` nor more than the size of one WAL segment, typically `16MB`. This value can be set manually if the automatic choice is too large or too small, but any positive value less than `32kB` will be treated as `32kB`. If this value is specified without units, it is taken as WAL blocks, that is `XLOG_BLCKSZ` bytes, typically 8kB. This parameter can only be set at server start.

The contents of the WAL buffers are written out to disk at every transaction commit, so extremely large values are unlikely to provide a significant benefit. However, setting this value to at least a few megabytes can improve write performance on a busy server where many clients are committing at once. The auto-tuning selected by the default setting of -1 should give reasonable results in most cases.

#### `wal_writer_delay` \(`integer`\)

Specifies how often the WAL writer flushes WAL, in time terms. After flushing WAL the writer sleeps for the length of time given by `wal_writer_delay`, unless woken up sooner by an asynchronously committing transaction. If the last flush happened less than `wal_writer_delay` ago and less than `wal_writer_flush_after` worth of WAL has been produced since, then WAL is only written to the operating system, not flushed to disk. If this value is specified without units, it is taken as milliseconds. The default value is 200 milliseconds \(`200ms`\). Note that on many systems, the effective resolution of sleep delays is 10 milliseconds; setting `wal_writer_delay` to a value that is not a multiple of 10 might have the same results as setting it to the next higher multiple of 10. This parameter can only be set in the `postgresql.conf` file or on the server command line.

#### `wal_writer_flush_after` \(`integer`\)

Specifies how often the WAL writer flushes WAL, in volume terms. If the last flush happened less than `wal_writer_delay` ago and less than `wal_writer_flush_after` worth of WAL has been produced since, then WAL is only written to the operating system, not flushed to disk. If `wal_writer_flush_after` is set to `0` then WAL data is always flushed immediately. If this value is specified without units, it is taken as WAL blocks, that is `XLOG_BLCKSZ` bytes, typically 8kB. The default is `1MB`. This parameter can only be set in the `postgresql.conf` file or on the server command line.

#### `commit_delay` \(`integer`\)

Setting `commit_delay` adds a time delay before a WAL flush is initiated. This can improve group commit throughput by allowing a larger number of transactions to commit via a single WAL flush, if system load is high enough that additional transactions become ready to commit within the given interval. However, it also increases latency by up to the `commit_delay` for each WAL flush. Because the delay is just wasted if no other transactions become ready to commit, a delay is only performed if at least `commit_siblings` other transactions are active when a flush is about to be initiated. Also, no delays are performed if `fsync` is disabled. If this value is specified without units, it is taken as microseconds. The default `commit_delay` is zero \(no delay\). Only superusers can change this setting.

In PostgreSQL releases prior to 9.3, `commit_delay` behaved differently and was much less effective: it affected only commits, rather than all WAL flushes, and waited for the entire configured delay even if the WAL flush was completed sooner. Beginning in PostgreSQL 9.3, the first process that becomes ready to flush waits for the configured interval, while subsequent processes wait only until the leader completes the flush operation.

#### `commit_siblings` \(`integer`\)

Minimum number of concurrent open transactions to require before performing the `commit_delay` delay. A larger value makes it more probable that at least one other transaction will become ready to commit during the delay interval. The default is five transactions.

## 19.5.2. Checkpoints

#### `checkpoint_timeout` \(`integer`\)

自動 WAL 檢查點之間的最長時間。如果指定的值不帶單位，則以秒為單位。有效範圍是 30 秒至 1 天。預設值為五分鐘（5 分鐘）。增大此參數可能會增加當機回復所需的時間。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

#### `checkpoint_completion_target` \(`floating point`\)

指定檢查點完成的目標，佔檢查點之間總時間的一部分。預設值為 0.5。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

`checkpoint_flush_after` \(`integer`\)

Whenever more than this amount of data has been written while performing a checkpoint, attempt to force the OS to issue these writes to the underlying storage. Doing so will limit the amount of dirty data in the kernel's page cache, reducing the likelihood of stalls when an `fsync` is issued at the end of the checkpoint, or when the OS writes data back in larger batches in the background. Often that will result in greatly reduced transaction latency, but there also are some cases, especially with workloads that are bigger than [shared\_buffers](https://www.postgresql.org/docs/12/runtime-config-resource.html#GUC-SHARED-BUFFERS), but smaller than the OS's page cache, where performance might degrade. This setting may have no effect on some platforms. If this value is specified without units, it is taken as blocks, that is `BLCKSZ` bytes, typically 8kB. The valid range is between `0`, which disables forced writeback, and `2MB`. The default is `256kB` on Linux, `0` elsewhere. \(If `BLCKSZ` is not 8kB, the default and maximum values scale proportionally to it.\) This parameter can only be set in the `postgresql.conf` file or on the server command line.

#### `checkpoint_warning` \(`integer`\)

Write a message to the server log if checkpoints caused by the filling of WAL segment files happen closer together than this amount of time \(which suggests that `max_wal_size` ought to be raised\). If this value is specified without units, it is taken as seconds. The default is 30 seconds \(`30s`\). Zero disables the warning. No warnings will be generated if `checkpoint_timeout` is less than `checkpoint_warning`. This parameter can only be set in the `postgresql.conf` file or on the server command line.

#### `max_wal_size` \(`integer`\)

使 WAL 增長到自動 WAL 檢查點之間的最大大小。這是一個軟限制。在特殊情況下，例如重度負載，失敗的 archive\_command 或較高的 wal\_keep\_segments 設定，WAL 大小可能會超過 max\_wal\_size。如果指定的該值不帶單位，則以 MegaByte 為單位。預設值為1 GB。增大此參數可能會增加當機回復所需的時間。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

#### `min_wal_size` \(`integer`\)

As long as WAL disk usage stays below this setting, old WAL files are always recycled for future use at a checkpoint, rather than removed. This can be used to ensure that enough WAL space is reserved to handle spikes in WAL usage, for example when running large batch jobs. If this value is specified without units, it is taken as megabytes. The default is 80 MB. This parameter can only be set in the `postgresql.conf` file or on the server command line.

## 19.5.3. Archiving

`archive_mode` \(`enum`\)

When `archive_mode` is enabled, completed WAL segments are sent to archive storage by setting [archive\_command](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-ARCHIVE-COMMAND). In addition to `off`, to disable, there are two modes: `on`, and `always`. During normal operation, there is no difference between the two modes, but when set to `always` the WAL archiver is enabled also during archive recovery or standby mode. In `always` mode, all files restored from the archive or streamed with streaming replication will be archived \(again\). See [Section 26.2.9](https://www.postgresql.org/docs/12/warm-standby.html#CONTINUOUS-ARCHIVING-IN-STANDBY) for details.

`archive_mode` and `archive_command` are separate variables so that `archive_command` can be changed without leaving archiving mode. This parameter can only be set at server start. `archive_mode` cannot be enabled when `wal_level` is set to `minimal`.

`archive_command` \(`string`\)

The local shell command to execute to archive a completed WAL file segment. Any `%p` in the string is replaced by the path name of the file to archive, and any `%f` is replaced by only the file name. \(The path name is relative to the working directory of the server, i.e., the cluster's data directory.\) Use `%%` to embed an actual `%` character in the command. It is important for the command to return a zero exit status only if it succeeds. For more information see [Section 25.3.1](https://www.postgresql.org/docs/12/continuous-archiving.html#BACKUP-ARCHIVING-WAL).

This parameter can only be set in the `postgresql.conf` file or on the server command line. It is ignored unless `archive_mode` was enabled at server start. If `archive_command` is an empty string \(the default\) while `archive_mode` is enabled, WAL archiving is temporarily disabled, but the server continues to accumulate WAL segment files in the expectation that a command will soon be provided. Setting `archive_command` to a command that does nothing but return true, e.g. `/bin/true` \(`REM` on Windows\), effectively disables archiving, but also breaks the chain of WAL files needed for archive recovery, so it should only be used in unusual circumstances.

`archive_timeout` \(`integer`\)

The [archive\_command](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-ARCHIVE-COMMAND) is only invoked for completed WAL segments. Hence, if your server generates little WAL traffic \(or has slack periods where it does so\), there could be a long delay between the completion of a transaction and its safe recording in archive storage. To limit how old unarchived data can be, you can set `archive_timeout` to force the server to switch to a new WAL segment file periodically. When this parameter is greater than zero, the server will switch to a new segment file whenever this amount of time has elapsed since the last segment file switch, and there has been any database activity, including a single checkpoint \(checkpoints are skipped if there is no database activity\). Note that archived files that are closed early due to a forced switch are still the same length as completely full files. Therefore, it is unwise to use a very short `archive_timeout` — it will bloat your archive storage. `archive_timeout` settings of a minute or so are usually reasonable. You should consider using streaming replication, instead of archiving, if you want data to be copied off the master server more quickly than that. If this value is specified without units, it is taken as seconds. This parameter can only be set in the `postgresql.conf` file or on the server command line.

## 19.5.4. Archive Recovery

This section describes the settings that apply only for the duration of the recovery. They must be reset for any subsequent recovery you wish to perform.

“Recovery” covers using the server as a standby or for executing a targeted recovery. Typically, standby mode would be used to provide high availability and/or read scalability, whereas a targeted recovery is used to recover from data loss.

To start the server in standby mode, create a file called `standby.signal` in the data directory. The server will enter recovery and will not stop recovery when the end of archived WAL is reached, but will keep trying to continue recovery by connecting to the sending server as specified by the `primary_conninfo` setting and/or by fetching new WAL segments using `restore_command`. For this mode, the parameters from this section and [Section 19.6.3](https://www.postgresql.org/docs/12/runtime-config-replication.html#RUNTIME-CONFIG-REPLICATION-STANDBY) are of interest. Parameters from [Section 19.5.5](https://www.postgresql.org/docs/12/runtime-config-wal.html#RUNTIME-CONFIG-WAL-RECOVERY-TARGET) will also be applied but are typically not useful in this mode.

To start the server in targeted recovery mode, create a file called `recovery.signal` in the data directory. If both `standby.signal` and `recovery.signal` files are created, standby mode takes precedence. Targeted recovery mode ends when the archived WAL is fully replayed, or when `recovery_target` is reached. In this mode, the parameters from both this section and [Section 19.5.5](https://www.postgresql.org/docs/12/runtime-config-wal.html#RUNTIME-CONFIG-WAL-RECOVERY-TARGET) will be used.

#### `restore_command` \(`string`\)

The local shell command to execute to retrieve an archived segment of the WAL file series. This parameter is required for archive recovery, but optional for streaming replication. Any `%f` in the string is replaced by the name of the file to retrieve from the archive, and any `%p` is replaced by the copy destination path name on the server. \(The path name is relative to the current working directory, i.e., the cluster's data directory.\) Any `%r` is replaced by the name of the file containing the last valid restart point. That is the earliest file that must be kept to allow a restore to be restartable, so this information can be used to truncate the archive to just the minimum required to support restarting from the current restore. `%r` is typically only used by warm-standby configurations \(see [Section 26.2](https://www.postgresql.org/docs/12/warm-standby.html)\). Write `%%` to embed an actual `%` character.

It is important for the command to return a zero exit status only if it succeeds. The command _will_ be asked for file names that are not present in the archive; it must return nonzero when so asked. Examples:

```text
restore_command = 'cp /mnt/server/archivedir/%f "%p"'
restore_command = 'copy "C:\\server\\archivedir\\%f" "%p"'  # Windows
```

An exception is that if the command was terminated by a signal \(other than SIGTERM, which is used as part of a database server shutdown\) or an error by the shell \(such as command not found\), then recovery will abort and the server will not start up.

This parameter can only be set at server start.

#### `archive_cleanup_command` \(`string`\)

This optional parameter specifies a shell command that will be executed at every restartpoint. The purpose of `archive_cleanup_command` is to provide a mechanism for cleaning up old archived WAL files that are no longer needed by the standby server. Any `%r` is replaced by the name of the file containing the last valid restart point. That is the earliest file that must be _kept_ to allow a restore to be restartable, and so all files earlier than `%r` may be safely removed. This information can be used to truncate the archive to just the minimum required to support restart from the current restore. The [pg\_archivecleanup](https://www.postgresql.org/docs/12/pgarchivecleanup.html) module is often used in `archive_cleanup_command` for single-standby configurations, for example:

```text
archive_cleanup_command = 'pg_archivecleanup /mnt/server/archivedir %r'
```

Note however that if multiple standby servers are restoring from the same archive directory, you will need to ensure that you do not delete WAL files until they are no longer needed by any of the servers. `archive_cleanup_command` would typically be used in a warm-standby configuration \(see [Section 26.2](https://www.postgresql.org/docs/12/warm-standby.html)\). Write `%%` to embed an actual `%` character in the command.

If the command returns a nonzero exit status then a warning log message will be written. An exception is that if the command was terminated by a signal or an error by the shell \(such as command not found\), a fatal error will be raised.

This parameter can only be set in the `postgresql.conf` file or on the server command line.

#### `recovery_end_command` \(`string`\)

This parameter specifies a shell command that will be executed once only at the end of recovery. This parameter is optional. The purpose of the `recovery_end_command` is to provide a mechanism for cleanup following replication or recovery. Any `%r` is replaced by the name of the file containing the last valid restart point, like in [archive\_cleanup\_command](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-ARCHIVE-CLEANUP-COMMAND).

If the command returns a nonzero exit status then a warning log message will be written and the database will proceed to start up anyway. An exception is that if the command was terminated by a signal or an error by the shell \(such as command not found\), the database will not proceed with startup.

This parameter can only be set in the `postgresql.conf` file or on the server command line.

## 19.5.5. Recovery Target

By default, recovery will recover to the end of the WAL log. The following parameters can be used to specify an earlier stopping point. At most one of `recovery_target`, `recovery_target_lsn`, `recovery_target_name`, `recovery_target_time`, or `recovery_target_xid` can be used; if more than one of these is specified in the configuration file, an error will be raised. These parameters can only be set at server start.

#### `recovery_target` `= 'immediate'`

This parameter specifies that recovery should end as soon as a consistent state is reached, i.e. as early as possible. When restoring from an online backup, this means the point where taking the backup ended.

Technically, this is a string parameter, but `'immediate'` is currently the only allowed value.

#### `recovery_target_name` \(`string`\)

This parameter specifies the named restore point \(created with `pg_create_restore_point()`\) to which recovery will proceed.

#### `recovery_target_time` \(`timestamp`\)

This parameter specifies the time stamp up to which recovery will proceed. The precise stopping point is also influenced by [recovery\_target\_inclusive](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-RECOVERY-TARGET-INCLUSIVE).

#### `recovery_target_xid` \(`string`\)

This parameter specifies the transaction ID up to which recovery will proceed. Keep in mind that while transaction IDs are assigned sequentially at transaction start, transactions can complete in a different numeric order. The transactions that will be recovered are those that committed before \(and optionally including\) the specified one. The precise stopping point is also influenced by [recovery\_target\_inclusive](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-RECOVERY-TARGET-INCLUSIVE).

#### `recovery_target_lsn` \(`pg_lsn`\)

This parameter specifies the LSN of the write-ahead log location up to which recovery will proceed. The precise stopping point is also influenced by [recovery\_target\_inclusive](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-RECOVERY-TARGET-INCLUSIVE). This parameter is parsed using the system data type [`pg_lsn`](https://www.postgresql.org/docs/12/datatype-pg-lsn.html).

The following options further specify the recovery target, and affect what happens when the target is reached:

#### `recovery_target_inclusive` \(`boolean`\)

Specifies whether to stop just after the specified recovery target \(`on`\), or just before the recovery target \(`off`\). Applies when [recovery\_target\_lsn](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-RECOVERY-TARGET-LSN), [recovery\_target\_time](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-RECOVERY-TARGET-TIME), or [recovery\_target\_xid](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-RECOVERY-TARGET-XID) is specified. This setting controls whether transactions having exactly the target WAL location \(LSN\), commit time, or transaction ID, respectively, will be included in the recovery. Default is `on`.

#### `recovery_target_timeline` \(`string`\)

Specifies recovering into a particular timeline. The value can be a numeric timeline ID or a special value. The value `current` recovers along the same timeline that was current when the base backup was taken. The value `latest` recovers to the latest timeline found in the archive, which is useful in a standby server. `latest` is the default.

You usually only need to set this parameter in complex re-recovery situations, where you need to return to a state that itself was reached after a point-in-time recovery. See [Section 25.3.5](https://www.postgresql.org/docs/12/continuous-archiving.html#BACKUP-TIMELINES) for discussion.

#### `recovery_target_action` \(`enum`\)

Specifies what action the server should take once the recovery target is reached. The default is `pause`, which means recovery will be paused. `promote` means the recovery process will finish and the server will start to accept connections. Finally `shutdown` will stop the server after reaching the recovery target.

The intended use of the `pause` setting is to allow queries to be executed against the database to check if this recovery target is the most desirable point for recovery. The paused state can be resumed by using `pg_wal_replay_resume()` \(see [Table 9.86](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL-TABLE)\), which then causes recovery to end. If this recovery target is not the desired stopping point, then shut down the server, change the recovery target settings to a later target and restart to continue recovery.

The `shutdown` setting is useful to have the instance ready at the exact replay point desired. The instance will still be able to replay more WAL records \(and in fact will have to replay WAL records since the last checkpoint next time it is started\).

Note that because `recovery.signal` will not be removed when `recovery_target_action` is set to `shutdown`, any subsequent start will end with immediate shutdown unless the configuration is changed or the `recovery.signal` file is removed manually.

This setting has no effect if no recovery target is set. If [hot\_standby](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-HOT-STANDBY) is not enabled, a setting of `pause` will act the same as `shutdown`.

