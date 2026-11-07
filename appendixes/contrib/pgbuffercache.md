<a id="PGBUFFERCACHE"></a>

## F.25. pg_buffercache — 檢查 PostgreSQL 緩衝區快取狀態 [#](#pgbuffercache) <a href="#pgbuffercache" id="pgbuffercache"></a>

[F.25.1. `pg_buffercache` 檢視表](pgbuffercache/pgbuffercache-pg-buffercache.md#pgbuffercache-pg-buffercache)

[F.25.2. `pg_buffercache_numa` 檢視表](pgbuffercache/pgbuffercache-pg-buffercache-numa.md#pgbuffercache-pg-buffercache-numa)

[F.25.3. `pg_buffercache_summary()` 函式](pgbuffercache/pgbuffercache-summary.md#pgbuffercache-summary)

[F.25.4. `pg_buffercache_usage_counts()` 函式](pgbuffercache/pgbuffercache-usage-counts.md#pgbuffercache-usage-counts)

[F.25.5. `pg_buffercache_evict()` 函式](pgbuffercache.md#pgbuffercache-pg-buffercache-evict)

[F.25.6. `pg_buffercache_evict_relation()` 函式](pgbuffercache.md#pgbuffercache-pg-buffercache-evict-relation)

[F.25.7. `pg_buffercache_evict_all()` 函式](pgbuffercache.md#pgbuffercache-pg-buffercache-evict-all)

[F.25.8. 輸出範例](pgbuffercache.md#pgbuffercache-sample-output)

[F.25.9. 作者](pgbuffercache.md#pgbuffercache-authors)

<a id="id-1.11.7.35.2"></a>

`pg_buffercache` 模組提供一種即時檢視共享緩衝區快取中所發生情況的方法。它也提供一種低階的方式，可將資料從快取中逐出，供測試之用。

<a id="id-1.11.7.35.4"></a><a id="id-1.11.7.35.5"></a><a id="id-1.11.7.35.6"></a><a id="id-1.11.7.35.7"></a><a id="id-1.11.7.35.8"></a><a id="id-1.11.7.35.9"></a><a id="id-1.11.7.35.10"></a>

此模組提供 `pg_buffercache_pages()` 函式（包裝於 `pg_buffercache` 檢視表中）、`pg_buffercache_numa_pages()` 函式（包裝於 `pg_buffercache_numa` 檢視表中）、`pg_buffercache_summary()` 函式、`pg_buffercache_usage_counts()` 函式、`pg_buffercache_evict()` 函式、`pg_buffercache_evict_relation()` 函式，以及 `pg_buffercache_evict_all()` 函式。

`pg_buffercache_pages()` 函式傳回一組紀錄，每個資料列描述一個共享緩衝區項目的狀態。`pg_buffercache` 檢視表包裝了此函式，以便於使用。

`pg_buffercache_numa_pages()` 函式提供共享緩衝區項目對應到 NUMA 節點的資訊。此資訊不屬於 `pg_buffercache_pages()` 本身，因為擷取它要慢得多。`pg_buffercache_numa` 檢視表包裝了此函式，以便於使用。

`pg_buffercache_summary()` 函式傳回單一資料列，彙總共享緩衝區快取的狀態。

`pg_buffercache_usage_counts()` 函式傳回一組紀錄，每個資料列描述具有某個使用計數的緩衝區數量。

預設情況下，上述函式僅限超級使用者及具有 `pg_monitor` 角色權限的角色使用。可以使用 `GRANT` 將存取權授予其他人。

`pg_buffercache_evict()` 函式可在給定緩衝區識別碼時，將一個區塊從緩衝池中逐出。此函式僅限超級使用者使用。

`pg_buffercache_evict_relation()` 函式可在給定關聯識別碼時，將該關聯中所有未被釘住（unpinned）的共享緩衝區從緩衝池中逐出。此函式僅限超級使用者使用。

`pg_buffercache_evict_all()` 函式可將緩衝池中所有未被釘住的共享緩衝區逐出。此函式僅限超級使用者使用。

### F.25.1. `pg_buffercache` 檢視表 [#](#pgbuffercache-pg-buffercache) <a href="#pgbuffercache-pg-buffercache" id="pgbuffercache-pg-buffercache"></a>

完整內容請見 [F.25.1. pg_buffercache 檢視表](pgbuffercache/pgbuffercache-pg-buffercache.md#pgbuffercache-pg-buffercache)。

### F.25.2. `pg_buffercache_numa` 檢視表 [#](#pgbuffercache-pg-buffercache-numa) <a href="#pgbuffercache-pg-buffercache-numa" id="pgbuffercache-pg-buffercache-numa"></a>

完整內容請見 [F.25.2. pg_buffercache_numa 檢視表](pgbuffercache/pgbuffercache-pg-buffercache-numa.md#pgbuffercache-pg-buffercache-numa)。

### F.25.3. `pg_buffercache_summary()` 函式 [#](#pgbuffercache-summary) <a href="#pgbuffercache-summary" id="pgbuffercache-summary"></a>

完整內容請見 [F.25.3. pg_buffercache_summary() 函式](pgbuffercache/pgbuffercache-summary.md#pgbuffercache-summary)。

### F.25.4. `pg_buffercache_usage_counts()` 函式 [#](#pgbuffercache-usage-counts) <a href="#pgbuffercache-usage-counts" id="pgbuffercache-usage-counts"></a>

完整內容請見 [F.25.4. pg_buffercache_usage_counts() 函式](pgbuffercache/pgbuffercache-usage-counts.md#pgbuffercache-usage-counts)。

<a id="PGBUFFERCACHE-PG-BUFFERCACHE-EVICT"></a>

### F.25.5. `pg_buffercache_evict()` 函式 [#](#pgbuffercache-pg-buffercache-evict) <a href="#pgbuffercache-pg-buffercache-evict" id="pgbuffercache-pg-buffercache-evict"></a>

`pg_buffercache_evict()` 函式接受一個緩衝區識別碼，即 `bufferid` 欄位中所顯示者（屬於 `pg_buffercache` 檢視表）。它傳回該緩衝區是否已被逐出以及是否已被刷寫的資訊。成功時 buffer_evicted 欄位為 true；若緩衝區無效、因被釘住而無法逐出，或在嘗試將其寫出後又再度變髒，則為 false。若緩衝區已被刷寫，buffer_flushed 欄位為 true。這不一定表示該緩衝區是由我們刷寫的，也可能是由其他人刷寫的。結果在傳回的當下就已過時，因為並行活動可能隨時使該緩衝區再次變為有效。此函式僅供開發人員測試使用。

<a id="PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION"></a>

### F.25.6. `pg_buffercache_evict_relation()` 函式 [#](#pgbuffercache-pg-buffercache-evict-relation) <a href="#pgbuffercache-pg-buffercache-evict-relation" id="pgbuffercache-pg-buffercache-evict-relation"></a>

`pg_buffercache_evict_relation()` 函式與 `pg_buffercache_evict()` 函式非常相似。差別在於 `pg_buffercache_evict_relation()` 接受的是關聯識別碼，而不是緩衝區識別碼。它會嘗試逐出該關聯所有分支的所有緩衝區。它傳回已逐出的緩衝區數量、已刷寫的緩衝區數量，以及無法逐出的緩衝區數量。已刷寫的緩衝區不一定是由我們刷寫的，也可能是由其他人刷寫的。結果在傳回的當下就已過時，因為並行活動可能使緩衝區立即被再次讀入。此函式僅供開發人員測試使用。

<a id="PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL"></a>

### F.25.7. `pg_buffercache_evict_all()` 函式 [#](#pgbuffercache-pg-buffercache-evict-all) <a href="#pgbuffercache-pg-buffercache-evict-all" id="pgbuffercache-pg-buffercache-evict-all"></a>

`pg_buffercache_evict_all()` 函式與 `pg_buffercache_evict()` 函式非常相似。差別在於 `pg_buffercache_evict_all()` 函式不接受參數，而是嘗試逐出緩衝池中的所有緩衝區。它傳回已逐出的緩衝區數量、已刷寫的緩衝區數量，以及無法逐出的緩衝區數量。已刷寫的緩衝區不一定是由我們刷寫的，也可能是由其他人刷寫的。結果在傳回的當下就已過時，因為並行活動可能使緩衝區立即被再次讀入。此函式僅供開發人員測試使用。

<a id="PGBUFFERCACHE-SAMPLE-OUTPUT"></a>

### F.25.8. 輸出範例 [#](#pgbuffercache-sample-output) <a href="#pgbuffercache-sample-output" id="pgbuffercache-sample-output"></a>

```

regression=# SELECT n.nspname, c.relname, count(*) AS buffers
             FROM pg_buffercache b JOIN pg_class c
             ON b.relfilenode = pg_relation_filenode(c.oid) AND
                b.reldatabase IN (0, (SELECT oid FROM pg_database
                                      WHERE datname = current_database()))
             JOIN pg_namespace n ON n.oid = c.relnamespace
             GROUP BY n.nspname, c.relname
             ORDER BY 3 DESC
             LIMIT 10;

  nspname   |        relname         | buffers
------------+------------------------+---------
 public     | delete_test_table      |     593
 public     | delete_test_table_pkey |     494
 pg_catalog | pg_attribute           |     472
 public     | quad_poly_tbl          |     353
 public     | tenk2                  |     349
 public     | tenk1                  |     349
 public     | gin_test_idx           |     306
 pg_catalog | pg_largeobject         |     206
 public     | gin_test_tbl           |     188
 public     | spgist_text_tbl        |     182
(10 rows)


regression=# SELECT * FROM pg_buffercache_summary();
 buffers_used | buffers_unused | buffers_dirty | buffers_pinned | usagecount_avg
--------------+----------------+---------------+----------------+----------------
          248 |        2096904 |            39 |              0 |       3.141129
(1 row)


regression=# SELECT * FROM pg_buffercache_usage_counts();
 usage_count | buffers | dirty | pinned
-------------+---------+-------+--------
           0 |   14650 |     0 |      0
           1 |    1436 |   671 |      0
           2 |     102 |    88 |      0
           3 |      23 |    21 |      0
           4 |       9 |     7 |      0
           5 |     164 |   106 |      0
(6 rows)
```

<a id="PGBUFFERCACHE-AUTHORS"></a>

### F.25.9. 作者 [#](#pgbuffercache-authors) <a href="#pgbuffercache-authors" id="pgbuffercache-authors"></a>

Mark Kirkwood `<markir@paradise.net.nz>`

設計建議：Neil Conway `<neilc@samurai.com>`

除錯建議：Tom Lane `<tgl@sss.pgh.pa.us>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgbuffercache.html)（原文版本：18.6；核對日期：2026-10-23）
