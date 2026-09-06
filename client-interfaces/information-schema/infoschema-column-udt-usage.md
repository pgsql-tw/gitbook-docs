## 35.16. `column_udt_usage` [#](#INFOSCHEMA-COLUMN-UDT-USAGE)

The view `column_udt_usage` identifies all columns
that use data types owned by a currently enabled role. Note that in
PostgreSQL, built-in data types behave
like user-defined types, so they are included here as well. See
also [Section 35.17](infoschema-columns.md) for details.

<a id="id-1.7.6.20.3"></a>

**Table 35.14. `column_udt_usage` Columns**

<table border="1" class="table" summary="column_udt_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that the column data type (the underlying
       type of the domain, if applicable) is defined in (always the
       current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that the column data type (the underlying
       type of the domain, if applicable) is defined in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the column data type (the underlying type of the
       domain, if applicable)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
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
       Name of the column
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-column-udt-usage.html)（英文原文，待翻譯）
