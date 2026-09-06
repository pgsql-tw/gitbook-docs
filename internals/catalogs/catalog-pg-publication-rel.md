## 52.42. `pg_publication_rel` [#](#CATALOG-PG-PUBLICATION-REL)

<a id="id-1.10.4.44.2"></a>

The catalog `pg_publication_rel` contains the
mapping between relations and publications in the database. This is a
many-to-many mapping. See also [Section 53.18](../views/view-pg-publication-tables.md)
for a more user-friendly view of this information.

<a id="id-1.10.4.44.4"></a>

**Table 52.42. `pg_publication_rel` Columns**

<table border="1" class="table" summary="pg_publication_rel Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">prpubid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-publication.md"><code class="structname">pg_publication</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Reference to publication
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Reference to relation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prqual</code> <code class="type">pg_node_tree</code>
</p>
<p>Expression tree (in <code class="function">nodeToString()</code>
      representation) for the relation's publication qualifying condition. Null
      if there is no publication qualifying condition.</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prattrs</code> <code class="type">int2vector</code>
       (references <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>)
      </p>
<p>
       This is an array of values that indicates which table columns are
       part of the publication.  For example, a value of <code class="literal">1 3</code>
       would mean that the first and the third table columns are published.
       A null value indicates that all columns are published.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-publication-rel.html)（英文原文，待翻譯）
