## 35.9. `check_constraints` [#](#INFOSCHEMA-CHECK-CONSTRAINTS)

The view `check_constraints` contains all check
constraints, either defined on a table or on a domain, that are
owned by a currently enabled role. (The owner of the table or
domain is the owner of the constraint.)

The SQL standard considers not-null constraints to be check constraints
with a `CHECK (column_name IS NOT
NULL)` expression. So not-null constraints are also included here
and don't have a separate view.

<a id="id-1.7.6.13.4"></a>

**Table 35.7. `check_constraints` Columns**

<table border="1" class="table" summary="check_constraints Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">check_clause</code> <code class="type">character_data</code>
</p>
<p>
       The check expression of the check constraint
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-check-constraints.html)（英文原文，待翻譯）
