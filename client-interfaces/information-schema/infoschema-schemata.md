<a id="INFOSCHEMA-SCHEMATA"></a>
## 35.46. `schemata` [#](#INFOSCHEMA-SCHEMATA)

檢視表 `schemata` 包含目前資料庫中目前使用者可存取的所有綱要（使用者為其擁有者或具有某項權限時即可存取）。

<a id="id-1.7.6.50.3"></a>

**表 35.44. `schemata` 欄位**

<table border="1" class="table" summary="schemata 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">catalog_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該綱要的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schema_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schema_owner</code> <code class="type">sql_identifier</code>
</p>
<p>
       綱要擁有者的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_character_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_character_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_character_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sql_path</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-schemata.html)（原文版本：18.6；核對日期：2026-10-18）
