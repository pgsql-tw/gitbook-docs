<a id="CATALOG-PG-AMOP"></a>

# 53.4. pg_amop

<a id="id-1.10.4.6.2"></a>

The catalog `pg_amop` stores information about operators associated with access method operator families. There is one row for each operator that is a member of an operator family. A family member can be either a <em class="firstterm">search</em> operator or an <em class="firstterm">ordering</em> operator. An operator can appear in more than one family, but cannot appear in more than one search position nor more than one ordering position within a family. (It is allowed, though unlikely, for an operator to be used for both search and ordering purposes.)

<a id="id-1.10.4.6.4"></a>

<strong>Table 53.4. <code class="structname">pg&#95;amop</code> Columns</strong>

<table border="1" class="table" summary="pg_amop Columns">
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
<p class="column_definition"><code class="structfield">amopfamily</code> <code class="type">oid</code> (references <a class="link" href="pg_opfamily.md"><code class="structname">pg_opfamily</code></a>.<code class="structfield">oid</code>)</p>
<p>The operator family this entry is for</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amoplefttype</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Left-hand input data type of operator</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amoprighttype</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Right-hand input data type of operator</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amopstrategy</code> <code class="type">int2</code></p>
<p>Operator strategy number</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amoppurpose</code> <code class="type">char</code></p>
<p>Operator purpose, either <code class="literal">s</code> for search or <code class="literal">o</code> for ordering</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amopopr</code> <code class="type">oid</code> (references <a class="link" href="pg_operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>)</p>
<p>OID of the operator</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amopmethod</code> <code class="type">oid</code> (references <a class="link" href="pg_am.md"><code class="structname">pg_am</code></a>.<code class="structfield">oid</code>)</p>
<p>Index access method operator family is for</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">amopsortfamily</code> <code class="type">oid</code> (references <a class="link" href="pg_opfamily.md"><code class="structname">pg_opfamily</code></a>.<code class="structfield">oid</code>)</p>
<p>The B-tree operator family this entry sorts according to, if an ordering operator; zero if a search operator</p>
</td>
</tr>
</tbody>
</table>



A “search” operator entry indicates that an index of this operator family can be searched to find all rows satisfying `WHERE` <em class="replaceable"><code>indexed&#95;column</code></em> <em class="replaceable"><code>operator</code></em> <em class="replaceable"><code>constant</code></em>. Obviously, such an operator must return `boolean`, and its left-hand input type must match the index's column data type.

An “ordering” operator entry indicates that an index of this operator family can be scanned to return rows in the order represented by `ORDER BY` <em class="replaceable"><code>indexed&#95;column</code></em> <em class="replaceable"><code>operator</code></em> <em class="replaceable"><code>constant</code></em>. Such an operator could return any sortable data type, though again its left-hand input type must match the index's column data type. The exact semantics of the `ORDER BY` are specified by the `amopsortfamily` column, which must reference a B-tree operator family for the operator's result type.

## Note

At present, it's assumed that the sort order for an ordering operator is the default for the referenced operator family, i.e., `ASC NULLS LAST`. This might someday be relaxed by adding additional columns to specify sort options explicitly.

An entry's `amopmethod` must match the `opfmethod` of its containing operator family (including `amopmethod` here is an intentional denormalization of the catalog structure for performance reasons). Also, `amoplefttype` and `amoprighttype` must match the `oprleft` and `oprright` fields of the referenced [`pg_operator`](pg_operator.md) entry.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/catalog-pg-amop.html)（英文原文，待翻譯）
