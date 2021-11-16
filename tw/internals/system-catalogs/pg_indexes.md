# 51.72. pg\_indexes

檢視表 pg\_indexes 提供資料庫中每一個索引的資訊。

#### **Table 51.73. `pg_indexes` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>schemaname</code> <code>name</code> (references <a href="pg_namespace.md"><code>pg_namespace</code></a>.<code>nspname</code>)</p><p>Name of schema containing table and index</p>                                   |
| <p><code>tablename</code> <code>name</code> (references <a href="pg_class.md"><code>pg_class</code></a>.<code>relname</code>)</p><p>Name of table the index is for</p>                                                       |
| <p><code>indexname</code> <code>name</code> (references <a href="pg_class.md"><code>pg_class</code></a>.<code>relname</code>)</p><p>Name of index</p>                                                                        |
| <p><code>tablespace</code> <code>name</code> (references <a href="51.54.-pg_tablespace.md"><code>pg_tablespace</code></a>.<code>spcname</code>)</p><p>Name of tablespace containing index (null if default for database)</p> |
| <p><code>indexdef</code> <code>text</code></p><p>Index definition (a reconstructed <code>CREATE INDEX</code> command)</p>                                                                                                    |
