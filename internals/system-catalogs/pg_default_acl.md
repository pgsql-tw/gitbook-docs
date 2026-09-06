<a id="CATALOG-PG-DEFAULT-ACL"></a>

# 53.17. pg_default_acl

<a id="id-1.10.4.19.2"></a>

The catalog `pg_default_acl` stores initial privileges to be assigned to newly created objects.

<a id="id-1.10.4.19.4"></a>

<strong>Table 53.17. <code class="structname">pg&#95;default&#95;acl</code> Columns</strong>

<table border="1" class="table" summary="pg_default_acl Columns">
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
<p class="column_definition"><code class="structfield">defaclrole</code> <code class="type">oid</code> (references <a class="link" href="pg_authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the role associated with this entry</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">defaclnamespace</code> <code class="type">oid</code> (references <a class="link" href="pg_namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)</p>
<p>The OID of the namespace associated with this entry, or zero if none</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">defaclobjtype</code> <code class="type">char</code></p>
<p>Type of object this entry is for: <code class="literal">r</code> = relation (table, view), <code class="literal">S</code> = sequence, <code class="literal">f</code> = function, <code class="literal">T</code> = type, <code class="literal">n</code> = schema</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition"><code class="structfield">defaclacl</code> <code class="type">aclitem[]</code></p>
<p>Access privileges that this type of object should have on creation</p>
</td>
</tr>
</tbody>
</table>



A `pg_default_acl` entry shows the initial privileges to be assigned to an object belonging to the indicated user. There are currently two types of entry: “global” entries with `defaclnamespace` = zero, and “per-schema” entries that reference a particular schema. If a global entry is present then it <em>overrides</em> the normal hard-wired default privileges for the object type. A per-schema entry, if present, represents privileges to be <em>added to</em> the global or hard-wired default privileges.

Note that when an ACL entry in another catalog is null, it is taken to represent the hard-wired default privileges for its object, <em>not</em> whatever might be in `pg_default_acl` at the moment. `pg_default_acl` is only consulted during object creation.

---

原文：[PostgreSQL 15.19 Documentation](pg_default_acl.md)（英文原文，待翻譯）
