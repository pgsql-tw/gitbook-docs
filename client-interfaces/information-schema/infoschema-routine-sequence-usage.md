## 35.43. `routine_sequence_usage` [#](#INFOSCHEMA-ROUTINE-SEQUENCE-USAGE)

The view `routine_sequence_usage` identifies all sequences
that are used by a function or procedure, either in the SQL body or in
parameter default expressions. (This only works for unquoted SQL bodies,
not quoted bodies or functions in other languages.) A sequence is only
included if that sequence is owned by a currently enabled role.

<a id="id-1.7.6.47.3"></a>

**Table 35.41. `routine_sequence_usage` Columns**

<table border="1" class="table" summary="routine_sequence_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">schema_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the sequence that is used by the
       function (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the sequence that is used by the function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the sequence that is used by the function
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-routine-sequence-usage.html)（英文原文，待翻譯）
