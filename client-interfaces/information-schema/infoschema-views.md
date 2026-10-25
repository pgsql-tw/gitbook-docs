<a id="INFOSCHEMA-VIEWS"></a>
## 35.66. `views` [#](#infoschema-views) <a href="#infoschema-views" id="infoschema-views"></a>

檢視表 `views` 包含目前資料庫中定義的所有檢視表。只有目前使用者可存取的檢視表
才會顯示（使用者為其擁有者或具有某項權限時即可存取）。

<a id="id-1.7.6.70.3"></a>

**表 35.64. `views` 欄位**

<table border="1" class="table" summary="views 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含檢視表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含檢視表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       檢視表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">view_definition</code> <code class="type">character_data</code>
</p>
<p>
       定義此檢視表的查詢表示式（若檢視表並非由目前已啟用的角色擁有，
       則為 null）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">check_option</code> <code class="type">character_data</code>
</p>
<p>
<code class="literal">CASCADED</code> 或 <code class="literal">LOCAL</code>（若檢視表上
       定義了 <code class="literal">CHECK OPTION</code>）；若未定義則為
       <code class="literal">NONE</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_updatable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> 表示檢視表可更新（允許
       <code class="command">UPDATE</code> 與 <code class="command">DELETE</code>），
       <code class="literal">NO</code> 表示不可更新
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_insertable_into</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> 表示檢視表可插入（允許
       <code class="command">INSERT</code>），<code class="literal">NO</code> 表示不可插入
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_trigger_updatable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> 表示檢視表上定義了 <code class="literal">INSTEAD OF</code>
<code class="command">UPDATE</code> 觸發程序，<code class="literal">NO</code> 表示沒有
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_trigger_deletable</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> 表示檢視表上定義了 <code class="literal">INSTEAD OF</code>
<code class="command">DELETE</code> 觸發程序，<code class="literal">NO</code> 表示沒有
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_trigger_insertable_into</code> <code class="type">yes_or_no</code>
</p>
<p>
<code class="literal">YES</code> 表示檢視表上定義了 <code class="literal">INSTEAD OF</code>
<code class="command">INSERT</code> 觸發程序，<code class="literal">NO</code> 表示沒有
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-views.html)（原文版本：18.6；核對日期：2026-10-18）
