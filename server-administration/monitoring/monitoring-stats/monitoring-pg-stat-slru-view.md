# 27.2.25. pg_stat_slru

<a id="MONITORING-PG-STAT-SLRU-VIEW"></a>

## 27.2.25. `pg_stat_slru` [#](#monitoring-pg-stat-slru-view) <a href="#monitoring-pg-stat-slru-view" id="monitoring-pg-stat-slru-view"></a>

<a id="id-1.6.14.7.29.2"></a><a id="id-1.6.14.7.29.3"></a>

PostgreSQL 透過 `SLRU`（*simple least-recently-used*）
快取來存取某些磁碟上的資訊。
`pg_stat_slru` 檢視表中，每個
受追蹤的 SLRU 快取各會有一筆資料列，顯示有關已快取頁面
存取情形的統計資訊。

對於屬於核心伺服器一部分的每個 `SLRU` 快取，
都有一個以 `_buffers` 為字尾的組態參數
控制其大小。

<a id="PG-STAT-SLRU-VIEW"></a>

### 表 27.35. `pg_stat_slru` 檢視表 [#](#pg-stat-slru-view) <a href="#pg-stat-slru-view" id="pg-stat-slru-view"></a>

<table border="1" class="table" summary="pg_stat_slru 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       此 SLRU 的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_zeroed</code> <code class="type">bigint</code>
</p>
<p>
       在初始化期間被歸零的區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       發現磁碟區塊已存在於 SLRU 中，因此不需要進行讀取的
       次數（此欄位僅包含 SLRU 中的命中，不包含作業系統
       檔案系統快取中的命中）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_read</code> <code class="type">bigint</code>
</p>
<p>
       為此 SLRU 讀取的磁碟區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_written</code> <code class="type">bigint</code>
</p>
<p>
       為此 SLRU 寫入的磁碟區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_exists</code> <code class="type">bigint</code>
</p>
<p>
       為此 SLRU 檢查是否存在的區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">flushes</code> <code class="type">bigint</code>
</p>
<p>
       為此 SLRU 刷寫髒資料的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">truncates</code> <code class="type">bigint</code>
</p>
<p>
       為此 SLRU 執行截斷的次數
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
