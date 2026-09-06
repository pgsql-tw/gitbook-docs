## 53.12. `pg_indexes` [#](#VIEW-PG-INDEXES)

<a id="id-1.10.5.16.2"></a>

The view `pg_indexes` provides access to
useful information about each index in the database.

<a id="id-1.10.5.16.4"></a>

**Table 53.12. `pg_indexes` Columns**

<table border="1" class="table" summary="pg_indexes Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>)
      </p>
<p>
       Name of schema containing table and index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>)
      </p>
<p>
       Name of table the index is for
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>)
      </p>
<p>
       Name of index
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespace</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">spcname</code>)
      </p>
<p>
       Name of tablespace containing index (null if default for database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexdef</code> <code class="type">text</code>
</p>
<p>
       Index definition (a reconstructed <a class="xref" href="../../reference/sql-commands/sql-createindex.md"><span class="refentrytitle">CREATE INDEX</span></a>
       command)
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-indexes.html)（英文原文，待翻譯）
