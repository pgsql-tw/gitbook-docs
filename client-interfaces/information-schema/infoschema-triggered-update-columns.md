<a id="INFOSCHEMA-TRIGGERED-UPDATE-COLUMNS"></a>
## 35.56. `triggered_update_columns` [#](#INFOSCHEMA-TRIGGERED-UPDATE-COLUMNS)

對於目前資料庫中指定了欄位清單（例如 `UPDATE OF column1, column2`）的觸發程序，
檢視表 `triggered_update_columns` 會列出這些欄位。未指定欄位清單的觸發程序
不包含在此檢視表中。只會顯示目前使用者擁有，或具有 `SELECT` 以外某種權限的
欄位。

<a id="id-1.7.6.60.3"></a>

**表 35.54. `triggered_update_columns` 欄位**

<table border="1" class="table" summary="triggered_update_columns 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trigger_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該觸發程序的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trigger_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該觸發程序的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">trigger_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       觸發程序的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">event_object_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該觸發程序所在資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">event_object_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該觸發程序所在資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">event_object_table</code> <code class="type">sql_identifier</code>
</p>
<p>
       該觸發程序所在資料表的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">event_object_column</code> <code class="type">sql_identifier</code>
</p>
<p>
       該觸發程序所在欄位的名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-triggered-update-columns.html)（原文版本：18.6；核對日期：2026-10-18）
