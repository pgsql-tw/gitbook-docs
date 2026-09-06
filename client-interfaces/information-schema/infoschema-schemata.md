## 35.46. `schemata` [#](#INFOSCHEMA-SCHEMATA)

The view `schemata` contains all schemas in the current
database that the current user has access to (by way of being the owner or
having some privilege).

<a id="id-1.7.6.50.3"></a>

**Table 35.44. `schemata` Columns**

<table border="1" class="table" summary="schemata Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">catalog_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that the schema is contained in (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schema_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schema_owner</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the owner of the schema
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_character_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_character_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_character_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sql_path</code> <code class="type">character_data</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-schemata.html)（英文原文，待翻譯）
