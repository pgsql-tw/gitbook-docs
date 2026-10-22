<a id="PGSTATTUPLE"></a>

## F.33. pgstattuple — 取得元組層級的統計資訊 [#](#PGSTATTUPLE)

[F.33.1. 函式](pgstattuple.md#PGSTATTUPLE-FUNCS)

[F.33.2. 作者](pgstattuple.md#PGSTATTUPLE-AUTHORS)

<a id="id-1.11.7.43.2"></a>

`pgstattuple` 模組提供多種函式，用來取得元組（tuple）層級的統計資訊。

由於這些函式會傳回詳細的頁面層級資訊，預設會限制存取。預設情況下，只有
`pg_stat_scan_tables` 角色具有 `EXECUTE`
權限。超級使用者當然不受此限制。安裝擴充功能之後，使用者可以執行 `GRANT`
命令變更這些函式的權限，讓其他人也能執行它們。不過，改為將這些使用者加入
`pg_stat_scan_tables` 角色可能是較好的做法。

<a id="PGSTATTUPLE-FUNCS"></a>

### F.33.1. 函式 [#](#PGSTATTUPLE-FUNCS)

<a id="id-1.11.7.43.5.2.1.1.1"></a> `pgstattuple(regclass) returns record`
:   `pgstattuple` 會傳回關聯的實體長度、「死亡」資料列的百分比，以及其他資訊。這可以協助使用者判斷是否需要清理（vacuum）。引數是目標關聯的名稱（可選擇以綱要限定）或 OID。
    例如：

    ```

    test=> SELECT * FROM pgstattuple('pg_catalog.pg_proc');
    -[ RECORD 1 ]------+-------
    table_len          | 458752
    tuple_count        | 1470
    tuple_len          | 438896
    tuple_percent      | 95.67
    dead_tuple_count   | 11
    dead_tuple_len     | 3157
    dead_tuple_percent | 0.69
    free_space         | 8932
    free_percent       | 1.95
    ```

    輸出欄位說明請參閱[表 F.24](pgstattuple.md#PGSTATTUPLE-COLUMNS).

    <a id="PGSTATTUPLE-COLUMNS"></a>

    **表 F.24. `pgstattuple` 輸出欄位**

    <table border="1" class="table" summary="pgstattuple 輸出欄位"><colgroup><col/><col/><col/></colgroup><thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">table_len</code></td><td><code class="type">bigint</code></td><td>關聯的實體長度，以位元組為單位</td></tr><tr><td><code class="structfield">tuple_count</code></td><td><code class="type">bigint</code></td><td>存活資料列數</td></tr><tr><td><code class="structfield">tuple_len</code></td><td><code class="type">bigint</code></td><td>存活資料列的總長度，以位元組為單位</td></tr><tr><td><code class="structfield">tuple_percent</code></td><td><code class="type">float8</code></td><td>存活資料列的百分比</td></tr><tr><td><code class="structfield">dead_tuple_count</code></td><td><code class="type">bigint</code></td><td>死亡資料列數</td></tr><tr><td><code class="structfield">dead_tuple_len</code></td><td><code class="type">bigint</code></td><td>死亡資料列的總長度，以位元組為單位</td></tr><tr><td><code class="structfield">dead_tuple_percent</code></td><td><code class="type">float8</code></td><td>死亡資料列的百分比</td></tr><tr><td><code class="structfield">free_space</code></td><td><code class="type">bigint</code></td><td>可用空間總量，以位元組為單位</td></tr><tr><td><code class="structfield">free_percent</code></td><td><code class="type">float8</code></td><td>可用空間的百分比</td></tr></tbody></table>

    <br>

    ### 注意

    `table_len` 一定會大於
    `tuple_len`、`dead_tuple_len`
    與 `free_space` 的總和。差額來自固定的頁面額外負擔、每個頁面中指向元組的指標表，以及確保元組正確對齊的填補。

    `pgstattuple` 只會對關聯取得讀取鎖定。因此結果並不反映瞬間的快照；並行的更新會影響結果。

    若 `HeapTupleSatisfiesDirty` 傳回 false，
    `pgstattuple` 就判定該元組為「死亡」。

`pgstattuple(text) returns record`
:   此函式與 `pgstattuple(regclass)` 相同，只是目標關聯以 TEXT 指定。此函式目前是為了向後相容性而保留，並將在未來的某個版本中棄用。

<a id="id-1.11.7.43.5.2.3.1.1"></a> `pgstatindex(regclass) returns record`
:   `pgstatindex` 會傳回一筆紀錄，顯示 B-tree 索引的相關資訊。例如：

    ```

    test=> SELECT * FROM pgstatindex('pg_cast_oid_index');
    -[ RECORD 1 ]------+------
    version            | 2
    tree_level         | 0
    index_size         | 16384
    root_block_no      | 1
    internal_pages     | 0
    leaf_pages         | 1
    empty_pages        | 0
    deleted_pages      | 0
    avg_leaf_density   | 54.27
    leaf_fragmentation | 0
    ```

    輸出欄位如下：

    <table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">version</code></td><td><code class="type">integer</code></td><td>B-tree 版本編號</td></tr><tr><td><code class="structfield">tree_level</code></td><td><code class="type">integer</code></td><td>根頁面的樹層級</td></tr><tr><td><code class="structfield">index_size</code></td><td><code class="type">bigint</code></td><td>索引總大小，以位元組為單位</td></tr><tr><td><code class="structfield">root_block_no</code></td><td><code class="type">bigint</code></td><td>根頁面的位置（若無則為零）</td></tr><tr><td><code class="structfield">internal_pages</code></td><td><code class="type">bigint</code></td><td><span class="quote">「<span class="quote">內部</span>」</span>（上層）頁面數</td></tr><tr><td><code class="structfield">leaf_pages</code></td><td><code class="type">bigint</code></td><td>葉頁面數</td></tr><tr><td><code class="structfield">empty_pages</code></td><td><code class="type">bigint</code></td><td>空頁面數</td></tr><tr><td><code class="structfield">deleted_pages</code></td><td><code class="type">bigint</code></td><td>已刪除頁面數</td></tr><tr><td><code class="structfield">avg_leaf_density</code></td><td><code class="type">float8</code></td><td>葉頁面的平均密度</td></tr><tr><td><code class="structfield">leaf_fragmentation</code></td><td><code class="type">float8</code></td><td>葉頁面的碎片化程度</td></tr></tbody></table>

    回報的 `index_size` 通常會比 `internal_pages + leaf_pages +
    empty_pages + deleted_pages` 所計入的頁面多一個頁面，因為它還包含索引的中繼頁面（metapage）。

    與 `pgstattuple` 相同，結果是逐頁累計的，不應預期它代表整個索引的瞬間快照。

`pgstatindex(text) returns record`
:   此函式與 `pgstatindex(regclass)` 相同，只是目標索引以 TEXT 指定。此函式目前是為了向後相容性而保留，並將在未來的某個版本中棄用。

<a id="id-1.11.7.43.5.2.5.1.1"></a> `pgstatginindex(regclass) returns record`
:   `pgstatginindex` 會傳回一筆紀錄，顯示 GIN 索引的相關資訊。例如：

    ```

    test=> SELECT * FROM pgstatginindex('test_gin_index');
    -[ RECORD 1 ]--+--
    version        | 1
    pending_pages  | 0
    pending_tuples | 0
    ```

    輸出欄位如下：

    <table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">version</code></td><td><code class="type">integer</code></td><td>GIN 版本編號</td></tr><tr><td><code class="structfield">pending_pages</code></td><td><code class="type">integer</code></td><td>待處理清單中的頁面數</td></tr><tr><td><code class="structfield">pending_tuples</code></td><td><code class="type">bigint</code></td><td>待處理清單中的元組數</td></tr></tbody></table>

<a id="id-1.11.7.43.5.2.6.1.1"></a> `pgstathashindex(regclass) returns record`
:   `pgstathashindex` 會傳回一筆紀錄，顯示 HASH 索引的相關資訊。例如：

    ```

    test=> select * from pgstathashindex('con_hash_index');
    -[ RECORD 1 ]--+-----------------
    version        | 4
    bucket_pages   | 33081
    overflow_pages | 0
    bitmap_pages   | 1
    unused_pages   | 32455
    live_items     | 10204006
    dead_items     | 0
    free_percent   | 61.8005949100872
    ```

    輸出欄位如下：

    <table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">version</code></td><td><code class="type">integer</code></td><td>HASH 版本編號</td></tr><tr><td><code class="structfield">bucket_pages</code></td><td><code class="type">bigint</code></td><td>桶（bucket）頁面數</td></tr><tr><td><code class="structfield">overflow_pages</code></td><td><code class="type">bigint</code></td><td>溢位頁面數</td></tr><tr><td><code class="structfield">bitmap_pages</code></td><td><code class="type">bigint</code></td><td>點陣圖頁面數</td></tr><tr><td><code class="structfield">unused_pages</code></td><td><code class="type">bigint</code></td><td>未使用頁面數</td></tr><tr><td><code class="structfield">live_items</code></td><td><code class="type">bigint</code></td><td>存活資料列數</td></tr><tr><td><code class="structfield">dead_tuples</code></td><td><code class="type">bigint</code></td><td>死亡資料列數</td></tr><tr><td><code class="structfield">free_percent</code></td><td><code class="type">float</code></td><td>可用空間的百分比</td></tr></tbody></table>

    譯註：上表中第七個欄位的名稱寫作 dead_tuples，但上方範例輸出顯示的是 dead_items。經核對 REL_18_STABLE 的 contrib/pgstattuple/pgstattuple--1.4--1.5.sql，pgstathashindex 實際傳回的欄位名稱為 dead_items（bigint），表中 dead_tuples 為原文誤植；表格內容依原文保留。

<a id="id-1.11.7.43.5.2.7.1.1"></a> `pg_relpages(regclass) returns bigint`
:   `pg_relpages` 會傳回關聯中的頁面數。

`pg_relpages(text) returns bigint`
:   此函式與 `pg_relpages(regclass)` 相同，只是目標關聯以 TEXT 指定。此函式目前是為了向後相容性而保留，並將在未來的某個版本中棄用。

<a id="id-1.11.7.43.5.2.9.1.1"></a> `pgstattuple_approx(regclass) returns record`
:   `pgstattuple_approx` 是
    `pgstattuple` 的較快替代方案，會傳回近似的結果。
    引數是目標關聯的名稱或 OID。
    例如：

    ```

    test=> SELECT * FROM pgstattuple_approx('pg_catalog.pg_proc'::regclass);
    -[ RECORD 1 ]--------+-------
    table_len            | 573440
    scanned_percent      | 2
    approx_tuple_count   | 2740
    approx_tuple_len     | 561210
    approx_tuple_percent | 97.87
    dead_tuple_count     | 0
    dead_tuple_len       | 0
    dead_tuple_percent   | 0
    approx_free_space    | 11996
    approx_free_percent  | 2.09
    ```

    輸出欄位說明請參閱[表 F.25](pgstattuple.md#PGSTATAPPROX-COLUMNS).

    `pgstattuple` 一律執行全資料表掃描，並傳回存活與死亡資料列的精確數量（及其大小）與可用空間；`pgstattuple_approx`
    則會盡量避免全資料表掃描，傳回精確的死亡資料列統計資訊，以及存活資料列數量與大小和可用空間的近似值。

    它的做法是依據可見性對應表略過只包含可見元組的頁面（若某頁面已設定對應的 VM 位元，就假設它不包含任何死亡資料列）。對於這類頁面，它會從可用空間對應表取得可用空間的值，並假設頁面上其餘的空間都由存活資料列占用。

    對於無法略過的頁面，它會掃描每個元組，將其存在與大小記錄到相應的計數器中，並累加頁面上的可用空間。最後，它會根據已掃描的頁面數與元組數估計存活資料列的總數（方式與 VACUUM 估計 pg_class.reltuples 相同）。

    <a id="PGSTATAPPROX-COLUMNS"></a>

    **表 F.25. `pgstattuple_approx` 輸出欄位**

    <table border="1" class="table" summary="pgstattuple_approx 輸出欄位"><colgroup><col/><col/><col/></colgroup><thead><tr><th>欄位</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="structfield">table_len</code></td><td><code class="type">bigint</code></td><td>關聯的實體長度，以位元組為單位（精確值）</td></tr><tr><td><code class="structfield">scanned_percent</code></td><td><code class="type">float8</code></td><td>已掃描資料表的百分比</td></tr><tr><td><code class="structfield">approx_tuple_count</code></td><td><code class="type">bigint</code></td><td>存活資料列數（估計值）</td></tr><tr><td><code class="structfield">approx_tuple_len</code></td><td><code class="type">bigint</code></td><td>存活資料列的總長度，以位元組為單位（估計值）</td></tr><tr><td><code class="structfield">approx_tuple_percent</code></td><td><code class="type">float8</code></td><td>存活資料列的百分比</td></tr><tr><td><code class="structfield">dead_tuple_count</code></td><td><code class="type">bigint</code></td><td>死亡資料列數（精確值）</td></tr><tr><td><code class="structfield">dead_tuple_len</code></td><td><code class="type">bigint</code></td><td>死亡資料列的總長度，以位元組為單位（精確值）</td></tr><tr><td><code class="structfield">dead_tuple_percent</code></td><td><code class="type">float8</code></td><td>死亡資料列的百分比</td></tr><tr><td><code class="structfield">approx_free_space</code></td><td><code class="type">bigint</code></td><td>可用空間總量，以位元組為單位（估計值）</td></tr><tr><td><code class="structfield">approx_free_percent</code></td><td><code class="type">float8</code></td><td>可用空間的百分比</td></tr></tbody></table>

    <br>

    在上述輸出中，可用空間的數字可能與
    `pgstattuple` 的輸出不完全相符，因為可用空間對應表雖然提供確切的數字，但不保證精確到位元組。

<a id="PGSTATTUPLE-AUTHORS"></a>

### F.33.2. 作者 [#](#PGSTATTUPLE-AUTHORS)

Tatsuo Ishii、Satoshi Nagayasu 與 Abhijit Menon-Sen

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgstattuple.html)（原文版本：18.6；核對日期：2026-10-23）
