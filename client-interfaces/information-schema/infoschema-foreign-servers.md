<a id="INFOSCHEMA-FOREIGN-SERVERS"></a>
## 35.29. `foreign_servers` [#](#INFOSCHEMA-FOREIGN-SERVERS)

檢視表 `foreign_servers` 包含目前資料庫中定義的所有外部伺服器。只有目前使用者可存取（身為擁有者或具有某種權限）的外部伺服器才會顯示。

<a id="id-1.7.6.33.3"></a>

**表 35.27. `foreign_servers` 欄位**

<table border="1" class="table" summary="foreign_servers 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">foreign_data_wrapper_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該外部伺服器所使用之外部資料包裝器的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_data_wrapper_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該外部伺服器所使用的外部資料包裝器名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_type</code> <code class="type">character_data</code>
</p>
<p>
       外部伺服器的類型資訊（若建立時有指定）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_version</code> <code class="type">character_data</code>
</p>
<p>
       外部伺服器的版本資訊（若建立時有指定）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">authorization_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部伺服器擁有者的名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-foreign-servers.html)（原文版本：18.6；核對日期：2026-10-18）
