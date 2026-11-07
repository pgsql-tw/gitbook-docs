# 27.2.24. pg_stat_user_functions

<a id="MONITORING-PG-STAT-USER-FUNCTIONS-VIEW"></a>

## 27.2.24. `pg_stat_user_functions` [#](#monitoring-pg-stat-user-functions-view) <a href="#monitoring-pg-stat-user-functions-view" id="monitoring-pg-stat-user-functions-view"></a>

<a id="id-1.6.14.7.28.2"></a>

`pg_stat_user_functions` 檢視表中，每個
受追蹤的函式各會有一筆資料列，顯示有關該函式
執行情形的統計資訊。[track_functions](../../runtime-config/runtime-config-statistics.md#GUC-TRACK-FUNCTIONS) 參數
確切控制了哪些函式會被追蹤。

<a id="PG-STAT-USER-FUNCTIONS-VIEW"></a>

### 表 27.34. `pg_stat_user_functions` 檢視表 [#](#pg-stat-user-functions-view) <a href="#pg-stat-user-functions-view" id="pg-stat-user-functions-view"></a>

<table border="1" class="table" summary="pg_stat_user_functions 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">funcid</code> <code class="type">oid</code>
</p>
<p>
       某個函式的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       此函式所屬綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">funcname</code> <code class="type">name</code>
</p>
<p>
       此函式的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">calls</code> <code class="type">bigint</code>
</p>
<p>
       此函式被呼叫的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_time</code> <code class="type">double precision</code>
</p>
<p>
       花費在此函式，以及由此函式呼叫的所有其他函式上的
       總時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">self_time</code> <code class="type">double precision</code>
</p>
<p>
       花費在此函式本身上的總時間，不包含
       由此函式呼叫的其他函式，以毫秒為單位
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
