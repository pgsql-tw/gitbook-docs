## 35.31. `foreign_tables` [#](#INFOSCHEMA-FOREIGN-TABLES)

The view `foreign_tables` contains all foreign
tables defined in the current database. Only those foreign
tables are shown that the current user has access to (by way of
being the owner or having some privilege).

<a id="id-1.7.6.35.3"></a>

**Table 35.29. `foreign_tables` Columns**

<table border="1" class="table" summary="foreign_tables Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that the foreign table is defined in (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the foreign table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the foreign table
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that the foreign server is defined in (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the foreign server
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-foreign-tables.html)（英文原文，待翻譯）
