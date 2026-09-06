## 35.10. `collations` [#](#INFOSCHEMA-COLLATIONS)

The view `collations` contains the collations
available in the current database.

<a id="id-1.7.6.14.3"></a>

**Table 35.8. `collations` Columns**

<table border="1" class="table" summary="collations Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the collation (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the collation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the default collation
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pad_attribute</code> <code class="type">character_data</code>
</p>
<p>
       Always <code class="literal">NO PAD</code> (The alternative <code class="literal">PAD
       SPACE</code> is not supported by PostgreSQL.)
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-collations.html)（英文原文，待翻譯）
