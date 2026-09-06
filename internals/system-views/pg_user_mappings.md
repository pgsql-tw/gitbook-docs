<a id="VIEW-PG-USER-MAPPINGS"></a>

# 54.34. pg_user_mappings

<a id="id-1.10.5.38.2"></a>

The view `pg_user_mappings` provides access to information about user mappings. This is essentially a publicly readable view of [`pg_user_mapping`](../system-catalogs/pg_user_mapping.md) that leaves out the options field if the user has no rights to use it.

<a id="id-1.10.5.38.4"></a>

<strong>Table 54.34. <code class="structname">pg&#95;user&#95;mappings</code> Columns</strong>

<table border="1" class="table" summary="pg_user_mappings Columns">
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
<p class="column_definition"><code class="structfield">umid</code> <code class="type">oid</code> (references <a class="link" href="../system-catalogs/pg_user_mapping.md"><code class="structname">pg_user_mapping</code></a>.<code class="structfield">oid</code>)</p>
<p>OID of the user mapping</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">srvid</code> <code class="type">oid</code> (references <a class="link" href="../system-catalogs/pg_foreign_server.md"><code class="structname">pg_foreign_server</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the foreign server that contains this mapping</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">srvname</code> <code class="type">name</code> (references <a class="link" href="../system-catalogs/pg_foreign_server.md"><code class="structname">pg_foreign_server</code></a>.<code class="structfield">srvname</code>)</p>
<p>Name of the foreign server</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">umuser</code> <code class="type">oid</code> (references <a class="link" href="../system-catalogs/pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>OID of the local role being mapped, or zero if the user mapping is public</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">usename</code> <code class="type">name</code></p>
<p>Name of the local user to be mapped</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">umoptions</code> <code class="type">text[]</code></p>
<p>User mapping specific options, as <span class="quote">“<span class="quote">keyword=value</span>”</span> strings</p>
</td>
</tr>
</tbody>
</table>



To protect password information stored as a user mapping option, the `umoptions` column will read as null unless one of the following applies:

* current user is the user being mapped, and owns the server or holds `USAGE` privilege on it
* current user is the server owner and mapping is for `PUBLIC`
* current user is a superuser

---

原文：[PostgreSQL 15.19 Documentation](pg_user_mappings.md)（英文原文，待翻譯）
