## CONNECT

CONNECT — establish a database connection

## Synopsis

```

CONNECT TO connection_target [ AS connection_name ] [ USER connection_user ]
CONNECT TO DEFAULT
CONNECT connection_user
DATABASE connection_target
```

<a id="id-1.7.5.20.4.3"></a>

## Description

The `CONNECT` command establishes a connection
between the client and the PostgreSQL server.

<a id="id-1.7.5.20.4.4"></a>

## Parameters

<a id="ECPG-SQL-CONNECT-CONNECTION-TARGET"></a>

*`connection_target`* [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET)
:   *`connection_target`*
    specifies the target server of the connection on one of
    several forms.

    <a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-DATABASE-NAME"></a>

    [ *`database_name`* ] [ `@`*`host`* ] [ `:`*`port`* ] [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-DATABASE-NAME)
    :   Connect over TCP/IP
    <a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-UNIX-DOMAIN-SOCKETS"></a>

    `unix:postgresql://`*`host`* [ `:`*`port`* ] `/` [ *`database_name`* ] [ `?`*`connection_option`* ] [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-UNIX-DOMAIN-SOCKETS)
    :   Connect over Unix-domain sockets
    <a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-TCP-IP"></a>

    `tcp:postgresql://`*`host`* [ `:`*`port`* ] `/` [ *`database_name`* ] [ `?`*`connection_option`* ] [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-TCP-IP)
    :   Connect over TCP/IP
    <a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-CONSTANT"></a>

    SQL string constant [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-CONSTANT)
    :   containing a value in one of the above forms
    <a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-HOST-VARIABLE"></a>

    host variable [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-HOST-VARIABLE)
    :   host variable of type `char[]`
        or `VARCHAR[]` containing a value in one of the
        above forms
<a id="ECPG-SQL-CONNECT-CONNECTION-NAME"></a>

*`connection_name`* [#](#ECPG-SQL-CONNECT-CONNECTION-NAME)
:   An optional identifier for the connection, so that it can be
    referred to in other commands. This can be an SQL identifier
    or a host variable.
<a id="ECPG-SQL-CONNECT-CONNECTION-USER"></a>

*`connection_user`* [#](#ECPG-SQL-CONNECT-CONNECTION-USER)
:   The user name for the database connection.

    This parameter can also specify user name and password, using one the forms
    `user_name/password`,
    `user_name IDENTIFIED BY password`, or
    `user_name USING password`.

    User name and password can be SQL identifiers, string
    constants, or host variables.
<a id="ECPG-SQL-CONNECT-DEFAULT"></a>

`DEFAULT` [#](#ECPG-SQL-CONNECT-DEFAULT)
:   Use all default connection parameters, as defined by libpq.

<a id="id-1.7.5.20.4.5"></a>

## Examples

Here a several variants for specifying connection parameters:

```

EXEC SQL CONNECT TO "connectdb" AS main;
EXEC SQL CONNECT TO "connectdb" AS second;
EXEC SQL CONNECT TO "unix:postgresql://200.46.204.71/connectdb" AS main USER connectuser;
EXEC SQL CONNECT TO "unix:postgresql://localhost/connectdb" AS main USER connectuser;
EXEC SQL CONNECT TO 'connectdb' AS main;
EXEC SQL CONNECT TO 'unix:postgresql://localhost/connectdb' AS main USER :user;
EXEC SQL CONNECT TO :db AS :id;
EXEC SQL CONNECT TO :db USER connectuser USING :pw;
EXEC SQL CONNECT TO @localhost AS main USER connectdb;
EXEC SQL CONNECT TO REGRESSDB1 as main;
EXEC SQL CONNECT TO AS main USER connectdb;
EXEC SQL CONNECT TO connectdb AS :id;
EXEC SQL CONNECT TO connectdb AS main USER connectuser/connectdb;
EXEC SQL CONNECT TO connectdb AS main;
EXEC SQL CONNECT TO connectdb@localhost AS main;
EXEC SQL CONNECT TO tcp:postgresql://localhost/ USER connectdb;
EXEC SQL CONNECT TO tcp:postgresql://localhost/connectdb USER connectuser IDENTIFIED BY connectpw;
EXEC SQL CONNECT TO tcp:postgresql://localhost:20/connectdb USER connectuser IDENTIFIED BY connectpw;
EXEC SQL CONNECT TO unix:postgresql://localhost/ AS main USER connectdb;
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb AS main USER connectuser;
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb USER connectuser IDENTIFIED BY "connectpw";
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb USER connectuser USING "connectpw";
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb?connect_timeout=14 USER connectuser;
```

Here is an example program that illustrates the use of host
variables to specify connection parameters:

```

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    char *dbname     = "testdb";    /* database name */
    char *user       = "testuser";  /* connection user name */
    char *connection = "tcp:postgresql://localhost:5432/testdb";
                                    /* connection string */
    char ver[256];                  /* buffer to store the version string */
EXEC SQL END DECLARE SECTION;

    ECPGdebug(1, stderr);

    EXEC SQL CONNECT TO :dbname USER :user;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL SELECT version() INTO :ver;
    EXEC SQL DISCONNECT;

    printf("version: %s\n", ver);

    EXEC SQL CONNECT TO :connection USER :user;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL SELECT version() INTO :ver;
    EXEC SQL DISCONNECT;

    printf("version: %s\n", ver);

    return 0;
}
```

<a id="id-1.7.5.20.4.6"></a>

## Compatibility

`CONNECT` is specified in the SQL standard, but
the format of the connection parameters is
implementation-specific.

<a id="id-1.7.5.20.4.7"></a>

## See Also

[DISCONNECT](ecpg-sql-disconnect.md), [SET CONNECTION](ecpg-sql-set-connection.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-connect.html)（英文原文，待翻譯）
