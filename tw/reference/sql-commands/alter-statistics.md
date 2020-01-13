---
description: 版本：11
---

# ALTER STATISTICS

ALTER STATISTICS — change the definition of an extended statistics object

## Synopsis

```text
ALTER STATISTICS name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER STATISTICS name RENAME TO new_name
ALTER STATISTICS name SET SCHEMA new_schema
```

## Description

`ALTER STATISTICS` changes the parameters of an existing extended statistics object. Any parameters not specifically set in the `ALTER STATISTICS` command retain their prior settings.

You must own the statistics object to use `ALTER STATISTICS`. To change a statistics object's schema, you must also have `CREATE` privilege on the new schema. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the statistics object's schema. \(These restrictions enforce that altering the owner doesn't do anything you couldn't do by dropping and recreating the statistics object. However, a superuser can alter ownership of any statistics object anyway.\)

## Parameters

_`name`_

The name \(optionally schema-qualified\) of the statistics object to be altered.

_`new_owner`_

The user name of the new owner of the statistics object.

_`new_name`_

The new name for the statistics object.

_`new_schema`_

The new schema for the statistics object.

## Compatibility

There is no `ALTER STATISTICS` command in the SQL standard.

## See Also

[CREATE STATISTICS](create-statistics.md), [DROP STATISTICS](drop-statistics.md)

