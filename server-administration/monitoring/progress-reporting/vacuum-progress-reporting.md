# 27.4.5. VACUUM 進度回報

<a id="VACUUM-PROGRESS-REPORTING"></a>

## 27.4.5. VACUUM 進度回報 [#](#vacuum-progress-reporting) <a href="#vacuum-progress-reporting" id="vacuum-progress-reporting"></a>

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
請參閱 [27.4.2 節](cluster-progress-reporting.md#cluster-progress-reporting)。

<a id="PG-STAT-PROGRESS-VACUUM-VIEW"></a>

### 表 27.45. `pg_stat_progress_vacuum` 檢視表 [#](#pg-stat-progress-vacuum-view) <a href="#pg-stat-progress-vacuum-view" id="pg-stat-progress-vacuum-view"></a>

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
       目前清理的處理階段。請參閱<a class="xref" href="#vacuum-phases">表 27.46</a>。
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
       <a class="link" href="../../../internals/storage/storage-vm.md">能見度映射（visibility map）</a>
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
       <a class="xref" href="../../runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM">maintenance_work_mem</a>，
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
       <a class="xref" href="../../runtime-config/runtime-config-vacuum.md#runtime-config-resource-vacuum-cost">19.10.2 節</a>）
       而耗費在休眠上的總時間，以毫秒為單位
       （若已啟用 <a class="xref" href="../../runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING">track_cost_delay_timing</a>，
       否則為零）。這包括任何相關聯的平行工作者
       休眠的時間。然而，平行工作者回報其休眠時間的頻率
       最多為每秒一次，因此所回報的值，
       可能會略微過時。
      </p></td></tr></tbody></table>

<br><a id="VACUUM-PHASES"></a>

### 表 27.46. VACUUM 各階段 [#](#vacuum-phases) <a href="#vacuum-phases" id="vacuum-phases"></a>

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
       <a class="xref" href="../../runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM">maintenance_work_mem</a>
       （或在自動 vacuum 的情況下，
       若有設定
       <a class="xref" href="../../runtime-config/runtime-config-resource.md#GUC-AUTOVACUUM-WORK-MEM">autovacuum_work_mem</a>）
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

[返回 27.4. 進度回報](../progress-reporting.md#progress-reporting)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/progress-reporting.html)（原文版本：18.6；核對日期：2026-09-26）
