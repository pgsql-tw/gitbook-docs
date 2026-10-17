<a id="CATALOG-PG-TS-PARSER"></a>

## 52.62. `pg_ts_parser` [#](#CATALOG-PG-TS-PARSER)

<a id="id-1.10.4.64.2"></a>

`pg_ts_parser` 目錄包含定義文字搜尋剖析器的項目。剖析器負責將輸入文字切分為詞素（lexeme），並為每個詞素指定語彙單元類型（token type）。由於剖析器必須以 C 語言層級的函式實作，建立新剖析器僅限資料庫超級使用者。

PostgreSQL 的文字搜尋功能在[第 12 章](../../the-sql-language/textsearch/README.md)中有詳細說明。

<a id="id-1.10.4.64.5"></a>

**表 52.62. `pg_ts_parser` 欄位**

<table border="1" class="table" summary="表 52.62. pg_ts_parser 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">prsname</code> <code class="type">name</code>
</p>
<p>
       文字搜尋剖析器名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prsnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此剖析器之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prsstart</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       剖析器啟動函式的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prstoken</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       剖析器取得下一個語彙單元（next-token）函式的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prsend</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       剖析器關閉函式的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prsheadline</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       剖析器摘要（headline）函式的 OID（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prslextype</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       剖析器 lextype 函式的 OID
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-ts-parser.html)（原文版本：18.6；核對日期：2026-10-17）
