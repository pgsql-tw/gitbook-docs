<a id="VIEW-PG-STATS-EXT"></a>

## 53.30. `pg_stats_ext` [#](#view-pg-stats-ext) <a href="#view-pg-stats-ext" id="view-pg-stats-ext"></a>

<a id="id-1.10.5.34.2"></a>

檢視表 `pg_stats_ext` 提供對資料庫中每個擴充統計資訊物件之資訊的存取，結合了儲存在 [`pg_statistic_ext`](../catalogs/catalog-pg-statistic-ext.md) 與 [`pg_statistic_ext_data`](../catalogs/catalog-pg-statistic-ext-data.md) 系統目錄中的資訊。此檢視表只允許存取 [`pg_statistic_ext`](../catalogs/catalog-pg-statistic-ext.md) 與 [`pg_statistic_ext_data`](../catalogs/catalog-pg-statistic-ext-data.md) 中對應於使用者所擁有之資料表的資料列，因此允許公開讀取此檢視表是安全的。

`pg_stats_ext` 也被設計為以比底層系統目錄更易讀的格式呈現資訊——代價是每當有新的擴充統計資訊類型加入 [`pg_statistic_ext`](../catalogs/catalog-pg-statistic-ext.md) 時，就必須擴充此檢視表的結構。

<a id="id-1.10.5.34.5"></a>

**表 53.30. `pg_stats_ext` 欄位**

<table border="1" class="table" summary="表 53.30. pg_stats_ext 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含資料表之綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       資料表名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">statistics_schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含擴充統計資訊物件之綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">statistics_name</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-statistic-ext.md"><code class="structname">pg_statistic_ext</code></a>.<code class="structfield">stxname</code>）
      </p>
<p>
       擴充統計資訊物件的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">statistics_owner</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">rolname</code>）
      </p>
<p>
       擴充統計資訊物件的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">attnames</code> <code class="type">name[]</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attname</code>）
      </p>
<p>
       擴充統計資訊物件所包含之欄位的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">exprs</code> <code class="type">text[]</code>
</p>
<p>
       擴充統計資訊物件所包含的運算式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">kinds</code> <code class="type">char[]</code>
</p>
<p>
       此筆記錄所啟用的擴充統計資訊物件類型
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inherited</code> <code class="type">bool</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-statistic-ext-data.md"><code class="structname">pg_statistic_ext_data</code></a>.<code class="structfield">stxdinherit</code>）
      </p>
<p>
       若為 true，統計資訊包含來自子資料表的值，而不只是指定關聯中的值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_distinct</code> <code class="type">pg_ndistinct</code>
</p>
<p>
       欄位值組合的相異值個數（N-distinct）。若大於零，表示該組合中相異值的估計數量。若小於零，則為相異值數量除以資料列數量所得之值的負數。（當 <code class="command">ANALYZE</code> 認為相異值的數量可能會隨著資料表成長而增加時，使用負值形式；當欄位看起來只有固定數量的可能值時，使用正值形式。）例如，-1 表示一個唯一的欄位組合，其相異組合的數量與資料列數量相同。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dependencies</code> <code class="type">pg_dependencies</code>
</p>
<p>
       函數相依性統計資訊
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_vals</code> <code class="type">text[]</code>
</p>
<p>
       這些欄位中最常見之值組合的清單。（若沒有任何組合看起來比其他組合更常見，則為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_val_nulls</code> <code class="type">bool[]</code>
</p>
<p>
       最常見之值組合的 NULL 旗標清單。（當 <code class="structfield">most_common_vals</code> 為 null 時，此欄位也為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_freqs</code> <code class="type">float8[]</code>
</p>
<p>
       最常見之組合的頻率清單，亦即每個組合的出現次數除以資料列總數。（當 <code class="structfield">most_common_vals</code> 為 null 時，此欄位也為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_base_freqs</code> <code class="type">float8[]</code>
</p>
<p>
       最常見之組合的基礎頻率清單，亦即各值頻率的乘積。（當 <code class="structfield">most_common_vals</code> 為 null 時，此欄位也為 null。）
      </p></td></tr></tbody></table>

<br>

陣列欄位中的項目數上限，可以使用 [`ALTER
TABLE SET STATISTICS`](../../reference/sql-commands/sql-altertable.md) 命令逐欄控制，或透過設定 [default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET) 執行期參數進行全域控制。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-stats-ext.html)（原文版本：18.6；核對日期：2026-10-10）
