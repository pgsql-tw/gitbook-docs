<a id="INFOSCHEMA-COLUMN-COLUMN-USAGE"></a>
## 35.12. `column_column_usage` [#](#infoschema-column-column-usage) <a href="#infoschema-column-column-usage" id="infoschema-column-column-usage"></a>

檢視表 `column_column_usage` 列出所有相依於同一資料表中另一個基底欄位的產生欄位。只包含由目前已啟用角色所擁有的資料表。

<a id="id-1.7.6.16.3"></a>

**表 35.10. `column_column_usage` 欄位**

<table border="1" class="table" summary="column_column_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
       產生欄位所相依的基底欄位名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dependent_column</code> <code class="type">sql_identifier</code>
</p>
<p>
       產生欄位的名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-column-column-usage.html)（原文版本：18.6；核對日期：2026-10-18）
