<a id="INFOSCHEMA-UDT-PRIVILEGES"></a>
## 35.58. `udt_privileges` [#](#infoschema-udt-privileges) <a href="#infoschema-udt-privileges" id="infoschema-udt-privileges"></a>

檢視表 `udt_privileges` 列出在使用者自訂型別上授與目前已啟用的角色、
或由目前已啟用的角色授與的 `USAGE` 權限。每個型別、授與者與受授與者的組合
各有一列。此檢視表只顯示複合型別（原因請參閱[第 35.60 節](infoschema-user-defined-types.md)）；
網域的權限請參閱[第 35.59 節](infoschema-usage-privileges.md)。

<a id="id-1.7.6.62.3"></a>

**表 35.56. `udt_privileges` 欄位**

<table border="1" class="table" summary="udt_privileges 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantor</code> <code class="type">sql_identifier</code>
</p>
<p>
       授與此權限的角色名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">grantee</code> <code class="type">sql_identifier</code>
</p>
<p>
       被授與此權限的角色名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含型別的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含型別的綱要名稱
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
若此權限可再授與他人，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-udt-privileges.html)（原文版本：18.6；核對日期：2026-10-18）
