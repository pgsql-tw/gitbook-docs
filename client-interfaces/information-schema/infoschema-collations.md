<a id="INFOSCHEMA-COLLATIONS"></a>
## 35.10. `collations` [#](#infoschema-collations) <a href="#infoschema-collations" id="infoschema-collations"></a>

檢視表 `collations` 包含目前資料庫中可用的定序。

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
       包含該定序的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該定序的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collation_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       預設定序的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pad_attribute</code> <code class="type">character_data</code>
</p>
<p>
       一律為 <code class="literal">NO PAD</code>（PostgreSQL 不支援另一個值 <code class="literal">PAD
       SPACE</code>。）
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-collations.html)（原文版本：18.6；核對日期：2026-10-18）
