<a id="INFOSCHEMA-TRIGGERS"></a>
## 35.57. `triggers` [#](#infoschema-triggers) <a href="#infoschema-triggers" id="infoschema-triggers"></a>

檢視表 `triggers` 包含目前資料庫中，定義在目前使用者所擁有、或具有
`SELECT` 以外某項權限之資料表與檢視表上的所有觸發程序。

<a id="id-1.7.6.61.3"></a>

**表 35.55. `triggers` 欄位**

<table border="1" class="table" summary="triggers 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trigger_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含觸發程序的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trigger_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含觸發程序的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trigger_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       觸發程序名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">event_manipulation</code> <code class="type">character_data</code>
</p>
<p>
       引發此觸發程序的事件（<code class="literal">INSERT</code>、
       <code class="literal">UPDATE</code> 或 <code class="literal">DELETE</code>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">event_object_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含定義此觸發程序之資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">event_object_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含定義此觸發程序之資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">event_object_table</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義此觸發程序的資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">action_order</code> <code class="type">cardinal_number</code>
</p>
<p>
       同一資料表上具有相同
       <code class="literal">event_manipulation</code>、
       <code class="literal">action_timing</code> 與
       <code class="literal">action_orientation</code> 的觸發程序之間的觸發順序。在
       <span class="productname">PostgreSQL</span> 中，觸發程序依名稱順序觸發，
       因此此欄位反映的就是該順序。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">action_condition</code> <code class="type">character_data</code>
</p>
<p>
觸發程序的 <code class="literal">WHEN</code> 條件；若無則為 null
       （若資料表並非由目前已啟用的角色擁有，也為 null）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">action_statement</code> <code class="type">character_data</code>
</p>
<p>
       觸發程序所執行的陳述式（目前一律為
       <code class="literal">EXECUTE FUNCTION
       <em class="replaceable"><code>function</code></em>(...)</code>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">action_orientation</code> <code class="type">character_data</code>
</p>
<p>
       表示觸發程序是對每個處理的資料列各觸發一次，還是對每個陳述式各觸發一次
       （<code class="literal">ROW</code> 或
       <code class="literal">STATEMENT</code>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">action_timing</code> <code class="type">character_data</code>
</p>
<p>
       觸發程序的觸發時機（<code class="literal">BEFORE</code>、
       <code class="literal">AFTER</code> 或 <code class="literal">INSTEAD OF</code>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">action_reference_old_table</code> <code class="type">sql_identifier</code>
</p>
<p>
       <span class="quote">「<span class="quote">old</span>」</span>轉換資料表的名稱；若無則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">action_reference_new_table</code> <code class="type">sql_identifier</code>
</p>
<p>
       <span class="quote">「<span class="quote">new</span>」</span>轉換資料表的名稱；若無則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">action_reference_old_row</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">action_reference_new_row</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">created</code> <code class="type">time_stamp</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 未提供的功能
</p></td></tr></tbody></table>

<br>

PostgreSQL 中的觸發程序與 SQL 標準有兩處不相容，會影響其在資訊綱要中的
呈現方式。第一，在 PostgreSQL 中，觸發程序名稱是各資料表的區域名稱，而不是
獨立的綱要物件。因此，只要分屬不同的資料表，同一綱要中就可以定義名稱重複的
觸發程序。（`trigger_catalog` 與
`trigger_schema` 實際上是與定義該觸發程序之資料表相關的值。）第二，在
PostgreSQL 中，觸發程序可以定義為在多個事件上觸發（例如 `ON INSERT OR
UPDATE`），而 SQL 標準只允許一個事件。若觸發程序定義為在多個事件上觸發，
它在資訊綱要中會以多個資料列表示，每種事件型別各一列。由於這兩個問題，
檢視表 `triggers` 的主鍵實際上是
`(trigger_catalog, trigger_schema, event_object_table,
trigger_name, event_manipulation)`，而不是 SQL 標準所規定的
`(trigger_catalog, trigger_schema, trigger_name)`。
儘管如此，若你以符合 SQL 標準的方式定義觸發程序（觸發程序名稱在綱要中唯一，
且每個觸發程序只有一種事件型別），就不會受到影響。

### 注意

在 PostgreSQL 9.1 之前，此檢視表的欄位
`action_timing`、
`action_reference_old_table`、
`action_reference_new_table`、
`action_reference_old_row` 與
`action_reference_new_row`
分別命名為
`condition_timing`、
`condition_reference_old_table`、
`condition_reference_new_table`、
`condition_reference_old_row` 與
`condition_reference_new_row`。
這是它們在 SQL:1999 標準中的名稱；新的命名則符合 SQL:2003 及之後的標準。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-triggers.html)（原文版本：18.6；核對日期：2026-10-18）
