<a id="INFOSCHEMA-ROUTINE-ROUTINE-USAGE"></a>
## 35.42. `routine_routine_usage` [#](#infoschema-routine-routine-usage) <a href="#infoschema-routine-routine-usage" id="infoschema-routine-routine-usage"></a>

檢視表 `routine_routine_usage` 列出被另一個（或同一個）函式或程序在 SQL 主體或參數預設值表示式中使用的所有函式或程序。（這只適用於未加引號的 SQL 主體，不適用於加引號的主體或其他語言的函式。）只有當被使用的函式由目前已啟用的角色所擁有時，才會在此包含該項目。（使用方的函式則沒有此限制。）

請注意，此檢視表中兩個函式的項目都是指常式的「特定」名稱，即使欄位名稱的使用方式與其他關於常式的資訊綱要檢視表不一致。這是依照 SQL 標準的規定，儘管這可說是設計上的缺失。關於特定名稱的詳細資訊，請參閱[第 35.45 節](infoschema-routines.md)。

<a id="id-1.7.6.46.4"></a>

**表 35.40. `routine_routine_usage` 欄位**

<table border="1" class="table" summary="routine_routine_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含使用方函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含使用方函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       使用方函式的<span class="quote">“<span class="quote">特定名稱</span>”</span>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含第一個函式所使用之函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含第一個函式所使用之函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       第一個函式所使用之函式的<span class="quote">“<span class="quote">特定名稱</span>”</span>。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-routine-routine-usage.html)（原文版本：18.6；核對日期：2026-10-18）
