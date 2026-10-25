<a id="INFOSCHEMA-TABLE-CONSTRAINTS"></a>
## 35.52. `table_constraints` [#](#infoschema-table-constraints) <a href="#infoschema-table-constraints" id="infoschema-table-constraints"></a>

檢視表 `table_constraints` 包含屬於下列資料表的所有限制條件：目前使用者
擁有，或具有 `SELECT` 以外某種權限的資料表。

<a id="id-1.7.6.56.3"></a>

**表 35.50. `table_constraints` 欄位**

<table border="1" class="table" summary="table_constraints 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">constraint_type</code> <code class="type">character_data</code>
</p>
<p>
       限制條件的種類：<code class="literal">CHECK</code>（包含非空值限制條件）、
       <code class="literal">FOREIGN KEY</code>、<code class="literal">PRIMARY KEY</code>
       或 <code class="literal">UNIQUE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_deferrable</code> <code class="type">yes_or_no</code>
</p>
<p>
若此限制條件可延遲，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">initially_deferred</code> <code class="type">yes_or_no</code>
</p>
<p>
若此限制條件可延遲且初始即為延遲，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">enforced</code> <code class="type">yes_or_no</code>
</p>
<p>
若此限制條件會強制執行，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">nulls_distinct</code> <code class="type">yes_or_no</code>
</p>
<p>
       若此限制條件為唯一性限制條件，則將 null 視為相異時為 <code class="literal">YES</code>，
       將 null 視為不相異時為 <code class="literal">NO</code>；其他種類的
       限制條件則為 null。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-table-constraints.html)（原文版本：18.6；核對日期：2026-10-18）
