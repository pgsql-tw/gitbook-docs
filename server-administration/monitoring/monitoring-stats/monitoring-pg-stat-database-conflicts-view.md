# 27.2.18. pg_stat_database_conflicts

<a id="MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW"></a>

## 27.2.18. `pg_stat_database_conflicts` [#](#monitoring-pg-stat-database-conflicts-view) <a href="#monitoring-pg-stat-database-conflicts-view" id="monitoring-pg-stat-database-conflicts-view"></a>

<a id="id-1.6.14.7.22.2"></a>

`pg_stat_database_conflicts` 檢視表中，每個
資料庫都會有一筆資料列，顯示資料庫層級中，因與待命伺服器上復原作業
衝突而取消查詢的統計資訊。
由於主要伺服器上不會發生衝突，此檢視表僅會包含
待命伺服器上的資訊。

<a id="PG-STAT-DATABASE-CONFLICTS-VIEW"></a>

### 表 27.28. `pg_stat_database_conflicts` 檢視表 [#](#pg-stat-database-conflicts-view) <a href="#pg-stat-database-conflicts-view" id="pg-stat-database-conflicts-view"></a>

<table border="1" class="table" summary="pg_stat_database_conflicts 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       某個資料庫的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       此資料庫的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_tablespace</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中因資料表空間已被卸除（DROP）而取消的
       查詢數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_lock</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中因鎖定逾時而取消的
       查詢數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_snapshot</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中因過舊快照而取消的
       查詢數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_bufferpin</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中因緩衝區被釘選而取消的
       查詢數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_deadlock</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中因死結而取消的
       查詢數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_active_logicalslot</code> <code class="type">bigint</code>
</p>
<p>
       此資料庫中因過舊快照，或主要伺服器上
       <a class="xref" href="../../runtime-config/runtime-config-wal.md#GUC-WAL-LEVEL">wal_level</a> 設定過低而取消的
       邏輯插槽使用次數
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
