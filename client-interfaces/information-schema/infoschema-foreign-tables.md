<a id="INFOSCHEMA-FOREIGN-TABLES"></a>
## 35.31. `foreign_tables` [#](#INFOSCHEMA-FOREIGN-TABLES)

檢視表 `foreign_tables` 包含目前資料庫中定義的所有外部資料表。只有目前使用者可存取（身為擁有者或具有某種權限）的外部資料表才會顯示。

<a id="id-1.7.6.35.3"></a>

**表 35.29. `foreign_tables` 欄位**

<table border="1" class="table" summary="foreign_tables 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_table_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該外部資料表的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_table_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該外部資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_table_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       定義該外部伺服器的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">foreign_server_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       外部伺服器名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-foreign-tables.html)（原文版本：18.6；核對日期：2026-10-18）
