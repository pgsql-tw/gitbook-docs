<a id="CATALOG-PG-FOREIGN-DATA-WRAPPER"></a>

# 53.23. pg_foreign_data_wrapper

<a id="id-1.10.4.25.2"></a>

The catalog `pg_foreign_data_wrapper` stores foreign-data wrapper definitions. A foreign-data wrapper is the mechanism by which external data, residing on foreign servers, is accessed.

<a id="id-1.10.4.25.4"></a>

<strong>Table 53.23. <code class="structname">pg&#95;foreign&#95;data&#95;wrapper</code> Columns</strong>

<table border="1" class="table" summary="pg_foreign_data_wrapper Columns">
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
<p class="column_definition"><code class="structfield">fdwname</code> <code class="type">name</code></p>
<p>Name of the foreign-data wrapper</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">fdwowner</code> <code class="type">oid</code> (references <a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>Owner of the foreign-data wrapper</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">fdwhandler</code> <code class="type">oid</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>References a handler function that is responsible for supplying execution routines for the foreign-data wrapper. Zero if no handler is provided</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">fdwvalidator</code> <code class="type">oid</code> (references <a class="link" href="pg_proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)</p>
<p>References a validator function that is responsible for checking the validity of the options given to the foreign-data wrapper, as well as options for foreign servers and user mappings using the foreign-data wrapper. Zero if no validator is provided</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">fdwacl</code> <code class="type">aclitem[]</code></p>
<p>Access privileges; see <a class="xref" href="../../the-sql-language/ddl/privileges.md">Section 5.7</a> for details</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">fdwoptions</code> <code class="type">text[]</code></p>
<p>Foreign-data wrapper specific options, as <span class="quote">“<span class="quote">keyword=value</span>”</span> strings</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/catalog-pg-foreign-data-wrapper.html)（英文原文，待翻譯）
