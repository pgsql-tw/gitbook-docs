<a id="INFOSCHEMA-ROLE-USAGE-GRANTS"></a>
## 35.39. `role_usage_grants` [#](#infoschema-role-usage-grants) <a href="#infoschema-role-usage-grants" id="infoschema-role-usage-grants"></a>

檢視表 `role_usage_grants` 列出在各類物件上授與、且授與者或受授與者為目前已啟用角色的 `USAGE` 權限。更多資訊可在 `usage_privileges` 中找到。此檢視表與 `usage_privileges` 唯一的實質差異在於，此檢視表會省略透過授與 `PUBLIC` 而讓目前使用者可存取的物件。

<a id="id-1.7.6.43.3"></a>

**表 35.37. `role_usage_grants` 欄位**

<table border="1" class="table" summary="role_usage_grants 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantor</code> <code class="type">sql_identifier</code>
</p>
<p>
       授與該權限的角色名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantee</code> <code class="type">sql_identifier</code>
</p>
<p>
       被授與該權限的角色名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該物件的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該物件的綱要名稱（若適用），否則為空字串
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       物件名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_type</code> <code class="type">character_data</code>
</p>
<p>
<code class="literal">COLLATION</code>、<code class="literal">DOMAIN</code>、<code class="literal">FOREIGN DATA WRAPPER</code>、<code class="literal">FOREIGN SERVER</code> 或 <code class="literal">SEQUENCE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privilege_type</code> <code class="type">character_data</code>
</p>
<p>
       一律為 <code class="literal">USAGE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
若該權限可再授與他人，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-role-usage-grants.html)（原文版本：18.6；核對日期：2026-10-18）
