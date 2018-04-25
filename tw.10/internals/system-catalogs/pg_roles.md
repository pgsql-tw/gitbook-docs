# 51.81 pg\_roles

The view `pg_roles` provides access to information about database roles. This is simply a publicly readable view of [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html) that blanks out the password field.

This view explicitly exposes the OID column of the underlying table, since that is needed to do joins to other catalogs.

**Table 51.82. `pg_roles` Columns**

| Name | Type | References | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `rolname` | `name` |   | Role name |
| `rolsuper` | `bool` |   | Role has superuser privileges |
| `rolinherit` | `bool` |   | Role automatically inherits privileges of roles it is a member of |
| `rolcreaterole` | `bool` |   | Role can create more roles |
| `rolcreatedb` | `bool` |   | Role can create databases |
| `rolcanlogin` | `bool` |   | Role can log in. That is, this role can be given as the initial session authorization identifier |
| `rolreplication` | `bool` |   | Role is a replication role. A replication role can initiate replication connections and create and drop replication slots. |
| `rolconnlimit` | `int4` |   | For roles that can log in, this sets maximum number of concurrent connections this role can make. -1 means no limit. |
| `rolpassword` | `text` |   | Not the password \(always reads as `********`\) |
| `rolvaliduntil` | `timestamptz` |   | Password expiry time \(only used for password authentication\); null if no expiration |
| `rolbypassrls` | `bool` |   | Role bypasses every row level security policy, see [Section 5.7](https://www.postgresql.org/docs/10/static/ddl-rowsecurity.html) for more information. |
| `rolconfig` | `text[]` |   | Role-specific defaults for run-time configuration variables |
| `oid` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | ID of role |

