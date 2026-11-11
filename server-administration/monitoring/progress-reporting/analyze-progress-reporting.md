# 27.4.1. ANALYZE 進度回報

<a id="ANALYZE-PROGRESS-REPORTING"></a>

## 27.4.1. ANALYZE 進度回報 [#](#analyze-progress-reporting) <a href="#analyze-progress-reporting" id="analyze-progress-reporting"></a>

<a id="id-1.6.14.9.3.2"></a>

每當 `ANALYZE` 正在執行時，
`pg_stat_progress_analyze` 檢視表中，
就會針對每個目前正在執行此命令的後端，各含有一列。
下方的表格，說明了會被回報的資訊，
並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-ANALYZE-VIEW"></a>

### 表 27.38. `pg_stat_progress_analyze` 檢視表 [#](#pg-stat-progress-analyze-view) <a href="#pg-stat-progress-analyze-view" id="pg-stat-progress-analyze-view"></a>

<table border="1" class="table" summary="pg_stat_progress_analyze View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       後端程序的 ID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       此後端所連線之資料庫的 OID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       此後端所連線之資料庫的名稱。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       正在被分析之資料表的 OID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       目前的處理階段。請參閱<a class="xref" href="#analyze-phases">表 27.39</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sample_blks_total</code> <code class="type">bigint</code>
</p>
<p>
       將被取樣的堆積區塊總數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sample_blks_scanned</code> <code class="type">bigint</code>
</p>
<p>
       已掃描的堆積區塊數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ext_stats_total</code> <code class="type">bigint</code>
</p>
<p>
       延伸統計資訊的數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">ext_stats_computed</code> <code class="type">bigint</code>
</p>
<p>
       已計算完成的延伸統計資訊數量。此計數器只會在
       階段為 <code class="literal">computing extended statistics</code>
       時才會前進。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">child_tables_total</code> <code class="type">bigint</code>
</p>
<p>
       子資料表的數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">child_tables_done</code> <code class="type">bigint</code>
</p>
<p>
       已掃描的子資料表數量。此計數器只會在
       階段為 <code class="literal">acquiring inherited sample rows</code>
       時才會前進。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">current_child_table_relid</code> <code class="type">oid</code>
</p>
<p>
       目前正在被掃描之子資料表的 OID。只有在
       階段為
       <code class="literal">acquiring inherited sample rows</code>
       時，此欄位才有效。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">delay_time</code> <code class="type">double precision</code>
</p>
<p>
       因基於成本的延遲（請參閱
       <a class="xref" href="../../runtime-config/runtime-config-vacuum.md#runtime-config-resource-vacuum-cost">19.10.2 節</a>）
       而耗費在休眠上的總時間，以毫秒為單位
       （若已啟用 <a class="xref" href="../../runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING">track_cost_delay_timing</a>，
       否則為零）。
      </p></td></tr></tbody></table>

<br><a id="ANALYZE-PHASES"></a>

### 表 27.39. ANALYZE 各階段 [#](#analyze-phases) <a href="#analyze-phases" id="analyze-phases"></a>

<table border="1" class="table" summary="ANALYZE Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>階段</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
       此命令正在準備開始掃描堆積。預期此階段
       耗時應非常短暫。
      </td></tr><tr><td><code class="literal">acquiring sample rows</code></td><td>
       此命令目前正在掃描
       <code class="structfield">relid</code> 所指定的資料表，
       以取得取樣資料列。
      </td></tr><tr><td><code class="literal">acquiring inherited sample rows</code></td><td>
       此命令目前正在掃描子資料表，
       以取得取樣資料列。欄位
       <code class="structfield">child_tables_total</code>、
       <code class="structfield">child_tables_done</code>，以及
       <code class="structfield">current_child_table_relid</code>，
       含有此階段的進度資訊。
      </td></tr><tr><td><code class="literal">computing statistics</code></td><td>
       此命令正在根據資料表掃描期間取得的取樣資料列，
       計算統計資訊。
      </td></tr><tr><td><code class="literal">computing extended statistics</code></td><td>
       此命令正在根據資料表掃描期間取得的取樣資料列，
       計算延伸統計資訊。
      </td></tr><tr><td><code class="literal">finalizing analyze</code></td><td>
       此命令正在更新 <code class="structname">pg_class</code>。
       此階段完成後，<code class="command">ANALYZE</code>
       就會結束。
      </td></tr></tbody></table>

<br>

### 注意

請注意，當你對某個分割資料表執行 `ANALYZE`，
且未加上 `ONLY` 關鍵字時，
其所有的分割區也都會被遞迴分析。在此情況下，
`ANALYZE` 進度會先針對父資料表回報
（此時會蒐集其繼承統計資訊），
接著才是各個分割區的進度。

[返回 27.4. 進度回報](../progress-reporting.md#progress-reporting)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/progress-reporting.html)（原文版本：18.6；核對日期：2026-09-26）
