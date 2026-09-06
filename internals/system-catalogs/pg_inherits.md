<a id="CATALOG-PG-INHERITS"></a>

# 53.27. pg_inherits

<a id="id-1.10.4.29.2"></a>

The catalog `pg_inherits` records information about table and index inheritance hierarchies. There is one entry for each direct parent-child table or index relationship in the database. (Indirect inheritance can be determined by following chains of entries.)

<a id="id-1.10.4.29.4"></a>

<strong>Table 53.27. <code class="structname">pg&#95;inherits</code> Columns</strong>

<table border="1" class="table" summary="pg_inherits Columns">
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
<p class="column_definition"><code class="structfield">inhrelid</code> <code class="type">oid</code> (references <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the child table or index</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">inhparent</code> <code class="type">oid</code> (references <a class="link" href="pg_class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the parent table or index</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">inhseqno</code> <code class="type">int4</code></p>
<p>If there is more than one direct parent for a child table (multiple inheritance), this number tells the order in which the inherited columns are to be arranged. The count starts at 1.</p>
<p>Indexes cannot have multiple inheritance, since they can only inherit when using declarative partitioning.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">inhdetachpending</code> <code class="type">bool</code></p>
<p><code class="literal">true</code> for a partition that is in the process of being detached; <code class="literal">false</code> otherwise.</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/catalog-pg-inherits.html)（英文原文，待翻譯）
