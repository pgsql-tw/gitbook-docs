<a id="INFOSCHEMA-DOMAINS"></a>
## 35.23. `domains` [#](#INFOSCHEMA-DOMAINS)

檢視表 `domains` 包含目前資料庫中定義的所有[*[網域](../../appendixes/glossary/README.md#GLOSSARY-DOMAIN)*](../../appendixes/glossary/README.md#GLOSSARY-DOMAIN)。只會顯示目前使用者有權存取（身為擁有者或具有某種權限）的網域。

<a id="id-1.7.6.27.3"></a>

**表 35.21. `domains` 欄位**

<table border="1" class="table" summary="domains 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該網域的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該網域的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       網域名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       若網域為內建型別，則為該網域的資料型別；若為某種陣列，則為 <code class="literal">ARRAY</code>（此時請參閱檢視表 <code class="literal">element_types</code>）；否則為 <code class="literal">USER-DEFINED</code>（此時型別由 <code class="literal">udt_name</code> 及相關欄位識別）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       若網域為字元或位元字串型別，則為宣告的最大長度；其他資料型別，或未宣告最大長度時，則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       若網域為字元型別，則為單一資料值以八位元組（位元組）計的最大可能長度；其他資料型別則為 null。最大八位元組長度取決於宣告的字元最大長度（見上方）與伺服器編碼。
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
       包含該網域之定序的資料庫名稱（一律為目前資料庫）；若為預設定序，或網域的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該網域之定序的綱要名稱；若為預設定序，或網域的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該網域之定序的名稱；若為預設定序，或網域的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       若網域為數值型別，此欄位包含此網域之型別的（宣告或隱含）精確度。精確度表示有效位數。它可以用十進位（基數 10）或二進位（基數 2）表示，如欄位 <code class="literal">numeric_precision_radix</code> 所指定。其他資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       若網域為數值型別，此欄位表示欄位 <code class="literal">numeric_precision</code> 與 <code class="literal">numeric_scale</code> 中的值以何種基數表示。其值為 2 或 10。其他資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       若網域為精確數值型別，此欄位包含此網域之型別的（宣告或隱含）小數位數。小數位數表示小數點右側的有效位數。它可以用十進位（基數 10）或二進位（基數 2）表示，如欄位 <code class="literal">numeric_precision_radix</code> 所指定。其他資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       若 <code class="literal">data_type</code> 表示日期、時間、時間戳記或時間間隔型別，此欄位包含此網域之型別的（宣告或隱含）小數秒精確度，也就是秒值中小數點之後保留的十進位位數。其他資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       若 <code class="literal">data_type</code> 表示時間間隔型別，此欄位包含此網域的時間間隔包含哪些時間欄位的規格，例如 <code class="literal">YEAR TO
       MONTH</code>、<code class="literal">DAY TO SECOND</code> 等。若未指定時間欄位限制（亦即該時間間隔接受所有時間欄位），以及其他所有資料型別，此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能（時間間隔型別網域的小數秒精確度請參閱 <code class="literal">datetime_precision</code>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_default</code> <code class="type">character_data</code>
</p>
<p>
       網域的預設值運算式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該網域之資料型別的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該網域之資料型別的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該網域之資料型別的名稱
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
       網域之資料型別描述子的識別碼，在與該網域相關的資料型別描述子中是唯一的（這是理所當然的，因為一個網域只包含一個資料型別描述子）。這主要用於與此類識別碼的其他實例進行連接。（識別碼的具體格式並未定義，也不保證在未來版本中維持不變。）
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-domains.html)（原文版本：18.6；核對日期：2026-10-18）
