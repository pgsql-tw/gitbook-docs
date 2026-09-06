## 52.57. `pg_transform` [#](#CATALOG-PG-TRANSFORM)

<a id="id-1.10.4.59.2"></a>

The catalog `pg_transform` stores information about
transforms, which are a mechanism to adapt data types to procedural
languages. See [CREATE TRANSFORM](../../reference/sql-commands/sql-createtransform.md) for more information.

<a id="id-1.10.4.59.4"></a>

**Table 52.57. `pg_transform` Columns**

<table border="1" class="table" summary="pg_transform Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">trftype</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the data type this transform is for
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trflang</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-language.md"><code class="structname">pg_language</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the language this transform is for
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trffromsql</code> <code class="type">regproc</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the function to use when converting the data type for input
       to the procedural language (e.g., function parameters).  Zero is stored
       if the default behavior should be used.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trftosql</code> <code class="type">regproc</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the function to use when converting output from the
       procedural language (e.g., return values) to the data type.  Zero is
       stored if the default behavior should be used.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-transform.html)（英文原文，待翻譯）
