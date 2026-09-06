<a id="ECPG-SQL-DECLARE-STATEMENT"></a>

# DECLARE STATEMENT

DECLARE STATEMENT — declare SQL statement identifier

## Synopsis

```

EXEC SQL [ AT connection_name ] DECLARE statement_name STATEMENT
```

<a id="id-1.7.5.20.7.3"></a>

## Description

`DECLARE STATEMENT` declares an SQL statement identifier. SQL statement identifier can be associated with the connection. When the identifier is used by dynamic SQL statements, the statements are executed using the associated connection. The namespace of the declaration is the precompile unit, and multiple declarations to the same SQL statement identifier are not allowed. Note that if the precompiler runs in Informix compatibility mode and some SQL statement is declared, "database" can not be used as a cursor name.

<a id="id-1.7.5.20.7.4"></a>

## Parameters

<em class="replaceable"><code>connection&#95;name</code></em>

A database connection name established by the `CONNECT` command.

AT clause can be omitted, but such statement has no meaning.

<em class="replaceable"><code>statement&#95;name</code></em>

The name of an SQL statement identifier, either as an SQL identifier or a host variable.

<a id="id-1.7.5.20.7.5"></a>

## Notes

This association is valid only if the declaration is physically placed on top of a dynamic statement.

<a id="id-1.7.5.20.7.6"></a>

## Examples

```

EXEC SQL CONNECT TO postgres AS con1;
EXEC SQL AT con1 DECLARE sql_stmt STATEMENT;
EXEC SQL DECLARE cursor_name CURSOR FOR sql_stmt;
EXEC SQL PREPARE sql_stmt FROM :dyn_string;
EXEC SQL OPEN cursor_name;
EXEC SQL FETCH cursor_name INTO :column1;
EXEC SQL CLOSE cursor_name;
```

<a id="id-1.7.5.20.7.7"></a>

## Compatibility

`DECLARE STATEMENT` is an extension of the SQL standard, but can be used in famous DBMSs.

<a id="id-1.7.5.20.7.8"></a>

## See Also

[CONNECT](ecpg-sql-connect.md), [DECLARE](ecpg-sql-declare.md), [OPEN](ecpg-sql-open.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-declare-statement.html)（英文原文，待翻譯）
