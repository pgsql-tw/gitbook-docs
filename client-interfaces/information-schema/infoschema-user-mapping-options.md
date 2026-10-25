<a id="INFOSCHEMA-USER-MAPPING-OPTIONS"></a>
## 35.61. `user_mapping_options` [#](#infoschema-user-mapping-options) <a href="#infoschema-user-mapping-options" id="infoschema-user-mapping-options"></a>

檢視表 `user_mapping_options` 包含目前資料庫中為使用者對應定義的所有選項。
只有目前使用者可存取相應外部伺服器的使用者對應才會顯示（使用者為該外部伺服器的
擁有者或具有某項權限時即可存取）。

<a id="id-1.7.6.65.3"></a>

**表 35.59. `user_mapping_options` 欄位**

<table border="1" class="table" summary="user_mapping_options 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">authorization_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       正在對應的使用者名稱；若為公開對應，則為 <code class="literal">PUBLIC</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義此對應所用外部伺服器的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       此對應所用外部伺服器的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">option_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       選項名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">option_value</code> <code class="type">character_data</code>
</p>
<p>
       選項值。除非目前使用者就是被對應的使用者，或此對應是針對
       <code class="literal">PUBLIC</code> 且目前使用者是該伺服器的擁有者，
       或目前使用者是超級使用者，否則此欄位會顯示為 null。這是為了保護以
       使用者對應選項形式儲存的密碼資訊。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-user-mapping-options.html)（原文版本：18.6；核對日期：2026-10-18）
