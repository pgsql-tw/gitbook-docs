# CREATE FOREIGN TABLE[^1]

CREATE FOREIGN TABLE — define a new foreign table

## Synopsis

```
CREATE FOREIGN TABLE [ IF NOT EXISTS ] 
table_name
 ( [
  { 
column_name
data_type
 [ OPTIONS ( 
option
 '
value
' [, ... ] ) ] [ COLLATE 
collation
 ] [ 
column_constraint
 [ ... ] ]
    | 
table_constraint
 }
    [, ... ]
] )
[ INHERITS ( 
parent_table
 [, ... ] ) ]
  SERVER 
server_name

[ OPTIONS ( 
option
 '
value
' [, ... ] ) ]

CREATE FOREIGN TABLE [ IF NOT EXISTS ] 
table_name

  PARTITION OF 
parent_table
 [ (
  { 
column_name
 [ WITH OPTIONS ] [ 
column_constraint
 [ ... ] ]
    | 
table_constraint
 }
    [, ... ]
) ] 
partition_bound_spec

  SERVER 
server_name

[ OPTIONS ( 
option
 '
value
' [, ... ] ) ]


where 
column_constraint
 is:


[ CONSTRAINT 
constraint_name
 ]
{ NOT NULL |
  NULL |
  CHECK ( 
expression
 ) [ NO INHERIT ] |
  DEFAULT 
default_expr
 }


and 
table_constraint
 is:


[ CONSTRAINT 
constraint_name
 ]
CHECK ( 
expression
 ) [ NO INHERIT ]

```

## Description

`CREATE FOREIGN TABLE`creates a new foreign table in the current database. The table will be owned by the user issuing the command.

If a schema name is given \(for example,`CREATE FOREIGN TABLE myschema.mytable ...`\) then the table is created in the specified schema. Otherwise it is created in the current schema. The name of the foreign table must be distinct from the name of any other foreign table, table, sequence, index, view, or materialized view in the same schema.

`CREATE FOREIGN TABLE`also automatically creates a data type that represents the composite type corresponding to one row of the foreign table. Therefore, foreign tables cannot have the same name as any existing data type in the same schema.

If`PARTITION OF`clause is specified then the table is created as a partition of`parent_table`with specified bounds.

To be able to create a foreign table, you must have`USAGE`privilege on the foreign server, as well as`USAGE`privilege on all column types used in the table.

## Parameters

`IF NOT EXISTS`

Do not throw an error if a relation with the same name already exists. A notice is issued in this case. Note that there is no guarantee that the existing relation is anything like the one that would have been created.

_`table_name`_

The name \(optionally schema-qualified\) of the table to be created.

_`column_name`_

The name of a column to be created in the new table.

_`data_type`_

The data type of the column. This can include array specifiers. For more information on the data types supported byPostgreSQL, refer to[Chapter 8](https://www.postgresql.org/docs/10/static/datatype.html).

`COLLATE`

_`collation`_

The`COLLATE`clause assigns a collation to the column \(which must be of a collatable data type\). If not specified, the column data type's default collation is used.

`INHERITS (`

_`parent_table`_

\[, ... \] \)

The optional`INHERITS`clause specifies a list of tables from which the new foreign table automatically inherits all columns. Parent tables can be plain tables or foreign tables. See the similar form of[CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html)for more details.

`CONSTRAINT`

_`constraint_name`_

An optional name for a column or table constraint. If the constraint is violated, the constraint name is present in error messages, so constraint names like`col must be positive`can be used to communicate helpful constraint information to client applications. \(Double-quotes are needed to specify constraint names that contain spaces.\) If a constraint name is not specified, the system generates a name.

`NOT NULL`

The column is not allowed to contain null values.

`NULL`

The column is allowed to contain null values. This is the default.

This clause is only provided for compatibility with non-standard SQL databases. Its use is discouraged in new applications.

`CHECK (`

_`expression`_

\) \[ NO INHERIT \]

