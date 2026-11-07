# 27.4.2. CLUSTER 進度回報

<a id="CLUSTER-PROGRESS-REPORTING"></a>

## 27.4.2. CLUSTER 進度回報 [#](#cluster-progress-reporting) <a href="#cluster-progress-reporting" id="cluster-progress-reporting"></a>

<a id="id-1.6.14.9.4.2"></a>

每當 `CLUSTER` 或 `VACUUM FULL`
正在執行時，`pg_stat_progress_cluster`
檢視表中，就會針對每個目前正在執行其中一項命令的後端，
各含有一列。下方的表格，
說明了會被回報的資訊，並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-CLUSTER-VIEW"></a>

### 表 27.40. `pg_stat_progress_cluster` 檢視表 [#](#pg-stat-progress-cluster-view) <a href="#pg-stat-progress-cluster-view" id="pg-stat-progress-cluster-view"></a>

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
       目前的處理階段。請參閱<a class="xref" href="#cluster-phases">表 27.41</a>。
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

### 表 27.41. CLUSTER 與 VACUUM FULL 各階段 [#](#cluster-phases) <a href="#cluster-phases" id="cluster-phases"></a>

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

[返回 27.4. 進度回報](../progress-reporting.md#progress-reporting)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/progress-reporting.html)（原文版本：18.6；核對日期：2026-09-26）
