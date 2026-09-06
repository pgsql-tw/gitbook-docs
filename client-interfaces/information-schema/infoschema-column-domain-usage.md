## 35.13. `column_domain_usage` [#](#INFOSCHEMA-COLUMN-DOMAIN-USAGE)

The view `column_domain_usage` identifies all
columns (of a table or a view) that make use of some domain defined
in the current database and owned by a currently enabled role.

<a id="id-1.7.6.17.3"></a>

**Table 35.11. `column_domain_usage` Columns**

<table border="1" class="table" summary="column_domain_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the domain (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the domain
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the domain
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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-column-domain-usage.html)（英文原文，待翻譯）
