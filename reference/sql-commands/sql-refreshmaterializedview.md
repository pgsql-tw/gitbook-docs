<a id="id-1.9.3.162.1"></a>

## REFRESH MATERIALIZED VIEW

REFRESH MATERIALIZED VIEW — replace the contents of a materialized view

## Synopsis

```

REFRESH MATERIALIZED VIEW [ CONCURRENTLY ] name
    [ WITH [ NO ] DATA ]
```

<a id="id-1.9.3.162.5"></a>

## Description

`REFRESH MATERIALIZED VIEW` completely replaces the
contents of a materialized view. To execute this command you must have the
`MAINTAIN`
privilege on the materialized view. The old contents are discarded. If
`WITH DATA` is specified (or defaults) the backing query
is executed to provide the new data, and the materialized view is left in a
scannable state. If `WITH NO DATA` is specified no new
data is generated and the materialized view is left in an unscannable
state.

`CONCURRENTLY` and `WITH NO DATA` may not
be specified together.

<a id="id-1.9.3.162.6"></a>

## Parameters

`CONCURRENTLY`
:   Refresh the materialized view without locking out concurrent selects on
    the materialized view. Without this option a refresh which affects a
    lot of rows will tend to use fewer resources and complete more quickly,
    but could block other connections which are trying to read from the
    materialized view. This option may be faster in cases where a small
    number of rows are affected.

    This option is only allowed if there is at least one
    `UNIQUE` index on the materialized view which uses only
    column names and includes all rows; that is, it must not be an
    expression index or include a `WHERE` clause.

    This option can only be used when the materialized view is already
    populated.

    Even with this option only one `REFRESH` at a time may
    run against any one materialized view.

*`name`*
:   The name (optionally schema-qualified) of the materialized view to
    refresh.

<a id="id-1.9.3.162.7"></a>

## Notes

If there is an `ORDER BY` clause in the materialized
view's defining query, the original contents of the materialized view
will be ordered that way; but `REFRESH MATERIALIZED
VIEW` does not guarantee to preserve that ordering.

While `REFRESH MATERIALIZED VIEW` is running, the [search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) is temporarily changed to `pg_catalog,
pg_temp`.

<a id="id-1.9.3.162.8"></a>

## Examples

This command will replace the contents of the materialized view called
`order_summary` using the query from the materialized
view's definition, and leave it in a scannable state:

```

REFRESH MATERIALIZED VIEW order_summary;
```

This command will free storage associated with the materialized view
`annual_statistics_basis` and leave it in an unscannable
state:

```

REFRESH MATERIALIZED VIEW annual_statistics_basis WITH NO DATA;
```

<a id="id-1.9.3.162.9"></a>

## Compatibility

`REFRESH MATERIALIZED VIEW` is a
PostgreSQL extension.

<a id="id-1.9.3.162.10"></a>

## See Also

[CREATE MATERIALIZED VIEW](sql-creatematerializedview.md), [ALTER MATERIALIZED VIEW](sql-altermaterializedview.md), [DROP MATERIALIZED VIEW](sql-dropmaterializedview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-refreshmaterializedview.html)（英文原文，待翻譯）
