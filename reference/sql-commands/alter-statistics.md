---
description: 版本：11
---

# ALTER STATISTICS

ALTER STATISTICS — change the definition of an extended statistics object

### Synopsis

```
ALTER STATISTICS name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER STATISTICS name RENAME TO new_name
ALTER STATISTICS name SET SCHEMA new_schema
ALTER STATISTICS name SET STATISTICS new_target
```

### Description

`ALTER STATISTICS` changes the parameters of an existing extended statistics object. Any parameters not specifically set in the `ALTER STATISTICS` command retain their prior settings.

You must own the statistics object to use `ALTER STATISTICS`. To change a statistics object's schema, you must also have `CREATE` privilege on the new schema. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the statistics object's schema. (These restrictions enforce that altering the owner doesn't do anything you couldn't do by dropping and recreating the statistics object. However, a superuser can alter ownership of any statistics object anyway.)

### Parameters

_`name`_

The name (optionally schema-qualified) of the statistics object to be altered.

_`new_owner`_

The user name of the new owner of the statistics object.

_`new_name`_

The new name for the statistics object.

_`new_schema`_

The new schema for the statistics object.

_`new_target`_

The statistic-gathering target for this statistics object for subsequent [ANALYZE](https://www.postgresql.org/docs/13/sql-analyze.html) operations. The target can be set in the range 0 to 10000; alternatively, set it to -1 to revert to using the maximum of the statistics target of the referenced columns, if set, or the system default statistics target ([default\_statistics\_target](https://www.postgresql.org/docs/13/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET)). For more information on the use of statistics by the PostgreSQL query planner, refer to [Section 14.2](https://www.postgresql.org/docs/13/planner-stats.html).

### Compatibility

There is no `ALTER STATISTICS` command in the SQL standard.

### See Also

[CREATE STATISTICS](create-statistics.md), [DROP STATISTICS](drop-statistics.md)
