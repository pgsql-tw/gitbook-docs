## 35.45. `routines` [#](#INFOSCHEMA-ROUTINES)

The view `routines` contains all functions and procedures in the
current database. Only those functions and procedures are shown that the current
user has access to (by way of being the owner or having some
privilege).

<a id="id-1.7.6.49.3"></a>

**Table 35.43. `routines` Columns**

<table border="1" class="table" summary="routines Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
       The <span class="quote">“<span class="quote">specific name</span>”</span> of the function.  This is a
       name that uniquely identifies the function in the schema, even
       if the real name of the function is overloaded.  The format of
       the specific name is not defined, it should only be used to
       compare it to other instances of specific routine names.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the function (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the function (might be duplicated in case of overloading)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_type</code> <code class="type">character_data</code>
</p>
<p>
<code class="literal">FUNCTION</code> for a
       function, <code class="literal">PROCEDURE</code> for a procedure
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">module_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">module_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">module_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       Return data type of the function, if it is a built-in type, or
       <code class="literal">ARRAY</code> if it is some array (in that case, see
       the view <code class="literal">element_types</code>), else
       <code class="literal">USER-DEFINED</code> (in that case, the type is
       identified in <code class="literal">type_udt_name</code> and associated
       columns).  Null for a procedure.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
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
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Always null, since this information is not applied to return data types in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type_udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that the return data type of the function
       is defined in (always the current database).  Null for a procedure.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type_udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that the return data type of the function is
       defined in.  Null for a procedure.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type_udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the return data type of the function.  Null for a procedure.
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
       An identifier of the data type descriptor of the return data
       type of this function, unique among the data type descriptors
       pertaining to the function.  This is mainly useful for joining
       with other instances of such identifiers.  (The specific format
       of the identifier is not defined and not guaranteed to remain
       the same in future versions.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_body</code> <code class="type">character_data</code>
</p>
<p>
       If the function is an SQL function, then
       <code class="literal">SQL</code>, else <code class="literal">EXTERNAL</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_definition</code> <code class="type">character_data</code>
</p>
<p>
       The source text of the function (null if the function is not
       owned by a currently enabled role).  (According to the SQL
       standard, this column is only applicable if
       <code class="literal">routine_body</code> is <code class="literal">SQL</code>, but
       in <span class="productname">PostgreSQL</span> it will contain
       whatever source text was specified when the function was
       created.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">external_name</code> <code class="type">character_data</code>
</p>
<p>
       If this function is a C function, then the external name (link
       symbol) of the function; else null.  (This works out to be the
       same value that is shown in
       <code class="literal">routine_definition</code>.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">external_language</code> <code class="type">character_data</code>
</p>
<p>
       The language the function is written in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parameter_style</code> <code class="type">character_data</code>
</p>
<p>
       Always <code class="literal">GENERAL</code> (The SQL standard defines
       other parameter styles, which are not available in <span class="productname">PostgreSQL</span>.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_deterministic</code> <code class="type">yes_or_no</code>
</p>
<p>
       If the function is declared immutable (called deterministic in
       the SQL standard), then <code class="literal">YES</code>, else
       <code class="literal">NO</code>.  (You cannot query the other volatility
       levels available in <span class="productname">PostgreSQL</span> through the information schema.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sql_data_access</code> <code class="type">character_data</code>
</p>
<p>
       Always <code class="literal">MODIFIES</code>, meaning that the function
       possibly modifies SQL data.  This information is not useful for
       <span class="productname">PostgreSQL</span>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_null_call</code> <code class="type">yes_or_no</code>
</p>
<p>
       If the function automatically returns null if any of its
       arguments are null, then <code class="literal">YES</code>, else
       <code class="literal">NO</code>.  Null for a procedure.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sql_path</code> <code class="type">character_data</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schema_level_routine</code> <code class="type">yes_or_no</code>
</p>
<p>
       Always <code class="literal">YES</code> (The opposite would be a method
       of a user-defined type, which is a feature not available in
       <span class="productname">PostgreSQL</span>.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_dynamic_result_sets</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_user_defined_cast</code> <code class="type">yes_or_no</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_implicitly_invocable</code> <code class="type">yes_or_no</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">security_type</code> <code class="type">character_data</code>
</p>
<p>
       If the function runs with the privileges of the current user,
       then <code class="literal">INVOKER</code>, if the function runs with the
       privileges of the user who defined it, then
       <code class="literal">DEFINER</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">to_sql_specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">to_sql_specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">to_sql_specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">as_locator</code> <code class="type">yes_or_no</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">created</code> <code class="type">time_stamp</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_altered</code> <code class="type">time_stamp</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">new_savepoint_level</code> <code class="type">yes_or_no</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_udt_dependent</code> <code class="type">yes_or_no</code>
</p>
<p>
       Currently always <code class="literal">NO</code>.  The alternative
       <code class="literal">YES</code> applies to a feature not available in
       <span class="productname">PostgreSQL</span>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_from_data_type</code> <code class="type">character_data</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_as_locator</code> <code class="type">yes_or_no</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_max_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_collation_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_interval_type</code> <code class="type">character_data</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_type_udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_type_udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_type_udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_scope_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_scope_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_scope_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_maximum_cardinality</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_dtd_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-routines.html)（英文原文，待翻譯）
