<a id="INFOSCHEMA-USER-DEFINED-TYPES"></a>
## 35.60. `user_defined_types` [#](#INFOSCHEMA-USER-DEFINED-TYPES)

檢視表 `user_defined_types` 目前包含目前資料庫中定義的所有複合型別。
只有目前使用者可存取的型別才會顯示（使用者為其擁有者或具有某項權限時即可存取）。

SQL 定義了兩種使用者自訂型別：結構化型別（structured type，在 PostgreSQL
中也稱為複合型別）與相異型別（distinct type，PostgreSQL 未實作）。為了因應日後
的變化，請使用欄位 `user_defined_type_category` 來區分這兩者。其他使用者自訂型別，
例如基本型別與列舉型別，屬於 PostgreSQL 對 SQL 標準的擴充，不會顯示在此處。
網域請改為參閱[第 35.23 節](infoschema-domains.md)。

<a id="id-1.7.6.64.4"></a>

**表 35.58. `user_defined_types` 欄位**

<table border="1" class="table" summary="user_defined_types 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">user_defined_type_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含型別的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">user_defined_type_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含型別的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">user_defined_type_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       型別名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">user_defined_type_category</code> <code class="type">character_data</code>
</p>
<p>
       目前一律為 <code class="literal">STRUCTURED</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_instantiable</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_final</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordering_form</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordering_category</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordering_routine_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordering_routine_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordering_routine_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reference_type</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">source_dtd_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ref_dtd_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-user-defined-types.html)（原文版本：18.6；核對日期：2026-10-18）
