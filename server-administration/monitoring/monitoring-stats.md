<a id="MONITORING-STATS"></a>

## 27.2. 累計統計系統 [#](#monitoring-stats) <a href="#monitoring-stats" id="monitoring-stats"></a>

[27.2.1. 統計收集設定](monitoring-stats.md#monitoring-stats-setup)

[27.2.2. 檢視統計資訊](monitoring-stats/monitoring-stats-views.md#monitoring-stats-views)

[27.2.3. `pg_stat_activity`](monitoring-stats.md#monitoring-pg-stat-activity-view)

[27.2.4. `pg_stat_replication`](monitoring-stats.md#monitoring-pg-stat-replication-view)

[27.2.5. `pg_stat_replication_slots`](monitoring-stats/monitoring-pg-stat-replication-slots-view.md#monitoring-pg-stat-replication-slots-view)

[27.2.6. `pg_stat_wal_receiver`](monitoring-stats/monitoring-pg-stat-wal-receiver-view.md#monitoring-pg-stat-wal-receiver-view)

[27.2.7. `pg_stat_recovery_prefetch`](monitoring-stats/monitoring-pg-stat-recovery-prefetch.md#monitoring-pg-stat-recovery-prefetch)

[27.2.8. `pg_stat_subscription`](monitoring-stats/monitoring-pg-stat-subscription.md#monitoring-pg-stat-subscription)

[27.2.9. `pg_stat_subscription_stats`](monitoring-stats/monitoring-pg-stat-subscription-stats.md#monitoring-pg-stat-subscription-stats)

[27.2.10. `pg_stat_ssl`](monitoring-stats/monitoring-pg-stat-ssl-view.md#monitoring-pg-stat-ssl-view)

[27.2.11. `pg_stat_gssapi`](monitoring-stats/monitoring-pg-stat-gssapi-view.md#monitoring-pg-stat-gssapi-view)

[27.2.12. `pg_stat_archiver`](monitoring-stats/monitoring-pg-stat-archiver-view.md#monitoring-pg-stat-archiver-view)

[27.2.13. `pg_stat_io`](monitoring-stats.md#monitoring-pg-stat-io-view)

[27.2.14. `pg_stat_bgwriter`](monitoring-stats/monitoring-pg-stat-bgwriter-view.md#monitoring-pg-stat-bgwriter-view)

[27.2.15. `pg_stat_checkpointer`](monitoring-stats/monitoring-pg-stat-checkpointer-view.md#monitoring-pg-stat-checkpointer-view)

[27.2.16. `pg_stat_wal`](monitoring-stats/monitoring-pg-stat-wal-view.md#monitoring-pg-stat-wal-view)

[27.2.17. `pg_stat_database`](monitoring-stats/monitoring-pg-stat-database-view.md#monitoring-pg-stat-database-view)

[27.2.18. `pg_stat_database_conflicts`](monitoring-stats/monitoring-pg-stat-database-conflicts-view.md#monitoring-pg-stat-database-conflicts-view)

[27.2.19. `pg_stat_all_tables`](monitoring-stats/monitoring-pg-stat-all-tables-view.md#monitoring-pg-stat-all-tables-view)

[27.2.20. `pg_stat_all_indexes`](monitoring-stats.md#monitoring-pg-stat-all-indexes-view)

[27.2.21. `pg_statio_all_tables`](monitoring-stats/monitoring-pg-statio-all-tables-view.md#monitoring-pg-statio-all-tables-view)

[27.2.22. `pg_statio_all_indexes`](monitoring-stats/monitoring-pg-statio-all-indexes-view.md#monitoring-pg-statio-all-indexes-view)

[27.2.23. `pg_statio_all_sequences`](monitoring-stats/monitoring-pg-statio-all-sequences-view.md#monitoring-pg-statio-all-sequences-view)

[27.2.24. `pg_stat_user_functions`](monitoring-stats/monitoring-pg-stat-user-functions-view.md#monitoring-pg-stat-user-functions-view)

[27.2.25. `pg_stat_slru`](monitoring-stats/monitoring-pg-stat-slru-view.md#monitoring-pg-stat-slru-view)

[27.2.26. 統計函式](monitoring-stats.md#monitoring-stats-functions)

<a id="id-1.6.14.7.2"></a>

PostgreSQL 的*累計統計系統*（cumulative statistics system）支援收集並回報有關伺服器活動的資訊。目前，對資料表與索引的存取都會以磁碟區塊與個別資料列兩種層面進行計數。每個資料表中的總資料列數，以及每個資料表的 vacuum 與 analyze 動作相關資訊，也都會被計數。若啟用該功能，對使用者自訂函式的呼叫次數，以及花費在每個函式上的總時間也會被計數。

PostgreSQL 也支援回報動態資訊，說明系統目前正在進行的確切動作，例如其他伺服器程序目前正在執行的確切命令，以及系統中存在哪些其他連線。此功能與累計統計系統是各自獨立的。

<a id="MONITORING-STATS-SETUP"></a>

### 27.2.1. 統計收集設定 [#](#monitoring-stats-setup) <a href="#monitoring-stats-setup" id="monitoring-stats-setup"></a>

由於統計資訊的收集會為查詢執行帶來一些額外負擔，系統可以設定為收集或不收集資訊。這是透過通常設定於 `postgresql.conf` 中的設定參數來控制的。（有關設定組態參數的詳情，請參閱[第 19 章](../runtime-config/README.md)。）

[track_activities](../runtime-config/runtime-config-statistics.md#GUC-TRACK-ACTIVITIES) 參數可啟用對任何伺服器程序目前正在執行的命令的監控。

[track_cost_delay_timing](../runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING) 參數可啟用對以成本為基礎的 vacuum 延遲的監控。

[track_counts](../runtime-config/runtime-config-statistics.md#GUC-TRACK-COUNTS) 參數控制是否收集有關資料表與索引存取的累計統計資訊。

[track_functions](../runtime-config/runtime-config-statistics.md#GUC-TRACK-FUNCTIONS) 參數可啟用對使用者自訂函式使用情形的追蹤。

[track_io_timing](../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING) 參數可啟用對區塊讀取、寫入、延伸及 fsync 時間的監控。

[track_wal_io_timing](../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING) 參數可啟用對 WAL 讀取、寫入及 fsync 時間的監控。

通常這些參數會設定於 `postgresql.conf` 中，以便套用至所有伺服器程序，但也可以使用 [SET](../../reference/sql-commands/sql-set.md) 命令在個別工作階段中開啟或關閉它們。（為防止一般使用者對管理者隱藏其活動，只有超級使用者才被允許使用 `SET` 變更這些參數。）

累計統計資訊會收集於共享記憶體中。每個 PostgreSQL 程序都會在本機收集統計資訊，然後在適當的間隔時間更新共享資料。當伺服器（包括實體複本）正常關閉時，統計資料的永久副本會儲存於 `pg_stat` 子目錄中，以便統計資訊能夠在伺服器重新啟動後保留下來。相反地，若是從非正常關閉狀態啟動（例如：立即關閉之後、伺服器當機、從基礎備份啟動，以及時間點復原），則所有統計計數器都會被重設。

### 27.2.2. 檢視統計資訊 [#](#monitoring-stats-views) <a href="#monitoring-stats-views" id="monitoring-stats-views"></a>

完整內容請見 [27.2.2. 檢視統計資訊](monitoring-stats/monitoring-stats-views.md#monitoring-stats-views)。

<a id="MONITORING-PG-STAT-ACTIVITY-VIEW"></a>

### 27.2.3. `pg_stat_activity` [#](#monitoring-pg-stat-activity-view) <a href="#monitoring-pg-stat-activity-view" id="monitoring-pg-stat-activity-view"></a>

<a id="id-1.6.14.7.7.2"></a>

`pg_stat_activity` 檢視表中，每個伺服器程序都會有一筆資料列，顯示與該程序目前活動相關的資訊。

<a id="PG-STAT-ACTIVITY-VIEW"></a>

**表 27.3. `pg_stat_activity` 檢視表**

<table border="1" class="table" summary="pg_stat_activity 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       此後端所連線資料庫的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       此後端所連線資料庫的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       此後端的程序 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">leader_pid</code> <code class="type">integer</code>
</p>
<p>
       若此程序是平行查詢工作程序，則為平行群組領導者的程序 ID；若此程序
       是平行套用工作程序，則為領導套用工作程序的程序 ID。<code class="literal">NULL</code> 表示此
       程序為平行群組領導者或領導套用工作程序，或未參與任何平行作業。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesysid</code> <code class="type">oid</code>
</p>
<p>
       登入此後端之使用者的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usename</code> <code class="type">name</code>
</p>
<p>
       登入此後端之使用者的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">application_name</code> <code class="type">text</code>
</p>
<p>
       連線至此後端之應用程式的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_addr</code> <code class="type">inet</code>
</p>
<p>
       連線至此後端之用戶端的 IP 位址。
       若此欄位為 null，則表示用戶端是透過伺服器機器上的 Unix socket 連線，
       或者這是內部程序（例如 autovacuum）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_hostname</code> <code class="type">text</code>
</p>
<p>
       依據對 <code class="structfield">client_addr</code> 進行反向 DNS 查詢所回報之已連線用戶端主機名稱。此欄位
       僅在 IP 連線時，且僅在啟用 <a class="xref" href="../runtime-config/runtime-config-logging.md#GUC-LOG-HOSTNAME">log_hostname</a> 時才會為非 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_port</code> <code class="type">integer</code>
</p>
<p>
       用戶端用於與此後端通訊之 TCP 埠號；若使用 Unix socket，則為 <code class="literal">-1</code>。
       若此欄位為 null，則表示這是內部伺服器程序。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_start</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此程序啟動的時間。對於用戶端後端而言，
       這是用戶端連線至伺服器的時間。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">xact_start</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此程序目前交易開始的時間；若沒有正在進行中的交易，則為 null。若目前
       查詢是其交易中的第一個查詢，則此欄位與
       <code class="structfield">query_start</code> 欄位相同。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">query_start</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       目前正在執行之查詢開始的時間；或者，若
       <code class="structfield">state</code> 不是 <code class="literal">active</code>，則為上一個查詢
       開始的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">state_change</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       <code class="structfield">state</code> 上次變更的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wait_event_type</code> <code class="type">text</code>
</p>
<p>
       後端目前正在等待之事件的類型（如果有的話）；
       否則為 NULL。請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-TABLE">表 27.4</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wait_event</code> <code class="type">text</code>
</p>
<p>
       若後端目前正在等待，則為等待事件名稱；否則為 NULL。
       請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-ACTIVITY-TABLE">表 27.5</a>至
       <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TIMEOUT-TABLE">表 27.13</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">state</code> <code class="type">text</code>
</p>
<p>
       此後端目前的整體狀態。
       可能的值有：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">starting</code>：後端正處於初始啟動階段。用戶端
          驗證便是在此階段進行。
         </p></li><li class="listitem"><p>
<code class="literal">active</code>：後端正在執行查詢。
         </p></li><li class="listitem"><p>
<code class="literal">idle</code>：後端正在等待新的用戶端命令。
         </p></li><li class="listitem"><p>
<code class="literal">idle in transaction</code>：後端正處於某個交易中，
          但目前並未執行查詢。
         </p></li><li class="listitem"><p>
<code class="literal">idle in transaction (aborted)</code>：此狀態與
          <code class="literal">idle in transaction</code> 類似，差別在於交易中
          有某個陳述式導致了錯誤。
         </p></li><li class="listitem"><p>
<code class="literal">fastpath function call</code>：後端正在執行
          快速路徑函式。
         </p></li><li class="listitem"><p>
<code class="literal">disabled</code>：若此後端中的 <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-ACTIVITIES">track_activities</a> 被停用，則會回報此狀態。
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_xid</code> <code class="type">xid</code>
</p>
<p>
       此後端的最上層交易識別碼（如果有的話）；請參閱
       <a class="xref" href="../../internals/transactions/transaction-id.md">第 67.1 節</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_xmin</code> <code class="type">xid</code>
</p>
<p>
       目前後端的 <code class="literal">xmin</code> 界限。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">query_id</code> <code class="type">bigint</code>
</p>
<p>
      此後端最近一次查詢的識別碼。若
      <code class="structfield">state</code> 為 <code class="literal">active</code>，此
      欄位會顯示目前正在執行之查詢的識別碼。在
      其他所有狀態下，則顯示上一次已執行查詢的識別碼。查詢識別碼
      預設並不會被計算，因此除非啟用了
      <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID">compute_query_id</a>
      參數，或設定了會計算查詢識別碼的第三方模組，否則此
      欄位將為 null。
     </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">query</code> <code class="type">text</code>
</p>
<p>
       此後端最近一次查詢的文字內容。若
       <code class="structfield">state</code> 為 <code class="literal">active</code>，此欄位會顯示
       目前正在執行的查詢。在其他所有狀態下，則顯示上一次已執行
       的查詢。預設情況下，查詢文字會在 1024
       位元組處截斷；此數值可以透過參數
       <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-ACTIVITY-QUERY-SIZE">track_activity_query_size</a> 來變更。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_type</code> <code class="type">text</code>
</p>
<p>
       目前後端的類型。可能的類型有
       <code class="literal">autovacuum launcher</code>、<code class="literal">autovacuum worker</code>、
       <code class="literal">logical replication launcher</code>、
       <code class="literal">logical replication worker</code>、
       <code class="literal">parallel worker</code>、<code class="literal">background writer</code>、
       <code class="literal">client backend</code>、<code class="literal">checkpointer</code>、
       <code class="literal">archiver</code>、<code class="literal">standalone backend</code>、
       <code class="literal">startup</code>、<code class="literal">walreceiver</code>、
       <code class="literal">walsender</code>、<code class="literal">walwriter</code> 以及
       <code class="literal">walsummarizer</code>。
       此外，由擴充功能註冊的背景工作程序可能還有
       其他的類型。
      </p></td></tr></tbody></table>

<br>

### 注意

`wait_event` 與 `state` 這兩個欄位是
彼此獨立的。若後端處於 `active` 狀態，
它可能正在等待（`waiting`）、也可能沒有在等待某個事件。若狀態
為 `active` 而 `wait_event` 為非 null，
則表示某個查詢正在執行，但在系統中某處被阻擋。為了將回報負擔維持在較低水準，系統並不會
嘗試同步某個後端活動資料的不同層面。
因此，此檢視表各欄位之間可能存在暫時性的不一致。

<a id="WAIT-EVENT-TABLE"></a>

**表 27.4. 等待事件類型**

<table border="1" class="table" summary="等待事件類型"><colgroup><col/><col/></colgroup><thead><tr><th>等待事件類型</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">Activity</code></td><td>伺服器程序處於閒置狀態。此事件類型表示程序
       正在其主要處理迴圈中等待活動。
       <code class="literal">wait_event</code> 將標明特定的等待點；
       請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-ACTIVITY-TABLE">表 27.5</a>。
      </td></tr><tr><td><code class="literal">BufferPin</code></td><td>伺服器程序正在等待對某個
       資料緩衝區的獨占存取權。若
       另一個程序持有某個開放游標，且該游標上次讀取資料時正是來自該緩衝區，則緩衝區釘選（pin）等待可能會拖延較長時間。請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-BUFFERPIN-TABLE">表 27.6</a>。
      </td></tr><tr><td><code class="literal">Client</code></td><td>伺服器程序正在等待與使用者應用程式相連之
       socket 上的活動。因此，伺服器所等待發生的事情，
       是獨立於其內部程序之外的。
       <code class="literal">wait_event</code> 將標明特定的等待點；
       請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-CLIENT-TABLE">表 27.7</a>。
      </td></tr><tr><td><code class="literal">Extension</code></td><td>伺服器程序正在等待由擴充功能模組定義的
       某項條件。
       請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-EXTENSION-TABLE">表 27.8</a>。
      </td></tr><tr><td><code class="literal">InjectionPoint</code></td><td>伺服器程序正在等待某個注入點（injection point）達到
       測試中所定義的結果。詳情請參閱
       <a class="xref" href="../../server-programming/extend/xfunc-c.md#xfunc-addin-injection-points">第 36.10.14 節</a>。此
       類型並無預先定義的等待點。
      </td></tr><tr><td><code class="literal">IO</code></td><td>伺服器程序正在等待某項 I/O 作業完成。
       <code class="literal">wait_event</code> 將標明特定的等待點；
       請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-IO-TABLE">表 27.9</a>。
      </td></tr><tr><td><code class="literal">IPC</code></td><td>伺服器程序正在等待與
       另一個伺服器程序的某項互動。<code class="literal">wait_event</code> 將
       標明特定的等待點；
       請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-IPC-TABLE">表 27.10</a>。
      </td></tr><tr><td><code class="literal">Lock</code></td><td>伺服器程序正在等待某個重量級鎖（heavyweight lock）。
       重量級鎖，也稱為鎖定管理器鎖（lock manager lock）或簡稱鎖，
       主要用於保護 SQL 可見的物件，例如資料表。然而，
       它們也用於確保某些內部作業（例如關聯延伸）的互斥性。
       <code class="literal">wait_event</code>
       將標明所等待鎖的類型；
       請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-LOCK-TABLE">表 27.11</a>。
      </td></tr><tr><td><code class="literal">LWLock</code></td><td>伺服器程序正在等待某個輕量級鎖（lightweight lock）。
       大多數此類鎖都是用來保護共享記憶體中某個特定的資料結構。
       <code class="literal">wait_event</code> 將包含用來識別該輕量級鎖用途的名稱。（有些鎖具有特定的名稱；其他
       鎖則屬於一組具有相似用途的鎖。）
       請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-LWLOCK-TABLE">表 27.12</a>。
      </td></tr><tr><td><code class="literal">Timeout</code></td><td>伺服器程序正在等待某個逾時
       到期。<code class="literal">wait_event</code> 將標明特定的等待
       點；請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-TIMEOUT-TABLE">表 27.13</a>。
      </td></tr></tbody></table>

<br><a id="WAIT-EVENT-ACTIVITY-TABLE"></a>

**表 27.5. `Activity` 類型的等待事件**

<table border="1" class="table" summary="Activity 類型的等待事件"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Activity</code> 等待事件</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">ArchiverMain</code></td><td>正在歸檔程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">AutovacuumMain</code></td><td>正在 autovacuum 啟動程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">BgwriterHibernate</code></td><td>正在背景寫入程序中等待，處於休眠狀態。</td></tr><tr><td><code class="literal">BgwriterMain</code></td><td>正在背景寫入程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">CheckpointerMain</code></td><td>正在檢查點程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">CheckpointerShutdown</code></td><td>正在等待檢查點程序被終止。</td></tr><tr><td><code class="literal">IoWorkerMain</code></td><td>正在 IO 工作程序（IO Worker）的主要迴圈中等待。</td></tr><tr><td><code class="literal">LogicalApplyMain</code></td><td>正在邏輯複寫套用程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">LogicalLauncherMain</code></td><td>正在邏輯複寫啟動程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">LogicalParallelApplyMain</code></td><td>正在邏輯複寫平行套用程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">RecoveryWalStream</code></td><td>在串流復原期間，正在啟動程序的主要迴圈中等待 WAL 送達。</td></tr><tr><td><code class="literal">ReplicationSlotsyncMain</code></td><td>正在插槽同步工作程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">ReplicationSlotsyncShutdown</code></td><td>正在等待插槽同步工作程序關閉。</td></tr><tr><td><code class="literal">SysloggerMain</code></td><td>正在系統記錄程序（syslogger）的主要迴圈中等待。</td></tr><tr><td><code class="literal">WalReceiverMain</code></td><td>正在 WAL 接收程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">WalSenderMain</code></td><td>正在 WAL 傳送程序的主要迴圈中等待。</td></tr><tr><td><code class="literal">WalSummarizerWal</code></td><td>WAL 摘要程序正在等待有更多 WAL 產生。</td></tr><tr><td><code class="literal">WalWriterMain</code></td><td>正在 WAL 寫入程序的主要迴圈中等待。</td></tr></tbody></table>

<br><a id="WAIT-EVENT-BUFFERPIN-TABLE"></a>

**表 27.6. `Bufferpin` 類型的等待事件**

<table border="1" class="table" summary="Bufferpin 類型的等待事件"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">BufferPin</code> 等待事件</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">BufferPin</code></td><td>正在等待取得緩衝區的獨占釘選（pin）。</td></tr></tbody></table>

<br><a id="WAIT-EVENT-CLIENT-TABLE"></a>

**表 27.7. `Client` 類型的等待事件**

<table border="1" class="table" summary="Client 類型的等待事件"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Client</code> 等待事件</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">ClientRead</code></td><td>正在等待從用戶端讀取資料。</td></tr><tr><td><code class="literal">ClientWrite</code></td><td>正在等待將資料寫入用戶端。</td></tr><tr><td><code class="literal">GssOpenServer</code></td><td>在建立 GSSAPI 工作階段期間，正在等待從用戶端讀取資料。</td></tr><tr><td><code class="literal">LibpqwalreceiverConnect</code></td><td>WAL 接收程序正在等待與遠端伺服器建立連線。</td></tr><tr><td><code class="literal">LibpqwalreceiverReceive</code></td><td>WAL 接收程序正在等待從遠端伺服器接收資料。</td></tr><tr><td><code class="literal">SslOpenServer</code></td><td>在嘗試建立連線期間，正在等待 SSL。</td></tr><tr><td><code class="literal">WaitForStandbyConfirmation</code></td><td>正在等待實體待命伺服器接收並刷寫 WAL。</td></tr><tr><td><code class="literal">WalSenderWaitForWal</code></td><td>WAL 傳送程序正在等待 WAL 被刷寫。</td></tr><tr><td><code class="literal">WalSenderWriteData</code></td><td>在 WAL 傳送程序中處理來自 WAL 接收程序的回覆時，正在等待任何活動。</td></tr></tbody></table>

<br><a id="WAIT-EVENT-EXTENSION-TABLE"></a>

**表 27.8. `Extension` 類型的等待事件**

<table border="1" class="table" summary="Extension 類型的等待事件"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Extension</code> 等待事件</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">Extension</code></td><td>正在擴充功能中等待。</td></tr></tbody></table>

<br><a id="WAIT-EVENT-IO-TABLE"></a>

**表 27.9. `Io` 類型的等待事件**

<table border="1" class="table" summary="Io 類型的等待事件"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">IO</code> 等待事件</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">AioIoCompletion</code></td><td>正在等待另一個程序完成 IO。</td></tr><tr><td><code class="literal">AioIoUringExecution</code></td><td>正在等待透過 io_uring 執行 IO。</td></tr><tr><td><code class="literal">AioIoUringSubmit</code></td><td>正在等待透過 io_uring 提交 IO。</td></tr><tr><td><code class="literal">BasebackupRead</code></td><td>正在等待基礎備份從檔案讀取。</td></tr><tr><td><code class="literal">BasebackupSync</code></td><td>正在等待基礎備份所寫入的資料到達持久性儲存體。</td></tr><tr><td><code class="literal">BasebackupWrite</code></td><td>正在等待基礎備份寫入檔案。</td></tr><tr><td><code class="literal">BuffileRead</code></td><td>正在等待從緩衝檔案讀取。</td></tr><tr><td><code class="literal">BuffileTruncate</code></td><td>正在等待緩衝檔案被截斷。</td></tr><tr><td><code class="literal">BuffileWrite</code></td><td>正在等待寫入緩衝檔案。</td></tr><tr><td><code class="literal">ControlFileRead</code></td><td>正在等待從 <code class="filename">pg_control</code> 檔案讀取。</td></tr><tr><td><code class="literal">ControlFileSync</code></td><td>正在等待 <code class="filename">pg_control</code> 檔案到達持久性儲存體。</td></tr><tr><td><code class="literal">ControlFileSyncUpdate</code></td><td>正在等待對 <code class="filename">pg_control</code> 檔案的更新到達持久性儲存體。</td></tr><tr><td><code class="literal">ControlFileWrite</code></td><td>正在等待寫入 <code class="filename">pg_control</code> 檔案。</td></tr><tr><td><code class="literal">ControlFileWriteUpdate</code></td><td>正在等待寫入以更新 <code class="filename">pg_control</code> 檔案。</td></tr><tr><td><code class="literal">CopyFileCopy</code></td><td>正在等待檔案複製作業。</td></tr><tr><td><code class="literal">CopyFileRead</code></td><td>在檔案複製作業期間，正在等待讀取。</td></tr><tr><td><code class="literal">CopyFileWrite</code></td><td>在檔案複製作業期間，正在等待寫入。</td></tr><tr><td><code class="literal">DataFileExtend</code></td><td>正在等待關聯資料檔案被延伸。</td></tr><tr><td><code class="literal">DataFileFlush</code></td><td>正在等待關聯資料檔案到達持久性儲存體。</td></tr><tr><td><code class="literal">DataFileImmediateSync</code></td><td>正在等待關聯資料檔案立即同步至持久性儲存體。</td></tr><tr><td><code class="literal">DataFilePrefetch</code></td><td>正在等待從關聯資料檔案進行非同步預先擷取。</td></tr><tr><td><code class="literal">DataFileRead</code></td><td>正在等待從關聯資料檔案讀取。</td></tr><tr><td><code class="literal">DataFileSync</code></td><td>正在等待對關聯資料檔案的變更到達持久性儲存體。</td></tr><tr><td><code class="literal">DataFileTruncate</code></td><td>正在等待關聯資料檔案被截斷。</td></tr><tr><td><code class="literal">DataFileWrite</code></td><td>正在等待寫入關聯資料檔案。</td></tr><tr><td><code class="literal">DsmAllocate</code></td><td>正在等待配置動態共享記憶體區段。</td></tr><tr><td><code class="literal">DsmFillZeroWrite</code></td><td>正在等待以零值填滿動態共享記憶體後備檔案。</td></tr><tr><td><code class="literal">LockFileAddtodatadirRead</code></td><td>在向資料目錄鎖定檔案新增一行內容時，正在等待讀取。</td></tr><tr><td><code class="literal">LockFileAddtodatadirSync</code></td><td>在向資料目錄鎖定檔案新增一行內容時，正在等待資料到達持久性儲存體。</td></tr><tr><td><code class="literal">LockFileAddtodatadirWrite</code></td><td>在向資料目錄鎖定檔案新增一行內容時，正在等待寫入。</td></tr><tr><td><code class="literal">LockFileCreateRead</code></td><td>在建立資料目錄鎖定檔案時，正在等待讀取。</td></tr><tr><td><code class="literal">LockFileCreateSync</code></td><td>在建立資料目錄鎖定檔案時，正在等待資料到達持久性儲存體。</td></tr><tr><td><code class="literal">LockFileCreateWrite</code></td><td>在建立資料目錄鎖定檔案時，正在等待寫入。</td></tr><tr><td><code class="literal">LockFileRecheckdatadirRead</code></td><td>在重新檢查資料目錄鎖定檔案期間，正在等待讀取。</td></tr><tr><td><code class="literal">LogicalRewriteCheckpointSync</code></td><td>在檢查點期間，正在等待邏輯重寫對應到達持久性儲存體。</td></tr><tr><td><code class="literal">LogicalRewriteMappingSync</code></td><td>在邏輯重寫期間，正在等待對應資料到達持久性儲存體。</td></tr><tr><td><code class="literal">LogicalRewriteMappingWrite</code></td><td>在邏輯重寫期間，正在等待寫入對應資料。</td></tr><tr><td><code class="literal">LogicalRewriteSync</code></td><td>正在等待邏輯重寫對應到達持久性儲存體。</td></tr><tr><td><code class="literal">LogicalRewriteTruncate</code></td><td>在邏輯重寫期間，正在等待截斷對應資料。</td></tr><tr><td><code class="literal">LogicalRewriteWrite</code></td><td>正在等待寫入邏輯重寫對應。</td></tr><tr><td><code class="literal">RelationMapRead</code></td><td>正在等待讀取關聯對應檔案。</td></tr><tr><td><code class="literal">RelationMapReplace</code></td><td>正在等待以持久性方式取代關聯對應檔案。</td></tr><tr><td><code class="literal">RelationMapWrite</code></td><td>正在等待寫入關聯對應檔案。</td></tr><tr><td><code class="literal">ReorderBufferRead</code></td><td>在重新排序緩衝區管理期間，正在等待讀取。</td></tr><tr><td><code class="literal">ReorderBufferWrite</code></td><td>在重新排序緩衝區管理期間，正在等待寫入。</td></tr><tr><td><code class="literal">ReorderLogicalMappingRead</code></td><td>在重新排序緩衝區管理期間，正在等待讀取邏輯對應。</td></tr><tr><td><code class="literal">ReplicationSlotRead</code></td><td>正在等待從複寫插槽控制檔案讀取。</td></tr><tr><td><code class="literal">ReplicationSlotRestoreSync</code></td><td>在將複寫插槽控制檔案還原至記憶體期間，正在等待其到達持久性儲存體。</td></tr><tr><td><code class="literal">ReplicationSlotSync</code></td><td>正在等待複寫插槽控制檔案到達持久性儲存體。</td></tr><tr><td><code class="literal">ReplicationSlotWrite</code></td><td>正在等待寫入複寫插槽控制檔案。</td></tr><tr><td><code class="literal">SlruFlushSync</code></td><td>在檢查點或資料庫關閉期間，正在等待 SLRU 資料到達持久性儲存體。</td></tr><tr><td><code class="literal">SlruRead</code></td><td>正在等待讀取某個 SLRU 分頁。</td></tr><tr><td><code class="literal">SlruSync</code></td><td>在寫入某個分頁之後，正在等待 SLRU 資料到達持久性儲存體。</td></tr><tr><td><code class="literal">SlruWrite</code></td><td>正在等待寫入某個 SLRU 分頁。</td></tr><tr><td><code class="literal">SnapbuildRead</code></td><td>正在等待讀取序列化的歷史目錄快照。</td></tr><tr><td><code class="literal">SnapbuildSync</code></td><td>正在等待序列化的歷史目錄快照到達持久性儲存體。</td></tr><tr><td><code class="literal">SnapbuildWrite</code></td><td>正在等待寫入序列化的歷史目錄快照。</td></tr><tr><td><code class="literal">TimelineHistoryFileSync</code></td><td>正在等待透過串流複寫接收的時間軸歷史檔案到達持久性儲存體。</td></tr><tr><td><code class="literal">TimelineHistoryFileWrite</code></td><td>正在等待寫入透過串流複寫接收的時間軸歷史檔案。</td></tr><tr><td><code class="literal">TimelineHistoryRead</code></td><td>正在等待讀取時間軸歷史檔案。</td></tr><tr><td><code class="literal">TimelineHistorySync</code></td><td>正在等待新建立的時間軸歷史檔案到達持久性儲存體。</td></tr><tr><td><code class="literal">TimelineHistoryWrite</code></td><td>正在等待寫入新建立的時間軸歷史檔案。</td></tr><tr><td><code class="literal">TwophaseFileRead</code></td><td>正在等待讀取二階段狀態檔案。</td></tr><tr><td><code class="literal">TwophaseFileSync</code></td><td>正在等待二階段狀態檔案到達持久性儲存體。</td></tr><tr><td><code class="literal">TwophaseFileWrite</code></td><td>正在等待寫入二階段狀態檔案。</td></tr><tr><td><code class="literal">VersionFileSync</code></td><td>在建立資料庫期間，正在等待版本檔案到達持久性儲存體。</td></tr><tr><td><code class="literal">VersionFileWrite</code></td><td>在建立資料庫期間，正在等待寫入版本檔案。</td></tr><tr><td><code class="literal">WalsenderTimelineHistoryRead</code></td><td>在 walsender 時間軸命令期間，正在等待讀取時間軸歷史檔案。</td></tr><tr><td><code class="literal">WalBootstrapSync</code></td><td>在自舉（bootstrapping）期間，正在等待 WAL 到達持久性儲存體。</td></tr><tr><td><code class="literal">WalBootstrapWrite</code></td><td>在自舉期間，正在等待寫入某個 WAL 分頁。</td></tr><tr><td><code class="literal">WalCopyRead</code></td><td>在透過複製既有 WAL 區段來建立新的 WAL 區段時，正在等待讀取。</td></tr><tr><td><code class="literal">WalCopySync</code></td><td>正在等待透過複製既有區段所建立的新 WAL 區段到達持久性儲存體。</td></tr><tr><td><code class="literal">WalCopyWrite</code></td><td>在透過複製既有 WAL 區段來建立新的 WAL 區段時，正在等待寫入。</td></tr><tr><td><code class="literal">WalInitSync</code></td><td>正在等待新初始化的 WAL 檔案到達持久性儲存體。</td></tr><tr><td><code class="literal">WalInitWrite</code></td><td>在初始化新的 WAL 檔案期間，正在等待寫入。</td></tr><tr><td><code class="literal">WalRead</code></td><td>正在等待從某個 WAL 檔案讀取。</td></tr><tr><td><code class="literal">WalSummaryRead</code></td><td>正在等待從某個 WAL 摘要檔案讀取。</td></tr><tr><td><code class="literal">WalSummaryWrite</code></td><td>正在等待寫入某個 WAL 摘要檔案。</td></tr><tr><td><code class="literal">WalSync</code></td><td>正在等待某個 WAL 檔案到達持久性儲存體。</td></tr><tr><td><code class="literal">WalSyncMethodAssign</code></td><td>在指定新的 WAL 同步方法時，正在等待資料到達持久性儲存體。</td></tr><tr><td><code class="literal">WalWrite</code></td><td>正在等待寫入某個 WAL 檔案。</td></tr></tbody></table>

<br><a id="WAIT-EVENT-IPC-TABLE"></a>

**表 27.10. `Ipc` 類型的等待事件**

<table border="1" class="table" summary="Ipc 類型的等待事件"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">IPC</code> 等待事件</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">AppendReady</code></td><td>正在等待 <code class="literal">Append</code> 規劃節點的子規劃節點就緒。</td></tr><tr><td><code class="literal">ArchiveCleanupCommand</code></td><td>正在等待 <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND">archive_cleanup_command</a> 完成。</td></tr><tr><td><code class="literal">ArchiveCommand</code></td><td>正在等待 <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-ARCHIVE-COMMAND">archive_command</a> 完成。</td></tr><tr><td><code class="literal">BackendTermination</code></td><td>正在等待另一個後端終止。</td></tr><tr><td><code class="literal">BackupWaitWalArchive</code></td><td>正在等待備份所需的 WAL 檔案成功歸檔。</td></tr><tr><td><code class="literal">BgworkerShutdown</code></td><td>正在等待背景工作程序關閉。</td></tr><tr><td><code class="literal">BgworkerStartup</code></td><td>正在等待背景工作程序啟動。</td></tr><tr><td><code class="literal">BtreePage</code></td><td>正在等待延續平行 B-tree 掃描所需的分頁編號變為可用。</td></tr><tr><td><code class="literal">BufferIo</code></td><td>正在等待緩衝區 I/O 完成。</td></tr><tr><td><code class="literal">CheckpointDelayComplete</code></td><td>正在等待某個阻擋檢查點完成的後端。</td></tr><tr><td><code class="literal">CheckpointDelayStart</code></td><td>正在等待某個阻擋檢查點開始的後端。</td></tr><tr><td><code class="literal">CheckpointDone</code></td><td>正在等待某個檢查點完成。</td></tr><tr><td><code class="literal">CheckpointStart</code></td><td>正在等待某個檢查點開始。</td></tr><tr><td><code class="literal">ExecuteGather</code></td><td>在執行 <code class="literal">Gather</code> 規劃節點時，正在等待來自子程序的活動。</td></tr><tr><td><code class="literal">HashBatchAllocate</code></td><td>正在等待已選定的 Parallel Hash 參與者配置雜湊表。</td></tr><tr><td><code class="literal">HashBatchElect</code></td><td>正在等待選出一個 Parallel Hash 參與者以配置雜湊表。</td></tr><tr><td><code class="literal">HashBatchLoad</code></td><td>正在等待其他 Parallel Hash 參與者完成載入雜湊表。</td></tr><tr><td><code class="literal">HashBuildAllocate</code></td><td>正在等待已選定的 Parallel Hash 參與者配置初始雜湊表。</td></tr><tr><td><code class="literal">HashBuildElect</code></td><td>正在等待選出一個 Parallel Hash 參與者以配置初始雜湊表。</td></tr><tr><td><code class="literal">HashBuildHashInner</code></td><td>正在等待其他 Parallel Hash 參與者完成對內部關聯進行雜湊處理。</td></tr><tr><td><code class="literal">HashBuildHashOuter</code></td><td>正在等待其他 Parallel Hash 參與者完成對外部關聯進行分割。</td></tr><tr><td><code class="literal">HashGrowBatchesDecide</code></td><td>正在等待選出一個 Parallel Hash 參與者以決定未來批次的成長方式。</td></tr><tr><td><code class="literal">HashGrowBatchesElect</code></td><td>正在等待選出一個 Parallel Hash 參與者以配置更多批次。</td></tr><tr><td><code class="literal">HashGrowBatchesFinish</code></td><td>正在等待已選定的 Parallel Hash 參與者決定未來批次的成長方式。</td></tr><tr><td><code class="literal">HashGrowBatchesReallocate</code></td><td>正在等待已選定的 Parallel Hash 參與者配置更多批次。</td></tr><tr><td><code class="literal">HashGrowBatchesRepartition</code></td><td>正在等待其他 Parallel Hash 參與者完成重新分割。</td></tr><tr><td><code class="literal">HashGrowBucketsElect</code></td><td>正在等待選出一個 Parallel Hash 參與者以配置更多雜湊桶（bucket）。</td></tr><tr><td><code class="literal">HashGrowBucketsReallocate</code></td><td>正在等待已選定的 Parallel Hash 參與者完成配置更多雜湊桶。</td></tr><tr><td><code class="literal">HashGrowBucketsReinsert</code></td><td>正在等待其他 Parallel Hash 參與者完成將元組（tuple）插入新的雜湊桶中。</td></tr><tr><td><code class="literal">LogicalApplySendData</code></td><td>正在等待邏輯複寫領導套用程序將資料傳送給平行套用程序。</td></tr><tr><td><code class="literal">LogicalParallelApplyStateChange</code></td><td>正在等待邏輯複寫平行套用程序變更狀態。</td></tr><tr><td><code class="literal">LogicalSyncData</code></td><td>正在等待邏輯複寫遠端伺服器傳送資料以進行初始資料表同步。</td></tr><tr><td><code class="literal">LogicalSyncStateChange</code></td><td>正在等待邏輯複寫遠端伺服器變更狀態。</td></tr><tr><td><code class="literal">MessageQueueInternal</code></td><td>正在等待另一個程序附接至共享訊息佇列。</td></tr><tr><td><code class="literal">MessageQueuePutMessage</code></td><td>正在等待將通訊協定訊息寫入共享訊息佇列。</td></tr><tr><td><code class="literal">MessageQueueReceive</code></td><td>正在等待從共享訊息佇列接收位元組。</td></tr><tr><td><code class="literal">MessageQueueSend</code></td><td>正在等待將位元組傳送至共享訊息佇列。</td></tr><tr><td><code class="literal">MultixactCreation</code></td><td>正在等待某個 multixact 建立完成。</td></tr><tr><td><code class="literal">ParallelBitmapScan</code></td><td>正在等待平行點陣圖掃描初始化完成。</td></tr><tr><td><code class="literal">ParallelCreateIndexScan</code></td><td>正在等待平行 <code class="command">CREATE INDEX</code> 工作程序完成堆積掃描。</td></tr><tr><td><code class="literal">ParallelFinish</code></td><td>正在等待平行工作程序完成計算。</td></tr><tr><td><code class="literal">ProcarrayGroupUpdate</code></td><td>正在等待群組領導者在交易結束時清除交易 ID。</td></tr><tr><td><code class="literal">ProcSignalBarrier</code></td><td>正在等待某個屏障（barrier）事件被所有後端處理完畢。</td></tr><tr><td><code class="literal">Promote</code></td><td>正在等待待命伺服器完成提升（promotion）作業。</td></tr><tr><td><code class="literal">RecoveryConflictSnapshot</code></td><td>正在等待某個 vacuum 清理作業的復原衝突解決。</td></tr><tr><td><code class="literal">RecoveryConflictTablespace</code></td><td>正在等待卸除某個資料表空間的復原衝突解決。</td></tr><tr><td><code class="literal">RecoveryEndCommand</code></td><td>正在等待 <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-RECOVERY-END-COMMAND">recovery_end_command</a> 完成。</td></tr><tr><td><code class="literal">RecoveryPause</code></td><td>正在等待復原被恢復執行。</td></tr><tr><td><code class="literal">ReplicationOriginDrop</code></td><td>正在等待某個複寫來源（origin）變為非活躍狀態，以便將其卸除。</td></tr><tr><td><code class="literal">ReplicationSlotDrop</code></td><td>正在等待某個複寫插槽變為非活躍狀態，以便將其卸除。</td></tr><tr><td><code class="literal">RestoreCommand</code></td><td>正在等待 <a class="xref" href="../runtime-config/runtime-config-wal.md#GUC-RESTORE-COMMAND">restore_command</a> 完成。</td></tr><tr><td><code class="literal">SafeSnapshot</code></td><td>正在等待為某個 <code class="literal">READ ONLY DEFERRABLE</code> 交易取得有效的快照。</td></tr><tr><td><code class="literal">SyncRep</code></td><td>在同步複寫期間，正在等待來自遠端伺服器的確認。</td></tr><tr><td><code class="literal">WalReceiverExit</code></td><td>正在等待 WAL 接收程序結束。</td></tr><tr><td><code class="literal">WalReceiverUpstreamCatchup</code></td><td>正在等待上游伺服器的 WAL 刷寫位置追上所要求的起始點。</td></tr><tr><td><code class="literal">WalReceiverWaitStart</code></td><td>正在等待啟動程序傳送用於串流複寫的初始資料。</td></tr><tr><td><code class="literal">WalSummaryReady</code></td><td>正在等待產生新的 WAL 摘要。</td></tr><tr><td><code class="literal">XactGroupUpdate</code></td><td>正在等待群組領導者在交易結束時更新交易狀態。</td></tr></tbody></table>

<br><a id="WAIT-EVENT-LOCK-TABLE"></a>

**表 27.11. `Lock` 類型的等待事件**

<table border="1" class="table" summary="Lock 類型的等待事件"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Lock</code> 等待事件</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">advisory</code></td><td>正在等待取得諮詢型（advisory）使用者鎖。</td></tr><tr><td><code class="literal">applytransaction</code></td><td>正在等待取得邏輯複寫訂閱者正在套用之遠端交易上的鎖。</td></tr><tr><td><code class="literal">extend</code></td><td>正在等待延伸某個關聯。</td></tr><tr><td><code class="literal">frozenid</code></td><td>正在等待更新 <code class="structname">pg_database</code>.<code class="structfield">datfrozenxid</code> 以及 <code class="structname">pg_database</code>.<code class="structfield">datminmxid</code>。</td></tr><tr><td><code class="literal">object</code></td><td>正在等待取得非關聯資料庫物件上的鎖。</td></tr><tr><td><code class="literal">page</code></td><td>正在等待取得關聯某個分頁上的鎖。</td></tr><tr><td><code class="literal">relation</code></td><td>正在等待取得關聯上的鎖。</td></tr><tr><td><code class="literal">spectoken</code></td><td>正在等待取得推測性插入（speculative insertion）鎖。</td></tr><tr><td><code class="literal">transactionid</code></td><td>正在等待某個交易完成。</td></tr><tr><td><code class="literal">tuple</code></td><td>正在等待取得元組上的鎖。</td></tr><tr><td><code class="literal">userlock</code></td><td>正在等待取得使用者鎖。</td></tr><tr><td><code class="literal">virtualxid</code></td><td>正在等待取得虛擬交易 ID 鎖；請參閱<a class="xref" href="../../internals/transactions/transaction-id.md">第 67.1 節</a>。</td></tr></tbody></table>

<br><a id="WAIT-EVENT-LWLOCK-TABLE"></a>

**表 27.12. `Lwlock` 類型的等待事件**

<table border="1" class="table" summary="Lwlock 類型的等待事件"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">LWLock</code> 等待事件</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">AddinShmemInit</code></td><td>正在等待管理擴充功能在共享記憶體中的空間配置。</td></tr><tr><td><code class="literal">AioUringCompletion</code></td><td>正在等待另一個程序透過 io_uring 完成 IO。</td></tr><tr><td><code class="literal">AioWorkerSubmissionQueue</code></td><td>正在等待存取 AIO 工作程序提交佇列。</td></tr><tr><td><code class="literal">AutoFile</code></td><td>正在等待更新 <code class="filename">postgresql.auto.conf</code> 檔案。</td></tr><tr><td><code class="literal">Autovacuum</code></td><td>正在等待讀取或更新 autovacuum 工作程序目前狀態。</td></tr><tr><td><code class="literal">AutovacuumSchedule</code></td><td>正在等待確認已選定進行 autovacuum 的資料表仍然需要被 vacuum。</td></tr><tr><td><code class="literal">BackgroundWorker</code></td><td>正在等待讀取或更新背景工作程序狀態。</td></tr><tr><td><code class="literal">BtreeVacuum</code></td><td>正在等待讀取或更新 B-tree 索引相關的 vacuum 資訊。</td></tr><tr><td><code class="literal">BufferContent</code></td><td>正在等待存取記憶體中的某個資料分頁。</td></tr><tr><td><code class="literal">BufferMapping</code></td><td>正在等待將某個資料區塊與緩衝池中的緩衝區建立關聯。</td></tr><tr><td><code class="literal">CheckpointerComm</code></td><td>正在等待管理 fsync 要求。</td></tr><tr><td><code class="literal">CommitTs</code></td><td>正在等待讀取或更新交易提交時間戳記所設定的最後一個值。</td></tr><tr><td><code class="literal">CommitTsBuffer</code></td><td>正在等待提交時間戳記 SLRU 緩衝區上的 I/O。</td></tr><tr><td><code class="literal">CommitTsSLRU</code></td><td>正在等待存取提交時間戳記 SLRU 快取。</td></tr><tr><td><code class="literal">ControlFile</code></td><td>正在等待讀取或更新 <code class="filename">pg_control</code> 檔案，或建立新的 WAL 檔案。</td></tr><tr><td><code class="literal">DSMRegistry</code></td><td>正在等待讀取或更新動態共享記憶體登錄表。</td></tr><tr><td><code class="literal">DSMRegistryDSA</code></td><td>正在等待存取動態共享記憶體登錄表的動態共享記憶體配置器。</td></tr><tr><td><code class="literal">DSMRegistryHash</code></td><td>正在等待存取動態共享記憶體登錄表的共享雜湊表。</td></tr><tr><td><code class="literal">DynamicSharedMemoryControl</code></td><td>正在等待讀取或更新動態共享記憶體配置資訊。</td></tr><tr><td><code class="literal">InjectionPoint</code></td><td>正在等待讀取或更新與注入點相關的資訊。</td></tr><tr><td><code class="literal">LockFastPath</code></td><td>正在等待讀取或更新某個程序的快速路徑鎖資訊。</td></tr><tr><td><code class="literal">LockManager</code></td><td>正在等待讀取或更新有關「重量級」鎖的資訊。</td></tr><tr><td><code class="literal">LogicalRepLauncherDSA</code></td><td>正在等待存取邏輯複寫啟動程序的動態共享記憶體配置器。</td></tr><tr><td><code class="literal">LogicalRepLauncherHash</code></td><td>正在等待存取邏輯複寫啟動程序的共享雜湊表。</td></tr><tr><td><code class="literal">LogicalRepWorker</code></td><td>正在等待讀取或更新邏輯複寫工作程序的狀態。</td></tr><tr><td><code class="literal">MultiXactGen</code></td><td>正在等待讀取或更新共享 multixact 狀態。</td></tr><tr><td><code class="literal">MultiXactMemberBuffer</code></td><td>正在等待 multixact 成員 SLRU 緩衝區上的 I/O。</td></tr><tr><td><code class="literal">MultiXactMemberSLRU</code></td><td>正在等待存取 multixact 成員 SLRU 快取。</td></tr><tr><td><code class="literal">MultiXactOffsetBuffer</code></td><td>正在等待 multixact 位移 SLRU 緩衝區上的 I/O。</td></tr><tr><td><code class="literal">MultiXactOffsetSLRU</code></td><td>正在等待存取 multixact 位移 SLRU 快取。</td></tr><tr><td><code class="literal">MultiXactTruncation</code></td><td>正在等待讀取或截斷 multixact 資訊。</td></tr><tr><td><code class="literal">NotifyBuffer</code></td><td>正在等待 <code class="command">NOTIFY</code> 訊息 SLRU 緩衝區上的 I/O。</td></tr><tr><td><code class="literal">NotifyQueue</code></td><td>正在等待讀取或更新 <code class="command">NOTIFY</code> 訊息。</td></tr><tr><td><code class="literal">NotifyQueueTail</code></td><td>正在等待更新 <code class="command">NOTIFY</code> 訊息儲存空間的限制。</td></tr><tr><td><code class="literal">NotifySLRU</code></td><td>正在等待存取 <code class="command">NOTIFY</code> 訊息 SLRU 快取。</td></tr><tr><td><code class="literal">OidGen</code></td><td>正在等待配置新的 OID。</td></tr><tr><td><code class="literal">ParallelAppend</code></td><td>在執行 Parallel Append 規劃期間，正在等待選出下一個子規劃。</td></tr><tr><td><code class="literal">ParallelBtreeScan</code></td><td>在執行 Parallel B-tree 掃描規劃期間，正在等待同步工作程序。</td></tr><tr><td><code class="literal">ParallelHashJoin</code></td><td>在執行 Parallel Hash Join 規劃期間，正在等待同步工作程序。</td></tr><tr><td><code class="literal">ParallelQueryDSA</code></td><td>正在等待平行查詢的動態共享記憶體配置。</td></tr><tr><td><code class="literal">ParallelVacuumDSA</code></td><td>正在等待平行 vacuum 的動態共享記憶體配置。</td></tr><tr><td><code class="literal">PerSessionDSA</code></td><td>正在等待平行查詢的動態共享記憶體配置。</td></tr><tr><td><code class="literal">PerSessionRecordType</code></td><td>正在等待存取平行查詢中有關複合型別的資訊。</td></tr><tr><td><code class="literal">PerSessionRecordTypmod</code></td><td>正在等待存取平行查詢中有關用來識別匿名記錄型別之型別修飾詞的資訊。</td></tr><tr><td><code class="literal">PerXactPredicateList</code></td><td>在平行查詢期間，正在等待存取目前可序列化交易所持有的謂詞鎖（predicate lock）清單。</td></tr><tr><td><code class="literal">PgStatsData</code></td><td>正在等待存取共享記憶體統計資料。</td></tr><tr><td><code class="literal">PgStatsDSA</code></td><td>正在等待存取統計動態共享記憶體配置器。</td></tr><tr><td><code class="literal">PgStatsHash</code></td><td>正在等待存取統計共享記憶體雜湊表。</td></tr><tr><td><code class="literal">PredicateLockManager</code></td><td>正在等待存取可序列化交易所使用的謂詞鎖（predicate lock）資訊。</td></tr><tr><td><code class="literal">ProcArray</code></td><td>正在等待存取共享的每程序資料結構（通常是為了取得快照，或回報某個工作階段的交易 ID）。</td></tr><tr><td><code class="literal">RelationMapping</code></td><td>正在等待讀取或更新 <code class="filename">pg_filenode.map</code> 檔案（用於追蹤某些系統目錄的檔案節點指派情形）。</td></tr><tr><td><code class="literal">RelCacheInit</code></td><td>正在等待讀取或更新 <code class="filename">pg_internal.init</code> 關聯快取初始化檔案。</td></tr><tr><td><code class="literal">ReplicationOrigin</code></td><td>正在等待建立、卸除或使用某個複寫來源。</td></tr><tr><td><code class="literal">ReplicationOriginState</code></td><td>正在等待讀取或更新某個複寫來源的進度。</td></tr><tr><td><code class="literal">ReplicationSlotAllocation</code></td><td>正在等待配置或釋放複寫插槽。</td></tr><tr><td><code class="literal">ReplicationSlotControl</code></td><td>正在等待讀取或更新複寫插槽狀態。</td></tr><tr><td><code class="literal">ReplicationSlotIO</code></td><td>正在等待複寫插槽上的 I/O。</td></tr><tr><td><code class="literal">SerialBuffer</code></td><td>正在等待可序列化交易衝突 SLRU 緩衝區上的 I/O。</td></tr><tr><td><code class="literal">SerialControl</code></td><td>正在等待讀取或更新共享的 <code class="filename">pg_serial</code> 狀態。</td></tr><tr><td><code class="literal">SerializableFinishedList</code></td><td>正在等待存取已完成之可序列化交易清單。</td></tr><tr><td><code class="literal">SerializablePredicateList</code></td><td>正在等待存取可序列化交易所持有的謂詞鎖（predicate lock）清單。</td></tr><tr><td><code class="literal">SerializableXactHash</code></td><td>正在等待讀取或更新有關可序列化交易的資訊。</td></tr><tr><td><code class="literal">SerialSLRU</code></td><td>正在等待存取可序列化交易衝突 SLRU 快取。</td></tr><tr><td><code class="literal">SharedTidBitmap</code></td><td>在平行點陣圖索引掃描期間，正在等待存取共享的 TID 點陣圖。</td></tr><tr><td><code class="literal">SharedTupleStore</code></td><td>在平行查詢期間，正在等待存取共享的元組儲存區。</td></tr><tr><td><code class="literal">ShmemIndex</code></td><td>正在等待於共享記憶體中尋找或配置空間。</td></tr><tr><td><code class="literal">SInvalRead</code></td><td>正在等待從共享目錄失效佇列擷取訊息。</td></tr><tr><td><code class="literal">SInvalWrite</code></td><td>正在等待將訊息新增至共享目錄失效佇列。</td></tr><tr><td><code class="literal">SubtransBuffer</code></td><td>正在等待子交易 SLRU 緩衝區上的 I/O。</td></tr><tr><td><code class="literal">SubtransSLRU</code></td><td>正在等待存取子交易 SLRU 快取。</td></tr><tr><td><code class="literal">SyncRep</code></td><td>正在等待讀取或更新有關同步複寫狀態的資訊。</td></tr><tr><td><code class="literal">SyncScan</code></td><td>正在等待選擇同步資料表掃描的起始位置。</td></tr><tr><td><code class="literal">TablespaceCreate</code></td><td>正在等待建立或卸除資料表空間。</td></tr><tr><td><code class="literal">TwoPhaseState</code></td><td>正在等待讀取或更新已備妥交易（prepared transaction）的狀態。</td></tr><tr><td><code class="literal">WaitEventCustom</code></td><td>正在等待讀取或更新自訂等待事件的資訊。</td></tr><tr><td><code class="literal">WALBufMapping</code></td><td>正在等待替換 WAL 緩衝區中的某個分頁。</td></tr><tr><td><code class="literal">WALInsert</code></td><td>正在等待將 WAL 資料插入記憶體緩衝區。</td></tr><tr><td><code class="literal">WALSummarizer</code></td><td>正在等待讀取或更新 WAL 摘要化狀態。</td></tr><tr><td><code class="literal">WALWrite</code></td><td>正在等待 WAL 緩衝區被寫入磁碟。</td></tr><tr><td><code class="literal">WrapLimitsVacuum</code></td><td>正在等待更新交易 ID 與 multixact 消耗量的限制。</td></tr><tr><td><code class="literal">XactBuffer</code></td><td>正在等待交易狀態 SLRU 緩衝區上的 I/O。</td></tr><tr><td><code class="literal">XactSLRU</code></td><td>正在等待存取交易狀態 SLRU 快取。</td></tr><tr><td><code class="literal">XactTruncation</code></td><td>正在等待執行 <code class="function">pg_xact_status</code>，或更新其可用的最舊交易 ID。</td></tr><tr><td><code class="literal">XidGen</code></td><td>正在等待配置新的交易 ID。</td></tr></tbody></table>

<br><a id="WAIT-EVENT-TIMEOUT-TABLE"></a>

**表 27.13. `Timeout` 類型的等待事件**

<table border="1" class="table" summary="Timeout 類型的等待事件"><colgroup><col/><col/></colgroup><thead><tr><th><code class="literal">Timeout</code> 等待事件</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">BaseBackupThrottle</code></td><td>在基礎備份期間，因節流（throttling）活動而正在等待。</td></tr><tr><td><code class="literal">CheckpointWriteDelay</code></td><td>在執行檢查點期間，正在各次寫入之間等待。</td></tr><tr><td><code class="literal">PgSleep</code></td><td>因呼叫 <code class="function">pg_sleep</code> 或其同系列函式而正在等待。</td></tr><tr><td><code class="literal">RecoveryApplyDelay</code></td><td>因延遲設定，在復原期間正在等待套用 WAL。</td></tr><tr><td><code class="literal">RecoveryRetrieveRetryInterval</code></td><td>在復原期間，當任何來源（<code class="filename">pg_wal</code>、歸檔或串流）皆無可用的 WAL 資料時，正在等待。</td></tr><tr><td><code class="literal">RegisterSyncRequest</code></td><td>因要求佇列已滿，在向檢查點程序傳送同步要求時正在等待。</td></tr><tr><td><code class="literal">SpinDelay</code></td><td>在取得有爭用的自旋鎖（spinlock）時正在等待。</td></tr><tr><td><code class="literal">VacuumDelay</code></td><td>正在以成本為基礎的 vacuum 延遲點上等待。</td></tr><tr><td><code class="literal">VacuumTruncate</code></td><td>正在等待取得獨占鎖，以截斷所 vacuum 資料表結尾處的任何空白分頁。</td></tr><tr><td><code class="literal">WalSummarizerError</code></td><td>在 WAL 摘要程序發生錯誤之後正在等待。</td></tr></tbody></table>

<br>

以下是檢視等待事件方式的一些範例：

```

SELECT pid, wait_event_type, wait_event FROM pg_stat_activity WHERE wait_event is NOT NULL;
 pid  | wait_event_type | wait_event
------+-----------------+------------
 2540 | Lock            | relation
 6644 | LWLock          | ProcArray
(2 rows)
```

```

SELECT a.pid, a.wait_event, w.description
  FROM pg_stat_activity a JOIN
       pg_wait_events w ON (a.wait_event_type = w.type AND
                            a.wait_event = w.name)
  WHERE a.wait_event is NOT NULL and a.state = 'active';
-[ RECORD 1 ]------------------------------------------------------​------------
pid         | 686674
wait_event  | WALInitSync
description | Waiting for a newly initialized WAL file to reach durable storage
```

譯註：上方範例輸出依原文保留；其中的 WALInitSync 與表 27.9 所列的正式等待事件名稱 WalInitSync 大小寫不一致，實際名稱應以表中的 WalInitSync 為準。

### 注意

擴充功能可以將 `Extension`、
`InjectionPoint` 及 `LWLock` 事件
新增至[表 27.8](monitoring-stats.md#WAIT-EVENT-EXTENSION-TABLE)與
[表 27.12](monitoring-stats.md#WAIT-EVENT-LWLOCK-TABLE)所示的清單中。在某些情況下，
由擴充功能指派的 `LWLock` 名稱在所有伺服器程序中
並非都能取得。它可能僅被回報為
「`extension`」，而非
擴充功能所指派的名稱。

<a id="MONITORING-PG-STAT-REPLICATION-VIEW"></a>

### 27.2.4. `pg_stat_replication` [#](#monitoring-pg-stat-replication-view) <a href="#monitoring-pg-stat-replication-view" id="monitoring-pg-stat-replication-view"></a>

<a id="id-1.6.14.7.8.2"></a>

`pg_stat_replication` 檢視表中，每個
WAL 傳送程序都會有一筆資料列，顯示有關該
傳送程序所連線待命伺服器複寫情形的統計資訊。此處僅列出直接連線的待命伺服器；
並不提供有關下游待命伺服器的資訊。

<a id="PG-STAT-REPLICATION-VIEW"></a>

**表 27.14. `pg_stat_replication` 檢視表**

<table border="1" class="table" summary="pg_stat_replication 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       某個 WAL 傳送程序的程序 ID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usesysid</code> <code class="type">oid</code>
</p>
<p>
       登入此 WAL 傳送程序之使用者的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usename</code> <code class="type">name</code>
</p>
<p>
       登入此 WAL 傳送程序之使用者的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">application_name</code> <code class="type">text</code>
</p>
<p>
       連線至此 WAL 傳送程序之應用程式的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_addr</code> <code class="type">inet</code>
</p>
<p>
       連線至此 WAL 傳送程序之用戶端的 IP 位址。
       若此欄位為 null，則表示用戶端是透過伺服器機器上的 Unix socket 連線。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_hostname</code> <code class="type">text</code>
</p>
<p>
       依據對 <code class="structfield">client_addr</code> 進行反向 DNS 查詢所回報之已連線用戶端主機名稱。此欄位
       僅在 IP 連線時，且僅在啟用 <a class="xref" href="../runtime-config/runtime-config-logging.md#GUC-LOG-HOSTNAME">log_hostname</a> 時才會為非 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">client_port</code> <code class="type">integer</code>
</p>
<p>
       用戶端用於與此 WAL 傳送程序通訊之 TCP 埠號；若使用 Unix socket，則為 <code class="literal">-1</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_start</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此程序啟動的時間，也就是
       用戶端連線至此 WAL 傳送程序的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backend_xmin</code> <code class="type">xid</code>
</p>
<p>
       此待命伺服器透過
       <a class="xref" href="../runtime-config/runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK">hot_standby_feedback</a> 所回報的 <code class="literal">xmin</code> 界限。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">state</code> <code class="type">text</code>
</p>
<p>
       目前 WAL 傳送程序的狀態。
       可能的值有：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">startup</code>：此 WAL 傳送程序正在啟動中。
         </p></li><li class="listitem"><p>
<code class="literal">catchup</code>：此 WAL 傳送程序所連線的待命伺服器
          正在追趕主要伺服器。
         </p></li><li class="listitem"><p>
<code class="literal">streaming</code>：在其所連線的待命伺服器已追上主要伺服器之後，
          此 WAL 傳送程序正在串流變更內容。
         </p></li><li class="listitem"><p>
<code class="literal">backup</code>：此 WAL 傳送程序正在傳送備份。
         </p></li><li class="listitem"><p>
<code class="literal">stopping</code>：此 WAL 傳送程序正在停止中。
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sent_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       此連線上最後傳送的預寫式日誌位置
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">write_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       此待命伺服器最後寫入磁碟的預寫式日誌位置
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">flush_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       此待命伺服器最後刷寫至磁碟的預寫式日誌位置
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">replay_lsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       此待命伺服器上最後重播（replay）至資料庫的預寫式日誌位置
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">write_lag</code> <code class="type">interval</code>
</p>
<p>
       在本機刷寫最近的 WAL，與接收到此待命伺服器已將其寫入（但尚未
       刷寫或套用）的通知之間，所經過的時間。若此
       伺服器被設定為同步待命伺服器，這可以用來估算 <code class="literal">synchronous_commit</code>
       層級為 <code class="literal">remote_write</code> 時，在提交交易時所引入的延遲。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">flush_lag</code> <code class="type">interval</code>
</p>
<p>
       在本機刷寫最近的 WAL，與接收到此待命伺服器已將其寫入並刷寫
       （但尚未套用）的通知之間，所經過的時間。若此
       伺服器被設定為同步待命伺服器，這可以用來估算 <code class="literal">synchronous_commit</code>
       層級為 <code class="literal">on</code> 時，在提交交易時所引入的延遲。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">replay_lag</code> <code class="type">interval</code>
</p>
<p>
       在本機刷寫最近的 WAL，與接收到此待命伺服器已將其寫入、刷寫並
       套用的通知之間，所經過的時間。若此
       伺服器被設定為同步待命伺服器，這可以用來估算 <code class="literal">synchronous_commit</code>
       層級為 <code class="literal">remote_apply</code> 時，在提交交易時所引入的延遲。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sync_priority</code> <code class="type">integer</code>
</p>
<p>
       此待命伺服器在以優先順序為基礎的同步複寫中，被選為
       同步待命伺服器的優先順序。
       在以法定人數（quorum）為基礎的同步複寫中，此欄位並無作用。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sync_state</code> <code class="type">text</code>
</p>
<p>
       此待命伺服器的同步狀態。
       可能的值有：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">async</code>：此待命伺服器為非同步。
         </p></li><li class="listitem"><p>
<code class="literal">potential</code>：此待命伺服器目前為非同步，
          但若目前的某個同步待命伺服器發生故障，它可能會變為同步。
         </p></li><li class="listitem"><p>
<code class="literal">sync</code>：此待命伺服器為同步。
         </p></li><li class="listitem"><p>
<code class="literal">quorum</code>：此待命伺服器被視為法定人數待命伺服器的
          候選者。
         </p></li></ul></div><p>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reply_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       從待命伺服器收到最後一則回覆訊息的傳送時間
      </p></td></tr></tbody></table>

<br>

`pg_stat_replication` 檢視表中所回報的延遲時間，是針對最近的 WAL 從寫入、
刷寫、重播，到傳送端得知此事所耗費時間的量測值。若遠端伺服器被設定為
同步待命伺服器，這些時間代表的是每種同步提交層級所引入（或將會引入）的提交延遲。
對於非同步待命伺服器而言，`replay_lag` 欄位可近似估算最近交易
變得對查詢可見之前的延遲。若待命
伺服器已完全追上傳送端伺服器，且不再有 WAL 活動，則最近一次量測到的延遲時間
將會繼續顯示一小段時間，之後便會顯示為 NULL。

延遲時間對實體複寫會自動運作。邏輯解碼
外掛程式可以選擇性地發出追蹤訊息；若它們沒有這麼做，則追蹤
機制將直接顯示 NULL 延遲。

### 注意

所回報的延遲時間，並不是在假設目前重播速率下，用來預測待命伺服器追上
傳送端伺服器所需時間的預測值。這樣的系統在持續產生新 WAL 時會顯示類似的時間，
但在傳送端進入閒置狀態時則會有所不同。特別是，當待命伺服器已完全追上時，
`pg_stat_replication` 顯示的是寫入、刷寫並重播最近所回報 WAL 位置
所花費的時間，而非某些使用者可能預期的零值。這與量測近期寫入交易的同步提交
與交易可見性延遲此一目標是一致的。
為了減少期望不同延遲模型之使用者的困惑，在一個完全重播完畢的閒置系統上，
延遲欄位會在短暫時間後回復為 NULL。監控系統應自行選擇是要將此情況
表示為資料缺漏、零值，或是繼續顯示最後已知的值。

### 27.2.5. `pg_stat_replication_slots` [#](#monitoring-pg-stat-replication-slots-view) <a href="#monitoring-pg-stat-replication-slots-view" id="monitoring-pg-stat-replication-slots-view"></a>

完整內容請見 [27.2.5. pg_stat_replication_slots](monitoring-stats/monitoring-pg-stat-replication-slots-view.md#monitoring-pg-stat-replication-slots-view)。

### 27.2.6. `pg_stat_wal_receiver` [#](#monitoring-pg-stat-wal-receiver-view) <a href="#monitoring-pg-stat-wal-receiver-view" id="monitoring-pg-stat-wal-receiver-view"></a>

完整內容請見 [27.2.6. pg_stat_wal_receiver](monitoring-stats/monitoring-pg-stat-wal-receiver-view.md#monitoring-pg-stat-wal-receiver-view)。

### 27.2.7. `pg_stat_recovery_prefetch` [#](#monitoring-pg-stat-recovery-prefetch) <a href="#monitoring-pg-stat-recovery-prefetch" id="monitoring-pg-stat-recovery-prefetch"></a>

完整內容請見 [27.2.7. pg_stat_recovery_prefetch](monitoring-stats/monitoring-pg-stat-recovery-prefetch.md#monitoring-pg-stat-recovery-prefetch)。

### 27.2.8. `pg_stat_subscription` [#](#monitoring-pg-stat-subscription) <a href="#monitoring-pg-stat-subscription" id="monitoring-pg-stat-subscription"></a>

完整內容請見 [27.2.8. pg_stat_subscription](monitoring-stats/monitoring-pg-stat-subscription.md#monitoring-pg-stat-subscription)。

### 27.2.9. `pg_stat_subscription_stats` [#](#monitoring-pg-stat-subscription-stats) <a href="#monitoring-pg-stat-subscription-stats" id="monitoring-pg-stat-subscription-stats"></a>

完整內容請見 [27.2.9. pg_stat_subscription_stats](monitoring-stats/monitoring-pg-stat-subscription-stats.md#monitoring-pg-stat-subscription-stats)。

### 27.2.10. `pg_stat_ssl` [#](#monitoring-pg-stat-ssl-view) <a href="#monitoring-pg-stat-ssl-view" id="monitoring-pg-stat-ssl-view"></a>

完整內容請見 [27.2.10. pg_stat_ssl](monitoring-stats/monitoring-pg-stat-ssl-view.md#monitoring-pg-stat-ssl-view)。

### 27.2.11. `pg_stat_gssapi` [#](#monitoring-pg-stat-gssapi-view) <a href="#monitoring-pg-stat-gssapi-view" id="monitoring-pg-stat-gssapi-view"></a>

完整內容請見 [27.2.11. pg_stat_gssapi](monitoring-stats/monitoring-pg-stat-gssapi-view.md#monitoring-pg-stat-gssapi-view)。

### 27.2.12. `pg_stat_archiver` [#](#monitoring-pg-stat-archiver-view) <a href="#monitoring-pg-stat-archiver-view" id="monitoring-pg-stat-archiver-view"></a>

完整內容請見 [27.2.12. pg_stat_archiver](monitoring-stats/monitoring-pg-stat-archiver-view.md#monitoring-pg-stat-archiver-view)。

<a id="MONITORING-PG-STAT-IO-VIEW"></a>

### 27.2.13. `pg_stat_io` [#](#monitoring-pg-stat-io-view) <a href="#monitoring-pg-stat-io-view" id="monitoring-pg-stat-io-view"></a>

<a id="id-1.6.14.7.17.2"></a>

`pg_stat_io` 檢視表中，後端類型、目標 I/O 物件與 I/O
情境（context）的每種組合各會有一筆資料列，顯示叢集層級的 I/O 統計資訊。
不合理的組合會被省略。

目前，系統會追蹤關聯（例如資料表、索引）的 I/O 以及 WAL 活動。然而，
繞過共享緩衝區的關聯 I/O（例如將資料表從一個資料表空間
移至另一個資料表空間時）目前並未被追蹤。

<a id="PG-STAT-IO-VIEW"></a>

**表 27.23. `pg_stat_io` 檢視表**

<table border="1" class="table" summary="pg_stat_io 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry">
<p class="column_definition">
        欄位類型
       </p>
<p>
        說明
       </p>
</th></tr></thead><tbody><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">backend_type</code> <code class="type">text</code>
</p>
<p>
        後端的類型（例如背景工作程序、autovacuum 工作程序）。請參閱<a class="link" href="monitoring-stats.md#monitoring-pg-stat-activity-view">
<code class="structname">pg_stat_activity</code></a>，以取得有關
        <code class="varname">backend_type</code> 的更多資訊。
        某些 <code class="varname">backend_type</code>
        並不會累計 I/O 作業統計資訊，因此不會被包含於此檢視表中。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">object</code> <code class="type">text</code>
</p>
<p>
        I/O 作業的目標物件。可能的值有：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">relation</code>：永久性關聯。
         </p></li><li class="listitem"><p>
<code class="literal">temp relation</code>：暫存關聯。
         </p></li><li class="listitem"><p>
<code class="literal">wal</code>：預寫式日誌。
         </p></li></ul></div><p>
</p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">context</code> <code class="type">text</code>
</p>
<p>
        I/O 作業的情境。可能的值有：
       </p>
<div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">normal</code>：某種 I/O 作業類型的預設或標準
          <code class="varname">context</code>。舉例來說，預設情況下，
          關聯資料會被讀入共享緩衝區，並從共享緩衝區寫出。因此，這類讀入共享緩衝區及從共享緩衝區寫出的動作，會被追蹤於
          <code class="varname">context</code>
<code class="literal">normal</code> 之下。
         </p></li><li class="listitem"><p>
<code class="literal">init</code>：在建立 WAL 區段期間所執行的 I/O 作業，
          會被追蹤於 <code class="varname">context</code>
<code class="literal">init</code> 之下。
         </p></li><li class="listitem"><p>
<code class="literal">vacuum</code>：在對永久性關聯執行 vacuum 與 analyze 時，
          在共享緩衝區之外所執行的 I/O 作業。暫存資料表的 vacuum
          使用與其他暫存資料表 I/O 作業相同的本機緩衝池，
          會被追蹤於 <code class="varname">context</code>
<code class="literal">normal</code> 之下。
         </p></li><li class="listitem"><p>
<code class="literal">bulkread</code>：在共享緩衝區之外
          所執行的某些大型讀取 I/O 作業，例如對大型資料表進行
          循序掃描。
         </p></li><li class="listitem"><p>
<code class="literal">bulkwrite</code>：在共享緩衝區之外
          所執行的某些大型寫入 I/O 作業，例如 <code class="command">COPY</code>。
         </p></li></ul></div>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">reads</code> <code class="type">bigint</code>
</p>
<p>
        讀取作業的次數。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">read_bytes</code> <code class="type">numeric</code>
</p>
<p>
        讀取作業的總大小（以位元組計）。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">read_time</code> <code class="type">double precision</code>
</p>
<p>
        花費在等待讀取作業上的時間，以毫秒為單位（若啟用了
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> 且
        <code class="varname">object</code> 不是 <code class="literal">wal</code>，
        或者若啟用了 <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">track_wal_io_timing</a>
        且 <code class="varname">object</code> 為 <code class="literal">wal</code>；
        否則為零）
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">writes</code> <code class="type">bigint</code>
</p>
<p>
        寫入作業的次數。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">write_bytes</code> <code class="type">numeric</code>
</p>
<p>
        寫入作業的總大小（以位元組計）。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">write_time</code> <code class="type">double precision</code>
</p>
<p>
        花費在等待寫入作業上的時間，以毫秒為單位（若啟用了
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> 且
        <code class="varname">object</code> 不是 <code class="literal">wal</code>，
        或者若啟用了 <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">track_wal_io_timing</a>
        且 <code class="varname">object</code> 為 <code class="literal">wal</code>；
        否則為零）
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">writebacks</code> <code class="type">bigint</code>
</p>
<p>
        程序要求核心將資料寫出至永久性儲存體之
        <code class="symbol">BLCKSZ</code>（通常為 8kB）大小單位的數量。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">writeback_time</code> <code class="type">double precision</code>
</p>
<p>
        花費在等待回寫（writeback）作業上的時間，以毫秒為單位（若啟用了
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>，否則為零）。這
        包含了排入寫出要求佇列所花費的時間，並可能也包含了
        寫出髒資料所花費的時間。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">extends</code> <code class="type">bigint</code>
</p>
<p>
        關聯延伸作業的次數。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">extend_bytes</code> <code class="type">numeric</code>
</p>
<p>
        關聯延伸作業的總大小（以位元組計）。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">extend_time</code> <code class="type">double precision</code>
</p>
<p>
        花費在等待延伸作業上的時間，以毫秒為單位。（若啟用了
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> 且
        <code class="varname">object</code> 不是 <code class="literal">wal</code>，
        或者若啟用了 <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">track_wal_io_timing</a>
        且 <code class="varname">object</code> 為 <code class="literal">wal</code>；
        否則為零）
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">hits</code> <code class="type">bigint</code>
</p>
<p>
        在共享緩衝區中找到所需區塊的次數。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">evictions</code> <code class="type">bigint</code>
</p>
<p>
        為了讓緩衝區可供其他用途使用，而將其中的區塊從共享緩衝區或本機
        緩衝區中寫出的次數。
       </p>
<p>
        在 <code class="varname">context</code> <code class="literal">normal</code> 之下，此欄位計算的是
        某個區塊從緩衝區中被逐出並以另一個區塊取代的次數。在
        <code class="varname">context</code> 為
        <code class="literal">bulkwrite</code>、<code class="literal">bulkread</code> 以及
        <code class="literal">vacuum</code> 之下，此欄位計算的是某個區塊從共享緩衝區中
        被逐出，以便將該共享緩衝區加入用於大量 I/O 作業之獨立、大小受限
        環狀緩衝區（ring buffer）的次數。
        </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">reuses</code> <code class="type">bigint</code>
</p>
<p>
        在 <code class="literal">bulkread</code>、<code class="literal">bulkwrite</code> 或
        <code class="literal">vacuum</code> <code class="varname">context</code> 之下，共享緩衝區之外某個
        大小受限環狀緩衝區中既有緩衝區，作為 I/O 作業一部分而被
        重複使用的次數。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">fsyncs</code> <code class="type">bigint</code>
</p>
<p>
        <code class="literal">fsync</code> 呼叫的次數。此欄位僅於
        <code class="varname">context</code> <code class="literal">normal</code> 之下被追蹤。
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">fsync_time</code> <code class="type">double precision</code>
</p>
<p>
        花費在等待 fsync 作業上的時間，以毫秒為單位（若啟用了
        <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a> 且
        <code class="varname">object</code> 不是 <code class="literal">wal</code>，
        或者若啟用了 <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">track_wal_io_timing</a>
        且 <code class="varname">object</code> 為 <code class="literal">wal</code>；
        否則為零）
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
        這些統計資訊上次重設的時間。
       </p>
</td></tr></tbody></table>

<br>

某些後端類型永遠不會對某些 I/O 物件，及／或在某些 I/O 情境下，執行
I/O 作業。這些資料列會從檢視表中被省略。舉例來說，
檢查點程序並不會對暫存資料表執行檢查點，因此不會出現
`backend_type` 為 `checkpointer` 且
`object` 為 `temp relation` 的資料列。

此外，某些 I/O 作業永遠不會由特定後端類型，或針對特定 I/O
物件，及／或在特定 I/O 情境下執行。這些儲存格將會是 NULL。舉例來說，
暫存資料表不會被 `fsync`，因此在 `object` 為
`temp relation` 時，`fsyncs` 將為 NULL。此外，
背景寫入程序不會執行讀取作業，因此在 `backend_type` 為
`background
writer` 的資料列中，`reads` 將
為 NULL。

對於 `object` 為 `wal` 的情況，
`fsyncs` 與 `fsync_time` 所追蹤的是
在 `issue_xlog_fsync` 中對 WAL 檔案所執行的 fsync 活動。
`writes` 與 `write_time`
所追蹤的是在 `XLogWrite` 中對 WAL 檔案
所執行的寫入活動。
詳情請參閱[第 28.5 節](../wal/wal-configuration.md)。

`pg_stat_io` 可以用來作為資料庫調校的依據。
舉例來說：

* 較高的 `evictions` 計數可能表示應增加共享
  緩衝區的大小。
* 用戶端後端依賴檢查點程序來確保資料被持久化至
  永久性儲存體。若 `client backend` 出現大量
  `fsyncs`，可能表示共享緩衝區或檢查點程序的組態
  設定有誤。有關檢查點程序設定的更多資訊，請參閱[第 28.5 節](../wal/wal-configuration.md)。
* 一般而言，用戶端後端應能依賴檢查點程序與背景寫入程序等輔助
  程序來盡可能寫出髒資料。若用戶端後端出現大量
  寫入，可能表示共享緩衝區或檢查點程序的組態設定
  有誤。有關檢查點程序設定的更多資訊，請參閱[第 28.5 節](../wal/wal-configuration.md)。

### 注意

追蹤 I/O 等待時間的欄位，只有在啟用
[track_io_timing](../runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING) 時才會為非零值。若自上次
統計資訊重設以來，`track_io_timing` 並非整段時間都是啟用的，使用者在
將這些欄位與其對應 I/O 作業一併參考時應特別小心。

譯註：上述說法有例外：pg_stat_io 中 WAL 相關 I/O 的等待時間由 track_wal_io_timing 控制，因此即使未啟用 track_io_timing，這些欄位仍可能為非零值。比較 WAL 作業次數與時間時，同樣要留意 track_wal_io_timing 在統計期間是否一直啟用。

### 27.2.14. `pg_stat_bgwriter` [#](#monitoring-pg-stat-bgwriter-view) <a href="#monitoring-pg-stat-bgwriter-view" id="monitoring-pg-stat-bgwriter-view"></a>

完整內容請見 [27.2.14. pg_stat_bgwriter](monitoring-stats/monitoring-pg-stat-bgwriter-view.md#monitoring-pg-stat-bgwriter-view)。

### 27.2.15. `pg_stat_checkpointer` [#](#monitoring-pg-stat-checkpointer-view) <a href="#monitoring-pg-stat-checkpointer-view" id="monitoring-pg-stat-checkpointer-view"></a>

完整內容請見 [27.2.15. pg_stat_checkpointer](monitoring-stats/monitoring-pg-stat-checkpointer-view.md#monitoring-pg-stat-checkpointer-view)。

### 27.2.16. `pg_stat_wal` [#](#monitoring-pg-stat-wal-view) <a href="#monitoring-pg-stat-wal-view" id="monitoring-pg-stat-wal-view"></a>

完整內容請見 [27.2.16. pg_stat_wal](monitoring-stats/monitoring-pg-stat-wal-view.md#monitoring-pg-stat-wal-view)。

### 27.2.17. `pg_stat_database` [#](#monitoring-pg-stat-database-view) <a href="#monitoring-pg-stat-database-view" id="monitoring-pg-stat-database-view"></a>

完整內容請見 [27.2.17. pg_stat_database](monitoring-stats/monitoring-pg-stat-database-view.md#monitoring-pg-stat-database-view)。

### 27.2.18. `pg_stat_database_conflicts` [#](#monitoring-pg-stat-database-conflicts-view) <a href="#monitoring-pg-stat-database-conflicts-view" id="monitoring-pg-stat-database-conflicts-view"></a>

完整內容請見 [27.2.18. pg_stat_database_conflicts](monitoring-stats/monitoring-pg-stat-database-conflicts-view.md#monitoring-pg-stat-database-conflicts-view)。

### 27.2.19. `pg_stat_all_tables` [#](#monitoring-pg-stat-all-tables-view) <a href="#monitoring-pg-stat-all-tables-view" id="monitoring-pg-stat-all-tables-view"></a>

完整內容請見 [27.2.19. pg_stat_all_tables](monitoring-stats/monitoring-pg-stat-all-tables-view.md#monitoring-pg-stat-all-tables-view)。

<a id="MONITORING-PG-STAT-ALL-INDEXES-VIEW"></a>

### 27.2.20. `pg_stat_all_indexes` [#](#monitoring-pg-stat-all-indexes-view) <a href="#monitoring-pg-stat-all-indexes-view" id="monitoring-pg-stat-all-indexes-view"></a>

<a id="id-1.6.14.7.24.2"></a>

`pg_stat_all_indexes` 檢視表中，目前資料庫中的
每個索引各會有一筆資料列，
顯示有關對該特定索引存取情形的統計資訊。
`pg_stat_user_indexes` 與
`pg_stat_sys_indexes` 檢視表
包含相同的資訊，
但分別經過篩選，僅顯示使用者索引與系統索引。

<a id="PG-STAT-ALL-INDEXES-VIEW"></a>

**表 27.30. `pg_stat_all_indexes` 檢視表**

<table border="1" class="table" summary="pg_stat_all_indexes 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       此索引所屬資料表的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelid</code> <code class="type">oid</code>
</p>
<p>
       此索引的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       此索引所屬綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       此索引所屬資料表的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelname</code> <code class="type">name</code>
</p>
<p>
       此索引的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_scan</code> <code class="type">bigint</code>
</p>
<p>
       在此索引上發起的索引掃描次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_idx_scan</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此索引上最後一次掃描的時間，根據最近一次
       交易停止的時間計算
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_tup_read</code> <code class="type">bigint</code>
</p>
<p>
       此索引上掃描所回傳的索引項目數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_tup_fetch</code> <code class="type">bigint</code>
</p>
<p>
       使用此索引的簡單索引掃描所擷取的存活資料表資料列數
      </p></td></tr></tbody></table>

<br>

索引可以被簡單索引掃描、「點陣圖」索引掃描，
以及最佳化程式所使用。在點陣圖掃描中，
數個索引的輸出結果可以透過 AND 或 OR 規則加以合併，
因此在使用點陣圖掃描時，很難將個別堆積資料列的擷取
與特定索引建立關聯。因此，點陣圖
掃描會遞增其所使用（每個）索引的
`pg_stat_all_indexes`.`idx_tup_read`
計數，並且會遞增該資料表的
`pg_stat_all_tables`.`idx_tup_fetch`
計數，但不會影響
`pg_stat_all_indexes`.`idx_tup_fetch`。
最佳化程式也會存取索引，以檢查所提供的常數值是否超出最佳化程式
統計資訊所記錄的範圍，因為最佳化程式統計資訊可能已過時。

### 注意

即使完全未使用點陣圖掃描，`idx_tup_read` 與 `idx_tup_fetch`
的計數也可能不同，
這是因為 `idx_tup_read` 計算的是從索引擷取的
索引項目，而 `idx_tup_fetch` 計算的則是從資料表擷取的
存活資料列。若使用索引擷取了任何死亡或尚未提交的資料列，
或者透過僅索引掃描避免了任何堆積擷取，則後者的計數
將會較低。

### 注意

索引掃描有時每次執行可能會執行多次索引搜尋。
每次索引搜尋都會使 `pg_stat_all_indexes`.`idx_scan` 遞增，
因此索引掃描的計數有可能明顯超過
索引掃描執行器節點執行的總次數。

這種情況可能發生於使用特定 SQL 結構，
以搜尋符合多個純量值清單或陣列中任一值之資料列的查詢
（請參閱[第 9.25 節](../../the-sql-language/functions/functions-comparisons.md)）。這種情況
也可能發生於使用
`column_name =
value1 OR
column_name =
value2 ...` 結構的查詢，
不過僅限於最佳化程式將此結構轉換為
等效的多值陣列表示形式的情況。同樣地，當 B-tree 索引掃描使用
跳躍掃描（skip scan）最佳化時，每當掃描重新定位到下一個可能有相符
元組的索引葉分頁時，就會執行一次索引搜尋
（請參閱[第 11.3 節](../../the-sql-language/indexes/indexes-multicolumn.md)）。

### 提示

`EXPLAIN ANALYZE` 會輸出每個索引掃描節點所執行的
索引搜尋總次數。有關此運作方式的範例，
請參閱[第 14.1.2 節](../../the-sql-language/performance-tips/using-explain.md#using-explain-analyze)。

### 27.2.21. `pg_statio_all_tables` [#](#monitoring-pg-statio-all-tables-view) <a href="#monitoring-pg-statio-all-tables-view" id="monitoring-pg-statio-all-tables-view"></a>

完整內容請見 [27.2.21. pg_statio_all_tables](monitoring-stats/monitoring-pg-statio-all-tables-view.md#monitoring-pg-statio-all-tables-view)。

### 27.2.22. `pg_statio_all_indexes` [#](#monitoring-pg-statio-all-indexes-view) <a href="#monitoring-pg-statio-all-indexes-view" id="monitoring-pg-statio-all-indexes-view"></a>

完整內容請見 [27.2.22. pg_statio_all_indexes](monitoring-stats/monitoring-pg-statio-all-indexes-view.md#monitoring-pg-statio-all-indexes-view)。

### 27.2.23. `pg_statio_all_sequences` [#](#monitoring-pg-statio-all-sequences-view) <a href="#monitoring-pg-statio-all-sequences-view" id="monitoring-pg-statio-all-sequences-view"></a>

完整內容請見 [27.2.23. pg_statio_all_sequences](monitoring-stats/monitoring-pg-statio-all-sequences-view.md#monitoring-pg-statio-all-sequences-view)。

### 27.2.24. `pg_stat_user_functions` [#](#monitoring-pg-stat-user-functions-view) <a href="#monitoring-pg-stat-user-functions-view" id="monitoring-pg-stat-user-functions-view"></a>

完整內容請見 [27.2.24. pg_stat_user_functions](monitoring-stats/monitoring-pg-stat-user-functions-view.md#monitoring-pg-stat-user-functions-view)。

### 27.2.25. `pg_stat_slru` [#](#monitoring-pg-stat-slru-view) <a href="#monitoring-pg-stat-slru-view" id="monitoring-pg-stat-slru-view"></a>

完整內容請見 [27.2.25. pg_stat_slru](monitoring-stats/monitoring-pg-stat-slru-view.md#monitoring-pg-stat-slru-view)。

<a id="MONITORING-STATS-FUNCTIONS"></a>

### 27.2.26. 統計函式 [#](#monitoring-stats-functions) <a href="#monitoring-stats-functions" id="monitoring-stats-functions"></a>

透過撰寫使用上述標準檢視表所使用之相同底層統計資訊存取函式的查詢，
也可以建立其他檢視統計資訊的方式。有關函式名稱等
詳情，請參閱標準檢視表的定義。（舉例來說，
在 psql 中你可以下達 `\d+ pg_stat_activity`。）
每個資料庫統計資訊的存取函式，會以資料庫 OID 作為
引數，以識別要回報哪個資料庫。
每個資料表與每個索引的函式，則會以資料表或索引 OID 作為引數。
每個函式統計資訊的函式，會以函式 OID 作為引數。
請注意，使用這些函式只能看到目前資料庫中的
資料表、索引與函式。

有關累計統計系統的其他函式，列於
[表 27.36](monitoring-stats.md#MONITORING-STATS-FUNCS-TABLE)中。

<a id="MONITORING-STATS-FUNCS-TABLE"></a>

**表 27.36. 其他統計函式**

<table border="1" class="table" summary="其他統計函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">pg_backend_pid</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳附加至目前工作階段之伺服器程序的
        程序 ID。
       </p></td></tr><tr><td class="func_table_entry" id="PG-STAT-GET-BACKEND-IO"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.2.1.1.1"></a>
<code class="function">pg_stat_get_backend_io</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        回傳指定程序 ID 之後端的 I/O
        統計資訊。輸出欄位與
        <code class="structname">pg_stat_io</code> 檢視表中的欄位完全相同。
       </p>
<p>
        此函式並不會回傳檢查點程序、
        背景寫入程序、啟動程序以及 autovacuum 啟動程序的 I/O 統計資訊，
        因為這些程序的統計資訊已顯示於 <code class="structname">pg_stat_io</code>
        檢視表中，且每一種各只有一個。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.3.1.1.1"></a>
<code class="function">pg_stat_get_activity</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        回傳有關指定程序 ID 之後端的一筆資訊記錄；若指定
        <code class="literal">NULL</code>，則回傳系統中每個活躍後端各一筆記錄。
        所回傳的欄位是
        <code class="structname">pg_stat_activity</code> 檢視表中欄位的子集合。
       </p></td></tr><tr><td class="func_table_entry" id="PG-STAT-GET-BACKEND-WAL"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.4.1.1.1"></a>
<code class="function">pg_stat_get_backend_wal</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
</p>
<p>
        回傳指定程序 ID 之後端的 WAL
        統計資訊。輸出欄位與
        <code class="structname">pg_stat_wal</code> 檢視表中的欄位完全相同。
       </p>
<p>
        此函式並不會回傳檢查點程序、
        背景寫入程序、啟動程序以及 autovacuum 啟動程序的 WAL 統計資訊。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.5.1.1.1"></a>
<code class="function">pg_stat_get_snapshot_timestamp</code> ()
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        回傳目前統計資訊快照的時間戳記；若尚未擷取任何
        統計資訊快照，則為 NULL。若
        <code class="varname">stats_fetch_consistency</code> 設為
        <code class="literal">snapshot</code>，則在某筆交易中首次
        存取累計統計資訊時，就會擷取快照
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.6.1.1.1"></a>
<code class="function">pg_stat_get_xact_blocks_fetched</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        回傳目前交易中，針對資料表或索引的區塊讀取
        要求次數。此數值減去
        <code class="function">pg_stat_get_xact_blocks_hit</code> 即為核心
        <code class="function">read()</code> 呼叫的次數；由於核心層級的緩衝，
        實際的實體讀取次數通常會較低。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.7.1.1.1"></a>
<code class="function">pg_stat_get_xact_blocks_hit</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        回傳目前交易中，針對資料表或索引的區塊讀取
        要求中，在快取中找到（未觸發核心
        <code class="function">read()</code> 呼叫）的次數。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.8.1.1.1"></a>
<code class="function">pg_stat_clear_snapshot</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        捨棄目前的統計資訊快照或快取的資訊。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.9.1.1.1"></a>
<code class="function">pg_stat_reset</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        將目前資料庫的所有統計計數器重設為零。
       </p>
<p>
        此函式預設僅限超級使用者使用，但可以將 EXECUTE 權限
        授予其他使用者以執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.10.1.1.1"></a>
<code class="function">pg_stat_reset_shared</code> ( [ <em class="parameter"><code>target</code></em> <code class="type">text</code> <code class="literal">DEFAULT</code> <code class="literal">NULL</code> ] )
        → <code class="returnvalue">void</code>
</p>
<p>
        依據引數，將部分叢集層級的統計計數器重設為零。
        <em class="parameter"><code>target</code></em> 可以是：
       </p><div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
<code class="literal">archiver</code>：重設
          <code class="structname">pg_stat_archiver</code> 檢視表中所顯示的所有計數器。
         </p></li><li class="listitem"><p>
<code class="literal">bgwriter</code>：重設
           <code class="structname">pg_stat_bgwriter</code> 檢視表中所顯示的所有計數器。
         </p></li><li class="listitem"><p>
<code class="literal">checkpointer</code>：重設
          <code class="structname">pg_stat_checkpointer</code> 檢視表中所顯示的所有計數器。
         </p></li><li class="listitem"><p>
<code class="literal">io</code>：重設
          <code class="structname">pg_stat_io</code> 檢視表中所顯示的所有計數器。
         </p></li><li class="listitem"><p>
<code class="literal">recovery_prefetch</code>：重設
          <code class="structname">pg_stat_recovery_prefetch</code> 檢視表中所顯示的所有計數器。
         </p></li><li class="listitem"><p>
<code class="literal">slru</code>：重設
          <code class="structname">pg_stat_slru</code> 檢視表中所顯示的所有計數器。
         </p></li><li class="listitem"><p>
<code class="literal">wal</code>：重設
          <code class="structname">pg_stat_wal</code> 檢視表中所顯示的所有計數器。
         </p></li><li class="listitem"><p>
<code class="literal">NULL</code> 或未指定：重設上述所有
          檢視表中的所有計數器。
         </p></li></ul></div><p>
</p>
<p>
        此函式預設僅限超級使用者使用，但可以將 EXECUTE 權限
        授予其他使用者以執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.11.1.1.1"></a>
<code class="function">pg_stat_reset_single_table_counters</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        將目前資料庫中或整個叢集所有資料庫共享的單一
        資料表或索引的統計資訊重設為零。
       </p>
<p>
        此函式預設僅限超級使用者使用，但可以將 EXECUTE 權限
        授予其他使用者以執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.12.1.1.1"></a>
<code class="function">pg_stat_reset_backend_stats</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        將指定程序 ID 之單一後端的統計資訊
        重設為零。
       </p>
<p>
        此函式預設僅限超級使用者使用，但可以將 EXECUTE 權限
        授予其他使用者以執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.13.1.1.1"></a>
<code class="function">pg_stat_reset_single_function_counters</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        將目前資料庫中單一函式的統計資訊重設為
        零。
       </p>
<p>
        此函式預設僅限超級使用者使用，但可以將 EXECUTE 權限
        授予其他使用者以執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.14.1.1.1"></a>
<code class="function">pg_stat_reset_slru</code> ( [ <em class="parameter"><code>target</code></em> <code class="type">text</code> <code class="literal">DEFAULT</code> <code class="literal">NULL</code> ] )
        → <code class="returnvalue">void</code>
</p>
<p>
        將單一 SLRU 快取，或叢集中所有 SLRU 的統計資訊重設為零。
        若 <em class="parameter"><code>target</code></em> 為
        <code class="literal">NULL</code> 或未指定，則會重設
        <code class="structname">pg_stat_slru</code> 檢視表中所有 SLRU 快取所顯示的所有計數器。
        此引數可以是
        <code class="literal">commit_timestamp</code>、
        <code class="literal">multixact_member</code>、
        <code class="literal">multixact_offset</code>、
        <code class="literal">notify</code>、
        <code class="literal">serializable</code>、
        <code class="literal">subtransaction</code> 或
        <code class="literal">transaction</code> 之一，
        以僅重設該項目的計數器。
        若引數為 <code class="literal">other</code>（或者其實是任何
        無法識別的名稱），則會重設所有其他 SLRU 快取（例如擴充功能
        自訂快取）的計數器。
       </p>
<p>
        此函式預設僅限超級使用者使用，但可以將 EXECUTE 權限
        授予其他使用者以執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.15.1.1.1"></a>
<code class="function">pg_stat_reset_replication_slot</code> ( <code class="type">text</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        重設由引數所指定複寫插槽的統計資訊。若
        引數為 <code class="literal">NULL</code>，則重設所有
        複寫插槽的統計資訊。
       </p>
<p>
         此函式預設僅限超級使用者使用，但可以將 EXECUTE 權限
         授予其他使用者以執行此函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.4.2.2.16.1.1.1"></a>
<code class="function">pg_stat_reset_subscription_stats</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        將 <code class="structname">pg_stat_subscription_stats</code> 檢視表中所顯示
        單一訂閱的統計資訊重設為零。若
        引數為 <code class="literal">NULL</code>，則重設所有
        訂閱的統計資訊。
       </p>
<p>
        此函式預設僅限超級使用者使用，但可以將 EXECUTE 權限
        授予其他使用者以執行此函式。
       </p></td></tr></tbody></table>

<br>

### 警告

使用 `pg_stat_reset()` 也會重設 autovacuum
用來判斷何時觸發 vacuum 或 analyze 的計數器。
重設這些計數器可能導致 autovacuum 無法執行必要
的工作，進而可能導致資料表膨脹或資料表統計資訊
過時等問題。建議在重設統計資訊之後執行一次
全資料庫範圍的 `ANALYZE`。

`pg_stat_get_activity` 是
`pg_stat_activity` 檢視表的底層函式，會回傳一組
包含每個後端程序所有可用資訊的記錄。
有時候，僅取得這些資訊的一部分可能較為方便。
在這種情況下，可以使用另一組逐後端統計資訊
存取函式；這些函式列於[表 27.37](monitoring-stats.md#MONITORING-STATS-BACKEND-FUNCS-TABLE)中。
這些存取函式使用的是工作階段的後端 ID 編號，這是一個
小型整數（>= 0），與任何並行工作階段的後端 ID 不同，
不過某個工作階段結束後，其 ID 可能會立即被回收再利用。
後端 ID 除了其他用途外，也用於識別
該工作階段的暫存綱要（如果有的話）。
`pg_stat_get_backend_idset` 函式提供了一種
方便的方式，可以列出所有活躍後端的 ID 編號，
以便呼叫這些函式。舉例來說，若要顯示所有後端的 PID 與
目前查詢：

```

SELECT pg_stat_get_backend_pid(backendid) AS pid,
       pg_stat_get_backend_activity(backendid) AS query
FROM pg_stat_get_backend_idset() AS backendid;
```

<a id="MONITORING-STATS-BACKEND-FUNCS-TABLE"></a>

**表 27.37. 逐後端統計函式**

<table border="1" class="table" summary="逐後端統計函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.1.1.1.1"></a>
<code class="function">pg_stat_get_backend_activity</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳此後端最近一次查詢的文字內容。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.2.1.1.1"></a>
<code class="function">pg_stat_get_backend_activity_start</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        回傳此後端最近一次查詢開始的時間。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.3.1.1.1"></a>
<code class="function">pg_stat_get_backend_client_addr</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        回傳連線至此後端之用戶端的 IP 位址。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.4.1.1.1"></a>
<code class="function">pg_stat_get_backend_client_port</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳用戶端用於通訊的 TCP 埠號。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.5.1.1.1"></a>
<code class="function">pg_stat_get_backend_dbid</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        回傳此後端所連線資料庫的 OID。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.6.1.1.1"></a>
<code class="function">pg_stat_get_backend_idset</code> ()
        → <code class="returnvalue">setof integer</code>
</p>
<p>
        回傳目前所有活躍後端 ID 編號所組成的集合。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.7.1.1.1"></a>
<code class="function">pg_stat_get_backend_pid</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳此後端的程序 ID。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.8.1.1.1"></a>
<code class="function">pg_stat_get_backend_start</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        回傳此程序啟動的時間。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.9.1.1.1"></a>
<code class="function">pg_stat_get_backend_subxact</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
</p>
<p>
        回傳有關指定 ID 之後端子交易的一筆
        資訊記錄。
        所回傳的欄位有 <em class="parameter"><code>subxact_count</code></em>（此後端
        子交易快取中的子交易數量），
        以及 <em class="parameter"><code>subxact_overflow</code></em>（表示
        此後端的子交易快取是否已溢位）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.10.1.1.1"></a>
<code class="function">pg_stat_get_backend_userid</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        回傳登入此後端之使用者的 OID。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.11.1.1.1"></a>
<code class="function">pg_stat_get_backend_wait_event</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        若此後端目前正在等待，則回傳等待事件名稱；
        否則為 NULL。請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-ACTIVITY-TABLE">表 27.5</a>至
        <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TIMEOUT-TABLE">表 27.13</a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.12.1.1.1"></a>
<code class="function">pg_stat_get_backend_wait_event_type</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        若此後端目前正在等待，則回傳等待事件類型名稱；
        否則為 NULL。詳情請參閱<a class="xref" href="monitoring-stats.md#WAIT-EVENT-TABLE">表 27.4</a>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.6.14.7.30.7.2.2.13.1.1.1"></a>
<code class="function">pg_stat_get_backend_xact_start</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        回傳此後端目前交易開始的時間。
       </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
