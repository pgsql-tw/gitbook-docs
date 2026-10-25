<a id="INFOSCHEMA-COLUMN-UDT-USAGE"></a>
## 35.16. `column_udt_usage` [#](#infoschema-column-udt-usage) <a href="#infoschema-column-udt-usage" id="infoschema-column-udt-usage"></a>

檢視表 `column_udt_usage` 列出所有使用了由目前已啟用角色所擁有之資料型別的欄位。請注意，在 PostgreSQL 中，內建資料型別的行為與使用者定義型別相同，因此它們也會包含在這裡。詳細資訊另請參閱[第 35.17 節](infoschema-columns.md)。

<a id="id-1.7.6.20.3"></a>

**表 35.14. `column_udt_usage` 欄位**

<table border="1" class="table" summary="column_udt_usage 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該欄位資料型別（若適用，則為網域的底層型別）的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該欄位資料型別（若適用，則為網域的底層型別）的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       欄位資料型別（若適用，則為網域的底層型別）的名稱
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
<code class="structfield">column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       欄位名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-column-udt-usage.html)（原文版本：18.6；核對日期：2026-10-18）
