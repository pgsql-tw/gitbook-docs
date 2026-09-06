## 35.10. `collations` [#](#INFOSCHEMA-COLLATIONS)

檢視表 `collations` 包含目前資料庫中可用的排序規則。

<a id="id-1.7.6.14.3"></a>

**表 35.8. `collations` 欄位**

<table border="1" class="table" summary="collations 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含此排序規則的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含此排序規則的 schema 名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       預設排序規則的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pad_attribute</code> <code class="type">character_data</code>
</p>
<p>
       一律為 <code class="literal">NO PAD</code>（PostgreSQL 不支援替代值 <code class="literal">PAD
       SPACE</code>。）
      </p></td></tr></tbody></table>

<br>

---

【[PostgreSQL 18.6 文件](https://www.postgresql.org/docs/18/infoschema-collations.html)】
