<a id="CATALOG-PG-PARTITIONED-TABLE"></a>

# 53.37. pg_partitioned_table

<a id="id-1.10.4.39.2"></a>

The catalog `pg_partitioned_table` stores information about how tables are partitioned.

<a id="id-1.10.4.39.4"></a>

<strong>Table 53.37. <code class="structname">pg&#95;partitioned&#95;table</code> Columns</strong>

<table border="1" class="table" summary="pg_partitioned_table Columns">
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
<p class="column_definition"><code class="structfield">partrelid</code> <code class="type">oid</code> (references <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a> entry for this partitioned table</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">partstrat</code> <code class="type">char</code></p>
<p>Partitioning strategy; <code class="literal">h</code> = hash partitioned table, <code class="literal">l</code> = list partitioned table, <code class="literal">r</code> = range partitioned table</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">partnatts</code> <code class="type">int2</code></p>
<p>The number of columns in the partition key</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">partdefid</code> <code class="type">oid</code> (references <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a> entry for the default partition of this partitioned table, or zero if this partitioned table does not have a default partition</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">partattrs</code> <code class="type">int2vector</code> (references <a class="link" href="pg_attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>)</p>
<p>This is an array of <code class="structfield">partnatts</code> values that indicate which table columns are part of the partition key. For example, a value of <code class="literal">1 3</code> would mean that the first and the third table columns make up the partition key. A zero in this array indicates that the corresponding partition key column is an expression, rather than a simple column reference.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">partclass</code> <code class="type">oidvector</code> (references <a class="link" href="pg_opclass.md"><code class="structname">pg_opclass</code></a>.<code class="structfield">oid</code>)</p>
<p>For each column in the partition key, this contains the OID of the operator class to use. See <a class="link" href="pg_opclass.md"><code class="structname">pg_opclass</code></a> for details.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">partcollation</code> <code class="type">oidvector</code> (references <a class="link" href="pg_collation.md"><code class="structname">pg_collation</code></a>.<code class="structfield">oid</code>)</p>
<p>For each column in the partition key, this contains the OID of the collation to use for partitioning, or zero if the column is not of a collatable data type.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">partexprs</code> <code class="type">pg_node_tree</code></p>
<p>Expression trees (in <code class="function">nodeToString()</code> representation) for partition key columns that are not simple column references. This is a list with one element for each zero entry in <code class="structfield">partattrs</code>. Null if all partition key columns are simple references.</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_partitioned_table.md)（英文原文，待翻譯）
