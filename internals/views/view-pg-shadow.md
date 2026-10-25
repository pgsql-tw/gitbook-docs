<a id="VIEW-PG-SHADOW"></a>

## 53.26. `pg_shadow` [#](#view-pg-shadow) <a href="#view-pg-shadow" id="view-pg-shadow"></a>

<a id="id-1.10.5.30.2"></a>

檢視表 `pg_shadow` 為了向後相容性而存在：它模擬 PostgreSQL 8.1 版之前存在的一個系統目錄。它顯示 [`pg_authid`](../catalogs/catalog-pg-authid.md) 中所有標記為 `rolcanlogin` 之角色的屬性。

這個名稱源自於此資料表因為包含密碼，而不應讓大眾讀取。[`pg_user`](view-pg-user.md) 是建立在 `pg_shadow` 之上、公開可讀的檢視表，並將密碼欄位遮蔽為空白。

<a id="id-1.10.5.30.5"></a>

**表 53.26. `pg_shadow` 欄位**

<table border="1" class="table" summary="表 53.26. pg_shadow 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>）
      </p>
<p>
       使用者名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesysid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此使用者的 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usecreatedb</code> <code class="type">bool</code>
</p>
<p>
       使用者可以建立資料庫
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesuper</code> <code class="type">bool</code>
</p>
<p>
       使用者是超級使用者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">userepl</code> <code class="type">bool</code>
</p>
<p>
       使用者可以啟動串流複寫，並可讓系統進入及離開備份模式。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usebypassrls</code> <code class="type">bool</code>
</p>
<p>
       使用者會略過所有資料列層級安全性政策，更多資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-rowsecurity.md">第 5.9 節</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">passwd</code> <code class="type">text</code>
</p>
<p>
       加密後的密碼；若無則為 null。關於加密密碼如何儲存的細節，請參閱<a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">valuntil</code> <code class="type">timestamptz</code>
</p>
<p>
       密碼到期時間（僅用於密碼認證）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">useconfig</code> <code class="type">text[]</code>
</p>
<p>
       執行期設定變數的工作階段預設值
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-shadow.html)（原文版本：18.6；核對日期：2026-10-10）
