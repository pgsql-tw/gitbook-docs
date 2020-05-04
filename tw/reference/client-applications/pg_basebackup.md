# pg\_basebackup

pg\_basebackup — take a base backup of a PostgreSQL cluster

### Synopsis

`pg_basebackup` \[_`option`_...\]

### Description

pg\_basebackup is used to take base backups of a running PostgreSQL database cluster. These are taken without affecting other clients to the database, and can be used both for point-in-time recovery \(see [Section 25.3](https://www.postgresql.org/docs/12/continuous-archiving.html)\) and as the starting point for a log shipping or streaming replication standby servers \(see [Section 26.2](https://www.postgresql.org/docs/12/warm-standby.html)\).

pg\_basebackup makes a binary copy of the database cluster files, while making sure the system is put in and out of backup mode automatically. Backups are always taken of the entire database cluster; it is not possible to back up individual databases or database objects. For individual database backups, a tool such as [pg\_dump](https://www.postgresql.org/docs/12/app-pgdump.html) must be used.

The backup is made over a regular PostgreSQL connection, and uses the replication protocol. The connection must be made with a superuser or a user having `REPLICATION` permissions \(see [Section 21.2](https://www.postgresql.org/docs/12/role-attributes.html)\), and `pg_hba.conf` must explicitly permit the replication connection. The server must also be configured with [max\_wal\_senders](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-MAX-WAL-SENDERS) set high enough to leave at least one session available for the backup and one for WAL streaming \(if used\).

There can be multiple `pg_basebackup`s running at the same time, but it is better from a performance point of view to take only one backup, and copy the result.

pg\_basebackup can make a base backup from not only the master but also the standby. To take a backup from the standby, set up the standby so that it can accept replication connections \(that is, set `max_wal_senders` and [hot\_standby](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-HOT-STANDBY), and configure [host-based authentication](https://www.postgresql.org/docs/12/auth-pg-hba-conf.html)\). You will also need to enable [full\_page\_writes](https://www.postgresql.org/docs/12/runtime-config-wal.html#GUC-FULL-PAGE-WRITES) on the master.

Note that there are some limitations in an online backup from the standby:

* The backup history file is not created in the database cluster backed up.
* If you are using `-X none`, there is no guarantee that all WAL files required for the backup are archived at the end of backup.
* If the standby is promoted to the master during online backup, the backup fails.
* All WAL records required for the backup must contain sufficient full-page writes, which requires you to enable `full_page_writes` on the master and not to use a tool like pg\_compresslog as `archive_command` to remove full-page writes from WAL files.

### Options

The following command-line options control the location and format of the output.

`-D` _`directory`_  
`--pgdata=`_`directory`_

Directory to write the output to. pg\_basebackup will create the directory and any parent directories if necessary. The directory may already exist, but it is an error if the directory already exists and is not empty.

When the backup is in tar mode, and the directory is specified as `-` \(dash\), the tar file will be written to `stdout`.

This option is required.

`-F` _`format`_  
`--format=`_`format`_

Selects the format for the output. _`format`_ can be one of the following:

`p`  
`plain`

Write the output as plain files, with the same layout as the current data directory and tablespaces. When the cluster has no additional tablespaces, the whole database will be placed in the target directory. If the cluster contains additional tablespaces, the main data directory will be placed in the target directory, but all other tablespaces will be placed in the same absolute path as they have on the server.

This is the default format.

`t`  
`tar`

Write the output as tar files in the target directory. The main data directory will be written to a file named `base.tar`, and all other tablespaces will be named after the tablespace OID.

If the value `-` \(dash\) is specified as target directory, the tar contents will be written to standard output, suitable for piping to for example gzip. This is only possible if the cluster has no additional tablespaces and WAL streaming is not used.

`-r` _`rate`_  
`--max-rate=`_`rate`_

The maximum transfer rate of data transferred from the server. Values are in kilobytes per second. Use a suffix of `M` to indicate megabytes per second. A suffix of `k` is also accepted, and has no effect. Valid values are between 32 kilobytes per second and 1024 megabytes per second.

The purpose is to limit the impact of pg\_basebackup on the running server.

This option always affects transfer of the data directory. Transfer of WAL files is only affected if the collection method is `fetch`.

`-R`  
`--write-recovery-conf`

Create `standby.signal` and append connection settings to `postgresql.auto.conf` in the output directory \(or into the base archive file when using tar format\) to ease setting up a standby server. The `postgresql.auto.conf` file will record the connection settings and, if specified, the replication slot that pg\_basebackup is using, so that the streaming replication will use the same settings later on.

`-T` _`olddir`_=_`newdir`_  
`--tablespace-mapping=`_`olddir`_=_`newdir`_

Relocate the tablespace in directory _`olddir`_ to _`newdir`_ during the backup. To be effective, _`olddir`_ must exactly match the path specification of the tablespace as it is currently defined. \(But it is not an error if there is no tablespace in _`olddir`_ contained in the backup.\) Both _`olddir`_ and _`newdir`_ must be absolute paths. If a path happens to contain a `=` sign, escape it with a backslash. This option can be specified multiple times for multiple tablespaces. See examples below.

If a tablespace is relocated in this way, the symbolic links inside the main data directory are updated to point to the new location. So the new data directory is ready to be used for a new server instance with all tablespaces in the updated locations.

`--waldir=`_`waldir`_

Specifies the location for the write-ahead log directory. _`waldir`_ must be an absolute path. The write-ahead log directory can only be specified when the backup is in plain mode.

`-X` _`method`_  
`--wal-method=`_`method`_

Includes the required write-ahead log files \(WAL files\) in the backup. This will include all write-ahead logs generated during the backup. Unless the method `none` is specified, it is possible to start a postmaster directly in the extracted directory without the need to consult the log archive, thus making this a completely standalone backup.

The following methods for collecting the write-ahead logs are supported:

`n`  
`none`

Don't include write-ahead log in the backup.

`f`  
`fetch`

The write-ahead log files are collected at the end of the backup. Therefore, it is necessary for the [wal\_keep\_segments](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-WAL-KEEP-SEGMENTS) parameter to be set high enough that the log is not removed before the end of the backup. If the log has been rotated when it's time to transfer it, the backup will fail and be unusable.

When tar format mode is used, the write-ahead log files will be written to the `base.tar` file.

`s`  
`stream`

Stream the write-ahead log while the backup is created. This will open a second connection to the server and start streaming the write-ahead log in parallel while running the backup. Therefore, it will use up two connections configured by the [max\_wal\_senders](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-MAX-WAL-SENDERS) parameter. As long as the client can keep up with write-ahead log received, using this mode requires no extra write-ahead logs to be saved on the master.

When tar format mode is used, the write-ahead log files will be written to a separate file named `pg_wal.tar` \(if the server is a version earlier than 10, the file will be named `pg_xlog.tar`\).

This value is the default.

`-z`  
`--gzip`

Enables gzip compression of tar file output, with the default compression level. Compression is only available when using the tar format, and the suffix `.gz` will automatically be added to all tar filenames.

`-Z` _`level`_  
`--compress=`_`level`_

Enables gzip compression of tar file output, and specifies the compression level \(0 through 9, 0 being no compression and 9 being best compression\). Compression is only available when using the tar format, and the suffix `.gz` will automatically be added to all tar filenames.

The following command-line options control the generation of the backup and the running of the program.

`-c` _`fast|spread`_  
`--checkpoint=`_`fast|spread`_

Sets checkpoint mode to fast \(immediate\) or spread \(default\) \(see [Section 25.3.3](https://www.postgresql.org/docs/12/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP)\).

`-C`  
`--create-slot`

This option causes creation of a replication slot named by the `--slot` option before starting the backup. An error is raised if the slot already exists.

`-l` _`label`_  
`--label=`_`label`_

Sets the label for the backup. If none is specified, a default value of “`pg_basebackup base backup`” will be used.

`-n`  
`--no-clean`

By default, when `pg_basebackup` aborts with an error, it removes any directories it might have created before discovering that it cannot finish the job \(for example, data directory and write-ahead log directory\). This option inhibits tidying-up and is thus useful for debugging.

Note that tablespace directories are not cleaned up either way.

`-N`  
`--no-sync`

By default, `pg_basebackup` will wait for all files to be written safely to disk. This option causes `pg_basebackup` to return without waiting, which is faster, but means that a subsequent operating system crash can leave the base backup corrupt. Generally, this option is useful for testing but should not be used when creating a production installation.

`-P`  
`--progress`

Enables progress reporting. Turning this on will deliver an approximate progress report during the backup. Since the database may change during the backup, this is only an approximation and may not end at exactly `100%`. In particular, when WAL log is included in the backup, the total amount of data cannot be estimated in advance, and in this case the estimated target size will increase once it passes the total estimate without WAL.

When this is enabled, the backup will start by enumerating the size of the entire database, and then go back and send the actual contents. This may make the backup take slightly longer, and in particular it will take longer before the first data is sent.

`-S` _`slotname`_  
`--slot=`_`slotname`_

This option can only be used together with `-X stream`. It causes the WAL streaming to use the specified replication slot. If the base backup is intended to be used as a streaming replication standby using replication slots, it should then use the same replication slot name in [primary\_slot\_name](https://www.postgresql.org/docs/12/runtime-config-replication.html#GUC-PRIMARY-SLOT-NAME). That way, it is ensured that the server does not remove any necessary WAL data in the time between the end of the base backup and the start of streaming replication.

The specified replication slot has to exist unless the option `-C` is also used.

If this option is not specified and the server supports temporary replication slots \(version 10 and later\), then a temporary replication slot is automatically used for WAL streaming.

`-v`  
`--verbose`

Enables verbose mode. Will output some extra steps during startup and shutdown, as well as show the exact file name that is currently being processed if progress reporting is also enabled.

`--no-slot`

This option prevents the creation of a temporary replication slot during the backup even if it's supported by the server.

Temporary replication slots are created by default if no slot name is given with the option `-S` when using log streaming.

The main purpose of this option is to allow taking a base backup when the server is out of free replication slots. Using replication slots is almost always preferred, because it prevents needed WAL from being removed by the server during the backup.

`--no-verify-checksums`

Disables verification of checksums, if they are enabled on the server the base backup is taken from.

By default, checksums are verified and checksum failures will result in a non-zero exit status. However, the base backup will not be removed in such a case, as if the `--no-clean` option had been used. Checksum verifications failures will also be reported in the [pg\_stat\_database](https://www.postgresql.org/docs/12/monitoring-stats.html#PG-STAT-DATABASE-VIEW) view.

The following command-line options control the database connection parameters.

`-d` _`connstr`_  
`--dbname=`_`connstr`_

Specifies parameters used to connect to the server, as a connection string. See [Section 33.1.1](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING) for more information.

The option is called `--dbname` for consistency with other client applications, but because pg\_basebackup doesn't connect to any particular database in the cluster, database name in the connection string will be ignored.

`-h` _`host`_  
`--host=`_`host`_

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket. The default is taken from the `PGHOST` environment variable, if set, else a Unix domain socket connection is attempted.

`-p` _`port`_  
`--port=`_`port`_

Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections. Defaults to the `PGPORT` environment variable, if set, or a compiled-in default.

`-s` _`interval`_  
`--status-interval=`_`interval`_

Specifies the number of seconds between status packets sent back to the server. This allows for easier monitoring of the progress from server. A value of zero disables the periodic status updates completely, although an update will still be sent when requested by the server, to avoid timeout disconnect. The default value is 10 seconds.

`-U` _`username`_  
`--username=`_`username`_

User name to connect as.

`-w`  
`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.

`-W`  
`--password`

Force pg\_basebackup to prompt for a password before connecting to a database.

This option is never essential, since pg\_basebackup will automatically prompt for a password if the server demands password authentication. However, pg\_basebackup will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.

Other options are also available:

`-V`  
`--version`

Print the pg\_basebackup version and exit.

`-?`  
`--help`

Show help about pg\_basebackup command line arguments, and exit.

### Environment

This utility, like most other PostgreSQL utilities, uses the environment variables supported by libpq \(see [Section 33.14](https://www.postgresql.org/docs/12/libpq-envars.html)\).

The environment variable `PG_COLOR` specifies whether to use color in diagnostics messages. Possible values are `always`, `auto`, `never`.

### Notes

At the beginning of the backup, a checkpoint needs to be written on the server the backup is taken from. Especially if the option `--checkpoint=fast` is not used, this can take some time during which pg\_basebackup will be appear to be idle.

The backup will include all files in the data directory and tablespaces, including the configuration files and any additional files placed in the directory by third parties, except certain temporary files managed by PostgreSQL. But only regular files and directories are copied, except that symbolic links used for tablespaces are preserved. Symbolic links pointing to certain directories known to PostgreSQL are copied as empty directories. Other symbolic links and special device files are skipped. See [Section 52.4](https://www.postgresql.org/docs/12/protocol-replication.html) for the precise details.

Tablespaces will in plain format by default be backed up to the same path they have on the server, unless the option `--tablespace-mapping` is used. Without this option, running a plain format base backup on the same host as the server will not work if tablespaces are in use, because the backup would have to be written to the same directory locations as the original tablespaces.

When tar format mode is used, it is the user's responsibility to unpack each tar file before starting the PostgreSQL server. If there are additional tablespaces, the tar files for them need to be unpacked in the correct locations. In this case the symbolic links for those tablespaces will be created by the server according to the contents of the `tablespace_map` file that is included in the `base.tar` file.

pg\_basebackup works with servers of the same or an older major version, down to 9.1. However, WAL streaming mode \(`-X stream`\) only works with server version 9.3 and later, and tar format mode \(`--format=tar`\) of the current version only works with server version 9.5 or later.

pg\_basebackup will preserve group permissions in both the `plain` and `tar` formats if group permissions are enabled on the source cluster.

### Examples

To create a base backup of the server at `mydbserver` and store it in the local directory `/usr/local/pgsql/data`:

```text
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
```

To create a backup of the local server with one compressed tar file for each tablespace, and store it in the directory `backup`, showing a progress report while running:

```text
$ pg_basebackup -D backup -Ft -z -P
```

To create a backup of a single-tablespace local database and compress this with bzip2:

```text
$ pg_basebackup -D - -Ft -X fetch | bzip2 > backup.tar.bz2
```

\(This command will fail if there are multiple tablespaces in the database.\)

To create a backup of a local database where the tablespace in `/opt/ts` is relocated to `./backup/ts`:

```text
$ pg_basebackup -D backup/data -T /opt/ts=$(pwd)/backup/ts
```

### See Also

[pg\_dump](pg_dump.md)

