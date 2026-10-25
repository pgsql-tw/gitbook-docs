<a id="CATALOG-PG-FOREIGN-SERVER"></a>

## 52.24. `pg_foreign_server` [#](#catalog-pg-foreign-server) <a href="#catalog-pg-foreign-server" id="catalog-pg-foreign-server"></a>

<a id="id-1.10.4.26.2"></a>

目錄 `pg_foreign_server` 存放外部伺服器定義。外部伺服器描述外部資料的來源，例如遠端伺服器。外部伺服器是透過外部資料包裝器來存取的。

<a id="id-1.10.4.26.4"></a>

**表 52.24. `pg_foreign_server` 欄位**

<table border="1" class="table" summary="表 52.24. pg_foreign_server 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">srvname</code> <code class="type">name</code>
</p>
<p>
       外部伺服器的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srvowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       外部伺服器的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srvfdw</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-foreign-data-wrapper.md"><code class="structname">pg_foreign_data_wrapper</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此外部伺服器之外部資料包裝器的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srvtype</code> <code class="type">text</code>
</p>
<p>
       伺服器的類型（選用）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srvversion</code> <code class="type">text</code>
</p>
<p>
       伺服器的版本（選用）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srvacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">srvoptions</code> <code class="type">text[]</code>
</p>
<p>
       外部伺服器專屬的選項，以 <span class="quote">“<span class="quote">keyword=value</span>”</span> 字串形式呈現
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-foreign-server.html)（原文版本：18.6；核對日期：2026-10-17）
