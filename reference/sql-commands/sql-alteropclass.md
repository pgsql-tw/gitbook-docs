<a id="id-1.9.3.21.1"></a>

## ALTER OPERATOR CLASS

ALTER OPERATOR CLASS — change the definition of an operator class

## Synopsis

```

ALTER OPERATOR CLASS name USING index_method
    RENAME TO new_name

ALTER OPERATOR CLASS name USING index_method
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR CLASS name USING index_method
    SET SCHEMA new_schema
```

<a id="id-1.9.3.21.5"></a>

## Description

`ALTER OPERATOR CLASS` changes the definition of
an operator class.

You must own the operator class to use `ALTER OPERATOR CLASS`.
To alter the owner, you must be able to `SET ROLE` to the
new owning role, and that role must have `CREATE`
privilege on the operator class's schema.
(These restrictions enforce that altering the
owner doesn't do anything you couldn't do by dropping and recreating the
operator class. However, a superuser can alter ownership of any operator
class anyway.)

<a id="id-1.9.3.21.6"></a>

## Parameters

*`name`*
:   The name (optionally schema-qualified) of an existing operator
    class.

*`index_method`*
:   The name of the index method this operator class is for.

*`new_name`*
:   The new name of the operator class.

*`new_owner`*
:   The new owner of the operator class.

*`new_schema`*
:   The new schema for the operator class.

<a id="id-1.9.3.21.7"></a>

## Compatibility

There is no `ALTER OPERATOR CLASS` statement in
the SQL standard.

<a id="id-1.9.3.21.8"></a>

## See Also

[CREATE OPERATOR CLASS](sql-createopclass.md), [DROP OPERATOR CLASS](sql-dropopclass.md), [ALTER OPERATOR FAMILY](sql-alteropfamily.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alteropclass.html)（英文原文，待翻譯）
