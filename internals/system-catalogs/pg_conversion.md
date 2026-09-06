<a id="CATALOG-PG-CONVERSION"></a>

# 53.14. pg_conversion

<a id="id-1.10.4.16.2"></a>

The catalog `pg_conversion` describes encoding conversion functions. See [CREATE CONVERSION](../../reference/sql-commands/create-conversion.md) for more information.

<a id="id-1.10.4.16.4"></a>

<strong>Table 53.14. <code class="structname">pg&#95;conversion</code> Columns</strong>

<table border="1" class="table" summary="pg_conversion Columns">
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
<p class="column_definition"><code class="structfield">conname</code> <code class="type">name</code></p>
<p>Conversion name (unique within a namespace)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">connamespace</code> <code class="type">oid</code> (references <a class="link" href="pg_namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the namespace that contains this conversion</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">conowner</code> <code class="type">oid</code> (references <a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>Owner of the conversion</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">conforencoding</code> <code class="type">int4</code></p>
<p>Source encoding ID (<a class="link" href="../../the-sql-language/functions-and-operators/system-information-functions.md#PG-ENCODING-TO-CHAR"><code class="function">pg_encoding_to_char()</code></a> can translate this number to the encoding name)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">contoencoding</code> <code class="type">int4</code></p>
<p>Destination encoding ID (<a class="link" href="../../the-sql-language/functions-and-operators/system-information-functions.md#PG-ENCODING-TO-CHAR"><code class="function">pg_encoding_to_char()</code></a> can translate this number to the encoding name)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">conproc</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Conversion function</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">condefault</code> <code class="type">bool</code></p>
<p>True if this is the default conversion</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_conversion.md)（英文原文，待翻譯）
