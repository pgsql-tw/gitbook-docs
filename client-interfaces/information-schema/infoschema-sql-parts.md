## 35.50. `sql_parts` [#](#INFOSCHEMA-SQL-PARTS)

資料表 `sql_parts` 包含 PostgreSQL 支援 SQL 標準哪些部分的資訊。

<a id="id-1.7.6.54.3"></a>

**表 35.48. `sql_parts` 欄位**

<table border="1" class="table" summary="sql_parts 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">feature_id</code> <code class="type">character_data</code>
</p>
<p>
       包含部分編號的識別字串
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">feature_name</code> <code class="type">character_data</code>
</p>
<p>
       部分的描述性名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_supported</code> <code class="type">yes_or_no</code>
</p>
<p>
若目前版本的 <span class="productname">PostgreSQL</span> 完全支援該部分，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_verified_by</code> <code class="type">character_data</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 開發團隊不會對功能符合性
       執行正式測試
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comments</code> <code class="type">character_data</code>
</p>
<p>
       可能與該部分支援狀態相關的註解
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-sql-parts.html)】
