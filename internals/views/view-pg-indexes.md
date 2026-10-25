<a id="VIEW-PG-INDEXES"></a>

## 53.12. `pg_indexes` [#](#view-pg-indexes) <a href="#view-pg-indexes" id="view-pg-indexes"></a>

<a id="id-1.10.5.16.2"></a>

檢視表 `pg_indexes` 可用來存取資料庫中每個索引的實用資訊。

<a id="id-1.10.5.16.4"></a>

**表 53.12. `pg_indexes` 欄位**

<table border="1" class="table" summary="表 53.12. pg_indexes 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含此資料表與索引的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       此索引所屬資料表的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       索引名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespace</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">spcname</code>）
      </p>
<p>
       包含此索引的資料表空間名稱（若為資料庫的預設資料表空間則為 null）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexdef</code> <code class="type">text</code>
</p>
<p>
       索引定義（重建出的 <a class="xref" href="../../reference/sql-commands/sql-createindex.md"><span class="refentrytitle">CREATE INDEX</span></a> 命令）
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-indexes.html)（原文版本：18.6；核對日期：2026-10-10）
