<a id="id-1.9.3.142.1"></a>

## DROP TYPE

DROP TYPE — remove a data type

## Synopsis

```

DROP TYPE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.142.5"></a>

## Description

`DROP TYPE` removes a user-defined data type.
Only the owner of a type can remove it.

<a id="id-1.9.3.142.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the type does not exist. A notice is issued
    in this case.

*`name`*
:   The name (optionally schema-qualified) of the data type to remove.

`CASCADE`
:   Automatically drop objects that depend on the type (such as
    table columns, functions, and operators),
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the type if any objects depend on it. This is
    the default.

<a id="SQL-DROPTYPE-EXAMPLES"></a>

## Examples

To remove the data type `box`:

```

DROP TYPE box;
```

<a id="SQL-DROPTYPE-COMPATIBILITY"></a>

## Compatibility

This command is similar to the corresponding command in the SQL
standard, apart from the `IF EXISTS`
option, which is a PostgreSQL extension.
But note that much of the `CREATE TYPE` command
and the data type extension mechanisms in
PostgreSQL differ from the SQL standard.

<a id="SQL-DROPTYPE-SEE-ALSO"></a>

## See Also

[ALTER TYPE](sql-altertype.md), [CREATE TYPE](sql-createtype.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptype.html)（英文原文，待翻譯）
