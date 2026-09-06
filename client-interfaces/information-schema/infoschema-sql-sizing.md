## 35.51. `sql_sizing` [#](#INFOSCHEMA-SQL-SIZING)

The table `sql_sizing` contains information about
various size limits and maximum values in
PostgreSQL. This information is
primarily intended for use in the context of the ODBC interface;
users of other interfaces will probably find this information to be
of little use. For this reason, the individual sizing items are
not described here; you will find them in the description of the
ODBC interface.

<a id="id-1.7.6.55.3"></a>

**Table 35.49. `sql_sizing` Columns**

<table border="1" class="table" summary="sql_sizing Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sizing_id</code> <code class="type">cardinal_number</code>
</p>
<p>
       Identifier of the sizing item
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sizing_name</code> <code class="type">character_data</code>
</p>
<p>
       Descriptive name of the sizing item
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">supported_value</code> <code class="type">cardinal_number</code>
</p>
<p>
       Value of the sizing item, or 0 if the size is unlimited or
       cannot be determined, or null if the features for which the
       sizing item is applicable are not supported
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comments</code> <code class="type">character_data</code>
</p>
<p>
       Possibly a comment pertaining to the sizing item
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-sql-sizing.html)（英文原文，待翻譯）
