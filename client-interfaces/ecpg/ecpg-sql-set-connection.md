## SET CONNECTION

SET CONNECTION — select a database connection

## Synopsis

```

SET CONNECTION [ TO | = ] connection_name
```

<a id="id-1.7.5.20.15.3"></a>

## Description

`SET CONNECTION` sets the “current”
database connection, which is the one that all commands use
unless overridden.

<a id="id-1.7.5.20.15.4"></a>

## Parameters

<a id="ECPG-SQL-SET-CONNECTION-CONNECTION-NAME"></a>

*`connection_name`* [#](#ECPG-SQL-SET-CONNECTION-CONNECTION-NAME)
:   A database connection name established by
    the `CONNECT` command.
<a id="ECPG-SQL-SET-CONNECTION-CURRENT"></a>

`CURRENT` [#](#ECPG-SQL-SET-CONNECTION-CURRENT)
:   Set the connection to the current connection (thus, nothing happens).

<a id="id-1.7.5.20.15.5"></a>

## Examples

```

EXEC SQL SET CONNECTION TO con2;
EXEC SQL SET CONNECTION = con1;
```

<a id="id-1.7.5.20.15.6"></a>

## Compatibility

`SET CONNECTION` is specified in the SQL standard.

<a id="id-1.7.5.20.15.7"></a>

## See Also

[CONNECT](ecpg-sql-connect.md), [DISCONNECT](ecpg-sql-disconnect.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-set-connection.html)（英文原文，待翻譯）
