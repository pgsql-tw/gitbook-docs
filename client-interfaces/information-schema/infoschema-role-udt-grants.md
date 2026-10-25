<a id="INFOSCHEMA-ROLE-UDT-GRANTS"></a>
## 35.38. `role_udt_grants` [#](#infoschema-role-udt-grants) <a href="#infoschema-role-udt-grants" id="infoschema-role-udt-grants"></a>

檢視表 `role_udt_grants` 旨在列出在使用者定義型別上授與、且授與者或受授與者為目前已啟用角色的 `USAGE` 權限。更多資訊可在 `udt_privileges` 中找到。此檢視表與 `udt_privileges` 唯一的實質差異在於，此檢視表會省略透過授與 `PUBLIC` 而讓目前使用者可存取的物件。由於 PostgreSQL 中的資料型別沒有真正的權限，只有對 `PUBLIC` 的隱含授與，因此此檢視表是空的。

<a id="id-1.7.6.42.3"></a>

**表 35.36. `role_udt_grants` 欄位**

<table border="1" class="table" summary="role_udt_grants 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該型別的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該型別的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       型別名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privilege_type</code> <code class="type">character_data</code>
</p>
<p>
       一律為 <code class="literal">TYPE USAGE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
若該權限可再授與他人，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-role-udt-grants.html)（原文版本：18.6；核對日期：2026-10-18）
