# 52.4. Streaming Replication Protocol

To initiate streaming replication, the frontend sends the `replication` parameter in the startup message. A Boolean value of `true` \(or `on`, `yes`, `1`\) tells the backend to go into physical replication walsender mode, wherein a small set of replication commands, shown below, can be issued instead of SQL statements.

Passing `database` as the value for the `replication` parameter instructs the backend to go into logical replication walsender mode, connecting to the database specified in the `dbname` parameter. In logical replication walsender mode, the replication commands shown below as well as normal SQL commands can be issued.

In either physical replication or logical replication walsender mode, only the simple query protocol can be used.

For the purpose of testing replication commands, you can make a replication connection via psql or any other libpq-using tool with a connection string including the `replication` option, e.g.:

```text
psql "dbname=postgres replication=database" -c "IDENTIFY_SYSTEM;"
```

However, it is often more useful to use [pg\_receivewal](https://www.postgresql.org/docs/13/app-pgreceivewal.html) \(for physical replication\) or [pg\_recvlogical](https://www.postgresql.org/docs/13/app-pgrecvlogical.html) \(for logical replication\).

Replication commands are logged in the server log when [log\_replication\_commands](https://www.postgresql.org/docs/13/runtime-config-logging.html#GUC-LOG-REPLICATION-COMMANDS) is enabled.

The commands accepted in replication mode are:

`IDENTIFY_SYSTEM`

Requests the server to identify itself. Server replies with a result set of a single row, containing four fields:

`systemid` \(`text`\)

The unique system identifier identifying the cluster. This can be used to check that the base backup used to initialize the standby came from the same cluster.

`timeline` \(`int4`\)

Current timeline ID. Also useful to check that the standby is consistent with the master.

`xlogpos` \(`text`\)

Current WAL flush location. Useful to get a known location in the write-ahead log where streaming can start.

`dbname` \(`text`\)

Database connected to or null.

`SHOW` _`name`_

Requests the server to send the current setting of a run-time parameter. This is similar to the SQL command [SHOW](https://www.postgresql.org/docs/13/sql-show.html).

_`name`_

The name of a run-time parameter. Available parameters are documented in [Chapter 19](https://www.postgresql.org/docs/13/runtime-config.html).

`TIMELINE_HISTORY` _`tli`_

Requests the server to send over the timeline history file for timeline _`tli`_. Server replies with a result set of a single row, containing two fields:

`filename` \(`text`\)

File name of the timeline history file, e.g., `00000002.history`.

`content` \(`bytea`\)

Contents of the timeline history file.

`CREATE_REPLICATION_SLOT` _`slot_name`_ \[ `TEMPORARY` \] { `PHYSICAL` \[ `RESERVE_WAL` \] \| `LOGICAL` _`output_plugin`_ \[ `EXPORT_SNAPSHOT` \| `NOEXPORT_SNAPSHOT` \| `USE_SNAPSHOT` \] }

Create a physical or logical replication slot. See [Section 26.2.6](https://www.postgresql.org/docs/13/warm-standby.html#STREAMING-REPLICATION-SLOTS) for more about replication slots.

_`slot_name`_

The name of the slot to create. Must be a valid replication slot name \(see [Section 26.2.6.1](https://www.postgresql.org/docs/13/warm-standby.html#STREAMING-REPLICATION-SLOTS-MANIPULATION)\).

_`output_plugin`_

The name of the output plugin used for logical decoding \(see [Section 48.6](https://www.postgresql.org/docs/13/logicaldecoding-output-plugin.html)\).

`TEMPORARY`

Specify that this replication slot is a temporary one. Temporary slots are not saved to disk and are automatically dropped on error or when the session has finished.

`RESERVE_WAL`

Specify that this physical replication slot reserves WAL immediately. Otherwise, WAL is only reserved upon connection from a streaming replication client.

`EXPORT_SNAPSHOT`  
`NOEXPORT_SNAPSHOT`  
`USE_SNAPSHOT`

Decides what to do with the snapshot created during logical slot initialization. `EXPORT_SNAPSHOT`, which is the default, will export the snapshot for use in other sessions. This option can't be used inside a transaction. `USE_SNAPSHOT` will use the snapshot for the current transaction executing the command. This option must be used in a transaction, and `CREATE_REPLICATION_SLOT` must be the first command run in that transaction. Finally, `NOEXPORT_SNAPSHOT` will just use the snapshot for logical decoding as normal but won't do anything else with it.

In response to this command, the server will send a one-row result set containing the following fields:

`slot_name` \(`text`\)

The name of the newly-created replication slot.

`consistent_point` \(`text`\)

The WAL location at which the slot became consistent. This is the earliest location from which streaming can start on this replication slot.

`snapshot_name` \(`text`\)

The identifier of the snapshot exported by the command. The snapshot is valid until a new command is executed on this connection or the replication connection is closed. Null if the created slot is physical.

`output_plugin` \(`text`\)

The name of the output plugin used by the newly-created replication slot. Null if the created slot is physical.

`START_REPLICATION` \[ `SLOT` _`slot_name`_ \] \[ `PHYSICAL` \] _`XXX/XXX`_ \[ `TIMELINE` _`tli`_ \]

Instructs server to start streaming WAL, starting at WAL location _`XXX/XXX`_. If `TIMELINE` option is specified, streaming starts on timeline _`tli`_; otherwise, the server's current timeline is selected. The server can reply with an error, for example if the requested section of WAL has already been recycled. On success, server responds with a CopyBothResponse message, and then starts to stream WAL to the frontend.

If a slot's name is provided via _`slot_name`_, it will be updated as replication progresses so that the server knows which WAL segments, and if `hot_standby_feedback` is on which transactions, are still needed by the standby.

If the client requests a timeline that's not the latest but is part of the history of the server, the server will stream all the WAL on that timeline starting from the requested start point up to the point where the server switched to another timeline. If the client requests streaming at exactly the end of an old timeline, the server responds immediately with CommandComplete without entering COPY mode.

After streaming all the WAL on a timeline that is not the latest one, the server will end streaming by exiting the COPY mode. When the client acknowledges this by also exiting COPY mode, the server sends a result set with one row and two columns, indicating the next timeline in this server's history. The first column is the next timeline's ID \(type `int8`\), and the second column is the WAL location where the switch happened \(type `text`\). Usually, the switch position is the end of the WAL that was streamed, but there are corner cases where the server can send some WAL from the old timeline that it has not itself replayed before promoting. Finally, the server sends two CommandComplete messages \(one that ends the CopyData and the other ends the `START_REPLICATION` itself\), and is ready to accept a new command.

WAL data is sent as a series of CopyData messages. \(This allows other information to be intermixed; in particular the server can send an ErrorResponse message if it encounters a failure after beginning to stream.\) The payload of each CopyData message from server to the client contains a message of one of the following formats:

XLogData \(B\)

Byte1\('w'\)

Identifies the message as WAL data.

Int64

The starting point of the WAL data in this message.

Int64

The current end of WAL on the server.

Int64

The server's system clock at the time of transmission, as microseconds since midnight on 2000-01-01.

Byte_`n`_

A section of the WAL data stream.

A single WAL record is never split across two XLogData messages. When a WAL record crosses a WAL page boundary, and is therefore already split using continuation records, it can be split at the page boundary. In other words, the first main WAL record and its continuation records can be sent in different XLogData messages.

Primary keepalive message \(B\)

Byte1\('k'\)

Identifies the message as a sender keepalive.

Int64

The current end of WAL on the server.

Int64

The server's system clock at the time of transmission, as microseconds since midnight on 2000-01-01.

Byte1

1 means that the client should reply to this message as soon as possible, to avoid a timeout disconnect. 0 otherwise.

The receiving process can send replies back to the sender at any time, using one of the following message formats \(also in the payload of a CopyData message\):

Standby status update \(F\)

Byte1\('r'\)

Identifies the message as a receiver status update.

Int64

The location of the last WAL byte + 1 received and written to disk in the standby.

Int64

The location of the last WAL byte + 1 flushed to disk in the standby.Int64

The location of the last WAL byte + 1 applied in the standby.Int64

The client's system clock at the time of transmission, as microseconds since midnight on 2000-01-01.Byte1

If 1, the client requests the server to reply to this message immediately. This can be used to ping the server, to test if the connection is still healthy.Hot Standby feedback message \(F\)Byte1\('h'\)

Identifies the message as a Hot Standby feedback message.Int64

The client's system clock at the time of transmission, as microseconds since midnight on 2000-01-01.Int32

The standby's current global xmin, excluding the catalog\_xmin from any replication slots. If both this value and the following catalog\_xmin are 0 this is treated as a notification that Hot Standby feedback will no longer be sent on this connection. Later non-zero messages may reinitiate the feedback mechanism.Int32

The epoch of the global xmin xid on the standby.Int32

The lowest catalog\_xmin of any replication slots on the standby. Set to 0 if no catalog\_xmin exists on the standby or if hot standby feedback is being disabled.Int32

The epoch of the catalog\_xmin xid on the standby.`START_REPLICATION` `SLOT` _`slot_name`_ `LOGICAL` _`XXX/XXX`_ \[ \( _`option_name`_ \[ _`option_value`_ \] \[, ...\] \) \]

Instructs server to start streaming WAL for logical replication, starting at WAL location _`XXX/XXX`_. The server can reply with an error, for example if the requested section of WAL has already been recycled. On success, server responds with a CopyBothResponse message, and then starts to stream WAL to the frontend.

The messages inside the CopyBothResponse messages are of the same format documented for `START_REPLICATION ... PHYSICAL`, including two CommandComplete messages.

The output plugin associated with the selected slot is used to process the output for streaming.`SLOT` _`slot_name`_

The name of the slot to stream changes from. This parameter is required, and must correspond to an existing logical replication slot created with `CREATE_REPLICATION_SLOT` in `LOGICAL` mode._`XXX/XXX`_

The WAL location to begin streaming at._`option_name`_

The name of an option passed to the slot's logical decoding plugin._`option_value`_

Optional value, in the form of a string constant, associated with the specified option.`DROP_REPLICATION_SLOT` _`slot_name`_ \[ `WAIT` \]

Drops a replication slot, freeing any reserved server-side resources. If the slot is a logical slot that was created in a database other than the database the walsender is connected to, this command fails._`slot_name`_

The name of the slot to drop.`WAIT`

This option causes the command to wait if the slot is active until it becomes inactive, instead of the default behavior of raising an error.`BASE_BACKUP` \[ `LABEL` _`'label'`_ \] \[ `PROGRESS` \] \[ `FAST` \] \[ `WAL` \] \[ `NOWAIT` \] \[ `MAX_RATE` _`rate`_ \] \[ `TABLESPACE_MAP` \] \[ `NOVERIFY_CHECKSUMS` \] \[ `MANIFEST` _`manifest_option`_ \] \[ `MANIFEST_CHECKSUMS` _`checksum_algorithm`_ \]

Instructs the server to start streaming a base backup. The system will automatically be put in backup mode before the backup is started, and taken out of it when the backup is complete. The following options are accepted:`LABEL` _`'label'`_

Sets the label of the backup. If none is specified, a backup label of `base backup` will be used. The quoting rules for the label are the same as a standard SQL string with [standard\_conforming\_strings](https://www.postgresql.org/docs/13/runtime-config-compatible.html#GUC-STANDARD-CONFORMING-STRINGS) turned on.`PROGRESS`

Request information required to generate a progress report. This will send back an approximate size in the header of each tablespace, which can be used to calculate how far along the stream is done. This is calculated by enumerating all the file sizes once before the transfer is even started, and might as such have a negative impact on the performance. In particular, it might take longer before the first data is streamed. Since the database files can change during the backup, the size is only approximate and might both grow and shrink between the time of approximation and the sending of the actual files.`FAST`

Request a fast checkpoint.`WAL`

Include the necessary WAL segments in the backup. This will include all the files between start and stop backup in the `pg_wal` directory of the base directory tar file.`NOWAIT`

By default, the backup will wait until the last required WAL segment has been archived, or emit a warning if log archiving is not enabled. Specifying `NOWAIT` disables both the waiting and the warning, leaving the client responsible for ensuring the required log is available.`MAX_RATE` _`rate`_

Limit \(throttle\) the maximum amount of data transferred from server to client per unit of time. The expected unit is kilobytes per second. If this option is specified, the value must either be equal to zero or it must fall within the range from 32 kB through 1 GB \(inclusive\). If zero is passed or the option is not specified, no restriction is imposed on the transfer.`TABLESPACE_MAP`

Include information about symbolic links present in the directory `pg_tblspc` in a file named `tablespace_map`. The tablespace map file includes each symbolic link name as it exists in the directory `pg_tblspc/` and the full path of that symbolic link.`NOVERIFY_CHECKSUMS`

By default, checksums are verified during a base backup if they are enabled. Specifying `NOVERIFY_CHECKSUMS` disables this verification.`MANIFEST` _`manifest_option`_

When this option is specified with a value of `yes` or `force-encode`, a backup manifest is created and sent along with the backup. The manifest is a list of every file present in the backup with the exception of any WAL files that may be included. It also stores the size, last modification time, and optionally a checksum for each file. A value of `force-encode` forces all filenames to be hex-encoded; otherwise, this type of encoding is performed only for files whose names are non-UTF8 octet sequences. `force-encode` is intended primarily for testing purposes, to be sure that clients which read the backup manifest can handle this case. For compatibility with previous releases, the default is `MANIFEST 'no'`.`MANIFEST_CHECKSUMS` _`checksum_algorithm`_

Specifies the checksum algorithm that should be applied to each file included in the backup manifest. Currently, the available algorithms are `NONE`, `CRC32C`, `SHA224`, `SHA256`, `SHA384`, and `SHA512`. The default is `CRC32C`.

When the backup is started, the server will first send two ordinary result sets, followed by one or more CopyResponse results.

The first ordinary result set contains the starting position of the backup, in a single row with two columns. The first column contains the start position given in XLogRecPtr format, and the second column contains the corresponding timeline ID.

The second ordinary result set has one row for each tablespace. The fields in this row are:`spcoid` \(`oid`\)

The OID of the tablespace, or null if it's the base directory.`spclocation` \(`text`\)

The full path of the tablespace directory, or null if it's the base directory.`size` \(`int8`\)

The approximate size of the tablespace, in kilobytes \(1024 bytes\), if progress report has been requested; otherwise it's null.

After the second regular result set, one or more CopyResponse results will be sent, one for the main data directory and one for each additional tablespace other than `pg_default` and `pg_global`. The data in the CopyResponse results will be a tar format \(following the “ustar interchange format” specified in the POSIX 1003.1-2008 standard\) dump of the tablespace contents, except that the two trailing blocks of zeroes specified in the standard are omitted. After the tar data is complete, and if a backup manifest was requested, another CopyResponse result is sent, containing the manifest data for the current base backup. In any case, a final ordinary result set will be sent, containing the WAL end position of the backup, in the same format as the start position.

The tar archive for the data directory and each tablespace will contain all files in the directories, regardless of whether they are PostgreSQL files or other files added to the same directory. The only excluded files are:

* `postmaster.pid`
* `postmaster.opts`
* `pg_internal.init` \(found in multiple directories\)
* Various temporary files and directories created during the operation of the PostgreSQL server, such as any file or directory beginning with `pgsql_tmp` and temporary relations.
* Unlogged relations, except for the init fork which is required to recreate the \(empty\) unlogged relation on recovery.
* `pg_wal`, including subdirectories. If the backup is run with WAL files included, a synthesized version of `pg_wal` will be included, but it will only contain the files necessary for the backup to work, not the rest of the contents.
* `pg_dynshmem`, `pg_notify`, `pg_replslot`, `pg_serial`, `pg_snapshots`, `pg_stat_tmp`, and `pg_subtrans` are copied as empty directories \(even if they are symbolic links\).
* Files other than regular files and directories, such as symbolic links \(other than for the directories listed above\) and special device files, are skipped. \(Symbolic links in `pg_tblspc` are maintained.\)

Owner, group, and file mode are set if the underlying file system on the server supports it.

