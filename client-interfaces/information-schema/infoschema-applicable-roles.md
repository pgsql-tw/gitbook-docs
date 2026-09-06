## 35.5. `applicable_roles` [#](#INFOSCHEMA-APPLICABLE-ROLES)

檢視表 `applicable_roles` 列出目前使用者可使用其權限的所有角色。這表示從目前
使用者到所述角色之間存在某條角色授與鏈。目前使用者本身也是適用角色。適用角色
集合通常用於權限檢查。
<a id="id-1.7.6.9.2.2"></a>
<a id="id-1.7.6.9.2.3"></a>

<a id="id-1.7.6.9.3"></a>

**表 35.3. `applicable_roles` 欄位**

<table border="1" class="table" summary="applicable_roles 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantee</code> <code class="type">sql_identifier</code>
</p>
<p>
       被授與此角色成員資格的角色名稱（可以是目前使用者；若為巢狀角色成員資格，
       也可以是其他角色）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">role_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       角色名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
若受授與者具有此角色的管理選項，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-applicable-roles.html)】
