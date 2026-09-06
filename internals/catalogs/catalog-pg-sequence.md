## 52.47. `pg_sequence` [#](#CATALOG-PG-SEQUENCE)

<a id="id-1.10.4.49.2"></a>

系統目錄 `pg_sequence` 包含序列的資訊。序列的部分資訊，例如名稱與 schema，位於
[`pg_class`](catalog-pg-class.md)

<a id="id-1.10.4.49.4"></a>

**表 52.47. `pg_sequence` 欄位**

<table border="1" class="table" summary="pg_sequence Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seqrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       此序列在 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> 中項目的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seqtypid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       序列的資料型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seqstart</code> <code class="type">int8</code>
</p>
<p>
       序列的起始值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seqincrement</code> <code class="type">int8</code>
</p>
<p>
       序列的遞增值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seqmax</code> <code class="type">int8</code>
</p>
<p>
       序列的最大值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seqmin</code> <code class="type">int8</code>
</p>
<p>
       序列的最小值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seqcache</code> <code class="type">int8</code>
</p>
<p>
       序列的快取大小
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seqcycle</code> <code class="type">bool</code>
</p>
<p>
       序列是否循環
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-sequence.html)（原文版本：18.6；核對日期：2026-09-06）
