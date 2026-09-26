<a id="PROGRESS-REPORTING"></a>

## 27.4. 進度回報 [#](#PROGRESS-REPORTING)

[27.4.1. ANALYZE 進度回報](progress-reporting.md#ANALYZE-PROGRESS-REPORTING)

[27.4.2. CLUSTER 進度回報](progress-reporting.md#CLUSTER-PROGRESS-REPORTING)

[27.4.3. COPY 進度回報](progress-reporting.md#COPY-PROGRESS-REPORTING)

[27.4.4. CREATE INDEX 進度回報](progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING)

[27.4.5. VACUUM 進度回報](progress-reporting.md#VACUUM-PROGRESS-REPORTING)

[27.4.6. 基礎備份進度回報](progress-reporting.md#BASEBACKUP-PROGRESS-REPORTING)

PostgreSQL 具備在命令執行期間，
回報特定命令執行進度的能力。目前支援進度回報的命令，
僅有 `ANALYZE`、
`CLUSTER`、
`CREATE INDEX`、`VACUUM`、
`COPY`，
以及 [BASE_BACKUP](../../internals/protocol/protocol-replication.md#PROTOCOL-REPLICATION-BASE-BACKUP)
（也就是 [pg_basebackup](../../reference/reference-client/app-pgbasebackup.md)
用來取得基礎備份時所發出的複寫命令）。
未來可能會擴充支援的命令範圍。

<a id="ANALYZE-PROGRESS-REPORTING"></a>

### 27.4.1. ANALYZE 進度回報 [#](#ANALYZE-PROGRESS-REPORTING)

<a id="id-1.6.14.9.3.2"></a>

每當 `ANALYZE` 正在執行時，
`pg_stat_progress_analyze` 檢視表中，
就會針對每個目前正在執行此命令的後端，各含有一列。
下方的表格，說明了會被回報的資訊，
並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-ANALYZE-VIEW"></a>

**表 27.38. `pg_stat_progress_analyze` 檢視表**

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
       目前的處理階段。請參閱<a class="xref" href="progress-reporting.md#ANALYZE-PHASES">表 27.39</a>。
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
       <a class="xref" href="../runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST">19.10.2 節</a>）
       而耗費在休眠上的總時間，以毫秒為單位
       （若已啟用 <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING">track_cost_delay_timing</a>，
       否則為零）。
      </p></td></tr></tbody></table>

<br><a id="ANALYZE-PHASES"></a>

**表 27.39. ANALYZE 各階段**

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

<a id="CLUSTER-PROGRESS-REPORTING"></a>

### 27.4.2. CLUSTER 進度回報 [#](#CLUSTER-PROGRESS-REPORTING)

<a id="id-1.6.14.9.4.2"></a>

每當 `CLUSTER` 或 `VACUUM FULL`
正在執行時，`pg_stat_progress_cluster`
檢視表中，就會針對每個目前正在執行其中一項命令的後端，
各含有一列。下方的表格，
說明了會被回報的資訊，並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-CLUSTER-VIEW"></a>

**表 27.40. `pg_stat_progress_cluster` 檢視表**

<table border="1" class="table" summary="pg_stat_progress_cluster View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       後端的程序 ID。
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
       正在被重整（cluster）之資料表的 OID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">command</code> <code class="type">text</code>
</p>
<p>
       目前正在執行的命令。可能是 <code class="literal">CLUSTER</code>
       或 <code class="literal">VACUUM FULL</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       目前的處理階段。請參閱<a class="xref" href="progress-reporting.md#CLUSTER-PHASES">表 27.41</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">cluster_index_relid</code> <code class="type">oid</code>
</p>
<p>
       若此資料表正在使用索引進行掃描，
       此欄位即為所使用索引的 OID；否則為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_tuples_scanned</code> <code class="type">bigint</code>
</p>
<p>
       已掃描的堆積資料列數量。
       此計數器只會在階段為
       <code class="literal">seq scanning heap</code>、
       <code class="literal">index scanning heap</code>
       或 <code class="literal">writing new heap</code> 時才會前進。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_tuples_written</code> <code class="type">bigint</code>
</p>
<p>
       已寫入的堆積資料列數量。
       此計數器只會在階段為
       <code class="literal">seq scanning heap</code>、
       <code class="literal">index scanning heap</code>
       或 <code class="literal">writing new heap</code> 時才會前進。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_total</code> <code class="type">bigint</code>
</p>
<p>
       該資料表中堆積區塊的總數。此數字是在
       <code class="literal">seq scanning heap</code> 開始時所回報的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_scanned</code> <code class="type">bigint</code>
</p>
<p>
       已掃描的堆積區塊數。此計數器只會在
       階段為 <code class="literal">seq scanning heap</code>
       時才會前進。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">index_rebuild_count</code> <code class="type">bigint</code>
</p>
<p>
       已重建的索引數量。此計數器只會在
       階段為 <code class="literal">rebuilding index</code>
       時才會前進。
      </p></td></tr></tbody></table>

<br><a id="CLUSTER-PHASES"></a>

**表 27.41. CLUSTER 與 VACUUM FULL 各階段**

<table border="1" class="table" summary="CLUSTER and VACUUM FULL Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>階段</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
       此命令正在準備開始掃描堆積。預期此階段
       耗時應非常短暫。
     </td></tr><tr><td><code class="literal">seq scanning heap</code></td><td>
       此命令目前正在使用循序掃描來掃描資料表。
     </td></tr><tr><td><code class="literal">index scanning heap</code></td><td>
<code class="command">CLUSTER</code> 目前正在使用索引掃描來掃描資料表。
     </td></tr><tr><td><code class="literal">sorting tuples</code></td><td>
<code class="command">CLUSTER</code> 目前正在排序資料列。
     </td></tr><tr><td><code class="literal">writing new heap</code></td><td>
<code class="command">CLUSTER</code> 目前正在寫入新的堆積。
     </td></tr><tr><td><code class="literal">swapping relation files</code></td><td>
       此命令目前正在將新建置的檔案，
       替換到位。
     </td></tr><tr><td><code class="literal">rebuilding index</code></td><td>
       此命令目前正在重建某個索引。
     </td></tr><tr><td><code class="literal">performing final cleanup</code></td><td>
       此命令正在執行最終清理。此階段完成後，
       <code class="command">CLUSTER</code>
       或 <code class="command">VACUUM FULL</code> 就會結束。
     </td></tr></tbody></table>

<br>

<a id="COPY-PROGRESS-REPORTING"></a>

### 27.4.3. COPY 進度回報 [#](#COPY-PROGRESS-REPORTING)

<a id="id-1.6.14.9.5.2"></a>

每當 `COPY` 正在執行時，
`pg_stat_progress_copy` 檢視表中，
就會針對每個目前正在執行 `COPY` 命令的後端，
各含有一列。下方的表格，
說明了會被回報的資訊，並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-COPY-VIEW"></a>

**表 27.42. `pg_stat_progress_copy` 檢視表**

<table border="1" class="table" summary="pg_stat_progress_copy View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
       正在對其執行 <code class="command">COPY</code> 命令之資料表的
       OID。此值設為 <code class="literal">0</code>，適用於複製來源為
       <code class="command">SELECT</code> 查詢的情況。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">command</code> <code class="type">text</code>
</p>
<p>
       目前正在執行的命令：<code class="literal">COPY FROM</code>，
       或 <code class="literal">COPY TO</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type</code> <code class="type">text</code>
</p>
<p>
       讀取或寫入資料所使用的 I/O 類型：
       <code class="literal">FILE</code>、<code class="literal">PROGRAM</code>、
       <code class="literal">PIPE</code>（用於 <code class="command">COPY FROM STDIN</code> 與
       <code class="command">COPY TO STDOUT</code>），
       或 <code class="literal">CALLBACK</code>
       （例如用於邏輯複寫中初始資料表同步時）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bytes_processed</code> <code class="type">bigint</code>
</p>
<p>
       <code class="command">COPY</code> 命令已處理的位元組數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bytes_total</code> <code class="type">bigint</code>
</p>
<p>
       <code class="command">COPY FROM</code> 命令來源檔案的大小，
       以位元組表示。若無法取得，則設為
       <code class="literal">0</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_processed</code> <code class="type">bigint</code>
</p>
<p>
       <code class="command">COPY</code> 命令已處理的資料列數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_excluded</code> <code class="type">bigint</code>
</p>
<p>
       因被 <code class="command">WHERE</code> 子句（此子句屬於
       <code class="command">COPY</code> 命令）排除，而未被處理的
       資料列數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_skipped</code> <code class="type">bigint</code>
</p>
<p>
       因含有格式錯誤的資料而被略過的資料列數量。
       此計數器只會在
       非 <code class="literal">stop</code> 的值被指定給
       <code class="literal">ON_ERROR</code> 選項時才會前進。
      </p></td></tr></tbody></table>

<br>

<a id="CREATE-INDEX-PROGRESS-REPORTING"></a>

### 27.4.4. CREATE INDEX 進度回報 [#](#CREATE-INDEX-PROGRESS-REPORTING)

<a id="id-1.6.14.9.6.2"></a>

每當 `CREATE INDEX` 或 `REINDEX`
正在執行時，`pg_stat_progress_create_index`
檢視表中，就會針對每個目前正在建立索引的後端，
各含有一列。下方的表格，
說明了會被回報的資訊，並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-CREATE-INDEX-VIEW"></a>

**表 27.43. `pg_stat_progress_create_index` 檢視表**

<table border="1" class="table" summary="pg_stat_progress_create_index View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       正在建立索引之後端的程序 ID。
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
       正在為其建立索引之資料表的 OID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">index_relid</code> <code class="type">oid</code>
</p>
<p>
       正在建立或重建之索引的 OID。在非並行的
       <code class="command">CREATE INDEX</code> 期間，此值為 0。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">command</code> <code class="type">text</code>
</p>
<p>
       具體的命令類型：<code class="literal">CREATE INDEX</code>、
       <code class="literal">CREATE INDEX CONCURRENTLY</code>、
       <code class="literal">REINDEX</code>，
       或 <code class="literal">REINDEX CONCURRENTLY</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       目前建立索引的處理階段。請參閱<a class="xref" href="progress-reporting.md#CREATE-INDEX-PHASES">表 27.44</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lockers_total</code> <code class="type">bigint</code>
</p>
<p>
       在適用情況下，需要等待的鎖定持有者總數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">lockers_done</code> <code class="type">bigint</code>
</p>
<p>
       已等待完成的鎖定持有者數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">current_locker_pid</code> <code class="type">bigint</code>
</p>
<p>
       目前正在等待之鎖定持有者的程序 ID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blocks_total</code> <code class="type">bigint</code>
</p>
<p>
       目前階段中要處理的區塊總數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blocks_done</code> <code class="type">bigint</code>
</p>
<p>
       目前階段中已處理的區塊數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_total</code> <code class="type">bigint</code>
</p>
<p>
       目前階段中要處理的資料列總數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_done</code> <code class="type">bigint</code>
</p>
<p>
       目前階段中已處理的資料列數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partitions_total</code> <code class="type">bigint</code>
</p>
<p>
       要為其建立或附加索引的分割區總數，
       包含直接與間接的分割區。此值為 <code class="literal">0</code> 的情況，
       是在進行 <code class="literal">REINDEX</code>
       期間，或該索引未分割時。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">partitions_done</code> <code class="type">bigint</code>
</p>
<p>
       已為其建立或附加索引的分割區數量，
       包含直接與間接的分割區。此值為 <code class="literal">0</code> 的情況，
       是在進行 <code class="literal">REINDEX</code>
       期間，或該索引未分割時。
      </p></td></tr></tbody></table>

<br><a id="CREATE-INDEX-PHASES"></a>

**表 27.44. CREATE INDEX 各階段**

<table border="1" class="table" summary="CREATE INDEX Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>階段</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
<code class="command">CREATE INDEX</code> 或 <code class="command">REINDEX</code>
       正在準備建立索引。預期此階段耗時應非常短暫。
      </td></tr><tr><td><code class="literal">waiting for writers before build</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code> 或
       <code class="command">REINDEX CONCURRENTLY</code>，
       正在等待可能看得到該資料表、且持有寫入鎖定的交易結束。此階段在非並行模式下會被跳過。
       欄位 <code class="structname">lockers_total</code>、
       <code class="structname">lockers_done</code>
       與 <code class="structname">current_locker_pid</code>，
       含有此階段的進度資訊。
      </td></tr><tr><td><code class="literal">building index</code></td><td>
       正在由存取方法特有的程式碼建立索引。
       在此階段中，支援進度回報的存取方法，
       會填入自己的進度資料，
       並在此欄位中標示子階段。一般而言，
       <code class="structname">blocks_total</code>
       與 <code class="structname">blocks_done</code>，
       將含有進度資料，也可能包含
       <code class="structname">tuples_total</code>
       與 <code class="structname">tuples_done</code>。
      </td></tr><tr><td><code class="literal">waiting for writers before validation</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code> 或
       <code class="command">REINDEX CONCURRENTLY</code>，
       正在等待可能會寫入該資料表、且持有寫入鎖定的交易結束。此階段在非並行模式下會被跳過。
       欄位 <code class="structname">lockers_total</code>、
       <code class="structname">lockers_done</code>
       與 <code class="structname">current_locker_pid</code>，
       含有此階段的進度資訊。
      </td></tr><tr><td><code class="literal">index validation: scanning index</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code>
       正在掃描該索引，尋找需要被驗證的 資料列。
       此階段在非並行模式下會被跳過。
       欄位 <code class="structname">blocks_total</code>
       （設為該索引的總大小）與
       <code class="structname">blocks_done</code>，
       含有此階段的進度資訊。
      </td></tr><tr><td><code class="literal">index validation: sorting tuples</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code>
       正在排序索引掃描階段的輸出結果。
      </td></tr><tr><td><code class="literal">index validation: scanning table</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code>
       正在掃描該資料表，
       以驗證前兩個階段所蒐集到的索引 資料列。
       此階段在非並行模式下會被跳過。
       欄位 <code class="structname">blocks_total</code>
       （設為該資料表的總大小）與
       <code class="structname">blocks_done</code>，
       含有此階段的進度資訊。
      </td></tr><tr><td><code class="literal">waiting for old snapshots</code></td><td>
<code class="command">CREATE INDEX CONCURRENTLY</code> 或
       <code class="command">REINDEX CONCURRENTLY</code>，
       正在等待可能看得到該資料表的交易，
       釋出其快照。此階段在非並行模式下會被跳過。
       欄位 <code class="structname">lockers_total</code>、
       <code class="structname">lockers_done</code>
       與 <code class="structname">current_locker_pid</code>，
       含有此階段的進度資訊。
      </td></tr><tr><td><code class="literal">waiting for readers before marking dead</code></td><td>
<code class="command">REINDEX CONCURRENTLY</code>，
       正在等待對該資料表持有讀取鎖定的交易結束，
       才將舊索引標示為失效（dead）。
       此階段在非並行模式下會被跳過。
       欄位 <code class="structname">lockers_total</code>、
       <code class="structname">lockers_done</code>
       與 <code class="structname">current_locker_pid</code>，
       含有此階段的進度資訊。
      </td></tr><tr><td><code class="literal">waiting for readers before dropping</code></td><td>
<code class="command">REINDEX CONCURRENTLY</code>，
       正在等待對該資料表持有讀取鎖定的交易結束，
       才捨棄舊索引。
       此階段在非並行模式下會被跳過。
       欄位 <code class="structname">lockers_total</code>、
       <code class="structname">lockers_done</code>
       與 <code class="structname">current_locker_pid</code>，
       含有此階段的進度資訊。
      </td></tr></tbody></table>

<br>

<a id="VACUUM-PROGRESS-REPORTING"></a>

### 27.4.5. VACUUM 進度回報 [#](#VACUUM-PROGRESS-REPORTING)

<a id="id-1.6.14.9.7.2"></a>

每當 `VACUUM` 正在執行時，
`pg_stat_progress_vacuum` 檢視表中，
就會針對每個目前正在執行清理（vacuum）的後端
（包括自動 vacuum 工作程序），各含有一列。
下方的表格，說明了會被回報的資訊，
並提供如何解讀這些資訊的說明。
`VACUUM FULL` 命令的進度，
是透過 `pg_stat_progress_cluster`
回報的，因為 `VACUUM FULL` 與
`CLUSTER` 都會重寫資料表，
而一般的 `VACUUM` 則只會就地修改資料表。
請參閱 [27.4.2 節](progress-reporting.md#CLUSTER-PROGRESS-REPORTING)。

<a id="PG-STAT-PROGRESS-VACUUM-VIEW"></a>

**表 27.45. `pg_stat_progress_vacuum` 檢視表**

<table border="1" class="table" summary="pg_stat_progress_vacuum View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       後端的程序 ID。
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
       正在被清理之資料表的 OID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       目前清理的處理階段。請參閱<a class="xref" href="progress-reporting.md#VACUUM-PHASES">表 27.46</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_total</code> <code class="type">bigint</code>
</p>
<p>
       該資料表中堆積區塊的總數。此數字是在
       掃描開始時所回報的；之後新增的區塊，
       不會（也不需要）被本次 <code class="command">VACUUM</code> 造訪。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_scanned</code> <code class="type">bigint</code>
</p>
<p>
       已掃描的堆積區塊數。由於
       <a class="link" href="../../internals/storage/storage-vm.md">能見度映射（visibility map）</a>
       被用來最佳化掃描，有些區塊會被跳過而不進行檢查；
       這些被跳過的區塊，也計入此總數中，
       因此當清理完成時，此數字最終會等於
       <code class="structfield">heap_blks_total</code>。
       此計數器只會在階段為 <code class="literal">scanning heap</code>
       時才會前進。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_vacuumed</code> <code class="type">bigint</code>
</p>
<p>
       已清理的堆積區塊數。除非該資料表沒有索引，
       否則此計數器只會在階段為
       <code class="literal">vacuuming heap</code> 時才會前進。
       不含死亡資料列的區塊會被跳過，
       因此此計數器有時可能會以大幅度往前跳。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">index_vacuum_count</code> <code class="type">bigint</code>
</p>
<p>
       已完成的索引清理循環次數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_dead_tuple_bytes</code> <code class="type">bigint</code>
</p>
<p>
       依據
       <a class="xref" href="../runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM">maintenance_work_mem</a>，
       在需要執行索引清理循環之前，
       我們能夠儲存的死亡資料列資料量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dead_tuple_bytes</code> <code class="type">bigint</code>
</p>
<p>
       自上次索引清理循環以來，
       所蒐集到的死亡資料列資料量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">num_dead_item_ids</code> <code class="type">bigint</code>
</p>
<p>
       自上次索引清理循環以來，
       所蒐集到的死亡項目識別碼數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexes_total</code> <code class="type">bigint</code>
</p>
<p>
       將被清理（vacuum）或清除（clean up）的索引總數。此數字是在
       <code class="literal">vacuuming indexes</code> 階段，
       或 <code class="literal">cleaning up indexes</code>
       階段開始時回報的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexes_processed</code> <code class="type">bigint</code>
</p>
<p>
       已處理的索引數量。此計數器只會在
       階段為 <code class="literal">vacuuming indexes</code>
       或 <code class="literal">cleaning up indexes</code>
       時才會前進。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">delay_time</code> <code class="type">double precision</code>
</p>
<p>
       因基於成本的延遲（請參閱
       <a class="xref" href="../runtime-config/runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST">19.10.2 節</a>）
       而耗費在休眠上的總時間，以毫秒為單位
       （若已啟用 <a class="xref" href="../runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING">track_cost_delay_timing</a>，
       否則為零）。這包括任何相關聯的平行工作者
       休眠的時間。然而，平行工作者回報其休眠時間的頻率
       最多為每秒一次，因此所回報的值，
       可能會略微過時。
      </p></td></tr></tbody></table>

<br><a id="VACUUM-PHASES"></a>

**表 27.46. VACUUM 各階段**

<table border="1" class="table" summary="VACUUM Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>階段</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
<code class="command">VACUUM</code>
       正在準備開始掃描堆積。預期此階段
       耗時應非常短暫。
     </td></tr><tr><td><code class="literal">scanning heap</code></td><td>
<code class="command">VACUUM</code>
       目前正在掃描堆積。若有需要，它會對每個頁面進行
       修剪與重組，並可能執行凍結作業。
       <code class="structfield">heap_blks_scanned</code> 欄位，
       可用來監控此次掃描的進度。
     </td></tr><tr><td><code class="literal">vacuuming indexes</code></td><td>
<code class="command">VACUUM</code>
       目前正在清理索引。若某個資料表含有
       任何索引，此動作在堆積完全掃描完成後，
       每次清理至少會發生一次。若
       <a class="xref" href="../runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM">maintenance_work_mem</a>
       （或在自動 vacuum 的情況下，
       若有設定
       <a class="xref" href="../runtime-config/runtime-config-resource.md#GUC-AUTOVACUUM-WORK-MEM">autovacuum_work_mem</a>）
       不足以儲存所找到的死亡資料列數量，
       則此動作每次清理可能會發生多次。
     </td></tr><tr><td><code class="literal">vacuuming heap</code></td><td>
<code class="command">VACUUM</code>
       目前正在清理堆積。清理堆積
       與掃描堆積不同，會在每次清理索引之後發生。
       若 <code class="structfield">heap_blks_scanned</code>
       小於 <code class="structfield">heap_blks_total</code>，
       此階段完成後，系統就會回到掃描堆積；
       否則，此階段完成後，
       系統就會開始清除索引。
     </td></tr><tr><td><code class="literal">cleaning up indexes</code></td><td>
<code class="command">VACUUM</code>
       目前正在清除索引。這會在堆積已完全掃描完成，
       且索引與堆積的所有清理動作都已完成後發生。
     </td></tr><tr><td><code class="literal">truncating heap</code></td><td>
<code class="command">VACUUM</code>
       目前正在截斷堆積，
       以將該關聯結尾的空白頁面，交還給作業系統。
       這會在清理索引之後發生。
     </td></tr><tr><td><code class="literal">performing final cleanup</code></td><td>
<code class="command">VACUUM</code>
       正在執行最終清理。在此階段期間，
       <code class="command">VACUUM</code> 會清理可用空間對應表（free space map）、
       更新 <code class="literal">pg_class</code> 中的統計資訊，
       並向累計統計資訊系統回報統計資訊。此階段完成後，
       <code class="command">VACUUM</code> 就會結束。
     </td></tr></tbody></table>

<br>

<a id="BASEBACKUP-PROGRESS-REPORTING"></a>

### 27.4.6. 基礎備份進度回報 [#](#BASEBACKUP-PROGRESS-REPORTING)

<a id="id-1.6.14.9.8.2"></a>

每當像 pg_basebackup 這樣的應用程式
正在取得基礎備份時，
`pg_stat_progress_basebackup`
檢視表中，就會針對每個目前正在執行
`BASE_BACKUP` 複寫命令、
並串流傳輸備份資料的 WAL 傳送程序，各含有一列。
下方的表格，說明了會被回報的資訊，
並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-BASEBACKUP-VIEW"></a>

**表 27.47. `pg_stat_progress_basebackup` 檢視表**

<table border="1" class="table" summary="pg_stat_progress_basebackup View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       某個 WAL 傳送程序的程序 ID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       目前的處理階段。請參閱<a class="xref" href="progress-reporting.md#BASEBACKUP-PHASES">表 27.48</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backup_total</code> <code class="type">bigint</code>
</p>
<p>
       將被串流傳輸的資料總量。此為預估值，
       在 <code class="literal">streaming database files</code>
       階段開始時回報。請注意，這只是一個近似值，
       因為在 <code class="literal">streaming database files</code>
       階段期間，資料庫可能會發生變化，
       且 WAL 日誌之後也可能會被納入備份中。
       一旦已串流傳輸的資料量超過預估的總大小，
       此值就會與 <code class="structfield">backup_streamed</code>
       永遠保持相同。若在
       <span class="application">pg_basebackup</span>
       中停用了此項預估（也就是指定了
       <code class="literal">--no-estimate-size</code> 選項），
       則此值為 <code class="literal">NULL</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backup_streamed</code> <code class="type">bigint</code>
</p>
<p>
       已串流傳輸的資料量。此計數器只會在
       階段為 <code class="literal">streaming database files</code>
       或 <code class="literal">transferring wal files</code>
       時才會前進。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespaces_total</code> <code class="type">bigint</code>
</p>
<p>
       將被串流傳輸的資料表空間總數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespaces_streamed</code> <code class="type">bigint</code>
</p>
<p>
       已串流傳輸的資料表空間數。此計數器只會在
       階段為 <code class="literal">streaming database files</code>
       時才會前進。
      </p></td></tr></tbody></table>

<br><a id="BASEBACKUP-PHASES"></a>

**表 27.48. 基礎備份各階段**

<table border="1" class="table" summary="Base Backup Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>階段</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
       此 WAL 傳送程序正在準備開始備份。
       預期此階段耗時應非常短暫。
      </td></tr><tr><td><code class="literal">waiting for checkpoint to finish</code></td><td>
       此 WAL 傳送程序目前正在執行
       <code class="function">pg_backup_start</code>，
       以準備取得基礎備份，
       並正在等待備份開始檢查點完成。
      </td></tr><tr><td><code class="literal">estimating backup size</code></td><td>
       此 WAL 傳送程序目前正在預估，
       將以基礎備份形式串流傳輸之資料庫檔案的總量。
      </td></tr><tr><td><code class="literal">streaming database files</code></td><td>
       此 WAL 傳送程序目前正在以基礎備份形式，
       串流傳輸資料庫檔案。
      </td></tr><tr><td><code class="literal">waiting for wal archiving to finish</code></td><td>
       此 WAL 傳送程序目前正在執行
       <code class="function">pg_backup_stop</code>
       以完成此次備份，
       並正在等待此次基礎備份所需的所有 WAL 檔案，
       都成功歸檔完成。
       若在
       <span class="application">pg_basebackup</span>
       中指定了 <code class="literal">--wal-method=none</code>
       或 <code class="literal">--wal-method=stream</code>，
       則此階段完成後，備份就會結束。
      </td></tr><tr><td><code class="literal">transferring wal files</code></td><td>
       此 WAL 傳送程序目前正在傳輸備份期間
       所產生的所有 WAL 日誌。此階段會在
       <code class="literal">waiting for wal archiving to finish</code>
       階段之後發生，前提是在
       <span class="application">pg_basebackup</span>
       中指定了 <code class="literal">--wal-method=fetch</code>。
       此階段完成後，備份就會結束。
      </td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/progress-reporting.html)（原文版本：18.6；核對日期：2026-09-26）
