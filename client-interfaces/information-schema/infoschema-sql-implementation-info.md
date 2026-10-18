<a id="INFOSCHEMA-SQL-IMPLEMENTATION-INFO"></a>
## 35.49. `sql_implementation_info` [#](#INFOSCHEMA-SQL-IMPLEMENTATION-INFO)

資料表 `sql_implementation_info` 包含 SQL 標準留給實作自行定義的各個方面的
資訊。此資訊主要供 ODBC 介面使用；其他介面的使用者可能會覺得此資訊用處不大。
因此，這裡不說明個別的實作資訊項目；你可以在 ODBC 介面的說明中找到它們。

<a id="id-1.7.6.53.3"></a>

**表 35.47. `sql_implementation_info` 欄位**

<table border="1" class="table" summary="sql_implementation_info 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">implementation_info_id</code> <code class="type">character_data</code>
</p>
<p>
       實作資訊項目的識別字串
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">implementation_info_name</code> <code class="type">character_data</code>
</p>
<p>
       實作資訊項目的描述性名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">integer_value</code> <code class="type">cardinal_number</code>
</p>
<p>
       實作資訊項目的值；若值存放在欄位
       <code class="literal">character_value</code> 中，則為 null
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_value</code> <code class="type">character_data</code>
</p>
<p>
       實作資訊項目的值；若值存放在欄位
       <code class="literal">integer_value</code> 中，則為 null
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">comments</code> <code class="type">character_data</code>
</p>
<p>
       可能與此實作資訊項目相關的註解
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-sql-implementation-info.html)（原文版本：18.6；核對日期：2026-10-18）
