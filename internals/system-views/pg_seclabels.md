<a id="VIEW-PG-SECLABELS"></a>

# 54.22. pg_seclabels

<a id="id-1.10.5.26.2"></a>

The view `pg_seclabels` provides information about security labels. It as an easier-to-query version of the [`pg_seclabel`](../system-catalogs/pg_seclabel.md) catalog.

<a id="id-1.10.5.26.4"></a>

<strong>Table 54.22. <code class="structname">pg&#95;seclabels</code> Columns</strong>

<table border="1" class="table" summary="pg_seclabels Columns">
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
<p class="column_definition"><code class="structfield">objoid</code> <code class="type">oid</code> (references any OID column)</p>
<p>The OID of the object this security label pertains to</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">classoid</code> <code class="type">oid</code> (references <a class="link" href="../system-catalogs/pg_class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the system catalog this object appears in</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">objsubid</code> <code class="type">int4</code></p>
<p>For a security label on a table column, this is the column number (the <code class="structfield">objoid</code> and <code class="structfield">classoid</code> refer to the table itself). For all other object types, this column is zero.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">objtype</code> <code class="type">text</code></p>
<p>The type of object to which this label applies, as text.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">objnamespace</code> <code class="type">oid</code> (references <a class="link" href="../system-catalogs/pg_namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the namespace for this object, if applicable; otherwise NULL.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">objname</code> <code class="type">text</code></p>
<p>The name of the object to which this label applies, as text.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">provider</code> <code class="type">text</code> (references <a class="link" href="../system-catalogs/pg_seclabel.md"><code class="structname">pg_seclabel</code></a>.<code class="structfield">provider</code>)</p>
<p>The label provider associated with this label.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">label</code> <code class="type">text</code> (references <a class="link" href="../system-catalogs/pg_seclabel.md"><code class="structname">pg_seclabel</code></a>.<code class="structfield">label</code>)</p>
<p>The security label applied to this object.</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_seclabels.md)（英文原文，待翻譯）
