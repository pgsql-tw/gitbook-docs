<a id="CATALOG-PG-AMPROC"></a>

## 52.5. `pg_amproc` [#](#CATALOG-PG-AMPROC)

<a id="id-1.10.4.7.2"></a>

系統目錄 `pg_amproc` 存放與存取方法運算子家族相關聯之支援函式的資訊。
屬於某個運算子家族的每個支援函式各有一筆資料列。

<a id="id-1.10.4.7.4"></a>

**表 52.5. `pg_amproc` 欄位**

<table border="1" class="table" summary="表 52.5. pg_amproc 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">amprocfamily</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-opfamily.md"><code class="structname">pg_opfamily</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此項目所屬的運算子家族
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amproclefttype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       相關聯運算子的左側輸入資料型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amprocrighttype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       相關聯運算子的右側輸入資料型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amprocnum</code> <code class="type">int2</code>
</p>
<p>
       支援函式編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amproc</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       函式的 OID
      </p></td></tr></tbody></table>

<br>

`amproclefttype` 與 `amprocrighttype` 欄位通常的解讀是：
它們識別出某個支援函式所支援之運算子的左側與右側輸入型別。
對某些存取方法而言，這些型別與支援函式本身的輸入資料型別相符，對其他存取方法則不然。
索引有「預設」支援函式的概念，也就是 `amproclefttype` 與
`amprocrighttype` 都等於索引運算子類別之
`opcintype` 的那些支援函式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-amproc.html)（原文版本：18.6；核對日期：2026-10-17）
