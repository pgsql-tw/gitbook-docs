<a id="CATALOG-PG-LARGEOBJECT-METADATA"></a>

# 53.31. pg_largeobject_metadata

<a id="id-1.10.4.33.2"></a>

The catalog `pg_largeobject_metadata` holds metadata associated with large objects. The actual large object data is stored in [`pg_largeobject`](pg_largeobject.md).

<a id="id-1.10.4.33.4"></a>

<strong>Table 53.31. <code class="structname">pg&#95;largeobject&#95;metadata</code> Columns</strong>

<table border="1" class="table" summary="pg_largeobject_metadata Columns">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="catalog_table_entry">
<p class="column_definition">Column Type</p>
<p>Description</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oid</code> <code class="type">oid</code></p>
<p>Row identifier</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">lomowner</code> <code class="type">oid</code> (references <a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>Owner of the large object</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">lomacl</code> <code class="type">aclitem[]</code></p>
<p>Access privileges; see <a class="xref" href="../../the-sql-language/ddl/privileges.md">Section 5.7</a> for details</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/catalog-pg-largeobject-metadata.html)（英文原文，待翻譯）
