# 51.54. pg\_tablespace

The catalog `pg_tablespace` stores information about the available tablespaces. Tables can be placed in particular tablespaces to aid administration of disk layout.

Unlike most system catalogs, `pg_tablespace` is shared across all databases of a cluster: there is only one copy of `pg_tablespace` per cluster, not one per database.

**Table 51.54. `pg_tablespace` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- | --- |
| `oid` | `oid` |   | Row identifier \(hidden attribute; must be explicitly selected\) |
| `spcname` | `name` |   | Tablespace name |
| `spcowner` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | Owner of the tablespace, usually the user who created it |
| `spcacl` | `aclitem[]` |   | Access privileges; see [GRANT](https://www.postgresql.org/docs/10/static/sql-grant.html) and [REVOKE](https://www.postgresql.org/docs/10/static/sql-revoke.html) for details |
| `spcoptions` | `text[]` |   | Tablespace-level options, as “keyword=value” strings |

