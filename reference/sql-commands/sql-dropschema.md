<a id="id-1.9.3.129.1"></a>

## DROP SCHEMA

DROP SCHEMA — remove a schema

## Synopsis

```

DROP SCHEMA [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.129.5"></a>

## Description

`DROP SCHEMA` removes schemas from the database.

A schema can only be dropped by its owner or a superuser. Note that
the owner can drop the schema (and thereby all contained objects)
even if they do not own some of the objects within the schema.

<a id="id-1.9.3.129.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the schema does not exist. A notice is issued
    in this case.

*`name`*
:   The name of a schema.

`CASCADE`
:   Automatically drop objects (tables, functions, etc.) that are
    contained in the schema,
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the schema if it contains any objects. This is
    the default.

<a id="id-1.9.3.129.7"></a>

## Notes

Using the `CASCADE` option might make the command
remove objects in other schemas besides the one(s) named.

<a id="id-1.9.3.129.8"></a>

## Examples

To remove schema `mystuff` from the database,
along with everything it contains:

```

DROP SCHEMA mystuff CASCADE;
```

<a id="id-1.9.3.129.9"></a>

## Compatibility

`DROP SCHEMA` is fully conforming with the SQL
standard, except that the standard only allows one schema to be
dropped per command, and apart from the
`IF EXISTS` option, which is a PostgreSQL
extension.

<a id="id-1.9.3.129.10"></a>

## See Also

[ALTER SCHEMA](sql-alterschema.md), [CREATE SCHEMA](sql-createschema.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropschema.html)（英文原文，待翻譯）
