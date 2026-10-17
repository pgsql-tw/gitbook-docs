<a id="CATALOG-PG-TS-DICT"></a>

## 52.61. `pg_ts_dict` [#](#CATALOG-PG-TS-DICT)

<a id="id-1.10.4.63.2"></a>

目錄 `pg_ts_dict` 包含定義文字搜尋字典的項目。字典相依於文字搜尋範本，範本指定了所需的全部實作函式；字典本身則為範本所支援、可由使用者設定的參數提供值。這樣的分工讓非特權使用者也能建立字典。參數以文字字串 `dictinitoption` 指定，其格式與意義依範本而異。

PostgreSQL 的文字搜尋功能在[第 12 章](../../the-sql-language/textsearch/README.md)中有詳細說明。

<a id="id-1.10.4.63.5"></a>

**表 52.61. `pg_ts_dict` 欄位**

<table border="1" class="table" summary="表 52.61. pg_ts_dict 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">dictname</code> <code class="type">name</code>
</p>
<p>
       文字搜尋字典名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dictnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此字典之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dictowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       字典的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dicttemplate</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-ts-template.md"><code class="structname">pg_ts_template</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此字典所用文字搜尋範本的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dictinitoption</code> <code class="type">text</code>
</p>
<p>
       範本的初始化選項字串
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-ts-dict.html)（原文版本：18.6；核對日期：2026-10-17）
