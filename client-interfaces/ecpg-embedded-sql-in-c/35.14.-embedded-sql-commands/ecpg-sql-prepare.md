<a id="ECPG-SQL-PREPARE"></a>

# PREPARE

PREPARE — prepare a statement for execution

## Synopsis

```

PREPARE prepared_name FROM string
```

<a id="id-1.7.5.20.13.3"></a>

## Description

`PREPARE` prepares a statement dynamically specified as a string for execution. This is different from the direct SQL statement [PREPARE](../../../reference/sql-commands/prepare.md), which can also be used in embedded programs. The [EXECUTE](../../../reference/sql-commands/execute.md) command is used to execute either kind of prepared statement.

<a id="id-1.7.5.20.13.4"></a>

## Parameters

<em class="replaceable"><code>prepared&#95;name</code></em>

An identifier for the prepared query.

<em class="replaceable"><code>string</code></em>

A literal string or a host variable containing a preparable SQL statement, one of SELECT, INSERT, UPDATE, or DELETE. Use question marks (`?`) for parameter values to be supplied at execution.

<a id="id-1.7.5.20.13.5"></a>

## Notes

In typical usage, the <em class="replaceable"><code>string</code></em> is a host variable reference to a string containing a dynamically-constructed SQL statement. The case of a literal string is not very useful; you might as well just write a direct SQL `PREPARE` statement.

If you do use a literal string, keep in mind that any double quotes you might wish to include in the SQL statement must be written as octal escapes (`\042`) not the usual C idiom `\"`. This is because the string is inside an `EXEC SQL` section, so the ECPG lexer parses it according to SQL rules not C rules. Any embedded backslashes will later be handled according to C rules; but `\"` causes an immediate syntax error because it is seen as ending the literal.

<a id="id-1.7.5.20.13.6"></a>

## Examples

```

char *stmt = "SELECT * FROM test1 WHERE a = ? AND b = ?";

EXEC SQL ALLOCATE DESCRIPTOR outdesc;
EXEC SQL PREPARE foo FROM :stmt;

EXEC SQL EXECUTE foo USING SQL DESCRIPTOR indesc INTO SQL DESCRIPTOR outdesc;
```

<a id="id-1.7.5.20.13.7"></a>

## Compatibility

`PREPARE` is specified in the SQL standard.

<a id="id-1.7.5.20.13.8"></a>

## See Also

[EXECUTE](../../../reference/sql-commands/execute.md)

---

原文：[PostgreSQL 15.19 Documentation](ecpg-sql-prepare.md)（英文原文，待翻譯）
