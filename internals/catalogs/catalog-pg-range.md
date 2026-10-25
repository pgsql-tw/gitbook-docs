<a id="CATALOG-PG-RANGE"></a>

## 52.43. `pg_range` [#](#catalog-pg-range) <a href="#catalog-pg-range" id="catalog-pg-range"></a>

<a id="id-1.10.4.45.2"></a>

系統目錄 `pg_range` 存放範圍型別的相關資訊。這些資訊是在這些型別於 [`pg_type`](catalog-pg-type.md) 中的項目之外另行存放的。

<a id="id-1.10.4.45.4"></a>

**表 52.43. `pg_range` 欄位**

<table border="1" class="table" summary="表 52.43. pg_range 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngtypid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       範圍型別的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngsubtype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此範圍型別之元素型別（子型別）的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngmultitypid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此範圍型別所對應之多重範圍型別的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngcollation</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       範圍比較所使用之定序的 OID；若無則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngsubopc</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-opclass.md"><code class="structname">pg_opclass</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       範圍比較所使用之子型別運算子類別的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngcanonical</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       將範圍值轉換為正規形式之函式的 OID；若無則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rngsubdiff</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       以 <code class="type">double precision</code> 傳回兩個元素值之差的函式的 OID；若無則為零
      </p></td></tr></tbody></table>

<br>

`rngsubopc`（若元素型別可定序，再加上 `rngcollation`）決定範圍型別所使用的排序順序。元素型別為離散型別時會使用 `rngcanonical`。`rngsubdiff` 是選用的，但應該提供，以改善該範圍型別上 GiST 索引的效能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-range.html)（原文版本：18.6；核對日期：2026-10-17）
