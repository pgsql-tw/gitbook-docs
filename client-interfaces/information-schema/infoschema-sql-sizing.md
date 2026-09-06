## 35.51. `sql_sizing` [#](#INFOSCHEMA-SQL-SIZING)

資料表 `sql_sizing` 包含 PostgreSQL 中各種大小限制與最大值的資訊。此資訊主要
供 ODBC 介面使用；其他介面的使用者可能很少需要使用。因此，這裡不會說明個別的
大小項目；請參閱 ODBC 介面的說明。

<a id="id-1.7.6.55.3"></a>

**表 35.49. `sql_sizing` 欄位**

<table border="1" class="table" summary="sql_sizing 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sizing_id</code> <code class="type">cardinal_number</code>
</p>
<p>
       大小項目的識別字
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sizing_name</code> <code class="type">character_data</code>
</p>
<p>
       大小項目的描述性名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">supported_value</code> <code class="type">cardinal_number</code>
</p>
<p>
       大小項目的值；若大小無限制或無法判定則為 0；若不支援適用此大小項目的
       功能則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comments</code> <code class="type">character_data</code>
</p>
<p>
       可能與大小項目相關的註解
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-sql-sizing.html)】
