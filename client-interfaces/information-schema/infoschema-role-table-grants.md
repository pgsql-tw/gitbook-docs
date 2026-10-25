<a id="INFOSCHEMA-ROLE-TABLE-GRANTS"></a>
## 35.37. `role_table_grants` [#](#infoschema-role-table-grants) <a href="#infoschema-role-table-grants" id="infoschema-role-table-grants"></a>

檢視表 `role_table_grants` 列出在資料表或檢視表上授與、且授與者或受授與者為目前已啟用角色的所有權限。更多資訊可在 `table_privileges` 中找到。此檢視表與 `table_privileges` 唯一的實質差異在於，此檢視表會省略透過授與 `PUBLIC` 而讓目前使用者可存取的資料表。

<a id="id-1.7.6.41.3"></a>

**表 35.35. `role_table_grants` 欄位**

<table border="1" class="table" summary="role_table_grants 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privilege_type</code> <code class="type">character_data</code>
</p>
<p>
       權限類型：<code class="literal">SELECT</code>、<code class="literal">INSERT</code>、<code class="literal">UPDATE</code>、<code class="literal">DELETE</code>、<code class="literal">TRUNCATE</code>、<code class="literal">REFERENCES</code> 或 <code class="literal">TRIGGER</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
若該權限可再授與他人，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">with_hierarchy</code> <code class="type">yes_or_no</code>
</p>
<p>
       在 SQL 標準中，<code class="literal">WITH HIERARCHY OPTION</code> 是一項獨立的（子）權限，允許對資料表繼承階層執行某些操作。在 PostgreSQL 中，這包含在 <code class="literal">SELECT</code> 權限之內，因此此欄位會顯示 <code class="literal">YES</code>（當該權限為 <code class="literal">SELECT</code> 時），否則顯示 <code class="literal">NO</code>。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-role-table-grants.html)（原文版本：18.6；核對日期：2026-10-18）
