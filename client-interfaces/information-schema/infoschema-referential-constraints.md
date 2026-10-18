<a id="INFOSCHEMA-REFERENTIAL-CONSTRAINTS"></a>
## 35.34. `referential_constraints` [#](#INFOSCHEMA-REFERENTIAL-CONSTRAINTS)

檢視表 `referential_constraints` 包含目前資料庫中所有的參照（外鍵）限制條件。只有目前使用者對參照端資料表具有寫入權限（身為擁有者，或具有 `SELECT` 以外的某種權限）的限制條件才會顯示。

<a id="id-1.7.6.38.3"></a>

**表 35.32. `referential_constraints` 欄位**

<table border="1" class="table" summary="referential_constraints 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">unique_constraint_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該外鍵限制條件所參照之唯一限制條件或主鍵限制條件的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">unique_constraint_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該外鍵限制條件所參照之唯一限制條件或主鍵限制條件的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">unique_constraint_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該外鍵限制條件所參照之唯一限制條件或主鍵限制條件的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">match_option</code> <code class="type">character_data</code>
</p>
<p>
       外鍵限制條件的比對選項：<code class="literal">FULL</code>、<code class="literal">PARTIAL</code> 或 <code class="literal">NONE</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">update_rule</code> <code class="type">character_data</code>
</p>
<p>
       外鍵限制條件的更新規則：<code class="literal">CASCADE</code>、<code class="literal">SET NULL</code>、<code class="literal">SET DEFAULT</code>、<code class="literal">RESTRICT</code> 或 <code class="literal">NO ACTION</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">delete_rule</code> <code class="type">character_data</code>
</p>
<p>
       外鍵限制條件的刪除規則：<code class="literal">CASCADE</code>、<code class="literal">SET NULL</code>、<code class="literal">SET DEFAULT</code>、<code class="literal">RESTRICT</code> 或 <code class="literal">NO ACTION</code>。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-referential-constraints.html)（原文版本：18.6；核對日期：2026-10-18）
