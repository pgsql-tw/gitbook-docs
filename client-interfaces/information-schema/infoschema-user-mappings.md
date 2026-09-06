## 35.62. `user_mappings` [#](#INFOSCHEMA-USER-MAPPINGS)

檢視表 `user_mappings` 包含目前資料庫中定義的所有使用者對應。只有目前使用者
可存取相應外部伺服器的使用者對應會顯示在此檢視表中（使用者為其擁有者或具有某項
權限時即可存取）。

<a id="id-1.7.6.66.3"></a>

**表 35.60. `user_mappings` 欄位**

<table border="1" class="table" summary="user_mappings 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-user-mappings.html)】
