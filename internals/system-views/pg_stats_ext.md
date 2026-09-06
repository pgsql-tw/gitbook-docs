<a id="VIEW-PG-STATS-EXT"></a>

# 54.28. pg_stats_ext

<a id="id-1.10.5.32.2"></a>

The view `pg_stats_ext` provides access to information about each extended statistics object in the database, combining information stored in the [`pg_statistic_ext`](../system-catalogs/pg_statistic_ext.md) and [`pg_statistic_ext_data`](../system-catalogs/pg_statistic_ext_data.md) catalogs. This view allows access only to rows of [`pg_statistic_ext`](../system-catalogs/pg_statistic_ext.md) and [`pg_statistic_ext_data`](../system-catalogs/pg_statistic_ext_data.md) that correspond to tables the user owns, and therefore it is safe to allow public read access to this view.

`pg_stats_ext` is also designed to present the information in a more readable format than the underlying catalogs — at the cost that its schema must be extended whenever new types of extended statistics are added to [`pg_statistic_ext`](../system-catalogs/pg_statistic_ext.md).

<a id="id-1.10.5.32.5"></a>

<strong>Table 54.28. <code class="structname">pg&#95;stats&#95;ext</code> Columns</strong>

<table border="1" class="table" summary="pg_stats_ext Columns">
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
<p>Name of table</p>
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
<p class="column_definition"><code class="structfield">attnames</code> <code class="type">name[]</code> (references <a class="link" href="../system-catalogs/pg_attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attname</code>)</p>
<p>Names of the columns included in the extended statistics object</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">exprs</code> <code class="type">text[]</code></p>
<p>Expressions included in the extended statistics object</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">kinds</code> <code class="type">char[]</code></p>
<p>Types of extended statistics object enabled for this record</p>
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
<p class="column_definition"><code class="structfield">n_distinct</code> <code class="type">pg_ndistinct</code></p>
<p>N-distinct counts for combinations of column values. If greater than zero, the estimated number of distinct values in the combination. If less than zero, the negative of the number of distinct values divided by the number of rows. (The negated form is used when <code class="command">ANALYZE</code> believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the column seems to have a fixed number of possible values.) For example, -1 indicates a unique combination of columns in which the number of distinct combinations is the same as the number of rows.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">dependencies</code> <code class="type">pg_dependencies</code></p>
<p>Functional dependency statistics</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">most_common_vals</code> <code class="type">text[]</code></p>
<p>A list of the most common combinations of values in the columns. (Null if no combinations seem to be more common than any others.)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">most_common_val_nulls</code> <code class="type">bool[]</code></p>
<p>A list of NULL flags for the most common combinations of values. (Null when <code class="structfield">most_common_vals</code> is.)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">most_common_freqs</code> <code class="type">float8[]</code></p>
<p>A list of the frequencies of the most common combinations, i.e., number of occurrences of each divided by total number of rows. (Null when <code class="structfield">most_common_vals</code> is.)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">most_common_base_freqs</code> <code class="type">float8[]</code></p>
<p>A list of the base frequencies of the most common combinations, i.e., product of per-value frequencies. (Null when <code class="structfield">most_common_vals</code> is.)</p>
</td>
</tr>
</tbody>
</table>



The maximum number of entries in the array fields can be controlled on a column-by-column basis using the [`ALTER TABLE SET STATISTICS`](../../reference/sql-commands/alter-table.md) command, or globally by setting the [default_statistics_target](https://www.postgresql.org/docs/15/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET) run-time parameter.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/view-pg-stats-ext.html)（英文原文，待翻譯）
