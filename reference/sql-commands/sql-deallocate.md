<a id="id-1.9.3.98.1"></a><a id="id-1.9.3.98.2"></a>

## DEALLOCATE

DEALLOCATE — deallocate a prepared statement

## Synopsis

```

DEALLOCATE [ PREPARE ] { name | ALL }
```

<a id="id-1.9.3.98.6"></a>

## Description

`DEALLOCATE` is used to deallocate a previously
prepared SQL statement. If you do not explicitly deallocate a
prepared statement, it is deallocated when the session ends.

For more information on prepared statements, see [PREPARE](sql-prepare.md).

<a id="id-1.9.3.98.7"></a>

## Parameters

`PREPARE`
:   This key word is ignored.

*`name`*
:   The name of the prepared statement to deallocate.

`ALL`
:   Deallocate all prepared statements.

<a id="id-1.9.3.98.8"></a>

## Compatibility

The SQL standard includes a `DEALLOCATE`
statement, but it is only for use in embedded SQL.

<a id="id-1.9.3.98.9"></a>

## See Also

[EXECUTE](sql-execute.md), [PREPARE](sql-prepare.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-deallocate.html)（英文原文，待翻譯）
