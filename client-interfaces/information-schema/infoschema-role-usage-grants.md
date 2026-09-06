## 35.39. `role_usage_grants` [#](#INFOSCHEMA-ROLE-USAGE-GRANTS)

The view `role_usage_grants` identifies
`USAGE` privileges granted on various kinds of
objects where the grantor or grantee is a currently enabled role.
Further information can be found under
`usage_privileges`. The only effective difference
between this view and `usage_privileges` is that
this view omits objects that have been made accessible to the
current user by way of a grant to `PUBLIC`.

<a id="id-1.7.6.43.3"></a>

**Table 35.37. `role_usage_grants` Columns**

<table border="1" class="table" summary="role_usage_grants Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantor</code> <code class="type">sql_identifier</code>
</p>
<p>
       The name of the role that granted the privilege
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantee</code> <code class="type">sql_identifier</code>
</p>
<p>
       The name of the role that the privilege was granted to
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the object (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the object, if applicable,
       else an empty string
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_type</code> <code class="type">character_data</code>
</p>
<p>
<code class="literal">COLLATION</code> or <code class="literal">DOMAIN</code> or <code class="literal">FOREIGN DATA WRAPPER</code> or <code class="literal">FOREIGN SERVER</code> or <code class="literal">SEQUENCE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privilege_type</code> <code class="type">character_data</code>
</p>
<p>
       Always <code class="literal">USAGE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the privilege is grantable, <code class="literal">NO</code> if not
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-role-usage-grants.html)（英文原文，待翻譯）
