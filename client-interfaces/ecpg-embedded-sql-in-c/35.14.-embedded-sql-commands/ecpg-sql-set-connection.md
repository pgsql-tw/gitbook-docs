<a id="ECPG-SQL-SET-CONNECTION"></a>

# SET CONNECTION

SET CONNECTION — select a database connection

## Synopsis

```

SET CONNECTION [ TO | = ] connection_name
```

<a id="id-1.7.5.20.15.3"></a>

## Description

`SET CONNECTION` sets the “current” database connection, which is the one that all commands use unless overridden.

<a id="id-1.7.5.20.15.4"></a>

## Parameters

<em class="replaceable"><code>connection&#95;name</code></em>

A database connection name established by the `CONNECT` command.

`CURRENT`

Set the connection to the current connection (thus, nothing happens).

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

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-set-connection.html)（英文原文，待翻譯）
