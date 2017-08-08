# IMPORT FOREIGN SCHEMA[^1]

IMPORT FOREIGN SCHEMA — import table definitions from a foreign server

## Synopsis

```
IMPORT FOREIGN SCHEMA 
remote_schema

    [ { LIMIT TO | EXCEPT } ( 
table_name
 [, ...] ) ]
    FROM SERVER 
server_name

    INTO 
local_schema

    [ OPTIONS ( 
option
 '
value
' [, ... ] ) ]

```

## Description

`IMPORT FOREIGN SCHEMA`creates foreign tables that represent tables existing on a foreign server. The new foreign tables will be owned by the user issuing the command and are created with the correct column definitions and options to match the remote tables.

By default, all tables and views existing in a particular schema on the foreign server are imported. Optionally, the list of tables can be limited to a specified subset, or specific tables can be excluded. The new foreign tables are all created in the target schema, which must already exist.

To use`IMPORT FOREIGN SCHEMA`, the user must have`USAGE`privilege on the foreign server, as well as`CREATE`privilege on the target schema.

## Parameters

_`remote_schema`_

The remote schema to import from. The specific meaning of a remote schema depends on the foreign data wrapper in use.

`LIMIT TO (`

_`table_name`_

\[, ...\] \)

Import only foreign tables matching one of the given table names. Other tables existing in the foreign schema will be ignored.

`EXCEPT (`

_`table_name`_

\[, ...\] \)

Exclude specified foreign tables from the import. All tables existing in the foreign schema will be imported except the ones listed here.

_`server_name`_

The foreign server to import from.

_`local_schema`_

The schema in which the imported foreign tables will be created.

`OPTIONS (`

_`option`_

'

_`value`_

' \[, ...\] \)

Options to be used during the import. The allowed option names and values are specific to each foreign data wrapper.

## Examples

Import table definitions from a remote schema`foreign_films`on server`film_server`, creating the foreign tables in local schema`films`:

```
IMPORT FOREIGN SCHEMA foreign_films
    FROM SERVER film_server INTO films;

```

As above, but import only the two tables`actors`and`directors`\(if they exist\):

```
IMPORT FOREIGN SCHEMA foreign_films LIMIT TO (actors, directors)
    FROM SERVER film_server INTO films;

```

## Compatibility

The`IMPORT FOREIGN SCHEMA`command conforms to theSQLstandard, except that the`OPTIONS`clause is aPostgreSQLextension.

## See Also

[CREATE FOREIGN TABLE](https://www.postgresql.org/docs/10/static/sql-createforeigntable.html)

,

[CREATE SERVER](https://www.postgresql.org/docs/10/static/sql-createserver.html)

---



[^1]:  [PostgreSQL: Documentation: 10: IMPORT FOREIGN SCHEMA](https://www.postgresql.org/docs/10/static/sql-importforeignschema.html)

