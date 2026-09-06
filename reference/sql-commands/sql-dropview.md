<a id="id-1.9.3.145.1"></a>

## DROP VIEW

DROP VIEW — remove a view

## Synopsis

```

DROP VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.145.5"></a>

## Description

`DROP VIEW` drops an existing view. To execute
this command you must be the owner of the view.

<a id="id-1.9.3.145.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the view does not exist. A notice is issued
    in this case.

*`name`*
:   The name (optionally schema-qualified) of the view to remove.

`CASCADE`
:   Automatically drop objects that depend on the view (such as
    other views),
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the view if any objects depend on it. This is
    the default.

<a id="id-1.9.3.145.7"></a>

## Examples

This command will remove the view called `kinds`:

```

DROP VIEW kinds;
```

<a id="id-1.9.3.145.8"></a>

## Compatibility

This command conforms to the SQL standard, except that the standard only
allows one view to be dropped per command, and apart from the
`IF EXISTS` option, which is a PostgreSQL
extension.

<a id="id-1.9.3.145.9"></a>

## See Also

[ALTER VIEW](sql-alterview.md), [CREATE VIEW](sql-createview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropview.html)（英文原文，待翻譯）
