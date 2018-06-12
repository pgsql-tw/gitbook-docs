---
description: 版本：10
---

# EXECUTE

EXECUTE — execute a prepared statement

### Synopsis

```text
EXECUTE name [ ( parameter [, ...] ) ]
```

### Description

`EXECUTE` is used to execute a previously prepared statement. Since prepared statements only exist for the duration of a session, the prepared statement must have been created by a `PREPARE` statement executed earlier in the current session.

If the `PREPARE` statement that created the statement specified some parameters, a compatible set of parameters must be passed to the `EXECUTE` statement, or else an error is raised. Note that \(unlike functions\) prepared statements are not overloaded based on the type or number of their parameters; the name of a prepared statement must be unique within a database session.

For more information on the creation and usage of prepared statements, see [PREPARE](https://www.postgresql.org/docs/10/static/sql-prepare.html).

### Parameters

_`name`_

The name of the prepared statement to execute.

_`parameter`_

The actual value of a parameter to the prepared statement. This must be an expression yielding a value that is compatible with the data type of this parameter, as was determined when the prepared statement was created.

### Outputs

The command tag returned by `EXECUTE` is that of the prepared statement, and not `EXECUTE`.

### Examples

Examples are given in the [Examples](https://www.postgresql.org/docs/10/static/sql-prepare.html#SQL-PREPARE-EXAMPLES) section of the [PREPARE](https://www.postgresql.org/docs/10/static/sql-prepare.html) documentation.

### Compatibility

The SQL standard includes an `EXECUTE` statement, but it is only for use in embedded SQL. This version of the `EXECUTE` statement also uses a somewhat different syntax.

### See Also

[DEALLOCATE](https://www.postgresql.org/docs/10/static/sql-deallocate.html), [PREPARE](https://www.postgresql.org/docs/10/static/sql-prepare.html)

