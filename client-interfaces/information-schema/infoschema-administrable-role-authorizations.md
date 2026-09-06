## 35.4. `administrable_role_authorizations` [#](#INFOSCHEMA-ADMINISTRABLE-ROLE-AUTHORIZATIONS)

檢視表 `administrable_role_authorizations` 列出目前使用者具有管理選項的所有角色。

<a id="id-1.7.6.8.3"></a>

**表 35.2. `administrable_role_authorizations` 欄位**

<table border="1" class="table" summary="administrable_role_authorizations 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
       一律為 <code class="literal">YES</code>
</p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-administrable-role-authorizations.html)】
