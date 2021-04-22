# 51.90. pg\_tables

The view `pg_tables` provides access to useful information about each table in the database.

## **Table 51.91. `pg_tables` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `schemaname` | `name` | [`pg_namespace`](https://www.postgresql.org/docs/12/catalog-pg-namespace.html).nspname | Name of schema containing table |
| `tablename` | `name` | [`pg_class`](https://www.postgresql.org/docs/12/catalog-pg-class.html).relname | Name of table |
| `tableowner` | `name` | [`pg_authid`](https://www.postgresql.org/docs/12/catalog-pg-authid.html).rolname | Name of table's owner |
| `tablespace` | `name` | [`pg_tablespace`](https://www.postgresql.org/docs/12/catalog-pg-tablespace.html).spcname | Name of tablespace containing table \(null if default for database\) |
| `hasindexes` | `boolean` | [`pg_class`](https://www.postgresql.org/docs/12/catalog-pg-class.html).relhasindex | True if table has \(or recently had\) any indexes |
| `hasrules` | `boolean` | [`pg_class`](https://www.postgresql.org/docs/12/catalog-pg-class.html).relhasrules | True if table has \(or once had\) rules |
| `hastriggers` | `boolean` | [`pg_class`](https://www.postgresql.org/docs/12/catalog-pg-class.html).relhastriggers | True if table has \(or once had\) triggers |
| `rowsecurity` | `boolean` | [`pg_class`](https://www.postgresql.org/docs/12/catalog-pg-class.html).relrowsecurity | True if row security is enabled on the table |

