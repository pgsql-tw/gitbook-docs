## 35.33. `parameters` [#](#INFOSCHEMA-PARAMETERS)

The view `parameters` contains information about
the parameters (arguments) of all functions in the current database.
Only those functions are shown that the current user has access to
(by way of being the owner or having some privilege).

<a id="id-1.7.6.37.3"></a>

**Table 35.31. `parameters` Columns**

<table border="1" class="table" summary="parameters Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the function (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       The <span class="quote">“<span class="quote">specific name</span>”</span> of the function.  See <a class="xref" href="infoschema-routines.md">Section 35.45</a> for more information.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordinal_position</code> <code class="type">cardinal_number</code>
</p>
<p>
       Ordinal position of the parameter in the argument list of the
       function (count starts at 1)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parameter_mode</code> <code class="type">character_data</code>
</p>
<p>
<code class="literal">IN</code> for input parameter,
       <code class="literal">OUT</code> for output parameter,
       and <code class="literal">INOUT</code> for input/output parameter.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_result</code> <code class="type">yes_or_no</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">as_locator</code> <code class="type">yes_or_no</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parameter_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the parameter, or null if the parameter has no name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       Data type of the parameter, if it is a built-in type, or
       <code class="literal">ARRAY</code> if it is some array (in that case, see
       the view <code class="literal">element_types</code>), else
       <code class="literal">USER-DEFINED</code> (in that case, the type is
       identified in <code class="literal">udt_name</code> and associated
       columns).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to parameter data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that the data type of the parameter is
       defined in (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that the data type of the parameter is
       defined in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the data type of the parameter
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">scope_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">scope_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">scope_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">maximum_cardinality</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, because arrays always have unlimited maximum cardinality in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dtd_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       An identifier of the data type descriptor of the parameter,
       unique among the data type descriptors pertaining to the
       function.  This is mainly useful for joining with other
       instances of such identifiers.  (The specific format of the
       identifier is not defined and not guaranteed to remain the same
       in future versions.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parameter_default</code> <code class="type">character_data</code>
</p>
<p>
       The default expression of the parameter, or null if none or if the
       function is not owned by a currently enabled role.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-parameters.html)（英文原文，待翻譯）
