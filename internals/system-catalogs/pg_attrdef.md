<a id="CATALOG-PG-ATTRDEF"></a>

# 53.6. pg_attrdef

<a id="id-1.10.4.8.2"></a>

The catalog `pg_attrdef` stores column default values. The main information about columns is stored in [`pg_attribute`](pg_attribute.md). Only columns for which a default value has been explicitly set will have an entry here.

<a id="id-1.10.4.8.4"></a>

<strong>Table 53.6. <code class="structname">pg&#95;attrdef</code> Columns</strong>

<table border="1" class="table" summary="pg_attrdef Columns">
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
<p class="column_definition"><code class="structfield">adrelid</code> <code class="type">oid</code> (references <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)</p>
<p>The table this column belongs to</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">adnum</code> <code class="type">int2</code> (references <a class="link" href="pg_attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>)</p>
<p>The number of the column</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">adbin</code> <code class="type">pg_node_tree</code></p>
<p>The column default value, in <code class="function">nodeToString()</code> representation. Use <code class="literal">pg_get_expr(adbin, adrelid)</code> to convert it to an SQL expression.</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_attrdef.md)（英文原文，待翻譯）
