<a id="APP-CLUSTERDB"></a><a id="id-1.9.4.3.1"></a>

# clusterdb

clusterdb — cluster a PostgreSQL database

## Synopsis

<a id="id-1.9.4.3.4.1"></a>

`clusterdb` [<em class="replaceable"><code>connection-option</code></em>...] [ `--verbose` | `-v` ] [ `--table` | `-t` <em class="replaceable"><code>table</code></em> ] ... [<em class="replaceable"><code>dbname</code></em>]

<a id="id-1.9.4.3.4.2"></a>

`clusterdb` [<em class="replaceable"><code>connection-option</code></em>...] [ `--verbose` | `-v` ] `--all` | `-a`

<a id="id-1.9.4.3.5"></a>

## Description

clusterdb is a utility for reclustering tables in a PostgreSQL database. It finds tables that have previously been clustered, and clusters them again on the same index that was last used. Tables that have never been clustered are not affected.

clusterdb is a wrapper around the SQL command [CLUSTER](../sql-commands/cluster.md). There is no effective difference between clustering databases via this utility and via other methods for accessing the server.

<a id="id-1.9.4.3.6"></a>

## Options

clusterdb accepts the following command-line arguments:

`-a`<br>`--all`

Cluster all databases.

<code class="option">&#91;<span class="optional">-d</span>&#93; <em class="replaceable"><code>dbname</code></em></code><br><code class="option">&#91;<span class="optional">--dbname=</span>&#93;<em class="replaceable"><code>dbname</code></em></code>

Specifies the name of the database to be clustered, when `-a`/`--all` is not used. If this is not specified, the database name is read from the environment variable `PGDATABASE`. If that is not set, the user name specified for the connection is used. The <em class="replaceable"><code>dbname</code></em> can be a [connection string](../../client-interfaces/libpq-c-library/database-connection-control-functions.md#LIBPQ-CONNSTRING). If so, connection string parameters will override any conflicting command line options.

`-e`<br>`--echo`

Echo the commands that clusterdb generates and sends to the server.

`-q`<br>`--quiet`

Do not display progress messages.

<code class="option">-t <em class="replaceable"><code>table</code></em></code><br><code class="option">--table=<em class="replaceable"><code>table</code></em></code>

Cluster <em class="replaceable"><code>table</code></em> only. Multiple tables can be clustered by writing multiple `-t` switches.

`-v`<br>`--verbose`

Print detailed information during processing.

`-V`<br>`--version`

Print the clusterdb version and exit.

`-?`<br>`--help`

Show help about clusterdb command line arguments, and exit.

clusterdb also accepts the following command-line arguments for connection parameters:

<code class="option">-h <em class="replaceable"><code>host</code></em></code><br><code class="option">--host=<em class="replaceable"><code>host</code></em></code>

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket.

<code class="option">-p <em class="replaceable"><code>port</code></em></code><br><code class="option">--port=<em class="replaceable"><code>port</code></em></code>

Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections.

<code class="option">-U <em class="replaceable"><code>username</code></em></code><br><code class="option">--username=<em class="replaceable"><code>username</code></em></code>

User name to connect as.

`-w`<br>`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.

`-W`<br>`--password`

Force clusterdb to prompt for a password before connecting to a database.

This option is never essential, since clusterdb will automatically prompt for a password if the server demands password authentication. However, clusterdb will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.

<code class="option">--maintenance-db=<em class="replaceable"><code>dbname</code></em></code>

When the `-a`/`--all` is used, connect to this database to gather the list of databases to cluster. If not specified, the `postgres` database will be used, or if that does not exist, `template1` will be used. This can be a [connection string](../../client-interfaces/libpq-c-library/database-connection-control-functions.md#LIBPQ-CONNSTRING). If so, connection string parameters will override any conflicting command line options. Also, connection string parameters other than the database name itself will be re-used when connecting to other databases.

<a id="id-1.9.4.3.7"></a>

## Environment

`PGDATABASE`<br>`PGHOST`<br>`PGPORT`<br>`PGUSER`

Default connection parameters

`PG_COLOR`

Specifies whether to use color in diagnostic messages. Possible values are `always`, `auto` and `never`.

This utility, like most other PostgreSQL utilities, also uses the environment variables supported by libpq (see [Section 34.15](../../client-interfaces/libpq-c-library/environment-variables.md)).

<a id="id-1.9.4.3.8"></a>

## Diagnostics

In case of difficulty, see [CLUSTER](../sql-commands/cluster.md) and [psql](psql.md) for discussions of potential problems and error messages. The database server must be running at the targeted host. Also, any default connection settings and environment variables used by the libpq front-end library will apply.

<a id="id-1.9.4.3.9"></a>

## Examples

To cluster the database `test`:

```

$ clusterdb test
```

To cluster a single table `foo` in a database named `xyzzy`:

```

$ clusterdb --table=foo xyzzy
```

<a id="id-1.9.4.3.10"></a>

## See Also

[CLUSTER](../sql-commands/cluster.md)

---

原文：[PostgreSQL 15.19 Documentation](clusterdb.md)（英文原文，待翻譯）
