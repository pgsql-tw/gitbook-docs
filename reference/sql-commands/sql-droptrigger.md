<a id="id-1.9.3.141.1"></a>

## DROP TRIGGER

DROP TRIGGER — remove a trigger

## Synopsis

```

DROP TRIGGER [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.141.5"></a>

## Description

`DROP TRIGGER` removes an existing
trigger definition. To execute this command, the current
user must be the owner of the table for which the trigger is defined.

<a id="id-1.9.3.141.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the trigger does not exist. A notice is issued
    in this case.

*`name`*
:   The name of the trigger to remove.

*`table_name`*
:   The name (optionally schema-qualified) of the table for which
    the trigger is defined.

`CASCADE`
:   Automatically drop objects that depend on the trigger,
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the trigger if any objects depend on it. This is
    the default.

<a id="SQL-DROPTRIGGER-EXAMPLES"></a>

## Examples

Destroy the trigger `if_dist_exists` on the table
`films`:

```

DROP TRIGGER if_dist_exists ON films;
```

<a id="SQL-DROPTRIGGER-COMPATIBILITY"></a>

## Compatibility

The `DROP TRIGGER` statement in
PostgreSQL is incompatible with the SQL
standard. In the SQL standard, trigger names are not local to
tables, so the command is simply `DROP TRIGGER
name`.

<a id="id-1.9.3.141.9"></a>

## See Also

[CREATE TRIGGER](sql-createtrigger.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptrigger.html)（英文原文，待翻譯）
