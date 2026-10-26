<a id="PGBUFFERCACHE"></a>

## F.25. pg_buffercache — 檢查 PostgreSQL 緩衝區快取狀態 [#](#pgbuffercache) <a href="#pgbuffercache" id="pgbuffercache"></a>

[F.25.1. `pg_buffercache` 檢視表](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE)

[F.25.2. `pg_buffercache_numa` 檢視表](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA)

[F.25.3. `pg_buffercache_summary()` 函式](pgbuffercache.md#PGBUFFERCACHE-SUMMARY)

[F.25.4. `pg_buffercache_usage_counts()` 函式](pgbuffercache.md#PGBUFFERCACHE-USAGE-COUNTS)

[F.25.5. `pg_buffercache_evict()` 函式](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT)

[F.25.6. `pg_buffercache_evict_relation()` 函式](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION)

[F.25.7. `pg_buffercache_evict_all()` 函式](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL)

[F.25.8. 輸出範例](pgbuffercache.md#PGBUFFERCACHE-SAMPLE-OUTPUT)

[F.25.9. 作者](pgbuffercache.md#PGBUFFERCACHE-AUTHORS)

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

<a id="PGBUFFERCACHE-PG-BUFFERCACHE"></a>

### F.25.1. `pg_buffercache` 檢視表 [#](#PGBUFFERCACHE-PG-BUFFERCACHE)

此檢視表所提供欄位的定義如[表 F.14](pgbuffercache.md#PGBUFFERCACHE-COLUMNS)所示。

<a id="PGBUFFERCACHE-COLUMNS"></a>

**表 F.14. `pg_buffercache` 欄位**

<table border="1" class="table" summary="pg_buffercache 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bufferid</code> <code class="type">integer</code>
</p>
<p>
       ID，範圍為 1..<code class="varname">shared_buffers</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relfilenode</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../internals/catalogs/catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relfilenode</code>）
      </p>
<p>
       關聯的檔案節點（filenode）編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltablespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../internals/catalogs/catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       關聯的資料表空間 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reldatabase</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../internals/catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       關聯的資料庫 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relforknumber</code> <code class="type">smallint</code>
</p>
<p>
       關聯內的分支（fork）編號；請參閱
       <code class="filename">common/relpath.h</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relblocknumber</code> <code class="type">bigint</code>
</p>
<p>
       關聯內的頁面編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">isdirty</code> <code class="type">boolean</code>
</p>
<p>
       頁面是否為髒頁？
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">usagecount</code> <code class="type">smallint</code>
</p>
<p>
       時鐘掃描（clock-sweep）存取計數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pinning_backends</code> <code class="type">integer</code>
</p>
<p>
       釘住此緩衝區的後端數量
      </p></td></tr></tbody></table>

<br>

共享快取中的每個緩衝區各有一個資料列。未使用的緩衝區除了 `bufferid` 以外，所有欄位皆顯示為 null。共享的系統目錄會顯示為屬於資料庫 0。

由於快取由所有資料庫共享，通常會有來自不屬於目前資料庫之關聯的頁面。這表示對某些資料列而言，`pg_class` 中可能沒有可與之連接的對應資料列，甚至可能產生不正確的連接。若你要與 `pg_class` 連接，最好將連接限制在 `reldatabase` 等於目前資料庫的 OID 或 0 的資料列。

由於複製此檢視表要顯示的緩衝區狀態資料時，不會取得緩衝區管理器的鎖定，存取 `pg_buffercache` 檢視表對正常緩衝區活動的影響較小，但它無法提供在所有緩衝區之間一致的結果集。不過，我們會確保每個緩衝區的資訊本身是一致的。

<a id="PGBUFFERCACHE-PG-BUFFERCACHE-NUMA"></a>

### F.25.2. `pg_buffercache_numa` 檢視表 [#](#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA)

此檢視表所提供欄位的定義如[表 F.15](pgbuffercache.md#PGBUFFERCACHE-NUMA-COLUMNS)所示。

<a id="PGBUFFERCACHE-NUMA-COLUMNS"></a>

**表 F.15. `pg_buffercache_numa` 欄位**

<table border="1" class="table" summary="pg_buffercache_numa 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bufferid</code> <code class="type">integer</code>
</p>
<p>
       ID，範圍為 1..<code class="varname">shared_buffers</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">os_page_num</code> <code class="type">bigint</code>
</p>
<p>
       此緩衝區所在的作業系統記憶體頁面編號
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">numa_node</code> <code class="type">int</code>
</p>
<p>
       <acronym class="acronym">NUMA</acronym> 節點的 ID
      </p></td></tr></tbody></table>

<br>

由於查詢每個頁面的 NUMA 節點 ID 需要先將記憶體頁面調入（page in），此函式第一次執行時可能需要相當可觀的時間。在所有情況下（無論是否為第一次執行），擷取此資訊的成本都很高，因此不建議高頻率查詢此檢視表。

### 警告

在判定 NUMA 節點時，此檢視表會存取（touch）共享記憶體區段的所有記憶體頁面。若共享記憶體尚未配置，這會強制配置它，而且記憶體可能會被配置在單一 NUMA 節點上（取決於系統設定）。

<a id="PGBUFFERCACHE-SUMMARY"></a>

### F.25.3. `pg_buffercache_summary()` 函式 [#](#PGBUFFERCACHE-SUMMARY)

此函式所提供欄位的定義如[表 F.16](pgbuffercache.md#PGBUFFERCACHE-SUMMARY-COLUMNS)所示。

<a id="PGBUFFERCACHE-SUMMARY-COLUMNS"></a>

**表 F.16. `pg_buffercache_summary()` 輸出欄位**

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

<a id="PGBUFFERCACHE-USAGE-COUNTS"></a>

### F.25.4. `pg_buffercache_usage_counts()` 函式 [#](#PGBUFFERCACHE-USAGE-COUNTS)

此函式所提供欄位的定義如[表 F.17](pgbuffercache.md#PGBUFFERCACHE_USAGE_COUNTS-COLUMNS)所示。

<a id="PGBUFFERCACHE_USAGE_COUNTS-COLUMNS"></a>

**表 F.17. `pg_buffercache_usage_counts()` 輸出欄位**

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

<a id="PGBUFFERCACHE-PG-BUFFERCACHE-EVICT"></a>

### F.25.5. `pg_buffercache_evict()` 函式 [#](#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT)

`pg_buffercache_evict()` 函式接受一個緩衝區識別碼，即 `bufferid` 欄位中所顯示者（屬於 `pg_buffercache` 檢視表）。它傳回該緩衝區是否已被逐出以及是否已被刷寫的資訊。成功時 buffer_evicted 欄位為 true；若緩衝區無效、因被釘住而無法逐出，或在嘗試將其寫出後又再度變髒，則為 false。若緩衝區已被刷寫，buffer_flushed 欄位為 true。這不一定表示該緩衝區是由我們刷寫的，也可能是由其他人刷寫的。結果在傳回的當下就已過時，因為並行活動可能隨時使該緩衝區再次變為有效。此函式僅供開發人員測試使用。

<a id="PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION"></a>

### F.25.6. `pg_buffercache_evict_relation()` 函式 [#](#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION)

`pg_buffercache_evict_relation()` 函式與 `pg_buffercache_evict()` 函式非常相似。差別在於 `pg_buffercache_evict_relation()` 接受的是關聯識別碼，而不是緩衝區識別碼。它會嘗試逐出該關聯所有分支的所有緩衝區。它傳回已逐出的緩衝區數量、已刷寫的緩衝區數量，以及無法逐出的緩衝區數量。已刷寫的緩衝區不一定是由我們刷寫的，也可能是由其他人刷寫的。結果在傳回的當下就已過時，因為並行活動可能使緩衝區立即被再次讀入。此函式僅供開發人員測試使用。

<a id="PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL"></a>

### F.25.7. `pg_buffercache_evict_all()` 函式 [#](#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL)

`pg_buffercache_evict_all()` 函式與 `pg_buffercache_evict()` 函式非常相似。差別在於 `pg_buffercache_evict_all()` 函式不接受參數，而是嘗試逐出緩衝池中的所有緩衝區。它傳回已逐出的緩衝區數量、已刷寫的緩衝區數量，以及無法逐出的緩衝區數量。已刷寫的緩衝區不一定是由我們刷寫的，也可能是由其他人刷寫的。結果在傳回的當下就已過時，因為並行活動可能使緩衝區立即被再次讀入。此函式僅供開發人員測試使用。

<a id="PGBUFFERCACHE-SAMPLE-OUTPUT"></a>

### F.25.8. 輸出範例 [#](#PGBUFFERCACHE-SAMPLE-OUTPUT)

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

### F.25.9. 作者 [#](#PGBUFFERCACHE-AUTHORS)

Mark Kirkwood `<markir@paradise.net.nz>`

設計建議：Neil Conway `<neilc@samurai.com>`

除錯建議：Tom Lane `<tgl@sss.pgh.pa.us>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgbuffercache.html)（原文版本：18.6；核對日期：2026-10-23）
