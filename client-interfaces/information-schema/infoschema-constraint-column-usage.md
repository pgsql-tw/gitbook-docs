## 35.18. `constraint_column_usage` [#](#INFOSCHEMA-CONSTRAINT-COLUMN-USAGE)

The view `constraint_column_usage` identifies all
columns in the current database that are used by some constraint.
Only those columns are shown that are contained in a table owned by
a currently enabled role. For a check constraint, this view
identifies the columns that are used in the check expression. For a
not-null constraint, this view identifies the column that the constraint is
defined on. For
a foreign key constraint, this view identifies the columns that the
foreign key references. For a unique or primary key constraint,
this view identifies the constrained columns.

<a id="id-1.7.6.22.3"></a>

**Table 35.16. `constraint_column_usage` Columns**

<table border="1" class="table" summary="constraint_column_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the table that contains the
       column that is used by some constraint (always the current
       database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the table that contains the
       column that is used by some constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the table that contains the column that is used by some
       constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the column that is used by some constraint
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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-constraint-column-usage.html)（英文原文，待翻譯）
