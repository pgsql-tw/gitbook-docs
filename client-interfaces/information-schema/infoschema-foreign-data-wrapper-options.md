<a id="INFOSCHEMA-FOREIGN-DATA-WRAPPER-OPTIONS"></a>
## 35.26. `foreign_data_wrapper_options` [#](#INFOSCHEMA-FOREIGN-DATA-WRAPPER-OPTIONS)

檢視表 `foreign_data_wrapper_options` 包含目前資料庫中為外部資料包裝器定義的所有選項。只有目前使用者可存取（身為擁有者或具有某種權限）的外部資料包裝器才會顯示。

<a id="id-1.7.6.30.3"></a>

**表 35.24. `foreign_data_wrapper_options` 欄位**

<table border="1" class="table" summary="foreign_data_wrapper_options 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該外部資料包裝器的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部資料包裝器名稱
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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-foreign-data-wrapper-options.html)（原文版本：18.6；核對日期：2026-10-18）
