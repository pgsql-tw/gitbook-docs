## 35.63. `view_column_usage` [#](#INFOSCHEMA-VIEW-COLUMN-USAGE)

The view `view_column_usage` identifies all
columns that are used in the query expression of a view (the
`SELECT` statement that defines the view). A
column is only included if the table that contains the column is
owned by a currently enabled role.

### Note

Columns of system tables are not included. This should be fixed
sometime.

<a id="id-1.7.6.67.4"></a>

**Table 35.61. `view_column_usage` Columns**

<table border="1" class="table" summary="view_column_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">view_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the view (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">view_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">view_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the table that contains the
       column that is used by the view (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the table that contains the
       column that is used by the view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the table that contains the column that is used by the
       view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the column that is used by the view
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-view-column-usage.html)（英文原文，待翻譯）
