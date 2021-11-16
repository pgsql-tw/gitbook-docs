# pg\_isready

pg\_isready — check the connection status of a PostgreSQL server

### Synopsis

`pg_isready` \[_`connection-option`_...] \[_`option`_...]

### Description

pg\_isready is a utility for checking the connection status of a PostgreSQL database server. The exit status specifies the result of the connection check.

### Options

`-d `_`dbname`_\
`--dbname=`_`dbname`_

Specifies the name of the database to connect to. The _`dbname`_ can be a [connection string](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-CONNSTRING). If so, connection string parameters will override any conflicting command line options.

`-h `_`hostname`_\
`--host=`_`hostname`_

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix-domain socket.

`-p `_`port`_\
`--port=`_`port`_

Specifies the TCP port or the local Unix-domain socket file extension on which the server is listening for connections. Defaults to the value of the `PGPORT` environment variable or, if not set, to the port specified at compile time, usually 5432.

`-q`\
`--quiet`

Do not display status message. This is useful when scripting.

`-t `_`seconds`_\
`--timeout=`_`seconds`_

The maximum number of seconds to wait when attempting connection before returning that the server is not responding. Setting to 0 disables. The default is 3 seconds.

`-U `_`username`_\
`--username=`_`username`_

Connect to the database as the user _`username`_ instead of the default.

`-V`\
`--version`

Print the pg\_isready version and exit.

`-?`\
`--help`

Show help about pg\_isready command line arguments, and exit.

### Exit Status

pg\_isready returns `0` to the shell if the server is accepting connections normally, `1` if the server is rejecting connections (for example during startup), `2` if there was no response to the connection attempt, and `3` if no attempt was made (for example due to invalid parameters).

### Environment

`pg_isready`, like most other PostgreSQL utilities, also uses the environment variables supported by libpq (see [Section 33.14](https://www.postgresql.org/docs/13/libpq-envars.html)).

The environment variable `PG_COLOR` specifies whether to use color in diagnostic messages. Possible values are `always`, `auto` and `never`.

### Notes

It is not necessary to supply correct user name, password, or database name values to obtain the server status; however, if incorrect values are provided, the server will log a failed connection attempt.

### Examples

Standard Usage:

```
$ pg_isready
/tmp:5432 - accepting connections
$ echo $?
0
```

Running with connection parameters to a PostgreSQL cluster in startup:

```
$ pg_isready -h localhost -p 5433
localhost:5433 - rejecting connections
$ echo $?
1
```

Running with connection parameters to a non-responsive PostgreSQL cluster:

```
$ pg_isready -h someremotehost
someremotehost:5432 - no response
$ echo $?
2
```
