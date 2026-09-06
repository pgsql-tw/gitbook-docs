## 52.52. `pg_statistic_ext` [#](#CATALOG-PG-STATISTIC-EXT)

<a id="id-1.10.4.54.2"></a>

The catalog `pg_statistic_ext`
holds definitions of extended planner statistics.
Each row in this catalog corresponds to a *statistics object*
created with [`CREATE STATISTICS`](../../reference/sql-commands/sql-createstatistics.md).

<a id="id-1.10.4.54.4"></a>

**Table 52.52. `pg_statistic_ext` Columns**

<table border="1" class="table" summary="pg_statistic_ext Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       Row identifier
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Table containing the columns described by this object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxname</code> <code class="type">name</code>
</p>
<p>
       Name of the statistics object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxnamespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the namespace that contains this statistics object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the statistics object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxkeys</code> <code class="type">int2vector</code>
       (references <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>)
      </p>
<p>
       An array of attribute numbers, indicating which table columns are
       covered by this statistics object;
       for example a value of <code class="literal">1 3</code> would
       mean that the first and the third table columns are covered
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxstattarget</code> <code class="type">int2</code>
</p>
<p>
<code class="structfield">stxstattarget</code> controls the level of detail
       of statistics accumulated for this statistics object by
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a>.
       A zero value indicates that no statistics should be collected.
       A null value says to use the maximum of the statistics targets of
       the referenced columns, if set, or the system default statistics target.
       Positive values of <code class="structfield">stxstattarget</code>
       determine the target number of <span class="quote">“<span class="quote">most common values</span>”</span>
       to collect.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxkind</code> <code class="type">char[]</code>
</p>
<p>
       An array containing codes for the enabled statistics kinds;
       valid values are:
       <code class="literal">d</code> for n-distinct statistics,
       <code class="literal">f</code> for functional dependency statistics,
       <code class="literal">m</code> for most common values (MCV) list statistics, and
       <code class="literal">e</code> for expression statistics
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxexprs</code> <code class="type">pg_node_tree</code>
</p>
<p>
       Expression trees (in <code class="function">nodeToString()</code>
       representation) for statistics object attributes that are not simple
       column references.  This is a list with one element per expression.
       Null if all statistics object attributes are simple references.
      </p></td></tr></tbody></table>

<br>

The `pg_statistic_ext` entry is filled in
completely during [`CREATE STATISTICS`](../../reference/sql-commands/sql-createstatistics.md), but the actual
statistical values are not computed then.
Subsequent [`ANALYZE`](../../reference/sql-commands/sql-analyze.md) commands compute the desired values
and populate an entry in the
[`pg_statistic_ext_data`](catalog-pg-statistic-ext-data.md)
catalog.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-statistic-ext.html)（英文原文，待翻譯）
