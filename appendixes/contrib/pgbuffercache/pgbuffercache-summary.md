# F.25.3. pg_buffercache_summary() 函式

<a id="PGBUFFERCACHE-SUMMARY"></a>

## F.25.3. `pg_buffercache_summary()` 函式 [#](#pgbuffercache-summary) <a href="#pgbuffercache-summary" id="pgbuffercache-summary"></a>

此函式所提供欄位的定義如[表 F.16](#pgbuffercache-summary-columns)所示。

<a id="PGBUFFERCACHE-SUMMARY-COLUMNS"></a>

### 表 F.16. `pg_buffercache_summary()` 輸出欄位 [#](#pgbuffercache-summary-columns) <a href="#pgbuffercache-summary-columns" id="pgbuffercache-summary-columns"></a>

<table border="1" class="table" summary="pg_buffercache_summary() 輸出欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_used</code> <code class="type">int4</code>
</p>
<p>
       已使用的共享緩衝區數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_unused</code> <code class="type">int4</code>
</p>
<p>
       未使用的共享緩衝區數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_dirty</code> <code class="type">int4</code>
</p>
<p>
       髒的共享緩衝區數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">buffers_pinned</code> <code class="type">int4</code>
</p>
<p>
       被釘住的共享緩衝區數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usagecount_avg</code> <code class="type">float8</code>
</p>
<p>
       已使用共享緩衝區的平均使用計數
      </p></td></tr></tbody></table>

<br>

`pg_buffercache_summary()` 函式傳回單一資料列，彙總所有共享緩衝區的狀態。`pg_buffercache` 檢視表提供類似且更詳細的資訊，但 `pg_buffercache_summary()` 的成本低得多。

與 `pg_buffercache` 檢視表一樣，`pg_buffercache_summary()` 不會取得緩衝區管理器的鎖定。因此，並行活動可能導致結果略有不準確。

[返回 F.25. pg_buffercache — 檢查 PostgreSQL 緩衝區快取狀態](../pgbuffercache.md#pgbuffercache)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgbuffercache.html)（原文版本：18.6；核對日期：2026-10-23）
