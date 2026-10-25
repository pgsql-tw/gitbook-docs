<a id="CATALOG-PG-TRANSFORM"></a>

## 52.57. `pg_transform` [#](#catalog-pg-transform) <a href="#catalog-pg-transform" id="catalog-pg-transform"></a>

<a id="id-1.10.4.59.2"></a>

目錄 `pg_transform` 儲存關於轉換（transform）的資訊；轉換是一種讓資料型別適應程序語言的機制。詳細資訊請參閱 [CREATE TRANSFORM](../../reference/sql-commands/sql-createtransform.md)。

<a id="id-1.10.4.59.4"></a>

**表 52.57. `pg_transform` 欄位**

<table border="1" class="table" summary="表 52.57. pg_transform 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">trftype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此轉換所適用之資料型別的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trflang</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-language.md"><code class="structname">pg_language</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此轉換所適用之語言的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trffromsql</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       將資料型別轉換為程序語言的輸入（例如函式參數）時所使用函式的 OID。
       若應使用預設行為，則儲存零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trftosql</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       將程序語言的輸出（例如回傳值）轉換為資料型別時所使用函式的 OID。
       若應使用預設行為，則儲存零。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-transform.html)（原文版本：18.6；核對日期：2026-10-17）
