## 35.42. `routine_routine_usage` [#](#INFOSCHEMA-ROUTINE-ROUTINE-USAGE)

The view `routine_routine_usage` identifies all functions
or procedures that are used by another (or the same) function or procedure,
either in the SQL body or in parameter default expressions. (This only
works for unquoted SQL bodies, not quoted bodies or functions in other
languages.) An entry is included here only if the used function is owned
by a currently enabled role. (There is no such restriction on the using
function.)

Note that the entries for both functions in the view refer to the
“specific” name of the routine, even though the column names
are used in a way that is inconsistent with other information schema views
about routines. This is per SQL standard, although it is arguably a
misdesign. See [Section 35.45](infoschema-routines.md) for more information
about specific names.

<a id="id-1.7.6.46.4"></a>

**Table 35.40. `routine_routine_usage` Columns**

<table border="1" class="table" summary="routine_routine_usage Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database containing the using function (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema containing the using function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       The <span class="quote">“<span class="quote">specific name</span>”</span> of the using function.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the database that contains the function that is used by the
       first function (always the current database)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       Name of the schema that contains the function that is used by the first
       function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       The <span class="quote">“<span class="quote">specific name</span>”</span> of the function that is used by the
       first function.
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-routine-routine-usage.html)（英文原文，待翻譯）
