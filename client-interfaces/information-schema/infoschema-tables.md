<a id="INFOSCHEMA-TABLES"></a>
## 35.54. `tables` [#](#INFOSCHEMA-TABLES)

檢視表 `tables` 包含目前資料庫中定義的所有資料表與檢視表。只會顯示目前使用者
有權存取（身為擁有者或具有某種權限）的資料表與檢視表。

<a id="id-1.7.6.58.3"></a>

**表 35.52. `tables` 欄位**

<table border="1" class="table" summary="tables 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">table_type</code> <code class="type">character_data</code>
</p>
<p>
       資料表的種類：<code class="literal">BASE TABLE</code> 表示
       持久性基底資料表（一般的資料表種類）、
       <code class="literal">VIEW</code> 表示檢視表、<code class="literal">FOREIGN</code>
       表示外部資料表，或
       <code class="literal">LOCAL TEMPORARY</code> 表示暫時資料表
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">self_referencing_column_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reference_generation</code> <code class="type">character_data</code>
</p>
<p>
       適用於 <span class="productname">PostgreSQL</span> 中未提供的功能
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">user_defined_type_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       若此資料表為型別化資料表，則為包含其底層資料型別的資料庫名稱
       （一律為目前資料庫）；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">user_defined_type_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       若此資料表為型別化資料表，則為包含其底層資料型別的綱要名稱；
       否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">user_defined_type_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       若此資料表為型別化資料表，則為其底層資料型別的名稱；否則為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_insertable_into</code> <code class="type">yes_or_no</code>
</p>
<p>
若可對此資料表插入資料，則為 <code class="literal">YES</code>；
       否則為 <code class="literal">NO</code>（基底資料表一律可插入資料，
       檢視表則不一定。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_typed</code> <code class="type">yes_or_no</code>
</p>
<p>
若此資料表為型別化資料表，則為 <code class="literal">YES</code>；否則為 <code class="literal">NO</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">commit_action</code> <code class="type">character_data</code>
</p>
<p>
       尚未實作
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-tables.html)（原文版本：18.6；核對日期：2026-10-18）
