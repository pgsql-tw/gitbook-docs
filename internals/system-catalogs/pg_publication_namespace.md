<a id="CATALOG-PG-PUBLICATION-NAMESPACE"></a>

# 53.41. pg_publication_namespace

<a id="id-1.10.4.43.2"></a>

The catalog `pg_publication_namespace` contains the mapping between schemas and publications in the database. This is a many-to-many mapping.

<a id="id-1.10.4.43.4"></a>

<strong>Table 53.41. <code class="structname">pg&#95;publication&#95;namespace</code> Columns</strong>

<table border="1" class="table" summary="pg_publication_namespace Columns">
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
<p class="column_definition"><code class="structfield">pnpubid</code> <code class="type">oid</code> (references <a class="link" href="pg_publication.md"><code class="structname">pg_publication</code></a>.<code class="structfield">oid</code>)</p>
<p>Reference to publication</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">pnnspid</code> <code class="type">oid</code> (references <a class="link" href="pg_namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)</p>
<p>Reference to schema</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/catalog-pg-publication-namespace.html)（英文原文，待翻譯）
