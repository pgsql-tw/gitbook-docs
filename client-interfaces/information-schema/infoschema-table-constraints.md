## 35.52. `table_constraints` [#](#INFOSCHEMA-TABLE-CONSTRAINTS)

The view `table_constraints` contains all
constraints belonging to tables that the current user owns or has
some privilege other than `SELECT` on.

<a id="id-1.7.6.56.3"></a>

**Table 35.50. `table_constraints` Columns**

<table border="1" class="table" summary="table_constraints Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the constraint (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the constraint
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
<code class="structfield">constraint_type</code> <code class="type">character_data</code>
</p>
<p>
       Type of the constraint: <code class="literal">CHECK</code> (includes not-null constraints),
       <code class="literal">FOREIGN KEY</code>, <code class="literal">PRIMARY KEY</code>,
       or <code class="literal">UNIQUE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_deferrable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the constraint is deferrable, <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">initially_deferred</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the constraint is deferrable and initially deferred, <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">enforced</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the constraint is enforced, <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">nulls_distinct</code> <code class="type">yes_or_no</code>
</p>
<p>
       If the constraint is a unique constraint, then <code class="literal">YES</code>
       if the constraint treats nulls as distinct or <code class="literal">NO</code> if
       it treats nulls as not distinct, otherwise null for other types of
       constraints.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-table-constraints.html)（英文原文，待翻譯）
