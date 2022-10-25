# 51.95. pg\_views

檢視表 pg\_views 提供對資料庫中每個檢視表的詳細資訊。

#### **Table 51.96. `pg_views` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>schemaname</code> <code>name</code> (references <a href="pg_namespace.md"><code>pg_namespace</code></a>.<code>nspname</code>)</p><p>檢視表的綱要名稱</p> |
| <p><code>viewname</code> <code>name</code> (references <a href="pg_class.md"><code>pg_class</code></a>.<code>relname</code>)</p><p>檢視表名稱</p>              |
| <p><code>viewowner</code> <code>name</code> (references <a href="pg_authid.md"><code>pg_authid</code></a>.<code>rolname</code>)</p><p>檢視圖的擁有者名稱</p>       |
| <p><code>definition</code> <code>text</code></p><p>檢視表的定義（重新建構的 SELECT 查詢）</p>                                                                            |
