## 53.29. `pg_stats` [#](#VIEW-PG-STATS)

<a id="id-1.10.5.33.2"></a>

The view `pg_stats` provides access to
the information stored in the [`pg_statistic`](../catalogs/catalog-pg-statistic.md)
catalog. This view allows access only to rows of
[`pg_statistic`](../catalogs/catalog-pg-statistic.md) that correspond to tables the
user has permission to read, and therefore it is safe to allow public
read access to this view.

`pg_stats` is also designed to present the
information in a more readable format than the underlying catalog
— at the cost that its schema must be extended whenever new slot types
are defined for [`pg_statistic`](../catalogs/catalog-pg-statistic.md).

<a id="id-1.10.5.33.5"></a>

**Table 53.29. `pg_stats` Columns**

<table border="1" class="table" summary="pg_stats Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>)
      </p>
<p>
       Name of schema containing table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>)
      </p>
<p>
       Name of table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attname</code> <code class="type">name</code>
       (references <a class="link" href="../catalogs/catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attname</code>)
      </p>
<p>
       Name of column described by this row
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inherited</code> <code class="type">bool</code>
</p>
<p>
       If true, this row includes values from child tables, not just the
       values in the specified table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">null_frac</code> <code class="type">float4</code>
</p>
<p>
       Fraction of column entries that are null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">avg_width</code> <code class="type">int4</code>
</p>
<p>
       Average width in bytes of column's entries
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_distinct</code> <code class="type">float4</code>
</p>
<p>
       If greater than zero, the estimated number of distinct values in the
       column.  If less than zero, the negative of the number of distinct
       values divided by the number of rows.  (The negated form is used when
       <code class="command">ANALYZE</code> believes that the number of distinct values is
       likely to increase as the table grows; the positive form is used when
       the column seems to have a fixed number of possible values.)  For
       example, -1 indicates a unique column in which the number of distinct
       values is the same as the number of rows.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_vals</code> <code class="type">anyarray</code>
</p>
<p>
       A list of the most common values in the column. (Null if
       no values seem to be more common than any others.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_freqs</code> <code class="type">float4[]</code>
</p>
<p>
       A list of the frequencies of the most common values,
       i.e., number of occurrences of each divided by total number of rows.
       (Null when <code class="structfield">most_common_vals</code> is.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">histogram_bounds</code> <code class="type">anyarray</code>
</p>
<p>
       A list of values that divide the column's values into groups of
       approximately equal population.  The values in
       <code class="structfield">most_common_vals</code>, if present, are omitted from this
       histogram calculation.  (This column is null if the column data type
       does not have a <code class="literal">&lt;</code> operator or if the
       <code class="structfield">most_common_vals</code> list accounts for the entire
       population.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">correlation</code> <code class="type">float4</code>
</p>
<p>
       Statistical correlation between physical row ordering and
       logical ordering of the column values.  This ranges from -1 to +1.
       When the value is near -1 or +1, an index scan on the column will
       be estimated to be cheaper than when it is near zero, due to reduction
       of random access to the disk.  (This column is null if the column data
       type does not have a <code class="literal">&lt;</code> operator.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_elems</code> <code class="type">anyarray</code>
</p>
<p>
       A list of non-null element values most often appearing within values of
       the column. (Null for scalar types.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_elem_freqs</code> <code class="type">float4[]</code>
</p>
<p>
       A list of the frequencies of the most common element values, i.e., the
       fraction of rows containing at least one instance of the given value.
       Two or three additional values follow the per-element frequencies;
       these are the minimum and maximum of the preceding per-element
       frequencies, and optionally the frequency of null elements.
       (Null when <code class="structfield">most_common_elems</code> is.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">elem_count_histogram</code> <code class="type">float4[]</code>
</p>
<p>
       A histogram of the counts of distinct non-null element values within the
       values of the column, followed by the average number of distinct
       non-null elements.  (Null for scalar types.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">range_length_histogram</code> <code class="type">anyarray</code>
</p>
<p>
       A histogram of the lengths of non-empty and non-null range values of a
       range type column. (Null for non-range types.)
      </p>
<p>
       This histogram is calculated using the <code class="function">subtype_diff</code>
       range function regardless of whether range bounds are inclusive.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">range_empty_frac</code> <code class="type">float4</code>
</p>
<p>
       Fraction of column entries whose values are empty ranges.
       (Null for non-range types.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">range_bounds_histogram</code> <code class="type">anyarray</code>
</p>
<p>
       A histogram of lower and upper bounds of non-empty and non-null range
       values. (Null for non-range types.)
      </p>
<p>
       These two histograms are represented as a single array of ranges, whose
       lower bounds represent the histogram of lower bounds, and upper bounds
       represent the histogram of upper bounds.
      </p></td></tr></tbody></table>

<br>

The maximum number of entries in the array fields can be controlled on a
column-by-column basis using the [`ALTER
TABLE SET STATISTICS`](../../reference/sql-commands/sql-altertable.md)
command, or globally by setting the
[default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET) run-time parameter.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-stats.html)（英文原文，待翻譯）
