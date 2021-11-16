---
description: 版本：11
---

# 51.32. pg\_namespace

The catalog `pg_namespace` stores namespaces. A namespace is the structure underlying SQL schemas: each namespace can have a separate collection of relations, types, etc. without name conflicts.

#### **Table 51.32. `pg_namespace` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>oid</code> <code>oid</code></p><p>Row identifier</p>                                                                                              |
| <p><code>nspname</code> <code>name</code></p><p>Name of the namespace</p>                                                                                  |
| <p><code>nspowner</code> <code>oid</code> (references <a href="pg_authid.md"><code>pg_authid</code></a>.<code>oid</code>)</p><p>Owner of the namespace</p> |
| <p><code>nspacl</code> <code>aclitem[]</code></p><p>存取權限； 詳見 <a href="../../the-sql-language/ddl/privileges.md">5.7 節</a></p>                              |
