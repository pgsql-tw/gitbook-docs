<a id="INFOSCHEMA-ROUTINE-TABLE-USAGE"></a>

# 37.44. routine_table_usage

The view `routine_table_usage` is meant to identify all tables that are used by a function or procedure. This information is currently not tracked by PostgreSQL.

<a id="id-1.7.6.48.3"></a>

<strong>Table 37.42. <code class="literal">routine&#95;table&#95;usage</code> Columns</strong>

<table border="1" class="table" summary="routine_table_usage Columns">
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
<p class="column_definition"><code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code></p>
<p>Name of the database containing the function (always the current database)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">specific_schema</code> <code class="type">sql_identifier</code></p>
<p>Name of the schema containing the function</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">specific_name</code> <code class="type">sql_identifier</code></p>
<p>The <span class="quote">“<span class="quote">specific name</span>”</span> of the function. See <a class="xref" href="36.40.-routines.md">Section 37.45</a> for more information.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">routine_catalog</code> <code class="type">sql_identifier</code></p>
<p>Name of the database containing the function (always the current database)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">routine_schema</code> <code class="type">sql_identifier</code></p>
<p>Name of the schema containing the function</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">routine_name</code> <code class="type">sql_identifier</code></p>
<p>Name of the function (might be duplicated in case of overloading)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">table_catalog</code> <code class="type">sql_identifier</code></p>
<p>Name of the database that contains the table that is used by the function (always the current database)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">table_schema</code> <code class="type">sql_identifier</code></p>
<p>Name of the schema that contains the table that is used by the function</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">table_name</code> <code class="type">sql_identifier</code></p>
<p>Name of the table that is used by the function</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](routine_table_usage.md)（英文原文，待翻譯）
