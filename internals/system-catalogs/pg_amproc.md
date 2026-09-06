<a id="CATALOG-PG-AMPROC"></a>

# 53.5. pg_amproc

<a id="id-1.10.4.7.2"></a>

The catalog `pg_amproc` stores information about support functions associated with access method operator families. There is one row for each support function belonging to an operator family.

<a id="id-1.10.4.7.4"></a>

<strong>Table 53.5. <code class="structname">pg&#95;amproc</code> Columns</strong>

<table border="1" class="table" summary="pg_amproc Columns">
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
<p class="column_definition"><code class="structfield">amprocfamily</code> <code class="type">oid</code> (references <a class="link" href="pg_opfamily.md"><code class="structname">pg_opfamily</code></a>.<code class="structfield">oid</code>)</p>
<p>The operator family this entry is for</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amproclefttype</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Left-hand input data type of associated operator</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amprocrighttype</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Right-hand input data type of associated operator</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amprocnum</code> <code class="type">int2</code></p>
<p>Support function number</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amproc</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>OID of the function</p>
</td>
</tr>
</tbody>
</table>



The usual interpretation of the `amproclefttype` and `amprocrighttype` fields is that they identify the left and right input types of the operator(s) that a particular support function supports. For some access methods these match the input data type(s) of the support function itself, for others not. There is a notion of “default” support functions for an index, which are those with `amproclefttype` and `amprocrighttype` both equal to the index operator class's `opcintype`.

---

原文：[PostgreSQL 15.19 Documentation](pg_amproc.md)（英文原文，待翻譯）
