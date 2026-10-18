<a id="INFOSCHEMA-CONSTRAINT-COLUMN-USAGE"></a>
## 35.18. `constraint_column_usage` [#](#INFOSCHEMA-CONSTRAINT-COLUMN-USAGE)

檢視表 `constraint_column_usage` 列出目前資料庫中被某個限制條件使用的所有欄位。只會顯示包含在目前已啟用角色所擁有之資料表中的欄位。對於檢查限制條件，此檢視表列出檢查運算式中所使用的欄位。對於非空值限制條件，此檢視表列出該限制條件所定義的欄位。對於外鍵限制條件，此檢視表列出該外鍵所參照的欄位。對於唯一限制條件或主鍵限制條件，此檢視表列出該限制條件所限制的欄位。

<a id="id-1.7.6.22.3"></a>

**表 35.16. `constraint_column_usage` 欄位**

<table border="1" class="table" summary="constraint_column_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含「被某個限制條件使用之欄位」所屬資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含「被某個限制條件使用之欄位」所屬資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含被某個限制條件使用之欄位的資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       被某個限制條件使用的欄位名稱
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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-constraint-column-usage.html)（原文版本：18.6；核對日期：2026-10-18）
