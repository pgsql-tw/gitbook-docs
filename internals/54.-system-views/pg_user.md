# 54.33. pg\_user

The view `pg_user` provides access to information about database users. This is simply a publicly readable view of [`pg_shadow`](https://www.postgresql.org/docs/current/view-pg-shadow.html) that blanks out the password field.

#### **Table 54.33. `pg_user` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p><code>usename</code> <code>name</code></p><p>User name</p>                                                                                                                                                            |
| <p><code>usesysid</code> <code>oid</code></p><p>ID of this user</p>                                                                                                                                                      |
| <p><code>usecreatedb</code> <code>bool</code></p><p>User can create databases</p>                                                                                                                                        |
| <p><code>usesuper</code> <code>bool</code></p><p>User is a superuser</p>                                                                                                                                                 |
| <p><code>userepl</code> <code>bool</code></p><p>User can initiate streaming replication and put the system in and out of backup mode.</p>                                                                                |
| <p><code>usebypassrls</code> <code>bool</code></p><p>User bypasses every row-level security policy, see <a href="https://www.postgresql.org/docs/current/ddl-rowsecurity.html">Section 5.8</a> for more information.</p> |
| <p><code>passwd</code> <code>text</code></p><p>Not the password (always reads as <code>********</code>)</p>                                                                                                              |
| <p><code>valuntil</code> <code>timestamptz</code></p><p>Password expiry time (only used for password authentication)</p>                                                                                                 |
| <p><code>useconfig</code> <code>text[]</code></p><p>Session defaults for run-time configuration variables</p>                                                                                                            |
