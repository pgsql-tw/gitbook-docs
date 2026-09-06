## 35.12. `column_column_usage` [#](#INFOSCHEMA-COLUMN-COLUMN-USAGE)

檢視表 `column_column_usage` 列出相同資料表中依賴另一個基礎欄位的所有產生欄位。
只包含目前已啟用角色所擁有的資料表。

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
       包含資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含資料表的 schema 名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       產生欄位所依賴的基礎欄位名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dependent_column</code> <code class="type">sql_identifier</code>
</p>
<p>
       產生欄位名稱
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-column-column-usage.html)】
