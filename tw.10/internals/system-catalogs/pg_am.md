# 51.3. pg\_am

The catalog `pg_am` stores information about relation access methods. There is one row for each access method supported by the system. Currently, only indexes have access methods. The requirements for index access methods are discussed in detail in [Chapter 60](https://www.postgresql.org/docs/10/static/indexam.html).

**Table 51.3. `pg_am` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- |
| `oid` | `oid` |   | Row identifier \(hidden attribute; must be explicitly selected\) |
| `amname` | `name` |   | Name of the access method |
| `amhandler` | `regproc` | [`pg_proc`](https://www.postgresql.org/docs/10/static/catalog-pg-proc.html).oid | OID of a handler function that is responsible for supplying information about the access method |
| `amtype` | `char` |   | Currently always `i` to indicate an index access method; other values may be allowed in future |

#### Note

Before PostgreSQL 9.6, `pg_am` contained many additional columns representing properties of index access methods. That data is now only directly visible at the C code level. However,`pg_index_column_has_property()` and related functions have been added to allow SQL queries to inspect index access method properties; see [Table 9.63](https://www.postgresql.org/docs/10/static/functions-info.html#FUNCTIONS-INFO-CATALOG-TABLE).

