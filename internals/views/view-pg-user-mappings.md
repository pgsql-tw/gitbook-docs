<a id="VIEW-PG-USER-MAPPINGS"></a>

## 53.36. `pg_user_mappings` [#](#view-pg-user-mappings) <a href="#view-pg-user-mappings" id="view-pg-user-mappings"></a>

<a id="id-1.10.5.40.2"></a>

檢視表 `pg_user_mappings` 提供對使用者對應資訊的存取。它基本上是 [`pg_user_mapping`](../catalogs/catalog-pg-user-mapping.md) 的一個可公開讀取的檢視表，在使用者無權使用選項欄位時會略去該欄位。

<a id="id-1.10.5.40.4"></a>

**表 53.36. `pg_user_mappings` 欄位**

<table border="1" class="table" summary="表 53.36. pg_user_mappings 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">umid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-user-mapping.md"><code class="structname">pg_user_mapping</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       使用者對應的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srvid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-foreign-server.md"><code class="structname">pg_foreign_server</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此對應之外部伺服器的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srvname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-foreign-server.md"><code class="structname">pg_foreign_server</code></a>.<code class="structfield">srvname</code>）
      </p>
<p>
       外部伺服器名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">umuser</code> <code class="type">oid</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       被對應之本地角色的 OID；若此使用者對應為公用（public）則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usename</code> <code class="type">name</code>
</p>
<p>
       要被對應之本地使用者的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">umoptions</code> <code class="type">text[]</code>
</p>
<p>
       使用者對應專屬的選項，以 <span class="quote">“<span class="quote">keyword=value</span>”</span> 字串形式呈現
      </p></td></tr></tbody></table>

<br>

為了保護以使用者對應選項形式儲存的密碼資訊，除非符合下列其中一項條件，否則 `umoptions` 欄位讀出的值將為 null：

* 目前使用者就是被對應的使用者，且擁有該伺服器或持有該伺服器的 `USAGE` 權限
* 目前使用者是該伺服器的擁有者，且此對應是針對 `PUBLIC`
* 目前使用者是超級使用者

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-user-mappings.html)（原文版本：18.6；核對日期：2026-10-10）
