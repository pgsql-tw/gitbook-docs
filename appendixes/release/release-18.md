<a id="RELEASE-18"></a>

## E.6. 18 版 [#](#release-18) <a href="#release-18" id="release-18"></a>

[E.6.1. 概覽](release-18.md#RELEASE-18-HIGHLIGHTS)

[E.6.2. 遷移至 18 版](release-18.md#RELEASE-18-MIGRATION)

[E.6.3. 變更內容](release-18.md#RELEASE-18-CHANGES)

[E.6.4. 致謝](release-18.md#RELEASE-18-ACKNOWLEDGEMENTS)

**發佈日期：**2025-09-25

<a id="RELEASE-18-HIGHLIGHTS"></a>

### E.6.1. 概覽 [#](#RELEASE-18-HIGHLIGHTS)

PostgreSQL 18 包含許多新功能與改進，包括：

* 非同步 I/O（AIO）子系統，可以提升循序掃描、點陣圖堆積掃描、清理（vacuum）及其他操作的效能。
* [pg_upgrade](../../reference/reference-server/pgupgrade.md)
  現在會保留最佳化器統計資訊。
* 支援「跳躍掃描」（skip scan）查找，讓
  [多欄位 B-tree 索引](../../the-sql-language/indexes/indexes-multicolumn.md)能在更多情況下使用。
* 新增 [`uuidv7()`](../../the-sql-language/functions/functions-uuid.md#FUNC_UUID_GEN_TABLE)
  函式，用於產生依時間戳記排序的
  [UUID](../../the-sql-language/datatype/datatype-uuid.md)。
* 虛擬
  [產生欄位](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-GENERATED-STORED)，
  在讀取操作時才計算其值。這現在是產生欄位的預設方式。
* 支援 [OAuth 認證](../../server-administration/client-authentication/auth-oauth.md)。
* 在 [INSERT](../../reference/sql-commands/sql-insert.md)、[UPDATE](../../reference/sql-commands/sql-update.md)、
  [DELETE](../../reference/sql-commands/sql-delete.md) 與 [MERGE](../../reference/sql-commands/sql-merge.md) 命令的
  [`RETURNING`](../../the-sql-language/dml/dml-returning.md) 子句中支援 `OLD` 與 `NEW`。
* 時態限制條件（temporal constraints），即以範圍為對象的限制條件，適用於
  [PRIMARY KEY](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-PRIMARY-KEY)、
  [UNIQUE](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-UNIQUE) 與
  [FOREIGN KEY](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES)
  限制條件。

以上項目以及 PostgreSQL 18 的其他新功能，在以下各節有更詳細的說明。

<a id="RELEASE-18-MIGRATION"></a>

### E.6.2. 遷移至 18 版 [#](#RELEASE-18-MIGRATION)

想從任何先前版本遷移資料的使用者，必須使用 [pg_dumpall](../../reference/reference-client/app-pg-dumpall.md) 進行傾印／還原，或使用
[pg_upgrade](../../reference/reference-server/pgupgrade.md)，或使用邏輯複寫。關於遷移至新主要版本的一般資訊，請參閱[第 18.6 節](../../server-administration/runtime/upgrading.md)。

18 版包含一些可能影響與先前版本相容性的變更。請注意以下不相容之處：

* 將 [initdb](../../reference/reference-server/app-initdb.md) 的預設值改為啟用資料檢查碼
  (Greg Sabino Mullane)
  [§](https://postgr.es/c/04bec894a04)

  可以使用新的 initdb 選項
  `--no-data-checksums` 停用檢查碼。[pg_upgrade](../../reference/reference-server/pgupgrade.md)
  要求新舊叢集的檢查碼設定一致，因此這個新選項可用於升級未啟用檢查碼的舊叢集。
* 變更時區縮寫的處理方式 (Tom Lane)
  [§](https://postgr.es/c/d7674c9fa)

  系統現在會先採用目前工作階段時區的縮寫，再檢查伺服器變數
  [timezone_abbreviations](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS)。先前會先檢查
  `timezone_abbreviations`。
* 棄用 [MD5 密碼](../../server-administration/client-authentication/auth-password.md)
  認證 (Nathan Bossart)
  [§](https://postgr.es/c/db6a4a985)

  對 MD5 密碼的支援將在未來的主要版本中移除。[CREATE ROLE](../../reference/sql-commands/sql-createrole.md) 與 [ALTER ROLE](../../reference/sql-commands/sql-alterrole.md) 現在於設定 MD5 密碼時會發出棄用警告。可以將
  [md5_password_warnings](../../server-administration/runtime-config/runtime-config-connection.md#GUC-MD5-PASSWORD-WARNINGS) 參數設為
  `off` 來停用這些警告。
* 變更 [VACUUM](../../reference/sql-commands/sql-vacuum.md) 與 [ANALYZE](../../reference/sql-commands/sql-analyze.md)，
  使其處理父資料表的繼承子資料表 (Michael Harris)
  [§](https://postgr.es/c/62ddf7ee9)

  可以使用新的
  `ONLY` 選項執行先前的行為。
* 防止 [`COPY FROM`](../../reference/sql-commands/sql-copy.md)
  在讀取 CSV 檔案時將 `\.` 視為檔案結束標記 (Daniel Vérité, Tom Lane)
  [§](https://postgr.es/c/770233748)
  [§](https://postgr.es/c/da8a4c166)

  [psql](../../reference/reference-client/app-psql.md) 從 `STDIN` 讀取 CSV 檔案時，仍會將
  `\.` 視為檔案結束標記。
  連線到 PostgreSQL 18 伺服器的舊版 psql 用戶端，可能會遇到 [`\copy`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMANDS-COPY)
  問題。此版本也強制規定 `\.`
  必須單獨出現在一行。
* 不再允許無日誌（unlogged）分割資料表 (Michael Paquier)
  [§](https://postgr.es/c/e2bab2d79)

  先前 [`ALTER TABLE SET
  [UN]LOGGED`](../../reference/sql-commands/sql-altertable.md) 不會有任何作用，而且建立無日誌分割資料表時，其子資料表也不會成為無日誌資料表。
* 以觸發事件排入佇列時作用中的角色執行 `AFTER` [觸發程序](../../server-programming/triggers/README.md) (Laurenz Albe)
  [§](https://postgr.es/c/01463e1cc)

  先前這類觸發程序是以觸發程序執行當時（例如在 [COMMIT](../../reference/sql-commands/sql-commit.md) 時）作用中的角色執行。
  在排入佇列到交易提交之間變更角色的情況下，這項差異很重要。
* 移除 [GRANT](../../reference/sql-commands/sql-grant.md)/[REVOKE](../../reference/sql-commands/sql-revoke.md) 中對規則（rule）權限的無作用支援 (Fujii Masao)
  [§](https://postgr.es/c/fefa76f70)

  這些自 PostgreSQL 8.2 起就已不具作用。
* 移除欄位 [`pg_backend_memory_contexts`](../../internals/views/view-pg-backend-memory-contexts.md).`parent`
  (Melih Mutlu)
  [§](https://postgr.es/c/f0d112759)

  由於已新增
  `pg_backend_memory_contexts`.`path`，
  不再需要此欄位。
* 將
  `pg_backend_memory_contexts`.`level`
  與 [`pg_log_backend_memory_contexts()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE)
  改為從 1 起算 (Melih Mutlu, Atsushi Torikoshi, David Rowley,
  Fujii Masao)
  [§](https://postgr.es/c/32d3ed816)
  [§](https://postgr.es/c/d9e03864b)
  [§](https://postgr.es/c/706cbed35)

  這些先前是從 0 起算。
* 變更[全文檢索](../../the-sql-language/textsearch/README.md)，改用叢集預設的定序提供者讀取設定檔與字典，而不再一律使用 libc (Peter Eisentraut)
  [§](https://postgr.es/c/fb1a18810f0)

  預設使用非 libc 定序提供者（例如 ICU、builtin），且這些提供者對 LC_CTYPE 所處理字元的行為與 libc 不同的叢集，可能會觀察到某些全文檢索函式以及 [pg_trgm](../contrib/pgtrgm.md) 擴充功能的行為改變。
  使用 [pg_upgrade](../../reference/reference-server/pgupgrade.md) 升級這類叢集時，建議在升級後重建所有與全文檢索及 pg_trgm 相關的索引。

<a id="RELEASE-18-CHANGES"></a>
### E.6.3. 變更內容 [#](#RELEASE-18-CHANGES)

以下詳細說明 PostgreSQL 18 與前一個主要版本之間的變更。

<a id="RELEASE-18-SERVER"></a>

#### E.6.3.1. 伺服器 [#](#RELEASE-18-SERVER)

<a id="RELEASE-18-OPTIMIZER"></a>

##### E.6.3.1.1. 最佳化器 [#](#RELEASE-18-OPTIMIZER)

* 自動移除某些不必要的資料表自我連接 (Andrey
  Lepikhov, Alexander Kuzmenkov, Alexander Korotkov, Alena Rybakina)
  [§](https://postgr.es/c/fc069a3a6)

  可以使用伺服器變數 [enable_self_join_elimination](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-SELF-JOIN-ELIMINATION) 停用此最佳化。
* 將某些 [`IN (VALUES
  ...)`](../../the-sql-language/functions/functions-comparisons.md#FUNCTIONS-COMPARISONS-IN-SCALAR) 轉換為 `x = ANY ...`，以取得更好的最佳化器統計資訊 (Alena Rybakina, Andrei Lepikhov)
  [§](https://postgr.es/c/c0962a113)
* 允許將 [`OR`](../../the-sql-language/functions/functions-logical.md) 子句轉換為陣列，以加快索引處理 (Alexander Korotkov, Andrey
  Lepikhov)
  [§](https://postgr.es/c/ae4569161)
* 加快 [`INTERSECT`](../../reference/sql-commands/sql-select.md#SQL-INTERSECT)、
  [`EXCEPT`](../../reference/sql-commands/sql-select.md#SQL-EXCEPT)、[視窗彙總函式](../../tutorial/tutorial-advanced/tutorial-window.md)與[檢視表欄位別名](../../reference/sql-commands/sql-createview.md)的處理速度 (Tom Lane,
  David Rowley)
  [§](https://postgr.es/c/52c707483)
  [§](https://postgr.es/c/276279295)
  [§](https://postgr.es/c/8d96f57d5)
  [§](https://postgr.es/c/908a96861)
* 允許在內部重新排列 [`SELECT
  DISTINCT`](../../reference/sql-commands/sql-select.md#SQL-DISTINCT) 的鍵順序以避免排序
  (Richard Guo)
  [§](https://postgr.es/c/a8ccf4e93)

  可以使用 [enable_distinct_reordering](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-DISTINCT-REORDERING) 停用此最佳化。
* 忽略函數相依於其他欄位的 [`GROUP BY`](../../reference/sql-commands/sql-select.md#SQL-GROUPBY)
  欄位 (Zhang
  Mingli, Jian He, David Rowley)
  [§](https://postgr.es/c/bd10ec529)

  若 `GROUP BY` 子句包含某個唯一值索引的所有欄位，以及同一資料表的其他欄位，那些其他欄位就是多餘的，可以從分組中捨去。
  對於非延遲的主鍵，原本就已如此。
* 允許將 [`GROUPING
  SETS`](../../the-sql-language/queries/queries-table-expressions.md#QUERIES-GROUPING-SETS) 上的某些 [`HAVING`](../../reference/sql-commands/sql-select.md#SQL-HAVING) 子句下推為 [`WHERE`](../../reference/sql-commands/sql-select.md#SQL-WHERE) 子句
  (Richard Guo)
  [§](https://postgr.es/c/67a54b9e8)
  [§](https://postgr.es/c/247dea89f)
  [§](https://postgr.es/c/f5050f795)
  [§](https://postgr.es/c/cc5d98525)

  這讓資料列可以更早被篩選。此版本也修正了某些過去會傳回錯誤結果的
  `GROUPING SETS` 查詢。
* 改進對使用 [`numeric`](../../the-sql-language/datatype/datatype-numeric.md)
  與 [`timestamp`](../../the-sql-language/datatype/datatype-datetime.md)
  值的 [`generate_series()`](../../the-sql-language/functions/functions-srf.md#FUNCTIONS-SRF-SERIES) 的資料列數估計 (David Rowley, Song Jinzhou)
  [§](https://postgr.es/c/036bdcec9)
  [§](https://postgr.es/c/97173536e)
* 允許最佳化器使用 `Right Semi Join` 計畫
  (Richard Guo)
  [§](https://postgr.es/c/aa86129e1)

  半連接用於需要判斷是否存在至少一筆相符資料的情況。
* 允許合併連接使用[遞增排序](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-INCREMENTAL-SORT)
  (Richard Guo)
  [§](https://postgr.es/c/828e94c9d)
* 提高規劃存取大量分割區之查詢的效率
  (Ashutosh Bapat, Yuya Watari, David Rowley)
  [§](https://postgr.es/c/88f55bc97)
  [§](https://postgr.es/c/d69d45a5a)
* 允許在更多情況下使用[分割區層級連接（partitionwise
  joins）](../../server-administration/runtime-config/runtime-config-query.md#GUC-ENABLE-PARTITIONWISE-JOIN)，並減少其記憶體用量 (Richard Guo,
  Tom Lane, Ashutosh Bapat)
  [§](https://postgr.es/c/9b282a935)
  [§](https://postgr.es/c/513f4472a)
* 改進分割區查詢的成本估計 (Nikita Malakhov,
  Andrei Lepikhov)
  [§](https://postgr.es/c/fae535da0)
* 改進 [SQL 語言函式](../../server-programming/extend/xfunc-sql.md)的計畫快取 (Alexander Pyhalov, Tom Lane)
  [§](https://postgr.es/c/0dca5d68d)
  [§](https://postgr.es/c/09b07c295)
* 改進對已停用最佳化器功能的處理 (Robert Haas)
  [§](https://postgr.es/c/e22253467)

<a id="RELEASE-18-INDEXES"></a>

##### E.6.3.1.2. 索引 [#](#RELEASE-18-INDEXES)

* 允許對 [btree](../../server-programming/extend/xfunc-sql.md) 索引進行跳躍掃描
  (Peter Geoghegan)
  [§](https://postgr.es/c/92fe23d93)
  [§](https://postgr.es/c/8a510275d)

  這讓多欄位 btree 索引能在更多情況下使用，例如第一個或前幾個索引欄位沒有限制條件（或只有非等值的限制條件），而後面的索引欄位有可用的限制條件時。
* 允許非 btree 的唯一值索引作為分割鍵，以及用於具體化檢視表 (Mark Dilger)
  [§](https://postgr.es/c/f278e1fe3)
  [§](https://postgr.es/c/9d6db8bec)

  該索引類型仍必須支援等值比較。
* 允許平行建立 [`GIN`](../../internals/indextypes/gin.md) 索引 (Tomas Vondra, Matthias van de Meent)
  [§](https://postgr.es/c/8492feb98)
* 允許先將值排序，以加快範圍型別 [GiST](../../internals/indextypes/gist.md) 與 [btree](../../internals/indextypes/btree.md)
  索引的建立 (Bernd Helmle)
  [§](https://postgr.es/c/e9e7b6604)

<a id="RELEASE-18-PERFORMANCE"></a>

##### E.6.3.1.3. 一般效能 [#](#RELEASE-18-PERFORMANCE)

* 新增非同步 I/O 子系統 (Andres Freund, Thomas Munro,
  Nazir Bilal Yavuz, Melanie Plageman)
  [§](https://postgr.es/c/02844012b)
  [§](https://postgr.es/c/da7226993)
  [§](https://postgr.es/c/55b454d0e)
  [§](https://postgr.es/c/247ce06b8)
  [§](https://postgr.es/c/10f664684)
  [§](https://postgr.es/c/06fb5612c)
  [§](https://postgr.es/c/c325a7633)
  [§](https://postgr.es/c/50cb7505b)
  [§](https://postgr.es/c/047cba7fa)
  [§](https://postgr.es/c/12ce89fd0)
  [§](https://postgr.es/c/2a5e709e7)

  此功能讓後端可以將多個讀取請求排入佇列，使循序掃描、點陣圖堆積掃描、清理等操作更有效率。此功能由伺服器變數 [io_method](../../server-administration/runtime-config/runtime-config-resource.md#GUC-IO-METHOD) 啟用，並新增伺服器變數 [io_combine_limit](../../server-administration/runtime-config/runtime-config-resource.md#GUC-IO-COMBINE-LIMIT) 與 [io_max_combine_limit](../../server-administration/runtime-config/runtime-config-resource.md#GUC-IO-MAX-COMBINE-LIMIT) 加以控制。
  這也讓不支援
  `fadvise()` 的系統可以將 [effective_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY)
  與 [maintenance_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY)
  設為大於零的值。新的系統檢視表 [`pg_aios`](../../internals/views/view-pg-aios.md)
  會顯示用於非同步 I/O 的檔案控制代碼。
* 改進存取大量關聯之查詢的鎖定效能
  (Tomas Vondra)
  [§](https://postgr.es/c/c4d5cb71d)
* 改進雜湊連接與
  [`GROUP BY`](../../reference/sql-commands/sql-select.md#SQL-GROUPBY) 的效能並減少記憶體用量
  (David Rowley, Jeff Davis)
  [§](https://postgr.es/c/adf97c156)
  [§](https://postgr.es/c/0f5738202)
  [§](https://postgr.es/c/4d143509c)
  [§](https://postgr.es/c/a0942f441)
  [§](https://postgr.es/c/626df47ad)

  這也改進了 [`EXCEPT`](../../reference/sql-commands/sql-select.md#SQL-EXCEPT) 使用的雜湊集合運算，以及子計畫值的雜湊查找。
* 允許一般清理凍結某些頁面，即使這些頁面已全部可見 (Melanie Plageman)
  [§](https://postgr.es/c/052026c9b)
  [§](https://postgr.es/c/06eae9e62)

  這可以減少之後對整個關聯進行凍結的負擔。凍結的積極程度可以透過伺服器變數與個別資料表設定 [vacuum_max_eager_freeze_failure_rate](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE) 控制。先前清理在需要凍結之前，從不處理已全部可見的頁面。
* 新增伺服器變數 [vacuum_truncate](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-TRUNCATE)，用於控制 [VACUUM](../../reference/sql-commands/sql-vacuum.md) 期間的檔案截斷 (Nathan Bossart,
  Gurjeet Singh)
  [§](https://postgr.es/c/0164a0f9e)

  先前已存在名稱與行為相同的儲存層級參數。
* 將伺服器變數 [effective_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY) 與 [maintenance_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY) 的預設值提高為 16
  (Melanie Plageman)
  [§](https://postgr.es/c/ff79b5b2a)
  [§](https://postgr.es/c/cc6be07eb)

  這更準確地反映現代硬體的情況。

<a id="RELEASE-18-MONITORING"></a>
##### E.6.3.1.4. 監控 [#](#RELEASE-18-MONITORING)

* 提高伺服器變數 [log_connections](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-CONNECTIONS) 的記錄細緻度 (Melanie Plageman)
  [§](https://postgr.es/c/9219093ca)

  此伺服器變數先前只是布林值，布林值仍受支援。
* 新增 `log_connections` 選項，用於回報各連線階段的持續時間 (Melanie Plageman)
  [§](https://postgr.es/c/18cd15e70)
* 新增 [log_line_prefix](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-LINE-PREFIX) 跳脫序列
  `%L`，用於輸出用戶端 IP 位址 (Greg Sabino Mullane)
  [§](https://postgr.es/c/3516ea768)
* 新增伺服器變數 [log_lock_failures](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-LOCK-FAILURES)，用於記錄取得鎖定失敗的情況 (Yuki Seino, Fujii Masao)
  [§](https://postgr.es/c/6d376c3b0)
  [§](https://postgr.es/c/73bdcfab3)

  具體來說，它會回報 [`SELECT
  ... NOWAIT`](../../reference/sql-commands/sql-select.md#SQL-FOR-UPDATE-SHARE) 的鎖定失敗。
* 修改 [`pg_stat_all_tables`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW)
  及其變體，以回報花費在 [VACUUM](../../reference/sql-commands/sql-vacuum.md)、[ANALYZE](../../reference/sql-commands/sql-analyze.md) 及其
  [自動](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)版本上的時間 (Sami Imseih)
  [§](https://postgr.es/c/30a6ed0ce)

  新欄位為 `total_vacuum_time`、
  `total_autovacuum_time`、
  `total_analyze_time` 與
  `total_autoanalyze_time`。
* 為 [VACUUM](../../reference/sql-commands/sql-vacuum.md) 與 [ANALYZE](../../reference/sql-commands/sql-analyze.md) 新增延遲時間回報 (Bertrand Drouvot, Nathan Bossart)
  [§](https://postgr.es/c/bb8dff999)
  [§](https://postgr.es/c/7720082ae)

  此資訊會出現在伺服器日誌、系統檢視表 [`pg_stat_progress_vacuum`](../../server-administration/monitoring/progress-reporting.md#VACUUM-PROGRESS-REPORTING)
  與 [`pg_stat_progress_analyze`](../../server-administration/monitoring/progress-reporting.md#PG-STAT-PROGRESS-ANALYZE-VIEW)，
  以及 [VACUUM](../../reference/sql-commands/sql-vacuum.md) 與 [ANALYZE](../../reference/sql-commands/sql-analyze.md) 在 `VERBOSE`
  模式下的輸出中；必須以伺服器變數 [track_cost_delay_timing](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING) 啟用追蹤。
* 在 `ANALYZE VERBOSE` 的輸出中新增 WAL、CPU 與平均讀取統計資訊
  (Anthonin Bonnefoy)
  [§](https://postgr.es/c/4c1b4cdb8)
  [§](https://postgr.es/c/bb7775234)
* 在
  `VACUUM`/`ANALYZE (VERBOSE)`
  與 autovacuum 的日誌輸出中新增 WAL 緩衝區已滿的次數 (Bertrand Drouvot)
  [§](https://postgr.es/c/6a8a7ce47)
* 新增個別後端的 I/O 統計資訊回報 (Bertrand Drouvot)
  [§](https://postgr.es/c/9aea73fc6)
  [§](https://postgr.es/c/3f1db99bf)

  可以透過 [`pg_stat_get_backend_io()`](../../server-administration/monitoring/monitoring-stats.md#PG-STAT-GET-BACKEND-IO) 存取這些統計資訊。
  可以透過 [`pg_stat_reset_backend_stats()`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-STATS-FUNCS-TABLE) 清除個別後端的 I/O 統計資訊。
* 新增 [`pg_stat_io`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW)
  欄位，以位元組為單位回報 I/O 活動 (Nazir Bilal Yavuz)
  [§](https://postgr.es/c/f92c854cf)

  新欄位為 `read_bytes`、
  `write_bytes` 與
  `extend_bytes`。原本恆等於
  [`BLCKSZ`](../../server-administration/runtime-config/runtime-config-preset.md#GUC-BLOCK-SIZE) 的
  `op_bytes` 欄位已移除。
* 在
  `pg_stat_io` 中新增 WAL I/O 活動的資料列 (Nazir Bilal Yavuz, Bertrand
  Drouvot, Michael Paquier)
  [§](https://postgr.es/c/a051e71e2)
  [§](https://postgr.es/c/4538bd3f1)
  [§](https://postgr.es/c/7f7f324eb)

  這包括 WAL 接收程序的活動，以及這類寫入的等待事件。
* 變更伺服器變數 [track_wal_io_timing](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING)，
  改為控制在 `pg_stat_io` 中追蹤 WAL 時間，而不是在 [`pg_stat_wal`](../../server-administration/monitoring/monitoring-stats.md#PG-STAT-WAL-VIEW) 中
  (Bertrand Drouvot)
  [§](https://postgr.es/c/6c349d83b)
* 從 `pg_stat_wal` 移除讀取／同步相關欄位
  (Bertrand Drouvot)
  [§](https://postgr.es/c/2421e9a51)
  [§](https://postgr.es/c/6c349d83b)

  這會移除欄位 `wal_write`、
  `wal_sync`、
  `wal_write_time` 與
  `wal_sync_time`。（原文此處寫作 read/sync，但移除的欄位實為寫入與同步相關。）
* 新增函式 [`pg_stat_get_backend_wal()`](../../server-administration/monitoring/monitoring-stats.md#PG-STAT-GET-BACKEND-WAL)，
  用於傳回個別後端的 WAL 統計資訊 (Bertrand
  Drouvot)
  [§](https://postgr.es/c/76def4cdd)

  可以透過 [`pg_stat_reset_backend_stats()`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-STATS-FUNCS-TABLE) 清除個別後端的 WAL 統計資訊。
* 新增函式 [`pg_ls_summariesdir()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-GENFILE-TABLE)，
  專門用於列出 [`PGDATA`](../../internals/storage/storage-file-layout.md)/[`pg_wal/summaries`](../../server-administration/runtime-config/runtime-config-wal.md#GUC-WAL-SUMMARY-KEEP-TIME) 的內容
  (Yushi Ogiwara)
  [§](https://postgr.es/c/4e1fad378)
* 新增欄位 [`pg_stat_checkpointer`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW).`num_done`，
  用於回報已完成的檢查點數量 (Anton A. Melnikov)
  [§](https://postgr.es/c/559efce1d)

  欄位 `num_timed` 與
  `num_requested` 會同時計入已完成與已略過的檢查點。
* 新增欄位
  `pg_stat_checkpointer`.`slru_written`，
  用於回報已寫入的 SLRU 緩衝區 (Nitin Jadhav)
  [§](https://postgr.es/c/17cc5f666)

  此外，也修改檢查點的伺服器日誌訊息，分別回報共享緩衝區與 SLRU 緩衝區的值。
* 在 [`pg_stat_database`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW) 中新增欄位，
  用於回報平行工作程序的活動 (Benoit Lobréau)
  [§](https://postgr.es/c/e7a9496de)

  新欄位為
  `parallel_workers_to_launch` 與
  `parallel_workers_launched`。
* 計算[查詢識別碼](../../server-administration/runtime-config/runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID)時，常數清單只考慮第一個與最後一個常數 (Dmitry
  Dolgov, Sami Imseih)
  [§](https://postgr.es/c/62d712ecf)
  [§](https://postgr.es/c/9fbd53dea)
  [§](https://postgr.es/c/c2da1a5d6)

  [pg_stat_statements](../contrib/pgstatstatements.md) 會使用這種雜湊化計算（jumbling）。
* 調整查詢識別碼的計算方式，將使用相同關聯名稱的查詢歸為一組 (Michael Paquier, Sami Imseih)
  [§](https://postgr.es/c/787514b30)

  即使位於不同綱要中的資料表具有不同的欄位名稱，也是如此。
* 新增欄位 [`pg_backend_memory_contexts`](../../internals/views/view-pg-backend-memory-contexts.md).`type`，
  用於回報記憶體上下文的類型 (David Rowley)
  [§](https://postgr.es/c/12227a1d5)
* 新增欄位
  `pg_backend_memory_contexts`.`path`，
  用於顯示記憶體上下文的上層 (Melih Mutlu)
  [§](https://postgr.es/c/32d3ed816)

<a id="RELEASE-18-PRIVILEGES"></a>

##### E.6.3.1.5. 權限 [#](#RELEASE-18-PRIVILEGES)

* 新增函式 [`pg_get_acl()`](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-OBJECT-TABLE)，
  用於取得資料庫存取控制的詳細資訊 (Joel Jacobson)
  [§](https://postgr.es/c/4564f1ceb)
  [§](https://postgr.es/c/d898665bf)
* 新增函式 [`has_largeobject_privilege()`](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-ACCESS-TABLE)，
  用於檢查大型物件權限 (Yugo Nagata)
  [§](https://postgr.es/c/4eada203a)
* 允許 [ALTER DEFAULT PRIVILEGES](../../reference/sql-commands/sql-alterdefaultprivileges.md) 定義大型物件的預設權限 (Takatsuka Haruka, Yugo Nagata,
  Laurenz Albe)
  [§](https://postgr.es/c/0d6c47766)
* 新增預先定義角色 [`pg_signal_autovacuum_worker`](../../server-administration/user-manag/predefined-roles.md)
  (Kirill Reshke)
  [§](https://postgr.es/c/ccd38024b)

  這允許向 autovacuum 工作程序傳送訊號。

<a id="RELEASE-18-SERVER-CONFIG"></a>
##### E.6.3.1.6. 伺服器設定 [#](#RELEASE-18-SERVER-CONFIG)

* 新增對 [OAuth 認證方法](../../server-administration/client-authentication/auth-oauth.md)的支援 (Jacob Champion, Daniel Gustafsson, Thomas Munro)
  [§](https://postgr.es/c/b3f0be788)

  這為 [`pg_hba.conf`](../../server-administration/client-authentication/auth-pg-hba-conf.md) 新增 `oauth` 認證方法，
  並新增 libpq 的 OAuth 選項、用於載入權杖驗證程式庫的伺服器變數 [oauth_validator_libraries](../../server-administration/runtime-config/runtime-config-connection.md#GUC-OAUTH-VALIDATOR-LIBRARIES)，以及用於加入所需編譯時期程式庫的 configure 旗標 [`--with-libcurl`](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBCURL)。
* 新增伺服器變數 [ssl_tls13_ciphers](../../server-administration/runtime-config/runtime-config-connection.md#GUC-SSL-TLS13-CIPHERS)，允許指定多個以冒號分隔的 TLSv1.3 加密套件
  (Erica Zhang, Daniel Gustafsson)
  [§](https://postgr.es/c/45188c2ea)
* 將伺服器變數 [ssl_groups](../../server-administration/runtime-config/runtime-config-connection.md#GUC-SSL-GROUPS) 的預設值改為包含橢圓曲線 X25519 (Daniel Gustafsson, Jacob Champion)
  [§](https://postgr.es/c/daa02c6bd)
* 將伺服器變數 `ssl_ecdh_curve` 更名為 [ssl_groups](../../server-administration/runtime-config/runtime-config-connection.md#GUC-SSL-GROUPS)，並允許指定多個以冒號分隔的 ECDH 曲線 (Erica Zhang,
  Daniel Gustafsson)
  [§](https://postgr.es/c/3d1ef3a15)

  舊名稱仍然可用。
* 將[取消請求金鑰](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE)改為 256 位元 (Heikki Linnakangas, Jelte Fennema-Nio)
  [§](https://postgr.es/c/a460251f0)
  [§](https://postgr.es/c/9d9b9d46f)

  只有在伺服器與用戶端都支援此版本引入的通訊協定（wire protocol）3.2 版時，才能這麼做。
* 新增伺服器變數 [autovacuum_worker_slots](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS)，
  用於指定背景工作程序的最大數量 (Nathan Bossart)
  [§](https://postgr.es/c/c758119e5)

  設定此變數後，可以在執行期間將 [autovacuum_max_workers](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS)
  調整到不超過此最大值，而不需要重新啟動伺服器。
* 允許指定觸發 [autovacuum](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM) 的固定死亡資料列數量 (Nathan
  Bossart, Frédéric Yhuel)
  [§](https://postgr.es/c/306dc520b)

  此伺服器變數為 [autovacuum_vacuum_max_threshold](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD)。觸發條件仍會使用百分比。
* 變更伺服器變數 [max_files_per_process](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-FILES-PER-PROCESS)，
  使其只限制後端開啟的檔案 (Andres Freund)
  [§](https://postgr.es/c/adb5f85fa)

  先前 postmaster 開啟的檔案也會計入此限制。
* 新增伺服器變數 [num_os_semaphores](../../server-administration/runtime-config/runtime-config-preset.md#GUC-NUM-OS-SEMAPHORES)，
  用於回報所需的號誌數量 (Nathan Bossart)
  [§](https://postgr.es/c/0dcaea569)

  這對作業系統設定很有用。
* 新增伺服器變數 [extension_control_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-EXTENSION-CONTROL-PATH)，
  用於指定擴充功能控制檔的位置 (Peter Eisentraut,
  Matheus Alcantara)
  [§](https://postgr.es/c/4f7f7b037)
  [§](https://postgr.es/c/81eaaa2c4)

<a id="RELEASE-18-REPLICATION"></a>

##### E.6.3.1.7. 串流複寫與復原 [#](#RELEASE-18-REPLICATION)

* 允許使用伺服器變數 [idle_replication_slot_timeout](../../server-administration/runtime-config/runtime-config-replication.md#GUC-IDLE-REPLICATION-SLOT-TIMEOUT) 自動使非作用中的複寫插槽失效
  (Nisha Moond, Bharath Rupireddy)
  [§](https://postgr.es/c/ac0e33136)
* 新增伺服器變數 [max_active_replication_origins](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-ACTIVE-REPLICATION-ORIGINS)，用於控制作用中複寫來源的最大數量 (Euler Taveira)
  [§](https://postgr.es/c/04ff636cb)

  此數量先前由 [max_replication_slots](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-REPLICATION-SLOTS) 控制，但這個新設定可以在所需插槽較少的情況下，允許較多的複寫來源。

<a id="RELEASE-18-LOGICAL"></a>

##### E.6.3.1.8. [邏輯複寫](../../server-administration/logical-replication/README.md) [#](#RELEASE-18-LOGICAL)

* 允許以邏輯複寫方式複寫[產生欄位](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-GENERATED-STORED)的值 (Shubham Khanna, Vignesh C,
  Zhijie Hou, Shlok Kyal, Peter Smith)
  [§](https://postgr.es/c/745217a05)
  [§](https://postgr.es/c/7054186c4)
  [§](https://postgr.es/c/87ce27de6)
  [§](https://postgr.es/c/6252b1eaf)

  若發佈指定了欄位清單，則所有指定的欄位（無論是否為產生欄位）都會發佈。
  若未指定欄位清單，則由發佈選項
  `publish_generated_columns` 控制是否發佈產生欄位。先前產生欄位不會被複寫，訂閱者必須在可能的情況下自行計算其值；這對缺乏此能力的非 PostgreSQL 訂閱者特別有用。
* 將 [CREATE SUBSCRIPTION](../../reference/sql-commands/sql-createsubscription.md) 的串流（streaming）選項預設值從 `off` 改為 `parallel`
  (Vignesh C)
  [§](https://postgr.es/c/1bf1140be)
* 允許 [ALTER SUBSCRIPTION](../../reference/sql-commands/sql-altersubscription.md) 變更複寫插槽的兩階段提交行為 (Hayato Kuroda, Ajin
  Cherian, Amit Kapila, Zhijie Hou)
  [§](https://postgr.es/c/1462aad2e)
  [§](https://postgr.es/c/4868c96bc)
* 在套用邏輯複寫變更時記錄[衝突](../../server-administration/high-availability/hot-standby.md#HOT-STANDBY-CONFLICT) (Zhijie Hou, Nisha Moond)
  [§](https://postgr.es/c/9758174e2)
  [§](https://postgr.es/c/edcb71258)
  [§](https://postgr.es/c/640178c92)
  [§](https://postgr.es/c/6c2b5edec)
  [§](https://postgr.es/c/73eba5004)

  同時也在 [`pg_stat_subscription_stats`](../../server-administration/monitoring/monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS) 的新欄位中回報。

<a id="RELEASE-18-UTILITY"></a>

#### E.6.3.2. 公用程式命令 [#](#RELEASE-18-UTILITY)

* 允許[產生欄位](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-GENERATED-STORED)為虛擬欄位，並將其設為預設 (Peter
  Eisentraut, Jian He, Richard Guo, Dean Rasheed)
  [§](https://postgr.es/c/83ea6c540)
  [§](https://postgr.es/c/cdc168ad4)
  [§](https://postgr.es/c/1e4351af3)

  虛擬產生欄位會在讀取欄位時（而不是寫入時）產生其值。仍可以透過 `STORED` 選項指定寫入時產生的行為。
* 在 DML 查詢的 [`RETURNING`](../../the-sql-language/dml/dml-returning.md) 中新增 `OLD`/`NEW` 支援 (Dean Rasheed)
  [§](https://postgr.es/c/80feb727c)

  先前 `RETURNING` 對 [INSERT](../../reference/sql-commands/sql-insert.md) 與 [UPDATE](../../reference/sql-commands/sql-update.md) 只傳回新值，對 [DELETE](../../reference/sql-commands/sql-delete.md) 只傳回舊值；[MERGE](../../reference/sql-commands/sql-merge.md)
  則會傳回其內部所執行查詢的對應值。
  這個新語法讓
  `INSERT`/`UPDATE`/`DELETE`/`MERGE`
  的 `RETURNING` 清單可以使用特殊別名
  `old` 與 `new` 明確傳回舊值與新值。這些別名可以重新命名，以避免識別字衝突。
* 允許仿照現有的本機資料表建立外部資料表
  (Zhang Mingli)
  [§](https://postgr.es/c/302cf1575)

  語法為 [`CREATE
  FOREIGN TABLE ... LIKE`](../../reference/sql-commands/sql-createforeigntable.md)。
* 允許在[非確定性定序](../../server-administration/charset/collation.md#COLLATION-NONDETERMINISTIC)下使用 [`LIKE`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-LIKE) (Peter Eisentraut)
  [§](https://postgr.es/c/85b7efa1c)
* 允許在非確定性定序下使用文字位置搜尋函式
  (Peter Eisentraut)
  [§](https://postgr.es/c/329304c90)

  這些過去會產生錯誤。
* 新增內建定序提供者 [`PG_UNICODE_FAST`](../../server-administration/charset/locale.md#LOCALE-PROVIDERS)
  (Jeff Davis)
  [§](https://postgr.es/c/d3d098316)

  此語系支援大小寫對應，但依碼位順序排序，而非自然語言順序。
* 允許 [VACUUM](../../reference/sql-commands/sql-vacuum.md) 與 [ANALYZE](../../reference/sql-commands/sql-analyze.md)
  處理分割資料表而不處理其子資料表
  (Michael Harris)
  [§](https://postgr.es/c/62ddf7ee9)

  這由新的 `ONLY` 選項啟用。由於 autovacuum 不會處理分割資料表，只處理其子資料表，因此這很有用。
* 新增用於修改個別關聯與個別欄位最佳化器統計資訊的函式 (Corey Huinker)
  [§](https://postgr.es/c/e839c8ecc)
  [§](https://postgr.es/c/d32d14639)
  [§](https://postgr.es/c/650ab8aaf)

  這些函式為 [`pg_restore_relation_stats()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-STATSMOD)、
  `pg_restore_attribute_stats()`、
  `pg_clear_relation_stats()` 與
  `pg_clear_attribute_stats()`。
* 新增伺服器變數 [file_copy_method](../../server-administration/runtime-config/runtime-config-resource.md#GUC-FILE-COPY-METHOD)，用於控制檔案複製方式 (Nazir Bilal Yavuz)
  [§](https://postgr.es/c/f78ca6f3e)

  它控制 [`CREATE DATABASE
  ... STRATEGY=FILE_COPY`](../../reference/sql-commands/sql-createdatabase.md) 與 [`ALTER DATABASE ... SET
  TABLESPACE`](../../reference/sql-commands/sql-alterdatabase.md) 要使用一般的檔案複製，還是檔案系統的複製（clone）功能。

<a id="RELEASE-18-CONSTRAINTS"></a>
##### E.6.3.2.1. [限制條件](../../the-sql-language/ddl/ddl-constraints.md) [#](#RELEASE-18-CONSTRAINTS)

* 允許指定不重疊的 [`PRIMARY
  KEY`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-PRIMARY-KEY)、[`UNIQUE`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-UNIQUE) 與
  [外鍵](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES)
  限制條件 (Paul A. Jungwirth)
  [§](https://postgr.es/c/fc0438b4e)
  [§](https://postgr.es/c/89f908a6d)

  對 `PRIMARY KEY` 與 `UNIQUE` 以 `WITHOUT OVERLAPS` 指定，對外鍵則以
  `PERIOD` 指定，兩者都套用於最後一個指定的欄位。
* 允許將 [`CHECK`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-CHECK)
  與[外鍵](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES)限制條件指定為 `NOT
  ENFORCED` (Amul Sul)
  [§](https://postgr.es/c/ca87c415e)
  [§](https://postgr.es/c/eec0040c4)

  這也新增了欄位 [`pg_constraint`](../../internals/catalogs/catalog-pg-constraint.md).`conenforced`。
* 要求[主鍵／外鍵](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES)
  關係使用確定性定序，或使用相同的非確定性定序 (Peter Eisentraut)
  [§](https://postgr.es/c/9321d2fdf)

  若不符合這些要求，還原 [pg_dump](../../reference/reference-client/app-pgdump.md) 的傾印（[pg_upgrade](../../reference/reference-server/pgupgrade.md) 也會使用此方式）將會失敗；
  必須先修改綱要，這些升級方式才能成功。
* 將欄位的 [`NOT
  NULL`](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-PARMS-NOT-NULL) 設定儲存在 [`pg_constraint`](../../internals/catalogs/catalog-pg-constraint.md) 中
  (Álvaro Herrera, Bernd Helmle)
  [§](https://postgr.es/c/14e87ffa5)
  [§](https://postgr.es/c/81ce602d4)

  這讓 `NOT NULL`
  限制條件可以指定名稱。這也為外部資料表加入 `NOT NULL` 限制條件，並為本機資料表加入 `NOT NULL` 繼承控制。
* 允許 [ALTER TABLE](../../reference/sql-commands/sql-altertable.md) 設定 `NOT NULL` 限制條件的 `NOT
  VALID` 屬性
  (Rushabh Lathia, Jian He)
  [§](https://postgr.es/c/a379061a2)
* 允許修改 `NOT
  NULL` 限制條件的可繼承性 (Suraj Kharage, Álvaro Herrera)
  [§](https://postgr.es/c/f4e53e10b)
  [§](https://postgr.es/c/4a02af8b1)

  語法為 [`ALTER TABLE
  ... ALTER CONSTRAINT ... [NO] INHERIT`](../../reference/sql-commands/sql-altertable.md)。
* 允許在分割資料表上使用 `NOT VALID` 外鍵限制條件 (Amul Sul)
  [§](https://postgr.es/c/b663b9436)
* 允許在分割資料表上以 `ONLY` [移除](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-DESC-DROP-CONSTRAINT)限制條件
  (Álvaro Herrera)
  [§](https://postgr.es/c/4dea33ce7)

  先前這項操作被錯誤地禁止。

<a id="RELEASE-18-COPY"></a>

##### E.6.3.2.2. [COPY](../../reference/sql-commands/sql-copy.md) [#](#RELEASE-18-COPY)

* 新增 `REJECT_LIMIT`，用於控制 `COPY FROM` 可以忽略的無效資料列數量 (Atsushi Torikoshi)
  [§](https://postgr.es/c/4ac2a9bec)

  此選項在 `ON_ERROR = 'ignore'` 時可用。
* 允許 `COPY TO` 從已填入資料的具體化檢視表複製資料列 (Jian He)
  [§](https://postgr.es/c/534874fac)
* 新增 `COPY` 的 `LOG_VERBOSITY` 層級
  `silent`，用於抑制被忽略資料列的日誌輸出
  (Atsushi Torikoshi)
  [§](https://postgr.es/c/e7834a1a2)

  這個新層級會在
  `on_error = 'ignore'` 時，抑制被捨棄輸入資料列的輸出。
* 不再允許對外部資料表使用 `COPY FREEZE` (Nathan
  Bossart)
  [§](https://postgr.es/c/401a6956f)

  先前 `COPY` 可以執行，但
  `FREEZE` 會被忽略，因此不再允許此命令。

<a id="RELEASE-18-EXPLAIN"></a>

##### E.6.3.2.3. [EXPLAIN](../../reference/sql-commands/sql-explain.md) [#](#RELEASE-18-EXPLAIN)

* 在 `EXPLAIN ANALYZE` 中自動包含 `BUFFERS` 輸出 (Guillaume Lelarge, David Rowley)
  [§](https://postgr.es/c/c2a4078eb)
* 在 `EXPLAIN
  (WAL)` 的輸出中新增 WAL 緩衝區已滿的次數 (Bertrand Drouvot)
  [§](https://postgr.es/c/320545bfc)
* 在 `EXPLAIN ANALYZE` 中，回報每個索引掃描節點所使用的索引查找次數 (Peter Geoghegan)
  [§](https://postgr.es/c/0fbceae84)
* 修改 `EXPLAIN`，使其輸出帶小數的資料列數
  (Ibrar Ahmed, Ilia Evdokimov, Robert Haas)
  [§](https://postgr.es/c/ddb17e387)
  [§](https://postgr.es/c/95dbd827f)
* 在 `EXPLAIN` 輸出中，為 `Material`、
  `Window Aggregate` 與通用資料表運算式（CTE）節點加入記憶體與磁碟用量的詳細資訊 (David Rowley, Tatsuo
  Ishii)
  [§](https://postgr.es/c/1eff8279d)
  [§](https://postgr.es/c/53abb1e0e)
  [§](https://postgr.es/c/95d6e9af0)
  [§](https://postgr.es/c/40708acd6)
* 在 `EXPLAIN` 輸出中加入視窗函式引數的詳細資訊 (Tom Lane)
  [§](https://postgr.es/c/8b1b34254)
* 在 `EXPLAIN ANALYZE` 中加入 `Parallel Bitmap Heap Scan` 工作程序的快取統計資訊 (David Geier,
  Heikki Linnakangas, Donghang Lin, Alena Rybakina, David Rowley)
  [§](https://postgr.es/c/5a1e6df3b)
* 在 `EXPLAIN ANALYZE` 輸出中標示已停用的節點
  (Robert Haas, David Rowley, Laurenz Albe)
  [§](https://postgr.es/c/c01743aa4)
  [§](https://postgr.es/c/161320b4b)
  [§](https://postgr.es/c/84b8fccbe)

<a id="RELEASE-18-DATATYPES"></a>

#### E.6.3.3. 資料型別 [#](#RELEASE-18-DATATYPES)

* 改進 [Unicode](../../server-administration/charset/collation.md#COLLATION-MANAGING-STANDARD)
  完整大小寫對應與轉換 (Jeff Davis)
  [§](https://postgr.es/c/4e7f62bc3)
  [§](https://postgr.es/c/286a365b9)

  這新增了條件式大小寫對應與首字大寫（title case）對應的能力，並能將單一字元對應為多個字元。
* 允許將 [`jsonb`](../../the-sql-language/datatype/datatype-json.md)
  的 `null` 值轉型為純量型別的
  `NULL` (Tom Lane)
  [§](https://postgr.es/c/a5579a90a)

  先前這類轉型會產生錯誤。
* 為 [`json{b}_strip_nulls`](../../the-sql-language/functions/functions-json.md#FUNCTIONS-JSON-PROCESSING-TABLE) 新增選用參數，
  允許移除值為 null 的陣列元素 (Florents Tselai)
  [§](https://postgr.es/c/4603903d2)
* 新增函式 [`array_sort()`](../../the-sql-language/functions/functions-array.md#ARRAY-FUNCTIONS-TABLE)，
  用於排序陣列的第一個維度 (Junwang Zhao, Jian He)
  [§](https://postgr.es/c/6c12ae09f)
* 新增函式 [`array_reverse()`](../../the-sql-language/functions/functions-array.md#ARRAY-FUNCTIONS-TABLE)，
  用於反轉陣列的第一個維度 (Aleksander Alekseev)
  [§](https://postgr.es/c/49d6c7d8d)
* 新增函式 [`reverse()`](../../the-sql-language/functions/functions-string.md#FUNCTIONS-STRING-OTHER)，
  用於反轉 bytea 的位元組 (Aleksander Alekseev)
  [§](https://postgr.es/c/0697b2390)
* 允許在整數型別與 [`bytea`](../../the-sql-language/datatype/datatype-binary.md) 之間轉型 (Aleksander
  Alekseev)
  [§](https://postgr.es/c/6da469bad)

  整數值會以二補數形式儲存為 `bytea` 值。
* 將 Unicode 資料更新至 [Unicode](../../server-administration/charset/collation.md#COLLATION-MANAGING-STANDARD) 16.0.0 (Peter
  Eisentraut)
  [§](https://postgr.es/c/82a46cca9)
* 新增愛沙尼亞語的全文檢索[詞幹處理](../../the-sql-language/textsearch/textsearch-dictionaries.md#TEXTSEARCH-SNOWBALL-DICTIONARY)
  (Tom Lane)
  [§](https://postgr.es/c/b464e51ab)
* 改進 [`XML`](../../the-sql-language/datatype/datatype-xml.md)
  錯誤碼，使其更貼近 SQL 標準
  (Tom Lane)
  [§](https://postgr.es/c/cd838e200)

  這些錯誤會透過 [`SQLSTATE`](../errcodes-appendix/README.md) 回報。

<a id="RELEASE-18-FUNCTIONS"></a>
#### E.6.3.4. 函式 [#](#RELEASE-18-FUNCTIONS)

* 新增函式 [`casefold()`](../../the-sql-language/functions/functions-string.md#FUNCTIONS-STRING-OTHER)，
  以支援更精細的不區分大小寫比對 (Jeff Davis)
  [§](https://postgr.es/c/bfc599206)

  這能進行更準確的比較，也就是說，某個字元可能有多個大寫或小寫的對應字元，或者大小寫轉換會改變字元數量。
* 允許對陣列與複合型別使用 [`MIN()`](../../the-sql-language/functions/functions-aggregate.md#FUNCTIONS-AGGREGATE-TABLE)/[`MAX()`](../../the-sql-language/functions/functions-aggregate.md#FUNCTIONS-AGGREGATE-TABLE)
  彙總函式 (Aleksander Alekseev,
  Marat Buharov)
  [§](https://postgr.es/c/a0f1fce80)
  [§](https://postgr.es/c/2d24fd942)
* 為 [`EXTRACT()`](../../the-sql-language/functions/functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT) 新增 `WEEK` 選項
  (Tom Lane)
  [§](https://postgr.es/c/6be39d77a)
* 改進 `EXTRACT(QUARTER ...)` 對負值的輸出 (Tom Lane)
  [§](https://postgr.es/c/6be39d77a)
* 為 [`to_number()`](../../the-sql-language/functions/functions-formatting.md#FUNCTIONS-FORMATTING-TABLE) 新增羅馬數字支援
  (Hunaid Sohail)
  [§](https://postgr.es/c/172e6b3ad)

  可透過 `RN` 樣式使用此功能。
* 新增 [`UUID`](../../the-sql-language/datatype/datatype-uuid.md)
  第 7 版產生函式 [`uuidv7()`](../../the-sql-language/functions/functions-uuid.md#FUNC_UUID_GEN_TABLE)
  (Andrey Borodin)
  [§](https://postgr.es/c/78c5e141e)

  這種 `UUID` 值可以依時間排序。另新增函式別名 [`uuidv4()`](../../the-sql-language/functions/functions-uuid.md#FUNC_UUID_GEN_TABLE)，
  用於明確產生第 4 版 UUID。
* 新增函式 [`crc32()`](../../the-sql-language/functions/functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER)
  與 [`crc32c()`](../../the-sql-language/functions/functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER)，
  用於計算 CRC 值 (Aleksander Alekseev)
  [§](https://postgr.es/c/760162fed)
* 新增數學函式 [`gamma()`](../../the-sql-language/functions/functions-math.md#FUNCTIONS-MATH-FUNC-TABLE)
  與 [`lgamma()`](../../the-sql-language/functions/functions-math.md#FUNCTIONS-MATH-FUNC-TABLE)
  (Dean Rasheed)
  [§](https://postgr.es/c/a3b6dfd41)
* 在 [PL/pgSQL](../../server-programming/plpgsql/README.md) 中，允許以 `=>` 語法指定具名游標引數 (Pavel Stehule)
  [§](https://postgr.es/c/246dedc5d)

  先前只接受 `:=`。
* 允許 [`regexp_match[es]()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_like()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_replace()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_count()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_instr()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_substr()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_split_to_table()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)/[`regexp_split_to_array()`](../../the-sql-language/functions/functions-matching.md#FUNCTIONS-POSIX-REGEXP)
  使用具名引數 (Jian He)
  [§](https://postgr.es/c/580f8727c)

<a id="RELEASE-18-LIBPQ"></a>

#### E.6.3.5. [libpq](../../client-interfaces/libpq/README.md) [#](#RELEASE-18-LIBPQ)

* 新增函式 [`PQfullProtocolVersion()`](../../client-interfaces/libpq/libpq-status.md#libpq-pqfullprotocolversion)，
  用於回報包含次要版本號的完整協定版本號 (Jacob
  Champion, Jelte Fennema-Nio)
  [§](https://postgr.es/c/cdb6b0fdb)
* 新增 libpq 連線[參數](../../client-interfaces/libpq/libpq-paramkeywords.md#libpq-connect-ssl-max-protocol-version)
  與[環境變數](../../client-interfaces/libpq/libpq-envars.md)，
  用於指定連線可接受的最低與最高協定版本 (Jelte Fennema-Nio)
  [§](https://postgr.es/c/285613c60)
  [§](https://postgr.es/c/507034910)
* 將 [search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 的變更回報給用戶端
  (Alexander Kukushkin, Jelte Fennema-Nio, Tomas Vondra)
  [§](https://postgr.es/c/28a1121fd)
  [§](https://postgr.es/c/0d06a7eac)
* 為所有訊息類型（包括認證）新增 [`PQtrace()`](../../client-interfaces/libpq/libpq-control.md#libpq-pqtrace) 輸出 (Jelte Fennema-Nio)
  [§](https://postgr.es/c/ea92f3a0a)
  [§](https://postgr.es/c/a5c6b8f22)
  [§](https://postgr.es/c/b8b3f861f)
  [§](https://postgr.es/c/e87c14b19)
  [§](https://postgr.es/c/7adec2d5f)
* 新增 libpq 連線參數 [`sslkeylogfile`](../../client-interfaces/libpq/libpq-paramkeywords.md#libpq-connect-sslkeylogfile)，
  用於傾印 SSL 金鑰資料 (Abhishek Chanda,
  Daniel Gustafsson)
  [§](https://postgr.es/c/2da74d8d6)

  這對除錯很有用。
* 修改部分 libpq 函式的簽章，改用
  `int64_t` (Thomas Munro)
  [§](https://postgr.es/c/3c86223c9)

  這些函式先前使用 `pg_int64`，該型別現已棄用。

<a id="RELEASE-18-PSQL"></a>

#### E.6.3.6. [psql](../../reference/reference-client/app-psql.md) [#](#RELEASE-18-PSQL)

* 允許 psql 剖析、繫結與關閉具名預備陳述式 (Anthonin Bonnefoy, Michael Paquier)
  [§](https://postgr.es/c/d55322b0d)
  [§](https://postgr.es/c/fc39b286a)

  這是透過新命令 [`\parse`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-PARSE)、
  [`\bind_named`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-BIND-NAMED)
  與 [`\close_prepared`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-CLOSE-PREPARED) 完成的。
* 新增可發出管線查詢的 psql 反斜線命令 (Anthonin Bonnefoy)
  [§](https://postgr.es/c/41625ab8e)
  [§](https://postgr.es/c/17caf6644)
  [§](https://postgr.es/c/2cce0fe44)

  新命令為 [`\startpipeline`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-PIPELINE)、
  `\syncpipeline`、`\sendpipeline`、
  `\endpipeline`、`\flushrequest`、
  `\flush` 與 `\getresults`。
* 允許在 psql 提示字元中加入管線狀態，並新增相關的狀態變數 (Anthonin Bonnefoy)
  [§](https://postgr.es/c/3ce357584)

  新的提示字元代碼為 `%P`，
  新的 psql 變數為 [`PIPELINE_SYNC_COUNT`](../../reference/reference-client/app-psql.md#APP-PSQL-VARIABLES-PIPELINE-SYNC-COUNT)、
  [`PIPELINE_COMMAND_COUNT`](../../reference/reference-client/app-psql.md#APP-PSQL-VARIABLES-PIPELINE-COMMAND-COUNT)
  與 [`PIPELINE_RESULT_COUNT`](../../reference/reference-client/app-psql.md#APP-PSQL-VARIABLES-PIPELINE-RESULT-COUNT)。
* 允許在 psql 提示字元中加入連線服務名稱，或透過 psql 變數存取該名稱 (Michael Banck)
  [§](https://postgr.es/c/477728b5d)
* 新增讓所有清單命令使用展開模式（expanded mode）的 psql 選項 (Dean Rasheed)
  [§](https://postgr.es/c/00f4c2959)

  加上反斜線命令後綴 `x` 即可啟用。
* 變更 psql 的 [`\conninfo`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-CONNINFO)，改用表格格式並包含更多資訊 (Álvaro Herrera, Maiquel Grassi,
  Hunaid Sohail)
  [§](https://postgr.es/c/bba2fbc62)
* 在 psql 的 [`\df+`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-DF-LC)、
  `\do+`、`\dAo+` 與
  `\dC+` 輸出中加入函式的 leakproof 標示 (Yugo Nagata)
  [§](https://postgr.es/c/2355e5111)
* 在 [`\dP+`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-DP-UC) 中加入分割關聯的存取方法詳細資訊
  (Justin Pryzby)
  [§](https://postgr.es/c/978f38c77)
* 在 psql [`\dx`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-DX-LC)
  的擴充功能輸出中加入 `default_version` (Magnus Hagander)
  [§](https://postgr.es/c/d696406a9)
* 新增 psql 變數 [`WATCH_INTERVAL`](../../reference/reference-client/app-psql.md#APP-PSQL-VARIABLES-WATCH-INTERVAL)，用於設定 [`\watch`](../../reference/reference-client/app-psql.md#APP-PSQL-META-COMMAND-WATCH)
  的預設等待時間 (Daniel Gustafsson)
  [§](https://postgr.es/c/1a759c832)

<a id="RELEASE-18-SERVER-APPS"></a>

#### E.6.3.7. 伺服器應用程式 [#](#RELEASE-18-SERVER-APPS)

* 將 [initdb](../../reference/reference-server/app-initdb.md) 改為預設啟用檢查碼
  (Greg Sabino Mullane)
  [§](https://postgr.es/c/983a588e0)
  [§](https://postgr.es/c/04bec894a)

  新的 initdb 選項
  `--no-data-checksums` 可停用檢查碼。
* 新增 initdb 選項
  `--no-sync-data-files`，避免同步堆積／索引檔案 (Nathan Bossart)
  [§](https://postgr.es/c/cf131fa94)

  initdb 選項 `--no-sync`
  仍可用來避免同步任何檔案。
* 新增 [vacuumdb](../../reference/reference-client/app-vacuumdb.md) 選項
  `--missing-stats-only`，只計算缺少的最佳化器統計資訊 (Corey Huinker, Nathan Bossart)
  [§](https://postgr.es/c/edba754f0)
  [§](https://postgr.es/c/987910502)

  此選項只能由超級使用者執行，而且只能搭配選項 `--analyze-only` 與
  `--analyze-in-stages` 使用。
* 新增 [pg_combinebackup](../../reference/reference-client/app-pgcombinebackup.md) 選項
  `-k`/`--link`，以啟用硬連結
  (Israel Barth Rubio, Robert Haas)
  [§](https://postgr.es/c/99aeb8470)

  只有部分檔案可以使用硬連結。若各個備份將被獨立使用，則不應使用此選項。
* 允許 [pg_verifybackup](../../reference/reference-client/app-pgverifybackup.md) 驗證 tar 格式的備份 (Amul Sul)
  [§](https://postgr.es/c/8dfd31290)
* 若 [pg_rewind](../../reference/reference-server/app-pgrewind.md) 的 `--source-server`
  指定了資料庫名稱，則在
  `--write-recovery-conf` 的輸出中使用該名稱 (Masahiko Sawada)
  [§](https://postgr.es/c/4ecdd4110)
* 新增 [pg_resetwal](../../reference/reference-server/app-pgresetwal.md) 選項
  `--char-signedness`，用於變更預設的
  `char` 有號性 (Masahiko Sawada)
  [§](https://postgr.es/c/30666d185)

<a id="RELEASE-18-PGDUMP"></a>
##### E.6.3.7.1. [pg_dump](../../reference/reference-client/app-pgdump.md)/[pg_dumpall](../../reference/reference-client/app-pg-dumpall.md)/[pg_restore](../../reference/reference-client/app-pgrestore.md) [#](#RELEASE-18-PGDUMP)

* 新增 [pg_dump](../../reference/reference-client/app-pgdump.md) 選項 `--statistics`
  (Jeff Davis)
  [§](https://postgr.es/c/bde2fb797)
  [§](https://postgr.es/c/a3e8dc143)
* 新增 pg_dump 與 [pg_dumpall](../../reference/reference-client/app-pg-dumpall.md) 選項 `--sequence-data`，
  用於傾印通常會被排除的序列資料 (Nathan Bossart)
  [§](https://postgr.es/c/9c49f0e8c)
  [§](https://postgr.es/c/acea3fc49)
* 新增 [pg_dump](../../reference/reference-client/app-pgdump.md)、[pg_dumpall](../../reference/reference-client/app-pg-dumpall.md)
  與 [pg_restore](../../reference/reference-client/app-pgrestore.md) 選項
  `--statistics-only`、`--no-statistics`、
  `--no-data` 與 `--no-schema`
  (Corey Huinker, Jeff Davis)
  [§](https://postgr.es/c/1fd1bd871)
* 在 [pg_dump](../../reference/reference-client/app-pgdump.md)、
  [pg_dumpall](../../reference/reference-client/app-pg-dumpall.md)、[pg_restore](../../reference/reference-client/app-pgrestore.md) 中新增選項 `--no-policies`，用於停用資料列層級安全原則的處理
  (Nikolay Samokhvalov)
  [§](https://postgr.es/c/cd3c45125)

  這對遷移到原則不同的系統很有用。

<a id="RELEASE-18-PGUPGRADE"></a>

##### E.6.3.7.2. [pg_upgrade](../../reference/reference-server/pgupgrade.md) [#](#RELEASE-18-PGUPGRADE)

* 允許 pg_upgrade 保留最佳化器統計資訊 (Corey Huinker, Jeff Davis, Nathan Bossart)
  [§](https://postgr.es/c/1fd1bd871)
  [§](https://postgr.es/c/c9d502eb6)
  [§](https://postgr.es/c/d5f1b6a75)
  [§](https://postgr.es/c/1fd1bd871)

  擴充統計資訊不會被保留。另外也新增 pg_upgrade 選項
  `--no-statistics`，用於停用統計資訊的保留。
* 允許 pg_upgrade 平行處理資料庫檢查 (Nathan Bossart)
  [§](https://postgr.es/c/40e2e5e92)
  [§](https://postgr.es/c/6d3d2e8e5)
  [§](https://postgr.es/c/7baa36de5)
  [§](https://postgr.es/c/46cad8b31)
  [§](https://postgr.es/c/6ab8f27bc)
  [§](https://postgr.es/c/bbf83cab9)
  [§](https://postgr.es/c/9db3018cf)
  [§](https://postgr.es/c/c34eabfbb)
  [§](https://postgr.es/c/cf2f82a37)
  [§](https://postgr.es/c/f93f5f7b9)
  [§](https://postgr.es/c/c880cf258)

  這由既有的 `--jobs` 選項控制。
* 新增 pg_upgrade 選項
  `--swap`，以交換目錄的方式取代複製、clone 或連結檔案 (Nathan Bossart)
  [§](https://postgr.es/c/626d7236b)

  此模式可能是最快的。
* 新增 pg_upgrade 選項
  `--set-char-signedness`，用於設定新叢集預設的
  `char` 有號性 (Masahiko Sawada)
  [§](https://postgr.es/c/a8238f87f)
  [§](https://postgr.es/c/1aab68059)

  這是為了處理 PostgreSQL 18 之前版本的叢集預設 CPU 有號性與新叢集不一致的情況。

<a id="RELEASE-18-LOGICALREP-APP"></a>

##### E.6.3.7.3. 邏輯複寫應用程式 [#](#RELEASE-18-LOGICALREP-APP)

* 新增 [pg_createsubscriber](../../reference/reference-server/app-pgcreatesubscriber.md) 選項
  `--all`，為所有資料庫建立邏輯複本
  (Shubham Khanna)
  [§](https://postgr.es/c/fb2ea12f4)
* 新增 pg_createsubscriber 選項
  `--clean`，用於移除發佈 (Shubham Khanna)
  [§](https://postgr.es/c/e5aeed4b8)
  [§](https://postgr.es/c/60dda7bbc)
* 新增 pg_createsubscriber 選項
  `--enable-two-phase`，用於啟用預備交易
  (Shubham Khanna)
  [§](https://postgr.es/c/e117cfb2f)
* 新增 [pg_recvlogical](../../reference/reference-client/app-pgrecvlogical.md) 選項
  `--enable-failover`，用於指定容錯移轉插槽 (Hayato Kuroda)
  [§](https://postgr.es/c/cf2655a90)

  另外也新增選項 `--enable-two-phase` 作為
  `--two-phase` 的同義選項，並棄用後者。
* 允許 pg_recvlogical 的
  `--drop-slot` 在不指定
  `--dbname` 的情況下運作 (Hayato Kuroda)
  [§](https://postgr.es/c/c68100aa4)

<a id="RELEASE-18-SOURCE-CODE"></a>

#### E.6.3.8. 原始碼 [#](#RELEASE-18-SOURCE-CODE)

* 將[注入點](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS)的載入與執行分開
  (Michael Paquier, Heikki Linnakangas)
  [§](https://postgr.es/c/4b211003e)
  [§](https://postgr.es/c/a0a5869a8)

  現在可以透過 [`INJECTION_POINT_LOAD()`](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS) 建立注入點但不執行，
  並可以透過 [`INJECTION_POINT_CACHED()`](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS) 執行這類注入點。
* 支援注入點的執行期引數 (Michael Paquier)
  [§](https://postgr.es/c/371f2db8b)
* 允許使用 [`IS_INJECTION_POINT_ATTACHED()`](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS) 撰寫內嵌的注入點測試程式碼
  (Heikki Linnakangas)
  [§](https://postgr.es/c/20e0e7da9)
* 使用 SIMD（單一指令多重資料）提升處理長 [`JSON`](../../the-sql-language/datatype/datatype-json.md) 字串的效能 (David
  Rowley)
  [§](https://postgr.es/c/ca6fde922)
* 使用 x86 AVX-512 指令加快 CRC32C 計算 (Raghuveer Devulapalli, Paul Amonson)
  [§](https://postgr.es/c/3c6e8c123)
* 新增用於 popcount（整數位元計數）的 ARM Neon 與 SVE CPU 內建函式（intrinsics） (Chiranmoy
  Bhattacharya, Devanga Susmitha, Rama Malladi)
  [§](https://postgr.es/c/6be53c276)
  [§](https://postgr.es/c/519338ace)
* 提高 numeric 乘法與除法的速度 (Joel
  Jacobson, Dean Rasheed)
  [§](https://postgr.es/c/ca481d3c9)
  [§](https://postgr.es/c/c4e44224c)
  [§](https://postgr.es/c/8dc28d7eb)
  [§](https://postgr.es/c/9428c001f)
* 新增 configure 選項 [`--with-libnuma`](../../server-administration/installation/install-make.md#CONFIGURE-OPTION-WITH-LIBNUMA)，
  以啟用 NUMA 感知 (Jakub Wartak, Bertrand
  Drouvot)
  [§](https://postgr.es/c/65c298f61)
  [§](https://postgr.es/c/8cc139bec)
  [§](https://postgr.es/c/ba2a3c230)

  函式 [`pg_numa_available()`](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-SESSION-TABLE)
  會回報 NUMA 感知的狀態，系統檢視表 [`pg_shmem_allocations_numa`](../../internals/views/view-pg-shmem-allocations-numa.md)
  與 [`pg_buffercache_numa`](../contrib/pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA)
  則會回報共享記憶體在各 NUMA 節點間的分布。
* 為 [`pg_index`](../../internals/catalogs/catalog-pg-index.md) 新增 [TOAST](../../internals/storage/storage-toast.md) 資料表，
  以支援非常大的運算式索引 (Nathan Bossart)
  [§](https://postgr.es/c/b52c4fc3c)
* 移除欄位 [`pg_attribute`](../../internals/catalogs/catalog-pg-attribute.md).`attcacheoff`
  (David Rowley)
  [§](https://postgr.es/c/02a8d0c45)
* 新增欄位 [`pg_class`](../../internals/catalogs/catalog-pg-class.md).`relallfrozen`
  (Melanie Plageman)
  [§](https://postgr.es/c/99f8f3fbb)
* 在索引存取方法 API 中新增 [`amgettreeheight`](../../internals/indexam/README.md)、
  `amconsistentequality` 與
  `amconsistentordering` (Mark Dilger)
  [§](https://postgr.es/c/56fead44d)
  [§](https://postgr.es/c/af4002b38)
* 新增 GiST 支援函式 [`stratnum()`](../../internals/indextypes/gist.md#GIST-EXTENSIBILITY)
  (Paul A. Jungwirth)
  [§](https://postgr.es/c/7406ab623)
* 在 [pg_controldata](../../reference/reference-server/app-pgcontroldata.md) 中記錄
  `char` 的預設 CPU 有號性
  (Masahiko Sawada)
  [§](https://postgr.es/c/44fe30fda)
* 在 [PL/Python](../../server-programming/plpython/README.md) 中新增對 Python「Limited API」的支援 (Peter Eisentraut)
  [§](https://postgr.es/c/72a3d0462)
  [§](https://postgr.es/c/0793ab810)

  這有助於避免 Python 3.x 版本不一致所造成的問題。
* 將支援的最低 Python 版本改為 3.6.8 (Jacob Champion)
  [§](https://postgr.es/c/45363fca6)
* 移除對 1.1.1 之前 OpenSSL 版本的支援 (Daniel Gustafsson)
  [§](https://postgr.es/c/a70e01d43)
  [§](https://postgr.es/c/6c66b7443)
* 若啟用 LLVM，則要求 14 以上的版本 (Thomas Munro)
  [§](https://postgr.es/c/972c2cd28)
* 新增巨集 [`PG_MODULE_MAGIC_EXT`](../../the-sql-language/functions/functions-info.md)，
  讓擴充功能可以回報其名稱與版本 (Andrei Lepikhov)
  [§](https://postgr.es/c/9324c8c58)

  可以透過新函式 [`pg_get_loaded_modules()`](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-SESSION-TABLE) 存取此資訊。
* 在文件中說明 [`SPI_connect()`](../../server-programming/spi/spi-spi-connect.md)/[`SPI_connect_ext()`](../../server-programming/spi/spi-spi-connect.md)
  一律傳回成功（`SPI_OK_CONNECT`） (Stepan
  Neretin)
  [§](https://postgr.es/c/218527d01)

  錯誤一律透過 `ereport()` 回報。
* 新增關於 API 與 ABI 相容性的[文件章節](../../server-programming/extend/xfunc-c.md#XFUNC-API-ABI-STABILITY-GUIDANCE) (David Wheeler, Peter Eisentraut)
  [§](https://postgr.es/c/e54a42ac9)
* 移除 Windows 上 Meson 建置的實驗性標示 (Aleksander Alekseev)
  [§](https://postgr.es/c/5afaba629)
* 移除 configure 選項 `--disable-spinlocks` 與
  `--disable-atomics` (Thomas Munro)
  [§](https://postgr.es/c/e25626677)
  [§](https://postgr.es/c/813852613)

  現在必須支援 32 位元原子操作。
* 移除對 HPPA/PA-RISC 架構的支援
  (Tom Lane)
  [§](https://postgr.es/c/edadeb071)

<a id="RELEASE-18-MODULES"></a>
#### E.6.3.9. 附加模組 [#](#RELEASE-18-MODULES)

* 新增擴充功能 [pg_logicalinspect](../contrib/pglogicalinspect.md)，用於檢視邏輯快照 (Bertrand Drouvot)
  [§](https://postgr.es/c/7cdfeee32)
* 新增擴充功能 [pg_overexplain](../contrib/pgoverexplain.md)，在
  [`EXPLAIN`](../../reference/sql-commands/sql-explain.md)
  輸出中加入除錯細節 (Robert Haas)
  [§](https://postgr.es/c/8d5ceb113)
* 為 [`postgres_fdw_get_connections()`](../contrib/postgres-fdw.md#POSTGRES-FDW-FUNCTIONS) 新增輸出欄位
  (Hayato Kuroda, Sagar Dilip Shedge)
  [§](https://postgr.es/c/c297a47c5)
  [§](https://postgr.es/c/857df3cef)
  [§](https://postgr.es/c/4f08ab554)
  [§](https://postgr.es/c/fe186bda7)

  新輸出欄位 `used_in_xact` 表示該外部資料包裝器是否正被目前交易使用，
  `closed` 表示其是否已關閉，
  `user_name` 表示使用者名稱，
  `remote_backend_pid` 則表示遠端後端程序的識別碼。
* 允許將來自用戶端的 [SCRAM](../../server-administration/client-authentication/auth-password.md)
  認證傳遞給 [postgres_fdw](../contrib/postgres-fdw.md) 伺服器 (Matheus Alcantara, Peter Eisentraut)
  [§](https://postgr.es/c/761c79508)

  這可以避免在資料庫中儲存 postgres_fdw
  的認證資訊，並由 postgres_fdw 連線選項 [`use_scram_passthrough`](../contrib/postgres-fdw.md#POSTGRES-FDW-OPTION-USE-SCRAM-PASSTHROUGH)
  啟用。libpq 使用新的連線參數
  [scram_client_key](../../client-interfaces/libpq/libpq-paramkeywords.md#libpq-connect-scram-client-key) 與 [scram_server_key](../../client-interfaces/libpq/libpq-paramkeywords.md#libpq-connect-scram-server-key)。
* 允許將來自用戶端的 SCRAM 認證傳遞給 [dblink](../contrib/dblink.md) 伺服器 (Matheus Alcantara)
  [§](https://postgr.es/c/3642df265)
* 為 [file_fdw](../contrib/file-fdw.md) 新增 `on_error` 與 `log_verbosity`
  選項 (Atsushi Torikoshi)
  [§](https://postgr.es/c/a1c4c8a9e)

  這些選項控制 file_fdw 如何處理及回報檔案中的無效資料列。
* 新增 `reject_limit`，用於控制 file_fdw 可以忽略的無效資料列數量 (Atsushi
  Torikoshi)
  [§](https://postgr.es/c/6c8f67032)

  此選項在 `ON_ERROR = 'ignore'` 時有效。
* 為 [passwordcheck](../contrib/passwordcheck.md) 新增可設定的變數 `min_password_length` (Emanuele Musella, Maurizio Boriani)
  [§](https://postgr.es/c/f7e1b3828)

  此變數控制密碼的最小長度。
* 讓 [pgbench](../../reference/reference-client/pgbench.md) 在個別腳本的報告中回報失敗、重試或略過的交易數量 (Yugo Nagata)
  [§](https://postgr.es/c/cae0f3c40)
* 新增 [isn](../contrib/isn.md) 伺服器變數 `weak`，
  用於控制是否接受無效的檢查位數（check digit） (Viktor Holmberg)
  [§](https://postgr.es/c/448904423)

  先前只能透過函式 [`isn_weak()`](../contrib/isn.md#ISN-FUNCTIONS) 控制。
* 允許先將值排序，以加快 [btree_gist](../contrib/btree-gist.md)
  索引的建立 (Bernd Helmle, Andrey Borodin)
  [§](https://postgr.es/c/e4309f73f)
* 新增 [amcheck](../contrib/amcheck.md) 檢查函式 [`gin_index_check()`](../contrib/amcheck.md#AMCHECK-FUNCTIONS)，
  用於驗證 `GIN` 索引 (Grigory Kryachko, Heikki
  Linnakangas, Andrey Borodin)
  [§](https://postgr.es/c/14ffaece0)
* 新增函式 [`pg_buffercache_evict_relation()`](../contrib/pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION)
  與 [`pg_buffercache_evict_all()`](../contrib/pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL)，
  用於逐出未被釘住（unpinned）的共享緩衝區 (Nazir Bilal Yavuz)
  [§](https://postgr.es/c/dcf7e1697)

  既有函式 [`pg_buffercache_evict()`](../contrib/pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT)
  現在會傳回緩衝區的刷寫狀態。
* 允許擴充功能安裝自訂的 [EXPLAIN](../../reference/sql-commands/sql-explain.md)
  選項 (Robert Haas, Sami Imseih)
  [§](https://postgr.es/c/c65bc2e1d)
  [§](https://postgr.es/c/4fd02bf7c)
  [§](https://postgr.es/c/50ba65e73)
* 允許擴充功能使用伺服器的累計統計資訊 API (Michael Paquier)
  [§](https://postgr.es/c/7949d9594)
  [§](https://postgr.es/c/2eff9e678)

<a id="RELEASE-18-PGSTATSTATEMENTS"></a>

##### E.6.3.9.1. [pg_stat_statements](../contrib/pgstatstatements.md) [#](#RELEASE-18-PGSTATSTATEMENTS)

* 允許 pg_stat_statements 追蹤 [CREATE TABLE AS](../../reference/sql-commands/sql-createtableas.md)
  與 [DECLARE](../../reference/sql-commands/sql-declare.md) 的查詢 (Anthonin Bonnefoy)
  [§](https://postgr.es/c/6b652e6ce)

  現在也會為這些查詢指派查詢識別碼。
* 允許在 pg_stat_statements 中將 [SET](../../reference/sql-commands/sql-set.md) 的值參數化 (Greg Sabino Mullane,
  Michael Paquier)
  [§](https://postgr.es/c/dc6851596)

  這可以減少常數不同的 `SET` 陳述式所造成的膨脹。
* 新增 [`pg_stat_statements`](../contrib/pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)
  欄位，用於回報平行活動 (Guillaume Lelarge)
  [§](https://postgr.es/c/cf54a2c00)

  新欄位為
  `parallel_workers_to_launch` 與
  `parallel_workers_launched`。
* 新增
  `pg_stat_statements`.`wal_buffers_full`，
  用於回報 WAL 緩衝區已滿的次數 (Bertrand Drouvot)
  [§](https://postgr.es/c/ce5bcc4a9)

<a id="RELEASE-18-PGCRYPTO"></a>

##### E.6.3.9.2. [pgcrypto](../contrib/pgcrypto.md) [#](#RELEASE-18-PGCRYPTO)

* 新增 pgcrypto 演算法 [`sha256crypt`](../contrib/pgcrypto.md#PGCRYPTO-CRYPT-ALGORITHMS)
  與 [`sha512crypt`](../contrib/pgcrypto.md#PGCRYPTO-CRYPT-ALGORITHMS)
  (Bernd Helmle)
  [§](https://postgr.es/c/749a9e20c)
* 在 pgcrypto 的加密與解密中新增 [CFB](../contrib/pgcrypto.md#PGCRYPTO-RAW-ENC-FUNCS) 模式
  (Umar Hayat)
  [§](https://postgr.es/c/9ad1b3d01)
* 新增函式 [`fips_mode()`](../contrib/pgcrypto.md#PGCRYPTO-OPENSSL-SUPPORT-FUNCS)，
  用於回報伺服器的 FIPS 模式 (Daniel
  Gustafsson)
  [§](https://postgr.es/c/924d89a35)
* 新增 pgcrypto 伺服器變數 [`builtin_crypto_enabled`](../contrib/pgcrypto.md#PGCRYPTO-CONFIGURATION-PARAMETERS-BUILTIN_CRYPTO_ENABLED)，
  允許停用內建的非 FIPS 模式加密函式 (Daniel Gustafsson, Joe Conway)
  [§](https://postgr.es/c/035f99cbe)

  這對確保 FIPS 模式的行為很有用。

<a id="RELEASE-18-ACKNOWLEDGEMENTS"></a>

### E.6.4. 致謝 [#](#RELEASE-18-ACKNOWLEDGEMENTS)

下列人士（依字母順序排列）以修補程式作者、提交者、審閱者、測試者或問題回報者的身分，對此版本做出貢獻。

<table border="0" class="simplelist" summary="Simple list"><tr><td>Abhishek Chanda</td></tr><tr><td>Adam Guo</td></tr><tr><td>Adam Rauch</td></tr><tr><td>Aidar Imamov</td></tr><tr><td>Ajin Cherian</td></tr><tr><td>Alastair Turner</td></tr><tr><td>Alec Cozens</td></tr><tr><td>Aleksander Alekseev</td></tr><tr><td>Alena Rybakina</td></tr><tr><td>Alex Friedman</td></tr><tr><td>Alex Richman</td></tr><tr><td>Alexander Alehin</td></tr><tr><td>Alexander Borisov</td></tr><tr><td>Alexander Korotkov</td></tr><tr><td>Alexander Kozhemyakin</td></tr><tr><td>Alexander Kukushkin</td></tr><tr><td>Alexander Kuzmenkov</td></tr><tr><td>Alexander Kuznetsov</td></tr><tr><td>Alexander Lakhin</td></tr><tr><td>Alexander Pyhalov</td></tr><tr><td>Alexandra Wang</td></tr><tr><td>Alexey Dvoichenkov</td></tr><tr><td>Alexey Makhmutov</td></tr><tr><td>Alexey Shishkin</td></tr><tr><td>Ali Akbar</td></tr><tr><td>Álvaro Herrera</td></tr><tr><td>Álvaro Mongil</td></tr><tr><td>Amit Kapila</td></tr><tr><td>Amit Langote</td></tr><tr><td>Amul Sul</td></tr><tr><td>Andreas Karlsson</td></tr><tr><td>Andreas Scherbaum</td></tr><tr><td>Andreas Ulbrich</td></tr><tr><td>Andrei Lepikhov</td></tr><tr><td>Andres Freund</td></tr><tr><td>Andrew</td></tr><tr><td>Andrew Bille</td></tr><tr><td>Andrew Dunstan</td></tr><tr><td>Andrew Jackson</td></tr><tr><td>Andrew Kane</td></tr><tr><td>Andrew Watkins</td></tr><tr><td>Andrey Borodin</td></tr><tr><td>Andrey Chudnovsky</td></tr><tr><td>Andrey Rachitskiy</td></tr><tr><td>Andrey Rudometov</td></tr><tr><td>Andy Alsup</td></tr><tr><td>Andy Fan</td></tr><tr><td>Anthonin Bonnefoy</td></tr><tr><td>Anthony Hsu</td></tr><tr><td>Anthony Leung</td></tr><tr><td>Anton Melnikov</td></tr><tr><td>Anton Voloshin</td></tr><tr><td>Antonin Houska</td></tr><tr><td>Antti Lampinen</td></tr><tr><td>Arseniy Mukhin</td></tr><tr><td>Artur Zakirov</td></tr><tr><td>Arun Thirupathi</td></tr><tr><td>Ashutosh Bapat</td></tr><tr><td>Asphator</td></tr><tr><td>Atsushi Torikoshi</td></tr><tr><td>Avi Weinberg</td></tr><tr><td>Aya Iwata</td></tr><tr><td>Ayush Tiwari</td></tr><tr><td>Ayush Vatsa</td></tr><tr><td>Bastien Roucariès</td></tr><tr><td>Ben Peachey Higdon</td></tr><tr><td>Benoit Lobréau</td></tr><tr><td>Bernd Helmle</td></tr><tr><td>Bernd Reiß</td></tr><tr><td>Bernhard Wiedemann</td></tr><tr><td>Bertrand Drouvot</td></tr><tr><td>Bertrand Mamasam</td></tr><tr><td>Bharath Rupireddy</td></tr><tr><td>Bogdan Grigorenko</td></tr><tr><td>Boyu Yang</td></tr><tr><td>Braulio Fdo Gonzalez</td></tr><tr><td>Bruce Momjian</td></tr><tr><td>Bykov Ivan</td></tr><tr><td>Cameron Vogt</td></tr><tr><td>Cary Huang</td></tr><tr><td>Cédric Villemain</td></tr><tr><td>Cees van Zeeland</td></tr><tr><td>ChangAo Chen</td></tr><tr><td>Chao Li</td></tr><tr><td>Chapman Flack</td></tr><tr><td>Charles Samborski</td></tr><tr><td>Chengwen Wu</td></tr><tr><td>Chengxi Sun</td></tr><tr><td>Chiranmoy Bhattacharya</td></tr><tr><td>Chris Gooch</td></tr><tr><td>Christian Charukiewicz</td></tr><tr><td>Christoph Berg</td></tr><tr><td>Christophe Courtois</td></tr><tr><td>Christopher Inokuchi</td></tr><tr><td>Clemens Ruck</td></tr><tr><td>Corey Huinker</td></tr><tr><td>Craig Milhiser</td></tr><tr><td>Crisp Lee</td></tr><tr><td>Dagfinn Ilmari Mannsåker</td></tr><tr><td>Daniel Elishakov</td></tr><tr><td>Daniel Gustafsson</td></tr><tr><td>Daniel Vérité</td></tr><tr><td>Daniel Westermann</td></tr><tr><td>Daniele Varrazzo</td></tr><tr><td>Daniil Davydov</td></tr><tr><td>Daria Shanina</td></tr><tr><td>Dave Cramer</td></tr><tr><td>Dave Page</td></tr><tr><td>David Benjamin</td></tr><tr><td>David Christensen</td></tr><tr><td>David Fiedler</td></tr><tr><td>David G. Johnston</td></tr><tr><td>David Geier</td></tr><tr><td>David Rowley</td></tr><tr><td>David Steele</td></tr><tr><td>David Wheeler</td></tr><tr><td>David Zhang</td></tr><tr><td>Davinder Singh</td></tr><tr><td>Dean Rasheed</td></tr><tr><td>Devanga Susmitha</td></tr><tr><td>Devrim Gündüz</td></tr><tr><td>Dian Fay</td></tr><tr><td>Dilip Kumar</td></tr><tr><td>Dimitrios Apostolou</td></tr><tr><td>Dipesh Dhameliya</td></tr><tr><td>Dmitrii Bondar</td></tr><tr><td>Dmitry Dolgov</td></tr><tr><td>Dmitry Koval</td></tr><tr><td>Dmitry Kovalenko</td></tr><tr><td>Dmitry Yurichev</td></tr><tr><td>Dominique Devienne</td></tr><tr><td>Donghang Lin</td></tr><tr><td>Dorjpalam Batbaatar</td></tr><tr><td>Drew Callahan</td></tr><tr><td>Duncan Sands</td></tr><tr><td>Dwayne Towell</td></tr><tr><td>Dzmitry Jachnik</td></tr><tr><td>Egor Chindyaskin</td></tr><tr><td>Egor Rogov</td></tr><tr><td>Emanuel Ionescu</td></tr><tr><td>Emanuele Musella</td></tr><tr><td>Emre Hasegeli</td></tr><tr><td>Eric Cyr</td></tr><tr><td>Erica Zhang</td></tr><tr><td>Erik Nordström</td></tr><tr><td>Erik Rijkers</td></tr><tr><td>Erik Wienhold</td></tr><tr><td>Erki Eessaar</td></tr><tr><td>Ethan Mertz</td></tr><tr><td>Etienne LAFARGE</td></tr><tr><td>Etsuro Fujita</td></tr><tr><td>Euler Taveira</td></tr><tr><td>Evan Si</td></tr><tr><td>Evgeniy Gorbanev</td></tr><tr><td>Fabio R. Sluzala</td></tr><tr><td>Fabrízio de Royes Mello</td></tr><tr><td>Feike Steenbergen</td></tr><tr><td>Feliphe Pozzer</td></tr><tr><td>Felix</td></tr><tr><td>Fire Emerald</td></tr><tr><td>Florents Tselai</td></tr><tr><td>Francesco Degrassi</td></tr><tr><td>Frank Streitzig</td></tr><tr><td>Frédéric Yhuel</td></tr><tr><td>Fredrik Widlert</td></tr><tr><td>Gabriele Bartolini</td></tr><tr><td>Gavin Panella</td></tr><tr><td>Geoff Winkless</td></tr><tr><td>George MacKerron</td></tr><tr><td>Gilles Darold</td></tr><tr><td>Grant Gryczan</td></tr><tr><td>Greg Burd</td></tr><tr><td>Greg Sabino Mullane</td></tr><tr><td>Greg Stark</td></tr><tr><td>Grigory Kryachko</td></tr><tr><td>Guillaume Lelarge</td></tr><tr><td>Gunnar Morling</td></tr><tr><td>Gunnar Wagner</td></tr><tr><td>Gurjeet Singh</td></tr><tr><td>Haifang Wang</td></tr><tr><td>Hajime Matsunaga</td></tr><tr><td>Hamid Akhtar</td></tr><tr><td>Hannu Krosing</td></tr><tr><td>Hari Krishna Sunder</td></tr><tr><td>Haruka Takatsuka</td></tr><tr><td>Hayato Kuroda</td></tr><tr><td>Heikki Linnakangas</td></tr><tr><td>Hironobu Suzuki</td></tr><tr><td>Holger Jakobs</td></tr><tr><td>Hubert Lubaczewski</td></tr><tr><td>Hugo Dubois</td></tr><tr><td>Hugo Zhang</td></tr><tr><td>Hunaid Sohail</td></tr><tr><td>Hywel Carver</td></tr><tr><td>Ian Barwick</td></tr><tr><td>Ibrar Ahmed</td></tr><tr><td>Igor Gnatyuk</td></tr><tr><td>Igor Korot</td></tr><tr><td>Ilia Evdokimov</td></tr><tr><td>Ilya Gladyshev</td></tr><tr><td>Ilyasov Ian</td></tr><tr><td>Imran Zaheer</td></tr><tr><td>Isaac Morland</td></tr><tr><td>Israel Barth Rubio</td></tr><tr><td>Ivan Kush</td></tr><tr><td>Jacob Brazeal</td></tr><tr><td>Jacob Champion</td></tr><tr><td>Jaime Casanova</td></tr><tr><td>Jakob Egger</td></tr><tr><td>Jakub Wartak</td></tr><tr><td>James Coleman</td></tr><tr><td>James Hunter</td></tr><tr><td>Jan Behrens</td></tr><tr><td>Japin Li</td></tr><tr><td>Jason Smith</td></tr><tr><td>Jayesh Dehankar</td></tr><tr><td>Jeevan Chalke</td></tr><tr><td>Jeff Davis</td></tr><tr><td>Jehan-Guillaume de Rorthais</td></tr><tr><td>Jelte Fennema-Nio</td></tr><tr><td>Jian He</td></tr><tr><td>Jianghua Yang</td></tr><tr><td>Jiao Shuntian</td></tr><tr><td>Jim Jones</td></tr><tr><td>Jim Nasby</td></tr><tr><td>Jingtang Zhang</td></tr><tr><td>Jingzhou Fu</td></tr><tr><td>Joe Conway</td></tr><tr><td>Joel Jacobson</td></tr><tr><td>John Hutchins</td></tr><tr><td>John Naylor</td></tr><tr><td>Jonathan Katz</td></tr><tr><td>Jorge Solórzano</td></tr><tr><td>José Villanova</td></tr><tr><td>Josef Šimánek</td></tr><tr><td>Joseph Koshakow</td></tr><tr><td>Julien Rouhaud</td></tr><tr><td>Junwang Zhao</td></tr><tr><td>Justin Pryzby</td></tr><tr><td>Kaido Vaikla</td></tr><tr><td>Kaimeh</td></tr><tr><td>Karina Litskevich</td></tr><tr><td>Karthik S</td></tr><tr><td>Kartyshov Ivan</td></tr><tr><td>Kashif Zeeshan</td></tr><tr><td>Keisuke Kuroda</td></tr><tr><td>Kevin Hale Boyes</td></tr><tr><td>Kevin K Biju</td></tr><tr><td>Kirill Reshke</td></tr><tr><td>Kirill Zdornyy</td></tr><tr><td>Koen De Groote</td></tr><tr><td>Koichi Suzuki</td></tr><tr><td>Koki Nakamura</td></tr><tr><td>Konstantin Knizhnik</td></tr><tr><td>Kouhei Sutou</td></tr><tr><td>Kuntal Ghosh</td></tr><tr><td>Kyotaro Horiguchi</td></tr><tr><td>Lakshmi Narayana Velayudam</td></tr><tr><td>Lars Kanis</td></tr><tr><td>Laurence Parry</td></tr><tr><td>Laurenz Albe</td></tr><tr><td>Lele Gaifax</td></tr><tr><td>Li Yong</td></tr><tr><td>Lilian Ontowhee</td></tr><tr><td>Lingbin Meng</td></tr><tr><td>Luboslav Špilák</td></tr><tr><td>Luca Vallisa</td></tr><tr><td>Lukas Fittl</td></tr><tr><td>Maciek Sakrejda</td></tr><tr><td>Magnus Hagander</td></tr><tr><td>Mahendra Singh Thalor</td></tr><tr><td>Mahendrakar Srinivasarao</td></tr><tr><td>Maiquel Grassi</td></tr><tr><td>Maksim Korotkov</td></tr><tr><td>Maksim Melnikov</td></tr><tr><td>Man Zeng</td></tr><tr><td>Marat Buharov</td></tr><tr><td>Marc Balmer</td></tr><tr><td>Marco Nenciarini</td></tr><tr><td>Marcos Pegoraro</td></tr><tr><td>Marina Polyakova</td></tr><tr><td>Mark Callaghan</td></tr><tr><td>Mark Dilger</td></tr><tr><td>Marlene Brandstaetter</td></tr><tr><td>Marlene Reiterer</td></tr><tr><td>Martin Rakhmanov</td></tr><tr><td>Masahiko Sawada</td></tr><tr><td>Masahiro Ikeda</td></tr><tr><td>Masao Fujii</td></tr><tr><td>Mason Mackaman</td></tr><tr><td>Mat Arye</td></tr><tr><td>Matheus Alcantara</td></tr><tr><td>Mats Kindahl</td></tr><tr><td>Matthew Gabeler-Lee</td></tr><tr><td>Matthew Kim</td></tr><tr><td>Matthew Sterrett</td></tr><tr><td>Matthew Woodcraft</td></tr><tr><td>Matthias van de Meent</td></tr><tr><td>Matthieu Denais</td></tr><tr><td>Maurizio Boriani</td></tr><tr><td>Max Johnson</td></tr><tr><td>Max Madden</td></tr><tr><td>Maxim Boguk</td></tr><tr><td>Maxim Orlov</td></tr><tr><td>Maximilian Chrzan</td></tr><tr><td>Melanie Plageman</td></tr><tr><td>Melih Mutlu</td></tr><tr><td>Mert Alev</td></tr><tr><td>Michael Banck</td></tr><tr><td>Michael Bondarenko</td></tr><tr><td>Michael Christofides</td></tr><tr><td>Michael Guissine</td></tr><tr><td>Michael Harris</td></tr><tr><td>Michaël Paquier</td></tr><tr><td>Michail Nikolaev</td></tr><tr><td>Michal Kleczek</td></tr><tr><td>Michel Pelletier</td></tr><tr><td>Mikaël Gourlaouen</td></tr><tr><td>Mikhail Gribkov</td></tr><tr><td>Mikhail Kot</td></tr><tr><td>Milosz Chmura</td></tr><tr><td>Muralikrishna Bandaru</td></tr><tr><td>Murat Efendioglu</td></tr><tr><td>Mutaamba Maasha</td></tr><tr><td>Naeem Akhter</td></tr><tr><td>Nat Makarevitch</td></tr><tr><td>Nathan Bossart</td></tr><tr><td>Navneet Kumar</td></tr><tr><td>Nazir Bilal Yavuz</td></tr><tr><td>Neil Conway</td></tr><tr><td>Niccolò Fei</td></tr><tr><td>Nick Davies</td></tr><tr><td>Nicolas Maus</td></tr><tr><td>Niek Brasa</td></tr><tr><td>Nikhil Raj</td></tr><tr><td>Nikita</td></tr><tr><td>Nikita Kalinin</td></tr><tr><td>Nikita Malakhov</td></tr><tr><td>Nikolay Samokhvalov</td></tr><tr><td>Nikolay Shaplov</td></tr><tr><td>Nisha Moond</td></tr><tr><td>Nitin Jadhav</td></tr><tr><td>Nitin Motiani</td></tr><tr><td>Noah Misch</td></tr><tr><td>Noboru Saito</td></tr><tr><td>Noriyoshi Shinoda</td></tr><tr><td>Ole Peder Brandtzæg</td></tr><tr><td>Oleg Sibiryakov</td></tr><tr><td>Oleg Tselebrovskiy</td></tr><tr><td>Olleg Samoylov</td></tr><tr><td>Onder Kalaci</td></tr><tr><td>Ondrej Navratil</td></tr><tr><td>Patrick Stählin</td></tr><tr><td>Paul Amonson</td></tr><tr><td>Paul Jungwirth</td></tr><tr><td>Paul Ramsey</td></tr><tr><td>Pavel Borisov</td></tr><tr><td>Pavel Luzanov</td></tr><tr><td>Pavel Nekrasov</td></tr><tr><td>Pavel Stehule</td></tr><tr><td>Peter Eisentraut</td></tr><tr><td>Peter Geoghegan</td></tr><tr><td>Peter Mittere</td></tr><tr><td>Peter Smith</td></tr><tr><td>Phil Eaton</td></tr><tr><td>Philipp Salvisberg</td></tr><tr><td>Philippe Beaudoin</td></tr><tr><td>Pierre Giraud</td></tr><tr><td>Pixian Shi</td></tr><tr><td>Polina Bungina</td></tr><tr><td>Przemyslaw Sztoch</td></tr><tr><td>Quynh Tran</td></tr><tr><td>Rafia Sabih</td></tr><tr><td>Raghuveer Devulapalli</td></tr><tr><td>Rahila Syed</td></tr><tr><td>Rama Malladi</td></tr><tr><td>Ran Benita</td></tr><tr><td>Ranier Vilela</td></tr><tr><td>Renan Alves Fonseca</td></tr><tr><td>Richard Guo</td></tr><tr><td>Richard Neill</td></tr><tr><td>Rintaro Ikeda</td></tr><tr><td>Robert Haas</td></tr><tr><td>Robert Treat</td></tr><tr><td>Robins Tharakan</td></tr><tr><td>Roman Zharkov</td></tr><tr><td>Ronald Cruz</td></tr><tr><td>Ronan Dunklau</td></tr><tr><td>Rui Zhao</td></tr><tr><td>Rushabh Lathia</td></tr><tr><td>Rustam Allakov</td></tr><tr><td>Ryo Kanbayashi</td></tr><tr><td>Ryohei Takahashi</td></tr><tr><td>RyotaK</td></tr><tr><td>Sagar Dilip Shedge</td></tr><tr><td>Salvatore Dipietro</td></tr><tr><td>Sam Gabrielsson</td></tr><tr><td>Sam James</td></tr><tr><td>Sameer Kumar</td></tr><tr><td>Sami Imseih</td></tr><tr><td>Samuel Thibault</td></tr><tr><td>Satyanarayana Narlapuram</td></tr><tr><td>Sebastian Skalacki</td></tr><tr><td>Senglee Choi</td></tr><tr><td>Sergei Kornilov</td></tr><tr><td>Sergey Belyashov</td></tr><tr><td>Sergey Dudoladov</td></tr><tr><td>Sergey Prokhorenko</td></tr><tr><td>Sergey Sargsyan</td></tr><tr><td>Sergey Soloviev</td></tr><tr><td>Sergey Tatarintsev</td></tr><tr><td>Shaik Mohammad Mujeeb</td></tr><tr><td>Shawn McCoy</td></tr><tr><td>Shenhao Wang</td></tr><tr><td>Shihao Zhong</td></tr><tr><td>Shinya Kato</td></tr><tr><td>Shlok Kyal</td></tr><tr><td>Shubham Khanna</td></tr><tr><td>Shveta Malik</td></tr><tr><td>Simon Riggs</td></tr><tr><td>Smolkin Grigory</td></tr><tr><td>Sofia Kopikova</td></tr><tr><td>Song Hongyu</td></tr><tr><td>Song Jinzhou</td></tr><tr><td>Soumyadeep Chakraborty</td></tr><tr><td>Sravan Kumar</td></tr><tr><td>Srinath Reddy</td></tr><tr><td>Stan Hu</td></tr><tr><td>Stepan Neretin</td></tr><tr><td>Stephen Fewer</td></tr><tr><td>Stephen Frost</td></tr><tr><td>Steve Chavez</td></tr><tr><td>Steven Niu</td></tr><tr><td>Suraj Kharage</td></tr><tr><td>Sven Klemm</td></tr><tr><td>Takamichi Osumi</td></tr><tr><td>Takeshi Ideriha</td></tr><tr><td>Tatsuo Ishii</td></tr><tr><td>Ted Yu</td></tr><tr><td>Tels</td></tr><tr><td>Tender Wang</td></tr><tr><td>Teodor Sigaev</td></tr><tr><td>Thom Brown</td></tr><tr><td>Thomas Baehler</td></tr><tr><td>Thomas Krennwallner</td></tr><tr><td>Thomas Munro</td></tr><tr><td>Tim Wood</td></tr><tr><td>Timur Magomedov</td></tr><tr><td>Tobias Wendorff</td></tr><tr><td>Todd Cook</td></tr><tr><td>Tofig Aliev</td></tr><tr><td>Tom Lane</td></tr><tr><td>Tomas Vondra</td></tr><tr><td>Tomasz Rybak</td></tr><tr><td>Tomasz Szypowski</td></tr><tr><td>Torsten Foertsch</td></tr><tr><td>Toshi Harada</td></tr><tr><td>Tristan Partin</td></tr><tr><td>Triveni N</td></tr><tr><td>Umar Hayat</td></tr><tr><td>Vallimaharajan G</td></tr><tr><td>Vasya Boytsov</td></tr><tr><td>Victor Yegorov</td></tr><tr><td>Vignesh C</td></tr><tr><td>Viktor Holmberg</td></tr><tr><td>Vinícius Abrahão</td></tr><tr><td>Vinod Sridharan</td></tr><tr><td>Virender Singla</td></tr><tr><td>Vitaly Davydov</td></tr><tr><td>Vladlen Popolitov</td></tr><tr><td>Vladyslav Nebozhyn</td></tr><tr><td>Walid Ibrahim</td></tr><tr><td>Webbo Han</td></tr><tr><td>Wenhui Qiu</td></tr><tr><td>Will Mortensen</td></tr><tr><td>Will Storey</td></tr><tr><td>Wolfgang Walther</td></tr><tr><td>Xin Zhang</td></tr><tr><td>Xing Guo</td></tr><tr><td>Xuneng Zhou</td></tr><tr><td>Yan Chengpen</td></tr><tr><td>Yang Lei</td></tr><tr><td>Yaroslav Saburov</td></tr><tr><td>Yaroslav Syrytsia</td></tr><tr><td>Yasir Hussain</td></tr><tr><td>Yasuo Honda</td></tr><tr><td>Yogesh Sharma</td></tr><tr><td>Yonghao Lee</td></tr><tr><td>Yoran Heling</td></tr><tr><td>Yu Liang</td></tr><tr><td>Yugo Nagata</td></tr><tr><td>Yuhang Qiu</td></tr><tr><td>Yuki Seino</td></tr><tr><td>Yura Sokolov</td></tr><tr><td>Yurii Rashkovskii</td></tr><tr><td>Yushi Ogiwara</td></tr><tr><td>Yusuke Sugie</td></tr><tr><td>Yuta Katsuragi</td></tr><tr><td>Yuto Sasaki</td></tr><tr><td>Yuuki Fujii</td></tr><tr><td>Yuya Watari</td></tr><tr><td>Zane Duffield</td></tr><tr><td>Zeyuan Hu</td></tr><tr><td>Zhang Mingli</td></tr><tr><td>Zhihong Yu</td></tr><tr><td>Zhijie Hou</td></tr><tr><td>Zsolt Parragi</td></tr></table>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18.html)（原文版本：18.6；核對日期：2026-10-22）
