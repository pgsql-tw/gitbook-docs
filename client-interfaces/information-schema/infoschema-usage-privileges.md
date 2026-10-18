<a id="INFOSCHEMA-USAGE-PRIVILEGES"></a>
## 35.59. `usage_privileges` [#](#INFOSCHEMA-USAGE-PRIVILEGES)

檢視表 `usage_privileges` 列出在各類物件上授與目前已啟用的角色、
或由目前已啟用的角色授與的 `USAGE` 權限。在 PostgreSQL 中，目前適用於
定序、網域、外部資料包裝器、外部伺服器與序列。每個物件、授與者與受授與者的
組合各有一列。

由於定序在 PostgreSQL 中並沒有真正的權限，此檢視表會針對所有定序，
顯示由擁有者授與 `PUBLIC`、不可再授與他人的隱含 `USAGE` 權限。
不過，其他物件型別顯示的是真正的權限。

在 PostgreSQL 中，序列除了 `USAGE` 權限之外，也支援 `SELECT`
與 `UPDATE` 權限。這些權限不屬於標準，因此不會出現在資訊綱要中。

<a id="id-1.7.6.63.5"></a>

**表 35.57. `usage_privileges` 欄位**

<table border="1" class="table" summary="usage_privileges 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">object_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含物件的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含物件的綱要名稱（若適用）；否則為空字串
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
若此權限可再授與他人，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-usage-privileges.html)（原文版本：18.6；核對日期：2026-10-18）
