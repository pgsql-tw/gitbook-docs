## 19.14. Error Handling [#](#RUNTIME-CONFIG-ERROR-HANDLING)

<a id="GUC-EXIT-ON-ERROR"></a>

`exit_on_error` (`boolean`) <a id="id-1.6.6.17.2.1.1.3"></a> [#](#GUC-EXIT-ON-ERROR)
:   If on, any error will terminate the current session. By default,
    this is set to off, so that only FATAL errors will terminate the
    session.
<a id="GUC-RESTART-AFTER-CRASH"></a>

`restart_after_crash` (`boolean`) <a id="id-1.6.6.17.2.2.1.3"></a> [#](#GUC-RESTART-AFTER-CRASH)
:   When set to on, which is the default, PostgreSQL
    will automatically reinitialize after a backend crash. Leaving this
    value set to on is normally the best way to maximize the availability
    of the database. However, in some circumstances, such as when
    PostgreSQL is being invoked by clusterware, it may be
    useful to disable the restart so that the clusterware can gain
    control and take any actions it deems appropriate.

    This parameter can only be set in the `postgresql.conf`
    file or on the server command line.
<a id="GUC-DATA-SYNC-RETRY"></a>

`data_sync_retry` (`boolean`) <a id="id-1.6.6.17.2.3.1.3"></a> [#](#GUC-DATA-SYNC-RETRY)
:   When set to off, which is the default, PostgreSQL
    will raise a PANIC-level error on failure to flush modified data files
    to the file system. This causes the database server to crash. This
    parameter can only be set at server start.

    On some operating systems, the status of data in the kernel's page
    cache is unknown after a write-back failure. In some cases it might
    have been entirely forgotten, making it unsafe to retry; the second
    attempt may be reported as successful, when in fact the data has been
    lost. In these circumstances, the only way to avoid data loss is to
    recover from the WAL after any failure is reported, preferably
    after investigating the root cause of the failure and replacing any
    faulty hardware.

    If set to on, PostgreSQL will instead
    report an error but continue to run so that the data flushing
    operation can be retried in a later checkpoint. Only set it to on
    after investigating the operating system's treatment of buffered data
    in case of write-back failure.
<a id="GUC-RECOVERY-INIT-SYNC-METHOD"></a>

`recovery_init_sync_method` (`enum`) <a id="id-1.6.6.17.2.4.1.3"></a> [#](#GUC-RECOVERY-INIT-SYNC-METHOD)
:   When set to `fsync`, which is the default,
    PostgreSQL will recursively open and
    synchronize all files in the data directory before crash recovery
    begins. The search for files will follow symbolic links for the WAL
    directory and each configured tablespace (but not any other symbolic
    links). This is intended to make sure that all WAL and data files are
    durably stored on disk before replaying changes. This applies whenever
    starting a database cluster that did not shut down cleanly, including
    copies created with pg_basebackup.

    On Linux, `syncfs` may be used instead, to ask the
    operating system to synchronize the file systems that contain the
    data directory, the WAL files and each tablespace (but not any other
    file systems that may be reachable through symbolic links). This may
    be a lot faster than the `fsync` setting, because it
    doesn't need to open each file one by one. On the other hand, it may
    be slower if a file system is shared by other applications that
    modify a lot of files, since those files will also be written to disk.
    Furthermore, on versions of Linux before 5.8, I/O errors encountered
    while writing data to disk may not be reported to
    PostgreSQL, and relevant error messages may
    appear only in kernel logs.

    This parameter can only be set in the
    `postgresql.conf` file or on the server command line.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-error-handling.html)（英文原文，待翻譯）
