# 27.2.23. pg_statio_all_sequences

<a id="MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW"></a>

## 27.2.23. `pg_statio_all_sequences` [#](#monitoring-pg-statio-all-sequences-view) <a href="#monitoring-pg-statio-all-sequences-view" id="monitoring-pg-statio-all-sequences-view"></a>

<a id="id-1.6.14.7.27.2"></a>

`pg_statio_all_sequences` 檢視表中，目前資料庫中的
每個序列各會有一筆資料列，
顯示有關該特定序列 I/O 情形的統計資訊。

<a id="PG-STATIO-ALL-SEQUENCES-VIEW"></a>

### 表 27.33. `pg_statio_all_sequences` 檢視表 [#](#pg-statio-all-sequences-view) <a href="#pg-statio-all-sequences-view" id="pg-statio-all-sequences-view"></a>

<table border="1" class="table" summary="pg_statio_all_sequences 檢視表"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       某個序列的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">schemaname</code> <code class="type">name</code>
</p>
<p>
       此序列所屬綱要的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       此序列的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_read</code> <code class="type">bigint</code>
</p>
<p>
       從此序列讀取的磁碟區塊數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       此序列中緩衝區命中的次數
      </p></td></tr></tbody></table>

<br>

[返回 27.2. 累計統計系統](../monitoring-stats.md#monitoring-stats)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/monitoring-stats.html)（原文版本：18.6；核對日期：2026-10-23）
