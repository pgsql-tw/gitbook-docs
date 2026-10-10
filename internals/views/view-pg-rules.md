<a id="VIEW-PG-RULES"></a>

## 53.22. `pg_rules` [#](#VIEW-PG-RULES)

<a id="id-1.10.5.26.2"></a>

檢視表 `pg_rules` 提供對查詢重寫規則之實用資訊的存取。

<a id="id-1.10.5.26.4"></a>

**表 53.22. `pg_rules` 欄位**

<table border="1" class="table" summary="表 53.22. pg_rules 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含資料表之綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       此規則所屬之資料表的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rulename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-rewrite.md"><code class="structname">pg_rewrite</code></a>.<code class="structfield">rulename</code>）
      </p>
<p>
       規則名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">definition</code> <code class="type">text</code>
</p>
<p>
       規則定義（重建出的建立命令）
      </p></td></tr></tbody></table>

<br>

檢視表 `pg_rules` 不包含檢視表與具體化檢視表的 `ON SELECT` 規則；這些規則可在 [`pg_views`](view-pg-views.md) 與 [`pg_matviews`](view-pg-matviews.md) 中查看。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-rules.html)（原文版本：18.6；核對日期：2026-10-10）
