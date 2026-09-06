## 52.56. `pg_tablespace` [#](#CATALOG-PG-TABLESPACE)

<a id="id-1.10.4.58.2"></a>

The catalog `pg_tablespace` stores information
about the available tablespaces. Tables can be placed in particular
tablespaces to aid administration of disk layout.

Unlike most system catalogs, `pg_tablespace`
is shared across all databases of a cluster: there is only one
copy of `pg_tablespace` per cluster, not
one per database.

<a id="id-1.10.4.58.5"></a>

**Table 52.56. `pg_tablespace` Columns**

<table border="1" class="table" summary="pg_tablespace Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">spcname</code> <code class="type">name</code>
</p>
<p>
       Tablespace name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spcowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the tablespace, usually the user who created it
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spcacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       Access privileges; see <a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">Section 5.8</a> for details
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spcoptions</code> <code class="type">text[]</code>
</p>
<p>
       Tablespace-level options, as <span class="quote">“<span class="quote">keyword=value</span>”</span> strings
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-tablespace.html)（英文原文，待翻譯）
