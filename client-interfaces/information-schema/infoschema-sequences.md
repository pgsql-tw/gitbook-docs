<a id="INFOSCHEMA-SEQUENCES"></a>
## 35.47. `sequences` [#](#infoschema-sequences) <a href="#infoschema-sequences" id="infoschema-sequences"></a>

檢視表 `sequences` 包含目前資料庫中定義的所有序列。只有目前使用者可存取的序列才會顯示（使用者為其擁有者或具有某項權限時即可存取）。

<a id="id-1.7.6.51.3"></a>

**表 35.45. `sequences` 欄位**

<table border="1" class="table" summary="sequences 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該序列的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該序列的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       序列名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       序列的資料型別。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       此欄位包含序列資料型別（見上文）的精確度（宣告的或隱含的）。精確度表示有效位數。它可以用十進位（以 10 為底）或二進位（以 2 為底）表示，由欄位 <code class="literal">numeric_precision_radix</code> 指定。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       此欄位表示欄位 <code class="literal">numeric_precision</code> 與 <code class="literal">numeric_scale</code> 中的值以何種基數表示。其值為 2 或 10。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       此欄位包含序列資料型別（見上文）的小數位數（宣告的或隱含的）。小數位數表示小數點右側的有效位數。它可以用十進位（以 10 為底）或二進位（以 2 為底）表示，由欄位 <code class="literal">numeric_precision_radix</code> 指定。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">start_value</code> <code class="type">character_data</code>
</p>
<p>
       序列的起始值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">minimum_value</code> <code class="type">character_data</code>
</p>
<p>
       序列的最小值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">maximum_value</code> <code class="type">character_data</code>
</p>
<p>
       序列的最大值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">increment</code> <code class="type">character_data</code>
</p>
<p>
       序列的遞增量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cycle_option</code> <code class="type">yes_or_no</code>
</p>
<p>
若序列會循環，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
</p></td></tr></tbody></table>

<br>

請注意，依照 SQL 標準，起始值、最小值、最大值與遞增量會以字串形式傳回。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-sequences.html)（原文版本：18.6；核對日期：2026-10-18）
