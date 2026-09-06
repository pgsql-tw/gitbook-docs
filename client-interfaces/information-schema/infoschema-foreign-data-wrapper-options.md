## 35.26. `foreign_data_wrapper_options` [#](#INFOSCHEMA-FOREIGN-DATA-WRAPPER-OPTIONS)

The view `foreign_data_wrapper_options` contains
all the options defined for foreign-data wrappers in the current
database. Only those foreign-data wrappers are shown that the
current user has access to (by way of being the owner or having
some privilege).

<a id="id-1.7.6.30.3"></a>

**Table 35.24. `foreign_data_wrapper_options` Columns**

<table border="1" class="table" summary="foreign_data_wrapper_options Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that the foreign-data wrapper is defined in (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the foreign-data wrapper
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">option_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of an option
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">option_value</code> <code class="type">character_data</code>
</p>
<p>
       Value of the option
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-foreign-data-wrapper-options.html)（英文原文，待翻譯）
