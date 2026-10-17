<a id="CATALOG-PG-STATISTIC-EXT"></a>

## 52.52. `pg_statistic_ext` [#](#CATALOG-PG-STATISTIC-EXT)

<a id="id-1.10.4.54.2"></a>

系統目錄 `pg_statistic_ext` 存放擴充規劃器統計資訊的定義。此系統目錄中的每一筆資料列對應一個以 [`CREATE STATISTICS`](../../reference/sql-commands/sql-createstatistics.md) 建立的*統計資訊物件*。

<a id="id-1.10.4.54.4"></a>

**表 52.52. `pg_statistic_ext` 欄位**

<table border="1" class="table" summary="表 52.52. pg_statistic_ext 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">stxrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此物件所描述之欄位的資料表
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxname</code> <code class="type">name</code>
</p>
<p>
       統計資訊物件的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此統計資訊物件之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       統計資訊物件的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxkeys</code> <code class="type">int2vector</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       屬性編號的陣列，指出此統計資訊物件涵蓋哪些資料表欄位；例如值 <code class="literal">1 3</code> 表示涵蓋資料表的第一個與第三個欄位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxstattarget</code> <code class="type">int2</code>
</p>
<p>
<code class="structfield">stxstattarget</code> 控制 <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a> 為此統計資訊物件累積之統計資訊的詳細程度。值為零表示不應收集任何統計資訊。null 值表示使用所參照欄位之統計目標中的最大值（若有設定），否則使用系統預設統計目標。<code class="structfield">stxstattarget</code> 的正值決定要收集之<span class="quote">“<span class="quote">最常見值</span>”</span>的目標數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxkind</code> <code class="type">char[]</code>
</p>
<p>
       包含已啟用統計資訊種類代碼的陣列；有效值為：<code class="literal">d</code> 表示 n-distinct 統計資訊、<code class="literal">f</code> 表示函數相依統計資訊、<code class="literal">m</code> 表示最常見值（MCV）清單統計資訊，以及 <code class="literal">e</code> 表示運算式統計資訊
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxexprs</code> <code class="type">pg_node_tree</code>
</p>
<p>
       統計資訊物件中非簡單欄位參照之屬性的運算式樹（採 <code class="function">nodeToString()</code> 表示法）。這是一個清單，每個運算式對應一個元素。若統計資訊物件的所有屬性都是簡單參照，則為 null。
      </p></td></tr></tbody></table>

<br>

`pg_statistic_ext` 項目會在 [`CREATE STATISTICS`](../../reference/sql-commands/sql-createstatistics.md) 期間完整填入，但當時並不會計算實際的統計值。後續的 [`ANALYZE`](../../reference/sql-commands/sql-analyze.md) 命令會計算所需的值，並在 [`pg_statistic_ext_data`](catalog-pg-statistic-ext-data.md) 系統目錄中填入一筆項目。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-statistic-ext.html)（原文版本：18.6；核對日期：2026-10-17）
