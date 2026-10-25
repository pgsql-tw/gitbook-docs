<a id="CATALOG-PG-USER-MAPPING"></a>

## 52.65. `pg_user_mapping` [#](#catalog-pg-user-mapping) <a href="#catalog-pg-user-mapping" id="catalog-pg-user-mapping"></a>

<a id="id-1.10.4.67.2"></a>

目錄 `pg_user_mapping` 儲存從本機使用者到遠端的對應。一般使用者無法存取此目錄，請改用檢視表
[`pg_user_mappings`](../views/view-pg-user-mappings.md)。

<a id="id-1.10.4.67.4"></a>

**表 52.66. `pg_user_mapping` 欄位**

<table border="1" class="table" summary="表 52.66. pg_user_mapping 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       資料列識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">umuser</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       被對應之本機角色的 OID；若此使用者對應為 public，則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">umserver</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-foreign-server.md"><code class="structname">pg_foreign_server</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此對應之外部伺服器的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">umoptions</code> <code class="type">text[]</code>
</p>
<p>
       使用者對應專屬的選項，以 <span class="quote">“<span class="quote">keyword=value</span>”</span> 字串形式呈現
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-user-mapping.html)（原文版本：18.6；核對日期：2026-10-17）
