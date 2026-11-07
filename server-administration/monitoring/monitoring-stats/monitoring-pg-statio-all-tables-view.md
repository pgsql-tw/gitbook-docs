# 27.2.21. pg_statio_all_tables

<a id="MONITORING-PG-STATIO-ALL-TABLES-VIEW"></a>

## 27.2.21. `pg_statio_all_tables` [#](#monitoring-pg-statio-all-tables-view) <a href="#monitoring-pg-statio-all-tables-view" id="monitoring-pg-statio-all-tables-view"></a>

<a id="id-1.6.14.7.25.2"></a>

`pg_statio_all_tables` 檢視表中，目前資料庫中的
每個資料表（包括 TOAST
資料表）各會有一筆資料列，顯示有關該特定資料表 I/O 情形的統計資訊。
`pg_statio_user_tables` 與
`pg_statio_sys_tables` 檢視表
包含相同的資訊，
但分別經過篩選，僅顯示使用者資料表與系統資料表。

<a id="PG-STATIO-ALL-TABLES-VIEW"></a>

### 表 27.31. `pg_statio_all_tables` 檢視表 [#](#pg-statio-all-tables-view) <a href="#pg-statio-all-tables-view" id="pg-statio-all-tables-view"></a>

<table border="1" class="table" summary="pg_statio_all_tables 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">heap_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       從此資料表讀取的磁碟區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">heap_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       此資料表中緩衝區命中的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       從此資料表所有索引讀取的磁碟區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">idx_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       此資料表所有索引中緩衝區命中的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">toast_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       從此資料表的 TOAST 資料表（若有的話）讀取的磁碟區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">toast_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       此資料表的 TOAST 資料表（若有的話）中緩衝區命中的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tidx_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       從此資料表的 TOAST 資料表索引（若有的話）讀取的磁碟區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tidx_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       此資料表的 TOAST 資料表索引（若有的話）中緩衝區命中的次數
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
