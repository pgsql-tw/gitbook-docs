## 35.49. `sql_implementation_info` [#](#INFOSCHEMA-SQL-IMPLEMENTATION-INFO)

The table `sql_implementation_info` contains
information about various aspects that are left
implementation-defined by the SQL standard. This information is
primarily intended for use in the context of the ODBC interface;
users of other interfaces will probably find this information to be
of little use. For this reason, the individual implementation
information items are not described here; you will find them in the
description of the ODBC interface.

<a id="id-1.7.6.53.3"></a>

**Table 35.47. `sql_implementation_info` Columns**

<table border="1" class="table" summary="sql_implementation_info Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">implementation_info_id</code> <code class="type">character_data</code>
</p>
<p>
       Identifier string of the implementation information item
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">implementation_info_name</code> <code class="type">character_data</code>
</p>
<p>
       Descriptive name of the implementation information item
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">integer_value</code> <code class="type">cardinal_number</code>
</p>
<p>
       Value of the implementation information item, or null if the
       value is contained in the column
       <code class="literal">character_value</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_value</code> <code class="type">character_data</code>
</p>
<p>
       Value of the implementation information item, or null if the
       value is contained in the column
       <code class="literal">integer_value</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comments</code> <code class="type">character_data</code>
</p>
<p>
       Possibly a comment pertaining to the implementation information item
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-sql-implementation-info.html)（英文原文，待翻譯）
