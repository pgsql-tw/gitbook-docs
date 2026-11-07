# 27.2.17. pg_stat_database

<a id="MONITORING-PG-STAT-DATABASE-VIEW"></a>

## 27.2.17. `pg_stat_database` [#](#monitoring-pg-stat-database-view) <a href="#monitoring-pg-stat-database-view" id="monitoring-pg-stat-database-view"></a>

<a id="id-1.6.14.7.21.2"></a>

`pg_stat_database` 檢視表中，叢集中的每個資料庫
各會有一筆資料列，另外加上一筆屬於共享物件的資料列，顯示
資料庫層級的統計資訊。

<a id="PG-STAT-DATABASE-VIEW"></a>

### 表 27.27. `pg_stat_database` 檢視表 [#](#pg-stat-database-view) <a href="#pg-stat-database-view" id="pg-stat-database-view"></a>

<table border="1" class="table" summary="pg_stat_database 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       此資料庫的 OID；若為屬於共享關聯的物件，則為 0
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       此資料庫的名稱；若為共享
       物件，則為 <code class="literal">NULL</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numbackends</code> <code class="type">integer</code>
</p>
<p>
       目前連線至此資料庫的後端數量；若為共享
       物件，則為 <code class="literal">NULL</code>。這是此檢視表中唯一一個
       回傳反映目前狀態之值的欄位；所有其他
       欄位所回傳的，都是自上次重設以來所累計的值。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">xact_commit</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中已提交的
       交易數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">xact_rollback</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中已回復（rolled back）的
       交易數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_read</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中已讀取的磁碟區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       發現磁碟區塊已存在於緩衝快取中，因此不需要進行讀取的
       次數（此欄位僅包含 PostgreSQL 緩衝快取中的命中，
       不包含作業系統檔案系統快取中的命中）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_returned</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中由循序掃描擷取的存活資料列數，以及由索引掃描所回傳的索引項目數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_fetched</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中由索引掃描所擷取的存活資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_inserted</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中由查詢所插入的資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_updated</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中由查詢所更新的資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tup_deleted</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中由查詢所刪除的資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conflicts</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中因與復原作業衝突而取消的查詢數量。
       （衝突僅發生於待命伺服器上；詳情請參閱
       <a class="link" href="monitoring-pg-stat-database-conflicts-view.md#monitoring-pg-stat-database-conflicts-view">
<code class="structname">pg_stat_database_conflicts</code></a>。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_files</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中由查詢所建立的暫存檔案數量。
       無論建立暫存檔案的原因為何（例如排序或雜湊處理），
       也無論 <a class="xref" href="../../runtime-config/runtime-config-logging.md#GUC-LOG-TEMP-FILES">log_temp_files</a> 的設定
       為何，所有暫存檔案都會被計入。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_bytes</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中由查詢寫入暫存檔案的
       總資料量。無論建立暫存檔案的原因為何，
       也無論 <a class="xref" href="../../runtime-config/runtime-config-logging.md#GUC-LOG-TEMP-FILES">log_temp_files</a> 的設定為何，所有
       暫存檔案都會被計入。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">deadlocks</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中偵測到的死結（deadlock）數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">checksum_failures</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中（或某個共享物件上）偵測到的資料分頁總和檢查碼
       失敗次數；若停用資料總和檢查碼，則為 NULL。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">checksum_last_failure</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此資料庫中（或某個共享物件上）偵測到最後一次資料分頁總和檢查碼
       失敗的時間；若停用資料總和檢查碼，則為 NULL。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       此資料庫中後端讀取資料檔案區塊所花費的時間，
       以毫秒為單位（若啟用了 <a class="xref" href="../../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>，
       否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       此資料庫中後端寫入資料檔案區塊所花費的時間，
       以毫秒為單位（若啟用了 <a class="xref" href="../../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>，
       否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">session_time</code> <code class="type">double precision</code>
</p>
<p>
       此資料庫中資料庫工作階段所花費的時間，以毫秒為單位
       （請注意，統計資訊僅在工作階段狀態變更時才會更新，因此若
       工作階段已閒置很長一段時間，這段閒置時間並不會被計入）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">active_time</code> <code class="type">double precision</code>
</p>
<p>
       此資料庫中執行 SQL 陳述式所花費的時間，以毫秒為單位
       （這對應於
       <code class="literal">active</code> 與
       <code class="literal">fastpath function call</code> 這兩個狀態，見 <a class="link" href="../monitoring-stats.md#monitoring-pg-stat-activity-view">
<code class="structname">pg_stat_activity</code></a>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idle_in_transaction_time</code> <code class="type">double precision</code>
</p>
<p>
       此資料庫中處於交易內閒置狀態所花費的時間，以毫秒為單位
       （這對應於
       <code class="literal">idle in transaction</code> 與
       <code class="literal">idle in transaction (aborted)</code> 這兩個狀態，見 <a class="link" href="../monitoring-stats.md#monitoring-pg-stat-activity-view">
<code class="structname">pg_stat_activity</code></a>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sessions</code> <code class="type">bigint</code>
</p>
<p>
       建立至此資料庫的工作階段總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sessions_abandoned</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫因與用戶端的連線遺失而終止的
       資料庫工作階段數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sessions_fatal</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫因嚴重錯誤而終止的
       資料庫工作階段數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sessions_killed</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫因操作人員介入而終止的
       資料庫工作階段數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parallel_workers_to_launch</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫上的查詢計畫要啟動的平行工作程序數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parallel_workers_launched</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫上查詢已啟動的平行工作程序數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       這些統計資訊上次重設的時間
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
