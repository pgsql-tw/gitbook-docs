<a id="id-1.9.3.29.1"></a>

## ALTER SCHEMA

ALTER SCHEMA — change the definition of a schema

## Synopsis

```

ALTER SCHEMA name RENAME TO new_name
ALTER SCHEMA name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.29.5"></a>

## Description

`ALTER SCHEMA` changes the definition of a schema.

You must own the schema to use `ALTER SCHEMA`.
To rename a schema you must also have the
`CREATE` privilege for the database.
To alter the owner, you must be able to `SET ROLE` to the
new owning role, and that role must have the
`CREATE` privilege for the database.
(Note that superusers have all these privileges automatically.)

<a id="id-1.9.3.29.6"></a>

## Parameters

*`name`*
:   The name of an existing schema.

*`new_name`*
:   The new name of the schema. The new name cannot
    begin with `pg_`, as such names
    are reserved for system schemas.

*`new_owner`*
:   The new owner of the schema.

<a id="id-1.9.3.29.7"></a>

## Compatibility

There is no `ALTER SCHEMA` statement in the SQL
standard.

<a id="id-1.9.3.29.8"></a>

## See Also

[CREATE SCHEMA](sql-createschema.md), [DROP SCHEMA](sql-dropschema.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterschema.html)（英文原文，待翻譯）
