<a id="INFOSCHEMA-VIEW-TABLE-USAGE"></a>
## 35.65. `view_table_usage` [#](#infoschema-view-table-usage) <a href="#infoschema-view-table-usage" id="infoschema-view-table-usage"></a>

檢視表 `view_table_usage` 列出檢視表的查詢表示式（定義該檢視表的 `SELECT`
陳述式）中使用的所有資料表。只有由目前已啟用的角色擁有的資料表才會納入。

### 注意

不包含系統資料表。此問題日後應予修正。

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
       包含檢視表的綱要名稱
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
       包含檢視表所用資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       檢視表所用資料表的名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-view-table-usage.html)（原文版本：18.6；核對日期：2026-10-18）
