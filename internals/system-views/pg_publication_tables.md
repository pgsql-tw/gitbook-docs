<a id="VIEW-PG-PUBLICATION-TABLES"></a>

# 54.17. pg_publication_tables

<a id="id-1.10.5.21.2"></a>

The view `pg_publication_tables` provides information about the mapping between publications and information of tables they contain. Unlike the underlying catalog [`pg_publication_rel`](../system-catalogs/pg_publication_rel.md), this view expands publications defined as `FOR ALL TABLES` and `FOR TABLES IN SCHEMA`, so for such publications there will be a row for each eligible table.

<a id="id-1.10.5.21.4"></a>

<strong>Table 54.17. <code class="structname">pg&#95;publication&#95;tables</code> Columns</strong>

<table border="1" class="table" summary="pg_publication_tables Columns">
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
<p class="column_definition"><code class="structfield">pubname</code> <code class="type">name</code> (references <a class="link" href="../system-catalogs/pg_publication.md"><code class="structname">pg_publication</code></a>.<code class="structfield">pubname</code>)</p>
<p>Name of publication</p>
</td>
</tr>
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
<p class="column_definition"><code class="structfield">attnames</code> <code class="type">name[]</code> (references <a class="link" href="../system-catalogs/pg_attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attname</code>)</p>
<p>Names of table columns included in the publication. This contains all the columns of the table when the user didn't specify the column list for the table.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">rowfilter</code> <code class="type">text</code></p>
<p>Expression for the table's publication qualifying condition</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/view-pg-publication-tables.html)（英文原文，待翻譯）
