# 54.25. pg\_shadow

The view `pg_shadow` exists for backwards compatibility: it emulates a catalog that existed in PostgreSQL before version 8.1. It shows properties of all roles that are marked as `rolcanlogin` in [`pg_authid`](../system-catalogs/pg_authid.md).

The name stems from the fact that this table should not be readable by the public since it contains passwords. [`pg_user`](../system-catalogs/pg_user.md) is a publicly readable view on `pg_shadow` that blanks out the password field.

#### **Table 54.25. `pg_shadow` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>usename</code> <code>name</code> (references <a href="../system-catalogs/pg_authid.md"><code>pg_authid</code></a>.<code>rolname</code>)</p><p>User name</p>                                                        |
| <p><code>usesysid</code> <code>oid</code> (references <a href="../system-catalogs/pg_authid.md"><code>pg_authid</code></a>.<code>oid</code>)</p><p>ID of this user</p>                                                      |
| <p><code>usecreatedb</code> <code>bool</code></p><p>User can create databases</p>                                                                                                                                                                          |
| <p><code>usesuper</code> <code>bool</code></p><p>User is a superuser</p>                                                                                                                                                                                   |
| <p><code>userepl</code> <code>bool</code></p><p>User can initiate streaming replication and put the system in and out of backup mode.</p>                                                                                                                  |
| <p><code>usebypassrls</code> <code>bool</code></p><p>User bypasses every row-level security policy, see <a href="../../the-sql-language/ddl/row-security-policies.md">Section 5.8</a> for more information.</p>                                   |
| <p><code>passwd</code> <code>text</code></p><p>Password (possibly encrypted); null if none. See <a href="../system-catalogs/pg_authid.md"><code>pg_authid</code></a> for details of how encrypted passwords are stored.</p> |
| <p><code>valuntil</code> <code>timestamptz</code></p><p>Password expiry time (only used for password authentication)</p>                                                                                                                                   |
| <p><code>useconfig</code> <code>text[]</code></p><p>Session defaults for run-time configuration variables</p>                                                                                                                                              |
