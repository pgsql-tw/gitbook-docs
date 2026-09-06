## 35.65. `view_table_usage` [#](#INFOSCHEMA-VIEW-TABLE-USAGE)

檢視表 `view_table_usage` 列出檢視表查詢表示式（定義該檢視表的 `SELECT`
敘述）所使用的所有資料表。只有目前已啟用角色所擁有的資料表才會包含在內。

### 注意

不包含系統資料表。此問題應於未來修正。

<a id="id-1.7.6.69.4"></a>

**表 35.63. `view_table_usage` 欄位**

<table border="1" class="table" summary="view_table_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">view_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含檢視表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">view_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含檢視表的 schema 名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">view_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       檢視表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含檢視表所用資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含檢視表所用資料表的 schema 名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       檢視表所用資料表的名稱
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-view-table-usage.html)】
