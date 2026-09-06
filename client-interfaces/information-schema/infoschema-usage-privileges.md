## 35.59. `usage_privileges` [#](#INFOSCHEMA-USAGE-PRIVILEGES)

The view `usage_privileges` identifies
`USAGE` privileges granted on various kinds of
objects to a currently enabled role or by a currently enabled role.
In PostgreSQL, this currently applies to
collations, domains, foreign-data wrappers, foreign servers, and sequences. There is one
row for each combination of object, grantor, and grantee.

Since collations do not have real privileges
in PostgreSQL, this view shows implicit
non-grantable `USAGE` privileges granted by the
owner to `PUBLIC` for all collations. The other
object types, however, show real privileges.

In PostgreSQL, sequences also support `SELECT`
and `UPDATE` privileges in addition to
the `USAGE` privilege. These are nonstandard and therefore
not visible in the information schema.

<a id="id-1.7.6.63.5"></a>

**Table 35.57. `usage_privileges` Columns**

<table border="1" class="table" summary="usage_privileges Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-usage-privileges.html)（英文原文，待翻譯）