The`CHECK`clause specifies an expression producing a Boolean result which each row in the foreign table is expected to satisfy; that is, the expression should produce TRUE or UNKNOWN, never FALSE, for all rows in the foreign table. A check constraint specified as a column constraint should reference that column's value only, while an expression appearing in a table constraint can reference multiple columns.

Currently,`CHECK`expressions cannot contain subqueries nor refer to variables other than columns of the current row. The system column`tableoid`may be referenced, but not any other system column.

A constraint marked with`NO INHERIT`will not propagate to child tables.

`DEFAULT`

_`default_expr`_

The`DEFAULT`clause assigns a default data value for the column whose column definition it appears within. The value is any variable-free expression \(subqueries and cross-references to other columns in the current table are not allowed\). The data type of the default expression must match the data type of the column.

The default expression will be used in any insert operation that does not specify a value for the column. If there is no default for a column, then the default is null.

_`server_name`_

The name of an existing foreign server to use for the foreign table. For details on defining a server, see[CREATE SERVER](https://www.postgresql.org/docs/10/static/sql-createserver.html).

`OPTIONS (`

_`option`_

'

_`value`_

' \[, ...\] \)

Options to be associated with the new foreign table or one of its columns. The allowed option names and values are specific to each foreign data wrapper and are validated using the foreign-data wrapper's validator function. Duplicate option names are not allowed \(although it's OK for a table option and a column option to have the same name\).

## Notes

Constraints on foreign tables \(such as`CHECK`or`NOT NULL`clauses\) are not enforced by the corePostgreSQLsystem, and most foreign data wrappers do not attempt to enforce them either; that is, the constraint is simply assumed to hold true. There would be little point in such enforcement since it would only apply to rows inserted or updated via the foreign table, and not to rows modified by other means, such as directly on the remote server. Instead, a constraint attached to a foreign table should represent a constraint that is being enforced by the remote server.

Some special-purpose foreign data wrappers might be the only access mechanism for the data they access, and in that case it might be appropriate for the foreign data wrapper itself to perform constraint enforcement. But you should not assume that a wrapper does that unless its documentation says so.

AlthoughPostgreSQLdoes not attempt to enforce constraints on foreign tables, it does assume that they are correct for purposes of query optimization. If there are rows visible in the foreign table that do not satisfy a declared constraint, queries on the table might produce incorrect answers. It is the user's responsibility to ensure that the constraint definition matches reality.

## Examples

Create foreign table`films`, which will be accessed through the server`film_server`:

```
CREATE FOREIGN TABLE films (
    code        char(5) NOT NULL,
    title       varchar(40) NOT NULL,
    did         integer NOT NULL,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute
)
SERVER film_server;

```

Create foreign table`measurement_y2016m07`, which will be accessed through the server`server_07`, as a partition of the range partitioned table`measurement`:

```
CREATE FOREIGN TABLE measurement_y2016m07
    PARTITION OF measurement FOR VALUES FROM ('2016-07-01') TO ('2016-08-01')
    SERVER server_07;

```

## Compatibility

The`CREATE FOREIGN TABLE`command largely conforms to theSQLstandard; however, much as with[`CREATE TABLE`](https://www.postgresql.org/docs/10/static/sql-createtable.html),`NULL`constraints and zero-column foreign tables are permitted. The ability to specify column default values is also aPostgreSQLextension. Table inheritance, in the form defined byPostgreSQL, is nonstandard.

## See Also

[ALTER FOREIGN TABLE](https://www.postgresql.org/docs/10/static/sql-alterforeigntable.html)

,

[DROP FOREIGN TABLE](https://www.postgresql.org/docs/10/static/sql-dropforeigntable.html)

,

[CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html)

,

[CREATE SERVER](https://www.postgresql.org/docs/10/static/sql-createserver.html)

,

[IMPORT FOREIGN SCHEMA](https://www.postgresql.org/docs/10/static/sql-importforeignschema.html)

---



[^1]:  [PostgreSQL: Documentation: 10: CREATE FOREIGN TABLE](https://www.postgresql.org/docs/10/static/sql-createforeigntable.html)

