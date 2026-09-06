## 19.4. Resource Consumption [#](#RUNTIME-CONFIG-RESOURCE)

[19.4.1. Memory](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY)

[19.4.2. Disk](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-DISK)

[19.4.3. Kernel Resource Usage](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-KERNEL)

[19.4.4. Background Writer](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER)

[19.4.5. I/O](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-IO)

[19.4.6. Worker Processes](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-WORKER-PROCESSES)

<a id="RUNTIME-CONFIG-RESOURCE-MEMORY"></a>

### 19.4.1. Memory [#](#RUNTIME-CONFIG-RESOURCE-MEMORY)

<a id="GUC-SHARED-BUFFERS"></a>

`shared_buffers` (`integer`) <a id="id-1.6.6.7.2.2.1.1.3"></a> [#](#GUC-SHARED-BUFFERS)
:   Sets the amount of memory the database server uses for shared
    memory buffers. The default is typically 128 megabytes
    (`128MB`), but might be less if your kernel settings will
    not support it (as determined during initdb).
    This setting must be at least 128 kilobytes. However,
    settings significantly higher than the minimum are usually needed
    for good performance.
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    (Non-default values of `BLCKSZ` change the minimum
    value.)
    This parameter can only be set at server start.

    If you have a dedicated database server with 1GB or more of RAM, a
    reasonable starting value for `shared_buffers` is 25%
    of the memory in your system. There are some workloads where even
    larger settings for `shared_buffers` are effective, but
    because PostgreSQL also relies on the
    operating system cache, it is unlikely that an allocation of more than
    40% of RAM to `shared_buffers` will work better than a
    smaller amount. Larger settings for `shared_buffers`
    usually require a corresponding increase in
    `max_wal_size`, in order to spread out the
    process of writing large quantities of new or changed data over a
    longer period of time.

    On systems with less than 1GB of RAM, a smaller percentage of RAM is
    appropriate, so as to leave adequate space for the operating system.
<a id="GUC-HUGE-PAGES"></a>

`huge_pages` (`enum`) <a id="id-1.6.6.7.2.2.2.1.3"></a> [#](#GUC-HUGE-PAGES)
:   Controls whether huge pages are requested for the main shared memory
    area. Valid values are `try` (the default),
    `on`, and `off`.
    This parameter can only be set at server start. With
    `huge_pages` set to `try`, the
    server will try to request huge pages, but fall back to the default if
    that fails. With `on`, failure to request huge pages
    will prevent the server from starting up. With `off`,
    huge pages will not be requested. The actual state of huge pages is
    indicated by the server variable
    [huge_pages_status](runtime-config-preset.md#GUC-HUGE-PAGES-STATUS).

    At present, this setting is supported only on Linux and Windows. The
    setting is ignored on other systems when set to
    `try`. On Linux, it is only supported when
    `shared_memory_type` is set to `mmap`
    (the default).

    The use of huge pages results in smaller page tables and less CPU time
    spent on memory management, increasing performance. For more details about
    using huge pages on Linux, see [Section 18.4.5](../runtime/kernel-resources.md#LINUX-HUGE-PAGES).

    Huge pages are known as large pages on Windows. To use them, you need to
    assign the user right “Lock pages in memory” to the Windows user account
    that runs PostgreSQL.
    You can use Windows Group Policy tool (gpedit.msc) to assign the user right
    “Lock pages in memory”.
    To start the database server on the command prompt as a standalone process,
    not as a Windows service, the command prompt must be run as an administrator or
    User Access Control (UAC) must be disabled. When the UAC is enabled, the normal
    command prompt revokes the user right “Lock pages in memory” when started.

    Note that this setting only affects the main shared memory area.
    Operating systems such as Linux, FreeBSD, and Illumos can also use
    huge pages (also known as “super” pages or
    “large” pages) automatically for normal memory
    allocation, without an explicit request from
    PostgreSQL. On Linux, this is called
    “transparent huge pages”<a id="id-1.6.6.7.2.2.2.2.5.5"></a> (THP). That feature has been known to
    cause performance degradation with
    PostgreSQL for some users on some Linux
    versions, so its use is currently discouraged (unlike explicit use of
    `huge_pages`).
<a id="GUC-HUGE-PAGE-SIZE"></a>

`huge_page_size` (`integer`) <a id="id-1.6.6.7.2.2.3.1.3"></a> [#](#GUC-HUGE-PAGE-SIZE)
:   Controls the size of huge pages, when they are enabled with
    [huge_pages](runtime-config-resource.md#GUC-HUGE-PAGES).
    The default is zero (`0`).
    When set to `0`, the default huge page size on the
    system will be used. This parameter can only be set at server start.

    Some commonly available page sizes on modern 64 bit server architectures include:
    `2MB` and `1GB` (Intel and AMD), `16MB` and
    `16GB` (IBM POWER), and `64kB`, `2MB`,
    `32MB` and `1GB` (ARM). For more information
    about usage and support, see [Section 18.4.5](../runtime/kernel-resources.md#LINUX-HUGE-PAGES).

    Non-default settings are currently supported only on Linux.
<a id="GUC-TEMP-BUFFERS"></a>

`temp_buffers` (`integer`) <a id="id-1.6.6.7.2.2.4.1.3"></a> [#](#GUC-TEMP-BUFFERS)
:   Sets the maximum amount of memory used for temporary buffers within
    each database session. These are session-local buffers used only
    for access to temporary tables.
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The default is eight megabytes (`8MB`).
    (If `BLCKSZ` is not 8kB, the default value scales
    proportionally to it.)
    This setting can be changed within individual
    sessions, but only before the first use of temporary tables
    within the session; subsequent attempts to change the value will
    have no effect on that session.

    A session will allocate temporary buffers as needed up to the limit
    given by `temp_buffers`. The cost of setting a large
    value in sessions that do not actually need many temporary
    buffers is only a buffer descriptor, or about 64 bytes, per
    increment in `temp_buffers`. However if a buffer is
    actually used an additional 8192 bytes will be consumed for it
    (or in general, `BLCKSZ` bytes).
<a id="GUC-MAX-PREPARED-TRANSACTIONS"></a>

`max_prepared_transactions` (`integer`) <a id="id-1.6.6.7.2.2.5.1.3"></a> [#](#GUC-MAX-PREPARED-TRANSACTIONS)
:   Sets the maximum number of transactions that can be in the
    “prepared” state simultaneously (see [PREPARE TRANSACTION](../../reference/sql-commands/sql-prepare-transaction.md)).
    Setting this parameter to zero (which is the default)
    disables the prepared-transaction feature.
    This parameter can only be set at server start.

    If you are not planning to use prepared transactions, this parameter
    should be set to zero to prevent accidental creation of prepared
    transactions. If you are using prepared transactions, you will
    probably want `max_prepared_transactions` to be at
    least as large as [max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS), so that every
    session can have a prepared transaction pending.

    When running a standby server, you must set this parameter to the
    same or higher value than on the primary server. Otherwise, queries
    will not be allowed in the standby server.
<a id="GUC-WORK-MEM"></a>

`work_mem` (`integer`) <a id="id-1.6.6.7.2.2.6.1.3"></a> [#](#GUC-WORK-MEM)
:   Sets the base maximum amount of memory to be used by a query operation
    (such as a sort or hash table) before writing to temporary disk files.
    If this value is specified without units, it is taken as kilobytes.
    The default value is four megabytes (`4MB`).
    Note that a complex query might perform several sort and hash
    operations at the same time, with each operation generally being
    allowed to use as much memory as this value specifies before
    it starts
    to write data into temporary files. Also, several running
    sessions could be doing such operations concurrently.
    Therefore, the total memory used could be many times the value
    of `work_mem`; it is necessary to keep this
    fact in mind when choosing the value. Sort operations are used
    for `ORDER BY`, `DISTINCT`,
    and merge joins.
    Hash tables are used in hash joins, hash-based aggregation, memoize
    nodes and hash-based processing of `IN` subqueries.

    Hash-based operations are generally more sensitive to memory
    availability than equivalent sort-based operations. The
    memory limit for a hash table is computed by multiplying
    `work_mem` by
    `hash_mem_multiplier`. This makes it
    possible for hash-based operations to use an amount of memory
    that exceeds the usual `work_mem` base
    amount.
<a id="GUC-HASH-MEM-MULTIPLIER"></a>

`hash_mem_multiplier` (`floating point`) <a id="id-1.6.6.7.2.2.7.1.3"></a> [#](#GUC-HASH-MEM-MULTIPLIER)
:   Used to compute the maximum amount of memory that hash-based
    operations can use. The final limit is determined by
    multiplying `work_mem` by
    `hash_mem_multiplier`. The default value is
    2.0, which makes hash-based operations use twice the usual
    `work_mem` base amount.

    Consider increasing `hash_mem_multiplier` in
    environments where spilling by query operations is a regular
    occurrence, especially when simply increasing
    `work_mem` results in memory pressure (memory
    pressure typically takes the form of intermittent out of
    memory errors). The default setting of 2.0 is often effective with
    mixed workloads. Higher settings in the range of 2.0 - 8.0 or
    more may be effective in environments where
    `work_mem` has already been increased to 40MB
    or more.
<a id="GUC-MAINTENANCE-WORK-MEM"></a>

`maintenance_work_mem` (`integer`) <a id="id-1.6.6.7.2.2.8.1.3"></a> [#](#GUC-MAINTENANCE-WORK-MEM)
:   Specifies the maximum amount of memory to be used by maintenance
    operations, such as `VACUUM`, `CREATE
    INDEX`, and `ALTER TABLE ADD FOREIGN KEY`.
    If this value is specified without units, it is taken as kilobytes.
    It defaults
    to 64 megabytes (`64MB`). Since only one of these
    operations can be executed at a time by a database session, and
    an installation normally doesn't have many of them running
    concurrently, it's safe to set this value significantly larger
    than `work_mem`. Larger settings might improve
    performance for vacuuming and for restoring database dumps.

    Note that when autovacuum runs, up to
    [autovacuum_max_workers](runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS) times this memory
    may be allocated, so be careful not to set the default value
    too high. It may be useful to control for this by separately
    setting [autovacuum_work_mem](runtime-config-resource.md#GUC-AUTOVACUUM-WORK-MEM).
<a id="GUC-AUTOVACUUM-WORK-MEM"></a>

`autovacuum_work_mem` (`integer`) <a id="id-1.6.6.7.2.2.9.1.3"></a> [#](#GUC-AUTOVACUUM-WORK-MEM)
:   Specifies the maximum amount of memory to be used by each
    autovacuum worker process.
    If this value is specified without units, it is taken as kilobytes.
    It defaults to -1, indicating that
    the value of [maintenance_work_mem](runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM) should
    be used instead. The setting has no effect on the behavior of
    `VACUUM` when run in other contexts.
    This parameter can only be set in the
    `postgresql.conf` file or on the server command
    line.
<a id="GUC-VACUUM-BUFFER-USAGE-LIMIT"></a>

`vacuum_buffer_usage_limit` (`integer`) <a id="id-1.6.6.7.2.2.10.1.3"></a> [#](#GUC-VACUUM-BUFFER-USAGE-LIMIT)
:   Specifies the size of the
    [*[Buffer Access Strategy](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)*](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)
    used by the `VACUUM` and `ANALYZE`
    commands. A setting of `0` will allow the operation
    to use any number of `shared_buffers`. Otherwise
    valid sizes range from `128 kB` to
    `16 GB`. If the specified size would exceed 1/8 the
    size of `shared_buffers`, the size is silently capped
    to that value. The default value is `2MB`. If
    this value is specified without units, it is taken as kilobytes. This
    parameter can be set at any time. It can be overridden for
    [VACUUM](../../reference/sql-commands/sql-vacuum.md) and [ANALYZE](../../reference/sql-commands/sql-analyze.md)
    when passing the `BUFFER_USAGE_LIMIT` option. Higher
    settings can allow `VACUUM` and
    `ANALYZE` to run more quickly, but having too large a
    setting may cause too many other useful pages to be evicted from
    shared buffers.
<a id="GUC-LOGICAL-DECODING-WORK-MEM"></a>

`logical_decoding_work_mem` (`integer`) <a id="id-1.6.6.7.2.2.11.1.3"></a> [#](#GUC-LOGICAL-DECODING-WORK-MEM)
:   Specifies the maximum amount of memory to be used by logical decoding,
    before some of the decoded changes are written to local disk. This
    limits the amount of memory used by logical streaming replication
    connections. It defaults to 64 megabytes (`64MB`).
    Since each replication connection only uses a single buffer of this size,
    and an installation normally doesn't have many such connections
    concurrently (as limited by `max_wal_senders`), it's
    safe to set this value significantly higher than `work_mem`,
    reducing the amount of decoded changes written to disk.
<a id="GUC-COMMIT-TIMESTAMP-BUFFERS"></a>

`commit_timestamp_buffers` (`integer`) <a id="id-1.6.6.7.2.2.12.1.3"></a> [#](#GUC-COMMIT-TIMESTAMP-BUFFERS)
:   Specifies the amount of memory to use to cache the contents of
    `pg_commit_ts` (see
    [Table 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)).
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The default value is `0`, which requests
    `shared_buffers`/512 up to 1024 blocks,
    but not fewer than 16 blocks.
    This parameter can only be set at server start.
<a id="GUC-MULTIXACT-MEMBER-BUFFERS"></a>

`multixact_member_buffers` (`integer`) <a id="id-1.6.6.7.2.2.13.1.3"></a> [#](#GUC-MULTIXACT-MEMBER-BUFFERS)
:   Specifies the amount of shared memory to use to cache the contents
    of `pg_multixact/members` (see
    [Table 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)).
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The default value is `32`.
    This parameter can only be set at server start.
<a id="GUC-MULTIXACT-OFFSET-BUFFERS"></a>

`multixact_offset_buffers` (`integer`) <a id="id-1.6.6.7.2.2.14.1.3"></a> [#](#GUC-MULTIXACT-OFFSET-BUFFERS)
:   Specifies the amount of shared memory to use to cache the contents
    of `pg_multixact/offsets` (see
    [Table 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)).
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The default value is `16`.
    This parameter can only be set at server start.
<a id="GUC-NOTIFY-BUFFERS"></a>

`notify_buffers` (`integer`) <a id="id-1.6.6.7.2.2.15.1.3"></a> [#](#GUC-NOTIFY-BUFFERS)
:   Specifies the amount of shared memory to use to cache the contents
    of `pg_notify` (see
    [Table 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)).
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The default value is `16`.
    This parameter can only be set at server start.
<a id="GUC-SERIALIZABLE-BUFFERS"></a>

`serializable_buffers` (`integer`) <a id="id-1.6.6.7.2.2.16.1.3"></a> [#](#GUC-SERIALIZABLE-BUFFERS)
:   Specifies the amount of shared memory to use to cache the contents
    of `pg_serial` (see
    [Table 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)).
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The default value is `32`.
    This parameter can only be set at server start.
<a id="GUC-SUBTRANSACTION-BUFFERS"></a>

`subtransaction_buffers` (`integer`) <a id="id-1.6.6.7.2.2.17.1.3"></a> [#](#GUC-SUBTRANSACTION-BUFFERS)
:   Specifies the amount of shared memory to use to cache the contents
    of `pg_subtrans` (see
    [Table 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)).
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The default value is `0`, which requests
    `shared_buffers`/512 up to 1024 blocks,
    but not fewer than 16 blocks.
    This parameter can only be set at server start.
<a id="GUC-TRANSACTION-BUFFERS"></a>

`transaction_buffers` (`integer`) <a id="id-1.6.6.7.2.2.18.1.3"></a> [#](#GUC-TRANSACTION-BUFFERS)
:   Specifies the amount of shared memory to use to cache the contents
    of `pg_xact` (see
    [Table 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)).
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The default value is `0`, which requests
    `shared_buffers`/512 up to 1024 blocks,
    but not fewer than 16 blocks.
    This parameter can only be set at server start.
<a id="GUC-MAX-STACK-DEPTH"></a>

`max_stack_depth` (`integer`) <a id="id-1.6.6.7.2.2.19.1.3"></a> [#](#GUC-MAX-STACK-DEPTH)
:   Specifies the maximum safe depth of the server's execution stack.
    The ideal setting for this parameter is the actual stack size limit
    enforced by the kernel (as set by `ulimit -s` or local
    equivalent), less a safety margin of a megabyte or so. The safety
    margin is needed because the stack depth is not checked in every
    routine in the server, but only in key potentially-recursive routines.
    If this value is specified without units, it is taken as kilobytes.
    The default setting is two megabytes (`2MB`), which
    is conservatively small and unlikely to risk crashes. However,
    it might be too small to allow execution of complex functions.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.

    Setting `max_stack_depth` higher than
    the actual kernel limit will mean that a runaway recursive function
    can crash an individual backend process. On platforms where
    PostgreSQL can determine the kernel limit,
    the server will not allow this variable to be set to an unsafe
    value. However, not all platforms provide the information,
    so caution is recommended in selecting a value.
<a id="GUC-SHARED-MEMORY-TYPE"></a>

`shared_memory_type` (`enum`) <a id="id-1.6.6.7.2.2.20.1.3"></a> [#](#GUC-SHARED-MEMORY-TYPE)
:   Specifies the shared memory implementation that the server
    should use for the main shared memory region that holds
    PostgreSQL's shared buffers and other
    shared data. Possible values are `mmap` (for
    anonymous shared memory allocated using `mmap`),
    `sysv` (for System V shared memory allocated via
    `shmget`) and `windows` (for Windows
    shared memory). Not all values are supported on all platforms; the
    first supported option is the default for that platform. The use of
    the `sysv` option, which is not the default on any
    platform, is generally discouraged because it typically requires
    non-default kernel settings to allow for large allocations (see [Section 18.4.1](../runtime/kernel-resources.md#SYSVIPC)).
    This parameter can only be set at server start.
<a id="GUC-DYNAMIC-SHARED-MEMORY-TYPE"></a>

`dynamic_shared_memory_type` (`enum`) <a id="id-1.6.6.7.2.2.21.1.3"></a> [#](#GUC-DYNAMIC-SHARED-MEMORY-TYPE)
:   Specifies the dynamic shared memory implementation that the server
    should use. Possible values are `posix` (for POSIX shared
    memory allocated using `shm_open`), `sysv`
    (for System V shared memory allocated via `shmget`),
    `windows` (for Windows shared memory),
    and `mmap` (to simulate shared memory using
    memory-mapped files stored in the data directory).
    Not all values are supported on all platforms; the first supported
    option is usually the default for that platform. The use of the
    `mmap` option, which is not the default on any platform,
    is generally discouraged because the operating system may write
    modified pages back to disk repeatedly, increasing system I/O load;
    however, it may be useful for debugging, when the
    `pg_dynshmem` directory is stored on a RAM disk, or when
    other shared memory facilities are not available.
    This parameter can only be set at server start.
<a id="GUC-MIN-DYNAMIC-SHARED-MEMORY"></a>

`min_dynamic_shared_memory` (`integer`) <a id="id-1.6.6.7.2.2.22.1.3"></a> [#](#GUC-MIN-DYNAMIC-SHARED-MEMORY)
:   Specifies the amount of memory that should be allocated at server
    startup for use by parallel queries. When this memory region is
    insufficient or exhausted by concurrent queries, new parallel queries
    try to allocate extra shared memory temporarily from the operating
    system using the method configured with
    `dynamic_shared_memory_type`, which may be slower due
    to memory management overheads. Memory that is allocated at startup
    with `min_dynamic_shared_memory` is affected by
    the `huge_pages` setting on operating systems where
    that is supported, and may be more likely to benefit from larger pages
    on operating systems where that is managed automatically.
    The default value is `0` (none). This parameter can
    only be set at server start.

<a id="RUNTIME-CONFIG-RESOURCE-DISK"></a>

### 19.4.2. Disk [#](#RUNTIME-CONFIG-RESOURCE-DISK)

<a id="GUC-TEMP-FILE-LIMIT"></a>

`temp_file_limit` (`integer`) <a id="id-1.6.6.7.3.2.1.1.3"></a> [#](#GUC-TEMP-FILE-LIMIT)
:   Specifies the maximum amount of disk space that a process can use
    for temporary files, such as sort and hash temporary files, or the
    storage file for a held cursor. A transaction attempting to exceed
    this limit will be canceled.
    If this value is specified without units, it is taken as kilobytes.
    `-1` (the default) means no limit.
    Only superusers and users with the appropriate `SET`
    privilege can change this setting.

    This setting constrains the total space used at any instant by all
    temporary files used by a given PostgreSQL process.
    It should be noted that disk space used for explicit temporary
    tables, as opposed to temporary files used behind-the-scenes in query
    execution, does *not* count against this limit.
<a id="GUC-FILE-COPY-METHOD"></a>

`file_copy_method` (`enum`) <a id="id-1.6.6.7.3.2.2.1.3"></a> [#](#GUC-FILE-COPY-METHOD)
:   Specifies the method used to copy files.
    Possible values are `COPY` (default) and
    `CLONE` (if operating support is available).

    This parameter affects:

    * `CREATE DATABASE ... STRATEGY=FILE_COPY`
    * `ALTER DATABASE ... SET TABLESPACE ...`

    `CLONE` uses the `copy_file_range()`
    (Linux, FreeBSD) or `copyfile`
    (macOS) system calls, giving the kernel the opportunity to share disk
    blocks or push work down to lower layers on some file systems.
<a id="GUC-FILE-EXTEND-METHOD"></a>

`file_extend_method` (`enum`) <a id="id-1.6.6.7.3.2.3.1.3"></a> [#](#GUC-FILE-EXTEND-METHOD)
:   Specifies the method used to extend data files during bulk operations
    such as `COPY`. The first available option is used as
    the default, depending on the operating system:

    * `posix_fallocate` (Unix) uses the standard POSIX
      interface for allocating disk space, but is missing on some systems.
      If it is present but the underlying file system doesn't support it,
      this option silently falls back to `write_zeros`.
      Current versions of BTRFS are known to disable compression when
      this option is used.
      This is the default on systems that have the function.
    * `write_zeros` extends files by writing out blocks
      of zero bytes. This is the default on systems that don't have the
      function `posix_fallocate`.

    The `write_zeros` method is always used when data
    files are extended by 8 blocks or fewer.
<a id="GUC-MAX-NOTIFY-QUEUE-PAGES"></a>

`max_notify_queue_pages` (`integer`) <a id="id-1.6.6.7.3.2.4.1.3"></a> [#](#GUC-MAX-NOTIFY-QUEUE-PAGES)
:   Specifies the maximum amount of allocated pages for
    [NOTIFY](../../reference/sql-commands/sql-notify.md) / [LISTEN](../../reference/sql-commands/sql-listen.md) queue.
    The default value is 1048576. For 8 KB pages it allows to consume
    up to 8 GB of disk space.
    This parameter can only be set at server start.

<a id="RUNTIME-CONFIG-RESOURCE-KERNEL"></a>

### 19.4.3. Kernel Resource Usage [#](#RUNTIME-CONFIG-RESOURCE-KERNEL)

<a id="GUC-MAX-FILES-PER-PROCESS"></a>

`max_files_per_process` (`integer`) <a id="id-1.6.6.7.4.2.1.1.3"></a> [#](#GUC-MAX-FILES-PER-PROCESS)
:   Sets the maximum number of open files each server subprocess is
    allowed to open simultaneously; files already opened in the
    postmaster are not counted toward this limit. The default is one
    thousand files.

    If the kernel is enforcing
    a safe per-process limit, you don't need to worry about this setting.
    But on some platforms (notably, most BSD systems), the kernel will
    allow individual processes to open many more files than the system
    can actually support if many processes all try to open
    that many files. If you find yourself seeing “Too many open
    files” failures, try reducing this setting.
    This parameter can only be set at server start.

<a id="RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER"></a>

### 19.4.4. Background Writer [#](#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER)

There is a separate server
process called the *background writer*, whose function
is to issue writes of “dirty” (new or modified) shared
buffers. When the number of clean shared buffers appears to be
insufficient, the background writer writes some dirty buffers to the
file system and marks them as clean. This reduces the likelihood
that server processes handling user queries will be unable to find
clean buffers and have to write dirty buffers themselves.
However, the background writer does cause a net overall
increase in I/O load, because while a repeatedly-dirtied page might
otherwise be written only once per checkpoint interval, the
background writer might write it several times as it is dirtied
in the same interval. The parameters discussed in this subsection
can be used to tune the behavior for local needs.

<a id="GUC-BGWRITER-DELAY"></a>

`bgwriter_delay` (`integer`) <a id="id-1.6.6.7.5.3.1.1.3"></a> [#](#GUC-BGWRITER-DELAY)
:   Specifies the delay between activity rounds for the
    background writer. In each round the writer issues writes
    for some number of dirty buffers (controllable by the
    following parameters). It then sleeps for
    the length of `bgwriter_delay`, and repeats.
    When there are no dirty buffers in the
    buffer pool, though, it goes into a longer sleep regardless of
    `bgwriter_delay`.
    If this value is specified without units, it is taken as milliseconds.
    The default value is 200
    milliseconds (`200ms`). Note that on some systems, the
    effective resolution of sleep delays is 10 milliseconds; setting
    `bgwriter_delay` to a value that is not a multiple of 10
    might have the same results as setting it to the next higher multiple
    of 10. This parameter can only be set in the
    `postgresql.conf` file or on the server command line.
<a id="GUC-BGWRITER-LRU-MAXPAGES"></a>

`bgwriter_lru_maxpages` (`integer`) <a id="id-1.6.6.7.5.3.2.1.3"></a> [#](#GUC-BGWRITER-LRU-MAXPAGES)
:   In each round, no more than this many buffers will be written
    by the background writer. Setting this to zero disables
    background writing. (Note that checkpoints, which are managed by
    a separate, dedicated auxiliary process, are unaffected.)
    The default value is 100 buffers.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-BGWRITER-LRU-MULTIPLIER"></a>

`bgwriter_lru_multiplier` (`floating point`) <a id="id-1.6.6.7.5.3.3.1.3"></a> [#](#GUC-BGWRITER-LRU-MULTIPLIER)
:   The number of dirty buffers written in each round is based on the
    number of new buffers that have been needed by server processes
    during recent rounds. The average recent need is multiplied by
    `bgwriter_lru_multiplier` to arrive at an estimate of the
    number of buffers that will be needed during the next round. Dirty
    buffers are written until there are that many clean, reusable buffers
    available. (However, no more than `bgwriter_lru_maxpages`
    buffers will be written per round.)
    Thus, a setting of 1.0 represents a “just in time” policy
    of writing exactly the number of buffers predicted to be needed.
    Larger values provide some cushion against spikes in demand,
    while smaller values intentionally leave writes to be done by
    server processes.
    The default is 2.0.
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-BGWRITER-FLUSH-AFTER"></a>

`bgwriter_flush_after` (`integer`) <a id="id-1.6.6.7.5.3.4.1.3"></a> [#](#GUC-BGWRITER-FLUSH-AFTER)
:   Whenever more than this amount of data has
    been written by the background writer, attempt to force the OS to issue these
    writes to the underlying storage. Doing so will limit the amount of
    dirty data in the kernel's page cache, reducing the likelihood of
    stalls when an `fsync` is issued at the end of a checkpoint, or when
    the OS writes data back in larger batches in the background. Often
    that will result in greatly reduced transaction latency, but there
    also are some cases, especially with workloads that are bigger than
    [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS), but smaller than the OS's page
    cache, where performance might degrade. This setting may have no
    effect on some platforms.
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The valid range is between
    `0`, which disables forced writeback, and
    `2MB`. The default is `512kB` on Linux,
    `0` elsewhere. (If `BLCKSZ` is not 8kB,
    the default and maximum values scale proportionally to it.)
    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.

Smaller values of `bgwriter_lru_maxpages` and
`bgwriter_lru_multiplier` reduce the extra I/O load
caused by the background writer, but make it more likely that server
processes will have to issue writes for themselves, delaying interactive
queries.

<a id="RUNTIME-CONFIG-RESOURCE-IO"></a>

### 19.4.5. I/O [#](#RUNTIME-CONFIG-RESOURCE-IO)

<a id="GUC-BACKEND-FLUSH-AFTER"></a>

`backend_flush_after` (`integer`) <a id="id-1.6.6.7.6.2.1.1.3"></a> [#](#GUC-BACKEND-FLUSH-AFTER)
:   Whenever more than this amount of data has
    been written by a single backend, attempt to force the OS to issue
    these writes to the underlying storage. Doing so will limit the
    amount of dirty data in the kernel's page cache, reducing the
    likelihood of stalls when an `fsync` is issued at the end of a
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
    and `2MB`. The default is `0`, i.e., no
    forced writeback. (If `BLCKSZ` is not 8kB,
    the maximum value scales proportionally to it.)
<a id="GUC-EFFECTIVE-IO-CONCURRENCY"></a>

`effective_io_concurrency` (`integer`) <a id="id-1.6.6.7.6.2.2.1.3"></a> [#](#GUC-EFFECTIVE-IO-CONCURRENCY)
:   Sets the number of concurrent storage I/O operations that
    PostgreSQL expects can be executed
    simultaneously. Raising this value will increase the number of I/O
    operations that any individual PostgreSQL
    session attempts to initiate in parallel. The allowed range is
    `1` to `1000`, or
    `0` to disable issuance of asynchronous I/O requests.
    The default is `16`.

    Higher values will have the most impact on higher latency storage
    where queries otherwise experience noticeable I/O stalls and on
    devices with high IOPs. Unnecessarily high values may increase I/O
    latency for all queries on the system.

    On systems with prefetch advice support,
    `effective_io_concurrency` also controls the
    prefetch distance.

    This value can be overridden for tables in a particular tablespace by
    setting the tablespace parameter of the same name (see [ALTER TABLESPACE](../../reference/sql-commands/sql-altertablespace.md)).
<a id="GUC-MAINTENANCE-IO-CONCURRENCY"></a>

`maintenance_io_concurrency` (`integer`) <a id="id-1.6.6.7.6.2.3.1.3"></a> [#](#GUC-MAINTENANCE-IO-CONCURRENCY)
:   Similar to `effective_io_concurrency`, but used
    for maintenance work that is done on behalf of many client sessions.

    The default is `16`. This value can be overridden
    for tables in a particular tablespace by setting the tablespace
    parameter of the same name (see [ALTER TABLESPACE](../../reference/sql-commands/sql-altertablespace.md)).
<a id="GUC-IO-MAX-COMBINE-LIMIT"></a>

`io_max_combine_limit` (`integer`) <a id="id-1.6.6.7.6.2.4.1.3"></a> [#](#GUC-IO-MAX-COMBINE-LIMIT)
:   Controls the largest I/O size in operations that combine I/O, and silently
    limits the user-settable parameter `io_combine_limit`.
    This parameter can only be set at server start.
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The maximum possible size depends on the operating system and block
    size, but is typically 1MB on Unix and 128kB on Windows.
    The default is 128kB.
<a id="GUC-IO-COMBINE-LIMIT"></a>

`io_combine_limit` (`integer`) <a id="id-1.6.6.7.6.2.5.1.3"></a> [#](#GUC-IO-COMBINE-LIMIT)
:   Controls the largest I/O size in operations that combine I/O. If set
    higher than the `io_max_combine_limit` parameter, the
    lower value will silently be used instead, so both may need to be raised
    to increase the I/O size.
    If this value is specified without units, it is taken as blocks,
    that is `BLCKSZ` bytes, typically 8kB.
    The maximum possible size depends on the operating system and block
    size, but is typically 1MB on Unix and 128kB on Windows.
    The default is 128kB.
<a id="GUC-IO-MAX-CONCURRENCY"></a>

`io_max_concurrency` (`integer`) <a id="id-1.6.6.7.6.2.6.1.3"></a> [#](#GUC-IO-MAX-CONCURRENCY)
:   Controls the maximum number of I/O operations that one process can
    execute simultaneously.

    The default setting of `-1` selects a number based
    on [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS) and the maximum number of
    processes ([max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS), [autovacuum_worker_slots](runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS), [max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) and [max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS)), but not more than
    `64`.

    This parameter can only be set at server start.
<a id="GUC-IO-METHOD"></a>

`io_method` (`enum`) <a id="id-1.6.6.7.6.2.7.1.3"></a> [#](#GUC-IO-METHOD)
:   Selects the method for executing asynchronous I/O.
    Possible values are:

    * `worker` (execute asynchronous I/O using worker processes)
    * `io_uring` (execute asynchronous I/O using
      io_uring, requires a build with
      [`--with-liburing`](../installation/install-make.md#CONFIGURE-OPTION-WITH-LIBURING) /
      [`-Dliburing`](../installation/install-meson.md#CONFIGURE-WITH-LIBURING-MESON))
    * `sync` (execute asynchronous-eligible I/O synchronously)

    The default is `worker`.

    This parameter can only be set at server start.
<a id="GUC-IO-WORKERS"></a>

`io_workers` (`integer`) <a id="id-1.6.6.7.6.2.8.1.3"></a> [#](#GUC-IO-WORKERS)
:   Selects the number of I/O worker processes to use. The default is
    3. This parameter can only be set in the
    `postgresql.conf` file or on the server command
    line.

    Only has an effect if [io_method](runtime-config-resource.md#GUC-IO-METHOD) is set to
    `worker`.

<a id="RUNTIME-CONFIG-RESOURCE-WORKER-PROCESSES"></a>

### 19.4.6. Worker Processes [#](#RUNTIME-CONFIG-RESOURCE-WORKER-PROCESSES)

<a id="GUC-MAX-WORKER-PROCESSES"></a>

`max_worker_processes` (`integer`) <a id="id-1.6.6.7.7.2.1.1.3"></a> [#](#GUC-MAX-WORKER-PROCESSES)
:   Sets the maximum number of background processes that the cluster
    can support. This parameter can only be set at server start. The
    default is 8.

    When running a standby server, you must set this parameter to the
    same or higher value than on the primary server. Otherwise, queries
    will not be allowed in the standby server.

    When changing this value, consider also adjusting
    [max_parallel_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS),
    [max_parallel_maintenance_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS), and
    [max_parallel_workers_per_gather](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER).
<a id="GUC-MAX-PARALLEL-WORKERS-PER-GATHER"></a>

`max_parallel_workers_per_gather` (`integer`) <a id="id-1.6.6.7.7.2.2.1.3"></a> [#](#GUC-MAX-PARALLEL-WORKERS-PER-GATHER)
:   Sets the maximum number of workers that can be started by a single
    `Gather` or `Gather Merge` node.
    Parallel workers are taken from the pool of processes established by
    [max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES), limited by
    [max_parallel_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS). Note that the requested
    number of workers may not actually be available at run time. If this
    occurs, the plan will run with fewer workers than expected, which may
    be inefficient. The default value is 2. Setting this value to 0
    disables parallel query execution.

    Note that parallel queries may consume very substantially more
    resources than non-parallel queries, because each worker process is
    a completely separate process which has roughly the same impact on the
    system as an additional user session. This should be taken into
    account when choosing a value for this setting, as well as when
    configuring other settings that control resource utilization, such
    as [work_mem](runtime-config-resource.md#GUC-WORK-MEM). Resource limits such as
    `work_mem` are applied individually to each worker,
    which means the total utilization may be much higher across all
    processes than it would normally be for any single process.
    For example, a parallel query using 4 workers may use up to 5 times
    as much CPU time, memory, I/O bandwidth, and so forth as a query which
    uses no workers at all.

    For more information on parallel query, see
    [Chapter 15](../../the-sql-language/parallel-query/README.md).
<a id="GUC-MAX-PARALLEL-MAINTENANCE-WORKERS"></a>

`max_parallel_maintenance_workers` (`integer`) <a id="id-1.6.6.7.7.2.3.1.3"></a> [#](#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS)
:   Sets the maximum number of parallel workers that can be
    started by a single utility command. Currently, the parallel
    utility commands that support the use of parallel workers are
    `CREATE INDEX` when building a B-tree,
    GIN, or BRIN index,
    and `VACUUM` without `FULL`
    option. Parallel workers are taken from the pool of processes
    established by [max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES), limited
    by [max_parallel_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS). Note that the requested
    number of workers may not actually be available at run time.
    If this occurs, the utility operation will run with fewer
    workers than expected. The default value is 2. Setting this
    value to 0 disables the use of parallel workers by utility
    commands.

    Note that parallel utility commands should not consume
    substantially more memory than equivalent non-parallel
    operations. This strategy differs from that of parallel
    query, where resource limits generally apply per worker
    process. Parallel utility commands treat the resource limit
    `maintenance_work_mem` as a limit to be applied to
    the entire utility command, regardless of the number of
    parallel worker processes. However, parallel utility
    commands may still consume substantially more CPU resources
    and I/O bandwidth.
<a id="GUC-MAX-PARALLEL-WORKERS"></a>

`max_parallel_workers` (`integer`) <a id="id-1.6.6.7.7.2.4.1.3"></a> [#](#GUC-MAX-PARALLEL-WORKERS)
:   Sets the maximum number of workers that the cluster can support for
    parallel operations. The default value is 8. When increasing or
    decreasing this value, consider also adjusting
    [max_parallel_maintenance_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS) and
    [max_parallel_workers_per_gather](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER).
    Also, note that a setting for this value which is higher than
    [max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) will have no effect,
    since parallel workers are taken from the pool of worker processes
    established by that setting.
<a id="GUC-PARALLEL-LEADER-PARTICIPATION"></a>

`parallel_leader_participation` (`boolean`) <a id="id-1.6.6.7.7.2.5.1.3"></a> [#](#GUC-PARALLEL-LEADER-PARTICIPATION)
:   Allows the leader process to execute the query plan under
    `Gather` and `Gather Merge` nodes
    instead of waiting for worker processes. The default is
    `on`. Setting this value to `off`
    reduces the likelihood that workers will become blocked because the
    leader is not reading tuples fast enough, but requires the leader
    process to wait for worker processes to start up before the first
    tuples can be produced. The degree to which the leader can help or
    hinder performance depends on the plan type, number of workers and
    query duration.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-resource.html)（英文原文，待翻譯）
