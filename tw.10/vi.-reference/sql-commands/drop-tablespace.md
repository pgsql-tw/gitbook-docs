# DROP TABLESPACE

DROP TABLESPACE — remove a tablespace

### Synopsis

```text
DROP TABLESPACE [ IF EXISTS ] name
```

### Description

`DROP TABLESPACE` removes a tablespace from the system.

A tablespace can only be dropped by its owner or a superuser. The tablespace must be empty of all database objects before it can be dropped. It is possible that objects in other databases might still reside in the tablespace even if no objects in the current database are using the tablespace. Also, if the tablespace is listed in the [temp\_tablespaces](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TEMP-TABLESPACES) setting of any active session, the `DROP` might fail due to temporary files residing in the tablespace.

### Parameters

`IF EXISTS`

Do not throw an error if the tablespace does not exist. A notice is issued in this case._`name`_

The name of a tablespace.

### Notes

`DROP TABLESPACE` cannot be executed inside a transaction block.

### Examples

To remove tablespace `mystuff` from the system:

```text
DROP TABLESPACE mystuff;
```

### Compatibility

`DROP TABLESPACE` is a PostgreSQL extension.

### See Also

[CREATE TABLESPACE](create-tablespace.md), [ALTER TABLESPACE](alter-tablespace.md)

