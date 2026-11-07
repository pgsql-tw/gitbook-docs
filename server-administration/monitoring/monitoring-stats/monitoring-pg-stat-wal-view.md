# 27.2.16. pg_stat_wal

<a id="MONITORING-PG-STAT-WAL-VIEW"></a>

## 27.2.16. `pg_stat_wal` [#](#monitoring-pg-stat-wal-view) <a href="#monitoring-pg-stat-wal-view" id="monitoring-pg-stat-wal-view"></a>

<a id="id-1.6.14.7.20.2"></a>

`pg_stat_wal` 檢視表始終只會有
一筆資料列，包含有關該叢集 WAL 活動的資料。

<a id="PG-STAT-WAL-VIEW"></a>

### 表 27.26. `pg_stat_wal` 檢視表 [#](#pg-stat-wal-view) <a href="#pg-stat-wal-view" id="pg-stat-wal-view"></a>

<table border="1" class="table" summary="pg_stat_wal 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_records</code> <code class="type">bigint</code>
</p>
<p>
       已產生的 WAL 記錄總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_fpi</code> <code class="type">bigint</code>
</p>
<p>
       已產生的 WAL 完整分頁映像總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_bytes</code> <code class="type">numeric</code>
</p>
<p>
       已產生的 WAL 總量，以位元組計
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_buffers_full</code> <code class="type">bigint</code>
</p>
<p>
       因 WAL 緩衝區已滿而將 WAL 資料寫入磁碟的次數
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
