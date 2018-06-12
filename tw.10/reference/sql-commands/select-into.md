---
description: 版本：10
---

# SELECT INTO

SELECT INTO — define a new table from the results of a query

### Synopsis

```text
[ WITH [ RECURSIVE ] with_query [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
    * | expression [ [ AS ] output_name ] [, ...]
    INTO [ TEMPORARY | TEMP | UNLOGGED ] [ TABLE ] new_table
    [ FROM from_item [, ...] ]
    [ WHERE condition ]
    [ GROUP BY expression [, ...] ]
    [ HAVING condition [, ...] ]
    [ WINDOW window_name AS ( window_definition ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select ]
    [ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY ]
    [ FOR { UPDATE | SHARE } [ OF table_name [, ...] ] [ NOWAIT ] [...] ]
```

### Description

`SELECT INTO` creates a new table and fills it with data computed by a query. The data is not returned to the client, as it is with a normal `SELECT`. The new table's columns have the names and data types associated with the output columns of the `SELECT`.

### Parameters

`TEMPORARY` or `TEMP`

If specified, the table is created as a temporary table. Refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details.`UNLOGGED`

If specified, the table is created as an unlogged table. Refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details._`new_table`_

The name \(optionally schema-qualified\) of the table to be created.

All other parameters are described in detail under [SELECT](https://www.postgresql.org/docs/10/static/sql-select.html).

### Notes

[CREATE TABLE AS](https://www.postgresql.org/docs/10/static/sql-createtableas.html) is functionally similar to `SELECT INTO`. `CREATE TABLE AS` is the recommended syntax, since this form of `SELECT INTO` is not available in ECPG or PL/pgSQL, because they interpret the `INTO` clause differently. Furthermore, `CREATE TABLE AS` offers a superset of the functionality provided by `SELECT INTO`.

To add OIDs to the table created by `SELECT INTO`, enable the [default\_with\_oids](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#GUC-DEFAULT-WITH-OIDS) configuration variable. Alternatively, `CREATE TABLE AS` can be used with the `WITH OIDS` clause.

### Examples

Create a new table `films_recent` consisting of only recent entries from the table `films`:

```text
SELECT * INTO films_recent FROM films WHERE date_prod >= '2002-01-01';
```

### Compatibility

The SQL standard uses `SELECT INTO` to represent selecting values into scalar variables of a host program, rather than creating a new table. This indeed is the usage found in ECPG \(see [Chapter 35](https://www.postgresql.org/docs/10/static/ecpg.html)\) and PL/pgSQL \(see [Chapter 42](https://www.postgresql.org/docs/10/static/plpgsql.html)\). The PostgreSQL usage of `SELECT INTO` to represent table creation is historical. It is best to use `CREATE TABLE AS` for this purpose in new code.

### See Also

[CREATE TABLE AS](create-table-as.md)

