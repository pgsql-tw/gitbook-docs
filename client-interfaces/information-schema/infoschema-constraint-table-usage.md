<a id="INFOSCHEMA-CONSTRAINT-TABLE-USAGE"></a>
## 35.19. `constraint_table_usage` [#](#infoschema-constraint-table-usage) <a href="#infoschema-constraint-table-usage" id="infoschema-constraint-table-usage"></a>

檢視表 `constraint_table_usage` 列出目前資料庫中被某個限制條件使用、且由目前已啟用角色所擁有的所有資料表。（這與檢視表 `table_constraints` 不同，後者列出所有資料表限制條件及其所定義的資料表。）對於外鍵限制條件，此檢視表列出該外鍵所參照的資料表。對於唯一限制條件或主鍵限制條件，此檢視表只列出該限制條件所屬的資料表。檢查限制條件與非空值限制條件不包含在此檢視表中。

<a id="id-1.7.6.23.3"></a>

**表 35.17. `constraint_table_usage` 欄位**

<table border="1" class="table" summary="constraint_table_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含被某個限制條件使用之資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含被某個限制條件使用之資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       被某個限制條件使用的資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
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
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-constraint-table-usage.html)（原文版本：18.6；核對日期：2026-10-18）
