<a id="RUNTIME-CONFIG-DEVELOPER"></a>

## 19.17. 開發人員選項 [#](#RUNTIME-CONFIG-DEVELOPER)

以下參數是供開發人員測試之用，絕不應該用於正式環境的資料庫。不過其中有些參數可用於協助修復嚴重損毀的資料庫。因此，這些參數已從範例
`postgresql.conf` 檔案中排除。請注意，其中許多參數需要特殊的原始碼編譯旗標才能運作。

<a id="GUC-ALLOW-IN-PLACE-TABLESPACES"></a>

`allow_in_place_tablespaces` (`boolean`) <a id="id-1.6.6.20.3.1.1.3"></a> [#](#GUC-ALLOW-IN-PLACE-TABLESPACES)
:   當提供空位置字串給 `CREATE TABLESPACE` 命令時，允許在
    `pg_tblspc` 內以目錄形式建立表空間。此設計是為了讓
    主要伺服器與待命伺服器可以在同一台機器上執行時，測試複寫情境。
    這類目錄可能會讓預期只會在該位置找到符號連結的備份工具感到混淆。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-ALLOW-SYSTEM-TABLE-MODS"></a>

`allow_system_table_mods` (`boolean`) <a id="id-1.6.6.20.3.2.1.3"></a> [#](#GUC-ALLOW-SYSTEM-TABLE-MODS)
:   允許修改系統表的結構，以及對系統表執行某些其他具風險性的操作。
    在此設定之外，即使是超級使用者也不允許這麼做。輕率使用此設定
    可能導致無法挽回的資料遺失，或嚴重損毀資料庫系統。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-BACKTRACE-FUNCTIONS"></a>

`backtrace_functions` (`string`) <a id="id-1.6.6.20.3.3.1.3"></a> [#](#GUC-BACKTRACE-FUNCTIONS)
:   此參數包含以逗號分隔的 C 函式名稱清單。
    如果發生錯誤，且發生錯誤的內部 C 函式名稱與清單中的值相符，
    則會將回溯（backtrace）連同錯誤訊息一併寫入伺服器日誌。這可
    用於除錯原始碼中的特定區域。

    並非所有平台都支援回溯功能，且回溯的品質取決於編譯選項。

    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-DEBUG-COPY-PARSE-PLAN-TREES"></a>

`debug_copy_parse_plan_trees` (`boolean`) <a id="id-1.6.6.20.3.4.1.3"></a> [#](#GUC-DEBUG-COPY-PARSE-PLAN-TREES)
:   啟用此選項會強制所有剖析樹與規劃樹都經過
    `copyObject()`，以協助找出
    `copyObject()` 中的錯誤與疏漏。預設值為關閉。

    此參數僅在編譯時定義了
    `DEBUG_NODE_TESTS_ENABLED`（使用
    configure 選項
    `--enable-cassert` 時會自動定義）時才可用。
<a id="GUC-DEBUG-DISCARD-CACHES"></a>

`debug_discard_caches` (`integer`) <a id="id-1.6.6.20.3.5.1.3"></a> [#](#GUC-DEBUG-DISCARD-CACHES)
:   當設為 `1` 時，每個系統目錄快取項目都會在第一時間被失效，
    無論是否真的發生了會使其失效的事件。因此，系統目錄的快取實質上會被停用，
    伺服器執行速度將會非常緩慢。更高的數值會遞迴執行快取失效，
    這會更慢，且只有在測試快取邏輯本身時才有用。預設值
    `0` 代表正常的目錄快取行為。

    此參數在嘗試觸發難以重現、涉及並行目錄變更的臭蟲時非常有用，
    但除此之外很少需要用到。詳情請參閱原始碼檔案
    `inval.c` 與
    `pg_config_manual.h`。

    此參數僅在編譯時定義了
    `DISCARD_CACHES_ENABLED`（使用
    configure 選項
    `--enable-cassert` 時會自動定義）時才受支援。在正式環境建置中，
    其值永遠是 `0`，嘗試將其設為其他值會引發錯誤。
<a id="GUC-DEBUG-IO-DIRECT"></a>

`debug_io_direct` (`string`) <a id="id-1.6.6.20.3.6.1.3"></a> [#](#GUC-DEBUG-IO-DIRECT)
:   要求核心對關聯資料檔與 WAL 檔案使用
    `O_DIRECT`（大多數類 Unix 系統）、
    `F_NOCACHE`（macOS）或
    `FILE_FLAG_NO_BUFFERING`（Windows）以降低快取效應。

    可設為空字串（預設值）以停用直接 I/O，
    或設為以逗號分隔、應使用直接 I/O 的操作清單。
    合法的選項有 `data`（表示
    主要資料檔）、`wal`（表示 WAL 檔案），以及
    `wal_init`（表示 WAL 檔案在最初配置時）。
    此參數只能在伺服器啟動時設定。

    部分作業系統與檔案系統不支援直接 I/O，因此非預設設定可能會在啟動時被拒絕或造成錯誤。

    目前此功能會降低效能，僅供開發人員測試之用。
<a id="GUC-DEBUG-PARALLEL-QUERY"></a>

`debug_parallel_query` (`enum`) <a id="id-1.6.6.20.3.7.1.3"></a> [#](#GUC-DEBUG-PARALLEL-QUERY)
:   即使在預期不會有效能提升的情況下，也允許基於測試目的使用平行查詢。
    `debug_parallel_query` 允許的值有
    `off`（僅在預期能提升效能時才使用平行模式）、`on`（對所有
    被認為安全的查詢強制使用平行查詢），以及 `regress`（與
    `on` 相同，但另有下述額外的行為變更）。

    更具體地說，將此值設為 `on` 會為所有看起來安全的查詢計畫
    在最上層加入一個 `Gather` 節點，使查詢在平行工作程序內執行。
    即使沒有可用的平行工作程序，或無法使用平行工作程序，
    在平行查詢情境下原本被禁止的操作（例如啟動子交易）仍會被禁止，
    除非規劃器認為這麼做會導致查詢失敗。如果設定此選項後發生失敗或非預期的結果，
    可能需要將查詢所使用的某些函式標記為
    `PARALLEL UNSAFE`
    （或視情況標記為 `PARALLEL RESTRICTED`）。

    將此值設為 `regress` 具備與設為 `on` 相同的所有效果，
    並另外加上一些為了方便自動化迴歸測試而設計的行為。
    通常來自平行工作程序的訊息會包含用以標示此點的上下文行，
    但設為 `regress` 會抑制這一行，使輸出與非平行執行時相同。
    此外，此設定加入計畫中的 `Gather` 節點在
    `EXPLAIN` 輸出中會被隱藏，使輸出結果與此設定關閉（`off`）時相符。
<a id="GUC-DEBUG-RAW-EXPRESSION-COVERAGE-TEST"></a>

`debug_raw_expression_coverage_test` (`boolean`) <a id="id-1.6.6.20.3.8.1.3"></a> [#](#GUC-DEBUG-RAW-EXPRESSION-COVERAGE-TEST)
:   啟用此選項會強制所有 DML 陳述式的原始剖析樹都由
    `raw_expression_tree_walker()` 掃描，以協助找出
    該函式中的錯誤與疏漏。預設值為關閉。

    此參數僅在編譯時定義了
    `DEBUG_NODE_TESTS_ENABLED`（使用
    configure 選項
    `--enable-cassert` 時會自動定義）時才可用。
<a id="GUC-DEBUG-WRITE-READ-PARSE-PLAN-TREES"></a>

`debug_write_read_parse_plan_trees` (`boolean`) <a id="id-1.6.6.20.3.9.1.3"></a> [#](#GUC-DEBUG-WRITE-READ-PARSE-PLAN-TREES)
:   啟用此選項會強制所有剖析樹與規劃樹都經過
    `outfuncs.c`／`readfuncs.c`，以協助找出
    這些模組中的錯誤與疏漏。預設值為關閉。

    此參數僅在編譯時定義了
    `DEBUG_NODE_TESTS_ENABLED`（使用
    configure 選項
    `--enable-cassert` 時會自動定義）時才可用。
<a id="GUC-IGNORE-SYSTEM-INDEXES"></a>

`ignore_system_indexes` (`boolean`) <a id="id-1.6.6.20.3.10.1.3"></a> [#](#GUC-IGNORE-SYSTEM-INDEXES)
:   讀取系統表時忽略系統索引（但修改資料表時仍會更新索引）。
    這在從損毀的系統索引復原時很有用。
    此參數無法在工作階段啟動後變更。
<a id="GUC-POST-AUTH-DELAY"></a>

`post_auth_delay` (`integer`) <a id="id-1.6.6.20.3.11.1.3"></a> [#](#GUC-POST-AUTH-DELAY)
:   新的伺服器程序啟動後，在完成驗證程序後延遲的時間量。
    這是為了讓開發人員有機會以除錯器附加到伺服器程序。
    若此值指定時未帶單位，則以秒為單位。
    值為零（預設值）代表停用此延遲。
    此參數無法在工作階段啟動後變更。
<a id="GUC-PRE-AUTH-DELAY"></a>

`pre_auth_delay` (`integer`) <a id="id-1.6.6.20.3.12.1.3"></a> [#](#GUC-PRE-AUTH-DELAY)
:   新的伺服器程序被 fork 出來後、在進行驗證程序之前延遲的時間量。
    這是為了讓開發人員有機會以除錯器附加到伺服器程序，
    以追蹤驗證過程中的異常行為。
    若此值指定時未帶單位，則以秒為單位。
    值為零（預設值）代表停用此延遲。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-TRACE-NOTIFY"></a>

`trace_notify` (`boolean`) <a id="id-1.6.6.20.3.13.1.3"></a> [#](#GUC-TRACE-NOTIFY)
:   為 `LISTEN` 與 `NOTIFY`
    命令產生大量的除錯輸出。
    [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) 或
    [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) 必須設為
    `DEBUG1` 或更低，才能將此輸出分別傳送到
    用戶端或伺服器日誌。
<a id="GUC-TRACE-SORT"></a>

`trace_sort` (`boolean`) <a id="id-1.6.6.20.3.14.1.3"></a> [#](#GUC-TRACE-SORT)
:   若為開啟，會在排序操作期間輸出資源使用資訊。
<a id="GUC-TRACE-LOCKS"></a>

`trace_locks` (`boolean`) <a id="id-1.6.6.20.3.15.1.3"></a> [#](#GUC-TRACE-LOCKS)
:   若為開啟，會輸出鎖定使用資訊。傾印的資訊
    包括鎖定操作的類型、鎖定的種類，以及被鎖定或解鎖之物件的唯一識別碼。
    另外還會包括此物件目前已授予的鎖定類型位元遮罩，
    以及正在等待的鎖定類型位元遮罩。針對每種鎖定類型，
    也會傾印已授予的鎖定數量與等待中的鎖定數量，以及各自的總計。
    以下是日誌檔輸出的範例：

    ```

    LOG:  LockAcquire: new: lock(0xb7acd844) id(24688,24696,0,0,0,1)
          grantMask(0) req(0,0,0,0,0,0,0)=0 grant(0,0,0,0,0,0,0)=0
          wait(0) type(AccessShareLock)
    LOG:  GrantLock: lock(0xb7acd844) id(24688,24696,0,0,0,1)
          grantMask(2) req(1,0,0,0,0,0,0)=1 grant(1,0,0,0,0,0,0)=1
          wait(0) type(AccessShareLock)
    LOG:  UnGrantLock: updated: lock(0xb7acd844) id(24688,24696,0,0,0,1)
          grantMask(0) req(0,0,0,0,0,0,0)=0 grant(0,0,0,0,0,0,0)=0
          wait(0) type(AccessShareLock)
    LOG:  CleanUpLock: deleting: lock(0xb7acd844) id(24688,24696,0,0,0,1)
          grantMask(0) req(0,0,0,0,0,0,0)=0 grant(0,0,0,0,0,0,0)=0
          wait(0) type(INVALID)
    ```

    此傾印結構的詳細內容可以在
    `src/include/storage/lock.h` 中找到。

    此參數僅在編譯 PostgreSQL 時定義了 `LOCK_DEBUG`
    巨集的情況下才可用。
<a id="GUC-TRACE-LWLOCKS"></a>

`trace_lwlocks` (`boolean`) <a id="id-1.6.6.20.3.16.1.3"></a> [#](#GUC-TRACE-LWLOCKS)
:   若為開啟，會輸出輕量鎖使用資訊。輕量鎖主要用於
    對共享記憶體資料結構提供互斥存取。

    此參數僅在編譯 PostgreSQL 時定義了 `LOCK_DEBUG`
    巨集的情況下才可用。
<a id="GUC-TRACE-USERLOCKS"></a>

`trace_userlocks` (`boolean`) <a id="id-1.6.6.20.3.17.1.3"></a> [#](#GUC-TRACE-USERLOCKS)
:   若為開啟，會輸出使用者鎖使用資訊。輸出內容與
    `trace_locks` 相同，只是針對建議鎖（advisory lock）而言。

    此參數僅在編譯 PostgreSQL 時定義了 `LOCK_DEBUG`
    巨集的情況下才可用。
<a id="GUC-TRACE-LOCK-OIDMIN"></a>

`trace_lock_oidmin` (`integer`) <a id="id-1.6.6.20.3.18.1.3"></a> [#](#GUC-TRACE-LOCK-OIDMIN)
:   若有設定，則不追蹤 OID 低於此值的資料表的鎖定
    （用以避免對系統表輸出）。

    此參數僅在編譯 PostgreSQL 時定義了 `LOCK_DEBUG`
    巨集的情況下才可用。
<a id="GUC-TRACE-LOCK-TABLE"></a>

`trace_lock_table` (`integer`) <a id="id-1.6.6.20.3.19.1.3"></a> [#](#GUC-TRACE-LOCK-TABLE)
:   無條件追蹤此資料表（OID）上的鎖定。

    此參數僅在編譯 PostgreSQL 時定義了 `LOCK_DEBUG`
    巨集的情況下才可用。
<a id="GUC-DEBUG-DEADLOCKS"></a>

`debug_deadlocks` (`boolean`) <a id="id-1.6.6.20.3.20.1.3"></a> [#](#GUC-DEBUG-DEADLOCKS)
:   若有設定，會在死結逾時發生時傾印所有目前鎖定的資訊。

    此參數僅在編譯 PostgreSQL 時定義了 `LOCK_DEBUG`
    巨集的情況下才可用。
<a id="GUC-LOG-BTREE-BUILD-STATS"></a>

`log_btree_build_stats` (`boolean`) <a id="id-1.6.6.20.3.21.1.3"></a> [#](#GUC-LOG-BTREE-BUILD-STATS)
:   若有設定，會記錄各種 B-tree 操作的系統資源使用統計（記憶體與 CPU）。

    此參數僅在編譯 PostgreSQL 時定義了 `BTREE_BUILD_STATS`
    巨集的情況下才可用。
<a id="GUC-WAL-CONSISTENCY-CHECKING"></a>

`wal_consistency_checking` (`string`) <a id="id-1.6.6.20.3.22.1.3"></a> [#](#GUC-WAL-CONSISTENCY-CHECKING)
:   此參數旨在用於檢查 WAL redo 常式中的臭蟲。啟用後，
    與 WAL 記錄相關而被修改之緩衝區的完整頁面映像會被加入該記錄中。
    若該記錄後續被重播，系統會先套用每筆記錄，
    然後測試該記錄所修改的緩衝區是否與儲存的映像相符。
    在某些情況下（例如 hint bit），細微差異是可接受的，會被忽略。
    任何非預期的差異都會導致嚴重錯誤，終止復原程序。

    此設定的預設值為空字串，代表停用此功能。可將其設為
    `all` 以檢查所有記錄，或設為以逗號分隔的資源管理員清單，
    以僅檢查來自那些資源管理員的記錄。目前支援的資源管理員有
    `heap`、
    `heap2`、`btree`、`hash`、
    `gin`、`gist`、`sequence`、
    `spgist`、`brin` 以及 `generic`。
    延伸模組可能會定義額外的資源管理員。只有超級使用者以及
    具備相應 `SET` 權限的使用者可以變更此設定。
<a id="GUC-WAL-DEBUG"></a>

`wal_debug` (`boolean`) <a id="id-1.6.6.20.3.23.1.3"></a> [#](#GUC-WAL-DEBUG)
:   若為開啟，會輸出與 WAL 相關的除錯資訊。此參數
    僅在編譯 PostgreSQL 時定義了 `WAL_DEBUG` 巨集的情況下才可用。
<a id="GUC-IGNORE-CHECKSUM-FAILURE"></a>

`ignore_checksum_failure` (`boolean`) <a id="id-1.6.6.20.3.24.1.3"></a> [#](#GUC-IGNORE-CHECKSUM-FAILURE)
:   僅在啟用[資料檢查碼](../wal/checksums.md)時才有效果。

    讀取時偵測到檢查碼失敗，通常會導致 PostgreSQL
    回報錯誤，中止目前的交易。將 `ignore_checksum_failure`
    設為開啟會使系統忽略此失敗（但仍會回報警告），並
    繼續進行處理。此行為可能會*導致當機、擴散
    或隱藏損毀，或其他嚴重問題*。不過，這可能讓你
    能夠繞過該錯誤，並取回資料表中仍完好、且區塊標頭仍正常的資料列。
    如果標頭本身已損毀，即使啟用此選項也仍會回報錯誤。
    預設設定為 `off`。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-ZERO-DAMAGED-PAGES"></a>

`zero_damaged_pages` (`boolean`) <a id="id-1.6.6.20.3.25.1.3"></a> [#](#GUC-ZERO-DAMAGED-PAGES)
:   偵測到損毀的頁面標頭通常會導致 PostgreSQL
    回報錯誤，中止目前的交易。將 `zero_damaged_pages`
    設為開啟會使系統改為回報警告，將記憶體中損毀的
    頁面清零，並繼續進行處理。此行為*將會破壞資料*，
    也就是該損毀頁面上的所有資料列。不過，這確實可以讓你
    繞過該錯誤，並取回資料表中任何未損毀頁面的資料列。
    這在因硬體或軟體錯誤造成損毀時，對資料復原很有用。
    你通常應該在放棄從損毀頁面復原資料的希望之前，都不要開啟此設定。
    清零後的頁面不會被強制寫入磁碟，因此建議在
    再次關閉此參數之前重新建立該資料表或索引。
    預設設定為 `off`。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-IGNORE-INVALID-PAGES"></a>

`ignore_invalid_pages` (`boolean`) <a id="id-1.6.6.20.3.26.1.3"></a> [#](#GUC-IGNORE-INVALID-PAGES)
:   若設為 `off`（預設值），在復原期間偵測到
    WAL 記錄參照到無效頁面時，會導致
    PostgreSQL 引發 PANIC 等級的錯誤，中止復原程序。
    將 `ignore_invalid_pages` 設為 `on`
    會使系統忽略 WAL 記錄中的無效頁面參照
    （但仍會回報警告），並繼續復原程序。
    此行為可能會*導致當機、資料遺失、
    擴散或隱藏損毀，或其他嚴重問題*。
    不過，這可能讓你能夠繞過該 PANIC 等級的錯誤，
    完成復原程序，並讓伺服器成功啟動。
    此參數只能在伺服器啟動時設定。它僅在
    復原期間或 standby 模式下才有效果。
<a id="GUC-JIT-DEBUGGING-SUPPORT"></a>

`jit_debugging_support` (`boolean`) <a id="id-1.6.6.20.3.27.1.3"></a> [#](#GUC-JIT-DEBUGGING-SUPPORT)
:   若 LLVM 具備所需功能，將產生的函式向 GDB 註冊。
    這可使除錯更容易。
    預設設定為 `off`。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以在工作階段啟動時變更此參數，
    且工作階段內完全無法變更此參數。
<a id="GUC-JIT-DUMP-BITCODE"></a>

`jit_dump_bitcode` (`boolean`) <a id="id-1.6.6.20.3.28.1.3"></a> [#](#GUC-JIT-DUMP-BITCODE)
:   將產生的 LLVM IR 寫出到
    檔案系統中，位於 [data_directory](runtime-config-file-locations.md#GUC-DATA-DIRECTORY) 內。
    這僅在研究 JIT 實作內部細節時才有用。
    預設設定為 `off`。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。
<a id="GUC-JIT-EXPRESSIONS"></a>

`jit_expressions` (`boolean`) <a id="id-1.6.6.20.3.29.1.3"></a> [#](#GUC-JIT-EXPRESSIONS)
:   決定在啟用 JIT 編譯時（參閱[30.2 節](../jit/jit-decision.md)），
    運算式是否經 JIT 編譯。預設值為
    `on`。
<a id="GUC-JIT-PROFILING-SUPPORT"></a>

`jit_profiling_support` (`boolean`) <a id="id-1.6.6.20.3.30.1.3"></a> [#](#GUC-JIT-PROFILING-SUPPORT)
:   若 LLVM 具備所需功能，會輸出讓
    perf 能夠分析 JIT 產生之函式所需的資料。
    這會將檔案寫出到 `~/.debug/jit/`；
    使用者需自行負責在適當時機清理這些檔案。
    預設設定為 `off`。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以在工作階段啟動時變更此參數，
    且工作階段內完全無法變更此參數。
<a id="GUC-JIT-TUPLE-DEFORMING"></a>

`jit_tuple_deforming` (`boolean`) <a id="id-1.6.6.20.3.31.1.3"></a> [#](#GUC-JIT-TUPLE-DEFORMING)
:   決定在啟用 JIT 編譯時（參閱[30.2 節](../jit/jit-decision.md)），
    tuple 解構（deforming）是否經 JIT 編譯。
    預設值為 `on`。
<a id="GUC-REMOVE-TEMP-FILES-AFTER-CRASH"></a>

`remove_temp_files_after_crash` (`boolean`) <a id="id-1.6.6.20.3.32.1.3"></a> [#](#GUC-REMOVE-TEMP-FILES-AFTER-CRASH)
:   當設為 `on`（預設值）時，
    PostgreSQL 會在 backend 當機後自動移除
    暫存檔案。若停用此選項，檔案會被保留，例如可用於除錯。
    然而，重複發生的當機可能導致這些無用檔案累積。此參數
    只能在 `postgresql.conf` 檔案中或
    伺服器命令列上設定。
<a id="GUC-SEND-ABORT-FOR-CRASH"></a>

`send_abort_for_crash` (`boolean`) <a id="id-1.6.6.20.3.33.1.3"></a> [#](#GUC-SEND-ABORT-FOR-CRASH)
:   預設情況下，backend 當機後，postmaster 會透過傳送
    SIGQUIT 訊號來停止其餘的子程序，
    使它們得以較為優雅地結束。當
    此選項設為 `on` 時，
    會改為傳送 SIGABRT。這通常會
    為每個這類子程序產生一份核心傾印檔案。
    這對於調查當機後其他程序的狀態很有幫助。
    但在反覆發生當機的情況下，也可能消耗大量磁碟空間，
    因此除非你有仔細監控該系統，否則不要啟用此選項。
    請注意，並沒有自動清理核心檔案的機制。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器
    命令列上設定。
<a id="GUC-SEND-ABORT-FOR-KILL"></a>

`send_abort_for_kill` (`boolean`) <a id="id-1.6.6.20.3.34.1.3"></a> [#](#GUC-SEND-ABORT-FOR-KILL)
:   預設情況下，在嘗試以 SIGQUIT
    停止子程序之後，postmaster 會等待五
    秒鐘，然後傳送 SIGKILL 以強制
    立即終止。當此選項設為
    `on` 時，會改為傳送
    SIGABRT 而非 SIGKILL。這通常
    會為每個這類子程序產生一份核心傾印檔案。
    這對於調查「卡住」的子程序的狀態
    很有幫助。但在反覆發生當機的情況下，也可能消耗大量
    磁碟空間，因此除非你有仔細監控該系統，否則不要啟用此選項。
    請注意，並沒有自動清理核心檔案的機制。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器
    命令列上設定。
<a id="GUC-DEBUG-LOGICAL-REPLICATION-STREAMING"></a>

`debug_logical_replication_streaming` (`enum`) <a id="id-1.6.6.20.3.35.1.3"></a> [#](#GUC-DEBUG-LOGICAL-REPLICATION-STREAMING)
:   允許的值有 `buffered` 與
    `immediate`。預設值為 `buffered`。
    此參數旨在用於測試大型交易的邏輯解碼與複寫。
    `debug_logical_replication_streaming` 對於
    發布端與訂閱端的效果不同：

    在發布端，`debug_logical_replication_streaming`
    允許在邏輯解碼中立即串流或序列化變更。
    當設為 `immediate` 時，若
    [`CREATE SUBSCRIPTION`](../../reference/sql-commands/sql-createsubscription.md)
    的
    [`streaming`](../../reference/sql-commands/sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING)
    選項已啟用，則會串流每項變更，否則會序列化每項變更。
    當設為 `buffered` 時，
    解碼會在達到 `logical_decoding_work_mem` 時
    才串流或序列化變更。

    在訂閱端，如果 `streaming` 選項設為
    `parallel`，則 `debug_logical_replication_streaming`
    可用於指示領導者（leader）套用工作程序將變更傳送到
    共享記憶體佇列，或是將所有變更序列化到檔案。當設為
    `buffered` 時，領導者會透過共享記憶體佇列
    將變更傳送給平行套用工作程序。當設為
    `immediate` 時，領導者會將所有變更序列化到檔案，
    並通知平行套用工作程序在交易結束時讀取並套用這些變更。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-developer.html)（原文版本：18.6；核對日期：2026-09-24）
