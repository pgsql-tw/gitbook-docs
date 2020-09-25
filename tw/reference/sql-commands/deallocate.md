# DEALLOCATE

DEALLOCATE — deallocate a prepared statement

### Synopsis

```text
DEALLOCATE [ PREPARE ] { name | ALL }
```

### Description

`DEALLOCATE` is used to deallocate a previously prepared SQL statement. If you do not explicitly deallocate a prepared statement, it is deallocated when the session ends.

For more information on prepared statements, see [PREPARE](https://www.postgresql.org/docs/13/sql-prepare.html).

### Parameters

`PREPARE`

This key word is ignored.

_`name`_

The name of the prepared statement to deallocate.

`ALL`

Deallocate all prepared statements.

### Compatibility

The SQL standard includes a `DEALLOCATE` statement, but it is only for use in embedded SQL.

### See Also

[EXECUTE](https://www.postgresql.org/docs/13/sql-execute.html), [PREPARE](https://www.postgresql.org/docs/13/sql-prepare.html)

