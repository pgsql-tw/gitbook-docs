# 19.5. Write Ahead Log

For additional information on tuning these settings, see [Section 30.4](https://www.postgresql.org/docs/10/static/wal-configuration.html).

## 19.5.1. Settings

`wal_level` \(`enum`\)

`wal_level` determines how much information is written to the WAL. The default value is `replica`, which writes enough data to support WAL archiving and replication, including running read-only queries on a standby server. `minimal` removes all logging except the information required to recover from a crash or immediate shutdown. Finally, `logical`adds information necessary to support logical decoding. Each level includes the information logged at all lower levels. This parameter can only be set at server start.

In `minimal` level, WAL-logging of some bulk operations can be safely skipped, which can make those operations much faster \(see [Section 14.4.7](https://www.postgresql.org/docs/10/static/populate.html#POPULATE-PITR)\). Operations in which this optimization can be applied include:

| `CREATE TABLE AS` |
| --- | --- | --- | --- |
| `CREATE INDEX` |
| `CLUSTER` |
| `COPY` into tables that were created or truncated in the same transaction |

But minimal WAL does not contain enough information to reconstruct the data from a base backup and the WAL logs, so `replica` or higher must be used to enable WAL archiving \([archive\_mode](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-ARCHIVE-MODE)\) and streaming replication.

In `logical` level, the same information is logged as with `replica`, plus information needed to allow extracting logical change sets from the WAL. Using a level of `logical` will increase the WAL volume, particularly if many tables are configured for `REPLICA IDENTITY FULL` and many `UPDATE` and `DELETE` statements are executed.

In releases prior to 9.6, this parameter also allowed the values `archive` and `hot_standby`. These are still accepted but mapped to `replica`.

`fsync` \(`boolean`\)

If this parameter is on, the PostgreSQL server will try to make sure that updates are physically written to disk, by issuing `fsync()` system calls or various equivalent methods \(see [wal\_sync\_method](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-WAL-SYNC-METHOD)\). This ensures that the database cluster can recover to a consistent state after an operating system or hardware crash.

While turning off `fsync` is often a performance benefit, this can result in unrecoverable data corruption in the event of a power failure or system crash. Thus it is only advisable to turn off `fsync` if you can easily recreate your entire database from external data.

Examples of safe circumstances for turning off `fsync` include the initial loading of a new database cluster from a backup file, using a database cluster for processing a batch of data after which the database will be thrown away and recreated, or for a read-only database clone which gets recreated frequently and is not used for failover. High quality hardware alone is not a sufficient justification for turning off `fsync`.

For reliable recovery when changing `fsync` off to on, it is necessary to force all modified buffers in the kernel to durable storage. This can be done while the cluster is shutdown or while `fsync` is on by running `initdb --sync-only`, running `sync`, unmounting the file system, or rebooting the server.

In many situations, turning off [synchronous\_commit](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT) for noncritical transactions can provide much of the potential performance benefit of turning off `fsync`, without the attendant risks of data corruption.

`fsync` can only be set in the `postgresql.conf` file or on the server command line. If you turn this parameter off, also consider turning off [full\_page\_writes](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-FULL-PAGE-WRITES).

`synchronous_commit` \(`enum`\)

Specifies whether transaction commit will wait for WAL records to be written to disk before the command returns a “success” indication to the client. Valid values are `on`,`remote_apply`, `remote_write`, `local`, and `off`. The default, and safe, setting is `on`. When `off`, there can be a delay between when success is reported to the client and when the transaction is really guaranteed to be safe against a server crash. \(The maximum delay is three times [wal\_writer\_delay](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-WAL-WRITER-DELAY).\) Unlike [fsync](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-FSYNC), setting this parameter to `off` does not create any risk of database inconsistency: an operating system or database crash might result in some recent allegedly-committed transactions being lost, but the database state will be just the same as if those transactions had been aborted cleanly. So, turning `synchronous_commit` off can be a useful alternative when performance is more important than exact certainty about the durability of a transaction. For more discussion see [Section 30.3](https://www.postgresql.org/docs/10/static/wal-async-commit.html).

If [synchronous\_standby\_names](https://www.postgresql.org/docs/10/static/runtime-config-replication.html#GUC-SYNCHRONOUS-STANDBY-NAMES) is non-empty, this parameter also controls whether or not transaction commits will wait for their WAL records to be replicated to the standby server\(s\). When set to `on`, commits will wait until replies from the current synchronous standby\(s\) indicate they have received the commit record of the transaction and flushed it to disk. This ensures the transaction will not be lost unless both the primary and all synchronous standbys suffer corruption of their database storage. When set to `remote_apply`, commits will wait until replies from the current synchronous standby\(s\) indicate they have received the commit record of the transaction and applied it, so that it has become visible to queries on the standby\(s\). When set to `remote_write`, commits will wait until replies from the current synchronous standby\(s\) indicate they have received the commit record of the transaction and written it out to their operating system. This setting is sufficient to ensure data preservation even if a standby instance of PostgreSQL were to crash, but not if the standby suffers an operating-system-level crash, since the data has not necessarily reached stable storage on the standby. Finally, the setting `local` causes commits to wait for local flush to disk, but not for replication. This is not usually desirable when synchronous replication is in use, but is provided for completeness.

If `synchronous_standby_names` is empty, the settings `on`, `remote_apply`, `remote_write` and `local` all provide the same synchronization level: transaction commits only wait for local flush to disk.

This parameter can be changed at any time; the behavior for any one transaction is determined by the setting in effect when it commits. It is therefore possible, and useful, to have some transactions commit synchronously and others asynchronously. For example, to make a single multistatement transaction commit asynchronously when the default is the opposite, issue `SET LOCAL synchronous_commit TO OFF` within the transaction.

`wal_sync_method` \(`enum`\)

Method used for forcing WAL updates out to disk. If `fsync` is off then this setting is irrelevant, since WAL file updates will not be forced out at all. Possible values are:

* `open_datasync` \(write WAL files with `open()` option `O_DSYNC`\)
* `fdatasync` \(call `fdatasync()` at each commit\)
* `fsync` \(call `fsync()` at each commit\)
* `fsync_writethrough` \(call `fsync()` at each commit, forcing write-through of any disk write cache\)
* `open_sync` \(write WAL files with `open()` option `O_SYNC`\)

The `open_`\* options also use `O_DIRECT` if available. Not all of these choices are available on all platforms. The default is the first method in the above list that is supported by the platform, except that `fdatasync` is the default on Linux. The default is not necessarily ideal; it might be necessary to change this setting or other aspects of your system configuration in order to create a crash-safe configuration or achieve optimal performance. These aspects are discussed in [Section 30.1](https://www.postgresql.org/docs/10/static/wal-reliability.html). This parameter can only be set in the `postgresql.conf` file or on the server command line.

`full_page_writes` \(`boolean`\)

When this parameter is on, the PostgreSQL server writes the entire content of each disk page to WAL during the first modification of that page after a checkpoint. This is needed because a page write that is in process during an operating system crash might be only partially completed, leading to an on-disk page that contains a mix of old and new data. The row-level change data normally stored in WAL will not be enough to completely restore such a page during post-crash recovery. Storing the full page image guarantees that the page can be correctly restored, but at the price of increasing the amount of data that must be written to WAL. \(Because WAL replay always starts from a checkpoint, it is sufficient to do this during the first change of each page after a checkpoint. Therefore, one way to reduce the cost of full-page writes is to increase the checkpoint interval parameters.\)

Turning this parameter off speeds normal operation, but might lead to either unrecoverable data corruption, or silent data corruption, after a system failure. The risks are similar to turning off `fsync`, though smaller, and it should be turned off only based on the same circumstances recommended for that parameter.

Turning off this parameter does not affect use of WAL archiving for point-in-time recovery \(PITR\) \(see [Section 25.3](https://www.postgresql.org/docs/10/static/continuous-archiving.html)\).

This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `on`.

`wal_log_hints` \(`boolean`\)

When this parameter is `on`, the PostgreSQL server writes the entire content of each disk page to WAL during the first modification of that page after a checkpoint, even for non-critical modifications of so-called hint bits.

If data checksums are enabled, hint bit updates are always WAL-logged and this setting is ignored. You can use this setting to test how much extra WAL-logging would occur if your database had data checksums enabled.

This parameter can only be set at server start. The default value is `off`.

`wal_compression` \(`boolean`\)

When this parameter is `on`, the PostgreSQL server compresses a full page image written to WAL when [full\_page\_writes](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-FULL-PAGE-WRITES) is on or during a base backup. A compressed page image will be decompressed during WAL replay. The default value is `off`. Only superusers can change this setting.

Turning this parameter on can reduce the WAL volume without increasing the risk of unrecoverable data corruption, but at the cost of some extra CPU spent on the compression during WAL logging and on the decompression during WAL replay.

`wal_buffers` \(`integer`\)

The amount of shared memory used for WAL data that has not yet been written to disk. The default setting of -1 selects a size equal to 1/32nd \(about 3%\) of [shared\_buffers](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-SHARED-BUFFERS), but not less than `64kB` nor more than the size of one WAL segment, typically `16MB`. This value can be set manually if the automatic choice is too large or too small, but any positive value less than `32kB` will be treated as `32kB`. This parameter can only be set at server start.

The contents of the WAL buffers are written out to disk at every transaction commit, so extremely large values are unlikely to provide a significant benefit. However, setting this value to at least a few megabytes can improve write performance on a busy server where many clients are committing at once. The auto-tuning selected by the default setting of -1 should give reasonable results in most cases.

`wal_writer_delay` \(`integer`\)

Specifies how often the WAL writer flushes WAL. After flushing WAL it sleeps for `wal_writer_delay` milliseconds, unless woken up by an asynchronously committing transaction. If the last flush happened less than `wal_writer_delay` milliseconds ago and less than `wal_writer_flush_after` bytes of WAL have been produced since, then WAL is only written to the operating system, not flushed to disk. The default value is 200 milliseconds \(`200ms`\). Note that on many systems, the effective resolution of sleep delays is 10 milliseconds; setting `wal_writer_delay` to a value that is not a multiple of 10 might have the same results as setting it to the next higher multiple of 10. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`wal_writer_flush_after` \(`integer`\)

Specifies how often the WAL writer flushes WAL. If the last flush happened less than `wal_writer_delay` milliseconds ago and less than `wal_writer_flush_after` bytes of WAL have been produced since, then WAL is only written to the operating system, not flushed to disk. If `wal_writer_flush_after` is set to `0` then WAL data is flushed immediately. The default is `1MB`. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`commit_delay` \(`integer`\)

`commit_delay` adds a time delay, measured in microseconds, before a WAL flush is initiated. This can improve group commit throughput by allowing a larger number of transactions to commit via a single WAL flush, if system load is high enough that additional transactions become ready to commit within the given interval. However, it also increases latency by up to `commit_delay` microseconds for each WAL flush. Because the delay is just wasted if no other transactions become ready to commit, a delay is only performed if at least `commit_siblings` other transactions are active when a flush is about to be initiated. Also, no delays are performed if `fsync` is disabled. The default `commit_delay` is zero \(no delay\). Only superusers can change this setting.

In PostgreSQL releases prior to 9.3, `commit_delay` behaved differently and was much less effective: it affected only commits, rather than all WAL flushes, and waited for the entire configured delay even if the WAL flush was completed sooner. Beginning in PostgreSQL 9.3, the first process that becomes ready to flush waits for the configured interval, while subsequent processes wait only until the leader completes the flush operation.

`commit_siblings` \(`integer`\)

Minimum number of concurrent open transactions to require before performing the `commit_delay` delay. A larger value makes it more probable that at least one other transaction will become ready to commit during the delay interval. The default is five transactions.

## 19.5.2. Checkpoints

`checkpoint_timeout` \(`integer`\)

Maximum time between automatic WAL checkpoints, in seconds. The valid range is between 30 seconds and one day. The default is five minutes \(`5min`\). Increasing this parameter can increase the amount of time needed for crash recovery. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`checkpoint_completion_target` \(`floating point`\)

Specifies the target of checkpoint completion, as a fraction of total time between checkpoints. The default is 0.5. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`checkpoint_flush_after` \(`integer`\)

Whenever more than `checkpoint_flush_after` bytes have been written while performing a checkpoint, attempt to force the OS to issue these writes to the underlying storage. Doing so will limit the amount of dirty data in the kernel's page cache, reducing the likelihood of stalls when an `fsync` is issued at the end of the checkpoint, or when the OS writes data back in larger batches in the background. Often that will result in greatly reduced transaction latency, but there also are some cases, especially with workloads that are bigger than [shared\_buffers](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-SHARED-BUFFERS), but smaller than the OS's page cache, where performance might degrade. This setting may have no effect on some platforms. The valid range is between `0`, which disables forced writeback, and `2MB`. The default is `256kB` on Linux, `0` elsewhere. \(If `BLCKSZ` is not 8kB, the default and maximum values scale proportionally to it.\) This parameter can only be set in the `postgresql.conf` file or on the server command line.

`checkpoint_warning` \(`integer`\)

Write a message to the server log if checkpoints caused by the filling of checkpoint segment files happen closer together than this many seconds \(which suggests that `max_wal_size` ought to be raised\). The default is 30 seconds \(`30s`\). Zero disables the warning. No warnings will be generated if `checkpoint_timeout` is less than `checkpoint_warning`. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`max_wal_size` \(`integer`\)

Maximum size to let the WAL grow to between automatic WAL checkpoints. This is a soft limit; WAL size can exceed `max_wal_size` under special circumstances, like under heavy load, a failing `archive_command`, or a high `wal_keep_segments` setting. The default is 1 GB. Increasing this parameter can increase the amount of time needed for crash recovery. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`min_wal_size` \(`integer`\)

As long as WAL disk usage stays below this setting, old WAL files are always recycled for future use at a checkpoint, rather than removed. This can be used to ensure that enough WAL space is reserved to handle spikes in WAL usage, for example when running large batch jobs. The default is 80 MB. This parameter can only be set in the `postgresql.conf` file or on the server command line.

## 19.5.3. Archiving

`archive_mode` \(`enum`\)

When `archive_mode` is enabled, completed WAL segments are sent to archive storage by setting [archive\_command](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-ARCHIVE-COMMAND). In addition to `off`, to disable, there are two modes: `on`, and `always`. During normal operation, there is no difference between the two modes, but when set to `always` the WAL archiver is enabled also during archive recovery or standby mode. In `always` mode, all files restored from the archive or streamed with streaming replication will be archived \(again\). See [Section 26.2.9](https://www.postgresql.org/docs/10/static/warm-standby.html#CONTINUOUS-ARCHIVING-IN-STANDBY) for details.

`archive_mode` and `archive_command` are separate variables so that `archive_command` can be changed without leaving archiving mode. This parameter can only be set at server start. `archive_mode` cannot be enabled when `wal_level` is set to `minimal`.

`archive_command` \(`string`\)

The local shell command to execute to archive a completed WAL file segment. Any `%p` in the string is replaced by the path name of the file to archive, and any `%f` is replaced by only the file name. \(The path name is relative to the working directory of the server, i.e., the cluster's data directory.\) Use `%%` to embed an actual `%` character in the command. It is important for the command to return a zero exit status only if it succeeds. For more information see [Section 25.3.1](https://www.postgresql.org/docs/10/static/continuous-archiving.html#BACKUP-ARCHIVING-WAL).

This parameter can only be set in the `postgresql.conf` file or on the server command line. It is ignored unless `archive_mode` was enabled at server start. If `archive_command` is an empty string \(the default\) while `archive_mode` is enabled, WAL archiving is temporarily disabled, but the server continues to accumulate WAL segment files in the expectation that a command will soon be provided. Setting `archive_command` to a command that does nothing but return true, e.g. `/bin/true` \(`REM` on Windows\), effectively disables archiving, but also breaks the chain of WAL files needed for archive recovery, so it should only be used in unusual circumstances.

`archive_timeout` \(`integer`\)

The [archive\_command](https://www.postgresql.org/docs/10/static/runtime-config-wal.html#GUC-ARCHIVE-COMMAND) is only invoked for completed WAL segments. Hence, if your server generates little WAL traffic \(or has slack periods where it does so\), there could be a long delay between the completion of a transaction and its safe recording in archive storage. To limit how old unarchived data can be, you can set `archive_timeout` to force the server to switch to a new WAL segment file periodically. When this parameter is greater than zero, the server will switch to a new segment file whenever this many seconds have elapsed since the last segment file switch, and there has been any database activity, including a single checkpoint \(checkpoints are skipped if there is no database activity\). Note that archived files that are closed early due to a forced switch are still the same length as completely full files. Therefore, it is unwise to use a very short `archive_timeout` — it will bloat your archive storage. `archive_timeout` settings of a minute or so are usually reasonable. You should consider using streaming replication, instead of archiving, if you want data to be copied off the master server more quickly than that. This parameter can only be set in the `postgresql.conf` file or on the server command line.

