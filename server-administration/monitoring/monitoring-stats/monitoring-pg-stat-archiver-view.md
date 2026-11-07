# 27.2.12. pg_stat_archiver

<a id="MONITORING-PG-STAT-ARCHIVER-VIEW"></a>

## 27.2.12. `pg_stat_archiver` [#](#monitoring-pg-stat-archiver-view) <a href="#monitoring-pg-stat-archiver-view" id="monitoring-pg-stat-archiver-view"></a>

<a id="id-1.6.14.7.16.2"></a>

`pg_stat_archiver` 檢視表始終只會有
一筆資料列，包含有關該叢集歸檔程序的資料。

<a id="PG-STAT-ARCHIVER-VIEW"></a>

### 表 27.22. `pg_stat_archiver` 檢視表 [#](#pg-stat-archiver-view) <a href="#pg-stat-archiver-view" id="pg-stat-archiver-view"></a>

<table border="1" class="table" summary="pg_stat_archiver 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">archived_count</code> <code class="type">bigint</code>
</p>
<p>
       已成功歸檔的 WAL 檔案數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_archived_wal</code> <code class="type">text</code>
</p>
<p>
       最近一次成功歸檔之 WAL 檔案的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_archived_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       最近一次成功歸檔作業的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">failed_count</code> <code class="type">bigint</code>
</p>
<p>
       歸檔 WAL 檔案失敗的嘗試次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_failed_wal</code> <code class="type">text</code>
</p>
<p>
       最近一次失敗歸檔作業之 WAL 檔案的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_failed_time</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       最近一次失敗歸檔作業的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       這些統計資訊上次重設的時間
      </p></td></tr></tbody></table>

<br>

一般而言，WAL 檔案會依由舊到新的順序歸檔，但這並非保證，並且在某些特殊情況下
（例如將待命伺服器提升為主要伺服器，或當機後復原之後）並不成立。因此，
不能安全地假設所有比
`last_archived_wal` 更舊的檔案也都已成功歸檔。

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
