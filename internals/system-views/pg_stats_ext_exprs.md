<a id="VIEW-PG-STATS-EXT-EXPRS"></a>

# 54.29. pg_stats_ext_exprs

<a id="id-1.10.5.33.2"></a>

The view `pg_stats_ext_exprs` provides access to information about all expressions included in extended statistics objects, combining information stored in the [`pg_statistic_ext`](../system-catalogs/pg_statistic_ext.md) and [`pg_statistic_ext_data`](../system-catalogs/pg_statistic_ext_data.md) catalogs. This view allows access only to rows of [`pg_statistic_ext`](../system-catalogs/pg_statistic_ext.md) and [`pg_statistic_ext_data`](../system-catalogs/pg_statistic_ext_data.md) that correspond to tables the user owns, and therefore it is safe to allow public read access to this view.

`pg_stats_ext_exprs` is also designed to present the information in a more readable format than the underlying catalogs — at the cost that its schema must be extended whenever the structure of statistics in `pg_statistic_ext` changes.

<a id="id-1.10.5.33.5"></a>

<strong>Table 54.29. <code class="structname">pg&#95;stats&#95;ext&#95;exprs</code> Columns</strong>

<table border="1" class="table" summary="pg_stats_ext_exprs Columns">
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
<p class="column_definition"><code class="structfield">schemaname</code> <code class="type">name</code> (references <a class="link" href="../system-catalogs/pg_namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>)</p>
<p>Name of schema containing table</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">tablename</code> <code class="type">name</code> (references <a class="link" href="../system-catalogs/pg_class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>)</p>
<p>Name of table the statistics object is defined on</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">statistics_schemaname</code> <code class="type">name</code> (references <a class="link" href="../system-catalogs/pg_namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>)</p>
<p>Name of schema containing extended statistics object</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">statistics_name</code> <code class="type">name</code> (references <a class="link" href="../system-catalogs/pg_statistic_ext.md"><code class="structname">pg_statistic_ext</code></a>.<code class="structfield">stxname</code>)</p>
<p>Name of extended statistics object</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">statistics_owner</code> <code class="type">name</code> (references <a class="link" href="../system-catalogs/pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>)</p>
<p>Owner of the extended statistics object</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">expr</code> <code class="type">text</code></p>
<p>Expression included in the extended statistics object</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">inherited</code> <code class="type">bool</code> (references <a class="link" href="../system-catalogs/pg_statistic_ext_data.md"><code class="structname">pg_statistic_ext_data</code></a>.<code class="structfield">stxdinherit</code>)</p>
<p>If true, the stats include values from child tables, not just the values in the specified relation</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">null_frac</code> <code class="type">float4</code></p>
<p>Fraction of expression entries that are null</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">avg_width</code> <code class="type">int4</code></p>
<p>Average width in bytes of expression's entries</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">n_distinct</code> <code class="type">float4</code></p>
<p>If greater than zero, the estimated number of distinct values in the expression. If less than zero, the negative of the number of distinct values divided by the number of rows. (The negated form is used when <code class="command">ANALYZE</code> believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the expression seems to have a fixed number of possible values.) For example, -1 indicates a unique expression in which the number of distinct values is the same as the number of rows.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">most_common_vals</code> <code class="type">anyarray</code></p>
<p>A list of the most common values in the expression. (Null if no values seem to be more common than any others.)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">most_common_freqs</code> <code class="type">float4[]</code></p>
<p>A list of the frequencies of the most common values, i.e., number of occurrences of each divided by total number of rows. (Null when <code class="structfield">most_common_vals</code> is.)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">histogram_bounds</code> <code class="type">anyarray</code></p>
<p>A list of values that divide the expression's values into groups of approximately equal population. The values in <code class="structfield">most_common_vals</code>, if present, are omitted from this histogram calculation. (This expression is null if the expression data type does not have a <code class="literal">&lt;</code> operator or if the <code class="structfield">most_common_vals</code> list accounts for the entire population.)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">correlation</code> <code class="type">float4</code></p>
<p>Statistical correlation between physical row ordering and logical ordering of the expression values. This ranges from -1 to +1. When the value is near -1 or +1, an index scan on the expression will be estimated to be cheaper than when it is near zero, due to reduction of random access to the disk. (This expression is null if the expression's data type does not have a <code class="literal">&lt;</code> operator.)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">most_common_elems</code> <code class="type">anyarray</code></p>
<p>A list of non-null element values most often appearing within values of the expression. (Null for scalar types.)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">most_common_elem_freqs</code> <code class="type">float4[]</code></p>
<p>A list of the frequencies of the most common element values, i.e., the fraction of rows containing at least one instance of the given value. Two or three additional values follow the per-element frequencies; these are the minimum and maximum of the preceding per-element frequencies, and optionally the frequency of null elements. (Null when <code class="structfield">most_common_elems</code> is.)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">elem_count_histogram</code> <code class="type">float4[]</code></p>
<p>A histogram of the counts of distinct non-null element values within the values of the expression, followed by the average number of distinct non-null elements. (Null for scalar types.)</p>
</td>
</tr>
</tbody>
</table>



The maximum number of entries in the array fields can be controlled on a column-by-column basis using the [`ALTER TABLE SET STATISTICS`](../../reference/sql-commands/alter-table.md) command, or globally by setting the [default_statistics_target](https://www.postgresql.org/docs/15/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET) run-time parameter.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/view-pg-stats-ext-exprs.html)（英文原文，待翻譯）
