<a id="INFOSCHEMA-CHECK-CONSTRAINTS"></a>
## 35.9. `check_constraints` [#](#infoschema-check-constraints) <a href="#infoschema-check-constraints" id="infoschema-check-constraints"></a>

檢視表 `check_constraints` 包含由目前已啟用角色所擁有的所有檢查限制條件，無論是
定義在資料表上或網域上。（資料表或網域的擁有者即為限制條件的擁有者。）

SQL 標準將非空值限制條件視為具有 `CHECK (column_name IS NOT
NULL)` 表示式的檢查限制條件。因此，非空值限制條件也包含在這裡，而沒有獨立的檢視表。

<a id="id-1.7.6.13.4"></a>

**表 35.7. `check_constraints` 欄位**

<table border="1" class="table" summary="check_constraints 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該限制條件的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該限制條件的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       限制條件名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">check_clause</code> <code class="type">character_data</code>
</p>
<p>
       檢查限制條件的檢查表示式
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-check-constraints.html)（原文版本：18.6；核對日期：2026-10-18）
