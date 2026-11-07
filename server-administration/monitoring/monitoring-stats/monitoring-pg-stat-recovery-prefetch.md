# 27.2.7. pg_stat_recovery_prefetch

<a id="MONITORING-PG-STAT-RECOVERY-PREFETCH"></a>

## 27.2.7. `pg_stat_recovery_prefetch` [#](#monitoring-pg-stat-recovery-prefetch) <a href="#monitoring-pg-stat-recovery-prefetch" id="monitoring-pg-stat-recovery-prefetch"></a>

<a id="id-1.6.14.7.11.2"></a>

`pg_stat_recovery_prefetch` 檢視表僅會有
一筆資料列。`wal_distance`、
`block_distance` 以及
`io_depth` 這幾個欄位顯示的是目前的值，而
其他欄位顯示的則是可以透過
`pg_stat_reset_shared` 函式重設的累計計數器。

<a id="PG-STAT-RECOVERY-PREFETCH-VIEW"></a>

### 表 27.17. `pg_stat_recovery_prefetch` 檢視表 [#](#pg-stat-recovery-prefetch-view) <a href="#pg-stat-recovery-prefetch-view" id="pg-stat-recovery-prefetch-view"></a>

<table border="1" class="table" summary="pg_stat_recovery_prefetch 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
        這些統計資訊上次重設的時間
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">prefetch</code> <code class="type">bigint</code>
</p>
<p>
        因不在緩衝池中而被預先擷取的區塊數量
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">hit</code> <code class="type">bigint</code>
</p>
<p>
        因已存在於緩衝池中而未被預先擷取的區塊數量
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">skip_init</code> <code class="type">bigint</code>
</p>
<p>
        因將以零值初始化而未被預先擷取的區塊數量
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">skip_new</code> <code class="type">bigint</code>
</p>
<p>
        因尚不存在而未被預先擷取的區塊數量
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">skip_fpw</code> <code class="type">bigint</code>
</p>
<p>
        因 WAL 中已包含完整分頁映像而未被預先擷取的區塊數量
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">skip_rep</code> <code class="type">bigint</code>
</p>
<p>
        因最近已經被預先擷取過而未被再次預先擷取的區塊數量
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">wal_distance</code> <code class="type">int</code>
</p>
<p>
        預先擷取程序目前向前查看的位元組數
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">block_distance</code> <code class="type">int</code>
</p>
<p>
        預先擷取程序目前向前查看的區塊數
       </p>
</td></tr><tr><td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">io_depth</code> <code class="type">int</code>
</p>
<p>
        已發起但尚未確定完成的預先擷取數量
       </p>
</td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
