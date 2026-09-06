<a id="id-1.9.3.71.1"></a>

## CREATE MATERIALIZED VIEW

CREATE MATERIALIZED VIEW — define a new materialized view

## Synopsis

```

CREATE MATERIALIZED VIEW [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ USING method ]
    [ WITH ( storage_parameter [= value] [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]
```

<a id="id-1.9.3.71.5"></a>

## Description

`CREATE MATERIALIZED VIEW` defines a materialized view of
a query. The query is executed and used to populate the view at the time
the command is issued (unless `WITH NO DATA` is used) and may be
refreshed later using `REFRESH MATERIALIZED VIEW`.

`CREATE MATERIALIZED VIEW` is similar to
`CREATE TABLE AS`, except that it also remembers the query used
to initialize the view, so that it can be refreshed later upon demand.
A materialized view has many of the same properties as a table, but there
is no support for temporary materialized views.

`CREATE MATERIALIZED VIEW` requires
`CREATE` privilege on the schema used for the materialized
view.

<a id="id-1.9.3.71.6"></a>

## Parameters

`IF NOT EXISTS`
:   Do not throw an error if a materialized view with the same name already
    exists. A notice is issued in this case. Note that there is no guarantee
    that the existing materialized view is anything like the one that would
    have been created.

*`table_name`*
:   The name (optionally schema-qualified) of the materialized view to be
    created. The name must be distinct from the name of any other relation
    (table, sequence, index, view, materialized view, or foreign table) in
    the same schema.

*`column_name`*
:   The name of a column in the new materialized view. If column names are
    not provided, they are taken from the output column names of the query.

`USING method`
:   This optional clause specifies the table access method to use to store
    the contents for the new materialized view; the method needs be an
    access method of type `TABLE`. See [Chapter 62](../../internals/tableam/README.md) for more information. If this option is not
    specified, the default table access method is chosen for the new
    materialized view. See [default_table_access_method](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD)
    for more information.

`WITH ( storage_parameter [= value] [, ... ] )`
:   This clause specifies optional storage parameters for the new
    materialized view; see
    [Storage Parameters](sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS) in the
    [CREATE TABLE](sql-createtable.md) documentation for more
    information. All parameters supported for `CREATE
    TABLE` are also supported for `CREATE MATERIALIZED
    VIEW`.
    See [CREATE TABLE](sql-createtable.md) for more information.

`TABLESPACE tablespace_name`
:   The *`tablespace_name`* is the name
    of the tablespace in which the new materialized view is to be created.
    If not specified, [default_tablespace](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLESPACE) is consulted.

*`query`*
:   A [`SELECT`](sql-select.md), [`TABLE`](sql-select.md#SQL-TABLE),
    or [`VALUES`](sql-values.md) command. This query will run within a
    security-restricted operation; in particular, calls to functions that
    themselves create temporary tables will fail. Also, while the query is
    running, the [search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) is temporarily changed to
    `pg_catalog, pg_temp`.

`WITH [ NO ] DATA`
:   This clause specifies whether or not the materialized view should be
    populated at creation time. If not, the materialized view will be
    flagged as unscannable and cannot be queried until `REFRESH
    MATERIALIZED VIEW` is used.

<a id="id-1.9.3.71.7"></a>

## Compatibility

`CREATE MATERIALIZED VIEW` is a
PostgreSQL extension.

<a id="id-1.9.3.71.8"></a>

## See Also

[ALTER MATERIALIZED VIEW](sql-altermaterializedview.md), [CREATE TABLE AS](sql-createtableas.md), [CREATE VIEW](sql-createview.md), [DROP MATERIALIZED VIEW](sql-dropmaterializedview.md), [REFRESH MATERIALIZED VIEW](sql-refreshmaterializedview.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-creatematerializedview.html)（英文原文，待翻譯）
