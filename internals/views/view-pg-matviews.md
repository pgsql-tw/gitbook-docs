<a id="VIEW-PG-MATVIEWS"></a>

## 53.14. `pg_matviews` [#](#view-pg-matviews) <a href="#view-pg-matviews" id="view-pg-matviews"></a>

<a id="id-1.10.5.18.2"></a><a id="id-1.10.5.18.3"></a>

檢視表 `pg_matviews` 可用來存取資料庫中每個具體化檢視表的實用資訊。

<a id="id-1.10.5.18.5"></a>

**表 53.14. `pg_matviews` 欄位**

<table border="1" class="table" summary="表 53.14. pg_matviews 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含此具體化檢視表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">matviewname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       具體化檢視表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">matviewowner</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>）
      </p>
<p>
       具體化檢視表擁有者的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespace</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">spcname</code>）
      </p>
<p>
       包含此具體化檢視表的資料表空間名稱（若為資料庫的預設資料表空間則為 null）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">hasindexes</code> <code class="type">bool</code>
</p>
<p>
       若此具體化檢視表擁有（或最近曾擁有）任何索引，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ispopulated</code> <code class="type">bool</code>
</p>
<p>
       若此具體化檢視表目前已填入資料，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">definition</code> <code class="type">text</code>
</p>
<p>
       具體化檢視表定義（重建出的 <a class="xref" href="../../reference/sql-commands/sql-select.md"><span class="refentrytitle">SELECT</span></a> 查詢）
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-matviews.html)（原文版本：18.6；核對日期：2026-10-10）
