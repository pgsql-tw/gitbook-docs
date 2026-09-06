## 35.47. `sequences` [#](#INFOSCHEMA-SEQUENCES)

The view `sequences` contains all sequences
defined in the current database. Only those sequences are shown
that the current user has access to (by way of being the owner or
having some privilege).

<a id="id-1.7.6.51.3"></a>

**Table 35.45. `sequences` Columns**

<table border="1" class="table" summary="sequences Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the sequence (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       The data type of the sequence.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       This column contains the (declared or implicit) precision of
       the sequence data type (see above).  The precision indicates
       the number of significant digits.  It can be expressed in
       decimal (base 10) or binary (base 2) terms, as specified in the
       column <code class="literal">numeric_precision_radix</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       This column indicates in which base the values in the columns
       <code class="literal">numeric_precision</code> and
       <code class="literal">numeric_scale</code> are expressed.  The value is
       either 2 or 10.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       This column contains the (declared or implicit) scale of the
       sequence data type (see above).  The scale indicates the number
       of significant digits to the right of the decimal point.  It
       can be expressed in decimal (base 10) or binary (base 2) terms,
       as specified in the column
       <code class="literal">numeric_precision_radix</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">start_value</code> <code class="type">character_data</code>
</p>
<p>
       The start value of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">minimum_value</code> <code class="type">character_data</code>
</p>
<p>
       The minimum value of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">maximum_value</code> <code class="type">character_data</code>
</p>
<p>
       The maximum value of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">increment</code> <code class="type">character_data</code>
</p>
<p>
       The increment of the sequence
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cycle_option</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the sequence cycles, else <code class="literal">NO</code>
</p></td></tr></tbody></table>

<br>

Note that in accordance with the SQL standard, the start, minimum,
maximum, and increment values are returned as character strings.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-sequences.html)（英文原文，待翻譯）
