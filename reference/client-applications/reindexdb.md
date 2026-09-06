<a id="APP-REINDEXDB"></a><a id="id-1.9.4.21.1"></a>

# reindexdb

reindexdb — reindex a PostgreSQL database

## Synopsis

<a id="id-1.9.4.21.4.1"></a>

`reindexdb` [<em class="replaceable"><code>connection-option</code></em>...] [<em class="replaceable"><code>option</code></em>...] [ `-S` | `--schema` <em class="replaceable"><code>schema</code></em> ] ... [ `-t` | `--table` <em class="replaceable"><code>table</code></em> ] ... [ `-i` | `--index` <em class="replaceable"><code>index</code></em> ] ... [<em class="replaceable"><code>dbname</code></em>]

<a id="id-1.9.4.21.4.2"></a>

`reindexdb` [<em class="replaceable"><code>connection-option</code></em>...] [<em class="replaceable"><code>option</code></em>...] `-a` | `--all`

<a id="id-1.9.4.21.4.3"></a>

`reindexdb` [<em class="replaceable"><code>connection-option</code></em>...] [<em class="replaceable"><code>option</code></em>...] `-s` | `--system` [<em class="replaceable"><code>dbname</code></em>]

<a id="id-1.9.4.21.5"></a>

## Description

reindexdb is a utility for rebuilding indexes in a PostgreSQL database.

reindexdb is a wrapper around the SQL command [`REINDEX`](../sql-commands/reindex.md). There is no effective difference between reindexing databases via this utility and via other methods for accessing the server.

<a id="id-1.9.4.21.6"></a>

## Options

reindexdb accepts the following command-line arguments:

`-a`<br>`--all`

Reindex all databases.

`--concurrently`

Use the `CONCURRENTLY` option. See [REINDEX](../sql-commands/reindex.md), where all the caveats of this option are explained in detail.

<code class="option">&#91;<span class="optional">-d</span>&#93; <em class="replaceable"><code>dbname</code></em></code><br><code class="option">&#91;<span class="optional">--dbname=</span>&#93;<em class="replaceable"><code>dbname</code></em></code>

Specifies the name of the database to be reindexed, when `-a`/`--all` is not used. If this is not specified, the database name is read from the environment variable `PGDATABASE`. If that is not set, the user name specified for the connection is used. The <em class="replaceable"><code>dbname</code></em> can be a [connection string](https://www.postgresql.org/docs/15/libpq-connect.html#LIBPQ-CONNSTRING). If so, connection string parameters will override any conflicting command line options.

`-e`<br>`--echo`

Echo the commands that reindexdb generates and sends to the server.

<code class="option">-i <em class="replaceable"><code>index</code></em></code><br><code class="option">--index=<em class="replaceable"><code>index</code></em></code>

Recreate <em class="replaceable"><code>index</code></em> only. Multiple indexes can be recreated by writing multiple `-i` switches.

<code class="option">-j <em class="replaceable"><code>njobs</code></em></code><br><code class="option">--jobs=<em class="replaceable"><code>njobs</code></em></code>

Execute the reindex commands in parallel by running <em class="replaceable"><code>njobs</code></em> commands simultaneously. This option may reduce the processing time but it also increases the load on the database server.

reindexdb will open <em class="replaceable"><code>njobs</code></em> connections to the database, so make sure your [max_connections](https://www.postgresql.org/docs/15/runtime-config-connection.html#GUC-MAX-CONNECTIONS) setting is high enough to accommodate all connections.

Note that this option is incompatible with the `--index` and `--system` options.

`-q`<br>`--quiet`

Do not display progress messages.

`-s`<br>`--system`

Reindex database's system catalogs only.

<code class="option">-S <em class="replaceable"><code>schema</code></em></code><br><code class="option">--schema=<em class="replaceable"><code>schema</code></em></code>

Reindex <em class="replaceable"><code>schema</code></em> only. Multiple schemas can be reindexed by writing multiple `-S` switches.

<code class="option">-t <em class="replaceable"><code>table</code></em></code><br><code class="option">--table=<em class="replaceable"><code>table</code></em></code>

Reindex <em class="replaceable"><code>table</code></em> only. Multiple tables can be reindexed by writing multiple `-t` switches.

<code class="option">--tablespace=<em class="replaceable"><code>tablespace</code></em></code>

Specifies the tablespace where indexes are rebuilt. (This name is processed as a double-quoted identifier.)

`-v`<br>`--verbose`

Print detailed information during processing.

`-V`<br>`--version`

Print the reindexdb version and exit.

`-?`<br>`--help`

Show help about reindexdb command line arguments, and exit.

reindexdb also accepts the following command-line arguments for connection parameters:

<code class="option">-h <em class="replaceable"><code>host</code></em></code><br><code class="option">--host=<em class="replaceable"><code>host</code></em></code>

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket.

<code class="option">-p <em class="replaceable"><code>port</code></em></code><br><code class="option">--port=<em class="replaceable"><code>port</code></em></code>

Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections.

<code class="option">-U <em class="replaceable"><code>username</code></em></code><br><code class="option">--username=<em class="replaceable"><code>username</code></em></code>

User name to connect as.

`-w`<br>`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.

`-W`<br>`--password`

Force reindexdb to prompt for a password before connecting to a database.

This option is never essential, since reindexdb will automatically prompt for a password if the server demands password authentication. However, reindexdb will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.

<code class="option">--maintenance-db=<em class="replaceable"><code>dbname</code></em></code>

When the `-a`/`--all` is used, connect to this database to gather the list of databases to reindex. If not specified, the `postgres` database will be used, or if that does not exist, `template1` will be used. This can be a [connection string](https://www.postgresql.org/docs/15/libpq-connect.html#LIBPQ-CONNSTRING). If so, connection string parameters will override any conflicting command line options. Also, connection string parameters other than the database name itself will be re-used when connecting to other databases.

<a id="id-1.9.4.21.7"></a>

## Environment

`PGDATABASE`<br>`PGHOST`<br>`PGPORT`<br>`PGUSER`

Default connection parameters

`PG_COLOR`

Specifies whether to use color in diagnostic messages. Possible values are `always`, `auto` and `never`.

This utility, like most other PostgreSQL utilities, also uses the environment variables supported by libpq (see [Section 34.15](../../client-interfaces/libpq-c-library/environment-variables.md)).

<a id="id-1.9.4.21.8"></a>

## Diagnostics

In case of difficulty, see [REINDEX](../sql-commands/reindex.md) and [psql](psql.md) for discussions of potential problems and error messages. The database server must be running at the targeted host. Also, any default connection settings and environment variables used by the libpq front-end library will apply.

<a id="id-1.9.4.21.9"></a>

## Notes

reindexdb might need to connect several times to the PostgreSQL server, asking for a password each time. It is convenient to have a `~/.pgpass` file in such cases. See [Section 34.16](../../client-interfaces/libpq-c-library/libpq-pgpass.md) for more information.

<a id="id-1.9.4.21.10"></a>

## Examples

To reindex the database `test`:

```

$ reindexdb test
```

To reindex the table `foo` and the index `bar` in a database named `abcd`:

```

$ reindexdb --table=foo --index=bar abcd
```

<a id="id-1.9.4.21.11"></a>

## See Also

[REINDEX](../sql-commands/reindex.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/app-reindexdb.html)（英文原文，待翻譯）
