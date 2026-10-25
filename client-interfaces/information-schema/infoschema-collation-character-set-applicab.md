<a id="INFOSCHEMA-COLLATION-CHARACTER-SET-APPLICAB"></a>
## 35.11. `collation_character_set_​applicability` [#](#infoschema-collation-character-set-applicab) <a href="#infoschema-collation-character-set-applicab" id="infoschema-collation-character-set-applicab"></a>

檢視表 `collation_character_set_applicability` 指出可用的定序分別適用於哪一個字元集。在 PostgreSQL 中，每個資料庫只有一個字元集（請參閱[第 35.7 節](infoschema-character-sets.md)中的說明），因此這個檢視表提供的有用資訊不多。

<a id="id-1.7.6.15.3"></a>

**表 35.9. `collation_character_set_applicability` 欄位**

<table border="1" class="table" summary="collation_character_set_applicability 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">character_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       字元集目前並未實作為綱要物件，因此此欄位為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       字元集目前並未實作為綱要物件，因此此欄位為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       字元集名稱
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-collation-character-set-applicab.html)（原文版本：18.6；核對日期：2026-10-18）
