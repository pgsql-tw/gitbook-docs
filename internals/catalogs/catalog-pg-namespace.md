## 52.32. `pg_namespace` [#](#CATALOG-PG-NAMESPACE)

<a id="id-1.10.4.34.2"></a>

The catalog `pg_namespace` stores namespaces.
A namespace is the structure underlying SQL schemas: each namespace
can have a separate collection of relations, types, etc. without name
conflicts.

<a id="id-1.10.4.34.4"></a>

**Table 52.32. `pg_namespace` Columns**

<table border="1" class="table" summary="pg_namespace Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">nspname</code> <code class="type">name</code>
</p>
<p>
       Name of the namespace
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">nspowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the namespace
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">nspacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       Access privileges; see <a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">Section 5.8</a> for details
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-namespace.html)（英文原文，待翻譯）
