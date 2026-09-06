## 35.21. `domain_constraints` [#](#INFOSCHEMA-DOMAIN-CONSTRAINTS)

The view `domain_constraints` contains all constraints
belonging to domains defined in the current database. Only those domains
are shown that the current user has access to (by way of being the owner or
having some privilege).

<a id="id-1.7.6.25.3"></a>

**Table 35.19. `domain_constraints` Columns**

<table border="1" class="table" summary="domain_constraints Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the constraint (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the domain (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the domain
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the domain
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_deferrable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the constraint is deferrable, <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">initially_deferred</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the constraint is deferrable and initially deferred, <code class="literal">NO</code> if not
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-domain-constraints.html)（英文原文，待翻譯）
