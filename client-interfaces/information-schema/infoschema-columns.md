<a id="INFOSCHEMA-COLUMNS"></a>
## 35.17. `columns` [#](#infoschema-columns) <a href="#infoschema-columns" id="infoschema-columns"></a>

檢視表 `columns` 包含資料庫中所有資料表欄位（或檢視表欄位）的資訊。系統欄位（`ctid` 等）不包含在內。只會顯示目前使用者有權存取（身為擁有者或具有某種權限）的欄位。

<a id="id-1.7.6.21.3"></a>

**表 35.15. `columns` 欄位**

<table border="1" class="table" summary="columns 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       欄位名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordinal_position</code> <code class="type">cardinal_number</code>
</p>
<p>
       欄位在資料表中的序數位置（從 1 開始計數）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">column_default</code> <code class="type">character_data</code>
</p>
<p>
       欄位的預設值運算式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_nullable</code> <code class="type">yes_or_no</code>
</p>
<p>
若欄位可能可以為 null，則為 <code class="literal">YES</code>；若已知欄位不可為 null，則為 <code class="literal">NO</code>。非 null 限制條件是得知欄位不可為 null 的一種方式，但也可能有其他方式。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       若欄位為內建型別，則為該欄位的資料型別；若為某種陣列，則為 <code class="literal">ARRAY</code>（此時請參閱檢視表 <code class="literal">element_types</code>）；否則為 <code class="literal">USER-DEFINED</code>（此時型別由 <code class="literal">udt_name</code> 及相關欄位識別）。若欄位以網域為基礎，此欄位指的是該網域的底層型別（而網域本身由 <code class="literal">domain_name</code> 及相關欄位識別）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是字元或位元字串型別，則為宣告的最大長度；若為其他所有資料型別，或未宣告最大長度，則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是字元型別，則為單一資料值（datum）可能的最大長度，以八位元組（位元組）計；若為其他所有資料型別，則為 null。最大八位元組長度取決於宣告的字元最大長度（見上文）以及伺服器編碼。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是數值型別，此欄位包含此欄位所用型別的（宣告或隱含的）精確度。精確度表示有效位數，可以用十進位（以 10 為基數）或二進位（以 2 為基數）表示，依欄位 <code class="literal">numeric_precision_radix</code> 所指定。若為其他所有資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是數值型別，此欄位指出欄位 <code class="literal">numeric_precision</code> 與 <code class="literal">numeric_scale</code> 中的值是以哪一種基數表示。其值為 2 或 10。若為其他所有資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是精確數值型別，此欄位包含此欄位所用型別的（宣告或隱含的）小數位數（scale）。小數位數表示小數點右側的有效位數，可以用十進位（以 10 為基數）或二進位（以 2 為基數）表示，依欄位 <code class="literal">numeric_precision_radix</code> 所指定。若為其他所有資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是日期、時間、時間戳記或時間間隔型別，此欄位包含此欄位所用型別的（宣告或隱含的）秒數小數部分精確度，也就是秒數值中小數點之後保留的十進位位數。若為其他所有資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       若 <code class="literal">data_type</code> 識別的是時間間隔型別，此欄位包含一項規格，說明此欄位的時間間隔包含哪些時間欄位（field），例如 <code class="literal">YEAR TO
       MONTH</code>、<code class="literal">DAY TO SECOND</code> 等。若未指定時間欄位限制（也就是該時間間隔接受所有時間欄位），以及對於其他所有資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能（時間間隔型別欄位的秒數小數部分精確度，請參閱 <code class="literal">datetime_precision</code>）
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
       包含該欄位之定序的資料庫名稱（一律為目前資料庫）；若為預設定序，或欄位的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該欄位之定序的綱要名稱；若為預設定序，或欄位的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       欄位的定序名稱；若為預設定序，或欄位的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       若欄位具有網域型別，則為定義該網域的資料庫名稱（一律為目前資料庫）；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       若欄位具有網域型別，則為定義該網域的綱要名稱；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       若欄位具有網域型別，則為該網域的名稱；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該欄位資料型別（若適用，則為網域的底層型別）的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該欄位資料型別（若適用，則為網域的底層型別）的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       欄位資料型別（若適用，則為網域的底層型別）的名稱
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
       欄位之資料型別描述子的識別碼，在與該資料表相關的資料型別描述子中是唯一的。這主要用於與此類識別碼的其他實例進行連接。（識別碼的具體格式並未定義，也不保證在未來版本中維持不變。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_self_referencing</code> <code class="type">yes_or_no</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_identity</code> <code class="type">yes_or_no</code>
</p>
<p>
       若欄位是識別欄位，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">identity_generation</code> <code class="type">character_data</code>
</p>
<p>
       若欄位是識別欄位，則為 <code class="literal">ALWAYS</code> 或 <code class="literal">BY DEFAULT</code>，反映該欄位的定義。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">identity_start</code> <code class="type">character_data</code>
</p>
<p>
       若欄位是識別欄位，則為內部序列的起始值；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">identity_increment</code> <code class="type">character_data</code>
</p>
<p>
       若欄位是識別欄位，則為內部序列的遞增量；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">identity_maximum</code> <code class="type">character_data</code>
</p>
<p>
       若欄位是識別欄位，則為內部序列的最大值；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">identity_minimum</code> <code class="type">character_data</code>
</p>
<p>
       若欄位是識別欄位，則為內部序列的最小值；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">identity_cycle</code> <code class="type">yes_or_no</code>
</p>
<p>
       若欄位是識別欄位，則內部序列會循環時為 <code class="literal">YES</code>，不會循環時為 <code class="literal">NO</code>；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_generated</code> <code class="type">character_data</code>
</p>
<p>
       若欄位是產生欄位，則為 <code class="literal">ALWAYS</code>；否則為 <code class="literal">NEVER</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">generation_expression</code> <code class="type">character_data</code>
</p>
<p>
       若欄位是產生欄位，則為其產生運算式；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_updatable</code> <code class="type">yes_or_no</code>
</p>
<p>
若欄位可更新，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>（基底資料表中的欄位一律可更新，檢視表中的欄位則不一定）
      </p></td></tr></tbody></table>

<br>

由於在 SQL 中可以用各種方式定義資料型別，而 PostgreSQL 又提供了額外的資料型別定義方式，因此要在資訊綱要中表示這些資料型別可能有些困難。欄位 `data_type` 的用意是識別欄位的底層內建型別。在 PostgreSQL 中，這表示該型別定義於系統目錄綱要 `pg_catalog` 中。若應用程式能對眾所周知的內建型別做特別處理（例如以不同方式格式化數值型別，或使用精確度欄位中的資料），這個欄位可能會有用。欄位 `udt_name`、`udt_schema` 與 `udt_catalog` 一律會識別欄位的底層資料型別，即使欄位以網域為基礎也是如此。（由於 PostgreSQL 將內建型別視同使用者定義型別處理，內建型別也會出現在這裡。這是對 SQL 標準的擴充。）若應用程式想依型別以不同方式處理資料，就應該使用這些欄位，因為在那種情況下，欄位實際上是否以網域為基礎並不重要。若欄位以網域為基礎，網域的識別資訊會存放在欄位 `domain_name`、`domain_schema` 與 `domain_catalog` 中。若你想將欄位與其相關聯的資料型別配對，並把網域視為獨立的型別，可以寫成 `coalesce(domain_name,
udt_name)` 等。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-columns.html)（原文版本：18.6；核對日期：2026-10-18）
