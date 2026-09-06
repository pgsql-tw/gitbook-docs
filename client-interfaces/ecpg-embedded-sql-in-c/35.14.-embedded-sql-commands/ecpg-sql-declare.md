<a id="ECPG-SQL-DECLARE"></a>

# DECLARE

DECLARE — define a cursor

## Synopsis

```

DECLARE cursor_name [ BINARY ] [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ] CURSOR [ { WITH | WITHOUT } HOLD ] FOR prepared_name
DECLARE cursor_name [ BINARY ] [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ] CURSOR [ { WITH | WITHOUT } HOLD ] FOR query
```

<a id="id-1.7.5.20.6.3"></a>

## Description

`DECLARE` declares a cursor for iterating over the result set of a prepared statement. This command has slightly different semantics from the direct SQL command `DECLARE`: Whereas the latter executes a query and prepares the result set for retrieval, this embedded SQL command merely declares a name as a “loop variable” for iterating over the result set of a query; the actual execution happens when the cursor is opened with the `OPEN` command.

<a id="id-1.7.5.20.6.4"></a>

## Parameters

<em class="replaceable"><code>cursor&#95;name</code></em>

A cursor name, case sensitive. This can be an SQL identifier or a host variable.

<em class="replaceable"><code>prepared&#95;name</code></em>

The name of a prepared query, either as an SQL identifier or a host variable.

<em class="replaceable"><code>query</code></em>

A [SELECT](../../../reference/sql-commands/select.md) or [VALUES](../../../reference/sql-commands/values.md) command which will provide the rows to be returned by the cursor.

For the meaning of the cursor options, see [DECLARE](../../../reference/sql-commands/declare.md).

<a id="id-1.7.5.20.6.5"></a>

## Examples

Examples declaring a cursor for a query:

```

EXEC SQL DECLARE C CURSOR FOR SELECT * FROM My_Table;
EXEC SQL DECLARE C CURSOR FOR SELECT Item1 FROM T;
EXEC SQL DECLARE cur1 CURSOR FOR SELECT version();
```

An example declaring a cursor for a prepared statement:

```

EXEC SQL PREPARE stmt1 AS SELECT version();
EXEC SQL DECLARE cur1 CURSOR FOR stmt1;
```

<a id="id-1.7.5.20.6.6"></a>

## Compatibility

`DECLARE` is specified in the SQL standard.

<a id="id-1.7.5.20.6.7"></a>

## See Also

[OPEN](ecpg-sql-open.md), [CLOSE](../../../reference/sql-commands/close.md), [DECLARE](../../../reference/sql-commands/declare.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-declare.html)（英文原文，待翻譯）
