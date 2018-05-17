# CREATE TABLE AS

CREATE TABLE AS — define a new table from the results of a query

### Synopsis

```text
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ WITH ( storage_parameter [= value] [, ... ] ) | WITH OIDS | WITHOUT OIDS ]
    [ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]
```

### Description

`CREATE TABLE AS` creates a table and fills it with data computed by a `SELECT` command. The table columns have the names and data types associated with the output columns of the `SELECT` \(except that you can override the column names by giving an explicit list of new column names\).

`CREATE TABLE AS` bears some resemblance to creating a view, but it is really quite different: it creates a new table and evaluates the query just once to fill the new table initially. The new table will not track subsequent changes to the source tables of the query. In contrast, a view re-evaluates its defining `SELECT` statement whenever it is queried.

### Parameters

`GLOBAL` or `LOCAL`

Ignored for compatibility. Use of these keywords is deprecated; refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details.

`TEMPORARY` or `TEMP`

If specified, the table is created as a temporary table. Refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details.

`UNLOGGED`

If specified, the table is created as an unlogged table. Refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details.

`IF NOT EXISTS`

Do not throw an error if a relation with the same name already exists. A notice is issued in this case. Refer to [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details._`table_name`_

The name \(optionally schema-qualified\) of the table to be created.

_`column_name`_

The name of a column in the new table. If column names are not provided, they are taken from the output column names of the query.

`WITH (` _`storage_parameter`_ \[= _`value`_\] \[, ... \] \)

This clause specifies optional storage parameters for the new table; see [Storage Parameters](https://www.postgresql.org/docs/10/static/sql-createtable.html#SQL-CREATETABLE-STORAGE-PARAMETERS) for more information. The `WITH` clause can also include `OIDS=TRUE` \(or just `OIDS`\) to specify that rows of the new table should have OIDs \(object identifiers\) assigned to them, or `OIDS=FALSE` to specify that the rows should not have OIDs. See [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for more information.

`WITH OIDS`  
`WITHOUT OIDS`

These are obsolescent syntaxes equivalent to `WITH (OIDS)` and `WITH (OIDS=FALSE)`, respectively. If you wish to give both an `OIDS` setting and storage parameters, you must use the `WITH ( ... )` syntax; see above.

`ON COMMIT`

The behavior of temporary tables at the end of a transaction block can be controlled using `ON COMMIT`. The three options are:

`PRESERVE ROWS`

No special action is taken at the ends of transactions. This is the default behavior.

`DELETE ROWS`

All rows in the temporary table will be deleted at the end of each transaction block. Essentially, an automatic [TRUNCATE](https://www.postgresql.org/docs/10/static/sql-truncate.html) is done at each commit.

`DROP`

The temporary table will be dropped at the end of the current transaction block.`TABLESPACE` _`tablespace_name`_

The _`tablespace_name`_ is the name of the tablespace in which the new table is to be created. If not specified, [default\_tablespace](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-DEFAULT-TABLESPACE) is consulted, or [temp\_tablespaces](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TEMP-TABLESPACES) if the table is temporary.

_`query`_

A [SELECT](https://www.postgresql.org/docs/10/static/sql-select.html), [TABLE](https://www.postgresql.org/docs/10/static/sql-select.html#SQL-TABLE), or [VALUES](https://www.postgresql.org/docs/10/static/sql-values.html) command, or an [EXECUTE](https://www.postgresql.org/docs/10/static/sql-execute.html) command that runs a prepared `SELECT`, `TABLE`, or `VALUES` query.

`WITH [ NO ] DATA`

This clause specifies whether or not the data produced by the query should be copied into the new table. If not, only the table structure is copied. The default is to copy the data.

### Notes

This command is functionally similar to [SELECT INTO](https://www.postgresql.org/docs/10/static/sql-selectinto.html), but it is preferred since it is less likely to be confused with other uses of the `SELECT INTO` syntax. Furthermore, `CREATE TABLE AS` offers a superset of the functionality offered by `SELECT INTO`.

The `CREATE TABLE AS` command allows the user to explicitly specify whether OIDs should be included. If the presence of OIDs is not explicitly specified, the [default\_with\_oids](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#GUC-DEFAULT-WITH-OIDS) configuration variable is used.

### Examples

Create a new table `films_recent` consisting of only recent entries from the table `films`:

```text
CREATE TABLE films_recent AS
  SELECT * FROM films WHERE date_prod >= '2002-01-01';
```

To copy a table completely, the short form using the `TABLE` command can also be used:

```text
CREATE TABLE films2 AS
  TABLE films;
```

Create a new temporary table `films_recent`, consisting of only recent entries from the table `films`, using a prepared statement. The new table has OIDs and will be dropped at commit:

```text
PREPARE recentfilms(date) AS
  SELECT * FROM films WHERE date_prod > $1;
CREATE TEMP TABLE films_recent WITH (OIDS) ON COMMIT DROP AS
  EXECUTE recentfilms('2002-01-01');
```

### Compatibility

`CREATE TABLE AS` conforms to the SQL standard. The following are nonstandard extensions:

* The standard requires parentheses around the subquery clause; in PostgreSQL, these parentheses are optional.
* In the standard, the `WITH [ NO ] DATA` clause is required; in PostgreSQL it is optional.
* PostgreSQL handles temporary tables in a way rather different from the standard; see [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) for details.
* The `WITH` clause is a PostgreSQL extension; neither storage parameters nor OIDs are in the standard.
* The PostgreSQL concept of tablespaces is not part of the standard. Hence, the clause `TABLESPACE` is an extension.

### See Also

[CREATE MATERIALIZED VIEW](create-materialized-view.md), [CREATE TABLE](create-table.md), [EXECUTE](https://www.postgresql.org/docs/10/static/sql-execute.html), [SELECT](select.md), [SELECT INTO](https://www.postgresql.org/docs/10/static/sql-selectinto.html), [VALUES](values.md)

