# 51.32. pg\_namespace

The catalog `pg_namespace` stores namespaces. A namespace is the structure underlying SQL schemas: each namespace can have a separate collection of relations, types, etc. without name conflicts.

**Table 51.32. `pg_namespace` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- |
| `oid` | `oid` |   | Row identifier \(hidden attribute; must be explicitly selected\) |
| `nspname` | `name` |   | Name of the namespace |
| `nspowner` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | Owner of the namespace |
| `nspacl` | `aclitem[]` |   | Access privileges; see [GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html) and [REVOKE](https://www.postgresql.org/docs/10/static/sql-revoke.html) for details |

