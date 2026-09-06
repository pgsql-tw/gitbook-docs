## 35.31. `foreign_tables` [#](#INFOSCHEMA-FOREIGN-TABLES)

檢視表 `foreign_tables` 包含目前資料庫中定義的所有外部資料表。只有目前使用者
可存取的外部資料表會顯示在此檢視表中（使用者為其擁有者或具有某項權限時即可
存取）。

<a id="id-1.7.6.35.3"></a>

**表 35.29. `foreign_tables` 欄位**

<table border="1" class="table" summary="foreign_tables 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義外部資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含外部資料表的 schema 名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義外部伺服器的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部伺服器名稱
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-foreign-tables.html)】
