## 35.53. `table_privileges` [#](#INFOSCHEMA-TABLE-PRIVILEGES)

The view `table_privileges` identifies all
privileges granted on tables or views to a currently enabled role
or by a currently enabled role. There is one row for each
combination of table, grantor, and grantee.

<a id="id-1.7.6.57.3"></a>

**Table 35.51. `table_privileges` Columns**

<table border="1" class="table" summary="table_privileges Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantor</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the role that granted the privilege
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantee</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the role that the privilege was granted to
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the table (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privilege_type</code> <code class="type">character_data</code>
</p>
<p>
       Type of the privilege: <code class="literal">SELECT</code>,
       <code class="literal">INSERT</code>, <code class="literal">UPDATE</code>,
       <code class="literal">DELETE</code>, <code class="literal">TRUNCATE</code>,
       <code class="literal">REFERENCES</code>, or <code class="literal">TRIGGER</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the privilege is grantable, <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">with_hierarchy</code> <code class="type">yes_or_no</code>
</p>
<p>
       In the SQL standard, <code class="literal">WITH HIERARCHY OPTION</code>
       is a separate (sub-)privilege allowing certain operations on
       table inheritance hierarchies.  In PostgreSQL, this is included
       in the <code class="literal">SELECT</code> privilege, so this column
       shows <code class="literal">YES</code> if the privilege
       is <code class="literal">SELECT</code>, else <code class="literal">NO</code>.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-table-privileges.html)（英文原文，待翻譯）
