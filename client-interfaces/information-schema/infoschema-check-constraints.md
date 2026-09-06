## 35.9. `check_constraints` [#](#INFOSCHEMA-CHECK-CONSTRAINTS)

檢視表 `check_constraints` 包含目前已啟用角色所擁有、定義於資料表或 domain
上的所有檢查約束。（資料表或 domain 的擁有者即為約束的擁有者。）

SQL 標準將非空值約束視為具有 `CHECK (column_name IS NOT
NULL)` 表示式的檢查約束。因此非空值約束也包含在此處，沒有專屬的檢視表。

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
       包含約束的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含約束的 schema 名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       約束名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">check_clause</code> <code class="type">character_data</code>
</p>
<p>
       檢查約束的檢查表示式
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-check-constraints.html)】
