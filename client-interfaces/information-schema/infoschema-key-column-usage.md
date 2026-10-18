<a id="INFOSCHEMA-KEY-COLUMN-USAGE"></a>
## 35.32. `key_column_usage` [#](#INFOSCHEMA-KEY-COLUMN-USAGE)

檢視表 `key_column_usage` 列出目前資料庫中受某個唯一、主鍵或外鍵限制條件所限制的所有欄位。檢查限制條件不包含在此檢視表中。只有目前使用者可存取（身為擁有者或具有某種權限）的欄位才會顯示。

<a id="id-1.7.6.36.3"></a>

**表 35.30. `key_column_usage` 欄位**

<table border="1" class="table" summary="key_column_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該限制條件的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該限制條件的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       限制條件名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含受此限制條件所限制之欄位所屬資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含受此限制條件所限制之欄位所屬資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含受此限制條件所限制之欄位的資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       受此限制條件所限制的欄位名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ordinal_position</code> <code class="type">cardinal_number</code>
</p>
<p>
       該欄位在限制條件鍵中的序數位置（從 1 起算）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">position_in_unique_constraint</code> <code class="type">cardinal_number</code>
</p>
<p>
       對外鍵限制條件而言，為被參照欄位在其唯一限制條件中的序數位置（從 1 起算）；否則為 null
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-key-column-usage.html)（原文版本：18.6；核對日期：2026-10-18）
