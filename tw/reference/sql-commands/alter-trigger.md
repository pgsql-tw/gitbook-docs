# ALTER TRIGGER

ALTER TRIGGER — change the definition of a trigger

### Synopsis

```
ALTER TRIGGER name ON table_name RENAME TO new_name
ALTER TRIGGER name ON table_name DEPENDS ON EXTENSION extension_name
```

### Description

`ALTER TRIGGER` changes properties of an existing trigger. The `RENAME` clause changes the name of the given trigger without otherwise changing the trigger definition. The `DEPENDS ON EXTENSION` clause marks the trigger as dependent on an extension, such that if the extension is dropped, the trigger will automatically be dropped as well.

You must own the table on which the trigger acts to be allowed to change its properties.

### Parameters

_`name`_

The name of an existing trigger to alter._`table_name`_

The name of the table on which this trigger acts._`new_name`_

The new name for the trigger._`extension_name`_

The name of the extension that the trigger is to depend on.

### Notes

The ability to temporarily enable or disable a trigger is provided by [ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html), not by `ALTER TRIGGER`, because `ALTER TRIGGER` has no convenient way to express the option of enabling or disabling all of a table's triggers at once.

### Examples

To rename an existing trigger:

```
ALTER TRIGGER emp_stamp ON emp RENAME TO emp_track_chgs;
```

To mark a trigger as being dependent on an extension:

```
ALTER TRIGGER emp_stamp ON emp DEPENDS ON EXTENSION emplib;
```

### Compatibility

`ALTER TRIGGER` is a PostgreSQL extension of the SQL standard.

### See Also

[ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html)
