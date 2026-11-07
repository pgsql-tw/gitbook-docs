# F.32.1. pg_stat_statements 檢視表

<a id="PGSTATSTATEMENTS-PG-STAT-STATEMENTS"></a>

## F.32.1. `pg_stat_statements` 檢視表 [#](#pgstatstatements-pg-stat-statements) <a href="#pgstatstatements-pg-stat-statements" id="pgstatstatements-pg-stat-statements"></a>

此模組所收集的統計資訊，透過名為 `pg_stat_statements` 的檢視表提供。對於資料庫 ID、使用者 ID、查詢 ID 以及是否為頂層陳述式的每一種不同組合，此檢視表各包含一筆資料列（最多到此模組所能追蹤的不同陳述式數量上限）。此檢視表的欄位列於[表 F.22](#pgstatstatements-columns)。

<a id="PGSTATSTATEMENTS-COLUMNS"></a>

### 表 F.22. `pg_stat_statements` 欄位 [#](#pgstatstatements-columns) <a href="#pgstatstatements-columns" id="pgstatstatements-columns"></a>

<table border="1" class="table" summary="表 F.22. pg_stat_statements 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">userid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../../internals/catalogs/catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       執行該陳述式之使用者的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dbid</code> <code class="type">oid</code>
       （參照 <a class="link" href="../../../internals/catalogs/catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>）
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
       該陳述式讀取共享區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">shared_blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式寫入共享區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式讀取本地區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">local_blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式寫入本地區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blk_read_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式讀取暫存檔區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">temp_blk_write_time</code> <code class="type">double precision</code>
</p>
<p>
       該陳述式寫入暫存檔區塊所花費的總時間，以毫秒為單位（若已啟用 <a class="xref" href="../../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-IO-TIMING">track_io_timing</a>；否則為零）
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

以下關於常數替換與 `queryid` 的細節，只在啟用 [compute_query_id](../../../server-administration/runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) 時適用。若你改用外部模組來計算 `queryid`，應該參閱該模組的文件以了解細節。

當某個常數的值為了將該查詢與其他查詢比對而被忽略時，該常數在 `pg_stat_statements` 的顯示中會以參數符號（例如 `$1`）取代。查詢文字的其餘部分，則取自第一個具有與該 `pg_stat_statements` 項目相關聯之特定 `queryid` 雜湊值的查詢。

可套用正規化的查詢，在 `pg_stat_statements` 中仍可能以帶有常數值的形式出現，尤其是在項目釋放的頻率很高時。為了降低發生這種情況的可能性，請考慮增加 `pg_stat_statements.max`。下文[第 F.32.2 節](pgstatstatements-pg-stat-statements-info.md#pgstatstatements-pg-stat-statements-info)所討論的 `pg_stat_statements_info` 檢視表，提供有關項目釋放的統計資訊。

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

[返回 F.32. pg_stat_statements — 追蹤 SQL 規劃與執行的統計資訊](../pgstatstatements.md#pgstatstatements)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgstatstatements.html)（原文版本：18.6；核對日期：2026-10-23）
