<a id="INFOSCHEMA-SQL-FEATURES"></a>
## 35.48. `sql_features` [#](#infoschema-sql-features) <a href="#infoschema-sql-features" id="infoschema-sql-features"></a>

資料表 `sql_features` 包含 PostgreSQL 支援 SQL 標準中所定義之哪些正式功能的
資訊。這與[附錄 D](../../appendixes/features/README.md)中呈現的資訊相同，
你也可以在該處找到一些額外的背景資訊。

<a id="id-1.7.6.52.3"></a>

**表 35.46. `sql_features` 欄位**

<table border="1" class="table" summary="sql_features 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">feature_id</code> <code class="type">character_data</code>
</p>
<p>
       功能的識別字串
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">feature_name</code> <code class="type">character_data</code>
</p>
<p>
       功能的描述性名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sub_feature_id</code> <code class="type">character_data</code>
</p>
<p>
       子功能的識別字串；若不是子功能，則為長度為零的字串
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sub_feature_name</code> <code class="type">character_data</code>
</p>
<p>
       子功能的描述性名稱；若不是子功能，則為長度為零的字串
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_supported</code> <code class="type">yes_or_no</code>
</p>
<p>
若目前版本的 <span class="productname">PostgreSQL</span> 完全支援此功能，
       則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_verified_by</code> <code class="type">character_data</code>
</p>
<p>
       一律為 null，因為 <span class="productname">PostgreSQL</span> 開發團隊不會對功能符合性
       執行正式測試
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comments</code> <code class="type">character_data</code>
</p>
<p>
       可能與此功能支援狀態相關的註解
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-sql-features.html)（原文版本：18.6；核對日期：2026-10-18）
