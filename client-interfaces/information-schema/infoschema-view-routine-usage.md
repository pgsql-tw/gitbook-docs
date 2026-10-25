<a id="INFOSCHEMA-VIEW-ROUTINE-USAGE"></a>
## 35.64. `view_routine_usage` [#](#infoschema-view-routine-usage) <a href="#infoschema-view-routine-usage" id="infoschema-view-routine-usage"></a>

檢視表 `view_routine_usage` 列出檢視表的查詢表示式（定義該檢視表的
`SELECT` 陳述式）中使用的所有常式（函式與程序）。只有由目前已啟用的
角色擁有的常式才會納入。

<a id="id-1.7.6.68.3"></a>

**表 35.62. `view_routine_usage` 欄位**

<table border="1" class="table" summary="view_routine_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       函式的<span class="quote">「<span class="quote">特定名稱</span>」</span>（specific name）。詳細資訊請參閱<a class="xref" href="infoschema-routines.md">第 35.45 節</a>。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-view-routine-usage.html)（原文版本：18.6；核對日期：2026-10-18）
