<a id="id-1.9.3.118.1"></a>

## DROP MATERIALIZED VIEW

DROP MATERIALIZED VIEW — remove a materialized view

## Synopsis

```

DROP MATERIALIZED VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.118.5"></a>

## Description

`DROP MATERIALIZED VIEW` drops an existing materialized
view. To execute this command you must be the owner of the materialized
view.

<a id="id-1.9.3.118.6"></a>

## Parameters

`IF EXISTS`
:   Do not throw an error if the materialized view does not exist. A notice
    is issued in this case.

*`name`*
:   The name (optionally schema-qualified) of the materialized view to
    remove.

`CASCADE`
:   Automatically drop objects that depend on the materialized view (such as
    other materialized views, or regular views),
    and in turn all objects that depend on those objects
    (see [Section 5.15](../../the-sql-language/ddl/ddl-depend.md)).

`RESTRICT`
:   Refuse to drop the materialized view if any objects depend on it. This
    is the default.

<a id="id-1.9.3.118.7"></a>

## Examples

This command will remove the materialized view called
`order_summary`:

```

DROP MATERIALIZED VIEW order_summary;
```

<a id="id-1.9.3.118.8"></a>

## Compatibility

`DROP MATERIALIZED VIEW` is a
PostgreSQL extension.

<a id="id-1.9.3.118.9"></a>

## See Also

[CREATE MATERIALIZED VIEW](sql-creatematerializedview.md), [ALTER MATERIALIZED VIEW](sql-altermaterializedview.md), [REFRESH MATERIALIZED VIEW](sql-refreshmaterializedview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropmaterializedview.html)（英文原文，待翻譯）
