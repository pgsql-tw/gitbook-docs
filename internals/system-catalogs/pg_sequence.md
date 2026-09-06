<a id="CATALOG-PG-SEQUENCE"></a>

# 53.47. pg_sequence

<a id="id-1.10.4.49.2"></a>

The catalog `pg_sequence` contains information about sequences. Some of the information about sequences, such as the name and the schema, is in [`pg_class`](pg_class.md)

<a id="id-1.10.4.49.4"></a>

<strong>Table 53.47. <code class="structname">pg&#95;sequence</code> Columns</strong>

<table border="1" class="table" summary="pg_sequence Columns">
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
<p class="column_definition"><code class="structfield">seqrelid</code> <code class="type">oid</code> (references <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a> entry for this sequence</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">seqtypid</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Data type of the sequence</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">seqstart</code> <code class="type">int8</code></p>
<p>Start value of the sequence</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">seqincrement</code> <code class="type">int8</code></p>
<p>Increment value of the sequence</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">seqmax</code> <code class="type">int8</code></p>
<p>Maximum value of the sequence</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">seqmin</code> <code class="type">int8</code></p>
<p>Minimum value of the sequence</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">seqcache</code> <code class="type">int8</code></p>
<p>Cache size of the sequence</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">seqcycle</code> <code class="type">bool</code></p>
<p>Whether the sequence cycles</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/catalog-pg-sequence.html)（英文原文，待翻譯）
