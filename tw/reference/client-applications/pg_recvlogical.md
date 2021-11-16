# pg\_recvlogical

pg\_recvlogical — control PostgreSQL logical decoding streams

### Synopsis

`pg_recvlogical` \[_`option`_...]

### Description

`pg_recvlogical` controls logical decoding replication slots and streams data from such replication slots.

It creates a replication-mode connection, so it is subject to the same constraints as [pg\_receivewal](https://www.postgresql.org/docs/13/app-pgreceivewal.html), plus those for logical replication (see [Chapter 48](https://www.postgresql.org/docs/13/logicaldecoding.html)).

`pg_recvlogical` has no equivalent to the logical decoding SQL interface's peek and get modes. It sends replay confirmations for data lazily as it receives it and on clean exit. To examine pending data on a slot without consuming it, use [`pg_logical_slot_peek_changes`](https://www.postgresql.org/docs/13/functions-admin.html#FUNCTIONS-REPLICATION).

### Options

At least one of the following options must be specified to select an action:

`--create-slot`

Create a new logical replication slot with the name specified by `--slot`, using the output plugin specified by `--plugin`, for the database specified by `--dbname`.

`--drop-slot`

Drop the replication slot with the name specified by `--slot`, then exit.

`--start`

Begin streaming changes from the logical replication slot specified by `--slot`, continuing until terminated by a signal. If the server side change stream ends with a server shutdown or disconnect, retry in a loop unless `--no-loop` is specified.

The stream format is determined by the output plugin specified when the slot was created.

The connection must be to the same database used to create the slot.

`--create-slot` and `--start` can be specified together. `--drop-slot` cannot be combined with another action.

The following command-line options control the location and format of the output and other replication behavior:

`-E `_`lsn`_\
`--endpos=`_`lsn`_

In `--start` mode, automatically stop replication and exit with normal exit status 0 when receiving reaches the specified LSN. If specified when not in `--start` mode, an error is raised.

If there's a record with LSN exactly equal to _`lsn`_, the record will be output.

The `--endpos` option is not aware of transaction boundaries and may truncate output partway through a transaction. Any partially output transaction will not be consumed and will be replayed again when the slot is next read from. Individual messages are never truncated.

`-f `_`filename`_\
`--file=`_`filename`_

Write received and decoded transaction data into this file. Use `-` for stdout.

`-F `_`interval_seconds`_\
`--fsync-interval=`_`interval_seconds`_

Specifies how often pg\_recvlogical should issue `fsync()` calls to ensure the output file is safely flushed to disk.

The server will occasionally request the client to perform a flush and report the flush position to the server. This setting is in addition to that, to perform flushes more frequently.

Specifying an interval of `0` disables issuing `fsync()` calls altogether, while still reporting progress to the server. In this case, data could be lost in the event of a crash.

`-I `_`lsn`_\
`--startpos=`_`lsn`_

In `--start` mode, start replication from the given LSN. For details on the effect of this, see the documentation in [Chapter 48](https://www.postgresql.org/docs/13/logicaldecoding.html) and [Section 52.4](https://www.postgresql.org/docs/13/protocol-replication.html). Ignored in other modes.

`--if-not-exists`

Do not error out when `--create-slot` is specified and a slot with the specified name already exists.

`-n`\
`--no-loop`

When the connection to the server is lost, do not retry in a loop, just exit.

`-o `_`name`_\[=_`value`_]\
`--option=`_`name`_\[=_`value`_]

Pass the option _`name`_ to the output plugin with, if specified, the option value _`value`_. Which options exist and their effects depends on the used output plugin.

`-P `_`plugin`_\
`--plugin=`_`plugin`_

When creating a slot, use the specified logical decoding output plugin. See [Chapter 48](https://www.postgresql.org/docs/13/logicaldecoding.html). This option has no effect if the slot already exists.

`-s `_`interval_seconds`_\
`--status-interval=`_`interval_seconds`_

This option has the same effect as the option of the same name in [pg\_receivewal](https://www.postgresql.org/docs/13/app-pgreceivewal.html). See the description there.

`-S `_`slot_name`_\
`--slot=`_`slot_name`_

In `--start` mode, use the existing logical replication slot named _`slot_name`_. In `--create-slot` mode, create the slot with this name. In `--drop-slot` mode, delete the slot with this name.

`-v`\
`--verbose`

Enables verbose mode.

The following command-line options control the database connection parameters.

`-d `_`dbname`_\
`--dbname=`_`dbname`_

The database to connect to. See the description of the actions for what this means in detail. The _`dbname`_ can be a [connection string](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-CONNSTRING). If so, connection string parameters will override any conflicting command line options. Defaults to the user name.

`-h `_`hostname-or-ip`_\
`--host=`_`hostname-or-ip`_

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket. The default is taken from the `PGHOST` environment variable, if set, else a Unix domain socket connection is attempted.

`-p `_`port`_\
`--port=`_`port`_

Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections. Defaults to the `PGPORT` environment variable, if set, or a compiled-in default.

`-U `_`user`_\
`--username=`_`user`_

User name to connect as. Defaults to current operating system user name.

`-w`\
`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.

`-W`\
`--password`

Force pg\_recvlogical to prompt for a password before connecting to a database.

This option is never essential, since pg\_recvlogical will automatically prompt for a password if the server demands password authentication. However, pg\_recvlogical will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.

The following additional options are available:

`-V`\
`--version`

Print the pg\_recvlogical version and exit.

`-?`\
`--help`

Show help about pg\_recvlogical command line arguments, and exit.

### Environment

This utility, like most other PostgreSQL utilities, uses the environment variables supported by libpq (see [Section 33.14](https://www.postgresql.org/docs/13/libpq-envars.html)).

The environment variable `PG_COLOR` specifies whether to use color in diagnostic messages. Possible values are `always`, `auto` and `never`.

### Notes

pg\_recvlogical will preserve group permissions on the received WAL files if group permissions are enabled on the source cluster.

### Examples

See [Section 48.1](https://www.postgresql.org/docs/13/logicaldecoding-example.html) for an example.

### See Also

[pg\_receivewal](https://www.postgresql.org/docs/13/app-pgreceivewal.html)
