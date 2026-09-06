# 54.35. pg\_views

The view `pg_views` provides access to useful information about each view in the database.

#### **Table 54.35. `pg_views` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>schemaname</code> <code>name</code> (references <a href="https://www.postgresql.org/docs/15/catalog-pg-namespace.html"><code>pg_namespace</code></a>.<code>nspname</code>)</p><p>Name of schema containing view</p> |
| <p><code>viewname</code> <code>name</code> (references <a href="https://www.postgresql.org/docs/15/catalog-pg-class.html"><code>pg_class</code></a>.<code>relname</code>)</p><p>Name of view</p>                             |
| <p><code>viewowner</code> <code>name</code> (references <a href="https://www.postgresql.org/docs/15/catalog-pg-authid.html"><code>pg_authid</code></a>.<code>rolname</code>)</p><p>Name of view's owner</p>                  |
| <p><code>definition</code> <code>text</code></p><p>View definition (a reconstructed <a href="https://www.postgresql.org/docs/15/sql-select.html">SELECT</a> query)</p>                                                       |
