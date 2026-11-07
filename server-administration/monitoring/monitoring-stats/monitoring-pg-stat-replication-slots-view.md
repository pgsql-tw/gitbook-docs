# 27.2.5. pg_stat_replication_slots

<a id="MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW"></a>

## 27.2.5. `pg_stat_replication_slots` [#](#monitoring-pg-stat-replication-slots-view) <a href="#monitoring-pg-stat-replication-slots-view" id="monitoring-pg-stat-replication-slots-view"></a>

<a id="id-1.6.14.7.9.2"></a>

`pg_stat_replication_slots` 檢視表中，每個
邏輯複寫插槽都會有一筆資料列，顯示有關其使用情形的統計資訊。

<a id="PG-STAT-REPLICATION-SLOTS-VIEW"></a>

### 表 27.15. `pg_stat_replication_slots` 檢視表 [#](#pg-stat-replication-slots-view) <a href="#pg-stat-replication-slots-view" id="pg-stat-replication-slots-view"></a>

<table border="1" class="table" summary="pg_stat_replication_slots 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
        欄位類型
       </p>
<p>
        說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">slot_name</code> <code class="type">text</code>
</p>
<p>
        該複寫插槽在整個叢集中唯一的識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spill_txns</code> <code class="type">bigint</code>
</p>
<p>
        一旦邏輯解碼用於從 WAL 解碼變更所使用的記憶體超過
        <code class="literal">logical_decoding_work_mem</code>，被溢出（spill）至磁碟的交易數量。
        此計數器對最上層交易與子交易都會遞增。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spill_count</code> <code class="type">bigint</code>
</p>
<p>
        在為此插槽從 WAL 解碼變更時，交易被溢出至磁碟的次數。
        每當有交易被溢出時，此計數器就會遞增，
        而同一個交易可能會被溢出多次。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">spill_bytes</code> <code class="type">bigint</code>
</p>
<p>
        在為此插槽執行從 WAL 解碼變更的過程中，被溢出至磁碟的已解碼
        交易資料量。此計數器及其他溢出計數器，可用來估算邏輯
        解碼期間所發生的 I/O，並可用來調校 <code class="literal">logical_decoding_work_mem</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stream_txns</code> <code class="type">bigint</code>
</p>
<p>
        在此插槽用於從 WAL 解碼變更的邏輯解碼記憶體使用量超過
        <code class="literal">logical_decoding_work_mem</code> 之後，被串流（stream）傳送至解碼輸出
        外掛程式的進行中交易數量。串流僅適用於最上層交易
        （子交易無法被獨立串流），因此此計數器不會對子交易遞增。
       </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stream_count</code><code class="type">bigint</code>
</p>
<p>
        在為此插槽從 WAL 解碼變更時，進行中交易被串流傳送至解碼輸出
        外掛程式的次數。每當有交易被串流傳送時，
        此計數器就會遞增，而同一個交易可能會被串流傳送多次。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stream_bytes</code><code class="type">bigint</code>
</p>
<p>
        在為此插槽執行從 WAL 解碼變更的過程中，為將進行中交易串流傳送至
        解碼輸出外掛程式所解碼的交易資料量。此插槽的此計數器及其他串流
        計數器，可用來調校 <code class="literal">logical_decoding_work_mem</code>。
       </p>
</td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_txns</code> <code class="type">bigint</code>
</p>
<p>
        為此插槽傳送至解碼輸出外掛程式的已解碼交易數量。此欄位僅計算
        最上層交易，不會對子交易遞增。請注意，此欄位包含已被
        串流傳送及／或溢出的交易。
       </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_bytes</code><code class="type">bigint</code>
</p>
<p>
        在為此插槽從 WAL 解碼變更的過程中，為將交易傳送至
        解碼輸出外掛程式所解碼的交易資料量。請注意，此欄位包含已被
        串流傳送及／或溢出的資料。
       </p>
</td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
        這些統計資訊上次重設的時間
       </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
