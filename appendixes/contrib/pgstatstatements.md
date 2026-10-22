<a id="PGSTATSTATEMENTS"></a>

## F.32. pg_stat_statements — 追蹤 SQL 規劃與執行的統計資訊 [#](#PGSTATSTATEMENTS)

[F.32.1. `pg_stat_statements` 檢視表](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)

[F.32.2. `pg_stat_statements_info` 檢視表](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)

[F.32.3. 函式](pgstatstatements.md#PGSTATSTATEMENTS-FUNCS)

[F.32.4. 設定參數](pgstatstatements.md#PGSTATSTATEMENTS-CONFIG-PARAMS)

[F.32.5. 輸出範例](pgstatstatements.md#PGSTATSTATEMENTS-SAMPLE-OUTPUT)

[F.32.6. 作者](pgstatstatements.md#PGSTATSTATEMENTS-AUTHORS)

<a id="id-1.11.7.42.2"></a>

`pg_stat_statements` 模組提供一種方式，用來追蹤伺服器所執行之所有 SQL 陳述式的規劃與執行統計資訊。

此模組必須透過在 `postgresql.conf` 的 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 中加入 `pg_stat_statements` 來載入，因為它需要額外的共享記憶體。這表示新增或移除此模組都需要重新啟動伺服器。此外，必須啟用查詢識別碼計算，此模組才會運作；若 [compute_query_id](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) 設為 `auto` 或 `on`，或已載入任何會計算查詢識別碼的第三方模組，就會自動啟用此計算。

`pg_stat_statements` 啟用時，會追蹤伺服器上所有資料庫的統計資訊。為了存取與操作這些統計資訊，此模組提供檢視表 `pg_stat_statements` 與 `pg_stat_statements_info`，以及公用函式 `pg_stat_statements_reset` 與 `pg_stat_statements`。這些並非全域可用，但可以用 `CREATE EXTENSION pg_stat_statements` 為特定資料庫啟用。

<a id="PGSTATSTATEMENTS-PG-STAT-STATEMENTS"></a>

### F.32.1. `pg_stat_statements` 檢視表 [#](#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)

此模組所收集的統計資訊，透過名為 `pg_stat_statements` 的檢視表提供。對於資料庫 ID、使用者 ID、查詢 ID 以及是否為頂層陳述式的每一種不同組合，此檢視表各包含一筆資料列（最多到此模組所能追蹤的不同陳述式數量上限）。此檢視表的欄位列於[表 F.22](pgstatstatements.md#PGSTATSTATEMENTS-COLUMNS)。

<a id="PGSTATSTATEMENTS-COLUMNS"></a>

**表 F.22. `pg_stat_statements` 欄位**

<table border="1" class="table" summary="表 F.22. pg_stat_statements 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">userid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../internals/catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       執行該陳述式之使用者的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dbid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../internals/catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       執行該陳述式所在資料庫的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">toplevel</code> <code class="type">bool</code>
</p>
<p>
       若該查詢是以頂層陳述式執行，則為真（若 <code class="varname">pg_stat_statements.track</code> 設為 <code class="literal">top</code>，則一律為真）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">queryid</code> <code class="type">bigint</code>
</p>
<p>
       用來識別相同之正規化查詢的雜湊碼。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">query</code> <code class="type">text</code>
</p>
<p>
       代表性陳述式的文字
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">plans</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式被規劃的次數（若已啟用 <code class="varname">pg_stat_statements.track_planning</code>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       規劃該陳述式所花費的總時間，以毫秒為單位（若已啟用 <code class="varname">pg_stat_statements.track_planning</code>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">min_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       規劃該陳述式所花費的最短時間，以毫秒為單位。若停用 <code class="varname">pg_stat_statements.track_planning</code>，或者計數器已透過 <code class="function">pg_stat_statements_reset</code> 函式並將 <code class="structfield">minmax_only</code> 參數設為 <code class="literal">true</code> 而重設、且此後未曾再被規劃，則此欄位為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       規劃該陳述式所花費的最長時間，以毫秒為單位。若停用 <code class="varname">pg_stat_statements.track_planning</code>，或者計數器已透過 <code class="function">pg_stat_statements_reset</code> 函式並將 <code class="structfield">minmax_only</code> 參數設為 <code class="literal">true</code> 而重設、且此後未曾再被規劃，則此欄位為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">mean_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       規劃該陳述式所花費的平均時間，以毫秒為單位（若已啟用 <code class="varname">pg_stat_statements.track_planning</code>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stddev_plan_time</code> <code class="type">double precision</code>
</p>
<p>
       規劃該陳述式所花費時間的母體標準差，以毫秒為單位（若已啟用 <code class="varname">pg_stat_statements.track_planning</code>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">calls</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式被執行的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">total_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       執行該陳述式所花費的總時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">min_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       執行該陳述式所花費的最短時間，以毫秒為單位；在透過 <code class="function">pg_stat_statements_reset</code> 函式並將 <code class="structfield">minmax_only</code> 參數設為 <code class="literal">true</code> 執行重設之後，直到該陳述式首次執行之前，此欄位為零
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       執行該陳述式所花費的最長時間，以毫秒為單位；在透過 <code class="function">pg_stat_statements_reset</code> 函式並將 <code class="structfield">minmax_only</code> 參數設為 <code class="literal">true</code> 執行重設之後，直到該陳述式首次執行之前，此欄位為零
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">mean_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       執行該陳述式所花費的平均時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stddev_exec_time</code> <code class="type">double precision</code>
</p>
<p>
       執行該陳述式所花費時間的母體標準差，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">rows</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所擷取或影響的資料列總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式的共享區塊快取命中總次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所讀取的共享區塊總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blks_dirtied</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所弄髒的共享區塊總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blks_written</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所寫入的共享區塊總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blks_hit</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式的本地區塊快取命中總次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所讀取的本地區塊總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blks_dirtied</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所弄髒的本地區塊總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blks_written</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所寫入的本地區塊總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blks_read</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所讀取的暫存區塊總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blks_written</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所寫入的暫存區塊總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式讀取共享區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式寫入共享區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式讀取本地區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式寫入本地區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式讀取暫存檔區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式寫入暫存檔區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_records</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所產生的 WAL 記錄總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_fpi</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式所產生的 WAL 完整頁面映像總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_bytes</code> <code class="type">numeric</code>
</p>
<p>
       該陳述式所產生的 WAL 總量，以位元組為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">wal_buffers_full</code> <code class="type">bigint</code>
</p>
<p>
       WAL 緩衝區已滿的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_functions</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式經 JIT 編譯的函式總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_generation_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式產生 JIT 程式碼所花費的總時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_inlining_count</code> <code class="type">bigint</code>
</p>
<p>
       函式被內嵌的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_inlining_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式內嵌函式所花費的總時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_optimization_count</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式被最佳化的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_optimization_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式進行最佳化所花費的總時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_emission_count</code> <code class="type">bigint</code>
</p>
<p>
       程式碼被發出（emit）的次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_emission_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式發出程式碼所花費的總時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_deform_count</code> <code class="type">bigint</code>
</p>
<p>
       該陳述式經 JIT 編譯的元組解構（tuple deform）函式總數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">jit_deform_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式以 JIT 編譯元組解構函式所花費的總時間，以毫秒為單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parallel_workers_to_launch</code> <code class="type">bigint</code>
</p>
<p>
       預計啟動的平行工作程序數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">parallel_workers_launched</code> <code class="type">bigint</code>
</p>
<p>
       實際啟動的平行工作程序數量
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_since</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       開始為該陳述式收集統計資訊的時間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">minmax_stats_since</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       開始為該陳述式收集最小／最大值統計資訊的時間（欄位 <code class="structfield">min_plan_time</code>、<code class="structfield">max_plan_time</code>、<code class="structfield">min_exec_time</code> 與 <code class="structfield">max_exec_time</code>）
      </p></td></tr></tbody></table>

<br>

基於安全考量，只有超級使用者以及具有 `pg_read_all_stats` 角色權限的角色，才能查看其他使用者所執行查詢的 SQL 文字與 `queryid`。不過，若此檢視表已安裝在其他使用者的資料庫中，他們仍可以查看統計資訊。

可規劃的查詢（也就是 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 與 `MERGE`）與公用程式命令，只要依內部雜湊計算具有相同的查詢結構，就會合併為單一 `pg_stat_statements` 項目。一般而言，若兩個查詢除了其中出現的字面常數值之外語意相同，就此目的而言會被視為相同。

### 注意

以下關於常數替換與 `queryid` 的細節，只在啟用 [compute_query_id](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) 時適用。若你改用外部模組來計算 `queryid`，應該參閱該模組的文件以了解細節。

當某個常數的值為了將該查詢與其他查詢比對而被忽略時，該常數在 `pg_stat_statements` 的顯示中會以參數符號（例如 `$1`）取代。查詢文字的其餘部分，則取自第一個具有與該 `pg_stat_statements` 項目相關聯之特定 `queryid` 雜湊值的查詢。

可套用正規化的查詢，在 `pg_stat_statements` 中仍可能以帶有常數值的形式出現，尤其是在項目釋放的頻率很高時。為了降低發生這種情況的可能性，請考慮增加 `pg_stat_statements.max`。下文[第 F.32.2 節](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)所討論的 `pg_stat_statements_info` 檢視表，提供有關項目釋放的統計資訊。

在某些情況下，文字明顯不同的查詢可能會被合併為單一 `pg_stat_statements` 項目；如上所述，對於語意相同的查詢，這是預期中的行為。此外，若查詢之間唯一的差異是常數清單中的元素個數，該清單會被壓縮為單一元素，但會附上一個被註解掉的清單標示來顯示：

```

=# SELECT pg_stat_statements_reset();
=# SELECT * FROM test WHERE a IN (1, 2, 3, 4, 5, 6, 7);
=# SELECT * FROM test WHERE a IN (1, 2, 3, 4, 5, 6, 7, 8);
=# SELECT query, calls FROM pg_stat_statements
   WHERE query LIKE 'SELECT%';
-[ RECORD 1 ]------------------------------
query | SELECT * FROM test WHERE a IN ($1 /*, ... */)
calls | 2
```

除了這些情況之外，也有很小的機率因雜湊碰撞而使不相關的查詢被合併為一個項目。（不過，屬於不同使用者或不同資料庫的查詢不會發生這種情況。）

由於 `queryid` 雜湊值是根據查詢經剖析分析後的表示形式計算的，相反的情況也可能發生：文字完全相同的查詢，若因為 `search_path` 設定不同等因素而具有不同意義，可能會顯示為不同的項目。

`pg_stat_statements` 的使用者可能會希望以 `queryid`（或許再搭配 `dbid` 與 `userid`）作為每個項目比查詢文字更穩定、更可靠的識別碼。然而，必須了解 `queryid` 雜湊值的穩定性只有有限的保證。由於此識別碼是從剖析分析後的樹狀結構推導而來，其值除了其他因素之外，也取決於出現在此表示形式中的內部物件識別碼。這會帶來一些違反直覺的結果。例如，若兩個看似相同的查詢參照了（舉例而言）某個在兩次查詢執行之間被移除並重新建立的函式，`pg_stat_statements` 會將它們視為不同的查詢。反過來說，若某個資料表在查詢執行之間被移除並重新建立，兩個看似相同的查詢可能會被視為相同。不過，若其他方面相似的查詢中資料表的別名不同，這些查詢會被視為不同。雜湊處理也會受到機器架構差異以及平台其他層面的影響。此外，假設 `queryid` 在 PostgreSQL 的不同主要版本之間保持穩定並不安全。

參與以實體 WAL 重播為基礎之複寫的兩台伺服器，可以預期對同一查詢具有相同的 `queryid` 值。然而，邏輯複寫機制並不保證讓複本在所有相關細節上都保持相同，因此 `queryid` 不適合作為在一組邏輯複本之間累計成本的識別碼。若有疑慮，建議直接進行測試。

一般而言，只要執行個體在相同的機器架構上執行，且系統目錄的中繼資料細節相符，就可以假設 `queryid` 值在 PostgreSQL 的次要版本之間是穩定的。只有在萬不得已時，才會在次要版本之間破壞相容性。

在代表性查詢文字中用來取代常數的參數符號，會從原始查詢文字中最大的 `$`*`n`* 參數的下一個編號開始；若原本沒有參數，則從 `$1` 開始。值得注意的是，在某些情況下可能存在會影響此編號的隱藏參數符號。例如，PL/pgSQL 會使用隱藏參數符號將函式區域變數的值插入查詢中，因此像 `SELECT i + 1 INTO j` 這樣的 PL/pgSQL 陳述式，其代表性文字會類似 `SELECT i + $2`。

代表性查詢文字保存在外部磁碟檔案中，不會占用共享記憶體。因此，即使是非常長的查詢文字也能成功儲存。然而，若累積了許多長的查詢文字，外部檔案可能會增長到難以管理的大小。作為發生這種情況時的復原方法，`pg_stat_statements` 可能會選擇捨棄查詢文字，此時 `pg_stat_statements` 檢視表中所有現有項目的 `query` 欄位都會顯示為 null，但與每個 `queryid` 相關聯的統計資訊仍會保留。若發生這種情況，請考慮減少 `pg_stat_statements.max` 以避免再次發生。

`plans` 與 `calls` 不一定會相符，因為規劃與執行的統計資訊分別在各自的結束階段更新，而且只針對成功的操作更新。例如，若某個陳述式規劃成功，但在執行階段失敗，則只有其規劃統計資訊會被更新。若因為使用了快取的計畫而略過規劃，則只有其執行統計資訊會被更新。

<a id="PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO"></a>

### F.32.2. `pg_stat_statements_info` 檢視表 [#](#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)

<a id="id-1.11.7.42.7.2"></a>

`pg_stat_statements` 模組本身的統計資訊也會被追蹤，並透過名為 `pg_stat_statements_info` 的檢視表提供。此檢視表只包含單一資料列。此檢視表的欄位列於[表 F.23](pgstatstatements.md#PGSTATSTATEMENTSINFO-COLUMNS)。

<a id="PGSTATSTATEMENTSINFO-COLUMNS"></a>

**表 F.23. `pg_stat_statements_info` 欄位**

<table border="1" class="table" summary="表 F.23. pg_stat_statements_info 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dealloc</code> <code class="type">bigint</code>
</p>
<p>
       <code class="structname">pg_stat_statements</code> 中有關執行次數最少之陳述式的項目，因觀察到的不同陳述式超過 <code class="varname">pg_stat_statements.max</code> 個而被釋放的總次數
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">stats_reset</code> <code class="type">timestamp with time zone</code>
</p>
<p>
       <code class="structname">pg_stat_statements</code> 檢視表中所有統計資訊最後一次重設的時間。
      </p></td></tr></tbody></table>

<br>

<a id="PGSTATSTATEMENTS-FUNCS"></a>

### F.32.3. 函式 [#](#PGSTATSTATEMENTS-FUNCS)

`pg_stat_statements_reset(userid Oid, dbid Oid, queryid bigint, minmax_only boolean) returns timestamp with time zone` <a id="id-1.11.7.42.8.2.1.1.2"></a>
:   `pg_stat_statements_reset` 會捨棄 `pg_stat_statements` 至今所收集、與指定之 `userid`、`dbid` 及 `queryid` 相對應的統計資訊。若有任何參數未指定，這些參數都會使用預設值 `0`（無效），並重設符合其他參數的統計資訊。若未指定任何參數，或所有指定的參數皆為 `0`（無效），則會捨棄所有統計資訊。若 `pg_stat_statements` 檢視表中的所有統計資訊都被捨棄，也會一併重設 `pg_stat_statements_info` 檢視表中的統計資訊。當 `minmax_only` 為 `true` 時，只會重設規劃與執行時間的最小值與最大值（亦即 `min_plan_time`、`max_plan_time`、`min_exec_time` 與 `max_exec_time` 欄位）。`minmax_only` 參數的預設值為 `false`。最後一次執行最小／最大值重設的時間，顯示在 `pg_stat_statements` 檢視表的 `minmax_stats_since` 欄位中。此函式會傳回重設的時間。若確實執行了相對應的重設，此時間會儲存到 `pg_stat_statements_info` 檢視表的 `stats_reset` 欄位，或 `pg_stat_statements` 檢視表的 `minmax_stats_since` 欄位。預設情況下，只有超級使用者可以執行此函式。可以使用 `GRANT` 將存取權授與其他人。

`pg_stat_statements(showtext boolean) returns setof record` <a id="id-1.11.7.42.8.2.2.1.2"></a>
:   `pg_stat_statements` 檢視表是以一個同樣名為 `pg_stat_statements` 的函式來定義的。用戶端可以直接呼叫 `pg_stat_statements` 函式，並藉由指定 `showtext := false` 來省略查詢文字（也就是說，對應於檢視表 `query` 欄位的 `OUT` 參數會傳回 null）。此功能旨在支援可能希望避免反覆擷取長度不定之查詢文字所造成負擔的外部工具。這類工具可以改為自行快取每個項目所觀察到的第一個查詢文字，因為 `pg_stat_statements` 本身也只是這麼做，之後只在需要時才擷取查詢文字。由於伺服器將查詢文字儲存在檔案中，這種做法可能減少反覆檢視 `pg_stat_statements` 資料時的實體 I/O。

<a id="PGSTATSTATEMENTS-CONFIG-PARAMS"></a>

### F.32.4. 設定參數 [#](#PGSTATSTATEMENTS-CONFIG-PARAMS)

`pg_stat_statements.max` (`integer`) <a id="id-1.11.7.42.9.2.1.1.3"></a>
:   `pg_stat_statements.max` 是此模組所追蹤之陳述式的最大數量（亦即 `pg_stat_statements` 檢視表中資料列的最大數量）。若觀察到的不同陳述式超過此數量，有關執行次數最少之陳述式的資訊就會被捨棄。此類資訊被捨棄的次數，可以在 `pg_stat_statements_info` 檢視表中查看。預設值為 5000。此參數只能在伺服器啟動時設定。

`pg_stat_statements.track` (`enum`) <a id="id-1.11.7.42.9.2.2.1.3"></a>
:   `pg_stat_statements.track` 控制此模組要計入哪些陳述式。指定 `top` 會追蹤頂層陳述式（由用戶端直接發出的陳述式），指定 `all` 會連巢狀陳述式（例如在函式中呼叫的陳述式）也一併追蹤，指定 `none` 則會停用陳述式統計資訊的收集。預設值為 `top`。只有超級使用者可以變更此設定。

`pg_stat_statements.track_utility` (`boolean`) <a id="id-1.11.7.42.9.2.3.1.3"></a>
:   `pg_stat_statements.track_utility` 控制此模組是否追蹤公用程式命令。公用程式命令是指 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 與 `MERGE` 以外的所有命令。預設值為 `on`。只有超級使用者可以變更此設定。

`pg_stat_statements.track_planning` (`boolean`) <a id="id-1.11.7.42.9.2.4.1.3"></a>
:   `pg_stat_statements.track_planning` 控制此模組是否追蹤規劃操作及其持續時間。啟用此參數可能造成明顯的效能損失，尤其是當具有相同查詢結構的陳述式由許多並行連線執行、而這些連線競相更新少數幾個 `pg_stat_statements` 項目時。預設值為 `off`。只有超級使用者可以變更此設定。

`pg_stat_statements.save` (`boolean`) <a id="id-1.11.7.42.9.2.5.1.3"></a>
:   `pg_stat_statements.save` 指定是否要在伺服器關閉後保留陳述式統計資訊。若設為 `off`，則統計資訊既不會在關閉時保存，也不會在伺服器啟動時重新載入。預設值為 `on`。此參數只能在 `postgresql.conf` 檔案中或伺服器命令列上設定。

此模組需要與 `pg_stat_statements.max` 成正比的額外共享記憶體。請注意，只要載入此模組就會占用這些記憶體，即使 `pg_stat_statements.track` 設為 `none` 也一樣。

這些參數必須在 `postgresql.conf` 中設定。典型的用法可能如下：

```

# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

compute_query_id = on
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

<a id="PGSTATSTATEMENTS-SAMPLE-OUTPUT"></a>

### F.32.5. 輸出範例 [#](#PGSTATSTATEMENTS-SAMPLE-OUTPUT)

```

bench=# SELECT pg_stat_statements_reset();

$ pgbench -i bench
$ pgbench -c10 -t300 bench

bench=# \x
bench=# SELECT query, calls, total_exec_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;
-[ RECORD 1 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_branches SET bbalance = bbalance + $1 WHERE bid = $2
calls           | 3000
total_exec_time | 25565.855387
rows            | 3000
hit_percent     | 100.0000000000000000
-[ RECORD 2 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_tellers SET tbalance = tbalance + $1 WHERE tid = $2
calls           | 3000
total_exec_time | 20756.669379
rows            | 3000
hit_percent     | 100.0000000000000000
-[ RECORD 3 ]---+--------------------------------------------------​------------------
query           | copy pgbench_accounts from stdin
calls           | 1
total_exec_time | 291.865911
rows            | 100000
hit_percent     | 100.0000000000000000
-[ RECORD 4 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_accounts SET abalance = abalance + $1 WHERE aid = $2
calls           | 3000
total_exec_time | 271.232977
rows            | 3000
hit_percent     | 98.8454011741682975
-[ RECORD 5 ]---+--------------------------------------------------​------------------
query           | alter table pgbench_accounts add primary key (aid)
calls           | 1
total_exec_time | 160.588563
rows            | 0
hit_percent     | 100.0000000000000000


bench=# SELECT pg_stat_statements_reset(0,0,s.queryid) FROM pg_stat_statements AS s
            WHERE s.query = 'UPDATE pgbench_branches SET bbalance = bbalance + $1 WHERE bid = $2';

bench=# SELECT query, calls, total_exec_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;
-[ RECORD 1 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_tellers SET tbalance = tbalance + $1 WHERE tid = $2
calls           | 3000
total_exec_time | 20756.669379
rows            | 3000
hit_percent     | 100.0000000000000000
-[ RECORD 2 ]---+--------------------------------------------------​------------------
query           | copy pgbench_accounts from stdin
calls           | 1
total_exec_time | 291.865911
rows            | 100000
hit_percent     | 100.0000000000000000
-[ RECORD 3 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_accounts SET abalance = abalance + $1 WHERE aid = $2
calls           | 3000
total_exec_time | 271.232977
rows            | 3000
hit_percent     | 98.8454011741682975
-[ RECORD 4 ]---+--------------------------------------------------​------------------
query           | alter table pgbench_accounts add primary key (aid)
calls           | 1
total_exec_time | 160.588563
rows            | 0
hit_percent     | 100.0000000000000000
-[ RECORD 5 ]---+--------------------------------------------------​------------------
query           | vacuum analyze pgbench_accounts
calls           | 1
total_exec_time | 136.448116
rows            | 0
hit_percent     | 99.9201915403032721

bench=# SELECT pg_stat_statements_reset(0,0,0);

bench=# SELECT query, calls, total_exec_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;
-[ RECORD 1 ]---+--------------------------------------------------​---------------------------
query           | SELECT pg_stat_statements_reset(0,0,0)
calls           | 1
total_exec_time | 0.189497
rows            | 1
hit_percent     |
-[ RECORD 2 ]---+--------------------------------------------------​---------------------------
query           | SELECT query, calls, total_exec_time, rows, $1 * shared_blks_hit /          +
                |                nullif(shared_blks_hit + shared_blks_read, $2) AS hit_percent+
                |           FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT $3
calls           | 0
total_exec_time | 0
rows            | 0
hit_percent     |
```

<a id="PGSTATSTATEMENTS-AUTHORS"></a>

### F.32.6. 作者 [#](#PGSTATSTATEMENTS-AUTHORS)

Takahiro Itagaki `<itagaki.takahiro@oss.ntt.co.jp>`。查詢正規化由 Peter Geoghegan `<peter@2ndquadrant.com>` 加入。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgstatstatements.html)（原文版本：18.6；核對日期：2026-10-23）
