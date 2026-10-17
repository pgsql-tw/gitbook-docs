<a id="CATALOG-PG-INHERITS"></a>

## 52.27. `pg_inherits` [#](#CATALOG-PG-INHERITS)

<a id="id-1.10.4.29.2"></a>

目錄 `pg_inherits` 記錄資料表與索引繼承階層的相關資訊。資料庫中每一個直接的父子資料表或索引關係，都各有一個項目。（間接繼承可以循著項目串成的鏈來判斷。）

<a id="id-1.10.4.29.4"></a>

**表 52.27. `pg_inherits` 欄位**

<table border="1" class="table" summary="表 52.27. pg_inherits 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inhrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       子資料表或子索引的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inhparent</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       父資料表或父索引的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inhseqno</code> <code class="type">int4</code>
</p>
<p>
       若子資料表有超過一個直接父資料表（多重繼承），此數字表示繼承而來的欄位應以何種順序排列。計數從 1 開始。
      </p>
<p>
       索引不能有多重繼承，因為索引只有在使用宣告式分割時才能繼承。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inhdetachpending</code> <code class="type">bool</code>
</p>
<p>
正在卸離過程中的分割區為 <code class="literal">true</code>；否則為 <code class="literal">false</code>。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-inherits.html)（原文版本：18.6；核對日期：2026-10-17）
