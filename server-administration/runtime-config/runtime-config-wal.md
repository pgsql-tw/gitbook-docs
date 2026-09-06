## 19.5. Write Ahead Log [#](#RUNTIME-CONFIG-WAL)

[19.5.1. Settings](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SETTINGS)

[19.5.2. Checkpoints](runtime-config-wal.md#RUNTIME-CONFIG-WAL-CHECKPOINTS)

[19.5.3. Archiving](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVING)

[19.5.4. Recovery](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY)

[19.5.5. Archive Recovery](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY)

[19.5.6. Recovery Target](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)

[19.5.7. WAL Summarization](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION)

For additional information on tuning these settings,
see [Section 28.5](../wal/wal-configuration.md).

<a id="RUNTIME-CONFIG-WAL-SETTINGS"></a>

### 19.5.1. Settings [#](#RUNTIME-CONFIG-WAL-SETTINGS)

<a id="GUC-WAL-LEVEL"></a>

`wal_level` (`enum`) <a id="id-1.6.6.8.3.2.1.1.3"></a> [#](#GUC-WAL-LEVEL)
:   `wal_level` determines how much information is written to
    the WAL. The default value is `replica`, which writes enough
    data to support WAL archiving and replication, including running
    read-only queries on a standby server. `minimal` removes all
    logging except the information required to recover from a crash or
    immediate shutdown. Finally,
    `logical` adds information necessary to support logical
    decoding. Each level includes the information logged at all lower
    levels. This parameter can only be set at server start.

    The `minimal` level generates the least WAL
    volume. It logs no row information for permanent relations
    in transactions that create or
    rewrite them. This can make operations much faster (see
    [Section 14.4.7](../../the-sql-language/performance-tips/populate.md#POPULATE-PITR)). Operations that initiate this
    optimization include:

    <table border="0" class="simplelist" summary="Simple list"><tr><td><code class="command">ALTER ... SET TABLESPACE</code></td></tr><tr><td><code class="command">CLUSTER</code></td></tr><tr><td><code class="command">CREATE TABLE</code></td></tr><tr><td><code class="command">REFRESH MATERIALIZED VIEW</code>
             (without <code class="option">CONCURRENTLY</code>)</td></tr><tr><td><code class="command">REINDEX</code></td></tr><tr><td><code class="command">TRUNCATE</code></td></tr></table>

    However, minimal WAL does not contain sufficient information for
    point-in-time recovery, so `replica` or
    higher must be used to enable continuous archiving
    ([archive_mode](runtime-config-wal.md#GUC-ARCHIVE-MODE)) and streaming binary replication.
    In fact, the server will not even start in this mode if
    `max_wal_senders` is non-zero.
    Note that changing `wal_level` to
    `minimal` makes previous base backups unusable
    for point-in-time recovery and standby servers.

    In `logical` level, the same information is logged as
    with `replica`, plus information needed to
    extract logical change sets from the WAL. Using a level of
    `logical` will increase the WAL volume, particularly if many
    tables are configured for `REPLICA IDENTITY FULL` and
    many `UPDATE` and `DELETE` statements are
    executed.

    In releases prior to 9.6, this parameter also allowed the
    values `archive` and `hot_standby`.
    These are still accepted but mapped to `replica`.
<a id="GUC-FSYNC"></a>

`fsync` (`boolean`) <a id="id-1.6.6.8.3.2.2.1.3"></a> [#](#GUC-FSYNC)
:   If this parameter is on, the PostgreSQL server
    will try to make sure that updates are physically written to
    disk, by issuing `fsync()` system calls or various
    equivalent methods (see [wal_sync_method](runtime-config-wal.md#GUC-WAL-SYNC-METHOD)).
    This ensures that the database cluster can recover to a
    consistent state after an operating system or hardware crash.

    While turning off `fsync` is often a performance
    benefit, this can result in unrecoverable data corruption in
    the event of a power failure or system crash. Thus it
    is only advisable to turn off `fsync` if
    you can easily recreate your entire database from external
    data.

    Examples of safe circumstances for turning off
    `fsync` include the initial loading of a new
    database cluster from a backup file, using a database cluster
    for processing a batch of data after which the database
    will be thrown away and recreated,
    or for a read-only database clone which
    gets recreated frequently and is not used for failover. High
    quality hardware alone is not a sufficient justification for
    turning off `fsync`.

    For reliable recovery when changing `fsync`
    off to on, it is necessary to force all modified buffers in the
    kernel to durable storage. This can be done while the cluster
    is shutdown or while `fsync` is on by running `initdb
    --sync-only`, running `sync`, unmounting the
    file system, or rebooting the server.

    In many situations, turning off [synchronous_commit](runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT)
    for noncritical transactions can provide much of the potential
    performance benefit of turning off `fsync`, without
    the attendant risks of data corruption.

    `fsync` can only be set in the `postgresql.conf`
    file or on the server command line.
    If you turn this parameter off, also consider turning off
    [full_page_writes](runtime-config-wal.md#GUC-FULL-PAGE-WRITES).
<a id="GUC-SYNCHRONOUS-COMMIT"></a>

`synchronous_commit` (`enum`) <a id="id-1.6.6.8.3.2.3.1.3"></a> [#](#GUC-SYNCHRONOUS-COMMIT)
:   Specifies how much WAL processing must complete before
    the database server returns a “success”
    indication to the client. Valid values are
    `remote_apply`, `on`
    (the default), `remote_write`,
    `local`, and `off`.

    If `synchronous_standby_names` is empty,
    the only meaningful settings are `on` and
    `off`; `remote_apply`,
    `remote_write` and `local`
    all provide the same local synchronization level
    as `on`. The local behavior of all
    non-`off` modes is to wait for local flush of WAL
    to disk. In `off` mode, there is no waiting,
    so there can be a delay between when success is reported to the
    client and when the transaction is later guaranteed to be safe
    against a server crash. (The maximum
    delay is three times [wal_writer_delay](runtime-config-wal.md#GUC-WAL-WRITER-DELAY).) Unlike
    [fsync](runtime-config-wal.md#GUC-FSYNC), setting this parameter to `off`
    does not create any risk of database inconsistency: an operating
    system or database crash might
    result in some recent allegedly-committed transactions being lost, but
    the database state will be just the same as if those transactions had
    been aborted cleanly. So, turning `synchronous_commit` off
    can be a useful alternative when performance is more important than
    exact certainty about the durability of a transaction. For more
    discussion see [Section 28.4](../wal/wal-async-commit.md).

    If [synchronous_standby_names](runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES) is non-empty,
    `synchronous_commit` also controls whether
    transaction commits will wait for their WAL records to be
    processed on the standby server(s).

    When set to `remote_apply`, commits will wait
    until replies from the current synchronous standby(s) indicate they
    have received the commit record of the transaction and applied
    it, so that it has become visible to queries on the standby(s),
    and also written to durable storage on the standbys. This will
    cause much larger commit delays than previous settings since
    it waits for WAL replay. When set to `on`,
    commits wait until replies
    from the current synchronous standby(s) indicate they have received
    the commit record of the transaction and flushed it to durable storage. This
    ensures the transaction will not be lost unless both the primary and
    all synchronous standbys suffer corruption of their database storage.
    When set to `remote_write`, commits will wait until replies
    from the current synchronous standby(s) indicate they have
    received the commit record of the transaction and written it to
    their file systems. This setting ensures data preservation if a standby instance of
    PostgreSQL crashes, but not if the standby
    suffers an operating-system-level crash because the data has not
    necessarily reached durable storage on the standby.
    The setting `local` causes commits to wait for
    local flush to disk, but not for replication. This is usually not
    desirable when synchronous replication is in use, but is provided for
    completeness.

    This parameter can be changed at any time; the behavior for any
    one transaction is determined by the setting in effect when it
    commits. It is therefore possible, and useful, to have some
    transactions commit synchronously and others asynchronously.
    For example, to make a single multistatement transaction commit
    asynchronously when the default is the opposite, issue `SET
    LOCAL synchronous_commit TO OFF` within the transaction.

    [Table 19.1](runtime-config-wal.md#SYNCHRONOUS-COMMIT-MATRIX) summarizes the
    capabilities of the `synchronous_commit` settings.

    <a id="SYNCHRONOUS-COMMIT-MATRIX"></a>

    **Table 19.1. synchronous_commit Modes**

    <table border="1" class="table" summary="synchronous_commit Modes"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/></colgroup><thead><tr><th>synchronous_commit setting</th><th>local durable commit</th><th>standby durable commit after PG crash</th><th>standby durable commit after OS crash</th><th>standby query consistency</th></tr></thead><tbody><tr><td>remote_apply</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center">•</td></tr><tr><td>on</td><td align="center">•</td><td align="center">•</td><td align="center">•</td><td align="center"> </td></tr><tr><td>remote_write</td><td align="center">•</td><td align="center">•</td><td align="center"> </td><td align="center"> </td></tr><tr><td>local</td><td align="center">•</td><td align="center"> </td><td align="center"> </td><td align="center"> </td></tr><tr><td>off</td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td></tr></tbody></table>

    <br>
<a id="GUC-WAL-SYNC-METHOD"></a>

`wal_sync_method` (`enum`) <a id="id-1.6.6.8.3.2.4.1.3"></a> [#](#GUC-WAL-SYNC-METHOD)
:   Method used for forcing WAL updates out to disk.
    If `fsync` is off then this setting is irrelevant,
    since WAL file updates will not be forced out at all.
    Possible values are:

    * `open_datasync` (write WAL files with `open()` option `O_DSYNC`)
    * `fdatasync` (call `fdatasync()` at each commit)
    * `fsync` (call `fsync()` at each commit)
    * `fsync_writethrough` (call `fsync()` at each commit, forcing write-through of any disk write cache)
    * `open_sync` (write WAL files with `open()` option `O_SYNC`)

    Not all of these choices are available on all platforms.
    The default is the first method in the above list that is supported
    by the platform, except that `fdatasync` is the default on
    Linux and FreeBSD. The default is not necessarily ideal; it might be
    necessary to change this setting or other aspects of your system
    configuration in order to create a crash-safe configuration or
    achieve optimal performance.
    These aspects are discussed in [Section 28.1](../wal/wal-reliability.md).
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-FULL-PAGE-WRITES"></a>

`full_page_writes` (`boolean`) <a id="id-1.6.6.8.3.2.5.1.3"></a> [#](#GUC-FULL-PAGE-WRITES)
:   When this parameter is on, the PostgreSQL server
    writes the entire content of each disk page to WAL during the
    first modification of that page after a checkpoint.
    This is needed because
    a page write that is in process during an operating system crash might
    be only partially completed, leading to an on-disk page
    that contains a mix of old and new data. The row-level change data
    normally stored in WAL will not be enough to completely restore
    such a page during post-crash recovery. Storing the full page image
    guarantees that the page can be correctly restored, but at the price
    of increasing the amount of data that must be written to WAL.
    (Because WAL replay always starts from a checkpoint, it is sufficient
    to do this during the first change of each page after a checkpoint.
    Therefore, one way to reduce the cost of full-page writes is to
    increase the checkpoint interval parameters.)

    Turning this parameter off speeds normal operation, but
    might lead to either unrecoverable data corruption, or silent
    data corruption, after a system failure. The risks are similar to turning off
    `fsync`, though smaller, and it should be turned off
    only based on the same circumstances recommended for that parameter.

    Turning off this parameter does not affect use of
    WAL archiving for point-in-time recovery (PITR)
    (see [Section 25.3](../backup/continuous-archiving.md)).

    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
    The default is `on`.
<a id="GUC-WAL-LOG-HINTS"></a>

`wal_log_hints` (`boolean`) <a id="id-1.6.6.8.3.2.6.1.3"></a> [#](#GUC-WAL-LOG-HINTS)
:   When this parameter is `on`, the PostgreSQL
    server writes the entire content of each disk page to WAL during the
    first modification of that page after a checkpoint, even for
    non-critical modifications of so-called hint bits.

    If data checksums are enabled, hint bit updates are always WAL-logged
    and this setting is ignored. You can use this setting to test how much
    extra WAL-logging would occur if your database had data checksums
    enabled.

    This parameter can only be set at server start. The default value is `off`.
<a id="GUC-WAL-COMPRESSION"></a>

`wal_compression` (`enum`) <a id="id-1.6.6.8.3.2.7.1.3"></a> [#](#GUC-WAL-COMPRESSION)
:   This parameter enables compression of WAL using the specified
    compression method.
    When enabled, the PostgreSQL
    server compresses full page images written to WAL (e.g. when
    [full_page_writes](runtime-config-wal.md#GUC-FULL-PAGE-WRITES) is on, during a base backup,
    etc.).
    A compressed page image will be decompressed during WAL replay.
    The supported methods are `pglz`,
    `lz4` (if PostgreSQL
    was compiled with `--with-lz4`) and
    `zstd` (if PostgreSQL
    was compiled with `--with-zstd`).
    The value `on` is a historical spelling of `pglz`.
    The default value is `off`.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.

    Enabling compression can reduce the WAL volume without
    increasing the risk of unrecoverable data corruption,
    but at the cost of some extra CPU spent on the compression during
    WAL logging and on the decompression during WAL replay.
<a id="GUC-WAL-INIT-ZERO"></a>

`wal_init_zero` (`boolean`) <a id="id-1.6.6.8.3.2.8.1.3"></a> [#](#GUC-WAL-INIT-ZERO)
:   If set to `on` (the default), this option causes new
    WAL files to be filled with zeroes. On some file systems, this ensures
    that space is allocated before we need to write WAL records. However,
    *Copy-On-Write* (COW) file systems may not benefit
    from this technique, so the option is given to skip the unnecessary
    work. If set to `off`, only the final byte is written
    when the file is created so that it has the expected size.
<a id="GUC-WAL-RECYCLE"></a>

`wal_recycle` (`boolean`) <a id="id-1.6.6.8.3.2.9.1.3"></a> [#](#GUC-WAL-RECYCLE)
:   If set to `on` (the default), this option causes WAL
    files to be recycled by renaming them, avoiding the need to create new
    ones. On COW file systems, it may be faster to create new ones, so the
    option is given to disable this behavior.
<a id="GUC-WAL-BUFFERS"></a>

`wal_buffers` (`integer`) <a id="id-1.6.6.8.3.2.10.1.3"></a> [#](#GUC-WAL-BUFFERS)
:   The amount of shared memory used for WAL data that has not yet been
    written to disk. The default setting of -1 selects a size equal to
    1/32nd (about 3%) of [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS), but not less
    than `64kB` nor more than the size of one WAL
    segment, typically `16MB`. This value can be set
    manually if the automatic choice is too large or too small,
    but any positive value less than `32kB` will be
    treated as `32kB`.
    If this value is specified without units, it is taken as WAL blocks,
    that is `XLOG_BLCKSZ` bytes, typically 8kB.
    This parameter can only be set at server start.

    The contents of the WAL buffers are written out to disk at every
    transaction commit, so extremely large values are unlikely to
    provide a significant benefit. However, setting this value to at
    least a few megabytes can improve write performance on a busy
    server where many clients are committing at once. The auto-tuning
    selected by the default setting of -1 should give reasonable
    results in most cases.
<a id="GUC-WAL-WRITER-DELAY"></a>

`wal_writer_delay` (`integer`) <a id="id-1.6.6.8.3.2.11.1.3"></a> [#](#GUC-WAL-WRITER-DELAY)
:   Specifies how often the WAL writer flushes WAL, in time terms.
    After flushing WAL the writer sleeps for the length of time given
    by `wal_writer_delay`, unless woken up sooner
    by an asynchronously committing transaction. If the last flush
    happened less than `wal_writer_delay` ago and less
    than `wal_writer_flush_after` worth of WAL has been
    produced since, then WAL is only written to the operating system, not
    flushed to disk.
    If this value is specified without units, it is taken as milliseconds.
    The default value is 200 milliseconds (`200ms`). Note that
    on some systems, the effective resolution of sleep delays is 10
    milliseconds; setting `wal_writer_delay` to a value that is
    not a multiple of 10 might have the same results as setting it to the
    next higher multiple of 10. This parameter can only be set in the
    `postgresql.conf` file or on the server command line.
<a id="GUC-WAL-WRITER-FLUSH-AFTER"></a>

`wal_writer_flush_after` (`integer`) <a id="id-1.6.6.8.3.2.12.1.3"></a> [#](#GUC-WAL-WRITER-FLUSH-AFTER)
:   Specifies how often the WAL writer flushes WAL, in volume terms.
    If the last flush happened less
    than `wal_writer_delay` ago and less
    than `wal_writer_flush_after` worth of WAL has been
    produced since, then WAL is only written to the operating system, not
    flushed to disk. If `wal_writer_flush_after` is set
    to `0` then WAL data is always flushed immediately.
    If this value is specified without units, it is taken as WAL blocks,
    that is `XLOG_BLCKSZ` bytes, typically 8kB.
    The default is `1MB`.
    This parameter can only be set in the
    `postgresql.conf` file or on the server command line.
<a id="GUC-WAL-SKIP-THRESHOLD"></a>

`wal_skip_threshold` (`integer`) <a id="id-1.6.6.8.3.2.13.1.3"></a> [#](#GUC-WAL-SKIP-THRESHOLD)
:   When `wal_level` is `minimal` and a
    transaction commits after creating or rewriting a permanent relation,
    this setting determines how to persist the new data. If the data is
    smaller than this setting, write it to the WAL log; otherwise, use an
    fsync of affected files. Depending on the properties of your storage,
    raising or lowering this value might help if such commits are slowing
    concurrent transactions. If this value is specified without units, it
    is taken as kilobytes. The default is two megabytes
    (`2MB`).
<a id="GUC-COMMIT-DELAY"></a>

`commit_delay` (`integer`) <a id="id-1.6.6.8.3.2.14.1.3"></a> [#](#GUC-COMMIT-DELAY)
:   Setting `commit_delay` adds a time delay
    before a WAL flush is initiated. This can improve
    group commit throughput by allowing a larger number of transactions
    to commit via a single WAL flush, if system load is high enough
    that additional transactions become ready to commit within the
    given interval. However, it also increases latency by up to the
    `commit_delay` for each WAL
    flush. Because the delay is just wasted if no other transactions
    become ready to commit, a delay is only performed if at least
    `commit_siblings` other transactions are active
    when a flush is about to be initiated. Also, no delays are
    performed if `fsync` is disabled.
    If this value is specified without units, it is taken as microseconds.
    The default `commit_delay` is zero (no delay).
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.

    In PostgreSQL releases prior to 9.3,
    `commit_delay` behaved differently and was much
    less effective: it affected only commits, rather than all WAL flushes,
    and waited for the entire configured delay even if the WAL flush
    was completed sooner. Beginning in PostgreSQL 9.3,
    the first process that becomes ready to flush waits for the configured
    interval, while subsequent processes wait only until the leader
    completes the flush operation.
<a id="GUC-COMMIT-SIBLINGS"></a>

`commit_siblings` (`integer`) <a id="id-1.6.6.8.3.2.15.1.3"></a> [#](#GUC-COMMIT-SIBLINGS)
:   Minimum number of concurrent open transactions to require
    before performing the `commit_delay` delay. A larger
    value makes it more probable that at least one other
    transaction will become ready to commit during the delay
    interval. The default is five transactions.

<a id="RUNTIME-CONFIG-WAL-CHECKPOINTS"></a>

### 19.5.2. Checkpoints [#](#RUNTIME-CONFIG-WAL-CHECKPOINTS)

<a id="GUC-CHECKPOINT-TIMEOUT"></a>

`checkpoint_timeout` (`integer`) <a id="id-1.6.6.8.4.2.1.1.3"></a> [#](#GUC-CHECKPOINT-TIMEOUT)
:   Maximum time between automatic WAL checkpoints.
    If this value is specified without units, it is taken as seconds.
    The valid range is between 30 seconds and one day.
    The default is five minutes (`5min`).
    Increasing this parameter can increase the amount of time needed
    for crash recovery.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-CHECKPOINT-COMPLETION-TARGET"></a>

`checkpoint_completion_target` (`floating point`) <a id="id-1.6.6.8.4.2.2.1.3"></a> [#](#GUC-CHECKPOINT-COMPLETION-TARGET)
:   Specifies the target of checkpoint completion, as a fraction of
    total time between checkpoints. The default is 0.9, which spreads the
    checkpoint across almost all of the available interval, providing fairly
    consistent I/O load while also leaving some time for checkpoint
    completion overhead. Reducing this parameter is not recommended because
    it causes the checkpoint to complete faster. This results in a higher
    rate of I/O during the checkpoint followed by a period of less I/O between
    the checkpoint completion and the next scheduled checkpoint. This
    parameter can only be set in the `postgresql.conf` file
    or on the server command line.
<a id="GUC-CHECKPOINT-FLUSH-AFTER"></a>

`checkpoint_flush_after` (`integer`) <a id="id-1.6.6.8.4.2.3.1.3"></a> [#](#GUC-CHECKPOINT-FLUSH-AFTER)
:   Whenever more than this amount of data has been
    written while performing a checkpoint, attempt to force the
    OS to issue these writes to the underlying storage. Doing so will
    limit the amount of dirty data in the kernel's page cache, reducing
    the likelihood of stalls when an `fsync` is issued at the end of the
    checkpoint, or when the OS writes data back in larger batches in the
    background. Often that will result in greatly reduced transaction
    latency, but there also are some cases, especially with workloads
    that are bigger than [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS), but smaller
    than the OS's page cache, where performance might degrade. This
    setting may have no effect on some platforms.
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The valid range is
    between `0`, which disables forced writeback,
    and `2MB`. The default is `256kB` on
    Linux, `0` elsewhere. (If `BLCKSZ` is not
    8kB, the default and maximum values scale proportionally to it.)
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-CHECKPOINT-WARNING"></a>

`checkpoint_warning` (`integer`) <a id="id-1.6.6.8.4.2.4.1.3"></a> [#](#GUC-CHECKPOINT-WARNING)
:   Write a message to the server log if checkpoints caused by
    the filling of WAL segment files happen closer together
    than this amount of time (which suggests that
    `max_wal_size` ought to be raised).
    If this value is specified without units, it is taken as seconds.
    The default is 30 seconds (`30s`).
    Zero disables the warning.
    No warnings will be generated if `checkpoint_timeout`
    is less than `checkpoint_warning`.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-MAX-WAL-SIZE"></a>

`max_wal_size` (`integer`) <a id="id-1.6.6.8.4.2.5.1.3"></a> [#](#GUC-MAX-WAL-SIZE)
:   Maximum size to let the WAL grow during automatic
    checkpoints. This is a soft limit; WAL size can exceed
    `max_wal_size` under special circumstances, such as
    heavy load, a failing `archive_command` or `archive_library`, or a high
    `wal_keep_size` setting.
    If this value is specified without units, it is taken as megabytes.
    The default is 1 GB.
    Increasing this parameter can increase the amount of time needed for
    crash recovery.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-MIN-WAL-SIZE"></a>

`min_wal_size` (`integer`) <a id="id-1.6.6.8.4.2.6.1.3"></a> [#](#GUC-MIN-WAL-SIZE)
:   As long as WAL disk usage stays below this setting, old WAL files are
    always recycled for future use at a checkpoint, rather than removed.
    This can be used to ensure that enough WAL space is reserved to
    handle spikes in WAL usage, for example when running large batch
    jobs.
    If this value is specified without units, it is taken as megabytes.
    The default is 80 MB.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.

<a id="RUNTIME-CONFIG-WAL-ARCHIVING"></a>

### 19.5.3. Archiving [#](#RUNTIME-CONFIG-WAL-ARCHIVING)

<a id="GUC-ARCHIVE-MODE"></a>

`archive_mode` (`enum`) <a id="id-1.6.6.8.5.2.1.1.3"></a> [#](#GUC-ARCHIVE-MODE)
:   When `archive_mode` is enabled, completed WAL segments
    are sent to archive storage by setting
    [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) or
    [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY). In addition to `off`,
    to disable, there are two modes: `on`, and
    `always`. During normal operation, there is no
    difference between the two modes, but when set to `always`
    the WAL archiver is enabled also during archive recovery or standby
    mode. In `always` mode, all files restored from the archive
    or streamed with streaming replication will be archived (again). See
    [Section 26.2.9](../high-availability/warm-standby.md#CONTINUOUS-ARCHIVING-IN-STANDBY) for details.

    `archive_mode` is a separate setting from
    `archive_command` and
    `archive_library` so that
    `archive_command` and
    `archive_library` can be changed without leaving
    archiving mode.
    This parameter can only be set at server start.
    `archive_mode` cannot be enabled when
    `wal_level` is set to `minimal`.
<a id="GUC-ARCHIVE-COMMAND"></a>

`archive_command` (`string`) <a id="id-1.6.6.8.5.2.2.1.3"></a> [#](#GUC-ARCHIVE-COMMAND)
:   The local shell command to execute to archive a completed WAL file
    segment. Any `%p` in the string is
    replaced by the path name of the file to archive, and any
    `%f` is replaced by only the file name.
    (The path name is relative to the working directory of the server,
    i.e., the cluster's data directory.)
    Use `%%` to embed an actual `%` character in the
    command. It is important for the command to return a zero
    exit status only if it succeeds. For more information see
    [Section 25.3.1](../backup/continuous-archiving.md#BACKUP-ARCHIVING-WAL).

    This parameter can only be set in the `postgresql.conf`
    file or on the server command line. It is only used if
    `archive_mode` was enabled at server start and
    `archive_library` is set to an empty string. If both
    `archive_command` and `archive_library`
    are set, an error will be raised.
    If `archive_command` is an empty string (the default) while
    `archive_mode` is enabled (and `archive_library`
    is set to an empty string), WAL archiving is temporarily
    disabled, but the server continues to accumulate WAL segment files in
    the expectation that a command will soon be provided. Setting
    `archive_command` to a command that does nothing but
    return true, e.g., `/bin/true` (`REM` on
    Windows), effectively disables
    archiving, but also breaks the chain of WAL files needed for
    archive recovery, so it should only be used in unusual circumstances.
<a id="GUC-ARCHIVE-LIBRARY"></a>

`archive_library` (`string`) <a id="id-1.6.6.8.5.2.3.1.3"></a> [#](#GUC-ARCHIVE-LIBRARY)
:   The library to use for archiving completed WAL file segments. If set to
    an empty string (the default), archiving via shell is enabled, and
    [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) is used. If both
    `archive_command` and `archive_library`
    are set, an error will be raised. Otherwise, the specified
    shared library is used for archiving. The WAL archiver process is
    restarted by the postmaster when this parameter changes. For more
    information, see [Section 25.3.1](../backup/continuous-archiving.md#BACKUP-ARCHIVING-WAL) and
    [Chapter 49](../../server-programming/archive-modules/README.md).

    This parameter can only be set in the
    `postgresql.conf` file or on the server command line.
<a id="GUC-ARCHIVE-TIMEOUT"></a>

`archive_timeout` (`integer`) <a id="id-1.6.6.8.5.2.4.1.3"></a> [#](#GUC-ARCHIVE-TIMEOUT)
:   The [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) or [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) is only invoked for
    completed WAL segments. Hence, if your server generates little WAL
    traffic (or has slack periods where it does so), there could be a
    long delay between the completion of a transaction and its safe
    recording in archive storage. To limit how old unarchived
    data can be, you can set `archive_timeout` to force the
    server to switch to a new WAL segment file periodically. When this
    parameter is greater than zero, the server will switch to a new
    segment file whenever this amount of time has elapsed since the last
    segment file switch, and there has been any database activity,
    including a single checkpoint (checkpoints are skipped if there is
    no database activity). Note that archived files that are closed
    early due to a forced switch are still the same length as completely
    full files. Therefore, it is unwise to use a very short
    `archive_timeout` — it will bloat your archive
    storage. `archive_timeout` settings of a minute or so are
    usually reasonable. You should consider using streaming replication,
    instead of archiving, if you want data to be copied off the primary
    server more quickly than that.
    If this value is specified without units, it is taken as seconds.
    This parameter can only be set in the
    `postgresql.conf` file or on the server command line.

<a id="RUNTIME-CONFIG-WAL-RECOVERY"></a>

### 19.5.4. Recovery [#](#RUNTIME-CONFIG-WAL-RECOVERY)

<a id="id-1.6.6.8.6.2"></a>

This section describes the settings that apply to recovery in general,
affecting crash recovery, streaming replication and archive-based
replication.

<a id="GUC-RECOVERY-PREFETCH"></a>

`recovery_prefetch` (`enum`) <a id="id-1.6.6.8.6.4.1.1.3"></a> [#](#GUC-RECOVERY-PREFETCH)
:   Whether to try to prefetch blocks that are referenced in the WAL that
    are not yet in the buffer pool, during recovery. Valid values are
    `off`, `on` and
    `try` (the default). The setting
    `try` enables
    prefetching only if the operating system provides support for issuing
    read-ahead advice.

    Prefetching blocks that will soon be needed can reduce I/O wait times
    during recovery with some workloads.
    See also the [wal_decode_buffer_size](runtime-config-wal.md#GUC-WAL-DECODE-BUFFER-SIZE) and
    [maintenance_io_concurrency](runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY) settings, which limit
    prefetching activity.
<a id="GUC-WAL-DECODE-BUFFER-SIZE"></a>

`wal_decode_buffer_size` (`integer`) <a id="id-1.6.6.8.6.4.2.1.3"></a> [#](#GUC-WAL-DECODE-BUFFER-SIZE)
:   A limit on how far ahead the server can look in the WAL, to find
    blocks to prefetch. If this value is specified without units, it is
    taken as bytes.
    The default is 512kB.
    This parameter can only be set at server start.

<a id="RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY"></a>

### 19.5.5. Archive Recovery [#](#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY)

<a id="id-1.6.6.8.7.2"></a>

This section describes the settings that apply only for the duration of
the recovery. They must be reset for any subsequent recovery you wish to
perform.

“Recovery” covers using the server as a standby or for
executing a targeted recovery. Typically, standby mode would be used to
provide high availability and/or read scalability, whereas a targeted
recovery is used to recover from data loss.

To start the server in standby mode, create a file called
`standby.signal`<a id="id-1.6.6.8.7.5.2"></a>
in the data directory. The server will enter recovery and will not stop
recovery when the end of archived WAL is reached, but will keep trying to
continue recovery by connecting to the sending server as specified by the
`primary_conninfo` setting and/or by fetching new WAL
segments using `restore_command`. For this mode, the
parameters from this section and [Section 19.6.3](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY) are of interest.
Parameters from [Section 19.5.6](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET) will
also be applied but are typically not useful in this mode.

To start the server in targeted recovery mode, create a file called
`recovery.signal`<a id="id-1.6.6.8.7.6.2"></a>
in the data directory. If both `standby.signal` and
`recovery.signal` files are created, standby mode
takes precedence. Targeted recovery mode ends when the archived WAL is
fully replayed, or when `recovery_target` is reached.
In this mode, the parameters from both this section and [Section 19.5.6](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET) will be used.

<a id="GUC-RESTORE-COMMAND"></a>

`restore_command` (`string`) <a id="id-1.6.6.8.7.7.1.1.3"></a> [#](#GUC-RESTORE-COMMAND)
:   The local shell command to execute to retrieve an archived segment of
    the WAL file series. This parameter is required for archive recovery,
    but optional for streaming replication.
    Any `%f` in the string is
    replaced by the name of the file to retrieve from the archive,
    and any `%p` is replaced by the copy destination path name
    on the server.
    (The path name is relative to the current working directory,
    i.e., the cluster's data directory.)
    Any `%r` is replaced by the name of the file containing the
    last valid restart point. That is the earliest file that must be kept
    to allow a restore to be restartable, so this information can be used
    to truncate the archive to just the minimum required to support
    restarting from the current restore. `%r` is typically only
    used by warm-standby configurations
    (see [Section 26.2](../high-availability/warm-standby.md)).
    Write `%%` to embed an actual `%` character.

    It is important for the command to return a zero exit status
    only if it succeeds. The command *will* be asked for file
    names that are not present in the archive; it must return nonzero
    when so asked. Examples:

    ```

    restore_command = 'cp /mnt/server/archivedir/%f "%p"'
    restore_command = 'copy "C:\\server\\archivedir\\%f" "%p"'  # Windows
    ```

    An exception is that if the command was terminated by a signal (other
    than SIGTERM, which is used as part of a
    database server shutdown) or an error by the shell (such as command
    not found), then recovery will abort and the server will not start up.

    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-ARCHIVE-CLEANUP-COMMAND"></a>

`archive_cleanup_command` (`string`) <a id="id-1.6.6.8.7.7.2.1.3"></a> [#](#GUC-ARCHIVE-CLEANUP-COMMAND)
:   This optional parameter specifies a shell command that will be executed
    at every restartpoint. The purpose of
    `archive_cleanup_command` is to provide a mechanism for
    cleaning up old archived WAL files that are no longer needed by the
    standby server.
    Any `%r` is replaced by the name of the file containing the
    last valid restart point.
    That is the earliest file that must be *kept* to allow a
    restore to be restartable, and so all files earlier than `%r`
    may be safely removed.
    This information can be used to truncate the archive to just the
    minimum required to support restart from the current restore.
    The [pg_archivecleanup](../../reference/reference-server/pgarchivecleanup.md) module
    is often used in `archive_cleanup_command` for
    single-standby configurations, for example:

    ```
    archive_cleanup_command = 'pg_archivecleanup /mnt/server/archivedir %r'
    ```

    Note however that if multiple standby servers are restoring from the
    same archive directory, you will need to ensure that you do not delete
    WAL files until they are no longer needed by any of the servers.
    `archive_cleanup_command` would typically be used in a
    warm-standby configuration (see [Section 26.2](../high-availability/warm-standby.md)).
    Write `%%` to embed an actual `%` character in the
    command.

    If the command returns a nonzero exit status then a warning log
    message will be written. An exception is that if the command was
    terminated by a signal or an error by the shell (such as command not
    found), a fatal error will be raised.

    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-RECOVERY-END-COMMAND"></a>

`recovery_end_command` (`string`) <a id="id-1.6.6.8.7.7.3.1.3"></a> [#](#GUC-RECOVERY-END-COMMAND)
:   This parameter specifies a shell command that will be executed once only
    at the end of recovery. This parameter is optional. The purpose of the
    `recovery_end_command` is to provide a mechanism for cleanup
    following replication or recovery.
    Any `%r` is replaced by the name of the file containing the
    last valid restart point, like in [archive_cleanup_command](runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND).

    If the command returns a nonzero exit status then a warning log
    message will be written and the database will proceed to start up
    anyway. An exception is that if the command was terminated by a
    signal or an error by the shell (such as command not found), the
    database will not proceed with startup.

    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.

<a id="RUNTIME-CONFIG-WAL-RECOVERY-TARGET"></a>

### 19.5.6. Recovery Target [#](#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)

By default, recovery will recover to the end of the WAL log. The
following parameters can be used to specify an earlier stopping point.
At most one of `recovery_target`,
`recovery_target_lsn`, `recovery_target_name`,
`recovery_target_time`, or `recovery_target_xid`
can be used; if more than one of these is specified in the configuration
file, an error will be raised.
These parameters can only be set at server start.

<a id="GUC-RECOVERY-TARGET"></a>

`recovery_target` `= 'immediate'` <a id="id-1.6.6.8.8.3.1.1.3"></a> [#](#GUC-RECOVERY-TARGET)
:   This parameter specifies that recovery should end as soon as a
    consistent state is reached, i.e., as early as possible. When restoring
    from an online backup, this means the point where taking the backup
    ended.

    Technically, this is a string parameter, but `'immediate'`
    is currently the only allowed value.
<a id="GUC-RECOVERY-TARGET-NAME"></a>

`recovery_target_name` (`string`) <a id="id-1.6.6.8.8.3.2.1.3"></a> [#](#GUC-RECOVERY-TARGET-NAME)
:   This parameter specifies the named restore point (created with
    `pg_create_restore_point()`) to which recovery will proceed.
<a id="GUC-RECOVERY-TARGET-TIME"></a>

`recovery_target_time` (`timestamp`) <a id="id-1.6.6.8.8.3.3.1.3"></a> [#](#GUC-RECOVERY-TARGET-TIME)
:   This parameter specifies the time stamp up to which recovery
    will proceed.
    The precise stopping point is also influenced by
    [recovery_target_inclusive](runtime-config-wal.md#GUC-RECOVERY-TARGET-INCLUSIVE).

    The value of this parameter is a time stamp in the same format
    accepted by the `timestamp with time zone` data type,
    except that you cannot use a time zone abbreviation (unless the
    [timezone_abbreviations](runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) variable has been set
    earlier in the configuration file). Preferred style is to use a
    numeric offset from UTC, or you can write a full time zone name,
    e.g., `Europe/Helsinki` not `EEST`.
<a id="GUC-RECOVERY-TARGET-XID"></a>

`recovery_target_xid` (`string`) <a id="id-1.6.6.8.8.3.4.1.3"></a> [#](#GUC-RECOVERY-TARGET-XID)
:   This parameter specifies the transaction ID up to which recovery
    will proceed. Keep in mind
    that while transaction IDs are assigned sequentially at transaction
    start, transactions can complete in a different numeric order.
    The transactions that will be recovered are those that committed
    before (and optionally including) the specified one.
    The precise stopping point is also influenced by
    [recovery_target_inclusive](runtime-config-wal.md#GUC-RECOVERY-TARGET-INCLUSIVE).
<a id="GUC-RECOVERY-TARGET-LSN"></a>

`recovery_target_lsn` (`pg_lsn`) <a id="id-1.6.6.8.8.3.5.1.3"></a> [#](#GUC-RECOVERY-TARGET-LSN)
:   This parameter specifies the LSN of the write-ahead log location up
    to which recovery will proceed. The precise stopping point is also
    influenced by [recovery_target_inclusive](runtime-config-wal.md#GUC-RECOVERY-TARGET-INCLUSIVE). This
    parameter is parsed using the system data type
    [`pg_lsn`](../../the-sql-language/datatype/datatype-pg-lsn.md).

The following options further specify the recovery target, and affect
what happens when the target is reached:

<a id="GUC-RECOVERY-TARGET-INCLUSIVE"></a>

`recovery_target_inclusive` (`boolean`) <a id="id-1.6.6.8.8.5.1.1.3"></a> [#](#GUC-RECOVERY-TARGET-INCLUSIVE)
:   Specifies whether to stop just after the specified recovery target
    (`on`), or just before the recovery target
    (`off`).
    Applies when [recovery_target_lsn](runtime-config-wal.md#GUC-RECOVERY-TARGET-LSN),
    [recovery_target_time](runtime-config-wal.md#GUC-RECOVERY-TARGET-TIME), or
    [recovery_target_xid](runtime-config-wal.md#GUC-RECOVERY-TARGET-XID) is specified.
    This setting controls whether transactions
    having exactly the target WAL location (LSN), commit time, or transaction ID, respectively, will
    be included in the recovery. Default is `on`.
<a id="GUC-RECOVERY-TARGET-TIMELINE"></a>

`recovery_target_timeline` (`string`) <a id="id-1.6.6.8.8.5.2.1.3"></a> [#](#GUC-RECOVERY-TARGET-TIMELINE)
:   Specifies recovering into a particular timeline. The value can be a
    numeric timeline ID or a special value. The value
    `current` recovers along the same timeline that was
    current when the base backup was taken. The
    value `latest` recovers
    to the latest timeline found in the archive, which is useful in
    a standby server. `latest` is the default.

    To specify a timeline ID in hexadecimal (for example, if extracted
    from a WAL file name or history file), prefix it with a
    `0x`. For instance, if the WAL file name is
    `00000011000000A10000004F`, then the timeline ID is
    `0x11` (or 17 decimal).

    You usually only need to set this parameter
    in complex re-recovery situations, where you need to return to
    a state that itself was reached after a point-in-time recovery.
    See [Section 25.3.6](../backup/continuous-archiving.md#BACKUP-TIMELINES) for discussion.
<a id="GUC-RECOVERY-TARGET-ACTION"></a>

`recovery_target_action` (`enum`) <a id="id-1.6.6.8.8.5.3.1.3"></a> [#](#GUC-RECOVERY-TARGET-ACTION)
:   Specifies what action the server should take once the recovery target is
    reached. The default is `pause`, which means recovery will
    be paused. `promote` means the recovery process will finish
    and the server will start to accept connections.
    Finally `shutdown` will stop the server after reaching the
    recovery target.

    The intended use of the `pause` setting is to allow queries
    to be executed against the database to check if this recovery target
    is the most desirable point for recovery.
    The paused state can be resumed by
    using `pg_wal_replay_resume()` (see
    [Table 9.99](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-RECOVERY-CONTROL-TABLE)), which then
    causes recovery to end. If this recovery target is not the
    desired stopping point, then shut down the server, change the
    recovery target settings to a later target and restart to
    continue recovery.

    The `shutdown` setting is useful to have the instance ready
    at the exact replay point desired. The instance will still be able to
    replay more WAL records (and in fact will have to replay WAL records
    since the last checkpoint next time it is started).

    Note that because `recovery.signal` will not be
    removed when `recovery_target_action` is set to `shutdown`,
    any subsequent start will end with immediate shutdown unless the
    configuration is changed or the `recovery.signal`
    file is removed manually.

    This setting has no effect if no recovery target is set.
    If [hot_standby](runtime-config-replication.md#GUC-HOT-STANDBY) is not enabled, a setting of
    `pause` will act the same as `shutdown`.
    If the recovery target is reached while a promotion is ongoing,
    a setting of `pause` will act the same as
    `promote`.

    In any case, if a recovery target is configured but the archive
    recovery ends before the target is reached, the server will shut down
    with a fatal error.

<a id="RUNTIME-CONFIG-WAL-SUMMARIZATION"></a>

### 19.5.7. WAL Summarization [#](#RUNTIME-CONFIG-WAL-SUMMARIZATION)

These settings control WAL summarization, a feature which must be
enabled in order to perform an
[incremental backup](../backup/continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP).

<a id="GUC-SUMMARIZE-WAL"></a>

`summarize_wal` (`boolean`) <a id="id-1.6.6.8.9.3.1.1.3"></a> [#](#GUC-SUMMARIZE-WAL)
:   Enables the WAL summarizer process. Note that WAL summarization can
    be enabled either on a primary or on a standby. This parameter can only
    be set in the `postgresql.conf` file or on the server
    command line. The default is `off`.

    The server cannot be started with `summarize_wal=on`
    if `wal_level` is set to `minimal`. If
    `summarize_wal=on` is configured after server startup
    while `wal_level=minimal`, the summarizer will run
    but refuse to generate summary files for any WAL generated with
    `wal_level=minimal`.
<a id="GUC-WAL-SUMMARY-KEEP-TIME"></a>

`wal_summary_keep_time` (`integer`) <a id="id-1.6.6.8.9.3.2.1.3"></a> [#](#GUC-WAL-SUMMARY-KEEP-TIME)
:   Configures the amount of time after which the WAL summarizer
    automatically removes old WAL summaries. The file timestamp is used to
    determine which files are old enough to remove. Typically, you should set
    this comfortably higher than the time that could pass between a backup
    and a later incremental backup that depends on it. WAL summaries must
    be available for the entire range of WAL records between the preceding
    backup and the new one being taken; if not, the incremental backup will
    fail. If this parameter is set to zero, WAL summaries will not be
    automatically deleted, but it is safe to manually remove files that you
    know will not be required for future incremental backups.
    This parameter can only be set in the
    `postgresql.conf` file or on the server command line.
    If this value is specified without units, it is taken as minutes.
    The default is 10 days. If `summarize_wal = off`,
    existing WAL summaries will not be removed regardless of the value of
    this parameter, because the WAL summarizer will not run.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-wal.html)（英文原文，待翻譯）
