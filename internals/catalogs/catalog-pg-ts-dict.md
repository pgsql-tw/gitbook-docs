## 52.61. `pg_ts_dict` [#](#CATALOG-PG-TS-DICT)

<a id="id-1.10.4.63.2"></a>

The `pg_ts_dict` catalog contains entries
defining text search dictionaries. A dictionary depends on a text
search template, which specifies all the implementation functions
needed; the dictionary itself provides values for the user-settable
parameters supported by the template. This division of labor allows
dictionaries to be created by unprivileged users. The parameters
are specified by a text string `dictinitoption`,
whose format and meaning vary depending on the template.

PostgreSQL's text search features are
described at length in [Chapter 12](../../the-sql-language/textsearch/README.md).

<a id="id-1.10.4.63.5"></a>

**Table 52.61. `pg_ts_dict` Columns**

<table border="1" class="table" summary="pg_ts_dict Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">dictname</code> <code class="type">name</code>
</p>
<p>
       Text search dictionary name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dictnamespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the namespace that contains this dictionary
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dictowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the dictionary
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dicttemplate</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-ts-template.md"><code class="structname">pg_ts_template</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the text search template for this dictionary
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dictinitoption</code> <code class="type">text</code>
</p>
<p>
       Initialization option string for the template
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-ts-dict.html)（英文原文，待翻譯）
