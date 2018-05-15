# DROP MATERIALIZED VIEW

DROP MATERIALIZED VIEW — remove a materialized view

### Synopsis

```text
DROP MATERIALIZED VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

### Description

`DROP MATERIALIZED VIEW` drops an existing materialized view. To execute this command you must be the owner of the materialized view.

### Parameters

`IF EXISTS`

Do not throw an error if the materialized view does not exist. A notice is issued in this case.

_`name`_

The name \(optionally schema-qualified\) of the materialized view to remove.

`CASCADE`

Automatically drop objects that depend on the materialized view \(such as other materialized views, or regular views\), and in turn all objects that depend on those objects \(see [Section 5.13](https://www.postgresql.org/docs/10/static/ddl-depend.html)\).

`RESTRICT`

Refuse to drop the materialized view if any objects depend on it. This is the default.

### Examples

This command will remove the materialized view called `order_summary`:

```text
DROP MATERIALIZED VIEW order_summary;
```

### Compatibility

`DROP MATERIALIZED VIEW` is a PostgreSQL extension.

### See Also

[CREATE MATERIALIZED VIEW](create-materialized-view.md), [ALTER MATERIALIZED VIEW](alter-materialized-view.md), [REFRESH MATERIALIZED VIEW](https://www.postgresql.org/docs/10/static/sql-refreshmaterializedview.html)

