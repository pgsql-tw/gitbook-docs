<a id="INFOSCHEMA-ELEMENT-TYPES"></a>
## 35.24. `element_types` [#](#infoschema-element-types) <a href="#infoschema-element-types" id="infoschema-element-types"></a>

檢視表 `element_types` 包含陣列元素的資料型別描述子。當資料表欄位、複合型別屬性、網域、函式參數或函式回傳值被定義為陣列型別時，相應的資訊綱要檢視表只會在欄位 `data_type` 中包含 `ARRAY`。若要取得陣列元素型別的資訊，你可以將相應的檢視表與此檢視表連接。例如，若要顯示某資料表的欄位及其資料型別，以及（若適用）陣列元素型別，你可以這樣做：

```

SELECT c.column_name, c.data_type, e.data_type AS element_type
FROM information_schema.columns c LEFT JOIN information_schema.element_types e
     ON ((c.table_catalog, c.table_schema, c.table_name, 'TABLE', c.dtd_identifier)
       = (e.object_catalog, e.object_schema, e.object_name, e.object_type, e.collection_type_identifier))
WHERE c.table_schema = '...' AND c.table_name = '...'
ORDER BY c.ordinal_position;
```

此檢視表只包含目前使用者有權存取（身為擁有者或具有某種權限）的物件。

<a id="id-1.7.6.28.3"></a>

**表 35.22. `element_types` 欄位**

<table border="1" class="table" summary="element_types 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含使用所描述陣列之物件的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含使用所描述陣列之物件的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       使用所描述陣列之物件的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_type</code> <code class="type">character_data</code>
</p>
<p>
       使用所描述陣列之物件的類型，為下列之一：<code class="literal">TABLE</code>（該陣列由該資料表的某個欄位使用）、<code class="literal">USER-DEFINED TYPE</code>（該陣列由該複合型別的某個屬性使用）、<code class="literal">DOMAIN</code>（該陣列由該網域使用）、<code class="literal">ROUTINE</code>（該陣列由該函式的某個參數或回傳資料型別使用）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collection_type_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       所描述陣列之資料型別描述子的識別碼。可用它與其他資訊綱要檢視表的 <code class="literal">dtd_identifier</code> 欄位進行連接。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">data_type</code> <code class="type">character_data</code>
</p>
<p>
       若陣列元素為內建型別，則為陣列元素的資料型別；否則為 <code class="literal">USER-DEFINED</code>（此時型別由 <code class="literal">udt_name</code> 及相關欄位識別）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_maximum_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於陣列元素資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_octet_length</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於陣列元素資料型別
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
       包含元素型別之定序的資料庫名稱（一律為目前資料庫）；若為預設定序，或元素的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含元素型別之定序的綱要名稱；若為預設定序，或元素的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       元素型別之定序的名稱；若為預設定序，或元素的資料型別不可定序，則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於陣列元素資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_precision_radix</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於陣列元素資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numeric_scale</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於陣列元素資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datetime_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於陣列元素資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_type</code> <code class="type">character_data</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於陣列元素資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">interval_precision</code> <code class="type">cardinal_number</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 不會將此資訊套用於陣列元素資料型別
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義元素資料型別的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義元素資料型別的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       元素資料型別的名稱
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
       元素之資料型別描述子的識別碼。此欄位目前沒有用處。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-element-types.html)（原文版本：18.6；核對日期：2026-10-18）
