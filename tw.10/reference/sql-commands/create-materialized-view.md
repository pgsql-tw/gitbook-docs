# CREATE MATERIALIZED VIEW

CREATE MATERIALIZED VIEW — define a new materialized view

### Synopsis

```text
CREATE MATERIALIZED VIEW [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ WITH ( storage_parameter [= value] [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]
```

### Description

`CREATE MATERIALIZED VIEW` defines a materialized view of a query. The query is executed and used to populate the view at the time the command is issued \(unless `WITH NO DATA`is used\) and may be refreshed later using `REFRESH MATERIALIZED VIEW`.

`CREATE MATERIALIZED VIEW` is similar to `CREATE TABLE AS`, except that it also remembers the query used to initialize the view, so that it can be refreshed later upon demand. A materialized view has many of the same properties as a table, but there is no support for temporary materialized views or automatic generation of OIDs.

### Parameters

`IF NOT EXISTS`

Do not throw an error if a materialized view with the same name already exists. A notice is issued in this case. Note that there is no guarantee that the existing materialized view is anything like the one that would have been created.

_`table_name`_

The name \(optionally schema-qualified\) of the materialized view to be created.

_`column_name`_

The name of a column in the new materialized view. If column names are not provided, they are taken from the output column names of the query.

`WITH ( `_`storage_parameter`_ \[= _`value`_\] \[, ... \] \)

This clause specifies optional storage parameters for the new materialized view; see [Storage Parameters](https://www.postgresql.org/docs/10/static/sql-createtable.html#SQL-CREATETABLE-STORAGE-PARAMETERS) for more information. All parameters supported for `CREATE TABLE`are also supported for `CREATE MATERIALIZED VIEW` with the exception of `OIDS`. See [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for more information.

`TABLESPACE `_`tablespace_name`_

The _`tablespace_name`_ is the name of the tablespace in which the new materialized view is to be created. If not specified, [default\_tablespace](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DEFAULT-TABLESPACE) is consulted.

_`query`_

A [SELECT](https://www.postgresql.org/docs/10/static/sql-select.html), [TABLE](https://www.postgresql.org/docs/10/static/sql-select.html#SQL-TABLE), or [VALUES](https://www.postgresql.org/docs/10/static/sql-values.html) command. This query will run within a security-restricted operation; in particular, calls to functions that themselves create temporary tables will fail.

`WITH [ NO ] DATA`

This clause specifies whether or not the materialized view should be populated at creation time. If not, the materialized view will be flagged as unscannable and cannot be queried until `REFRESH MATERIALIZED VIEW` is used.

### Compatibility

`CREATE MATERIALIZED VIEW` is a PostgreSQL extension.

### See Also

[ALTER MATERIALIZED VIEW](https://www.postgresql.org/docs/10/static/sql-altermaterializedview.html), [CREATE TABLE AS](https://www.postgresql.org/docs/10/static/sql-createtableas.html), [CREATE VIEW](https://www.postgresql.org/docs/10/static/sql-createview.html), [DROP MATERIALIZED VIEW](https://www.postgresql.org/docs/10/static/sql-dropmaterializedview.html), [REFRESH MATERIALIZED VIEW](https://www.postgresql.org/docs/10/static/sql-refreshmaterializedview.html)

