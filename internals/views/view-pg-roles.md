<a id="VIEW-PG-ROLES"></a>

## 53.21. `pg_roles` [#](#view-pg-roles) <a href="#view-pg-roles" id="view-pg-roles"></a>

<a id="id-1.10.5.25.2"></a>

檢視表 `pg_roles` 可用來存取資料庫角色的相關資訊。它只是 [`pg_authid`](../catalogs/catalog-pg-authid.md) 的一個公開可讀的檢視表，並會遮蔽密碼欄位（一律顯示為 ********）。

<a id="id-1.10.5.25.4"></a>

**表 53.21. `pg_roles` 欄位**

<table border="1" class="table" summary="表 53.21. pg_roles 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolname</code> <code class="type">name</code>
</p>
<p>
       角色名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolsuper</code> <code class="type">bool</code>
</p>
<p>
       角色具有超級使用者權限
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolinherit</code> <code class="type">bool</code>
</p>
<p>
       角色會自動繼承其身為成員之角色的權限
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolcreaterole</code> <code class="type">bool</code>
</p>
<p>
       角色可以建立更多角色
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolcreatedb</code> <code class="type">bool</code>
</p>
<p>
       角色可以建立資料庫
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolcanlogin</code> <code class="type">bool</code>
</p>
<p>
       角色可以登入。也就是說，此角色可以作為初始的工作階段授權識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolreplication</code> <code class="type">bool</code>
</p>
<p>
       角色是複寫角色。複寫角色可以發起複寫連線，並可建立與移除複寫插槽。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolconnlimit</code> <code class="type">int4</code>
</p>
<p>
       對於可以登入的角色，此欄位設定該角色可建立的最大並行連線數。-1 表示沒有限制。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolpassword</code> <code class="type">text</code>
</p>
<p>
       不是密碼（讀取時一律顯示為 <code class="literal">********</code>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolvaliduntil</code> <code class="type">timestamptz</code>
</p>
<p>
       密碼到期時間（僅用於密碼認證）；若無到期時間則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolbypassrls</code> <code class="type">bool</code>
</p>
<p>
       角色會略過所有資料列層級安全性政策，更多資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-rowsecurity.md">第 5.9 節</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rolconfig</code> <code class="type">text[]</code>
</p>
<p>
       角色專屬的執行期設定變數預設值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       角色的 ID
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-roles.html)（原文版本：18.6；核對日期：2026-10-10）
