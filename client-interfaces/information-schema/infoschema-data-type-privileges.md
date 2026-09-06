## 35.20. `data_type_privileges` [#](#INFOSCHEMA-DATA-TYPE-PRIVILEGES)

The view `data_type_privileges` identifies all
data type descriptors that the current user has access to, by way
of being the owner of the described object or having some privilege
for it. A data type descriptor is generated whenever a data type
is used in the definition of a table column, a domain, or a
function (as parameter or return type) and stores some information
about how the data type is used in that instance (for example, the
declared maximum length, if applicable). Each data type
descriptor is assigned an arbitrary identifier that is unique
among the data type descriptor identifiers assigned for one object
(table, domain, function). This view is probably not useful for
applications, but it is used to define some other views in the
information schema.

<a id="id-1.7.6.24.3"></a>

**Table 35.18. `data_type_privileges` Columns**

<table border="1" class="table" summary="data_type_privileges Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the described object (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the described object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the described object
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_type</code> <code class="type">character_data</code>
</p>
<p>
       The type of the described object: one of
       <code class="literal">TABLE</code> (the data type descriptor pertains to
       a column of that table), <code class="literal">DOMAIN</code> (the data
       type descriptors pertains to that domain),
       <code class="literal">ROUTINE</code> (the data type descriptor pertains
       to a parameter or the return data type of that function).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dtd_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       The identifier of the data type descriptor, which is unique
       among the data type descriptors for that same object.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-data-type-privileges.html)（英文原文，待翻譯）
