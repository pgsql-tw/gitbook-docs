## 35.34. `referential_constraints` [#](#INFOSCHEMA-REFERENTIAL-CONSTRAINTS)

The view `referential_constraints` contains all
referential (foreign key) constraints in the current database.
Only those constraints are shown for which the current user has
write access to the referencing table (by way of being the
owner or having some privilege other than `SELECT`).

<a id="id-1.7.6.38.3"></a>

**Table 35.32. `referential_constraints` Columns**

<table border="1" class="table" summary="referential_constraints Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the constraint (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">unique_constraint_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the unique or primary key
       constraint that the foreign key constraint references (always
       the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">unique_constraint_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the unique or primary key
       constraint that the foreign key constraint references
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">unique_constraint_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the unique or primary key constraint that the foreign
       key constraint references
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">match_option</code> <code class="type">character_data</code>
</p>
<p>
       Match option of the foreign key constraint:
       <code class="literal">FULL</code>, <code class="literal">PARTIAL</code>, or
       <code class="literal">NONE</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">update_rule</code> <code class="type">character_data</code>
</p>
<p>
       Update rule of the foreign key constraint:
       <code class="literal">CASCADE</code>, <code class="literal">SET NULL</code>,
       <code class="literal">SET DEFAULT</code>, <code class="literal">RESTRICT</code>, or
       <code class="literal">NO ACTION</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">delete_rule</code> <code class="type">character_data</code>
</p>
<p>
       Delete rule of the foreign key constraint:
       <code class="literal">CASCADE</code>, <code class="literal">SET NULL</code>,
       <code class="literal">SET DEFAULT</code>, <code class="literal">RESTRICT</code>, or
       <code class="literal">NO ACTION</code>.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-referential-constraints.html)（英文原文，待翻譯）
