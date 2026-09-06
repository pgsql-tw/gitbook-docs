## 35.38. `role_udt_grants` [#](#INFOSCHEMA-ROLE-UDT-GRANTS)

The view `role_udt_grants` is intended to identify
`USAGE` privileges granted on user-defined types
where the grantor or grantee is a currently enabled role. Further
information can be found under
`udt_privileges`. The only effective difference
between this view and `udt_privileges` is that
this view omits objects that have been made accessible to the
current user by way of a grant to `PUBLIC`. Since
data types do not have real privileges in PostgreSQL, but only an
implicit grant to `PUBLIC`, this view is empty.

<a id="id-1.7.6.42.3"></a>

**Table 35.36. `role_udt_grants` Columns**

<table border="1" class="table" summary="role_udt_grants Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the type (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privilege_type</code> <code class="type">character_data</code>
</p>
<p>
       Always <code class="literal">TYPE USAGE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the privilege is grantable, <code class="literal">NO</code> if not
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-role-udt-grants.html)（英文原文，待翻譯）
