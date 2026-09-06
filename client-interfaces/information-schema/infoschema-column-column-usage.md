## 35.12. `column_column_usage` [#](#INFOSCHEMA-COLUMN-COLUMN-USAGE)

The view `column_column_usage` identifies all generated
columns that depend on another base column in the same table. Only tables
owned by a currently enabled role are included.

<a id="id-1.7.6.16.3"></a>

**Table 35.10. `column_column_usage` Columns**

<table border="1" class="table" summary="column_column_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the table (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the base column that a generated column depends on
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dependent_column</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the generated column
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-column-column-usage.html)（英文原文，待翻譯）
