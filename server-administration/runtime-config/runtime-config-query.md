<a id="RUNTIME-CONFIG-QUERY"></a>

## 19.7. 查詢規劃 [#](#RUNTIME-CONFIG-QUERY)

[19.7.1. 規劃器方法組態設定](runtime-config-query.md#RUNTIME-CONFIG-QUERY-ENABLE)

[19.7.2. 規劃器成本常數](runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)

[19.7.3. 基因查詢最佳化器](runtime-config-query.md#RUNTIME-CONFIG-QUERY-GEQO)

[19.7.4. 其他規劃器選項](runtime-config-query.md#RUNTIME-CONFIG-QUERY-OTHER)

<a id="RUNTIME-CONFIG-QUERY-ENABLE"></a>

### 19.7.1. 規劃器方法組態設定 [#](#RUNTIME-CONFIG-QUERY-ENABLE)

這些組態設定參數提供一種粗略的方法，
用以影響查詢最佳化器所選擇的查詢計畫。若
最佳化器針對特定查詢所選擇的預設計畫
並非最佳，*暫時*的解決方式是使用
這些組態設定參數之一，強制最佳化器
選擇不同的計畫。
改善最佳化器所選計畫品質的較好方式，
包括調整規劃器成本常數（參閱[19.7.2 節](runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)）、
手動執行 [`ANALYZE`](../../reference/sql-commands/sql-analyze.md)、
提高 [default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET) 組態設定參數
的值，以及使用 `ALTER TABLE SET
STATISTICS` 增加為特定欄位收集的統計資訊量。

<a id="GUC-ENABLE-ASYNC-APPEND"></a>

`enable_async_append` (`boolean`) <a id="id-1.6.6.10.2.3.1.1.3"></a> [#](#GUC-ENABLE-ASYNC-APPEND)
:   啟用或停用查詢規劃器使用具備非同步感知能力（async-aware）
    append 計畫類型。預設值為 `on`。
<a id="GUC-ENABLE-BITMAPSCAN"></a>

`enable_bitmapscan` (`boolean`) <a id="id-1.6.6.10.2.3.2.1.3"></a> <a id="id-1.6.6.10.2.3.2.1.4"></a> [#](#GUC-ENABLE-BITMAPSCAN)
:   啟用或停用查詢規劃器使用點陣圖掃描（bitmap-scan）計畫
    類型。預設值為 `on`。
<a id="GUC-ENABLE-DISTINCT-REORDERING"></a>

`enable_distinct_reordering` (`boolean`) <a id="id-1.6.6.10.2.3.3.1.3"></a> [#](#GUC-ENABLE-DISTINCT-REORDERING)
:   啟用或停用查詢規劃器重新排序 DISTINCT
    鍵值以符合輸入路徑之路徑鍵值的能力。預設值為 `on`。
<a id="GUC-ENABLE-GATHERMERGE"></a>

`enable_gathermerge` (`boolean`) <a id="id-1.6.6.10.2.3.4.1.3"></a> [#](#GUC-ENABLE-GATHERMERGE)
:   啟用或停用查詢規劃器使用 gather
    merge 計畫類型。預設值為 `on`。
<a id="GUC-ENABLE-GROUPBY-REORDERING"></a>

`enable_group_by_reordering` (`boolean`) <a id="id-1.6.6.10.2.3.5.1.3"></a> [#](#GUC-ENABLE-GROUPBY-REORDERING)
:   控制查詢規劃器是否會產生一個計畫，使
    `GROUP BY` 鍵值依照計畫子節點
    （例如索引掃描）的鍵值順序排序。停用時，
    查詢規劃器只會產生 `GROUP BY`
    鍵值僅依 `ORDER BY` 子句（若有）排序的計畫。
    啟用時，規劃器會嘗試產生更有效率的
    計畫。預設值為 `on`。
<a id="GUC-ENABLE-HASHAGG"></a>

`enable_hashagg` (`boolean`) <a id="id-1.6.6.10.2.3.6.1.3"></a> [#](#GUC-ENABLE-HASHAGG)
:   啟用或停用查詢規劃器使用雜湊
    聚合（hashed aggregation）計畫類型。預設值為 `on`。
<a id="GUC-ENABLE-HASHJOIN"></a>

`enable_hashjoin` (`boolean`) <a id="id-1.6.6.10.2.3.7.1.3"></a> [#](#GUC-ENABLE-HASHJOIN)
:   啟用或停用查詢規劃器使用雜湊聯結（hash-join）計畫
    類型。預設值為 `on`。
<a id="GUC-ENABLE-INCREMENTAL-SORT"></a>

`enable_incremental_sort` (`boolean`) <a id="id-1.6.6.10.2.3.8.1.3"></a> [#](#GUC-ENABLE-INCREMENTAL-SORT)
:   啟用或停用查詢規劃器使用漸進式排序（incremental sort）步驟。
    預設值為 `on`。
<a id="GUC-ENABLE-INDEXSCAN"></a>

`enable_indexscan` (`boolean`) <a id="id-1.6.6.10.2.3.9.1.3"></a> <a id="id-1.6.6.10.2.3.9.1.4"></a> [#](#GUC-ENABLE-INDEXSCAN)
:   啟用或停用查詢規劃器使用索引掃描（index-scan）與
    純索引掃描（index-only-scan）計畫類型。預設值為 `on`。
    另請參閱 [enable_indexonlyscan](runtime-config-query.md#GUC-ENABLE-INDEXONLYSCAN)。
<a id="GUC-ENABLE-INDEXONLYSCAN"></a>

`enable_indexonlyscan` (`boolean`) <a id="id-1.6.6.10.2.3.10.1.3"></a> [#](#GUC-ENABLE-INDEXONLYSCAN)
:   啟用或停用查詢規劃器使用純索引掃描（index-only-scan）計畫
    類型（參閱[11.9 節](../../the-sql-language/indexes/indexes-index-only-scans.md)）。
    預設值為 `on`。查詢規劃器要考慮使用純索引掃描，
    也必須同時啟用
    [enable_indexscan](runtime-config-query.md#GUC-ENABLE-INDEXSCAN) 設定。
<a id="GUC-ENABLE-MATERIAL"></a>

`enable_material` (`boolean`) <a id="id-1.6.6.10.2.3.11.1.3"></a> [#](#GUC-ENABLE-MATERIAL)
:   啟用或停用查詢規劃器使用實體化（materialization）。
    完全抑制實體化是不可能的，
    但關閉此變數可防止規劃器插入
    materialize 節點，除非為求正確性而必須使用。
    預設值為 `on`。
<a id="GUC-ENABLE-MEMOIZE"></a>

`enable_memoize` (`boolean`) <a id="id-1.6.6.10.2.3.12.1.3"></a> [#](#GUC-ENABLE-MEMOIZE)
:   啟用或停用查詢規劃器使用 memoize 計畫，
    以在巢狀迴圈（nested-loop）聯結內快取參數化掃描的結果。
    此計畫類型允許在目前參數的結果已存在快取中時，
    略過對底層計畫的掃描。較不常被查詢的結果
    可能會在快取需要更多空間存放新項目時被淘汰。預設值為
    `on`。
<a id="GUC-ENABLE-MERGEJOIN"></a>

`enable_mergejoin` (`boolean`) <a id="id-1.6.6.10.2.3.13.1.3"></a> [#](#GUC-ENABLE-MERGEJOIN)
:   啟用或停用查詢規劃器使用合併聯結（merge-join）計畫
    類型。預設值為 `on`。
<a id="GUC-ENABLE-NESTLOOP"></a>

`enable_nestloop` (`boolean`) <a id="id-1.6.6.10.2.3.14.1.3"></a> [#](#GUC-ENABLE-NESTLOOP)
:   啟用或停用查詢規劃器使用巢狀迴圈聯結
    計畫。完全抑制巢狀迴圈聯結是不可能的，
    但關閉此變數會讓規劃器在有其他方法可用時，
    不傾向使用巢狀迴圈聯結。預設值為
    `on`。
<a id="GUC-ENABLE-PARALLEL-APPEND"></a>

`enable_parallel_append` (`boolean`) <a id="id-1.6.6.10.2.3.15.1.3"></a> [#](#GUC-ENABLE-PARALLEL-APPEND)
:   啟用或停用查詢規劃器使用具備平行感知能力的
    append 計畫類型。預設值為 `on`。
<a id="GUC-ENABLE-PARALLEL-HASH"></a>

`enable_parallel_hash` (`boolean`) <a id="id-1.6.6.10.2.3.16.1.3"></a> [#](#GUC-ENABLE-PARALLEL-HASH)
:   啟用或停用查詢規劃器使用搭配平行雜湊的
    雜湊聯結計畫類型。若未同時啟用雜湊聯結計畫，
    此設定無效果。預設值為 `on`。
<a id="GUC-ENABLE-PARTITION-PRUNING"></a>

`enable_partition_pruning` (`boolean`) <a id="id-1.6.6.10.2.3.17.1.3"></a> [#](#GUC-ENABLE-PARTITION-PRUNING)
:   啟用或停用查詢規劃器從查詢計畫中排除分割資料表
    分割區的能力。這也控制規劃器產生查詢計畫的能力，
    使查詢執行器可以在查詢執行期間移除（忽略）分割區。
    預設值為 `on`。
    詳情請參閱[5.12.4 節](../../the-sql-language/ddl/ddl-partitioning.md#DDL-PARTITION-PRUNING)。
<a id="GUC-ENABLE-PARTITIONWISE-JOIN"></a>

`enable_partitionwise_join` (`boolean`) <a id="id-1.6.6.10.2.3.18.1.3"></a> [#](#GUC-ENABLE-PARTITIONWISE-JOIN)
:   啟用或停用查詢規劃器使用分割區感知聯結（partitionwise
    join），此功能允許透過聯結對應的分割區來執行分割資料表之間的
    聯結。目前分割區感知聯結僅適用於聯結條件涵蓋
    所有分割鍵值，且這些鍵值必須是相同的資料型別，
    並具備一對一對應的子分割區集合。啟用此設定後，
    在最終計畫中，記憶體使用量受 `work_mem`
    限制的節點數量，可能會隨著被掃描的分割區數量
    呈線性成長。這可能導致查詢執行期間整體
    記憶體消耗大幅增加。查詢規劃在記憶體與 CPU 方面
    的成本也會顯著提高。預設值為 `off`。
<a id="GUC-ENABLE-PARTITIONWISE-AGGREGATE"></a>

`enable_partitionwise_aggregate` (`boolean`) <a id="id-1.6.6.10.2.3.19.1.3"></a> [#](#GUC-ENABLE-PARTITIONWISE-AGGREGATE)
:   啟用或停用查詢規劃器使用分割區感知分組或聚合
    （partitionwise grouping/aggregation），此功能允許分別對每個
    分割區執行分割資料表上的分組或聚合。如果
    `GROUP BY` 子句未包含分割鍵值，則只能
    逐分割區執行部分聚合，最終化則須在稍後執行。
    啟用此設定後，在最終計畫中，記憶體使用量受
    `work_mem` 限制的節點數量，可能會隨著被掃描的
    分割區數量呈線性成長。這可能導致查詢執行期間
    整體記憶體消耗大幅增加。查詢規劃在記憶體與 CPU 方面
    的成本也會顯著提高。預設值為
    `off`。
<a id="GUC-ENABLE-PRESORTED-AGGREGATE"></a>

`enable_presorted_aggregate` (`boolean`) <a id="id-1.6.6.10.2.3.20.1.3"></a> [#](#GUC-ENABLE-PRESORTED-AGGREGATE)
:   控制查詢規劃器是否會產生一個計畫，提供已依照
    查詢的 `ORDER BY` / `DISTINCT` 聚合
    函式所需順序預先排序的資料列。停用時，
    查詢規劃器產生的計畫，將永遠需要執行器在對含有
    `ORDER BY` 或 `DISTINCT` 子句的
    各個聚合函式進行聚合之前先執行排序。
    啟用時，規劃器會嘗試產生更有效率的計畫，
    提供已依聚合所需順序預先排序的輸入資料給聚合函式。
    預設值為
    `on`。
<a id="GUC-ENABLE-SELF-JOIN-ELIMINATION"></a>

`enable_self_join_elimination` (`boolean`) <a id="id-1.6.6.10.2.3.21.1.3"></a> [#](#GUC-ENABLE-SELF-JOIN-ELIMINATION)
:   啟用或停用查詢規劃器的最佳化功能，該功能會分析
    查詢樹，並將自我聯結（self join）替換為語意上等效的
    單一掃描。此功能僅考慮一般資料表。
    預設值為 `on`。
<a id="GUC-ENABLE-SEQSCAN"></a>

`enable_seqscan` (`boolean`) <a id="id-1.6.6.10.2.3.22.1.3"></a> <a id="id-1.6.6.10.2.3.22.1.4"></a> [#](#GUC-ENABLE-SEQSCAN)
:   啟用或停用查詢規劃器使用循序掃描
    計畫類型。完全抑制循序掃描是不可能的，
    但關閉此變數會讓規劃器在有其他方法可用時，
    不傾向使用循序掃描。
    預設值為 `on`。
<a id="GUC-ENABLE-SORT"></a>

`enable_sort` (`boolean`) <a id="id-1.6.6.10.2.3.23.1.3"></a> [#](#GUC-ENABLE-SORT)
:   啟用或停用查詢規劃器使用明確排序
    步驟。完全抑制明確排序是不可能的，
    但關閉此變數會讓規劃器在有其他方法可用時，
    不傾向使用明確排序。預設值
    為 `on`。
<a id="GUC-ENABLE-TIDSCAN"></a>

`enable_tidscan` (`boolean`) <a id="id-1.6.6.10.2.3.24.1.3"></a> [#](#GUC-ENABLE-TIDSCAN)
:   啟用或停用查詢規劃器使用 TID
    掃描計畫類型。預設值為 `on`。

<a id="RUNTIME-CONFIG-QUERY-CONSTANTS"></a>

### 19.7.2. 規劃器成本常數 [#](#RUNTIME-CONFIG-QUERY-CONSTANTS)

本節所述的*成本*變數是以任意尺度衡量的。
只有它們的相對值有意義，因此將這些值全部
同比例調高或調低，並不會改變規劃器的選擇。
根據預設，這些成本變數是以循序頁面擷取的成本為基準的；
也就是說，`seq_page_cost` 依慣例設為 `1.0`，
其他成本變數則參照此值設定。不過，
如果你偏好，也可以使用不同的尺度，例如特定機器上
以毫秒為單位的實際執行時間。

### 注意

很遺憾，目前並沒有一套定義完善的方法，
可用於判斷成本變數的理想值。最好將它們視為
特定安裝環境所接收之整體查詢混合負載的平均值。
這代表僅根據少數幾次實驗來變更這些值，是相當有風險的做法。

<a id="GUC-SEQ-PAGE-COST"></a>

`seq_page_cost` (`floating point`) <a id="id-1.6.6.10.3.4.1.1.3"></a> [#](#GUC-SEQ-PAGE-COST)
:   設定規劃器對於作為一系列循序擷取之一部分的磁碟頁面擷取
    成本的估計值。預設值為 1.0。
    可以透過設定同名的表空間參數，
    針對特定表空間中的資料表與索引覆寫此值
    （參閱 [ALTER TABLESPACE](../../reference/sql-commands/sql-altertablespace.md)）。
<a id="GUC-RANDOM-PAGE-COST"></a>

`random_page_cost` (`floating point`) <a id="id-1.6.6.10.3.4.2.1.3"></a> [#](#GUC-RANDOM-PAGE-COST)
:   設定規劃器對於非循序擷取的磁碟頁面
    成本的估計值。預設值為 4.0。
    可以透過設定同名的表空間參數，
    針對特定表空間中的資料表與索引覆寫此值
    （參閱 [ALTER TABLESPACE](../../reference/sql-commands/sql-altertablespace.md)）。

    相對於 `seq_page_cost` 降低此值，
    會使系統偏好使用索引掃描；提高此值，
    則會讓索引掃描相對而言顯得成本更高。你可以
    同時提高或降低這兩個值，以改變磁碟 I/O
    成本相對於 CPU 成本（以下參數所描述）的重要性。

    對永久性儲存裝置的隨機存取，通常遠比循序存取的
    四倍成本更高。不過，此處使用較低的預設值
    （4.0），因為大多數對儲存裝置的隨機存取
    （例如索引讀取）都假設會命中快取。此外，
    網路連接儲存裝置的延遲，也往往會降低
    隨機存取的相對額外負擔。

    如果你認為快取命中的頻率低於預設值所反映的情況，
    且網路延遲極小，可以提高
    random_page_cost，以更準確反映隨機儲存
    讀取的真實成本。相對循序存取而言，隨機讀取成本較高的
    儲存裝置（例如磁性磁碟），也可能適合以較高的
    random_page_cost 值來建模。相對地，如果你的資料
    很可能完全命中快取，例如資料庫小於
    伺服器總記憶體時，或網路延遲較高，
    降低 random_page_cost 可能會比較合適。

    ### 提示

    雖然系統允許你將 `random_page_cost` 設為
    比 `seq_page_cost` 更低，但這在實體上並不合理。
    不過，如果資料庫完全快取在 RAM 中，將兩者設為相等
    則是合理的，因為在這種情況下，不依循序讀取頁面
    並沒有任何額外代價。此外，在大量快取的資料庫中，
    你應該相對於 CPU 參數同時降低這兩個值，
    因為擷取一個已在 RAM 中的頁面的成本，
    遠比一般情況要小得多。
<a id="GUC-CPU-TUPLE-COST"></a>

`cpu_tuple_cost` (`floating point`) <a id="id-1.6.6.10.3.4.3.1.3"></a> [#](#GUC-CPU-TUPLE-COST)
:   設定規劃器對於查詢期間處理
    每一筆資料列成本的估計值。
    預設值為 0.01。
<a id="GUC-CPU-INDEX-TUPLE-COST"></a>

`cpu_index_tuple_cost` (`floating point`) <a id="id-1.6.6.10.3.4.4.1.3"></a> [#](#GUC-CPU-INDEX-TUPLE-COST)
:   設定規劃器對於索引掃描期間處理
    每一筆索引項目成本的估計值。
    預設值為 0.005。
<a id="GUC-CPU-OPERATOR-COST"></a>

`cpu_operator_cost` (`floating point`) <a id="id-1.6.6.10.3.4.5.1.3"></a> [#](#GUC-CPU-OPERATOR-COST)
:   設定規劃器對於查詢期間執行每個
    運算子或函式成本的估計值。
    預設值為 0.0025。
<a id="GUC-PARALLEL-SETUP-COST"></a>

`parallel_setup_cost` (`floating point`) <a id="id-1.6.6.10.3.4.6.1.3"></a> [#](#GUC-PARALLEL-SETUP-COST)
:   設定規劃器對於啟動平行工作
    程序成本的估計值。
    預設值為 1000。
<a id="GUC-PARALLEL-TUPLE-COST"></a>

`parallel_tuple_cost` (`floating point`) <a id="id-1.6.6.10.3.4.7.1.3"></a> [#](#GUC-PARALLEL-TUPLE-COST)
:   設定規劃器對於將一筆 tuple 從平行工作程序
    傳輸到另一個程序成本的估計值。
    預設值為 0.1。
<a id="GUC-MIN-PARALLEL-TABLE-SCAN-SIZE"></a>

`min_parallel_table_scan_size` (`integer`) <a id="id-1.6.6.10.3.4.8.1.3"></a> [#](#GUC-MIN-PARALLEL-TABLE-SCAN-SIZE)
:   設定考慮採用平行掃描所需掃描的最小資料表資料量。
    對於平行循序掃描而言，
    被掃描的資料表資料量永遠等於資料表的大小，
    但使用索引時，被掃描的資料表資料量
    通常會較少。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 8 百萬位元組（`8MB`）。
<a id="GUC-MIN-PARALLEL-INDEX-SCAN-SIZE"></a>

`min_parallel_index_scan_size` (`integer`) <a id="id-1.6.6.10.3.4.9.1.3"></a> [#](#GUC-MIN-PARALLEL-INDEX-SCAN-SIZE)
:   設定考慮採用平行掃描所需掃描的最小索引資料量。
    請注意，平行索引掃描通常不會觸及整個索引；
    真正相關的是規劃器認為掃描實際上會
    觸及的頁面數量。此參數也用於決定
    特定索引是否可以參與平行 vacuum。詳情請參閱
    [VACUUM](../../reference/sql-commands/sql-vacuum.md)。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 512 千位元組（`512kB`）。
<a id="GUC-EFFECTIVE-CACHE-SIZE"></a>

`effective_cache_size` (`integer`) <a id="id-1.6.6.10.3.4.10.1.3"></a> [#](#GUC-EFFECTIVE-CACHE-SIZE)
:   設定規劃器對於單一查詢可用之磁碟快取有效
    大小的假設。此值會被納入使用索引成本的
    估計中；較高的值會讓索引掃描較有可能被使用，
    較低的值則讓循序掃描較有可能被使用。
    設定此參數時，你應該同時考慮
    PostgreSQL 的共享緩衝區，以及會被用於
    PostgreSQL 資料檔的那部分核心磁碟快取，
    儘管某些資料可能同時存在於兩處。此外，
    也應考慮不同資料表上預期的並行查詢數量，
    因為它們必須共享可用的
    空間。此參數不會影響 PostgreSQL
    所配置共享記憶體的大小，也
    不會保留核心磁碟快取；此參數僅用於估計
    目的。系統也不會假設查詢之間資料會保留在
    磁碟快取中。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 4 十億位元組（`4GB`）。
    （若 `BLCKSZ` 不是 8kB，預設值會依比例
    縮放。）
<a id="GUC-JIT-ABOVE-COST"></a>

`jit_above_cost` (`floating point`) <a id="id-1.6.6.10.3.4.11.1.3"></a> [#](#GUC-JIT-ABOVE-COST)
:   若啟用 JIT 編譯（參閱[第 30 章](../jit/README.md)），
    設定觸發 JIT 編譯的查詢成本門檻。
    執行 JIT 需要花費規劃時間，但可以
    加速查詢執行。
    將此值設為 `-1` 會停用 JIT 編譯。
    預設值為 `100000`。
<a id="GUC-JIT-INLINE-ABOVE-COST"></a>

`jit_inline_above_cost` (`floating point`) <a id="id-1.6.6.10.3.4.12.1.3"></a> [#](#GUC-JIT-INLINE-ABOVE-COST)
:   設定 JIT 編譯嘗試內聯（inline）函式與運算子的
    查詢成本門檻。內聯會增加規劃時間，但可以
    改善執行速度。將此值設得比
    `jit_above_cost` 更低並無意義。
    將此值設為 `-1` 會停用內聯。
    預設值為 `500000`。
<a id="GUC-JIT-OPTIMIZE-ABOVE-COST"></a>

`jit_optimize_above_cost` (`floating point`) <a id="id-1.6.6.10.3.4.13.1.3"></a> [#](#GUC-JIT-OPTIMIZE-ABOVE-COST)
:   設定 JIT 編譯套用昂貴最佳化的查詢成本
    門檻。此類最佳化會增加規劃時間，但可以改善
    執行速度。將此值設得比
    `jit_above_cost` 更低並無意義，將此值
    設得比 `jit_inline_above_cost` 更高
    也不太可能帶來益處。
    將此值設為 `-1` 會停用昂貴的最佳化。
    預設值為 `500000`。

<a id="RUNTIME-CONFIG-QUERY-GEQO"></a>

### 19.7.3. 基因查詢最佳化器 [#](#RUNTIME-CONFIG-QUERY-GEQO)

基因查詢最佳化器（genetic query optimizer，GEQO）是一種使用啟發式
搜尋進行查詢規劃的演算法。這可以縮短複雜查詢
（涉及許多關聯聯結的查詢）的規劃時間，
但代價是產生的計畫有時會劣於一般
窮舉搜尋演算法所找到的計畫。
詳情請參閱[第 61 章](../../internals/geqo/README.md)。

<a id="GUC-GEQO"></a>

`geqo` (`boolean`) <a id="id-1.6.6.10.4.3.1.1.3"></a> <a id="id-1.6.6.10.4.3.1.1.4"></a> <a id="id-1.6.6.10.4.3.1.1.5"></a> [#](#GUC-GEQO)
:   啟用或停用基因查詢最佳化。
    此設定預設為開啟。在正式環境中通常最好不要關閉此功能；
    `geqo_threshold` 變數提供了更細緻的
    GEQO 控制方式。
<a id="GUC-GEQO-THRESHOLD"></a>

`geqo_threshold` (`integer`) <a id="id-1.6.6.10.4.3.2.1.3"></a> [#](#GUC-GEQO-THRESHOLD)
:   對於涉及至少這麼多個 `FROM` 項目的查詢，
    使用基因查詢最佳化來規劃。（請注意，
    `FULL OUTER JOIN` 結構僅計為一個 `FROM`
    項目。）預設值為 12。對於較簡單的查詢，
    通常最好使用一般的窮舉搜尋規劃器，但對於涉及
    許多資料表的查詢，窮舉搜尋耗時過長，
    往往比執行次佳計畫的代價還要高。因此，
    根據查詢大小設定門檻，是管理 GEQO 使用時機的
    一種便利方式。
<a id="GUC-GEQO-EFFORT"></a>

`geqo_effort` (`integer`) <a id="id-1.6.6.10.4.3.3.1.3"></a> [#](#GUC-GEQO-EFFORT)
:   控制 GEQO 中規劃時間與查詢計畫
    品質之間的取捨。此變數必須是介於 1 到 10 之間的
    整數。預設值為五。較大的值會
    增加花費在查詢規劃上的時間，但也會
    增加選出有效率查詢計畫的機率。

    `geqo_effort` 本身並不會直接進行任何操作；
    它僅用於計算影響 GEQO 行為的其他變數
    （如下所述）的預設值。如果你偏好，
    也可以自行手動設定其他參數。
<a id="GUC-GEQO-POOL-SIZE"></a>

`geqo_pool_size` (`integer`) <a id="id-1.6.6.10.4.3.4.1.3"></a> [#](#GUC-GEQO-POOL-SIZE)
:   控制 GEQO 所使用的池大小，也就是
    基因族群中個體的數量。此值至少
    必須為二，通常有用的值介於 100 到 1000
    之間。若設為零（預設設定），
    則會根據 `geqo_effort` 與
    查詢中資料表的數量選擇合適的值。
<a id="GUC-GEQO-GENERATIONS"></a>

`geqo_generations` (`integer`) <a id="id-1.6.6.10.4.3.5.1.3"></a> [#](#GUC-GEQO-GENERATIONS)
:   控制 GEQO 所使用的世代數，也就是
    演算法的迭代次數。此值至少
    必須為一，通常有用的值與池大小
    範圍相同。若設為零（預設設定），
    則會根據
    `geqo_pool_size` 選擇合適的值。
<a id="GUC-GEQO-SELECTION-BIAS"></a>

`geqo_selection_bias` (`floating point`) <a id="id-1.6.6.10.4.3.6.1.3"></a> [#](#GUC-GEQO-SELECTION-BIAS)
:   控制 GEQO 所使用的選擇偏誤（selection bias）。選擇偏誤
    是族群內的選擇壓力。值可以介於
    1.50 到 2.00 之間；後者為預設值。
<a id="GUC-GEQO-SEED"></a>

`geqo_seed` (`floating point`) <a id="id-1.6.6.10.4.3.7.1.3"></a> [#](#GUC-GEQO-SEED)
:   控制 GEQO 用於在聯結順序搜尋空間中選擇隨機路徑
    之亂數產生器的初始值。
    值的範圍可以從零（預設值）到一。變更
    此值會改變所探索的聯結路徑集合，可能導致
    找到較好或較差的最佳路徑。

<a id="RUNTIME-CONFIG-QUERY-OTHER"></a>

### 19.7.4. 其他規劃器選項 [#](#RUNTIME-CONFIG-QUERY-OTHER)

<a id="GUC-DEFAULT-STATISTICS-TARGET"></a>

`default_statistics_target` (`integer`) <a id="id-1.6.6.10.5.2.1.1.3"></a> [#](#GUC-DEFAULT-STATISTICS-TARGET)
:   為未透過 `ALTER TABLE
    SET STATISTICS` 設定欄位專屬目標值的資料表欄位，
    設定預設的統計目標值。較大的值會增加執行
    `ANALYZE` 所需的時間，但可能改善規劃器
    估計值的品質。預設值為 100。有關
    PostgreSQL 查詢規劃器使用統計資訊的
    更多資訊，請參閱[14.2 節](../../the-sql-language/performance-tips/planner-stats.md)。
<a id="GUC-CONSTRAINT-EXCLUSION"></a>

`constraint_exclusion` (`enum`) <a id="id-1.6.6.10.5.2.2.1.3"></a> <a id="id-1.6.6.10.5.2.2.1.4"></a> [#](#GUC-CONSTRAINT-EXCLUSION)
:   控制查詢規劃器使用資料表限制條件
    來最佳化查詢的方式。
    `constraint_exclusion` 允許的值有
    `on`（檢查所有資料表的限制條件）、
    `off`（永不檢查限制條件），以及
    `partition`（僅針對繼承子資料表與
    `UNION ALL` 子查詢檢查限制條件）。
    `partition` 是預設設定。
    此功能通常與傳統繼承樹搭配使用，以改善
    效能。

    當此參數允許對特定資料表使用此功能時，
    規劃器會將查詢條件與該資料表的 `CHECK`
    限制條件比對，並略過掃描條件與限制條件矛盾的
    資料表。舉例來說：

    ```

    CREATE TABLE parent(key integer, ...);
    CREATE TABLE child1000(check (key between 1000 and 1999)) INHERITS(parent);
    CREATE TABLE child2000(check (key between 2000 and 2999)) INHERITS(parent);
    ...
    SELECT * FROM parent WHERE key = 2400;
    ```

    啟用限制條件排除後，這個 `SELECT`
    完全不會掃描 `child1000`，藉此改善效能。

    目前，限制條件排除功能預設僅在常用於
    透過繼承樹實作資料表分割的情況下啟用。若對所有
    資料表開啟此功能，會帶來額外的規劃負擔，
    在簡單查詢上相當明顯，而且多數情況下對簡單查詢
    不會帶來任何好處。如果你沒有任何使用傳統繼承方式
    分割的資料表，可能會偏好完全關閉此功能。
    （請注意，分割資料表的對應功能是由另一個
    獨立參數
    [enable_partition_pruning](runtime-config-query.md#GUC-ENABLE-PARTITION-PRUNING) 控制的。）

    有關使用限制條件排除實作分割的更多資訊，
    請參閱[5.12.5 節](../../the-sql-language/ddl/ddl-partitioning.md#DDL-PARTITIONING-CONSTRAINT-EXCLUSION)。
<a id="GUC-CURSOR-TUPLE-FRACTION"></a>

`cursor_tuple_fraction` (`floating point`) <a id="id-1.6.6.10.5.2.3.1.3"></a> [#](#GUC-CURSOR-TUPLE-FRACTION)
:   設定規劃器對於游標所擷取資料列比例的
    估計值。預設值為 0.1。此設定的值越小，
    規劃器越傾向使用游標的「快速啟動」計畫，
    這種計畫可以快速擷取前幾筆資料列，但擷取
    所有資料列可能會花上較長時間。較大的值
    則會更著重於總估計時間。在最大設定值
    1.0 時，游標的規劃方式與一般查詢完全相同，
    只考慮總估計時間，而不考慮前幾筆資料列
    多快能夠傳回。
<a id="GUC-FROM-COLLAPSE-LIMIT"></a>

`from_collapse_limit` (`integer`) <a id="id-1.6.6.10.5.2.4.1.3"></a> [#](#GUC-FROM-COLLAPSE-LIMIT)
:   如果合併後的 `FROM` 清單項目數量不超過
    此值，規劃器就會將子查詢合併到上層查詢中。
    較小的值可以縮短規劃時間，但可能產生較差的
    查詢計畫。預設值為八。
    詳情請參閱[14.3 節](../../the-sql-language/performance-tips/explicit-joins.md)。

    將此值設為 [geqo_threshold](runtime-config-query.md#GUC-GEQO-THRESHOLD) 或更大，
    可能觸發使用 GEQO 規劃器，導致產生非最佳的
    計畫。參閱[19.7.3 節](runtime-config-query.md#RUNTIME-CONFIG-QUERY-GEQO)。
<a id="GUC-JIT"></a>

`jit` (`boolean`) <a id="id-1.6.6.10.5.2.5.1.3"></a> [#](#GUC-JIT)
:   決定 PostgreSQL 是否可以使用 JIT 編譯
    （若可用，參閱[第 30 章](../jit/README.md)）。
    預設值為 `on`。
<a id="GUC-JOIN-COLLAPSE-LIMIT"></a>

`join_collapse_limit` (`integer`) <a id="id-1.6.6.10.5.2.6.1.3"></a> [#](#GUC-JOIN-COLLAPSE-LIMIT)
:   只要重寫結果不超過此值個項目，規劃器就會將
    明確的 `JOIN` 結構（`FULL JOIN` 除外）
    重寫為 `FROM` 項目清單。較小的值可以
    縮短規劃時間，但可能產生較差的查詢計畫。

    根據預設，此變數的設定值與
    `from_collapse_limit` 相同，這對大多數
    用途而言是合適的。設為 1 可防止對明確的
    `JOIN` 進行任何重新排序。因此，查詢中
    指定的明確聯結順序，就會是關聯實際被
    聯結的順序。由於查詢規劃器不一定總是選擇
    最佳的聯結順序，進階使用者可以選擇暫時
    將此變數設為 1，然後自行明確指定所需的聯結
    順序。詳情請參閱[14.3 節](../../the-sql-language/performance-tips/explicit-joins.md)。

    將此值設為 [geqo_threshold](runtime-config-query.md#GUC-GEQO-THRESHOLD) 或更大，
    可能觸發使用 GEQO 規劃器，導致產生非最佳的
    計畫。參閱[19.7.3 節](runtime-config-query.md#RUNTIME-CONFIG-QUERY-GEQO)。
<a id="GUC-PLAN-CACHE-MODE"></a>

`plan_cache_mode` (`enum`) <a id="id-1.6.6.10.5.2.7.1.3"></a> [#](#GUC-PLAN-CACHE-MODE)
:   已備妥陳述式（prepared statement，無論是明確備妥，
    或是由例如 PL/pgSQL 隱含產生）可以使用自訂
    計畫或通用計畫執行。自訂計畫會針對每次執行
    使用其特定的參數值集合重新製作，通用計畫
    則不依賴參數值，可以在多次執行間重複使用。
    因此，使用通用計畫可以節省規劃時間，但如果
    理想的計畫高度依賴參數值，通用計畫可能會
    效率不彰。這兩個選項之間的選擇
    通常會自動進行，但可以透過
    `plan_cache_mode` 覆寫。
    允許的值有 `auto`（預設值）、
    `force_custom_plan`，以及
    `force_generic_plan`。
    此設定會在要執行已快取的計畫時考量，
    而非在備妥計畫時考量。
    詳情請參閱 [PREPARE](../../reference/sql-commands/sql-prepare.md)。
<a id="GUC-RECURSIVE-WORKTABLE-FACTOR"></a>

`recursive_worktable_factor` (`floating point`) <a id="id-1.6.6.10.5.2.8.1.3"></a> [#](#GUC-RECURSIVE-WORKTABLE-FACTOR)
:   設定規劃器對於[遞迴
    查詢](../../the-sql-language/queries/queries-with.md#QUERIES-WITH-RECURSIVE)工作資料表平均大小的
    估計值，以查詢初始非遞迴項目估計大小的倍數表示。
    這有助於規劃器選擇將工作資料表與
    查詢其他資料表聯結的最合適方法。
    預設值為 `10.0`。較小的值，例如
    `1.0`，在遞迴從一個步驟到下一個步驟
    的「扇出（fan-out）」較低時會很有幫助，例如
    最短路徑查詢。圖形分析查詢則可能
    受益於比預設值更大的值。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-query.html)（原文版本：18.6；核對日期：2026-09-24）
