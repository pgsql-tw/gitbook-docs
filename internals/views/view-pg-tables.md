## 53.32. `pg_tables` [#](#VIEW-PG-TABLES)

<a id="id-1.10.5.36.2"></a>

The view `pg_tables` provides access to
useful information about each table in the database.

<a id="id-1.10.5.36.4"></a>

**Table 53.32. `pg_tables` Columns**

<table border="1" class="table" summary="pg_tables Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>)
      </p>
<p>
       Name of schema containing table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>)
      </p>
<p>
       Name of table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tableowner</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>)
      </p>
<p>
       Name of table's owner
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespace</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">spcname</code>)
      </p>
<p>
       Name of tablespace containing table (null if default for database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">hasindexes</code> <code class="type">bool</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relhasindex</code>)
      </p>
<p>
       True if table has (or recently had) any indexes
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">hasrules</code> <code class="type">bool</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relhasrules</code>)
      </p>
<p>
       True if table has (or once had) rules
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">hastriggers</code> <code class="type">bool</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relhastriggers</code>)
      </p>
<p>
       True if table has (or once had) triggers
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rowsecurity</code> <code class="type">bool</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relrowsecurity</code>)
      </p>
<p>
       True if row security is enabled on the table
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-tables.html)（英文原文，待翻譯）
