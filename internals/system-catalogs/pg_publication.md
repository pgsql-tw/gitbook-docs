<a id="CATALOG-PG-PUBLICATION"></a>

# 53.40. pg_publication

<a id="id-1.10.4.42.2"></a>

The catalog `pg_publication` contains all publications created in the database. For more on publications see [Section 31.1](../../server-administration/logical-replication/publication.md).

<a id="id-1.10.4.42.4"></a>

<strong>Table 53.40. <code class="structname">pg&#95;publication</code> Columns</strong>

<table border="1" class="table" summary="pg_publication Columns">
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
<p class="column_definition"><code class="structfield">pubname</code> <code class="type">name</code></p>
<p>Name of the publication</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">pubowner</code> <code class="type">oid</code> (references <a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>Owner of the publication</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">puballtables</code> <code class="type">bool</code></p>
<p>If true, this publication automatically includes all tables in the database, including any that will be created in the future.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">pubinsert</code> <code class="type">bool</code></p>
<p>If true, <a class="xref" href="../../reference/sql-commands/insert.md"><span class="refentrytitle">INSERT</span></a> operations are replicated for tables in the publication.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">pubupdate</code> <code class="type">bool</code></p>
<p>If true, <a class="xref" href="../../reference/sql-commands/update.md"><span class="refentrytitle">UPDATE</span></a> operations are replicated for tables in the publication.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">pubdelete</code> <code class="type">bool</code></p>
<p>If true, <a class="xref" href="../../reference/sql-commands/delete.md"><span class="refentrytitle">DELETE</span></a> operations are replicated for tables in the publication.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">pubtruncate</code> <code class="type">bool</code></p>
<p>If true, <a class="xref" href="../../reference/sql-commands/truncate.md"><span class="refentrytitle">TRUNCATE</span></a> operations are replicated for tables in the publication.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">pubviaroot</code> <code class="type">bool</code></p>
<p>If true, operations on a leaf partition are replicated using the identity and schema of its topmost partitioned ancestor mentioned in the publication instead of its own.</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_publication.md)（英文原文，待翻譯）
