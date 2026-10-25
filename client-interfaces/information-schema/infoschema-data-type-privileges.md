<a id="INFOSCHEMA-DATA-TYPE-PRIVILEGES"></a>
## 35.20. `data_type_privileges` [#](#infoschema-data-type-privileges) <a href="#infoschema-data-type-privileges" id="infoschema-data-type-privileges"></a>

檢視表 `data_type_privileges` 列出目前使用者有權存取（身為所描述物件的擁有者，或對該物件具有某種權限）的所有資料型別描述子。每當資料型別用於資料表欄位、網域或函式（作為參數或回傳型別）的定義中時，就會產生資料型別描述子，其中儲存該資料型別在該處如何使用的一些資訊（例如宣告的最大長度，若適用的話）。每個資料型別描述子都會被指派一個任意的識別碼，此識別碼在為同一個物件（資料表、網域、函式）所指派的資料型別描述子識別碼中是唯一的。此檢視表對應用程式而言大概沒有用處，但資訊綱要中的其他一些檢視表是以它來定義的。

<a id="id-1.7.6.24.3"></a>

**表 35.18. `data_type_privileges` 欄位**

<table border="1" class="table" summary="data_type_privileges 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含所描述物件的資料庫名稱（一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含所描述物件的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       所描述物件的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">object_type</code> <code class="type">character_data</code>
</p>
<p>
       所描述物件的類型，為下列之一：<code class="literal">TABLE</code>（該資料型別描述子屬於該資料表的某個欄位）、<code class="literal">DOMAIN</code>（該資料型別描述子屬於該網域）、<code class="literal">ROUTINE</code>（該資料型別描述子屬於該函式的某個參數或回傳資料型別）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dtd_identifier</code> <code class="type">sql_identifier</code>
</p>
<p>
       資料型別描述子的識別碼，在同一個物件的資料型別描述子中是唯一的。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-data-type-privileges.html)（原文版本：18.6；核對日期：2026-10-18）
