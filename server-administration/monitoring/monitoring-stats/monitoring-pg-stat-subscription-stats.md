# 27.2.9. pg_stat_subscription_stats

<a id="MONITORING-PG-STAT-SUBSCRIPTION-STATS"></a>

## 27.2.9. `pg_stat_subscription_stats` [#](#monitoring-pg-stat-subscription-stats) <a href="#monitoring-pg-stat-subscription-stats" id="monitoring-pg-stat-subscription-stats"></a>

<a id="id-1.6.14.7.13.2"></a>

`pg_stat_subscription_stats` 檢視表中，每個
訂閱都會有一筆資料列。

<a id="PG-STAT-SUBSCRIPTION-STATS"></a>

### 表 27.19. `pg_stat_subscription_stats` 檢視表 [#](#pg-stat-subscription-stats) <a href="#pg-stat-subscription-stats" id="pg-stat-subscription-stats"></a>

<table border="1" class="table" summary="pg_stat_subscription_stats 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subid</code> <code class="type">oid</code>
</p>
<p>
       此訂閱的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subname</code> <code class="type">name</code>
</p>
<p>
       此訂閱的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">apply_error_count</code> <code class="type">bigint</code>
</p>
<p>
       在套用變更時發生錯誤的次數。請注意，任何導致套用錯誤的
       衝突，都會同時被計入 <code class="literal">apply_error_count</code> 以及對應的
       衝突計數（例如 <code class="literal">confl_*</code>）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sync_error_count</code> <code class="type">bigint</code>
</p>
<p>
       在初始資料表同步期間發生錯誤的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_insert_exists</code> <code class="type">bigint</code>
</p>
<p>
       在套用變更期間，資料列插入違反
       <code class="literal">NOT DEFERRABLE</code> 唯一值限制條件的次數。有關此衝突的詳情，
       請參閱<a class="xref" href="../../logical-replication/logical-replication-conflicts.md#CONFLICT-INSERT-EXISTS">insert_exists</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_update_origin_differs</code> <code class="type">bigint</code>
</p>
<p>
       在套用變更期間，對先前已被其他來源修改過的資料列
       套用更新的次數。有關此
       衝突的詳情，請參閱<a class="xref" href="../../logical-replication/logical-replication-conflicts.md#CONFLICT-UPDATE-ORIGIN-DIFFERS">update_origin_differs</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_update_exists</code> <code class="type">bigint</code>
</p>
<p>
       在套用變更期間，更新後的資料列值違反
       <code class="literal">NOT DEFERRABLE</code> 唯一值限制條件的次數。有關此衝突的詳情，
       請參閱<a class="xref" href="../../logical-replication/logical-replication-conflicts.md#CONFLICT-UPDATE-EXISTS">update_exists</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_update_missing</code> <code class="type">bigint</code>
</p>
<p>
       在套用變更期間，找不到欲更新之元組的次數。有關此衝突的詳情，
       請參閱<a class="xref" href="../../logical-replication/logical-replication-conflicts.md#CONFLICT-UPDATE-MISSING">update_missing</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_delete_origin_differs</code> <code class="type">bigint</code>
</p>
<p>
       在套用變更期間，對先前已被其他來源修改過的資料列
       套用刪除作業的次數。
       有關此衝突的詳情，請參閱<a class="xref" href="../../logical-replication/logical-replication-conflicts.md#CONFLICT-DELETE-ORIGIN-DIFFERS">delete_origin_differs</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_delete_missing</code> <code class="type">bigint</code>
</p>
<p>
       在套用變更期間，找不到欲刪除之元組的次數。有關此衝突
       的詳情，請參閱<a class="xref" href="../../logical-replication/logical-replication-conflicts.md#CONFLICT-DELETE-MISSING">delete_missing</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confl_multiple_unique_conflicts</code> <code class="type">bigint</code>
</p>
<p>
       在套用變更期間，資料列插入或更新後的資料列值違反多個
       <code class="literal">NOT DEFERRABLE</code> 唯一值限制條件的次數。有關此衝突的
       詳情，請參閱<a class="xref" href="../../logical-replication/logical-replication-conflicts.md#CONFLICT-MULTIPLE-UNIQUE-CONFLICTS">multiple_unique_conflicts</a>。
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
