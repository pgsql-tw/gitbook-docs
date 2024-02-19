---
description: 版本：11
---

# DROP STATISTICS

DROP STATISTICS — remove extended statistics

### Synopsis

```
DROP STATISTICS [ IF EXISTS ] name [, ...]
```

### Description

`DROP STATISTICS` removes statistics object(s) from the database. Only the statistics object's owner, the schema owner, or a superuser can drop a statistics object.

### Parameters

`IF EXISTS`

Do not throw an error if the statistics object does not exist. A notice is issued in this case.

_`name`_

The name (optionally schema-qualified) of the statistics object to drop.

### Examples

To destroy two statistics objects in different schemas, without failing if they don't exist:

```
DROP STATISTICS IF EXISTS
    accounting.users_uid_creation,
    public.grants_user_role;
```

### Compatibility

There is no `DROP STATISTICS` command in the SQL standard.

### See Also

[ALTER STATISTICS](alter-statistics.md), [CREATE STATISTICS](create-statistics.md)
