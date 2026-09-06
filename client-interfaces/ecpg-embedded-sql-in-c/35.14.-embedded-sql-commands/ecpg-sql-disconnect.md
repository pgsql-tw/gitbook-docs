<a id="ECPG-SQL-DISCONNECT"></a>

# DISCONNECT

DISCONNECT — terminate a database connection

## Synopsis

```

DISCONNECT connection_name
DISCONNECT [ CURRENT ]
DISCONNECT ALL
```

<a id="id-1.7.5.20.9.3"></a>

## Description

`DISCONNECT` closes a connection (or all connections) to the database.

<a id="id-1.7.5.20.9.4"></a>

## Parameters

<em class="replaceable"><code>connection&#95;name</code></em>

A database connection name established by the `CONNECT` command.

`CURRENT`

Close the “current” connection, which is either the most recently opened connection, or the connection set by the `SET CONNECTION` command. This is also the default if no argument is given to the `DISCONNECT` command.

`ALL`

Close all open connections.

<a id="id-1.7.5.20.9.5"></a>

## Examples

```

int
main(void)
{
    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL CONNECT TO testdb AS con2 USER testuser;
    EXEC SQL CONNECT TO testdb AS con3 USER testuser;

    EXEC SQL DISCONNECT CURRENT;  /* close con3          */
    EXEC SQL DISCONNECT ALL;      /* close con2 and con1 */

    return 0;
}
```

<a id="id-1.7.5.20.9.6"></a>

## Compatibility

`DISCONNECT` is specified in the SQL standard.

<a id="id-1.7.5.20.9.7"></a>

## See Also

[CONNECT](ecpg-sql-connect.md), [SET CONNECTION](ecpg-sql-set-connection.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-disconnect.html)（英文原文，待翻譯）
