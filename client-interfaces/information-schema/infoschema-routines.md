<a id="INFOSCHEMA-ROUTINES"></a>
## 35.45. `routines` [#](#INFOSCHEMA-ROUTINES)

檢視表 `routines` 包含目前資料庫中的所有函式與程序。只有目前使用者可存取的函式與程序才會顯示（使用者為其擁有者或具有某項權限時即可存取）。

<a id="id-1.7.6.49.3"></a>

**表 35.43. `routines` 欄位**

<table border="1" class="table" summary="routines 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
       函式的<span class="quote">“<span class="quote">特定名稱</span>”</span>。這是在綱要中唯一識別該函式的名稱，即使函式的實際名稱被多載也是如此。特定名稱的格式並未定義，只應該用來與其他特定常式名稱的實例進行比較。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       函式名稱（多載時可能重複）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_type</code> <code class="type">character_data</code>
</p>
<p>
函式為 <code class="literal">FUNCTION</code>，程序為 <code class="literal">PROCEDURE</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">module_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">module_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">module_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       若函式的回傳資料型別為內建型別，則為該型別；若為某種陣列，則為 <code class="literal">ARRAY</code>（此時請參閱檢視表 <code class="literal">element_types</code>）；否則為 <code class="literal">USER-DEFINED</code>（此時型別由 <code class="literal">type_udt_name</code> 及相關欄位識別）。程序則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
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
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於回傳資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type_udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義函式回傳資料型別的資料庫名稱（一律為目前資料庫）。程序則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type_udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義函式回傳資料型別的綱要名稱。程序則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type_udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       函式回傳資料型別的名稱。程序則為 null。
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
       此函式回傳資料型別之資料型別描述子的識別碼，在與該函式相關的資料型別描述子中是唯一的。這主要用於與此類識別碼的其他實例進行連接。（識別碼的具體格式並未定義，也不保證在未來版本中維持不變。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_body</code> <code class="type">character_data</code>
</p>
<p>
       若函式為 SQL 函式，則為 <code class="literal">SQL</code>；否則為 <code class="literal">EXTERNAL</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_definition</code> <code class="type">character_data</code>
</p>
<p>
       函式的原始碼文字（若函式不是由目前已啟用的角色所擁有，則為 null）。（依照 SQL 標準，此欄位只在 <code class="literal">routine_body</code> 為 <code class="literal">SQL</code> 時適用，但在 <span class="productname">PostgreSQL</span> 中，它會包含建立函式時所指定的任何原始碼文字。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">external_name</code> <code class="type">character_data</code>
</p>
<p>
       若此函式為 C 函式，則為函式的外部名稱（連結符號）；否則為 null。（其結果與 <code class="literal">routine_definition</code> 中顯示的值相同。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">external_language</code> <code class="type">character_data</code>
</p>
<p>
       撰寫該函式所用的語言
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parameter_style</code> <code class="type">character_data</code>
</p>
<p>
       一律為 <code class="literal">GENERAL</code>（SQL 標準定義了其他參數風格，但 <span class="productname">PostgreSQL</span> 中未提供這些風格。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_deterministic</code> <code class="type">yes_or_no</code>
</p>
<p>
       若函式宣告為不可變（immutable；在 SQL 標準中稱為 deterministic），則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>。（你無法透過資訊綱要查詢 <span class="productname">PostgreSQL</span> 中可用的其他易變性等級。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sql_data_access</code> <code class="type">character_data</code>
</p>
<p>
       一律為 <code class="literal">MODIFIES</code>，表示該函式可能會修改 SQL 資料。此資訊對 <span class="productname">PostgreSQL</span> 沒有用處。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_null_call</code> <code class="type">yes_or_no</code>
</p>
<p>
       若函式在任一引數為 null 時會自動傳回 null，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>。程序則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sql_path</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schema_level_routine</code> <code class="type">yes_or_no</code>
</p>
<p>
       一律為 <code class="literal">YES</code>（相反的情況是使用者定義型別的方法，這是 <span class="productname">PostgreSQL</span> 中未提供的功能。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_dynamic_result_sets</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_user_defined_cast</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_implicitly_invocable</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">security_type</code> <code class="type">character_data</code>
</p>
<p>
       若函式以目前使用者的權限執行，則為 <code class="literal">INVOKER</code>；若函式以定義它的使用者的權限執行，則為 <code class="literal">DEFINER</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">to_sql_specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">to_sql_specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">to_sql_specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">as_locator</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">created</code> <code class="type">time_stamp</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_altered</code> <code class="type">time_stamp</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">new_savepoint_level</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_udt_dependent</code> <code class="type">yes_or_no</code>
</p>
<p>
       目前一律為 <code class="literal">NO</code>。另一個值 <code class="literal">YES</code> 適用於 <span class="productname">PostgreSQL</span> 中未提供的功能。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_from_data_type</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_as_locator</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_max_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_char_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_collation_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_interval_type</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_type_udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_type_udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_type_udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_scope_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_scope_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_scope_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_maximum_cardinality</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">result_cast_dtd_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-routines.html)（原文版本：18.6；核對日期：2026-10-18）
