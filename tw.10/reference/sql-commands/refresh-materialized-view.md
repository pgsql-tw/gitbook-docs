# REFRESH MATERIALIZED VIEW

REFRESH MATERIALIZED VIEW — replace the contents of a materialized view

### Synopsis

```text
REFRESH MATERIALIZED VIEW [ CONCURRENTLY ] name
    [ WITH [ NO ] DATA ]
```

### Description

`REFRESH MATERIALIZED VIEW` completely replaces the contents of a materialized view. The old contents are discarded. If `WITH DATA` is specified \(or defaults\) the backing query is executed to provide the new data, and the materialized view is left in a scannable state. If `WITH NO DATA` is specified no new data is generated and the materialized view is left in an unscannable state.

`CONCURRENTLY` and `WITH NO DATA` may not be specified together.

### Parameters

`CONCURRENTLY`

Refresh the materialized view without locking out concurrent selects on the materialized view. Without this option a refresh which affects a lot of rows will tend to use fewer resources and complete more quickly, but could block other connections which are trying to read from the materialized view. This option may be faster in cases where a small number of rows are affected.

This option is only allowed if there is at least one `UNIQUE` index on the materialized view which uses only column names and includes all rows; that is, it must not index on any expressions nor include a `WHERE` clause.

This option may not be used when the materialized view is not already populated.

Even with this option only one `REFRESH` at a time may run against any one materialized view.

_`name`_

The name \(optionally schema-qualified\) of the materialized view to refresh.

### Notes

While the default index for future [CLUSTER](https://www.postgresql.org/docs/10/static/sql-cluster.html) operations is retained, `REFRESH MATERIALIZED VIEW` does not order the generated rows based on this property. If you want the data to be ordered upon generation, you must use an `ORDER BY` clause in the backing query.

### Examples

This command will replace the contents of the materialized view called `order_summary` using the query from the materialized view's definition, and leave it in a scannable state:

```text
REFRESH MATERIALIZED VIEW order_summary;
```

This command will free storage associated with the materialized view `annual_statistics_basis` and leave it in an unscannable state:

```text
REFRESH MATERIALIZED VIEW annual_statistics_basis WITH NO DATA;
```

### Compatibility

`REFRESH MATERIALIZED VIEW` is a PostgreSQL extension.

### See Also

[CREATE MATERIALIZED VIE](create-materialized-view.md)W, [ALTER MATERIALIZED VIEW](alter-materialized-view.md), [DROP MATERIALIZED VIEW](drop-materialized-view.md)

