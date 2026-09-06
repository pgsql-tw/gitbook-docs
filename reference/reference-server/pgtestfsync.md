<a id="id-1.9.5.11.1"></a>

## pg_test_fsync

pg_test_fsync — determine fastest `wal_sync_method` for PostgreSQL

## Synopsis

<a id="id-1.9.5.11.4.1"></a>

`pg_test_fsync` [*`option`*...]

<a id="id-1.9.5.11.5"></a>

## Description

pg_test_fsync is intended to give you a reasonable
idea of what the fastest [wal_sync_method](../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-SYNC-METHOD) is on your
specific system,
as well as supplying diagnostic information in the event of an identified I/O
problem. However, differences shown by
pg_test_fsync might not make any significant
difference in real database throughput, especially since many database servers
are not speed-limited by their write-ahead logs.
pg_test_fsync reports average file sync operation
time in microseconds for each `wal_sync_method`, which can also be used to
inform efforts to optimize the value of [commit_delay](../../server-administration/runtime-config/runtime-config-wal.md#GUC-COMMIT-DELAY).

<a id="id-1.9.5.11.6"></a>

## Options

pg_test_fsync accepts the following
command-line options:

`-f`<br>`--filename`
:   Specifies the file name to write test data in.
    This file should be in the same file system that the
    `pg_wal` directory is or will be placed in.
    (`pg_wal` contains the WAL files.)
    The default is `pg_test_fsync.out` in the current
    directory.

`-s`<br>`--secs-per-test`
:   Specifies the number of seconds for each test. The more time
    per test, the greater the test's accuracy, but the longer it takes
    to run. The default is 5 seconds, which allows the program to
    complete in under 2 minutes.

`-V`<br>`--version`
:   Print the pg_test_fsync version and exit.

`-?`<br>`--help`
:   Show help about pg_test_fsync command line
    arguments, and exit.

<a id="id-1.9.5.11.7"></a>

## Environment

The environment variable `PG_COLOR` specifies whether to use
color in diagnostic messages. Possible values are
`always`, `auto` and
`never`.

<a id="id-1.9.5.11.8"></a>

## See Also

[postgres](app-postgres.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgtestfsync.html)（英文原文，待翻譯）
