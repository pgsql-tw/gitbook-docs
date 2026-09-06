## 35.27. `foreign_data_wrappers` [#](#INFOSCHEMA-FOREIGN-DATA-WRAPPERS)

檢視表 `foreign_data_wrappers` 包含目前資料庫中定義的所有外部資料封裝器。只有
目前使用者可存取的外部資料封裝器會顯示在此檢視表中（使用者為其擁有者或具有某項
權限時即可存取）。

<a id="id-1.7.6.31.3"></a>

**表 35.25. `foreign_data_wrappers` 欄位**

<table border="1" class="table" summary="foreign_data_wrappers 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含外部資料封裝器的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部資料封裝器名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">authorization_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部伺服器擁有者的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">library_name</code> <code class="type">character_data</code>
</p>
<p>
       實作此外部資料封裝器的程式庫檔案名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_language</code> <code class="type">character_data</code>
</p>
<p>
       用於實作此外部資料封裝器的語言
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-foreign-data-wrappers.html)】
