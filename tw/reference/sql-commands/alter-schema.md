# ALTER SCHEMA

ALTER SCHEMA — change the definition of a schema

### Synopsis

```
ALTER SCHEMA name RENAME TO new_name
ALTER SCHEMA name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
```

### Description

`ALTER SCHEMA` changes the definition of a schema.

You must own the schema to use `ALTER SCHEMA`. To rename a schema you must also have the `CREATE` privilege for the database. To alter the owner, you must also be a direct or indirect member of the new owning role, and you must have the `CREATE` privilege for the database. (Note that superusers have all these privileges automatically.)

### Parameters

_`name`_

The name of an existing schema.

_`new_name`_

The new name of the schema. The new name cannot begin with `pg_`, as such names are reserved for system schemas.

_`new_owner`_

The new owner of the schema.

### Compatibility

There is no `ALTER SCHEMA` statement in the SQL standard.

### See Also

[CREATE SCHEMA](create-schema.md), [DROP SCHEMA](drop-schema.md)
