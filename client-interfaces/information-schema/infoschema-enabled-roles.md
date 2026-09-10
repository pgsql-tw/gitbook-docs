## 35.25. `enabled_roles` [#](#INFOSCHEMA-ENABLED-ROLES)

檢視表 `enabled_roles` 列出目前「已啟用的角色」。它會以遞迴方式將已啟用的角色
定義為目前使用者，以及所有透過自動繼承授與已啟用角色的角色。換言之，這些是
目前使用者直接或間接具有自動繼承成員資格的所有角色。
<a id="id-1.7.6.29.2.3"></a>
<a id="id-1.7.6.29.2.4"></a>

權限檢查使用的是「適用角色」集合，其範圍可能比已啟用角色集合更廣。因此通常
建議使用檢視表 `applicable_roles`，而非此檢視表；`applicable_roles` 檢視表的
詳細資訊請參閱[第 35.5 節](infoschema-applicable-roles.md)。

<a id="id-1.7.6.29.4"></a>

**表 35.23. `enabled_roles` 欄位**

<table border="1" class="table" summary="enabled_roles 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">role_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       角色名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-enabled-roles.html)（原文版本：18.6；核對日期：2026-09-10）
