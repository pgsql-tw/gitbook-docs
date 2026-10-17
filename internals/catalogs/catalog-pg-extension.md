<a id="CATALOG-PG-EXTENSION"></a>

## 52.22. `pg_extension` [#](#CATALOG-PG-EXTENSION)

<a id="id-1.10.4.24.2"></a>

系統目錄 `pg_extension` 存放已安裝擴充功能的相關資訊。關於擴充功能的詳細資訊，請參閱[第 36.17 節](../../server-programming/extend/extend-extensions.md)。

<a id="id-1.10.4.24.4"></a>

**表 52.22. `pg_extension` 欄位**

<table border="1" class="table" summary="表 52.22. pg_extension 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">extname</code> <code class="type">name</code>
</p>
<p>
       擴充功能的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">extowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       擴充功能的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">extnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此擴充功能所匯出物件的綱要
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">extrelocatable</code> <code class="type">bool</code>
</p>
<p>
       若擴充功能可以重新放置到其他綱要則為真
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">extversion</code> <code class="type">text</code>
</p>
<p>
       擴充功能的版本名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">extconfig</code> <code class="type">oid[]</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此擴充功能之設定資料表的 <code class="type">regclass</code> OID 陣列；若無則為 <code class="literal">NULL</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">extcondition</code> <code class="type">text[]</code>
</p>
<p>
       此擴充功能之設定資料表的 <code class="literal">WHERE</code> 子句過濾條件陣列；若無則為 <code class="literal">NULL</code>
      </p></td></tr></tbody></table>

<br>

請注意，與大多數具有「namespace」欄位的系統目錄不同，`extnamespace` 並不意味著該擴充功能屬於那個綱要。擴充功能名稱永遠不會以綱要限定。`extnamespace` 指出的是包含該擴充功能大部分或全部物件的綱要。若 `extrelocatable` 為真，則此綱要實際上必須包含屬於該擴充功能、所有可以用綱要限定的物件。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-extension.html)（原文版本：18.6；核對日期：2026-10-17）
