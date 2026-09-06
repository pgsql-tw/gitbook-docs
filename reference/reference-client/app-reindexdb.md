<a id="id-1.9.4.22.1"></a>

## reindexdb

reindexdb — reindex a PostgreSQL database

## Synopsis

<a id="id-1.9.4.22.4.1"></a>

`reindexdb` [*`connection-option`*...] [*`option`*...]
[
`-S` | `--schema`
*`schema`*
]
...
[
`-t` | `--table`
*`table`*
]
...
[
`-i` | `--index`
*`index`*
]
...
[
`-s` | `--system`
]
[
*`dbname`* | `-a` | `--all`
]

<a id="id-1.9.4.22.5"></a>

## Description

reindexdb is a utility for rebuilding indexes
in a PostgreSQL database.

reindexdb is a wrapper around the SQL
command [`REINDEX`](../sql-commands/sql-reindex.md).
There is no effective difference between reindexing databases via
this utility and via other methods for accessing the server.

<a id="id-1.9.4.22.6"></a>

## Options

reindexdb accepts the following command-line arguments:

`-a`<br>`--all`
:   Reindex all databases.

`--concurrently`
:   Use the `CONCURRENTLY` option. See
    [REINDEX](../sql-commands/sql-reindex.md), where all the caveats of this option
    are explained in detail.

`[-d] dbname`<br>`[--dbname=]dbname`
:   Specifies the name of the database to be reindexed,
    when `-a`/`--all` is not used.
    If this is not specified, the database name is read
    from the environment variable `PGDATABASE`. If
    that is not set, the user name specified for the connection is
    used. The *`dbname`* can be a [connection string](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNSTRING). If so,
    connection string parameters will override any conflicting command
    line options.

`-e`<br>`--echo`
:   Echo the commands that reindexdb generates
    and sends to the server.

`-i index`<br>`--index=index`
:   Recreate *`index`* only.
    Multiple indexes can be recreated by writing multiple
    `-i` switches.

`-j njobs`<br>`--jobs=njobs`
:   Execute the reindex commands in parallel by running
    *`njobs`*
    commands simultaneously. This option may reduce the processing time
    but it also increases the load on the database server.

    reindexdb will open
    *`njobs`* connections to the
    database, so make sure your [max_connections](../../server-administration/runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS)
    setting is high enough to accommodate all connections.

    Note that this option is incompatible with the `--system` option.

`-q`<br>`--quiet`
:   Do not display progress messages.

`-s`<br>`--system`
:   Reindex database's system catalogs only.

`-S schema`<br>`--schema=schema`
:   Reindex *`schema`* only.
    Multiple schemas can be reindexed by writing multiple
    `-S` switches.

`-t table`<br>`--table=table`
:   Reindex *`table`* only.
    Multiple tables can be reindexed by writing multiple
    `-t` switches.

`--tablespace=tablespace`
:   Specifies the tablespace where indexes are rebuilt. (This name is
    processed as a double-quoted identifier.)

`-v`<br>`--verbose`
:   Print detailed information during processing.

`-V`<br>`--version`
:   Print the reindexdb version and exit.

`-?`<br>`--help`
:   Show help about reindexdb command line
    arguments, and exit.

reindexdb also accepts
the following command-line arguments for connection parameters:

`-h host`<br>`--host=host`
:   Specifies the host name of the machine on which the server is
    running. If the value begins with a slash, it is used as the
    directory for the Unix domain socket.

`-p port`<br>`--port=port`
:   Specifies the TCP port or local Unix domain socket file
    extension on which the server
    is listening for connections.

`-U username`<br>`--username=username`
:   User name to connect as.

`-w`<br>`--no-password`
:   Never issue a password prompt. If the server requires
    password authentication and a password is not available by
    other means such as a `.pgpass` file, the
    connection attempt will fail. This option can be useful in
    batch jobs and scripts where no user is present to enter a
    password.

`-W`<br>`--password`
:   Force reindexdb to prompt for a
    password before connecting to a database.

    This option is never essential, since
    reindexdb will automatically prompt
    for a password if the server demands password authentication.
    However, reindexdb will waste a
    connection attempt finding out that the server wants a password.
    In some cases it is worth typing `-W` to avoid the extra
    connection attempt.

`--maintenance-db=dbname`
:   When the `-a`/`--all` is used, connect
    to this database to gather the list of databases to reindex.
    If not specified, the `postgres` database will be used,
    or if that does not exist, `template1` will be used.
    This can be a [connection
    string](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNSTRING). If so, connection string parameters will override any
    conflicting command line options. Also, connection string parameters
    other than the database name itself will be re-used when connecting
    to other databases.

<a id="id-1.9.4.22.7"></a>

## Environment

`PGDATABASE`<br>`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   Default connection parameters

`PG_COLOR`
:   Specifies whether to use color in diagnostic messages. Possible values
    are `always`, `auto` and
    `never`.

This utility, like most other PostgreSQL utilities,
also uses the environment variables supported by libpq
(see [Section 32.15](../../client-interfaces/libpq/libpq-envars.md)).

<a id="id-1.9.4.22.8"></a>

## Diagnostics

In case of difficulty, see [REINDEX](../sql-commands/sql-reindex.md)
and [psql](app-psql.md) for
discussions of potential problems and error messages.
The database server must be running at the
targeted host. Also, any default connection settings and environment
variables used by the libpq front-end
library will apply.

<a id="id-1.9.4.22.9"></a>

## Examples

To reindex the database `test`:

```

$ reindexdb test
```

To reindex the table `foo` and the index
`bar` in a database named `abcd`:

```

$ reindexdb --table=foo --index=bar abcd
```

<a id="id-1.9.4.22.10"></a>

## See Also

[REINDEX](../sql-commands/sql-reindex.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-reindexdb.html)（英文原文，待翻譯）
