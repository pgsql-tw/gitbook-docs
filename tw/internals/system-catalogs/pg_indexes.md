# 51.73. pg\_indexes

The view `pg_indexes` provides access to useful information about each index in the database.

#### **Table 51.74. `pg_indexes` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `schemaname` | `name` | [`pg_namespace`](https://www.postgresql.org/docs/12/catalog-pg-namespace.html).nspname | Name of schema containing table and index |
| `tablename` | `name` | [`pg_class`](https://www.postgresql.org/docs/12/catalog-pg-class.html).relname | Name of table the index is for |
| `indexname` | `name` | [`pg_class`](https://www.postgresql.org/docs/12/catalog-pg-class.html).relname | Name of index |
| `tablespace` | `name` | [`pg_tablespace`](https://www.postgresql.org/docs/12/catalog-pg-tablespace.html).spcname | Name of tablespace containing index \(null if default for database\) |
| `indexdef` | `text` |  | Index definition \(a reconstructed `CREATE INDEX` command\) |

