<a id="CATALOG-PG-TS-TEMPLATE"></a>

## 52.63. `pg_ts_template` [#](#CATALOG-PG-TS-TEMPLATE)

<a id="id-1.10.4.65.2"></a>

`pg_ts_template` 目錄包含定義文字搜尋範本的項目。範本是某一類文字搜尋字典的實作骨架。由於範本必須以 C 語言層級的函式實作，建立新範本僅限資料庫超級使用者。

PostgreSQL 的文字搜尋功能在[第 12 章](../../the-sql-language/textsearch/README.md)中有詳細說明。

<a id="id-1.10.4.65.5"></a>

**表 52.63. `pg_ts_template` 欄位**

<table border="1" class="table" summary="表 52.63. pg_ts_template 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">tmplname</code> <code class="type">name</code>
</p>
<p>
       文字搜尋範本名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tmplnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此範本之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tmplinit</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       範本初始化函式的 OID（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tmpllexize</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       範本 lexize 函式的 OID
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-ts-template.html)（原文版本：18.6；核對日期：2026-10-17）
