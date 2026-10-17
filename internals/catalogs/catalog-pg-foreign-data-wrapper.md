<a id="CATALOG-PG-FOREIGN-DATA-WRAPPER"></a>

## 52.23. `pg_foreign_data_wrapper` [#](#CATALOG-PG-FOREIGN-DATA-WRAPPER)

<a id="id-1.10.4.25.2"></a>

目錄 `pg_foreign_data_wrapper` 存放外部資料包裝器定義。外部資料包裝器是用來存取位於外部伺服器上之外部資料的機制。

<a id="id-1.10.4.25.4"></a>

**表 52.23. `pg_foreign_data_wrapper` 欄位**

<table border="1" class="table" summary="表 52.23. pg_foreign_data_wrapper 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">fdwname</code> <code class="type">name</code>
</p>
<p>
       外部資料包裝器的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">fdwowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       外部資料包裝器的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">fdwhandler</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       參照一個處理函式，負責為此外部資料包裝器提供執行常式。若未提供處理函式則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">fdwvalidator</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       參照一個驗證函式，負責檢查提供給此外部資料包裝器之選項的有效性，以及使用此外部資料包裝器之外部伺服器與使用者對應的選項。若未提供驗證函式則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">fdwacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">fdwoptions</code> <code class="type">text[]</code>
</p>
<p>
       外部資料包裝器專屬的選項，以 <span class="quote">“<span class="quote">keyword=value</span>”</span> 字串形式呈現
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-foreign-data-wrapper.html)（原文版本：18.6；核對日期：2026-10-17）
