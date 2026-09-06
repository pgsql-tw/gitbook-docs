# pg\_standby

pg\_standby — supports the creation of a PostgreSQL warm standby server

### Synopsis

`pg_standby` \[_`option`_...] _`archivelocation`_ _`nextwalfile`_ _`walfilepath`_ \[_`restartwalfile`_]

### Description

pg\_standby supports creation of a “warm standby” database server. It is designed to be a production-ready program, as well as a customizable template should you require specific modifications.

pg\_standby is designed to be a waiting `restore_command`, which is needed to turn a standard archive recovery into a warm standby operation. Other configuration is required as well, all of which is described in the main server manual (see [Section 26.2](https://www.postgresql.org/docs/10/static/warm-standby.html)).

To configure a standby server to use pg\_standby, put this into its `recovery.conf` configuration file:

```
restore_command = 'pg_standby archiveDir %f %p %r'
```

where _`archiveDir`_ is the directory from which WAL segment files should be restored.

If _`restartwalfile`_ is specified, normally by using the `%r` macro, then all WAL files logically preceding this file will be removed from _`archivelocation`_. This minimizes the number of files that need to be retained, while preserving crash-restart capability. Use of this parameter is appropriate if the _`archivelocation`_ is a transient staging area for this particular standby server, but _not_ when the _`archivelocation`_ is intended as a long-term WAL archive area.

pg\_standby assumes that _`archivelocation`_ is a directory readable by the server-owning user. If _`restartwalfile`_ (or `-k`) is specified, the _`archivelocation`_ directory must be writable too.

There are two ways to fail over to a “warm standby” database server when the master server fails:Smart Failover

In smart failover, the server is brought up after applying all WAL files available in the archive. This results in zero data loss, even if the standby server has fallen behind, but if there is a lot of unapplied WAL it can be a long time before the standby server becomes ready. To trigger a smart failover, create a trigger file containing the word `smart`, or just create it and leave it empty.Fast Failover

In fast failover, the server is brought up immediately. Any WAL files in the archive that have not yet been applied will be ignored, and all transactions in those files are lost. To trigger a fast failover, create a trigger file and write the word `fast` into it. pg\_standby can also be configured to execute a fast failover automatically if no new WAL file appears within a defined interval.

### Options

pg\_standby accepts the following command-line arguments:

`-c`

Use `cp` or `copy` command to restore WAL files from archive. This is the only supported behavior so this option is useless.`-d`

Print lots of debug logging output on `stderr`.

`-k`

Remove files from _`archivelocation`_ so that no more than this many WAL files before the current one are kept in the archive. Zero (the default) means not to remove any files from _`archivelocation`_. This parameter will be silently ignored if _`restartwalfile`_ is specified, since that specification method is more accurate in determining the correct archive cut-off point. Use of this parameter is _deprecated_ as of PostgreSQL 8.3; it is safer and more efficient to specify a _`restartwalfile`_ parameter. A too small setting could result in removal of files that are still needed for a restart of the standby server, while a too large setting wastes archive space.

`-r` _`maxretries`_

Set the maximum number of times to retry the copy command if it fails (default 3). After each failure, we wait for _`sleeptime`_ \* _`num_retries`_ so that the wait time increases progressively. So by default, we will wait 5 secs, 10 secs, then 15 secs before reporting the failure back to the standby server. This will be interpreted as end of recovery and the standby will come up fully as a result.

`-s` _`sleeptime`_

Set the number of seconds (up to 60, default 5) to sleep between tests to see if the WAL file to be restored is available in the archive yet. The default setting is not necessarily recommended; consult [Section 26.2](https://www.postgresql.org/docs/10/static/warm-standby.html) for discussion.

`-t` _`triggerfile`_

Specify a trigger file whose presence should cause failover. It is recommended that you use a structured file name to avoid confusion as to which server is being triggered when multiple servers exist on the same system; for example `/tmp/pgsql.trigger.5432`.

`-V`\
`--version`

Print the pg\_standby version and exit.

`-w` _`maxwaittime`_

Set the maximum number of seconds to wait for the next WAL file, after which a fast failover will be performed. A setting of zero (the default) means wait forever. The default setting is not necessarily recommended; consult [Section 26.2](https://www.postgresql.org/docs/10/static/warm-standby.html) for discussion.

`-?`\
`--help`

Show help about pg\_standby command line arguments, and exit.

### Notes

pg\_standby is designed to work with PostgreSQL 8.2 and later.

PostgreSQL 8.3 provides the `%r` macro, which is designed to let pg\_standby know the last file it needs to keep. With PostgreSQL 8.2, the `-k` option must be used if archive cleanup is required. This option remains available in 8.3, but its use is deprecated.

PostgreSQL 8.4 provides the `recovery_end_command` option. Without this option a leftover trigger file can be hazardous.

pg\_standby is written in C and has an easy-to-modify source code, with specifically designated sections to modify for your own needs

### Examples

On Linux or Unix systems, you might use:

```
archive_command = 'cp %p .../archive/%f'

restore_command = 'pg_standby -d -s 2 -t /tmp/pgsql.trigger.5442 .../archive %f %p %r 2>>standby.log'

recovery_end_command = 'rm -f /tmp/pgsql.trigger.5442'
```

where the archive directory is physically located on the standby server, so that the `archive_command` is accessing it across NFS, but the files are local to the standby (enabling use of `ln`). This will:

* produce debugging output in `standby.log`
* sleep for 2 seconds between checks for next WAL file availability
* stop waiting only when a trigger file called `/tmp/pgsql.trigger.5442` appears, and perform failover according to its content
* remove the trigger file when recovery ends
* remove no-longer-needed files from the archive directory

On Windows, you might use:

```
archive_command = 'copy %p ...\\archive\\%f'

restore_command = 'pg_standby -d -s 5 -t C:\pgsql.trigger.5442 ...\archive %f %p %r 2>>standby.log'

recovery_end_command = 'del C:\pgsql.trigger.5442'
```

Note that backslashes need to be doubled in the `archive_command`, but _not_ in the `restore_command` or `recovery_end_command`. This will:

* use the `copy` command to restore WAL files from archive
* produce debugging output in `standby.log`
* sleep for 5 seconds between checks for next WAL file availability
* stop waiting only when a trigger file called `C:\pgsql.trigger.5442` appears, and perform failover according to its content
* remove the trigger file when recovery ends
* remove no-longer-needed files from the archive directory

The `copy` command on Windows sets the final file size before the file is completely copied, which would ordinarily confuse pg\_standby. Therefore pg\_standby waits _`sleeptime`_ seconds once it sees the proper file size. GNUWin32's `cp` sets the file size only after the file copy is complete.

Since the Windows example uses `copy` at both ends, either or both servers might be accessing the archive directory across the network.

### Author

Simon Riggs `<`[`simon@2ndquadrant.com`](mailto:simon@2ndquadrant.com)`>`

### See Also

[pg\_archivecleanup](https://www.postgresql.org/docs/10/static/pgarchivecleanup.html)
