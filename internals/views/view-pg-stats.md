<a id="VIEW-PG-STATS"></a>

## 53.29. `pg_stats` [#](#VIEW-PG-STATS)

<a id="id-1.10.5.33.2"></a>

檢視表 `pg_stats` 提供對儲存在 [`pg_statistic`](../catalogs/catalog-pg-statistic.md) 系統目錄中之資訊的存取。此檢視表只允許存取 [`pg_statistic`](../catalogs/catalog-pg-statistic.md) 中對應於使用者有權讀取之資料表的資料列，因此允許公開讀取此檢視表是安全的。

`pg_stats` 也被設計為以比底層系統目錄更易讀的格式呈現資訊——代價是每當為 [`pg_statistic`](../catalogs/catalog-pg-statistic.md) 定義新的槽位（slot）類型時，就必須擴充此檢視表的結構。

<a id="id-1.10.5.33.5"></a>

**表 53.29. `pg_stats` 欄位**

<table border="1" class="table" summary="表 53.29. pg_stats 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">attname</code> <code class="type">name</code>
       （參照 <a class="link" href="../catalogs/catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attname</code>）
      </p>
<p>
       此資料列所描述之欄位的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">inherited</code> <code class="type">bool</code>
</p>
<p>
       若為 true，此資料列包含來自子資料表的值，而不只是指定資料表中的值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">null_frac</code> <code class="type">float4</code>
</p>
<p>
       欄位項目中為 null 的比例
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">avg_width</code> <code class="type">int4</code>
</p>
<p>
       欄位項目的平均寬度（以位元組為單位）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_distinct</code> <code class="type">float4</code>
</p>
<p>
       若大於零，表示欄位中相異值的估計數量。若小於零，則為相異值數量除以資料列數量所得之值的負數。（當 <code class="command">ANALYZE</code> 認為相異值的數量可能會隨著資料表成長而增加時，使用負值形式；當欄位看起來只有固定數量的可能值時，使用正值形式。）例如，-1 表示一個唯一的欄位，其相異值數量與資料列數量相同。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_vals</code> <code class="type">anyarray</code>
</p>
<p>
       欄位中最常見之值的清單。（若沒有任何值看起來比其他值更常見，則為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_freqs</code> <code class="type">float4[]</code>
</p>
<p>
       最常見之值的頻率清單，亦即每個值的出現次數除以資料列總數。（當 <code class="structfield">most_common_vals</code> 為 null 時，此欄位也為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">histogram_bounds</code> <code class="type">anyarray</code>
</p>
<p>
       將欄位的值劃分為數量大約相等之各組的值清單。若有 <code class="structfield">most_common_vals</code>，其中的值不納入此直方圖的計算。（若該欄位的資料型別沒有 <code class="literal">&lt;</code> 運算子，或 <code class="structfield">most_common_vals</code> 清單已涵蓋全部母體，則此欄位為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">correlation</code> <code class="type">float4</code>
</p>
<p>
       資料列的實體排列順序與欄位值的邏輯順序之間的統計相關性。其範圍從 -1 到 +1。當此值接近 -1 或 +1 時，由於減少了對磁碟的隨機存取，該欄位上的索引掃描會被估計為比此值接近零時更便宜。（若該欄位的資料型別沒有 <code class="literal">&lt;</code> 運算子，則此欄位為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_elems</code> <code class="type">anyarray</code>
</p>
<p>
       在欄位的值之中最常出現的非 null 元素值清單。（純量型別則為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">most_common_elem_freqs</code> <code class="type">float4[]</code>
</p>
<p>
       最常見之元素值的頻率清單，亦即包含至少一個該值實例之資料列的比例。在各元素的頻率之後，還會接著兩個或三個額外的值；它們是前述各元素頻率的最小值與最大值，以及可選的 null 元素頻率。（當 <code class="structfield">most_common_elems</code> 為 null 時，此欄位也為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">elem_count_histogram</code> <code class="type">float4[]</code>
</p>
<p>
       欄位的各個值之中相異非 null 元素值個數的直方圖，其後接著相異非 null 元素的平均個數。（純量型別則為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">range_length_histogram</code> <code class="type">anyarray</code>
</p>
<p>
       範圍型別欄位中非空且非 null 之範圍值長度的直方圖。（非範圍型別則為 null。）
      </p>
<p>
       無論範圍的邊界是否包含端點，此直方圖都是使用 <code class="function">subtype_diff</code> 範圍函式計算的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">range_empty_frac</code> <code class="type">float4</code>
</p>
<p>
       欄位項目中值為空範圍的比例。（非範圍型別則為 null。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">range_bounds_histogram</code> <code class="type">anyarray</code>
</p>
<p>
       非空且非 null 之範圍值的下界與上界的直方圖。（非範圍型別則為 null。）
      </p>
<p>
       這兩個直方圖以單一的範圍陣列表示，其中各範圍的下界代表下界的直方圖，上界則代表上界的直方圖。
      </p></td></tr></tbody></table>

<br>

陣列欄位中的項目數上限，可以使用 [`ALTER
TABLE SET STATISTICS`](../../reference/sql-commands/sql-altertable.md) 命令逐欄控制，或透過設定 [default_statistics_target](../../server-administration/runtime-config/runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET) 執行期參數進行全域控制。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-stats.html)（原文版本：18.6；核對日期：2026-10-10）
