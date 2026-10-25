<a id="INFOSCHEMA-DOMAIN-CONSTRAINTS"></a>
## 35.21. `domain_constraints` [#](#infoschema-domain-constraints) <a href="#infoschema-domain-constraints" id="infoschema-domain-constraints"></a>

檢視表 `domain_constraints` 包含屬於目前資料庫中所定義之網域的所有限制條件。只會顯示目前使用者有權存取（身為擁有者或具有某種權限）的網域。

<a id="id-1.7.6.25.3"></a>

**表 35.19. `domain_constraints` 欄位**

<table border="1" class="table" summary="domain_constraints 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">domain_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該網域的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該網域的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">domain_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       網域名稱
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
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-domain-constraints.html)（原文版本：18.6；核對日期：2026-10-18）
