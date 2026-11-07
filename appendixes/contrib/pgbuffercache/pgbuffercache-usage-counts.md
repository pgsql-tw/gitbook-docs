# F.25.4. pg_buffercache_usage_counts() 函式

<a id="PGBUFFERCACHE-USAGE-COUNTS"></a>

## F.25.4. `pg_buffercache_usage_counts()` 函式 [#](#pgbuffercache-usage-counts) <a href="#pgbuffercache-usage-counts" id="pgbuffercache-usage-counts"></a>

此函式所提供欄位的定義如[表 F.17](#pgbuffercache_usage_counts-columns)所示。

<a id="PGBUFFERCACHE_USAGE_COUNTS-COLUMNS"></a>

### 表 F.17. `pg_buffercache_usage_counts()` 輸出欄位 [#](#pgbuffercache_usage_counts-columns) <a href="#pgbuffercache_usage_counts-columns" id="pgbuffercache_usage_counts-columns"></a>

<table border="1" class="table" summary="pg_buffercache_usage_counts() 輸出欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usage_count</code> <code class="type">int4</code>
</p>
<p>
       一個可能的緩衝區使用計數值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers</code> <code class="type">int4</code>
</p>
<p>
       具有該使用計數的緩衝區數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dirty</code> <code class="type">int4</code>
</p>
<p>
       具有該使用計數的髒緩衝區數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pinned</code> <code class="type">int4</code>
</p>
<p>
       具有該使用計數且被釘住的緩衝區數量
      </p></td></tr></tbody></table>

<br>

`pg_buffercache_usage_counts()` 函式傳回一組資料列，依各個可能的使用計數值彙總所有共享緩衝區的狀態。`pg_buffercache` 檢視表提供類似且更詳細的資訊，但 `pg_buffercache_usage_counts()` 的成本低得多。

與 `pg_buffercache` 檢視表一樣，`pg_buffercache_usage_counts()` 不會取得緩衝區管理器的鎖定。因此，並行活動可能導致結果略有不準確。

[返回 F.25. pg_buffercache — 檢查 PostgreSQL 緩衝區快取狀態](../pgbuffercache.md#pgbuffercache)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgbuffercache.html)（原文版本：18.6；核對日期：2026-10-23）
