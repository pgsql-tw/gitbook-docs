# 27.2.2. 檢視統計資訊

<a id="MONITORING-STATS-VIEWS"></a>

## 27.2.2. 檢視統計資訊 [#](#monitoring-stats-views) <a href="#monitoring-stats-views" id="monitoring-stats-views"></a>

系統提供了幾個預先定義的檢視表，列於[表 27.1](#monitoring-stats-dynamic-views-table)中，可用來顯示系統目前的狀態。此外還有其他幾個檢視表，列於[表 27.2](#monitoring-stats-views-table)中，可用來顯示累計的統計資訊。另外，也可以使用底層的累計統計函式來建立自訂檢視表，詳見[第 27.2.26 節](../monitoring-stats.md#monitoring-stats-functions)中的討論。

在使用累計統計檢視表與函式來監控所收集的資料時，必須了解這些資訊並非即時更新。每個伺服器程序會在進入閒置狀態之前，將累積的統計資訊刷寫（flush）至共享記憶體，但頻率不會超過每 `PGSTAT_MIN_INTERVAL` 毫秒一次（除非在建置伺服器時另行變更，否則預設為 1 秒）；因此仍在進行中的查詢或交易並不會影響所顯示的總計值，所顯示的資訊會落後於實際活動。然而，由 `track_activities` 所收集的目前查詢資訊則始終是最新的。

另一個重要的地方是，當伺服器程序被要求顯示任何累計統計資訊時，在預設組態下，所存取的值會被快取，直到其目前交易結束為止。因此，只要目前交易持續進行，統計資訊就會顯示為靜態資訊。同樣地，關於所有工作階段目前查詢的資訊，會在某筆交易中首次要求此類資訊時被收集，並且在整個交易期間都會顯示相同的資訊。這是一項特性，而非臭蟲（bug），因為它讓你可以對統計資訊執行多次查詢並關聯其結果，而不必擔心數值會在底層發生變化。當以互動方式分析統計資訊，或使用成本高昂的查詢時，各次存取個別統計資訊之間的時間差，可能導致快取的統計資訊出現明顯的偏差。為了將偏差降至最低，可以將 `stats_fetch_consistency` 設為 `snapshot`，但代價是會增加用於快取非必要統計資料的記憶體用量。相反地，若已知統計資訊只會被存取一次，則快取所存取的統計資訊並無必要，可以將 `stats_fetch_consistency` 設為 `none` 以避免這種情況。你可以呼叫 `pg_stat_clear_snapshot()` 來捨棄目前交易的統計資訊快照或快取的值（如果有的話）。下一次使用統計資訊時，將會（在快照模式下）建立新的快照，或（在快取模式下）快取所存取的統計資訊。

交易也可以在 `pg_stat_xact_all_tables`、`pg_stat_xact_sys_tables`、`pg_stat_xact_user_tables` 以及 `pg_stat_xact_user_functions` 這些檢視表中，看到自己本身的統計資訊（尚未刷寫至共享記憶體統計資訊中的部分）。這些數值並不遵循上述行為；相反地，它們會在整個交易期間持續更新。

[表 27.1](#monitoring-stats-dynamic-views-table)中所示動態統計檢視表的部分資訊受到安全性限制。一般使用者只能看到有關自己工作階段（屬於他們身為成員之角色的工作階段）的所有資訊。在有關其他工作階段的資料列中，許多欄位將為 null。然而請注意，工作階段的存在及其一般屬性（例如其工作階段使用者與資料庫）對所有使用者都是可見的。超級使用者以及具備內建角色 [`pg_read_all_stats`](../../user-manag/predefined-roles.md#PREDEFINED-ROLE-PG-MONITOR) 權限的角色，則可以看到所有工作階段的所有資訊（此連結的目標錨點以 pg_monitor 命名，指向預先定義角色清單中 pg_monitor、pg_read_all_settings、pg_read_all_stats 與 pg_stat_scan_tables 四個角色的共同說明項目，pg_read_all_stats 的說明即在其中）。

<a id="MONITORING-STATS-DYNAMIC-VIEWS-TABLE"></a>

### 表 27.1. 動態統計檢視表 [#](#monitoring-stats-dynamic-views-table) <a href="#monitoring-stats-dynamic-views-table" id="monitoring-stats-dynamic-views-table"></a>

<table border="1" class="table" summary="動態統計檢視表"><colgroup><col/><col/></colgroup><thead><tr><th>檢視表名稱</th><th>說明</th></tr></thead><tbody><tr><td>
<code class="structname">pg_stat_activity</code>
<a class="indexterm" id="id-1.6.14.7.6.7.2.2.1.1.2"></a>
</td><td>
       每個伺服器程序一筆資料列，顯示與該程序目前活動相關的資訊，例如狀態與目前查詢。
       詳情請參閱<a class="link" href="../monitoring-stats.md#monitoring-pg-stat-activity-view">
<code class="structname">pg_stat_activity</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_replication</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.2.1.2"></a></td><td>每個 WAL 傳送程序一筆資料列，顯示有關該傳送程序所連線待命伺服器複寫情況的統計資訊。
       詳情請參閱<a class="link" href="../monitoring-stats.md#monitoring-pg-stat-replication-view">
<code class="structname">pg_stat_replication</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_wal_receiver</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.3.1.2"></a></td><td>僅有一筆資料列，顯示 WAL 接收程序從其所連線伺服器接收 WAL 的相關統計資訊。
       詳情請參閱<a class="link" href="monitoring-pg-stat-wal-receiver-view.md#monitoring-pg-stat-wal-receiver-view">
<code class="structname">pg_stat_wal_receiver</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_recovery_prefetch</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.4.1.2"></a></td><td>僅有一筆資料列，顯示有關復原期間預先擷取區塊的統計資訊。
       詳情請參閱<a class="link" href="monitoring-pg-stat-recovery-prefetch.md#monitoring-pg-stat-recovery-prefetch">
<code class="structname">pg_stat_recovery_prefetch</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_subscription</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.5.1.2"></a></td><td>每個訂閱至少一筆資料列，顯示有關訂閱工作程序的資訊。
       詳情請參閱<a class="link" href="monitoring-pg-stat-subscription.md#monitoring-pg-stat-subscription">
<code class="structname">pg_stat_subscription</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_ssl</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.6.1.2"></a></td><td>每個連線（一般連線與複寫連線）一筆資料列，顯示有關該連線所使用 SSL 的資訊。
       詳情請參閱<a class="link" href="monitoring-pg-stat-ssl-view.md#monitoring-pg-stat-ssl-view">
<code class="structname">pg_stat_ssl</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_gssapi</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.7.1.2"></a></td><td>每個連線（一般連線與複寫連線）一筆資料列，顯示有關該連線所使用 GSSAPI 驗證與加密的資訊。
       詳情請參閱<a class="link" href="monitoring-pg-stat-gssapi-view.md#monitoring-pg-stat-gssapi-view">
<code class="structname">pg_stat_gssapi</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_progress_analyze</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.8.1.2"></a></td><td>每個正在執行 <code class="command">ANALYZE</code> 的後端（包括 autovacuum 工作程序）各一筆資料列，顯示目前進度。
       請參閱<a class="xref" href="../progress-reporting/analyze-progress-reporting.md#analyze-progress-reporting">第 27.4.1 節</a>。
      </td></tr><tr><td><code class="structname">pg_stat_progress_create_index</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.9.1.2"></a></td><td>每個正在執行 <code class="command">CREATE INDEX</code> 或 <code class="command">REINDEX</code> 的後端各一筆資料列，顯示目前進度。
      請參閱<a class="xref" href="../progress-reporting/create-index-progress-reporting.md#create-index-progress-reporting">第 27.4.4 節</a>。
     </td></tr><tr><td><code class="structname">pg_stat_progress_vacuum</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.10.1.2"></a></td><td>每個正在執行 <code class="command">VACUUM</code> 的後端（包括 autovacuum 工作程序）各一筆資料列，顯示目前進度。
       請參閱<a class="xref" href="../progress-reporting/vacuum-progress-reporting.md#vacuum-progress-reporting">第 27.4.5 節</a>。
      </td></tr><tr><td><code class="structname">pg_stat_progress_cluster</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.11.1.2"></a></td><td>每個正在執行
       <code class="command">CLUSTER</code> 或 <code class="command">VACUUM FULL</code> 的後端各一筆資料列，顯示目前進度。
       請參閱<a class="xref" href="../progress-reporting/cluster-progress-reporting.md#cluster-progress-reporting">第 27.4.2 節</a>。
      </td></tr><tr><td><code class="structname">pg_stat_progress_basebackup</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.12.1.2"></a></td><td>每個正在串流基礎備份的 WAL 傳送程序各一筆資料列，
       顯示目前進度。
       請參閱<a class="xref" href="../progress-reporting/basebackup-progress-reporting.md#basebackup-progress-reporting">第 27.4.6 節</a>。
      </td></tr><tr><td><code class="structname">pg_stat_progress_copy</code><a class="indexterm" id="id-1.6.14.7.6.7.2.2.13.1.2"></a></td><td>每個正在執行 <code class="command">COPY</code> 的後端各一筆資料列，顯示目前進度。
       請參閱<a class="xref" href="../progress-reporting/copy-progress-reporting.md#copy-progress-reporting">第 27.4.3 節</a>。
      </td></tr></tbody></table>

<br><a id="MONITORING-STATS-VIEWS-TABLE"></a>

### 表 27.2. 已收集的統計檢視表 [#](#monitoring-stats-views-table) <a href="#monitoring-stats-views-table" id="monitoring-stats-views-table"></a>

<table border="1" class="table" summary="已收集的統計檢視表"><colgroup><col/><col/></colgroup><thead><tr><th>檢視表名稱</th><th>說明</th></tr></thead><tbody><tr><td><code class="structname">pg_stat_archiver</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.1.1.2"></a></td><td>僅有一筆資料列，顯示有關
       WAL 歸檔程序活動的統計資訊。詳情請參閱
       <a class="link" href="monitoring-pg-stat-archiver-view.md#monitoring-pg-stat-archiver-view">
<code class="structname">pg_stat_archiver</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_bgwriter</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.2.1.2"></a></td><td>僅有一筆資料列，顯示有關
       背景寫入程序活動的統計資訊。詳情請參閱
       <a class="link" href="monitoring-pg-stat-bgwriter-view.md#monitoring-pg-stat-bgwriter-view">
<code class="structname">pg_stat_bgwriter</code></a>。
     </td></tr><tr><td><code class="structname">pg_stat_checkpointer</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.3.1.2"></a></td><td>僅有一筆資料列，顯示有關
       檢查點程序活動的統計資訊。詳情請參閱
       <a class="link" href="monitoring-pg-stat-checkpointer-view.md#monitoring-pg-stat-checkpointer-view">
<code class="structname">pg_stat_checkpointer</code></a>。
     </td></tr><tr><td><code class="structname">pg_stat_database</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.4.1.2"></a></td><td>每個資料庫一筆資料列，顯示資料庫層級的統計資訊。詳情請參閱
       <a class="link" href="monitoring-pg-stat-database-view.md#monitoring-pg-stat-database-view">
<code class="structname">pg_stat_database</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_database_conflicts</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.5.1.2"></a></td><td>
       每個資料庫一筆資料列，顯示資料庫層級中，因與待命伺服器上復原作業衝突而導致查詢取消的統計資訊。
       詳情請參閱<a class="link" href="monitoring-pg-stat-database-conflicts-view.md#monitoring-pg-stat-database-conflicts-view">
<code class="structname">pg_stat_database_conflicts</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_io</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.6.1.2"></a></td><td>
       後端類型、情境（context）及目標物件的每種組合各一筆資料列，
       包含叢集層級的 I/O 統計資訊。
       詳情請參閱<a class="link" href="../monitoring-stats.md#monitoring-pg-stat-io-view">
<code class="structname">pg_stat_io</code></a>。
     </td></tr><tr><td><code class="structname">pg_stat_replication_slots</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.7.1.2"></a></td><td>每個複寫插槽一筆資料列，顯示有關該
       複寫插槽使用情形的統計資訊。詳情請參閱
       <a class="link" href="monitoring-pg-stat-replication-slots-view.md#monitoring-pg-stat-replication-slots-view">
<code class="structname">pg_stat_replication_slots</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_slru</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.8.1.2"></a></td><td>每個 SLRU 一筆資料列，顯示相關作業的統計資訊。詳情請參閱
       <a class="link" href="monitoring-pg-stat-slru-view.md#monitoring-pg-stat-slru-view">
<code class="structname">pg_stat_slru</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_subscription_stats</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.9.1.2"></a></td><td>每個訂閱一筆資料列，顯示有關錯誤與衝突的統計資訊。
      詳情請參閱<a class="link" href="monitoring-pg-stat-subscription-stats.md#monitoring-pg-stat-subscription-stats">
<code class="structname">pg_stat_subscription_stats</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_wal</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.10.1.2"></a></td><td>僅有一筆資料列，顯示有關 WAL 活動的統計資訊。詳情請參閱
       <a class="link" href="monitoring-pg-stat-wal-view.md#monitoring-pg-stat-wal-view">
<code class="structname">pg_stat_wal</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_all_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.11.1.2"></a></td><td>
       目前資料庫中每個資料表各一筆資料列，顯示有關
       該特定資料表存取情形的統計資訊。
       詳情請參閱<a class="link" href="monitoring-pg-stat-all-tables-view.md#monitoring-pg-stat-all-tables-view">
<code class="structname">pg_stat_all_tables</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_sys_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.12.1.2"></a></td><td>與 <code class="structname">pg_stat_all_tables</code> 相同，
      但僅顯示系統資料表。</td></tr><tr><td><code class="structname">pg_stat_user_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.13.1.2"></a></td><td>與 <code class="structname">pg_stat_all_tables</code> 相同，
      但僅顯示使用者資料表。</td></tr><tr><td><code class="structname">pg_stat_xact_all_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.14.1.2"></a></td><td>與 <code class="structname">pg_stat_all_tables</code> 類似，
      但計算的是目前交易中至今已執行的動作（這些動作<span class="emphasis"><em>尚未</em></span>
      被納入 <code class="structname">pg_stat_all_tables</code> 及相關檢視表中）。
      本檢視表中並未提供存活資料列數、死亡資料列數，以及 vacuum 與
      analyze 動作等欄位。</td></tr><tr><td><code class="structname">pg_stat_xact_sys_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.15.1.2"></a></td><td>與 <code class="structname">pg_stat_xact_all_tables</code> 相同，
      但僅顯示系統資料表。</td></tr><tr><td><code class="structname">pg_stat_xact_user_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.16.1.2"></a></td><td>與 <code class="structname">pg_stat_xact_all_tables</code> 相同，
      但僅顯示使用者資料表。</td></tr><tr><td><code class="structname">pg_stat_all_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.17.1.2"></a></td><td>
       目前資料庫中每個索引各一筆資料列，顯示有關
       該特定索引存取情形的統計資訊。
       詳情請參閱<a class="link" href="../monitoring-stats.md#monitoring-pg-stat-all-indexes-view">
<code class="structname">pg_stat_all_indexes</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_sys_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.18.1.2"></a></td><td>與 <code class="structname">pg_stat_all_indexes</code> 相同，
      但僅顯示系統資料表上的索引。</td></tr><tr><td><code class="structname">pg_stat_user_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.19.1.2"></a></td><td>與 <code class="structname">pg_stat_all_indexes</code> 相同，
      但僅顯示使用者資料表上的索引。</td></tr><tr><td><code class="structname">pg_stat_user_functions</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.20.1.2"></a></td><td>
       每個受追蹤的函式各一筆資料列，顯示有關
       該函式執行情形的統計資訊。詳情請參閱
       <a class="link" href="monitoring-pg-stat-user-functions-view.md#monitoring-pg-stat-user-functions-view">
<code class="structname">pg_stat_user_functions</code></a>。
      </td></tr><tr><td><code class="structname">pg_stat_xact_user_functions</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.21.1.2"></a></td><td>與 <code class="structname">pg_stat_user_functions</code> 類似，
      但僅計算目前交易期間的呼叫次數（這些呼叫<span class="emphasis"><em>尚未</em></span>
      被納入 <code class="structname">pg_stat_user_functions</code> 中）。</td></tr><tr><td><code class="structname">pg_statio_all_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.22.1.2"></a></td><td>
       目前資料庫中每個資料表各一筆資料列，顯示有關
       該特定資料表 I/O 情形的統計資訊。
       詳情請參閱<a class="link" href="monitoring-pg-statio-all-tables-view.md#monitoring-pg-statio-all-tables-view">
<code class="structname">pg_statio_all_tables</code></a>。
      </td></tr><tr><td><code class="structname">pg_statio_sys_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.23.1.2"></a></td><td>與 <code class="structname">pg_statio_all_tables</code> 相同，
      但僅顯示系統資料表。</td></tr><tr><td><code class="structname">pg_statio_user_tables</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.24.1.2"></a></td><td>與 <code class="structname">pg_statio_all_tables</code> 相同，
      但僅顯示使用者資料表。</td></tr><tr><td><code class="structname">pg_statio_all_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.25.1.2"></a></td><td>
       目前資料庫中每個索引各一筆資料列，
       顯示有關該特定索引 I/O 情形的統計資訊。
       詳情請參閱<a class="link" href="monitoring-pg-statio-all-indexes-view.md#monitoring-pg-statio-all-indexes-view">
<code class="structname">pg_statio_all_indexes</code></a>。
      </td></tr><tr><td><code class="structname">pg_statio_sys_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.26.1.2"></a></td><td>與 <code class="structname">pg_statio_all_indexes</code> 相同，
      但僅顯示系統資料表上的索引。</td></tr><tr><td><code class="structname">pg_statio_user_indexes</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.27.1.2"></a></td><td>與 <code class="structname">pg_statio_all_indexes</code> 相同，
      但僅顯示使用者資料表上的索引。</td></tr><tr><td><code class="structname">pg_statio_all_sequences</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.28.1.2"></a></td><td>
       目前資料庫中每個序列各一筆資料列，
       顯示有關該特定序列 I/O 情形的統計資訊。
       詳情請參閱<a class="link" href="monitoring-pg-statio-all-sequences-view.md#monitoring-pg-statio-all-sequences-view">
<code class="structname">pg_statio_all_sequences</code></a>。
     </td></tr><tr><td><code class="structname">pg_statio_sys_sequences</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.29.1.2"></a></td><td>與 <code class="structname">pg_statio_all_sequences</code> 相同，
      但僅顯示系統序列。（目前並未定義任何系統序列，
      因此本檢視表始終為空。）</td></tr><tr><td><code class="structname">pg_statio_user_sequences</code><a class="indexterm" id="id-1.6.14.7.6.8.2.2.30.1.2"></a></td><td>與 <code class="structname">pg_statio_all_sequences</code> 相同，
      但僅顯示使用者序列。</td></tr></tbody></table>

<br>

每個索引的統計資訊，對於判斷哪些索引正在被使用，以及它們的效用如何，特別有用。

`pg_stat_io` 以及 `pg_statio_` 這一系列檢視表，對於判斷緩衝快取的效用十分有用。它們可以用來計算快取命中率。請注意，雖然 PostgreSQL 的 I/O 統計資訊會擷取到大部分核心（kernel）被呼叫以執行 I/O 的情況，但它們並不會區分必須從磁碟擷取的資料，與已存在於核心分頁快取（page cache）中的資料。建議使用者將 PostgreSQL 的統計檢視表與作業系統工具程式搭配使用，以更完整地了解其資料庫的 I/O 效能。

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
