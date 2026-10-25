<a id="VIEW-PG-USER"></a>

## 53.35. `pg_user` [#](#view-pg-user) <a href="#view-pg-user" id="view-pg-user"></a>

<a id="id-1.10.5.39.2"></a>

檢視表 `pg_user` 可用來存取資料庫使用者的相關資訊。它只是 [`pg_shadow`](view-pg-shadow.md) 的一個公開可讀的檢視表，並會遮蔽密碼欄位（一律顯示為 ********）。

<a id="id-1.10.5.39.4"></a>

**表 53.35. `pg_user` 欄位**

<table border="1" class="table" summary="表 53.35. pg_user 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usename</code> <code class="type">name</code>
</p>
<p>
       使用者名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesysid</code> <code class="type">oid</code>
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
       不是密碼（讀取時一律顯示為 <code class="literal">********</code>）
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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-user.html)（原文版本：18.6；核對日期：2026-10-10）
