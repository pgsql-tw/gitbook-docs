<a id="VIEW-PG-STATS-EXT-EXPRS"></a>

## 53.31. `pg_stats_ext_exprs` [#](#VIEW-PG-STATS-EXT-EXPRS)

<a id="id-1.10.5.35.2"></a>

檢視表 `pg_stats_ext_exprs` 可用來存取擴充統計資訊物件中所包含之所有運算式的相關資訊，它結合了儲存在 [`pg_statistic_ext`](../catalogs/catalog-pg-statistic-ext.md) 與 [`pg_statistic_ext_data`](../catalogs/catalog-pg-statistic-ext-data.md) 系統目錄中的資訊。此檢視表只允許存取 [`pg_statistic_ext`](../catalogs/catalog-pg-statistic-ext.md) 與 [`pg_statistic_ext_data`](../catalogs/catalog-pg-statistic-ext-data.md) 中對應到使用者所擁有之資料表的資料列，因此允許大眾讀取此檢視表是安全的。

`pg_stats_ext_exprs` 也被設計成以比底層系統目錄更易讀的格式呈現資訊——代價是每當 `pg_statistic_ext` 中統計資訊的結構改變時，它的結構定義（schema）就必須跟著擴充。

<a id="id-1.10.5.35.5"></a>

**表 53.31. `pg_stats_ext_exprs` 欄位**

<table border="1" class="table" summary="表 53.31. pg_stats_ext_exprs 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含此資料表的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablename</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relname</code>）
      </p>
<p>
       定義此統計資訊物件之資料表的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">statistics_schemaname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">nspname</code>）
      </p>
<p>
       包含此擴充統計資訊物件的綱要名稱
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
<code class="structfield">expr</code> <code class="type">text</code>
</p>
<p>
       擴充統計資訊物件中所包含的運算式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inherited</code> <code class="type">bool</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-statistic-ext-data.md"><code class="structname">pg_statistic_ext_data</code></a>.<code class="structfield">stxdinherit</code>）
      </p>
<p>
       若為 true，則統計資訊包含來自子資料表的值，而不僅是指定關聯中的值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">null_frac</code> <code class="type">float4</code>
</p>
<p>
       運算式項目中為 null 的比例
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">avg_width</code> <code class="type">int4</code>
</p>
<p>
       運算式項目的平均寬度，以位元組為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_distinct</code> <code class="type">float4</code>
</p>
<p>
       若大於零，則為運算式中相異值的估計數量。若小於零，則為相異值數量除以資料列數量後的負值。（當 <code class="command">ANALYZE</code> 認為相異值的數量可能隨資料表成長而增加時，使用負值形式；當運算式看起來具有固定數量的可能值時，則使用正值形式。）例如，-1 表示唯一的運算式，其相異值數量與資料列數量相同。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_vals</code> <code class="type">anyarray</code>
</p>
<p>
       運算式中最常見值的清單。（若沒有任何值看起來比其他值更常見，則為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_freqs</code> <code class="type">float4[]</code>
</p>
<p>
       最常見值的頻率清單，也就是每個值的出現次數除以資料列總數。（當 <code class="structfield">most_common_vals</code> 為 null 時，此欄位也為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">histogram_bounds</code> <code class="type">anyarray</code>
</p>
<p>
       將運算式的值分成數量大約相等之各組的值清單。<code class="structfield">most_common_vals</code> 中的值（若有）不納入此直方圖計算。（若運算式的資料型別沒有 <code class="literal">&lt;</code> 運算子，或 <code class="structfield">most_common_vals</code> 清單已涵蓋整個母體，則此運算式為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">correlation</code> <code class="type">float4</code>
</p>
<p>
       實體資料列順序與運算式值之邏輯順序間的統計相關性。其範圍為 -1 到 +1。當此值接近 -1 或 +1 時，由於減少了對磁碟的隨機存取，針對該運算式的索引掃描會被估算為比此值接近零時更便宜。（若運算式的資料型別沒有 <code class="literal">&lt;</code> 運算子，則此運算式為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_elems</code> <code class="type">anyarray</code>
</p>
<p>
       在運算式的值中最常出現的非 null 元素值清單。（純量型別則為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_elem_freqs</code> <code class="type">float4[]</code>
</p>
<p>
       最常見元素值的頻率清單，也就是包含至少一個該值實例的資料列比例。在各元素頻率之後會接著兩個或三個額外的值；它們分別是前述各元素頻率的最小值與最大值，以及（視情況）null 元素的頻率。（當 <code class="structfield">most_common_elems</code> 為 null 時，此欄位也為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">elem_count_histogram</code> <code class="type">float4[]</code>
</p>
<p>
       運算式各值中相異非 null 元素值個數的直方圖，後面接著相異非 null 元素的平均個數。（純量型別則為 null。）
      </p></td></tr></tbody></table>

<br>

陣列欄位中的最大項目數，可以使用 [`ALTER
TABLE SET STATISTICS`](../../reference/sql-commands/sql-altertable.md) 命令逐欄控制，或透過設定 [default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET) 執行期參數進行全域控制。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-stats-ext-exprs.html)（原文版本：18.6；核對日期：2026-10-10）
