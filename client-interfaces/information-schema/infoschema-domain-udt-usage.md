## 35.22. `domain_udt_usage` [#](#INFOSCHEMA-DOMAIN-UDT-USAGE)

The view `domain_udt_usage` identifies all domains
that are based on data types owned by a currently enabled role.
Note that in PostgreSQL, built-in data
types behave like user-defined types, so they are included here as
well.

<a id="id-1.7.6.26.3"></a>

**Table 35.20. `domain_udt_usage` Columns**

<table border="1" class="table" summary="domain_udt_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that the domain data type is defined in (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that the domain data type is defined in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the domain data type
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
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-domain-udt-usage.html)（英文原文，待翻譯）
