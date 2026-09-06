## 53.37. `pg_views` [#](#VIEW-PG-VIEWS)

<a id="id-1.10.5.41.2"></a>

The view `pg_views` provides access to
useful information about each view in the database.

<a id="id-1.10.5.41.4"></a>

**Table 53.37. `pg_views` Columns**

<table border="1" class="table" summary="pg_views Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>)
      </p>
<p>
       Name of schema containing view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">viewname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>)
      </p>
<p>
       Name of view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">viewowner</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>)
      </p>
<p>
       Name of view's owner
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">definition</code> <code class="type">text</code>
</p>
<p>
       View definition (a reconstructed <a class="xref" href="../../reference/sql-commands/sql-select.md"><span class="refentrytitle">SELECT</span></a> query)
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-views.html)（英文原文，待翻譯）
