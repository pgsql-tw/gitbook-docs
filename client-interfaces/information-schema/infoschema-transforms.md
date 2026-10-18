<a id="INFOSCHEMA-TRANSFORMS"></a>
## 35.55. `transforms` [#](#INFOSCHEMA-TRANSFORMS)

檢視表 `transforms` 包含目前資料庫中所定義之轉換的資訊。更精確地說，
轉換中所包含的每個函式（「from SQL」或「to SQL」函式）在此檢視表中各有一個資料列。

<a id="id-1.7.6.59.3"></a>

**表 35.53. `transforms` 欄位**

<table border="1" class="table" summary="transforms 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含此轉換所適用型別的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含此轉換所適用型別的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">udt_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       此轉換所適用的型別名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含該函式的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">specific_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       該函式的<span class="quote">“<span class="quote">特定名稱</span>”</span>（specific name）。詳細資訊請參閱<a class="xref" href="infoschema-routines.md">第 35.45 節</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">group_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       SQL 標準允許以<span class="quote">“<span class="quote">群組</span>”</span>定義轉換，
       並在執行時選擇群組。PostgreSQL 不支援這項功能；轉換改為依程序語言而定。
       作為折衷，此欄位包含該轉換所適用的程序語言。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">transform_type</code> <code class="type">character_data</code>
</p>
<p>
<code class="literal">FROM SQL</code> 或 <code class="literal">TO SQL</code>
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-transforms.html)（原文版本：18.6；核對日期：2026-10-18）
