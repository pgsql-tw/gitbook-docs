<a id="INFOSCHEMA-FOREIGN-DATA-WRAPPERS"></a>
## 35.27. `foreign_data_wrappers` [#](#infoschema-foreign-data-wrappers) <a href="#infoschema-foreign-data-wrappers" id="infoschema-foreign-data-wrappers"></a>

檢視表 `foreign_data_wrappers` 包含目前資料庫中定義的所有外部資料包裝器。只有目前使用者可存取（身為擁有者或具有某種權限）的外部資料包裝器才會顯示。

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
       包含該外部資料包裝器的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部資料包裝器名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">authorization_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部伺服器擁有者的名稱（原文此處寫作「外部伺服器」（foreign server）；就此檢視表而言，此欄位實際上是該外部資料包裝器擁有者的名稱）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">library_name</code> <code class="type">character_data</code>
</p>
<p>
       實作此外部資料包裝器的程式庫檔案名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_language</code> <code class="type">character_data</code>
</p>
<p>
       用於實作此外部資料包裝器的語言
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-foreign-data-wrappers.html)（原文版本：18.6；核對日期：2026-10-18）
