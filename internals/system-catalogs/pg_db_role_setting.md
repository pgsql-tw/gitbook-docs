<a id="CATALOG-PG-DB-ROLE-SETTING"></a>

# 53.16. pg_db_role_setting

<a id="id-1.10.4.18.2"></a>

The catalog `pg_db_role_setting` records the default values that have been set for run-time configuration variables, for each role and database combination.

Unlike most system catalogs, `pg_db_role_setting` is shared across all databases of a cluster: there is only one copy of `pg_db_role_setting` per cluster, not one per database.

<a id="id-1.10.4.18.5"></a>

<strong>Table 53.16. <code class="structname">pg&#95;db&#95;role&#95;setting</code> Columns</strong>

<table border="1" class="table" summary="pg_db_role_setting Columns">
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
<p class="column_definition"><code class="structfield">setdatabase</code> <code class="type">oid</code> (references <a class="link" href="pg_database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the database the setting is applicable to, or zero if not database-specific</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">setrole</code> <code class="type">oid</code> (references <a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the role the setting is applicable to, or zero if not role-specific</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">setconfig</code> <code class="type">text[]</code></p>
<p>Defaults for run-time configuration variables</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_db_role_setting.md)（英文原文，待翻譯）
