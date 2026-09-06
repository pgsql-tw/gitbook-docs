## 52.63. `pg_ts_template` [#](#CATALOG-PG-TS-TEMPLATE)

<a id="id-1.10.4.65.2"></a>

The `pg_ts_template` catalog contains entries
defining text search templates. A template is the implementation
skeleton for a class of text search dictionaries.
Since a template must be implemented by C-language-level functions,
creation of new templates is restricted to database superusers.

PostgreSQL's text search features are
described at length in [Chapter 12](../../the-sql-language/textsearch/README.md).

<a id="id-1.10.4.65.5"></a>

**Table 52.63. `pg_ts_template` Columns**

<table border="1" class="table" summary="pg_ts_template Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       Row identifier
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tmplname</code> <code class="type">name</code>
</p>
<p>
       Text search template name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tmplnamespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the namespace that contains this template
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tmplinit</code> <code class="type">regproc</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the template's initialization function (zero if none)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tmpllexize</code> <code class="type">regproc</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the template's lexize function
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-ts-template.html)（英文原文，待翻譯）
