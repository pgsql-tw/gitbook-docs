# 54.30. pg\_tables

The view `pg_tables` provides access to useful information about each table in the database.

#### **Table 54.30. `pg_tables` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>schemaname</code> <code>name</code> (references <a href="https://www.postgresql.org/docs/current/catalog-pg-namespace.html"><code>pg_namespace</code></a>.<code>nspname</code>)</p><p>Name of schema containing table</p>                                      |
| <p><code>tablename</code> <code>name</code> (references <a href="https://www.postgresql.org/docs/current/catalog-pg-class.html"><code>pg_class</code></a>.<code>relname</code>)</p><p>Name of table</p>                                                                 |
| <p><code>tableowner</code> <code>name</code> (references <a href="https://www.postgresql.org/docs/current/catalog-pg-authid.html"><code>pg_authid</code></a>.<code>rolname</code>)</p><p>Name of table's owner</p>                                                      |
| <p><code>tablespace</code> <code>name</code> (references <a href="https://www.postgresql.org/docs/current/catalog-pg-tablespace.html"><code>pg_tablespace</code></a>.<code>spcname</code>)</p><p>Name of tablespace containing table (null if default for database)</p> |
| <p><code>hasindexes</code> <code>bool</code> (references <a href="https://www.postgresql.org/docs/current/catalog-pg-class.html"><code>pg_class</code></a>.<code>relhasindex</code>)</p><p>True if table has (or recently had) any indexes</p>                          |
| <p><code>hasrules</code> <code>bool</code> (references <a href="https://www.postgresql.org/docs/current/catalog-pg-class.html"><code>pg_class</code></a>.<code>relhasrules</code>)</p><p>True if table has (or once had) rules</p>                                      |
| <p><code>hastriggers</code> <code>bool</code> (references <a href="https://www.postgresql.org/docs/current/catalog-pg-class.html"><code>pg_class</code></a>.<code>relhastriggers</code>)</p><p>True if table has (or once had) triggers</p>                             |
| <p><code>rowsecurity</code> <code>bool</code> (references <a href="https://www.postgresql.org/docs/current/catalog-pg-class.html"><code>pg_class</code></a>.<code>relrowsecurity</code>)</p><p>True if row security is enabled on the table</p>                         |
