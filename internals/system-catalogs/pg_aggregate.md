<a id="CATALOG-PG-AGGREGATE"></a>

# 53.2. pg_aggregate

<a id="id-1.10.4.4.2"></a>

The catalog `pg_aggregate` stores information about aggregate functions. An aggregate function is a function that operates on a set of values (typically one column from each row that matches a query condition) and returns a single value computed from all these values. Typical aggregate functions are `sum`, `count`, and `max`. Each entry in `pg_aggregate` is an extension of an entry in [`pg_proc`](pg_proc.md). The `pg_proc` entry carries the aggregate's name, input and output data types, and other information that is similar to ordinary functions.

<a id="id-1.10.4.4.4"></a>

<strong>Table 53.2. <code class="structname">pg&#95;aggregate</code> Columns</strong>

<table border="1" class="table" summary="pg_aggregate Columns">
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
<p class="column_definition"><code class="structfield">aggfnoid</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p><code class="structname">pg_proc</code> OID of the aggregate function</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggkind</code> <code class="type">char</code></p>
<p>Aggregate kind: <code class="literal">n</code> for <span class="quote">“<span class="quote">normal</span>”</span> aggregates, <code class="literal">o</code> for <span class="quote">“<span class="quote">ordered-set</span>”</span> aggregates, or <code class="literal">h</code> for <span class="quote">“<span class="quote">hypothetical-set</span>”</span> aggregates</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggnumdirectargs</code> <code class="type">int2</code></p>
<p>Number of direct (non-aggregated) arguments of an ordered-set or hypothetical-set aggregate, counting a variadic array as one argument. If equal to <code class="structfield">pronargs</code>, the aggregate must be variadic and the variadic array describes the aggregated arguments as well as the final direct arguments. Always zero for normal aggregates.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggtransfn</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Transition function</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggfinalfn</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Final function (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggcombinefn</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Combine function (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggserialfn</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Serialization function (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggdeserialfn</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Deserialization function (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggmtransfn</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Forward transition function for moving-aggregate mode (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggminvtransfn</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Inverse transition function for moving-aggregate mode (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggmfinalfn</code> <code class="type">regproc</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>Final function for moving-aggregate mode (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggfinalextra</code> <code class="type">bool</code></p>
<p>True to pass extra dummy arguments to <code class="structfield">aggfinalfn</code></p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggmfinalextra</code> <code class="type">bool</code></p>
<p>True to pass extra dummy arguments to <code class="structfield">aggmfinalfn</code></p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggfinalmodify</code> <code class="type">char</code></p>
<p>Whether <code class="structfield">aggfinalfn</code> modifies the transition state value: <code class="literal">r</code> if it is read-only, <code class="literal">s</code> if the <code class="structfield">aggtransfn</code> cannot be applied after the <code class="structfield">aggfinalfn</code>, or <code class="literal">w</code> if it writes on the value</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggmfinalmodify</code> <code class="type">char</code></p>
<p>Like <code class="structfield">aggfinalmodify</code>, but for the <code class="structfield">aggmfinalfn</code></p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggsortop</code> <code class="type">oid</code> (references <a class="link" href="pg_operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>)</p>
<p>Associated sort operator (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggtranstype</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Data type of the aggregate function's internal transition (state) data</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggtransspace</code> <code class="type">int4</code></p>
<p>Approximate average size (in bytes) of the transition state data, or zero to use a default estimate</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggmtranstype</code> <code class="type">oid</code> (references <a class="link" href="pg_type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)</p>
<p>Data type of the aggregate function's internal transition (state) data for moving-aggregate mode (zero if none)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggmtransspace</code> <code class="type">int4</code></p>
<p>Approximate average size (in bytes) of the transition state data for moving-aggregate mode, or zero to use a default estimate</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">agginitval</code> <code class="type">text</code></p>
<p>The initial value of the transition state. This is a text field containing the initial value in its external string representation. If this field is null, the transition state value starts out null.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">aggminitval</code> <code class="type">text</code></p>
<p>The initial value of the transition state for moving-aggregate mode. This is a text field containing the initial value in its external string representation. If this field is null, the transition state value starts out null.</p>
</td>
</tr>
</tbody>
</table>



New aggregate functions are registered with the [`CREATE AGGREGATE`](../../reference/sql-commands/create-aggregate.md) command. See [Section 38.12](../../server-programming/extending-sql/user-defined-aggregates.md) for more information about writing aggregate functions and the meaning of the transition functions, etc.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/catalog-pg-aggregate.html)（英文原文，待翻譯）
