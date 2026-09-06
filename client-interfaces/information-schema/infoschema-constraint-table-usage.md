## 35.19. `constraint_table_usage` [#](#INFOSCHEMA-CONSTRAINT-TABLE-USAGE)

The view `constraint_table_usage` identifies all
tables in the current database that are used by some constraint and
are owned by a currently enabled role. (This is different from the
view `table_constraints`, which identifies all
table constraints along with the table they are defined on.) For a
foreign key constraint, this view identifies the table that the
foreign key references. For a unique or primary key constraint,
this view simply identifies the table the constraint belongs to.
Check constraints and not-null constraints are not included in this
view.

<a id="id-1.7.6.23.3"></a>

**Table 35.17. `constraint_table_usage` Columns**

<table border="1" class="table" summary="constraint_table_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the table that is used by
       some constraint (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the table that is used by some
       constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the table that is used by some constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
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
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-constraint-table-usage.html)（英文原文，待翻譯）
