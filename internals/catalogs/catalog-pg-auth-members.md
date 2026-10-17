<a id="CATALOG-PG-AUTH-MEMBERS"></a>

## 52.9. `pg_auth_members` [#](#CATALOG-PG-AUTH-MEMBERS)

<a id="id-1.10.4.11.2"></a>

系統目錄 `pg_auth_members` 呈現角色之間的成員關係。
任何不形成循環的關係集合都是允許的。

由於使用者身分是整個叢集通用的，
`pg_auth_members`
由叢集中的所有資料庫共用：每個叢集只有一份
`pg_auth_members`，而不是每個資料庫各一份。

<a id="id-1.10.4.11.5"></a>

**表 52.9. `pg_auth_members` 欄位**

<table border="1" class="table" summary="表 52.9. pg_auth_members 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       資料列識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">roleid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       擁有成員之角色的 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">member</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       身為 <code class="structfield">roleid</code> 成員之角色的 ID
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantor</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       授予此成員資格之角色的 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">admin_option</code> <code class="type">bool</code>
</p>
<p>
       若 <code class="structfield">member</code> 可以將
       <code class="structfield">roleid</code> 的成員資格授予他人，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inherit_option</code> <code class="type">bool</code>
</p>
<p>
       若該成員自動繼承所授予角色的權限，則為 true
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">set_option</code> <code class="type">bool</code>
</p>
<p>
       若該成員可以
       <a class="link" href="../../reference/sql-commands/sql-set-role.md"><code class="command">SET ROLE</code></a>
       為所授予的角色，則為 true
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-auth-members.html)（原文版本：18.6；核對日期：2026-10-17）
