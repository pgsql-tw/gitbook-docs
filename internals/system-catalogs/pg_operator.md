<a id="CATALOG-PG-OPERATOR"></a>

# 53.34. pg_operator

<a id="id-1.10.4.36.2"></a>

The catalog `pg_operator` stores information about operators. See [CREATE OPERATOR](../../reference/sql-commands/create-operator.md) and [Section 38.14](../../server-programming/extending-sql/user-defined-operators.md) for more information.

<a id="id-1.10.4.36.4"></a>

<strong>Table 53.34. <code class="structname">pg&#95;operator</code> Columns</strong>

<table border="1" class="table" summary="pg_operator Columns">
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
<p class="column_definition"><code class="structfield">oprname</code> <code class="type">name</code></p>
<p>Name of the operator</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprnamespace</code> <code class="type">oid</code> (references <a class="link" href="pg_namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the namespace that contains this operator</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprowner</code> <code class="type">oid</code> (references <a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>Owner of the operator</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprkind</code> <code class="type">char</code></p>
<p><code class="literal">b</code> = infix operator (<span class="quote">“<span class="quote">both</span>”</span>), or <code class="literal">l</code> = prefix operator (<span class="quote">“<span class="quote">left</span>”</span>)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprcanmerge</code> <code class="type">bool</code></p>
<p>This operator supports merge joins</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprcanhash</code> <code class="type">bool</code></p>
<p>This operator supports hash joins</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprleft</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Type of the left operand (zero for a prefix operator)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprright</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Type of the right operand</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprresult</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Type of the result (zero for a not-yet-defined <span class="quote">“<span class="quote">shell</span>”</span> operator)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprcom</code> <code class="type">oid</code> (references <a class="link" href="pg_operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>)</p>
<p>Commutator of this operator (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprnegate</code> <code class="type">oid</code> (references <a class="link" href="pg_operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>)</p>
<p>Negator of this operator (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprcode</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Function that implements this operator (zero for a not-yet-defined <span class="quote">“<span class="quote">shell</span>”</span> operator)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprrest</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Restriction selectivity estimation function for this operator (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">oprjoin</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Join selectivity estimation function for this operator (zero if none)</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_operator.md)（英文原文，待翻譯）
