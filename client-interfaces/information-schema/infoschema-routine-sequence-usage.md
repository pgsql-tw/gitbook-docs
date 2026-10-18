<a id="INFOSCHEMA-ROUTINE-SEQUENCE-USAGE"></a>
## 35.43. `routine_sequence_usage` [#](#INFOSCHEMA-ROUTINE-SEQUENCE-USAGE)

檢視表 `routine_sequence_usage` 列出函式或程序在 SQL 主體或參數預設值表示式中所使用的所有序列。（這只適用於未加引號的 SQL 主體，不適用於加引號的主體或其他語言的函式。）只有當序列由目前已啟用的角色所擁有時，才會包含該序列。

<a id="id-1.7.6.47.3"></a>

**表 35.41. `routine_sequence_usage` 欄位**

<table border="1" class="table" summary="routine_sequence_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
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
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       函式名稱（多載時可能重複）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schema_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式所使用之序列的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式所使用之序列的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sequence_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該函式所使用的序列名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-routine-sequence-usage.html)（原文版本：18.6；核對日期：2026-10-18）
