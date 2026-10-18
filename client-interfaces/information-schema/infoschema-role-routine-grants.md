<a id="INFOSCHEMA-ROLE-ROUTINE-GRANTS"></a>
## 35.36. `role_routine_grants` [#](#INFOSCHEMA-ROLE-ROUTINE-GRANTS)

檢視表 `role_routine_grants` 列出在函式上授與、且授與者或受授與者為目前已啟用角色的所有權限。更多資訊可在 `routine_privileges` 中找到。此檢視表與 `routine_privileges` 唯一的實質差異在於，此檢視表會省略透過授與 `PUBLIC` 而讓目前使用者可存取的函式。

<a id="id-1.7.6.40.3"></a>

**表 35.34. `role_routine_grants` 欄位**

<table border="1" class="table" summary="role_routine_grants 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該函式的<span class="quote">“<span class="quote">特定名稱</span>”</span>。詳細資訊請參閱<a class="xref" href="infoschema-routines.md">第 35.45 節</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">routine_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       函式名稱（多載時可能重複）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privilege_type</code> <code class="type">character_data</code>
</p>
<p>
       一律為 <code class="literal">EXECUTE</code>（函式唯一的權限類型）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
若該權限可再授與他人，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-role-routine-grants.html)（原文版本：18.6；核對日期：2026-10-18）
