<a id="INFOSCHEMA-CHECK-CONSTRAINT-ROUTINE-USAGE"></a>
## 35.8. `check_constraint_routine_usage` [#](#infoschema-check-constraint-routine-usage) <a href="#infoschema-check-constraint-routine-usage" id="infoschema-check-constraint-routine-usage"></a>

檢視表 `check_constraint_routine_usage` 識別被檢查限制條件所使用的常式（函式與
程序）。只會顯示由目前已啟用角色所擁有的常式。

<a id="id-1.7.6.12.3"></a>

**表 35.6. `check_constraint_routine_usage` 欄位**

<table border="1" class="table" summary="check_constraint_routine_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該函式的<span class="quote">“<span class="quote">特定名稱</span>”</span>。詳細資訊請參閱<a class="xref" href="infoschema-routines.md">第 35.45 節</a>。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-check-constraint-routine-usage.html)（原文版本：18.6；核對日期：2026-10-18）
