## 53.9. `pg_group` [#](#VIEW-PG-GROUP)

<a id="id-1.10.5.13.2"></a>

檢視表 `pg_group` 為了向後相容而存在：它模擬 PostgreSQL 8.1 版之前存在的系統目錄。它顯示所有標記為非 `rolcanlogin` 之角色的名稱與成員，這大致等同於作為群組使用的角色集合。

<a id="id-1.10.5.13.4"></a>

**表 53.9. `pg_group` 欄位**

<table border="1" class="table" summary="pg_group Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">groname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>)
      </p>
<p>
       群組名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grosysid</code> <code class="type">oid</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       此群組的 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grolist</code> <code class="type">oid[]</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       包含此群組中角色 ID 的陣列
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-group.html)（原文版本：18.6；核對日期：2026-09-06）
