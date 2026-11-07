# 27.2.22. pg_statio_all_indexes

<a id="MONITORING-PG-STATIO-ALL-INDEXES-VIEW"></a>

## 27.2.22. `pg_statio_all_indexes` [#](#monitoring-pg-statio-all-indexes-view) <a href="#monitoring-pg-statio-all-indexes-view" id="monitoring-pg-statio-all-indexes-view"></a>

<a id="id-1.6.14.7.26.2"></a>

`pg_statio_all_indexes` 檢視表中，目前資料庫中的
每個索引各會有一筆資料列，
顯示有關該特定索引 I/O 情形的統計資訊。
`pg_statio_user_indexes` 與
`pg_statio_sys_indexes` 檢視表
包含相同的資訊，
但分別經過篩選，僅顯示使用者索引與系統索引。

<a id="PG-STATIO-ALL-INDEXES-VIEW"></a>

### 表 27.32. `pg_statio_all_indexes` 檢視表 [#](#pg-statio-all-indexes-view) <a href="#pg-statio-all-indexes-view" id="pg-statio-all-indexes-view"></a>

<table border="1" class="table" summary="pg_statio_all_indexes 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       此索引所屬資料表的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelid</code> <code class="type">oid</code>
</p>
<p>
       此索引的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       此索引所屬綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       此索引所屬資料表的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">indexrelname</code> <code class="type">name</code>
</p>
<p>
       此索引的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       從此索引讀取的磁碟區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       此索引中緩衝區命中的次數
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
