## 35.50. `sql_parts` [#](#INFOSCHEMA-SQL-PARTS)

The table `sql_parts` contains information about
which of the several parts of the SQL standard are supported by
PostgreSQL.

<a id="id-1.7.6.54.3"></a>

**Table 35.48. `sql_parts` Columns**

<table border="1" class="table" summary="sql_parts Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">feature_id</code> <code class="type">character_data</code>
</p>
<p>
       An identifier string containing the number of the part
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">feature_name</code> <code class="type">character_data</code>
</p>
<p>
       Descriptive name of the part
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_supported</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> if the part is fully supported by the
       current version of <span class="productname">PostgreSQL</span>,
       <code class="literal">NO</code> if not
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_verified_by</code> <code class="type">character_data</code>
</p>
<p>
       Always null, since the <span class="productname">PostgreSQL</span> development group does not
       perform formal testing of feature conformance
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comments</code> <code class="type">character_data</code>
</p>
<p>
       Possibly a comment about the supported status of the part
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-sql-parts.html)（英文原文，待翻譯）
