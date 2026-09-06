## 53.14. `pg_matviews` [#](#VIEW-PG-MATVIEWS)

<a id="id-1.10.5.18.2"></a><a id="id-1.10.5.18.3"></a>

The view `pg_matviews` provides access to
useful information about each materialized view in the database.

<a id="id-1.10.5.18.5"></a>

**Table 53.14. `pg_matviews` Columns**

<table border="1" class="table" summary="pg_matviews Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>)
      </p>
<p>
       Name of schema containing materialized view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">matviewname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>)
      </p>
<p>
       Name of materialized view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">matviewowner</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>)
      </p>
<p>
       Name of materialized view's owner
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespace</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">spcname</code>)
      </p>
<p>
       Name of tablespace containing materialized view (null if default for database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">hasindexes</code> <code class="type">bool</code>
</p>
<p>
       True if materialized view has (or recently had) any indexes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ispopulated</code> <code class="type">bool</code>
</p>
<p>
       True if materialized view is currently populated
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">definition</code> <code class="type">text</code>
</p>
<p>
       Materialized view definition (a reconstructed <a class="xref" href="../../reference/sql-commands/sql-select.md"><span class="refentrytitle">SELECT</span></a> query)
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-matviews.html)（英文原文，待翻譯）
