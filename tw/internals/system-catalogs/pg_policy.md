# 52.38. pg\_policy

The catalog `pg_policy` stores row level security policies for tables. A policy includes the kind of command that it applies to \(possibly all commands\), the roles that it applies to, the expression to be added as a security-barrier qualification to queries that include the table, and the expression to be added as a `WITH CHECK` option for queries that attempt to add new records to the table.

**Table 51.38. `pg_policy` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `polname` | `name` |   | The name of the policy |
| `polrelid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | The table to which the policy applies |
| `polcmd` | `char` |   | The command type to which the policy is applied: `r` for `SELECT`, `a` for `INSERT`, `w` for `UPDATE`, `d` for `DELETE`, or `*` for all |
| `polpermissive` | `boolean` |   | Is the policy permissive or restrictive? |
| `polroles` | `oid[]` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | The roles to which the policy is applied |
| `polqual` | `pg_node_tree` |   | The expression tree to be added to the security barrier qualifications for queries that use the table |
| `polwithcheck` | `pg_node_tree` |   | The expression tree to be added to the WITH CHECK qualifications for queries that attempt to add rows to the table |

#### Note

Policies stored in `pg_policy` are applied only when `pg_class`.`relrowsecurity` is set for their table.

