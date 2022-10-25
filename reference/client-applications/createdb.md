# createdb

createdb — create a newPostgreSQLdatabase

## Synopsis

`createdb`\[`connection-option`...] \[`option`...] \[`dbname`\[`description`]]

## Description

createdbcreates a newPostgreSQLdatabase.

Normally, the database user who executes this command becomes the owner of the new database. However, a different owner can be specified via the`-O`option, if the executing user has appropriate privileges.

createdbis a wrapper around theSQLcommand[CREATE DATABASE](https://www.postgresql.org/docs/10/static/sql-createdatabase.html). There is no effective difference between creating databases via this utility and via other methods for accessing the server.

## Options

createdbaccepts the following command-line arguments:

`dbname`

Specifies the name of the database to be created. The name must be unique among allPostgreSQLdatabases in this cluster. The default is to create a database with the same name as the current system user.

`description`

Specifies a comment to be associated with the newly created database.

`-D`

`tablespace`

`--tablespace=`

`tablespace`

Specifies the default tablespace for the database. (This name is processed as a double-quoted identifier.)

`-e`

`--echo`

Echo the commands thatcreatedbgenerates and sends to the server.

`-E`

`encoding`

`--encoding=`

`encoding`

Specifies the character encoding scheme to be used in this database. The character sets supported by thePostgreSQLserver are described in[Section 23.3.1](https://www.postgresql.org/docs/10/static/multibyte.html#multibyte-charset-supported).

`-l`

`locale`

`--locale=`

`locale`

Specifies the locale to be used in this database. This is equivalent to specifying both`--lc-collate`and`--lc-ctype`.

`--lc-collate=`

`locale`

Specifies the LC\_COLLATE setting to be used in this database.

`--lc-ctype=`

`locale`

Specifies the LC\_CTYPE setting to be used in this database.

`-O`

`owner`

`--owner=`

`owner`

Specifies the database user who will own the new database. (This name is processed as a double-quoted identifier.)

`-T`

`template`

`--template=`

`template`

Specifies the template database from which to build this database. (This name is processed as a double-quoted identifier.)

`-V`

`--version`

Print thecreatedbversion and exit.

`-?`

`--help`

Show help aboutcreatedbcommand line arguments, and exit.

The options`-D`,`-l`,`-E`,`-O`, and`-T`correspond to options of the underlying SQL command[CREATE DATABASE](https://www.postgresql.org/docs/10/static/sql-createdatabase.html); see there for more information about them.

createdbalso accepts the following command-line arguments for connection parameters:

`-h`

`host`

`--host=`

`host`

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket.

`-p`

`port`

`--port=`

`port`

Specifies the TCP port or the local Unix domain socket file extension on which the server is listening for connections.

`-U`

`username`

`--username=`

`username`

User name to connect as.

`-w`

`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a`.pgpass`file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.

`-W`

`--password`

Forcecreatedbto prompt for a password before connecting to a database.

This option is never essential, sincecreatedbwill automatically prompt for a password if the server demands password authentication. However,createdbwill waste a connection attempt finding out that the server wants a password. In some cases it is worth typing`-W`to avoid the extra connection attempt.

`--maintenance-db=`

`dbname`

Specifies the name of the database to connect to when creating the new database. If not specified, the`postgres`database will be used; if that does not exist (or if it is the name of the new database being created),`template1`will be used.

## Environment

`PGDATABASE`

If set, the name of the database to create, unless overridden on the command line.

`PGHOST`

`PGPORT`

`PGUSER`

Default connection parameters.`PGUSER`also determines the name of the database to create, if it is not specified on the command line or by`PGDATABASE`.

This utility, like most otherPostgreSQLutilities, also uses the environment variables supported bylibpq(see[Section 33.14](https://www.postgresql.org/docs/10/static/libpq-envars.html)).

## Diagnostics

In case of difficulty, see[CREATE DATABASE](https://www.postgresql.org/docs/10/static/sql-createdatabase.html)and[psql](https://www.postgresql.org/docs/10/static/app-psql.html)for discussions of potential problems and error messages. The database server must be running at the targeted host. Also, any default connection settings and environment variables used by thelibpqfront-end library will apply.

## Examples

To create the database`demo`using the default database server:

```
$ 
createdb demo
```

To create the database`demo`using the server on host`eden`, port 5000, using the`template0`template database, here is the command-line command and the underlying SQL command:

```
$ 
createdb -p 5000 -h eden -T template0 -e demo
CREATE DATABASE demo TEMPLATE template0;
```

## See Also

[dropdb](https://www.postgresql.org/docs/10/static/app-dropdb.html)

,

[CREATE DATABASE](https://www.postgresql.org/docs/10/static/sql-createdatabase.html)
