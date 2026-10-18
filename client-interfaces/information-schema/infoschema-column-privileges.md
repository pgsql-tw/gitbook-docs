<a id="INFOSCHEMA-COLUMN-PRIVILEGES"></a>
## 35.15. `column_privileges` [#](#INFOSCHEMA-COLUMN-PRIVILEGES)

檢視表 `column_privileges` 列出在欄位上授與目前已啟用角色、或由目前已啟用角色所授與的所有權限。每個欄位、授與者與受授與者的組合各有一個資料列。

若某項權限是在整個資料表上授與的，它在此檢視表中會顯示為對每個欄位的授權，但僅限於能以欄位為單位授與的權限種類：`SELECT`、`INSERT`、`UPDATE`、`REFERENCES`。

<a id="id-1.7.6.19.4"></a>

**表 35.13. `column_privileges` 欄位**

<table border="1" class="table" summary="column_privileges 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該欄位所屬資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該欄位所屬資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該欄位的資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       欄位名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privilege_type</code> <code class="type">character_data</code>
</p>
<p>
       權限的種類：<code class="literal">SELECT</code>、<code class="literal">INSERT</code>、<code class="literal">UPDATE</code> 或 <code class="literal">REFERENCES</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_grantable</code> <code class="type">yes_or_no</code>
</p>
<p>
若此權限可再授與他人，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-column-privileges.html)（原文版本：18.6；核對日期：2026-10-18）
