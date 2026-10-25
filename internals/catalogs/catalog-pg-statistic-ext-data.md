<a id="CATALOG-PG-STATISTIC-EXT-DATA"></a>

## 52.53. `pg_statistic_ext_data` [#](#catalog-pg-statistic-ext-data) <a href="#catalog-pg-statistic-ext-data" id="catalog-pg-statistic-ext-data"></a>

<a id="id-1.10.4.55.2"></a>

系統目錄 `pg_statistic_ext_data` 存放 [`pg_statistic_ext`](catalog-pg-statistic-ext.md) 中所定義之擴充規劃器統計資訊的資料。此系統目錄中的每一筆資料列對應一個以 [`CREATE STATISTICS`](../../reference/sql-commands/sql-createstatistics.md) 建立的*統計資訊物件*。

通常每個已分析過的統計資訊物件會有一筆 `stxdinherit` = `false` 的項目。若資料表有繼承子資料表或分割區，還會另外建立一筆 `stxdinherit` = `true` 的項目。這筆資料列代表涵蓋整個繼承樹的統計資訊物件，亦即你以 `SELECT * FROM table*` 會看到之資料的統計資訊；而 `stxdinherit` = `false` 的資料列則代表 `SELECT * FROM ONLY table` 的結果。

與 [`pg_statistic`](catalog-pg-statistic.md) 相同，`pg_statistic_ext_data` 不應開放給一般大眾讀取，因為其內容可能被視為敏感資訊。（例如：欄位中最常見的值組合可能相當值得關注。）[`pg_stats_ext`](../views/view-pg-stats-ext.md) 是建立在 `pg_statistic_ext_data` 之上（與 [`pg_statistic_ext`](catalog-pg-statistic-ext.md) 連接之後）、可公開讀取的檢視表，只會揭露目前使用者所擁有之資料表的資訊。

<a id="id-1.10.4.55.6"></a>

**表 52.53. `pg_statistic_ext_data` 欄位**

<table border="1" class="table" summary="表 52.53. pg_statistic_ext_data 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxoid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-statistic-ext.md"><code class="structname">pg_statistic_ext</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此資料之定義的擴充統計資訊物件
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxdinherit</code> <code class="type">bool</code>
</p>
<p>
       若為真，統計資訊包含子資料表中的值，而不只是指定關聯中的值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxdndistinct</code> <code class="type">pg_ndistinct</code>
</p>
<p>
       N-distinct 計數，序列化為 <code class="structname">pg_ndistinct</code> 型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxddependencies</code> <code class="type">pg_dependencies</code>
</p>
<p>
       函數相依統計資訊，序列化為 <code class="structname">pg_dependencies</code> 型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxdmcv</code> <code class="type">pg_mcv_list</code>
</p>
<p>
       MCV（最常見值）清單統計資訊，序列化為 <code class="structname">pg_mcv_list</code> 型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stxdexpr</code> <code class="type">pg_statistic[]</code>
</p>
<p>
       逐運算式的統計資訊，序列化為 <code class="structname">pg_statistic</code> 型別的陣列
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-statistic-ext-data.html)（原文版本：18.6；核對日期：2026-10-17）
