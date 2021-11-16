# 51.52. pg\_subscription

目錄 pg\_subscription 包含所有現有訂閱的邏輯複寫。有關邏輯複寫的相關資訊，請參閱[第 30 章](../../server-administration/logical-replication/)。

與大多數系統目錄不同，pg\_subscription 在叢集的所有資料庫之間是共享的：每個叢集只有一個 pg\_subscription，而不是每個資料庫一個。

普通使用者沒有權限讀取 subconninfo 欄位，因為該欄位可能包含純文字密碼。

#### **Table 51.52. `pg_subscription` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>oid</code> <code>oid</code></p><p>Row identifier</p>                                                                                                                                                                                                                                   |
| <p><code>subdbid</code> <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-database.html"><code>pg_database</code></a>.<code>oid</code>)</p><p>OID of the database which the subscription resides in</p>                                                       |
| <p><code>subname</code> <code>name</code></p><p>Name of the subscription</p>                                                                                                                                                                                                                    |
| <p><code>subowner</code> <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-authid.html"><code>pg_authid</code></a>.<code>oid</code>)</p><p>Owner of the subscription</p>                                                                                      |
| <p><code>subenabled</code> <code>bool</code></p><p>If true, the subscription is enabled and should be replicating.</p>                                                                                                                                                                          |
| <p><code>subconninfo</code> <code>text</code></p><p>Connection string to the upstream database</p>                                                                                                                                                                                              |
| <p><code>subslotname</code> <code>name</code></p><p>Name of the replication slot in the upstream database (also used for the local replication origin name); null represents <code>NONE</code></p>                                                                                              |
| <p><code>subsynccommit</code> <code>text</code></p><p>Contains the value of the <code>synchronous_commit</code> setting for the subscription workers.</p>                                                                                                                                       |
| <p><code>subpublications</code> <code>text[]</code></p><p>Array of subscribed publication names. These reference the publications on the publisher server. For more on publications see <a href="https://www.postgresql.org/docs/13/logical-replication-publication.html">Section 30.1</a>.</p> |
