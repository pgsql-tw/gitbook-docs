## OPEN

OPEN — open a dynamic cursor

## Synopsis

```

OPEN cursor_name
OPEN cursor_name USING value [, ... ]
OPEN cursor_name USING SQL DESCRIPTOR descriptor_name
```

<a id="id-1.7.5.20.12.3"></a>

## Description

`OPEN` opens a cursor and optionally binds
actual values to the placeholders in the cursor's declaration.
The cursor must previously have been declared with
the `DECLARE` command. The execution
of `OPEN` causes the query to start executing on
the server.

<a id="id-1.7.5.20.12.4"></a>

## Parameters

<a id="ECPG-SQL-OPEN-CURSOR-NAME"></a>

*`cursor_name`* [#](#ECPG-SQL-OPEN-CURSOR-NAME)
:   The name of the cursor to be opened. This can be an SQL
    identifier or a host variable.
<a id="ECPG-SQL-OPEN-VALUE"></a>

*`value`* [#](#ECPG-SQL-OPEN-VALUE)
:   A value to be bound to a placeholder in the cursor. This can
    be an SQL constant, a host variable, or a host variable with
    indicator.
<a id="ECPG-SQL-OPEN-DESCRIPTOR-NAME"></a>

*`descriptor_name`* [#](#ECPG-SQL-OPEN-DESCRIPTOR-NAME)
:   The name of a descriptor containing values to be bound to the
    placeholders in the cursor. This can be an SQL identifier or
    a host variable.

<a id="id-1.7.5.20.12.5"></a>

## Examples

```

EXEC SQL OPEN a;
EXEC SQL OPEN d USING 1, 'test';
EXEC SQL OPEN c1 USING SQL DESCRIPTOR mydesc;
EXEC SQL OPEN :curname1;
```

<a id="id-1.7.5.20.12.6"></a>

## Compatibility

`OPEN` is specified in the SQL standard.

<a id="id-1.7.5.20.12.7"></a>

## See Also

[DECLARE](ecpg-sql-declare.md), [CLOSE](../../reference/sql-commands/sql-close.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-open.html)（英文原文，待翻譯）
