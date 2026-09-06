<a id="CATALOG-PG-PARAMETER-ACL"></a>

# 53.36. pg_parameter_acl

<a id="id-1.10.4.38.2"></a>

The catalog `pg_parameter_acl` records configuration parameters for which privileges have been granted to one or more roles. No entry is made for parameters that have default privileges.

Unlike most system catalogs, `pg_parameter_acl` is shared across all databases of a cluster: there is only one copy of `pg_parameter_acl` per cluster, not one per database.

<a id="id-1.10.4.38.5"></a>

<strong>Table 53.36. <code class="structname">pg&#95;parameter&#95;acl</code> Columns</strong>

<table border="1" class="table" summary="pg_parameter_acl Columns">
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
<p class="column_definition"><code class="structfield">parname</code> <code class="type">text</code></p>
<p>The name of a configuration parameter for which privileges are granted</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">paracl</code> <code class="type">aclitem[]</code></p>
<p>Access privileges; see <a class="xref" href="../../the-sql-language/ddl/privileges.md">Section 5.7</a> for details</p>
</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pg_parameter_acl.md)（英文原文，待翻譯）
