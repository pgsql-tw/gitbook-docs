## 35.28. `foreign_server_options` [#](#INFOSCHEMA-FOREIGN-SERVER-OPTIONS)

檢視表 `foreign_server_options` 包含目前資料庫中為外部伺服器定義的所有選項。
只有目前使用者可存取的外部伺服器會顯示在此檢視表中（使用者為其擁有者或具有某項
權限時即可存取）。

<a id="id-1.7.6.32.3"></a>

**表 35.26. `foreign_server_options` 欄位**

<table border="1" class="table" summary="foreign_server_options 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該外部伺服器的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部伺服器名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">option_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       選項名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">option_value</code> <code class="type">character_data</code>
</p>
<p>
       選項值
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-foreign-server-options.html)】
