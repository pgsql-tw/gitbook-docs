# 51.9. pg\_auth\_members

The catalog `pg_auth_members` shows the membership relations between roles. Any non-circular set of relationships is allowed.

Because user identities are cluster-wide, `pg_auth_members` is shared across all databases of a cluster: there is only one copy of `pg_auth_members` per cluster, not one per database.

**Table 51.9. `pg_auth_members` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- |
| `roleid` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | ID of a role that has a member |
| `member` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | ID of a role that is a member of `roleid` |
| `grantor` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | ID of the role that granted this membership |
| `admin_option` | `bool` |   | True if `member` can grant membership in `roleid` to others |

