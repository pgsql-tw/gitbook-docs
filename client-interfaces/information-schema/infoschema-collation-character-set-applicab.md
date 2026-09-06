## 35.11. `collation_character_set_​applicability` [#](#INFOSCHEMA-COLLATION-CHARACTER-SET-APPLICAB)

The view `collation_character_set_applicability`
identifies which character set the available collations are
applicable to. In PostgreSQL, there is only one character set per
database (see explanation
in [Section 35.7](infoschema-character-sets.md)), so this view does
not provide much useful information.

<a id="id-1.7.6.15.3"></a>

**Table 35.9. `collation_character_set_applicability` Columns**

<table border="1" class="table" summary="collation_character_set_applicability Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">character_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Character sets are currently not implemented as schema objects, so this column is null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Character sets are currently not implemented as schema objects, so this column is null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the character set
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-collation-character-set-applicab.html)（英文原文，待翻譯）
