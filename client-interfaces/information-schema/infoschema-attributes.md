<a id="INFOSCHEMA-ATTRIBUTES"></a>
## 35.6. `attributes` [#](#infoschema-attributes) <a href="#infoschema-attributes" id="infoschema-attributes"></a>

檢視表 `attributes` 包含資料庫中所定義之複合資料型別的屬性資訊。（請注意，此
檢視表不提供資料表欄位的資訊；在 PostgreSQL 的脈絡中，資料表欄位有時也稱為屬性。）
只會顯示目前使用者有權存取（身為該型別的擁有者或具有該型別的某種權限）的屬性。

<a id="id-1.7.6.10.3"></a>

**表 35.4. `attributes` 欄位**

<table border="1" class="table" summary="attributes 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該資料型別的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該資料型別的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       資料型別名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       屬性名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordinal_position</code> <code class="type">cardinal_number</code>
</p>
<p>
       屬性在該資料型別中的序數位置（從 1 開始計數）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_default</code> <code class="type">character_data</code>
</p>
<p>
       屬性的預設表示式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_nullable</code> <code class="type">yes_or_no</code>
</p>
<p>
若屬性可能可以為 null，則為 <code class="literal">YES</code>；
       若已知不可為 null，則為 <code class="literal">NO</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       若屬性的資料型別為內建型別，則為該資料型別；若為某種陣列，則為
       <code class="literal">ARRAY</code>（此時請參閱檢視表
       <code class="literal">element_types</code>）；否則為
       <code class="literal">USER-DEFINED</code>（此時型別由
       <code class="literal">attribute_udt_name</code> 及相關欄位識別）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是字元或位元字串型別，則為
       宣告的最大長度；若為其他所有資料型別，或未宣告最大長度，則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是字元型別，則為單一資料值（datum）
       可能的最大長度，以八位元組（位元組）計；若為其他所有資料型別，則為 null。最大八位元組
       長度取決於宣告的字元最大長度（見上文）以及伺服器編碼。
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
       包含該屬性之定序的資料庫名稱（一律為目前資料庫）；若為預設定序，或該屬性的
       資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該屬性之定序的綱要名稱；若為預設定序，或該屬性的資料型別不可定序，
       則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該屬性的定序名稱；若為預設定序，或該屬性的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是數值型別，此欄位包含此屬性之
       型別的（宣告或隱含的）精確度。精確度表示有效位數，可以用十進位（以 10 為基數）
       或二進位（以 2 為基數）表示，依欄位
       <code class="literal">numeric_precision_radix</code> 所指定。若為其他所有資料
       型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是數值型別，此欄位表示欄位
       <code class="literal">numeric_precision</code> 與
       <code class="literal">numeric_scale</code> 中的值是以哪一種基數表示。其值為
       2 或 10。若為其他所有資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是精確數值型別，此欄位包含
       此屬性之型別的（宣告或隱含的）小數位數（scale）。小數位數表示小數點右側的有效位數，
       可以用十進位（以 10 為基數）或二進位（以 2 為基數）表示，依欄位
       <code class="literal">numeric_precision_radix</code> 所指定。若為其他所有資料
       型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是日期、時間、
       時間戳記或時間間隔型別，此欄位包含此屬性之型別的（宣告或隱含的）
       秒數小數部分精確度，也就是秒數值中小數點之後保留的十進位位數。若為其他所有資料型別，
       此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是時間間隔型別，
       此欄位包含一項規格，說明此屬性的時間間隔包含哪些時間欄位（field），例如 <code class="literal">YEAR TO
       MONTH</code>、<code class="literal">DAY TO SECOND</code> 等。若未指定
       時間欄位限制（也就是該時間間隔接受所有時間欄位），以及對於其他所有資料型別，
       此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
       （時間間隔型別屬性的秒數小數部分精確度，請參閱
       <code class="literal">datetime_precision</code>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該屬性資料型別的資料庫名稱
       （一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該屬性資料型別的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attribute_udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       屬性資料型別的名稱
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
       此屬性之資料型別描述子的識別碼，在與該複合型別相關的資料型別描述子中是唯一的。
       這主要用於與此類識別碼的其他實例進行連接。（識別碼的具體格式並未定義，
       也不保證在未來版本中維持不變。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_derived_reference_attribute</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr></tbody></table>

<br>

關於部分欄位的進一步資訊，另請參閱結構類似的檢視表[第 35.17 節](infoschema-columns.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-attributes.html)（原文版本：18.6；核對日期：2026-10-18）
