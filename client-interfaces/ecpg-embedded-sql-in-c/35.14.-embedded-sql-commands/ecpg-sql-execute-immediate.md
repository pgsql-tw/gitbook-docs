<a id="ECPG-SQL-EXECUTE-IMMEDIATE"></a>

# EXECUTE IMMEDIATE

EXECUTE IMMEDIATE — dynamically prepare and execute a statement

## Synopsis

```

EXECUTE IMMEDIATE string
```

<a id="id-1.7.5.20.10.3"></a>

## Description

`EXECUTE IMMEDIATE` immediately prepares and executes a dynamically specified SQL statement, without retrieving result rows.

<a id="id-1.7.5.20.10.4"></a>

## Parameters

<em class="replaceable"><code>string</code></em>

A literal string or a host variable containing the SQL statement to be executed.

<a id="id-1.7.5.20.10.5"></a>

## Notes

In typical usage, the <em class="replaceable"><code>string</code></em> is a host variable reference to a string containing a dynamically-constructed SQL statement. The case of a literal string is not very useful; you might as well just write the SQL statement directly, without the extra typing of `EXECUTE IMMEDIATE`.

If you do use a literal string, keep in mind that any double quotes you might wish to include in the SQL statement must be written as octal escapes (`\042`) not the usual C idiom `\"`. This is because the string is inside an `EXEC SQL` section, so the ECPG lexer parses it according to SQL rules not C rules. Any embedded backslashes will later be handled according to C rules; but `\"` causes an immediate syntax error because it is seen as ending the literal.

<a id="id-1.7.5.20.10.6"></a>

## Examples

Here is an example that executes an `INSERT` statement using `EXECUTE IMMEDIATE` and a host variable named `command`:

```

sprintf(command, "INSERT INTO test (name, amount, letter) VALUES ('db: ''r1''', 1, 'f')");
EXEC SQL EXECUTE IMMEDIATE :command;
```

<a id="id-1.7.5.20.10.7"></a>

## Compatibility

`EXECUTE IMMEDIATE` is specified in the SQL standard.

---

原文：[PostgreSQL 15.19 Documentation](ecpg-sql-execute-immediate.md)（英文原文，待翻譯）
