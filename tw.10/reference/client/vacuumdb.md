# vacuumdb

vacuumdb — garbage-collect and analyze a PostgreSQL database

### Synopsis

`vacuumdb` \[_`connection-option`_...\] \[_`option`_...\] \[ `--table` \| `-t` _`table`_ \[\( _`column`_ \[,...\] \)\] \] ... \[_`dbname`_\]

`vacuumdb` \[_`connection-option`_...\] \[_`option`_...\] `--all` \| `-a`

### Description

vacuumdb is a utility for cleaning a PostgreSQL database. vacuumdb will also generate internal statistics used by the PostgreSQL query optimizer.

vacuumdb is a wrapper around the SQL command [VACUUM](https://www.postgresql.org/docs/10/static/sql-vacuum.html). There is no effective difference between vacuuming and analyzing databases via this utility and via other methods for accessing the server.

### Options

vacuumdb accepts the following command-line arguments:

`-a`  
`--all`

Vacuum all databases.

`[-d]` _`dbname`_  
`[--dbname=]`_`dbname`_

Specifies the name of the database to be cleaned or analyzed. If this is not specified and `-a` \(or `--all`\) is not used, the database name is read from the environment variable `PGDATABASE`. If that is not set, the user name specified for the connection is used.

`-e`  
`--echo`

Echo the commands that vacuumdb generates and sends to the server.

`-f`  
`--full`

Perform “full” vacuuming.

`-F`  
`--freeze`

Aggressively “freeze” tuples.

`-j` _`njobs`_  
`--jobs=`_`njobs`_

Execute the vacuum or analyze commands in parallel by running _`njobs`_ commands simultaneously. This option reduces the time of the processing but it also increases the load on the database server.

vacuumdb will open _`njobs`_ connections to the database, so make sure your [max\_connections](https://www.postgresql.org/docs/10/static/runtime-config-connection.html#GUC-MAX-CONNECTIONS) setting is high enough to accommodate all connections.

Note that using this mode together with the `-f` \(`FULL`\) option might cause deadlock failures if certain system catalogs are processed in parallel.

`-q`  
`--quiet`

Do not display progress messages.

`-t` _`table`_ \[ \(_`column`_ \[,...\]\) \]  
`--table=`_`table`_ \[ \(_`column`_ \[,...\]\) \]

Clean or analyze _`table`_ only. Column names can be specified only in conjunction with the `--analyze` or `--analyze-only` options. Multiple tables can be vacuumed by writing multiple `-t` switches.

#### Tip

If you specify columns, you probably have to escape the parentheses from the shell. \(See examples below.\)

`-v`  
`--verbose`

Print detailed information during processing.

`-V`  
`--version`

Print the vacuumdb version and exit.

`-z`  
`--analyze`

Also calculate statistics for use by the optimizer.

`-Z`  
`--analyze-only`

Only calculate statistics for use by the optimizer \(no vacuum\).

`--analyze-in-stages`

Only calculate statistics for use by the optimizer \(no vacuum\), like `--analyze-only`. Run several \(currently three\) stages of analyze with different configuration settings, to produce usable statistics faster.

This option is useful to analyze a database that was newly populated from a restored dump or by `pg_upgrade`. This option will try to create some statistics as fast as possible, to make the database usable, and then produce full statistics in the subsequent stages.

`-?`  
`--help`

Show help about vacuumdb command line arguments, and exit.

vacuumdb also accepts the following command-line arguments for connection parameters:

`-h` _`host`_  
`--host=`_`host`_

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket.

`-p` _`port`_  
`--port=`_`port`_

Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections.

`-U` _`username`_  
`--username=`_`username`_

User name to connect as.

`-w`  
`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.

`-W`  
`--password`

Force vacuumdb to prompt for a password before connecting to a database.

This option is never essential, since vacuumdb will automatically prompt for a password if the server demands password authentication. However, vacuumdb will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.

`--maintenance-db=`_`dbname`_

Specifies the name of the database to connect to discover what other databases should be vacuumed. If not specified, the `postgres` database will be used, and if that does not exist, `template1` will be used.

### Environment

`PGDATABASE`  
`PGHOST`  
`PGPORT`  
`PGUSER`

Default connection parameters

This utility, like most other PostgreSQL utilities, also uses the environment variables supported by libpq \(see [Section 33.14](https://www.postgresql.org/docs/10/static/libpq-envars.html)\).

### Diagnostics

In case of difficulty, see [VACUUM](https://www.postgresql.org/docs/10/static/sql-vacuum.html) and [psql](https://www.postgresql.org/docs/10/static/app-psql.html) for discussions of potential problems and error messages. The database server must be running at the targeted host. Also, any default connection settings and environment variables used by the libpq front-end library will apply.

### Notes

vacuumdb might need to connect several times to the PostgreSQL server, asking for a password each time. It is convenient to have a `~/.pgpass` file in such cases. See[Section 33.15 ](../../client-interfaces/libpq-c-library/password-file.md)for more information.

### Examples

To clean the database `test`:

```text
$ vacuumdb test
```

To clean and analyze for the optimizer a database named `bigdb`:

```text
$ vacuumdb --analyze bigdb
```

To clean a single table `foo` in a database named `xyzzy`, and analyze a single column `bar` of the table for the optimizer:

```text
$ vacuumdb --analyze --verbose --table='foo(bar)' xyzzy
```

### See Also

[VACUUM](../sql-commands/vacuum.md)

