<a id="VIEW-PG-RULES"></a>

# 54.21. pg_rules

<a id="id-1.10.5.25.2"></a>

The view `pg_rules` provides access to useful information about query rewrite rules.

<a id="id-1.10.5.25.4"></a>

<strong>Table 54.21. <code class="structname">pg&#95;rules</code> Columns</strong>

<table border="1" class="table" summary="pg_rules Columns">
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
<p>Name of table the rule is for</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">rulename</code> <code class="type">name</code> (references <a class="link" href="../system-catalogs/51.44.-pg_rewrite.md"><code class="structname">pg_rewrite</code></a>.<code class="structfield">rulename</code>)</p>
<p>Name of rule</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">definition</code> <code class="type">text</code></p>
<p>Rule definition (a reconstructed creation command)</p>
</td>
</tr>
</tbody>
</table>



The `pg_rules` view excludes the `ON SELECT` rules of views and materialized views; those can be seen in [`pg_views`](pg_views.md) and [`pg_matviews`](pg_matviews.md).

---

原文：[PostgreSQL 15.19 Documentation](pg_rules.md)（英文原文，待翻譯）
