<a id="CATALOG-PG-ENUM"></a>

## 52.20. `pg_enum` [#](#catalog-pg-enum) <a href="#catalog-pg-enum" id="catalog-pg-enum"></a>

<a id="id-1.10.4.22.2"></a>

`pg_enum` 系統目錄包含顯示每個列舉型別之值與標籤的項目。某個列舉值的內部表示法，實際上就是它在 `pg_enum` 中所對應資料列的 OID。

<a id="id-1.10.4.22.4"></a>

**表 52.20. `pg_enum` 欄位**

<table border="1" class="table" summary="表 52.20. pg_enum 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       資料列識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">enumtypid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       擁有此列舉值之 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a> 項目的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">enumsortorder</code> <code class="type">float4</code>
</p>
<p>
       此列舉值在其列舉型別中的排序位置
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">enumlabel</code> <code class="type">name</code>
</p>
<p>
       此列舉值的文字標籤
      </p></td></tr></tbody></table>

<br>

`pg_enum` 資料列的 OID 遵循一項特殊規則：偶數 OID 保證會依照其列舉型別的排序順序排列。也就是說，若兩個偶數 OID 屬於同一個列舉型別，則較小的 OID 必定具有較小的 `enumsortorder` 值。奇數 OID 值則不需要與排序順序有任何關聯。此規則讓列舉比較常式在許多常見情況下可以避免查詢系統目錄。建立與修改列舉型別的常式會盡可能嘗試為列舉值指派偶數 OID。

建立列舉型別時，其成員會被指派排序位置 1..*`n`*。但之後加入的成員可能會被給予負的或帶小數的 `enumsortorder` 值。對這些值唯一的要求，是它們在每個列舉型別內必須正確排序且不重複。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-enum.html)（原文版本：18.6；核對日期：2026-10-17）
