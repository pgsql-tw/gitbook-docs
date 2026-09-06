<a id="CATALOG-PG-TRANSFORM"></a>

# 53.57. pg_transform

<a id="id-1.10.4.59.2"></a>

The catalog `pg_transform` stores information about transforms, which are a mechanism to adapt data types to procedural languages. See [CREATE TRANSFORM](../../reference/sql-commands/create-transform.md) for more information.

<a id="id-1.10.4.59.4"></a>

<strong>Table 53.57. <code class="structname">pg&#95;transform</code> Columns</strong>

<table border="1" class="table" summary="pg_transform Columns">
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
<p class="column_definition"><code class="structfield">trftype</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>OID of the data type this transform is for</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">trflang</code> <code class="type">oid</code> (references <a class="link" href="pg_language.md"><code class="structname">pg_language</code></a>.<code class="structfield">oid</code>)</p>
<p>OID of the language this transform is for</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">trffromsql</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the function to use when converting the data type for input to the procedural language (e.g., function parameters). Zero is stored if the default behavior should be used.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">trftosql</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the function to use when converting output from the procedural language (e.g., return values) to the data type. Zero is stored if the default behavior should be used.</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_transform.md)（英文原文，待翻譯）
