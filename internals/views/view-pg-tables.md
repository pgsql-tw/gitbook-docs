<a id="VIEW-PG-TABLES"></a>

## 53.32. `pg_tables` [#](#view-pg-tables) <a href="#view-pg-tables" id="view-pg-tables"></a>

<a id="id-1.10.5.36.2"></a>

檢視表 `pg_tables` 可用來存取資料庫中每個資料表的實用資訊。

<a id="id-1.10.5.36.4"></a>

**表 53.32. `pg_tables` 欄位**

<table border="1" class="table" summary="表 53.32. pg_tables 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含此資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tableowner</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>）
      </p>
<p>
       資料表擁有者的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespace</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">spcname</code>）
      </p>
<p>
       包含此資料表的資料表空間名稱（若為資料庫的預設資料表空間則為 null）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">hasindexes</code> <code class="type">bool</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relhasindex</code>）
      </p>
<p>
       若此資料表擁有（或最近曾擁有）任何索引，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">hasrules</code> <code class="type">bool</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relhasrules</code>）
      </p>
<p>
       若此資料表擁有（或曾經擁有）規則，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">hastriggers</code> <code class="type">bool</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relhastriggers</code>）
      </p>
<p>
       若此資料表擁有（或曾經擁有）觸發程序，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rowsecurity</code> <code class="type">bool</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relrowsecurity</code>）
      </p>
<p>
       若此資料表已啟用資料列安全性，則為 true
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-tables.html)（原文版本：18.6；核對日期：2026-10-10）
