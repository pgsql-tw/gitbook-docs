## 52.25. `pg_foreign_table` [#](#CATALOG-PG-FOREIGN-TABLE)

<a id="id-1.10.4.27.2"></a>

The catalog `pg_foreign_table` contains
auxiliary information about foreign tables. A foreign table is
primarily represented by a
[`pg_class`](catalog-pg-class.md)
entry, just like a regular table. Its `pg_foreign_table`
entry contains the information that is pertinent only to foreign tables
and not any other kind of relation.

<a id="id-1.10.4.27.4"></a>

**Table 52.25. `pg_foreign_table` Columns**

<table border="1" class="table" summary="pg_foreign_table Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ftrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a> entry for this foreign table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ftserver</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-foreign-server.md"><code class="structname">pg_foreign_server</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the foreign server for this foreign table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ftoptions</code> <code class="type">text[]</code>
</p>
<p>
       Foreign table options, as <span class="quote">“<span class="quote">keyword=value</span>”</span> strings
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-foreign-table.html)（英文原文，待翻譯）
