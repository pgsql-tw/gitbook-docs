# 27.4.4. CREATE INDEX 進度回報

<a id="CREATE-INDEX-PROGRESS-REPORTING"></a>

## 27.4.4. CREATE INDEX 進度回報 [#](#create-index-progress-reporting) <a href="#create-index-progress-reporting" id="create-index-progress-reporting"></a>

<a id="id-1.6.14.9.6.2"></a>

每當 `CREATE INDEX` 或 `REINDEX`
正在執行時，`pg_stat_progress_create_index`
檢視表中，就會針對每個目前正在建立索引的後端，
各含有一列。下方的表格，
說明了會被回報的資訊，並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-CREATE-INDEX-VIEW"></a>

### 表 27.43. `pg_stat_progress_create_index` 檢視表 [#](#pg-stat-progress-create-index-view) <a href="#pg-stat-progress-create-index-view" id="pg-stat-progress-create-index-view"></a>

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
       目前建立索引的處理階段。請參閱<a class="xref" href="#create-index-phases">表 27.44</a>。
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

### 表 27.44. CREATE INDEX 各階段 [#](#create-index-phases) <a href="#create-index-phases" id="create-index-phases"></a>

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

[返回 27.4. 進度回報](../progress-reporting.md#progress-reporting)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/progress-reporting.html)（原文版本：18.6；核對日期：2026-09-26）
