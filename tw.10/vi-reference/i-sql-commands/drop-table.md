# DROP TABLE[^1]

DROP TABLE — remove a table

## Synopsis

```
DROP TABLE [ IF EXISTS ] 
name
 [, ...] [ CASCADE | RESTRICT ]

```

## Description

`DROP TABLE`removes tables from the database. Only the table owner, the schema owner, and superuser can drop a table. To empty a table of rows without destroying the table, use[DELETE](https://www.postgresql.org/docs/10/static/sql-delete.html)or[TRUNCATE](https://www.postgresql.org/docs/10/static/sql-truncate.html).

`DROP TABLE`always removes any indexes, rules, triggers, and constraints that exist for the target table. However, to drop a table that is referenced by a view or a foreign-key constraint of another table,`CASCADE`must be specified. \(`CASCADE`will remove a dependent view entirely, but in the foreign-key case it will only remove the foreign-key constraint, not the other table entirely.\)

## Parameters

`IF EXISTS`

Do not throw an error if the table does not exist. A notice is issued in this case.

_`name`_

The name \(optionally schema-qualified\) of the table to drop.

`CASCADE`

Automatically drop objects that depend on the table \(such as views\), and in turn all objects that depend on those objects \(see[Section 5.13](https://www.postgresql.org/docs/10/static/ddl-depend.html)\).

`RESTRICT`

Refuse to drop the table if any objects depend on it. This is the default.

## Examples

To destroy two tables,`films`and`distributors`:

```
DROP TABLE films, distributors;

```

## Compatibility

This command conforms to the SQL standard, except that the standard only allows one table to be dropped per command, and apart from the`IF EXISTS`option, which is aPostgreSQLextension.

## See Also

[ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html)

,

[CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html)

[^1]:  [PostgreSQL: Documentation: 10: DROP TABLE](https://www.postgresql.org/docs/10/static/sql-droptable.html)

