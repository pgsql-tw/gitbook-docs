<a id="INFOSCHEMA-PARAMETERS"></a>
## 35.33. `parameters` [#](#INFOSCHEMA-PARAMETERS)

檢視表 `parameters` 包含目前資料庫中所有函式之參數（引數）的相關資訊。只有目前使用者可存取（身為擁有者或具有某種權限）的函式才會顯示。

<a id="id-1.7.6.37.3"></a>

**表 35.31. `parameters` 欄位**

<table border="1" class="table" summary="parameters 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       函式的<span class="quote">“<span class="quote">特定名稱</span>”</span>。詳細資訊請參閱<a class="xref" href="infoschema-routines.md">第 35.45 節</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordinal_position</code> <code class="type">cardinal_number</code>
</p>
<p>
       該參數在函式引數清單中的序數位置（從 1 起算）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parameter_mode</code> <code class="type">character_data</code>
</p>
<p>
       <code class="literal">IN</code> 表示輸入參數，<code class="literal">OUT</code> 表示輸出參數，<code class="literal">INOUT</code> 表示輸入／輸出參數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_result</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">as_locator</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parameter_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       參數名稱；若參數沒有名稱，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       若參數的資料型別為內建型別，則為該型別；若為某種陣列，則為 <code class="literal">ARRAY</code>（此時請參閱檢視表 <code class="literal">element_types</code>）；否則為 <code class="literal">USER-DEFINED</code>（此時型別由 <code class="literal">udt_name</code> 及相關欄位識別）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於參數資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該參數資料型別的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該參數資料型別的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       參數資料型別的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">scope_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">scope_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">scope_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">maximum_cardinality</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為在 <span class="productname">PostgreSQL</span> 中陣列的最大基數一律為無限制
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dtd_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       此參數之資料型別描述子的識別碼，在與該函式相關的資料型別描述子中是唯一的。這主要用於與此類識別碼的其他實例進行連接。（識別碼的具體格式並未定義，也不保證在未來版本中維持不變。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parameter_default</code> <code class="type">character_data</code>
</p>
<p>
       參數的預設運算式；若沒有預設運算式，或該函式不是由目前已啟用的角色所擁有，則為 null。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-parameters.html)（原文版本：18.6；核對日期：2026-10-18）
