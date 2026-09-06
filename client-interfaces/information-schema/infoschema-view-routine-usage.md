## 35.64. `view_routine_usage` [#](#INFOSCHEMA-VIEW-ROUTINE-USAGE)

The view `view_routine_usage` identifies all
routines (functions and procedures) that are used in the query
expression of a view (the `SELECT` statement that
defines the view). A routine is only included if that routine is
owned by a currently enabled role.

<a id="id-1.7.6.68.3"></a>

**Table 35.62. `view_routine_usage` Columns**

<table border="1" class="table" summary="view_routine_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the view (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the view
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the function (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       The <span class="quote">“<span class="quote">specific name</span>”</span> of the function.  See <a class="xref" href="infoschema-routines.md">Section 35.45</a> for more information.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-view-routine-usage.html)（英文原文，待翻譯）
