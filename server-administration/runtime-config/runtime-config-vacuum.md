<a id="RUNTIME-CONFIG-VACUUM"></a>

## 19.10. Vacuum 處理 [#](#RUNTIME-CONFIG-VACUUM)

[19.10.1. 自動 Vacuum](runtime-config-vacuum.md#RUNTIME-CONFIG-AUTOVACUUM)

[19.10.2. 以成本為基礎的 Vacuum 延遲](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)

[19.10.3. 預設行為](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-DEFAULT)

[19.10.4. 凍結](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-FREEZING)

<a id="id-1.6.6.13.2"></a>

這些參數控制 vacuum 的行為。有關 vacuum 的目的與職責，
詳情請參閱[24.1 節](../maintenance/routine-vacuuming.md)。

<a id="RUNTIME-CONFIG-AUTOVACUUM"></a>

### 19.10.1. 自動 Vacuum [#](#RUNTIME-CONFIG-AUTOVACUUM)

這些設定控制 *autovacuum* 功能的行為。
詳情請參閱[24.1.6 節](../maintenance/routine-vacuuming.md#AUTOVACUUM)。
請注意，這些設定中有許多可以逐資料表覆寫；
請參閱[儲存參數](../../reference/sql-commands/sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS)。

<a id="GUC-AUTOVACUUM"></a>

`autovacuum` (`boolean`) <a id="id-1.6.6.13.4.3.1.1.3"></a> [#](#GUC-AUTOVACUUM)
:   控制伺服器是否應該執行
    autovacuum launcher 守護程序。此設定預設為開啟；不過
    [track_counts](runtime-config-statistics.md#GUC-TRACK-COUNTS) 也必須啟用，
    autovacuum 才能正常運作。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；不過可以透過變更資料表儲存參數，
    針對個別資料表停用 autovacuum。

    請注意，即使此參數已停用，系統在必要時仍會啟動
    autovacuum 程序，以防止交易 ID 回捲。詳情請參閱[24.1.5 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)。
<a id="GUC-AUTOVACUUM-WORKER-SLOTS"></a>

`autovacuum_worker_slots` (`integer`) <a id="id-1.6.6.13.4.3.2.1.3"></a> [#](#GUC-AUTOVACUUM-WORKER-SLOTS)
:   指定要保留給 autovacuum 工作程序的 backend 插槽（slot）數量。
    預設值通常為 16 個插槽，但若你的核心設定無法支援
    （由 initdb 期間判斷），則可能較少。
    此參數只能在伺服器啟動時設定。

    變更此值時，也請一併考慮調整
    [autovacuum_max_workers](runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS)。
<a id="GUC-AUTOVACUUM-MAX-WORKERS"></a>

`autovacuum_max_workers` (`integer`) <a id="id-1.6.6.13.4.3.3.1.3"></a> [#](#GUC-AUTOVACUUM-MAX-WORKERS)
:   指定同一時間可以執行的 autovacuum 程序（不含
    autovacuum launcher）最大數量。預設值
    為 `3`。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。

    請注意，若此值設定得比
    [autovacuum_worker_slots](runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS) 更高，將不會有任何效果，
    因為 autovacuum 工作程序是從該設定所建立的插槽集區
    中取得的。
<a id="GUC-AUTOVACUUM-NAPTIME"></a>

`autovacuum_naptime` (`integer`) <a id="id-1.6.6.13.4.3.4.1.3"></a> [#](#GUC-AUTOVACUUM-NAPTIME)
:   指定在同一個資料庫上，兩次 autovacuum 執行之間的
    最小延遲時間。在每一輪中，守護程序會檢查
    該資料庫，並視需要針對該資料庫中的資料表
    發出 `VACUUM` 與 `ANALYZE` 命令。
    若此值指定時未帶單位，則以秒為單位。
    預設值為一分鐘（`1min`）。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-AUTOVACUUM-VACUUM-THRESHOLD"></a>

`autovacuum_vacuum_threshold` (`integer`) <a id="id-1.6.6.13.4.3.5.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-THRESHOLD)
:   指定在任一資料表上觸發 `VACUUM`
    所需的最小已更新或已刪除 tuple 數量。
    預設值為 50 個 tuple。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；
    但可以透過變更資料表儲存參數，
    針對個別資料表覆寫此設定。
<a id="GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD"></a>

`autovacuum_vacuum_insert_threshold` (`integer`) <a id="id-1.6.6.13.4.3.6.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD)
:   指定在任一資料表上觸發
    `VACUUM` 所需的已插入 tuple 數量。
    預設值為 1000 個 tuple。若指定為 -1，autovacuum
    將不會根據插入次數對任何資料表觸發
    `VACUUM` 操作。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；
    但可以透過變更資料表儲存參數，
    針對個別資料表覆寫此設定。
<a id="GUC-AUTOVACUUM-ANALYZE-THRESHOLD"></a>

`autovacuum_analyze_threshold` (`integer`) <a id="id-1.6.6.13.4.3.7.1.3"></a> [#](#GUC-AUTOVACUUM-ANALYZE-THRESHOLD)
:   指定在任一資料表上觸發 `ANALYZE`
    所需的最小已插入、已更新或已刪除 tuple 數量。
    預設值為 50 個 tuple。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；
    但可以透過變更資料表儲存參數，
    針對個別資料表覆寫此設定。
<a id="GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR"></a>

`autovacuum_vacuum_scale_factor` (`floating point`) <a id="id-1.6.6.13.4.3.8.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR)
:   指定在決定是否要觸發 `VACUUM` 時，
    要加到 `autovacuum_vacuum_threshold`
    上的資料表大小比例。
    預設值為 `0.2`（資料表大小的 20%）。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；
    但可以透過變更資料表儲存參數，
    針對個別資料表覆寫此設定。
<a id="GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR"></a>

`autovacuum_vacuum_insert_scale_factor` (`floating point`) <a id="id-1.6.6.13.4.3.9.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR)
:   指定在決定是否要觸發 `VACUUM` 時，
    要加到 `autovacuum_vacuum_insert_threshold` 上的
    資料表中未凍結頁面的比例。預設值為
    `0.2`（資料表中未凍結頁面的 20%）。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；但可以透過變更資料表儲存參數，
    針對個別資料表覆寫此設定。
<a id="GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR"></a>

`autovacuum_analyze_scale_factor` (`floating point`) <a id="id-1.6.6.13.4.3.10.1.3"></a> [#](#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR)
:   指定在決定是否要觸發 `ANALYZE` 時，
    要加到 `autovacuum_analyze_threshold`
    上的資料表大小比例。
    預設值為 `0.1`（資料表大小的 10%）。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；
    但可以透過變更資料表儲存參數，
    針對個別資料表覆寫此設定。
<a id="GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD"></a>

`autovacuum_vacuum_max_threshold` (`integer`) <a id="id-1.6.6.13.4.3.11.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD)
:   指定在任一資料表上觸發 `VACUUM` 所需的
    已更新或已刪除 tuple 的最大數量，也就是以
    `autovacuum_vacuum_threshold` 與
    `autovacuum_vacuum_scale_factor` 計算所得值的
    上限。預設值為
    100,000,000 個 tuple。若指定為 -1，autovacuum 將不會
    對觸發 `VACUUM` 操作所需的已更新或已刪除 tuple 數量
    強制設定上限。此參數只能
    在 `postgresql.conf` 檔案中或伺服器
    命令列上設定；但可以透過變更儲存參數，
    針對個別資料表覆寫此設定。
<a id="GUC-AUTOVACUUM-FREEZE-MAX-AGE"></a>

`autovacuum_freeze_max_age` (`integer`) <a id="id-1.6.6.13.4.3.12.1.3"></a> [#](#GUC-AUTOVACUUM-FREEZE-MAX-AGE)
:   指定資料表的
    `pg_class`.`relfrozenxid` 欄位在被強制執行
    `VACUUM` 操作以防止該資料表內交易 ID 回捲之前，
    所能達到的最大年齡（以交易數計）。
    請注意，即使 autovacuum 在其他方面已停用，
    系統仍會啟動 autovacuum 程序以防止回捲。

    Vacuum 也可以移除
    `pg_xact` 子目錄中的舊檔案，這也是為何預設值
    相對較低，為兩億筆交易。
    此參數只能在伺服器啟動時設定，但可以
    透過變更資料表儲存參數，針對個別資料表調降此設定。
    詳情請參閱[24.1.5 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)。
<a id="GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE"></a>

`autovacuum_multixact_freeze_max_age` (`integer`) <a id="id-1.6.6.13.4.3.13.1.3"></a> [#](#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE)
:   指定資料表的
    `pg_class`.`relminmxid` 欄位在被強制執行
    `VACUUM` 操作以防止該資料表內 multixact ID 回捲之前，
    所能達到的最大年齡（以 multixact 數計）。
    請注意，即使 autovacuum 在其他方面已停用，
    系統仍會啟動 autovacuum 程序以防止回捲。

    對 multixact 執行 vacuum 也可以移除
    `pg_multixact/members` 與 `pg_multixact/offsets`
    子目錄中的舊檔案，這也是為何預設值相對較低，
    為四億筆 multixact。
    此參數只能在伺服器啟動時設定，但可以
    透過變更資料表儲存參數，針對個別資料表調降此設定。
    詳情請參閱[24.1.5.1 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND)。
<a id="GUC-AUTOVACUUM-VACUUM-COST-DELAY"></a>

`autovacuum_vacuum_cost_delay` (`floating point`) <a id="id-1.6.6.13.4.3.14.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-COST-DELAY)
:   指定自動 `VACUUM` 操作中所使用的成本延遲值。
    若指定為 -1，則會改用一般的
    [vacuum_cost_delay](runtime-config-vacuum.md#GUC-VACUUM-COST-DELAY) 值。
    若此值指定時未帶單位，則以毫秒為單位。
    預設值為 2 毫秒。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；
    但可以透過變更資料表儲存參數，
    針對個別資料表覆寫此設定。
<a id="GUC-AUTOVACUUM-VACUUM-COST-LIMIT"></a>

`autovacuum_vacuum_cost_limit` (`integer`) <a id="id-1.6.6.13.4.3.15.1.3"></a> [#](#GUC-AUTOVACUUM-VACUUM-COST-LIMIT)
:   指定自動 `VACUUM` 操作中所使用的成本上限值。
    若指定為 `-1`（此為預設值），
    則會改用一般的
    [vacuum_cost_limit](runtime-config-vacuum.md#GUC-VACUUM-COST-LIMIT) 值。請注意，
    若同時有多個 autovacuum 工作程序在執行，
    此值會按比例分配給各個工作程序，
    使各工作程序上限的總和不超過此變數的值。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；
    但可以透過變更資料表儲存參數，
    針對個別資料表覆寫此設定。

<a id="RUNTIME-CONFIG-RESOURCE-VACUUM-COST"></a>

### 19.10.2. 以成本為基礎的 Vacuum 延遲 [#](#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)

在執行 [VACUUM](../../reference/sql-commands/sql-vacuum.md)
與 [ANALYZE](../../reference/sql-commands/sql-analyze.md)
命令期間，系統會維護一個內部計數器，
用以追蹤所執行的各種 I/O 操作的估計成本。當累計
成本達到某個上限（由
`vacuum_cost_limit` 指定）時，執行該操作的程序
會休眠一段短暫的時間，時間長度由
`vacuum_cost_delay` 指定。接著，該程序
會重設計數器並繼續執行。

此功能的目的，是讓管理者能夠降低這些命令
對並行資料庫活動的 I/O 影響。在許多情況下，
`VACUUM` 與 `ANALYZE` 等維護命令
是否快速完成，其實並不重要；但通常非常重要的是，
這些命令不能顯著干擾系統執行其他資料庫操作的
能力。以成本為基礎的 vacuum 延遲，
提供了管理者達成此目標的一種方式。

對於手動下達的
`VACUUM` 命令，此功能預設為停用。若要啟用，
請將 `vacuum_cost_delay` 變數設為非零
的值。

<a id="GUC-VACUUM-COST-DELAY"></a>

`vacuum_cost_delay` (`floating point`) <a id="id-1.6.6.13.5.5.1.1.3"></a> [#](#GUC-VACUUM-COST-DELAY)
:   當成本上限被超過時，程序將休眠的時間量。若此值
    指定時未帶單位，則以毫秒為單位。預設值為
    `0`，這會停用以成本為基礎的 vacuum 延遲
    功能。正值則會啟用以成本為基礎的 vacuum 功能。

    使用以成本為基礎的 vacuum 時，
    `vacuum_cost_delay` 通常應設定為相當小的值，
    或許小於 1 毫秒。雖然 `vacuum_cost_delay`
    可以設為小數毫秒的值，但這類延遲在較舊的平台上
    可能無法精確測量。在這類平台上，若要在 1 毫秒所能達到的
    程度之上，進一步提高 `VACUUM` 受節流限制的資源消耗量，
    就需要變更其他 vacuum 成本參數。無論如何，
    你都應該將 `vacuum_cost_delay` 設定為
    你的平台能夠穩定測量的最小值；過大的延遲並沒有幫助。
<a id="GUC-VACUUM-COST-PAGE-HIT"></a>

`vacuum_cost_page_hit` (`integer`) <a id="id-1.6.6.13.5.5.2.1.3"></a> [#](#GUC-VACUUM-COST-PAGE-HIT)
:   對共享緩衝區快取中找到的緩衝區執行 vacuum 的估計成本。
    這代表鎖定緩衝集區、
    查詢共享雜湊表，以及掃描頁面內容的成本。
    預設值為 `1`。
<a id="GUC-VACUUM-COST-PAGE-MISS"></a>

`vacuum_cost_page_miss` (`integer`) <a id="id-1.6.6.13.5.5.3.1.3"></a> [#](#GUC-VACUUM-COST-PAGE-MISS)
:   對必須從磁碟讀取的緩衝區執行 vacuum 的估計成本。
    這代表鎖定緩衝集區、查詢共享雜湊表、
    從磁碟讀入所需區塊，以及掃描其內容的成本。預設值
    為 `2`。
<a id="GUC-VACUUM-COST-PAGE-DIRTY"></a>

`vacuum_cost_page_dirty` (`integer`) <a id="id-1.6.6.13.5.5.4.1.3"></a> [#](#GUC-VACUUM-COST-PAGE-DIRTY)
:   當 vacuum 修改一個先前為乾淨（clean）的區塊時所計入的估計成本。
    這代表將該髒（dirty）區塊再次排清（flush）回磁碟
    所需的額外 I/O。預設值為
    `20`。
<a id="GUC-VACUUM-COST-LIMIT"></a>

`vacuum_cost_limit` (`integer`) <a id="id-1.6.6.13.5.5.5.1.3"></a> [#](#GUC-VACUUM-COST-LIMIT)
:   這是會導致 vacuum 程序休眠
    `vacuum_cost_delay` 時間的累計成本上限。
    預設值為 `200`。

### 注意

有些操作會持有關鍵鎖定，因此應該盡快完成。
以成本為基礎的 vacuum 延遲不會在這類操作期間發生。
因此，累計成本有可能遠高於指定的上限。
為避免在這類情況下產生無謂的長延遲，實際的
延遲時間計算方式為 `vacuum_cost_delay` \*
`accumulated_balance` /
`vacuum_cost_limit`，最大值為
`vacuum_cost_delay` \* 4。

<a id="RUNTIME-CONFIG-VACUUM-DEFAULT"></a>

### 19.10.3. 預設行為 [#](#RUNTIME-CONFIG-VACUUM-DEFAULT)

<a id="GUC-VACUUM-TRUNCATE"></a>

`vacuum_truncate` (`boolean`) <a id="id-1.6.6.13.6.2.1.1.3"></a> [#](#GUC-VACUUM-TRUNCATE)
:   啟用或停用 vacuum 嘗試截斷資料表結尾任何空頁面的行為。
    預設值為 `true`。
    若為 `true`，`VACUUM` 與 autovacuum
    會執行截斷操作，且被截斷頁面所佔用的磁碟空間
    會歸還給作業系統。請注意，截斷操作需要對該資料表
    持有 `ACCESS EXCLUSIVE` 鎖。
    [`VACUUM`](../../reference/sql-commands/sql-vacuum.md) 的
    `TRUNCATE` 參數，若有指定，
    會覆寫此參數的值。此設定
    也可以透過變更資料表儲存參數，針對個別資料表覆寫。

<a id="RUNTIME-CONFIG-VACUUM-FREEZING"></a>

### 19.10.4. 凍結 [#](#RUNTIME-CONFIG-VACUUM-FREEZING)

為了在交易 ID 回捲後仍維持正確性，
PostgreSQL 會將足夠舊的資料列標記為
*已凍結（frozen）*。這些資料列對所有人皆可見；
其他交易不需要檢查其插入 XID 即可判斷可見性。
`VACUUM` 負責將資料列標記為已凍結。以下設定
控制 `VACUUM` 的凍結行為，應根據
系統的 XID 消耗速率，以及主要工作負載的資料存取模式進行調校。
有關交易 ID 回捲以及調校這些參數的詳情，
請參閱[24.1.5 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)。

<a id="GUC-VACUUM-FREEZE-TABLE-AGE"></a>

`vacuum_freeze_table_age` (`integer`) <a id="id-1.6.6.13.7.3.1.1.3"></a> [#](#GUC-VACUUM-FREEZE-TABLE-AGE)
:   如果資料表的
    `pg_class`.`relfrozenxid` 欄位已達到
    此設定所指定的年齡，`VACUUM` 會執行強制掃描
    （aggressive scan）。強制掃描與一般
    `VACUUM` 的差異在於，它會造訪每個可能包含未凍結
    XID 或 MXID 的頁面，而不僅是可能包含死亡 tuple 的頁面。
    預設值為一億五千萬筆交易。雖然使用者可以將此值
    設為零到二十億之間的任何值，但 `VACUUM`
    會默默地將有效值限制為
    [autovacuum_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE) 的 95%，
    以便在為該資料表啟動防回捲 autovacuum 之前，
    定期的手動 `VACUUM` 仍有機會執行。詳情
    請參閱
    [24.1.5 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)。
<a id="GUC-VACUUM-FREEZE-MIN-AGE"></a>

`vacuum_freeze_min_age` (`integer`) <a id="id-1.6.6.13.7.3.2.1.3"></a> [#](#GUC-VACUUM-FREEZE-MIN-AGE)
:   指定 `VACUUM` 用來決定是否要
    對 XID 較舊的頁面觸發凍結所使用的
    臨界年齡（以交易數計）。
    預設值為五千萬筆交易。雖然
    使用者可以將此值設為零到十億之間的任何值，
    `VACUUM` 會默默地將有效值限制為
    [autovacuum_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE) 值的一半，
    以避免強制 autovacuum 之間的間隔過短。
    詳情請參閱[24.1.5 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)。
<a id="GUC-VACUUM-FAILSAFE-AGE"></a>

`vacuum_failsafe_age` (`integer`) <a id="id-1.6.6.13.7.3.3.1.3"></a> [#](#GUC-VACUUM-FAILSAFE-AGE)
:   指定資料表的
    `pg_class`.`relfrozenxid`
    欄位在 `VACUUM` 採取非常手段
    以避免系統全域交易 ID 回捲失敗之前，
    所能達到的最大年齡（以交易數計）。這是
    `VACUUM` 的最後手段策略。當防止交易 ID 回捲的
    autovacuum 已經執行了一段時間時，通常就會觸發
    此故障保護機制，不過任何 `VACUUM` 期間
    都有可能觸發此機制。

    觸發故障保護機制時，任何原本生效中的
    以成本為基礎的延遲都將不再套用，其他非必要的
    維護作業（例如索引 vacuum）會被略過，任何正在使用的
    [*[緩衝區存取策略](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)*](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)
    都會被停用，使 `VACUUM` 可以
    自由使用所有的
    [*[共享緩衝區](../../appendixes/glossary/README.md#GLOSSARY-SHARED-MEMORY)*](../../appendixes/glossary/README.md#GLOSSARY-SHARED-MEMORY)。

    預設值為十六億筆交易。雖然使用者可以
    將此值設為零到二十一億之間的任何值，
    `VACUUM` 會默默地將有效值調整為不低於
    [autovacuum_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE) 的 105%。
<a id="GUC-VACUUM-MULTIXACT-FREEZE-TABLE-AGE"></a>

`vacuum_multixact_freeze_table_age` (`integer`) <a id="id-1.6.6.13.7.3.4.1.3"></a> [#](#GUC-VACUUM-MULTIXACT-FREEZE-TABLE-AGE)
:   如果資料表的
    `pg_class`.`relminmxid` 欄位已達到
    此設定所指定的年齡，`VACUUM` 會執行強制掃描。
    強制掃描與一般
    `VACUUM` 的差異在於，它會造訪每個可能包含未凍結
    XID 或 MXID 的頁面，而不僅是可能包含死亡 tuple 的頁面。
    預設值為一億五千萬個 multixact。
    雖然使用者可以將此值設為零到二十億之間的任何值，
    `VACUUM` 會默默地將有效值限制為
    [autovacuum_multixact_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE) 的 95%，
    以便在為該資料表啟動防回捲機制之前，
    定期的手動 `VACUUM` 仍有機會執行。
    詳情請參閱[24.1.5.1 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND)。
<a id="GUC-VACUUM-MULTIXACT-FREEZE-MIN-AGE"></a>

`vacuum_multixact_freeze_min_age` (`integer`) <a id="id-1.6.6.13.7.3.5.1.3"></a> [#](#GUC-VACUUM-MULTIXACT-FREEZE-MIN-AGE)
:   指定 `VACUUM` 用來決定是否要對
    multixact ID 較舊的頁面觸發凍結所使用的
    臨界年齡（以 multixact 數計）。預設值為五百萬個 multixact。
    雖然使用者可以將此值設為零到十億之間的任何值，
    `VACUUM` 會默默地將有效值限制為
    [autovacuum_multixact_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE)
    值的一半，以避免強制 autovacuum 之間的間隔過短。
    詳情請參閱[24.1.5.1 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-MULTIXACT-WRAPAROUND)。
<a id="GUC-VACUUM-MULTIXACT-FAILSAFE-AGE"></a>

`vacuum_multixact_failsafe_age` (`integer`) <a id="id-1.6.6.13.7.3.6.1.3"></a> [#](#GUC-VACUUM-MULTIXACT-FAILSAFE-AGE)
:   指定資料表的
    `pg_class`.`relminmxid`
    欄位在 `VACUUM` 採取非常手段
    以避免系統全域 multixact ID 回捲失敗之前，
    所能達到的最大年齡（以 multixact 數計）。這是
    `VACUUM` 的最後手段策略。當防止交易 ID 回捲的
    autovacuum 已經執行了一段時間時，通常就會觸發
    此故障保護機制，不過任何 `VACUUM` 期間
    都有可能觸發此機制。

    觸發故障保護機制時，任何原本生效中的
    以成本為基礎的延遲都將不再套用，其他非必要的
    維護作業（例如索引 vacuum）會被略過。

    預設值為十六億個 multixact。雖然使用者可以
    將此值設為零到二十一億之間的任何值，
    `VACUUM` 會默默地將有效值調整為不低於
    [autovacuum_multixact_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE) 的 105%。
<a id="GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE"></a>

`vacuum_max_eager_freeze_failure_rate` (`floating point`) <a id="id-1.6.6.13.7.3.7.1.3"></a> [#](#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE)
:   指定在停用主動掃描（eager scanning）之前，
    `VACUUM` 可以掃描並*未能*在可見度映射（visibility map）
    中將頁面標記為全部凍結（all-frozen）的頁面數量上限
    （以該關聯總頁面數的比例表示）。值為
    `0` 會完全停用主動掃描。預設值為
    `0.03`（3%）。

    請注意，啟用主動掃描時，只有凍結失敗的次數
    會計入此上限，成功凍結的次數則不計入。成功的頁面
    凍結內部上限為該關聯中全部可見但尚未
    全部凍結頁面的 20%。為成功的頁面凍結設定上限，
    有助於將額外負擔分攤到多次一般 vacuum 上，
    並限制對已在下次積極 vacuum 之前又再次被修改的頁面
    進行無謂積極凍結所可能帶來的潛在缺點。

    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定；但可以透過變更
    [對應的資料表儲存參數](../../reference/sql-commands/sql-createtable.md#RELOPTION-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE)，
    針對個別資料表覆寫此設定。
    有關調校 vacuum 凍結行為的更多資訊，
    請參閱[24.1.5 節](../maintenance/routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-vacuum.html)（原文版本：18.6；核對日期：2026-09-24）
