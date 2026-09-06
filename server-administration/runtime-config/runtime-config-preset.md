## 19.15. Preset Options [#](#RUNTIME-CONFIG-PRESET)

The following “parameters” are read-only.
As such, they have been excluded from the sample
`postgresql.conf` file. These options report
various aspects of PostgreSQL behavior
that might be of interest to certain applications, particularly
administrative front-ends.
Most of them are determined when PostgreSQL
is compiled or when it is installed.

<a id="GUC-BLOCK-SIZE"></a>

`block_size` (`integer`) <a id="id-1.6.6.18.3.1.1.3"></a> [#](#GUC-BLOCK-SIZE)
:   Reports the size of a disk block. It is determined by the value
    of `BLCKSZ` when building the server. The default
    value is 8192 bytes. The meaning of some configuration
    variables (such as [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS)) is
    influenced by `block_size`. See [Section 19.4](runtime-config-resource.md) for information.
<a id="GUC-DATA-CHECKSUMS"></a>

`data_checksums` (`boolean`) <a id="id-1.6.6.18.3.2.1.3"></a> [#](#GUC-DATA-CHECKSUMS)
:   Reports whether data checksums are enabled for this cluster.
    See [`-k`](../../reference/reference-server/app-initdb.md#APP-INITDB-DATA-CHECKSUMS) for more information.
<a id="GUC-DATA-DIRECTORY-MODE"></a>

`data_directory_mode` (`integer`) <a id="id-1.6.6.18.3.3.1.3"></a> [#](#GUC-DATA-DIRECTORY-MODE)
:   On Unix systems this parameter reports the permissions the data
    directory (defined by [data_directory](runtime-config-file-locations.md#GUC-DATA-DIRECTORY))
    had at server startup.
    (On Microsoft Windows this parameter will always display
    `0700`.) See
    [the
    initdb `-g` option](../../reference/reference-server/app-initdb.md#APP-INITDB-ALLOW-GROUP-ACCESS)
    for more information.
<a id="GUC-DEBUG-ASSERTIONS"></a>

`debug_assertions` (`boolean`) <a id="id-1.6.6.18.3.4.1.3"></a> [#](#GUC-DEBUG-ASSERTIONS)
:   Reports whether PostgreSQL has been built
    with assertions enabled. That is the case if the
    macro `USE_ASSERT_CHECKING` is defined
    when PostgreSQL is built (accomplished
    e.g., by the `configure` option
    `--enable-cassert`). By
    default PostgreSQL is built without
    assertions.
<a id="GUC-HUGE-PAGES-STATUS"></a>

`huge_pages_status` (`enum`) <a id="id-1.6.6.18.3.5.1.3"></a> [#](#GUC-HUGE-PAGES-STATUS)
:   Reports the state of huge pages in the current instance:
    `on`, `off`, or
    `unknown` (if displayed with
    `postgres -C`).
    This parameter is useful to determine whether allocation of huge pages
    was successful under `huge_pages=try`.
    See [huge_pages](runtime-config-resource.md#GUC-HUGE-PAGES) for more information.
<a id="GUC-INTEGER-DATETIMES"></a>

`integer_datetimes` (`boolean`) <a id="id-1.6.6.18.3.6.1.3"></a> [#](#GUC-INTEGER-DATETIMES)
:   Reports whether PostgreSQL was built with support for
    64-bit-integer dates and times. As of PostgreSQL 10,
    this is always `on`.
<a id="GUC-IN-HOT-STANDBY"></a>

`in_hot_standby` (`boolean`) <a id="id-1.6.6.18.3.7.1.3"></a> [#](#GUC-IN-HOT-STANDBY)
:   Reports whether the server is currently in hot standby mode. When
    this is `on`, all transactions are forced to be
    read-only. Within a session, this can change only if the server is
    promoted to be primary. See [Section 26.4](../high-availability/hot-standby.md) for more
    information.
<a id="GUC-MAX-FUNCTION-ARGS"></a>

`max_function_args` (`integer`) <a id="id-1.6.6.18.3.8.1.3"></a> [#](#GUC-MAX-FUNCTION-ARGS)
:   Reports the maximum number of function arguments. It is determined by
    the value of `FUNC_MAX_ARGS` when building the server. The
    default value is 100 arguments.
<a id="GUC-MAX-IDENTIFIER-LENGTH"></a>

`max_identifier_length` (`integer`) <a id="id-1.6.6.18.3.9.1.3"></a> [#](#GUC-MAX-IDENTIFIER-LENGTH)
:   Reports the maximum identifier length. It is determined as one
    less than the value of `NAMEDATALEN` when building
    the server. The default value of `NAMEDATALEN` is
    64; therefore the default
    `max_identifier_length` is 63 bytes, which
    can be less than 63 characters when using multibyte encodings.
<a id="GUC-MAX-INDEX-KEYS"></a>

`max_index_keys` (`integer`) <a id="id-1.6.6.18.3.10.1.3"></a> [#](#GUC-MAX-INDEX-KEYS)
:   Reports the maximum number of index keys. It is determined by
    the value of `INDEX_MAX_KEYS` when building the server. The
    default value is 32 keys.
<a id="GUC-NUM-OS-SEMAPHORES"></a>

`num_os_semaphores` (`integer`) <a id="id-1.6.6.18.3.11.1.3"></a> [#](#GUC-NUM-OS-SEMAPHORES)
:   Reports the number of semaphores that are needed for the server based
    on the configured number of allowed connections
    ([max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS)), allowed autovacuum worker
    processes ([autovacuum_max_workers](runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS)), allowed WAL
    sender processes ([max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS)), allowed
    background processes ([max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)), etc.
<a id="GUC-SEGMENT-SIZE"></a>

`segment_size` (`integer`) <a id="id-1.6.6.18.3.12.1.3"></a> [#](#GUC-SEGMENT-SIZE)
:   Reports the number of blocks (pages) that can be stored within a file
    segment. It is determined by the value of `RELSEG_SIZE`
    when building the server. The maximum size of a segment file in bytes
    is equal to `segment_size` multiplied by
    `block_size`; by default this is 1GB.
<a id="GUC-SERVER-ENCODING"></a>

`server_encoding` (`string`) <a id="id-1.6.6.18.3.13.1.3"></a> <a id="id-1.6.6.18.3.13.1.4"></a> [#](#GUC-SERVER-ENCODING)
:   Reports the database encoding (character set).
    It is determined when the database is created. Ordinarily,
    clients need only be concerned with the value of [client_encoding](runtime-config-client.md#GUC-CLIENT-ENCODING).
<a id="GUC-SERVER-VERSION"></a>

`server_version` (`string`) <a id="id-1.6.6.18.3.14.1.3"></a> [#](#GUC-SERVER-VERSION)
:   Reports the version number of the server. It is determined by the
    value of `PG_VERSION` when building the server.
<a id="GUC-SERVER-VERSION-NUM"></a>

`server_version_num` (`integer`) <a id="id-1.6.6.18.3.15.1.3"></a> [#](#GUC-SERVER-VERSION-NUM)
:   Reports the version number of the server as an integer. It is determined
    by the value of `PG_VERSION_NUM` when building the server.
<a id="GUC-SHARED-MEMORY-SIZE"></a>

`shared_memory_size` (`integer`) <a id="id-1.6.6.18.3.16.1.3"></a> [#](#GUC-SHARED-MEMORY-SIZE)
:   Reports the size of the main shared memory area, rounded up to the
    nearest megabyte.
<a id="GUC-SHARED-MEMORY-SIZE-IN-HUGE-PAGES"></a>

`shared_memory_size_in_huge_pages` (`integer`) <a id="id-1.6.6.18.3.17.1.3"></a> [#](#GUC-SHARED-MEMORY-SIZE-IN-HUGE-PAGES)
:   Reports the number of huge pages that are needed for the main shared
    memory area based on the specified [huge_page_size](runtime-config-resource.md#GUC-HUGE-PAGE-SIZE).
    If huge pages are not supported, this will be `-1`.

    This setting is supported only on Linux. It
    is always set to `-1` on other platforms. For more
    details about using huge pages on Linux, see
    [Section 18.4.5](../runtime/kernel-resources.md#LINUX-HUGE-PAGES).
<a id="GUC-SSL-LIBRARY"></a>

`ssl_library` (`string`) <a id="id-1.6.6.18.3.18.1.3"></a> [#](#GUC-SSL-LIBRARY)
:   Reports the name of the SSL library that this
    PostgreSQL server was built with (even if
    SSL is not currently configured or in use on this instance), for
    example `OpenSSL`, or an empty string if none.
<a id="GUC-WAL-BLOCK-SIZE"></a>

`wal_block_size` (`integer`) <a id="id-1.6.6.18.3.19.1.3"></a> [#](#GUC-WAL-BLOCK-SIZE)
:   Reports the size of a WAL disk block. It is determined by the value
    of `XLOG_BLCKSZ` when building the server. The default value
    is 8192 bytes.
<a id="GUC-WAL-SEGMENT-SIZE"></a>

`wal_segment_size` (`integer`) <a id="id-1.6.6.18.3.20.1.3"></a> [#](#GUC-WAL-SEGMENT-SIZE)
:   Reports the size of write ahead log segments. The default value is
    16MB. See [Section 28.5](../wal/wal-configuration.md) for more information.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-preset.html)（英文原文，待翻譯）
