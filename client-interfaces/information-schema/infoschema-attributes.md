## 35.6. `attributes` [#](#INFOSCHEMA-ATTRIBUTES)

The view `attributes` contains information about
the attributes of composite data types defined in the database.
(Note that the view does not give information about table columns,
which are sometimes called attributes in PostgreSQL contexts.)
Only those attributes are shown that the current user has access to (by way
of being the owner of or having some privilege on the type).

<a id="id-1.7.6.10.3"></a>

**Table 35.4. `attributes` Columns**

<table border="1" class="table" summary="attributes Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the data type (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the data type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the data type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the attribute
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordinal_position</code> <code class="type">cardinal_number</code>
</p>
<p>
       Ordinal position of the attribute within the data type (count starts at 1)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_default</code> <code class="type">character_data</code>
</p>
<p>
       Default expression of the attribute
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_nullable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the attribute is possibly nullable,
       <code class="literal">NO</code> if it is known not nullable.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       Data type of the attribute, if it is a built-in type, or
       <code class="literal">ARRAY</code> if it is some array (in that case, see
       the view <code class="literal">element_types</code>), else
       <code class="literal">USER-DEFINED</code> (in that case, the type is
       identified in <code class="literal">attribute_udt_name</code> and
       associated columns).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       If <code class="literal">data_type</code> identifies a character or bit
       string type, the declared maximum length; null for all other
       data types or if no maximum length was declared.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       If <code class="literal">data_type</code> identifies a character type,
       the maximum possible length in octets (bytes) of a datum; null
       for all other data types.  The maximum octet length depends on
       the declared character maximum length (see above) and the
       server encoding.
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
       Name of the database containing the collation of the attribute
       (always the current database), null if default or the data type
       of the attribute is not collatable
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the collation of the attribute,
       null if default or the data type of the attribute is not
       collatable
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the collation of the attribute, null if default or the
       data type of the attribute is not collatable
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       If <code class="literal">data_type</code> identifies a numeric type, this
       column contains the (declared or implicit) precision of the
       type for this attribute.  The precision indicates the number of
       significant digits.  It can be expressed in decimal (base 10)
       or binary (base 2) terms, as specified in the column
       <code class="literal">numeric_precision_radix</code>.  For all other data
       types, this column is null.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       If <code class="literal">data_type</code> identifies a numeric type, this
       column indicates in which base the values in the columns
       <code class="literal">numeric_precision</code> and
       <code class="literal">numeric_scale</code> are expressed.  The value is
       either 2 or 10.  For all other data types, this column is null.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       If <code class="literal">data_type</code> identifies an exact numeric
       type, this column contains the (declared or implicit) scale of
       the type for this attribute.  The scale indicates the number of
       significant digits to the right of the decimal point.  It can
       be expressed in decimal (base 10) or binary (base 2) terms, as
       specified in the column
       <code class="literal">numeric_precision_radix</code>.  For all other data
       types, this column is null.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       If <code class="literal">data_type</code> identifies a date, time,
       timestamp, or interval type, this column contains the (declared
       or implicit) fractional seconds precision of the type for this
       attribute, that is, the number of decimal digits maintained
       following the decimal point in the seconds value.  For all
       other data types, this column is null.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       If <code class="literal">data_type</code> identifies an interval type,
       this column contains the specification which fields the
       intervals include for this attribute, e.g., <code class="literal">YEAR TO
       MONTH</code>, <code class="literal">DAY TO SECOND</code>, etc.  If no
       field restrictions were specified (that is, the interval
       accepts all fields), and for all other data types, this field
       is null.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       Applies to a feature not available
       in <span class="productname">PostgreSQL</span>
       (see <code class="literal">datetime_precision</code> for the fractional
       seconds precision of interval type attributes)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that the attribute data type is defined in
       (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that the attribute data type is defined in
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the attribute data type
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
       An identifier of the data type descriptor of the attribute, unique
       among the data type descriptors pertaining to the composite type.  This
       is mainly useful for joining with other instances of such
       identifiers.  (The specific format of the identifier is not
       defined and not guaranteed to remain the same in future
       versions.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_derived_reference_attribute</code> <code class="type">yes_or_no</code>
</p>
<p>
       Applies to a feature not available in <span class="productname">PostgreSQL</span>
</p></td></tr></tbody></table>

<br>

See also under [Section 35.17](infoschema-columns.md), a similarly
structured view, for further information on some of the columns.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-attributes.html)（英文原文，待翻譯）
