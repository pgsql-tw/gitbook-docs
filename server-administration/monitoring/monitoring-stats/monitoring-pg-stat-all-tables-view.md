# 27.2.19. pg_stat_all_tables

<a id="MONITORING-PG-STAT-ALL-TABLES-VIEW"></a>

## 27.2.19. `pg_stat_all_tables` [#](#monitoring-pg-stat-all-tables-view) <a href="#monitoring-pg-stat-all-tables-view" id="monitoring-pg-stat-all-tables-view"></a>

<a id="id-1.6.14.7.23.2"></a>

`pg_stat_all_tables` 檢視表中，目前資料庫中的
每個資料表（包括 TOAST
資料表）各會有一筆資料列，顯示有關對該特定資料表存取情形的統計資訊。
`pg_stat_user_tables` 與
`pg_stat_sys_tables` 檢視表
包含相同的資訊，
但分別經過篩選，僅顯示使用者資料表與系統資料表。

<a id="PG-STAT-ALL-TABLES-VIEW"></a>

### 表 27.29. `pg_stat_all_tables` 檢視表 [#](#pg-stat-all-tables-view) <a href="#pg-stat-all-tables-view" id="pg-stat-all-tables-view"></a>

<table border="1" class="table" summary="pg_stat_all_tables 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       某個資料表的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       此資料表所屬綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       此資料表的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seq_scan</code> <code class="type">bigint</code>
</p>
<p>
       在此資料表上發起的循序掃描次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_seq_scan</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此資料表上最後一次循序掃描的時間，根據最近一次
       交易停止的時間計算
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">seq_tup_read</code> <code class="type">bigint</code>
</p>
<p>
       由循序掃描擷取的存活資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_scan</code> <code class="type">bigint</code>
</p>
<p>
       在此資料表上發起的索引掃描次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_idx_scan</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此資料表上最後一次索引掃描的時間，根據最近一次
       交易停止的時間計算
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_tup_fetch</code> <code class="type">bigint</code>
</p>
<p>
       由索引掃描擷取的存活資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_ins</code> <code class="type">bigint</code>
</p>
<p>
       已插入的資料列總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_upd</code> <code class="type">bigint</code>
</p>
<p>
       已更新的資料列總數。（此欄位包含計入
       <code class="structfield">n_tup_hot_upd</code> 與
       <code class="structfield">n_tup_newpage_upd</code> 的資料列更新，
       以及其餘非 <acronym class="acronym">HOT</acronym> 更新。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_del</code> <code class="type">bigint</code>
</p>
<p>
       已刪除的資料列總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_hot_upd</code> <code class="type">bigint</code>
</p>
<p>
       <a class="link" href="../../../internals/storage/storage-hot.md">HOT 更新</a>的資料列數量。
       這些是不需要在索引中建立後續版本的
       更新。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_tup_newpage_upd</code> <code class="type">bigint</code>
</p>
<p>
       更新後版本被放置於一個<span class="emphasis"><em>新</em></span>堆積分頁上，
       而留下具有指向不同堆積分頁之
       <a class="link" href="../../../internals/storage/storage-page-layout/storage-tuple-layout.md#storage-tuple-layout"><code class="structfield">t_ctid</code>
        欄位</a>之原始版本的資料列更新數量。這些
       一律屬於非 <acronym class="acronym">HOT</acronym> 更新。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_live_tup</code> <code class="type">bigint</code>
</p>
<p>
       估計的存活資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_dead_tup</code> <code class="type">bigint</code>
</p>
<p>
       估計的死亡資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_mod_since_analyze</code> <code class="type">bigint</code>
</p>
<p>
       自此資料表上次 analyze 以來，估計被修改的資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">n_ins_since_vacuum</code> <code class="type">bigint</code>
</p>
<p>
       自此資料表上次 vacuum 以來（不計入
       <code class="command">VACUUM FULL</code>），估計被插入的資料列數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_vacuum</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此資料表最後一次被手動清理（vacuum）
       （不計入 <code class="command">VACUUM FULL</code>）的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_autovacuum</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此資料表最後一次被 autovacuum 常駐程序清理（vacuum） 的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_analyze</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此資料表最後一次被手動分析（analyze） 的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">last_autoanalyze</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       此資料表最後一次被 autovacuum 常駐程序分析（analyze） 的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">vacuum_count</code> <code class="type">bigint</code>
</p>
<p>
       此資料表被手動清理（vacuum）
       （不計入 <code class="command">VACUUM FULL</code>）的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">autovacuum_count</code> <code class="type">bigint</code>
</p>
<p>
       此資料表被 autovacuum 常駐程序清理（vacuum） 的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">analyze_count</code> <code class="type">bigint</code>
</p>
<p>
       此資料表被手動分析（analyze） 的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">autoanalyze_count</code> <code class="type">bigint</code>
</p>
<p>
       此資料表被 autovacuum 常駐程序分析（analyze） 的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_vacuum_time</code> <code class="type">double precision</code>
</p>
<p>
       此資料表被手動清理（vacuum）（不計入
       <code class="command">VACUUM FULL</code>）的總時間，以毫秒為單位。
       （此欄位包含因成本延遲而休眠所花費的時間。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_autovacuum_time</code> <code class="type">double precision</code>
</p>
<p>
       此資料表被 autovacuum 常駐程序清理（vacuum） 的總時間，
       以毫秒為單位。（此欄位包含因成本延遲而休眠
       所花費的時間。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_analyze_time</code> <code class="type">double precision</code>
</p>
<p>
       此資料表被手動分析（analyze） 的總時間，以毫秒為單位。
       （此欄位包含因成本延遲而休眠所花費的時間。）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_autoanalyze_time</code> <code class="type">double precision</code>
</p>
<p>
       此資料表被 autovacuum 常駐程序分析（analyze） 的總時間，
       以毫秒為單位。（此欄位包含因成本延遲而休眠
       所花費的時間。）
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
