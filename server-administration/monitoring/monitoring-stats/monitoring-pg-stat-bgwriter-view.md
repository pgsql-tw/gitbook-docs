# 27.2.14. pg_stat_bgwriter

<a id="MONITORING-PG-STAT-BGWRITER-VIEW"></a>

## 27.2.14. `pg_stat_bgwriter` [#](#monitoring-pg-stat-bgwriter-view) <a href="#monitoring-pg-stat-bgwriter-view" id="monitoring-pg-stat-bgwriter-view"></a>

<a id="id-1.6.14.7.18.2"></a>

`pg_stat_bgwriter` 檢視表始終只會有
一筆資料列，包含有關該叢集背景寫入程序的資料。

<a id="PG-STAT-BGWRITER-VIEW"></a>

### 表 27.24. `pg_stat_bgwriter` 檢視表 [#](#pg-stat-bgwriter-view) <a href="#pg-stat-bgwriter-view" id="pg-stat-bgwriter-view"></a>

<table border="1" class="table" summary="pg_stat_bgwriter 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_clean</code> <code class="type">bigint</code>
</p>
<p>
       由背景寫入程序寫入的緩衝區數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">maxwritten_clean</code> <code class="type">bigint</code>
</p>
<p>
       背景寫入程序因寫入了過多緩衝區，而停止清理
       掃描的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_alloc</code> <code class="type">bigint</code>
</p>
<p>
       已配置的緩衝區數量
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
