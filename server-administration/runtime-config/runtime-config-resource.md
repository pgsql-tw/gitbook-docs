<a id="RUNTIME-CONFIG-RESOURCE"></a>

## 19.4. 資源消耗 [#](#RUNTIME-CONFIG-RESOURCE)

[19.4.1. 記憶體](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY)

[19.4.2. 磁碟](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-DISK)

[19.4.3. 核心資源使用量](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-KERNEL)

[19.4.4. 背景寫入程序](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER)

[19.4.5. I/O](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-IO)

[19.4.6. 工作程序](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-WORKER-PROCESSES)

<a id="RUNTIME-CONFIG-RESOURCE-MEMORY"></a>

### 19.4.1. 記憶體 [#](#RUNTIME-CONFIG-RESOURCE-MEMORY)

<a id="GUC-SHARED-BUFFERS"></a>

`shared_buffers` (`integer`) <a id="id-1.6.6.7.2.2.1.1.3"></a> [#](#GUC-SHARED-BUFFERS)
:   設定資料庫伺服器用於共享記憶體緩衝區的記憶體量。
    預設值通常為 128 百萬位元組
    （`128MB`），但若你的核心設定無法支援
    （由 initdb 期間判斷），則可能較少。
    此設定至少必須為 128 千位元組。不過，
    要獲得良好效能，通常需要遠高於此最小值的設定。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    （非預設的 `BLCKSZ` 會改變此最小值。）
    此參數只能在伺服器啟動時設定。

    如果你有一台配備 1GB 以上 RAM 的專屬資料庫伺服器，
    `shared_buffers` 合理的起始值，是系統記憶體的
    25%。有些工作負載即使將 `shared_buffers`
    設得更大也有效，但由於
    PostgreSQL 也依賴作業系統的快取，
    將超過 40% 的 RAM 配置給 `shared_buffers`
    通常不會比配置較小的量效果更好。將
    `shared_buffers` 設得較大，通常也需要
    相應提高 `max_wal_size`，
    以便將寫入大量新資料或已變更資料的過程，
    分散到較長的時間內進行。

    在 RAM 小於 1GB 的系統上，適合使用較小比例的
    RAM，以便為作業系統保留足夠的空間。
<a id="GUC-HUGE-PAGES"></a>

`huge_pages` (`enum`) <a id="id-1.6.6.7.2.2.2.1.3"></a> [#](#GUC-HUGE-PAGES)
:   控制是否為主要共享記憶體區域請求巨型分頁
    （huge page）。合法的值有 `try`（預設值）、
    `on`，以及 `off`。
    此參數只能在伺服器啟動時設定。當
    `huge_pages` 設為 `try` 時，
    伺服器會嘗試請求巨型分頁，但若失敗則會退回預設方式。
    設為 `on` 時，若請求巨型分頁失敗，
    伺服器將無法啟動。設為 `off` 時，
    則不會請求巨型分頁。巨型分頁的實際狀態，
    由伺服器變數
    [huge_pages_status](runtime-config-preset.md#GUC-HUGE-PAGES-STATUS) 表示。

    目前，此設定僅在 Linux 與 Windows 上受支援。
    在其他系統上，設為 `try` 時
    此設定會被忽略。在 Linux 上，只有在
    `shared_memory_type` 設為 `mmap`
    （預設值）時才受支援。

    使用巨型分頁可以縮小頁面表，並減少用於記憶體管理的
    CPU 時間，藉此提升效能。有關在 Linux 上使用巨型分頁的
    更多細節，請參閱[18.4.5 節](../runtime/kernel-resources.md#LINUX-HUGE-PAGES)。

    在 Windows 上，巨型分頁被稱為大分頁（large page）。若要使用它們，
    你需要為執行 PostgreSQL 的 Windows 使用者帳戶
    指派「鎖定記憶體中的分頁」使用者權限。
    你可以使用 Windows 群組原則工具（gpedit.msc），
    指派「鎖定記憶體中的分頁」使用者權限。
    若要以獨立程序的方式（而非 Windows 服務）在命令提示字元中
    啟動資料庫伺服器，該命令提示字元必須以系統管理員身分執行，
    或必須停用使用者帳戶控制（UAC）。啟用 UAC 時，
    一般的命令提示字元啟動時會撤銷「鎖定記憶體中的分頁」
    使用者權限。

    請注意，此設定僅影響主要共享記憶體區域。
    Linux、FreeBSD 與 Illumos 等作業系統，
    也可以在未經 PostgreSQL 明確請求的情況下，
    自動為一般記憶體配置使用巨型分頁
    （也稱為「超級（super）」分頁或
    「大（large）」分頁）。在 Linux 上，
    這被稱為「透明巨型分頁」<a id="id-1.6.6.7.2.2.2.2.5.5"></a>（THP）。已知這項功能
    在某些 Linux 版本上，會對某些使用者的
    PostgreSQL 造成效能下降，因此目前不建議
    使用（這與明確使用 `huge_pages` 不同）。
<a id="GUC-HUGE-PAGE-SIZE"></a>

`huge_page_size` (`integer`) <a id="id-1.6.6.7.2.2.3.1.3"></a> [#](#GUC-HUGE-PAGE-SIZE)
:   當透過
    [huge_pages](runtime-config-resource.md#GUC-HUGE-PAGES) 啟用巨型分頁時，
    控制巨型分頁的大小。
    預設值為零（`0`）。
    設為 `0` 時，會使用系統上預設的巨型分頁
    大小。此參數只能在伺服器啟動時設定。

    現代 64 位元伺服器架構上一些常見的分頁大小包括：
    `2MB` 與 `1GB`（Intel 與 AMD）、`16MB` 與
    `16GB`（IBM POWER），以及 `64kB`、`2MB`、
    `32MB` 與 `1GB`（ARM）。有關使用方式與支援情形的
    更多資訊，請參閱[18.4.5 節](../runtime/kernel-resources.md#LINUX-HUGE-PAGES)。

    目前僅在 Linux 上支援非預設設定。
<a id="GUC-TEMP-BUFFERS"></a>

`temp_buffers` (`integer`) <a id="id-1.6.6.7.2.2.4.1.3"></a> [#](#GUC-TEMP-BUFFERS)
:   設定每個資料庫工作階段中，用於暫存緩衝區的
    最大記憶體量。這些是僅供存取暫存資料表使用的
    工作階段本機緩衝區。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 8 百萬位元組（`8MB`）。
    （若 `BLCKSZ` 不是 8kB，預設值會依比例
    縮放。）
    此設定可以在個別工作階段內變更，
    但只能在該工作階段第一次使用暫存資料表
    之前變更；後續嘗試變更此值，
    對該工作階段將沒有效果。

    工作階段會依需要配置暫存緩衝區，
    直到達到 `temp_buffers` 所給定的上限為止。
    在實際上並不需要很多暫存緩衝區的工作階段中，
    設定較大值所需的代價，每增加一單位
    `temp_buffers`，只會多一個緩衝區描述子，
    約 64 位元組。不過，若某個緩衝區確實被使用，
    則會另外消耗 8192 位元組（或一般而言，
    `BLCKSZ` 位元組）。
<a id="GUC-MAX-PREPARED-TRANSACTIONS"></a>

`max_prepared_transactions` (`integer`) <a id="id-1.6.6.7.2.2.5.1.3"></a> [#](#GUC-MAX-PREPARED-TRANSACTIONS)
:   設定同一時間可以處於「已備妥（prepared）」狀態的
    最大交易數量（參閱 [PREPARE TRANSACTION](../../reference/sql-commands/sql-prepare-transaction.md)）。
    將此參數設為零（預設值）
    會停用已備妥交易功能。
    此參數只能在伺服器啟動時設定。

    如果你並不打算使用已備妥交易，應將此參數
    設為零，以防止意外建立已備妥交易。如果你確實
    使用已備妥交易，可能會希望
    `max_prepared_transactions` 至少與
    [max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS) 一樣大，
    以便每個工作階段都能有一筆待處理的已備妥交易。

    在執行待命伺服器時，你必須將此參數設為與
    主要伺服器相同或更高的值，否則
    待命伺服器中將不允許執行查詢。
<a id="GUC-WORK-MEM"></a>

`work_mem` (`integer`) <a id="id-1.6.6.7.2.2.6.1.3"></a> [#](#GUC-WORK-MEM)
:   設定查詢操作（例如排序或雜湊表）在寫入暫存磁碟檔案
    之前，所能使用的基本最大記憶體量。
    若此值指定時未帶單位，則以千位元組為單位。
    預設值為 4 百萬位元組（`4MB`）。
    請注意，一個複雜的查詢可能會同時執行多個排序
    與雜湊操作，一般而言，每個操作在開始
    寫入暫存檔案之前，都可以使用最多此值所指定的
    記憶體量。此外，也可能有多個工作階段
    正在並行執行這類操作。
    因此，實際使用的總記憶體量，可能是
    `work_mem` 值的許多倍；選擇此值時
    必須將此事實納入考量。排序操作用於
    `ORDER BY`、`DISTINCT`，
    以及合併聯結。
    雜湊表則用於雜湊聯結、以雜湊為基礎的聚合、memoize
    節點，以及以雜湊為基礎處理 `IN` 子查詢。

    以雜湊為基礎的操作，通常對可用記憶體比等效的
    以排序為基礎的操作更為敏感。雜湊表的
    記憶體上限，是以
    `work_mem` 乘以
    `hash_mem_multiplier` 計算得出的。這使得
    以雜湊為基礎的操作，可以使用超過一般
    `work_mem` 基本量的記憶體。
<a id="GUC-HASH-MEM-MULTIPLIER"></a>

`hash_mem_multiplier` (`floating point`) <a id="id-1.6.6.7.2.2.7.1.3"></a> [#](#GUC-HASH-MEM-MULTIPLIER)
:   用於計算以雜湊為基礎的操作可以使用的
    最大記憶體量。最終上限是以
    `work_mem` 乘以
    `hash_mem_multiplier` 決定的。預設值為
    2.0，這使得以雜湊為基礎的操作，會使用兩倍於一般
    `work_mem` 基本量的記憶體。

    在查詢操作經常發生資料溢出（spilling）的環境中，
    尤其是單純提高
    `work_mem` 會導致記憶體壓力（記憶體壓力
    通常表現為間歇性的記憶體不足錯誤）的情況下，
    可以考慮提高 `hash_mem_multiplier`。
    預設值 2.0 對於混合工作負載通常有效。
    在 `work_mem` 已經提高到 40MB 以上的
    環境中，設為 2.0 至 8.0 或
    更高的範圍可能會有效。
<a id="GUC-MAINTENANCE-WORK-MEM"></a>

`maintenance_work_mem` (`integer`) <a id="id-1.6.6.7.2.2.8.1.3"></a> [#](#GUC-MAINTENANCE-WORK-MEM)
:   指定維護操作（例如 `VACUUM`、`CREATE
    INDEX` 與 `ALTER TABLE ADD FOREIGN KEY`）
    所使用的最大記憶體量。
    若此值指定時未帶單位，則以千位元組為單位。
    預設值
    為 64 百萬位元組（`64MB`）。由於一個資料庫
    工作階段一次只能執行其中一種操作，且一套安裝
    通常不會同時並行執行很多這類操作，因此可以安全地
    將此值設得比 `work_mem`
    大得多。較大的設定可能改善 vacuum 以及
    還原資料庫傾印檔的效能。

    請注意，當 autovacuum 執行時，最多可能配置
    [autovacuum_max_workers](runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS) 倍的此記憶體，
    因此請小心，不要將預設值設得
    太高。透過分別設定
    [autovacuum_work_mem](runtime-config-resource.md#GUC-AUTOVACUUM-WORK-MEM) 來控制此情況，
    可能會很有用。
<a id="GUC-AUTOVACUUM-WORK-MEM"></a>

`autovacuum_work_mem` (`integer`) <a id="id-1.6.6.7.2.2.9.1.3"></a> [#](#GUC-AUTOVACUUM-WORK-MEM)
:   指定每個 autovacuum 工作程序所使用的
    最大記憶體量。
    若此值指定時未帶單位，則以千位元組為單位。
    預設值為 -1，代表應改用
    [maintenance_work_mem](runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM) 的值。
    此設定對其他情境下執行 `VACUUM`
    的行為沒有影響。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定。
<a id="GUC-VACUUM-BUFFER-USAGE-LIMIT"></a>

`vacuum_buffer_usage_limit` (`integer`) <a id="id-1.6.6.7.2.2.10.1.3"></a> [#](#GUC-VACUUM-BUFFER-USAGE-LIMIT)
:   指定 `VACUUM` 與 `ANALYZE`
    命令所使用的
    [*[緩衝區存取策略](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)*](../../appendixes/glossary/README.md#GLOSSARY-BUFFER-ACCESS-STRATEGY)
    大小。設為 `0` 會允許此操作使用
    任意數量的 `shared_buffers`。否則，
    合法的大小範圍是從 `128 kB` 到
    `16 GB`。若指定的大小超過
    `shared_buffers` 大小的 1/8，此大小會被
    默默限制為該值。預設值為 `2MB`。
    若此值指定時未帶單位，則以千位元組為單位。此
    參數可以隨時設定。傳遞
    `BUFFER_USAGE_LIMIT` 選項時，可以針對
    [VACUUM](../../reference/sql-commands/sql-vacuum.md) 與 [ANALYZE](../../reference/sql-commands/sql-analyze.md)
    覆寫此值。較高的設定可以讓 `VACUUM` 與
    `ANALYZE` 執行得更快，但設定過大
    可能導致其他有用的頁面被過多地從
    共享緩衝區中淘汰。
<a id="GUC-LOGICAL-DECODING-WORK-MEM"></a>

`logical_decoding_work_mem` (`integer`) <a id="id-1.6.6.7.2.2.11.1.3"></a> [#](#GUC-LOGICAL-DECODING-WORK-MEM)
:   指定邏輯解碼在部分已解碼的變更被寫入本機磁碟之前，
    所使用的最大記憶體量。這限制了邏輯串流複寫
    連線所使用的記憶體量。預設值為 64 百萬位元組
    （`64MB`）。由於每個複寫連線只使用一個
    此大小的緩衝區，且一套安裝通常不會同時
    並行有太多這類連線（受
    `max_wal_senders` 限制），因此可以安全地
    將此值設得比 `work_mem` 高得多，
    以減少寫入磁碟的已解碼變更量。
<a id="GUC-COMMIT-TIMESTAMP-BUFFERS"></a>

`commit_timestamp_buffers` (`integer`) <a id="id-1.6.6.7.2.2.12.1.3"></a> [#](#GUC-COMMIT-TIMESTAMP-BUFFERS)
:   指定用於快取
    `pg_commit_ts` 內容（參閱
    [表 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)）的記憶體量。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 `0`，此時會請求
    `shared_buffers`/512 個區塊，上限為 1024 個區塊，
    但不低於 16 個區塊。
    此參數只能在伺服器啟動時設定。
<a id="GUC-MULTIXACT-MEMBER-BUFFERS"></a>

`multixact_member_buffers` (`integer`) <a id="id-1.6.6.7.2.2.13.1.3"></a> [#](#GUC-MULTIXACT-MEMBER-BUFFERS)
:   指定用於快取
    `pg_multixact/members` 內容（參閱
    [表 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)）的共享記憶體量。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 `32`。
    此參數只能在伺服器啟動時設定。
<a id="GUC-MULTIXACT-OFFSET-BUFFERS"></a>

`multixact_offset_buffers` (`integer`) <a id="id-1.6.6.7.2.2.14.1.3"></a> [#](#GUC-MULTIXACT-OFFSET-BUFFERS)
:   指定用於快取
    `pg_multixact/offsets` 內容（參閱
    [表 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)）的共享記憶體量。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 `16`。
    此參數只能在伺服器啟動時設定。
<a id="GUC-NOTIFY-BUFFERS"></a>

`notify_buffers` (`integer`) <a id="id-1.6.6.7.2.2.15.1.3"></a> [#](#GUC-NOTIFY-BUFFERS)
:   指定用於快取
    `pg_notify` 內容（參閱
    [表 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)）的共享記憶體量。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 `16`。
    此參數只能在伺服器啟動時設定。
<a id="GUC-SERIALIZABLE-BUFFERS"></a>

`serializable_buffers` (`integer`) <a id="id-1.6.6.7.2.2.16.1.3"></a> [#](#GUC-SERIALIZABLE-BUFFERS)
:   指定用於快取
    `pg_serial` 內容（參閱
    [表 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)）的共享記憶體量。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 `32`。
    此參數只能在伺服器啟動時設定。
<a id="GUC-SUBTRANSACTION-BUFFERS"></a>

`subtransaction_buffers` (`integer`) <a id="id-1.6.6.7.2.2.17.1.3"></a> [#](#GUC-SUBTRANSACTION-BUFFERS)
:   指定用於快取
    `pg_subtrans` 內容（參閱
    [表 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)）的共享記憶體量。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 `0`，此時會請求
    `shared_buffers`/512 個區塊，上限為 1024 個區塊，
    但不低於 16 個區塊。
    此參數只能在伺服器啟動時設定。
<a id="GUC-TRANSACTION-BUFFERS"></a>

`transaction_buffers` (`integer`) <a id="id-1.6.6.7.2.2.18.1.3"></a> [#](#GUC-TRANSACTION-BUFFERS)
:   指定用於快取
    `pg_xact` 內容（參閱
    [表 66.1](../../internals/storage/storage-file-layout.md#PGDATA-CONTENTS-TABLE)）的共享記憶體量。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    預設值為 `0`，此時會請求
    `shared_buffers`/512 個區塊，上限為 1024 個區塊，
    但不低於 16 個區塊。
    此參數只能在伺服器啟動時設定。
<a id="GUC-MAX-STACK-DEPTH"></a>

`max_stack_depth` (`integer`) <a id="id-1.6.6.7.2.2.19.1.3"></a> [#](#GUC-MAX-STACK-DEPTH)
:   指定伺服器執行堆疊的最大安全深度。
    此參數的理想設定值，是核心所強制執行的實際堆疊大小
    上限（由 `ulimit -s` 或本機等效機制設定），
    再減去約一百萬位元組的安全邊界。之所以需要
    安全邊界，是因為堆疊深度並非在伺服器的每個
    常式中都會被檢查，只會在關鍵、有可能遞迴的常式中檢查。
    若此值指定時未帶單位，則以千位元組為單位。
    預設設定為兩百萬位元組（`2MB`），
    這是相對保守的小值，不太可能造成當機風險。不過，
    這可能太小，無法執行複雜的函式。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。

    將 `max_stack_depth` 設得比
    實際的核心上限更高，代表失控的遞迴函式
    有可能導致個別 backend 程序當機。在
    PostgreSQL 能夠判斷核心上限的平台上，
    伺服器不會允許將此變數設為不安全的
    值。不過，並非所有平台都提供這項資訊，
    因此在選擇此值時仍建議謹慎。
<a id="GUC-SHARED-MEMORY-TYPE"></a>

`shared_memory_type` (`enum`) <a id="id-1.6.6.7.2.2.20.1.3"></a> [#](#GUC-SHARED-MEMORY-TYPE)
:   指定伺服器應用於保存
    PostgreSQL 共享緩衝區及其他共享資料之主要
    共享記憶體區域的共享記憶體實作方式。可能的值有
    `mmap`（使用 `mmap` 配置的匿名
    共享記憶體）、
    `sysv`（透過 `shmget` 配置的
    System V 共享記憶體），以及 `windows`（用於 Windows
    共享記憶體）。並非所有平台都支援所有的值；
    對該平台而言第一個受支援的選項即為預設值。一般
    不建議使用 `sysv` 選項（此選項在任何平台上
    都不是預設值），因為它通常需要
    非預設的核心設定，才能允許大量配置
    （參閱[18.4.1 節](../runtime/kernel-resources.md#SYSVIPC)）。
    此參數只能在伺服器啟動時設定。
<a id="GUC-DYNAMIC-SHARED-MEMORY-TYPE"></a>

`dynamic_shared_memory_type` (`enum`) <a id="id-1.6.6.7.2.2.21.1.3"></a> [#](#GUC-DYNAMIC-SHARED-MEMORY-TYPE)
:   指定伺服器應使用的動態共享記憶體實作方式。
    可能的值有 `posix`（使用 `shm_open`
    配置的 POSIX 共享記憶體）、`sysv`
    （透過 `shmget` 配置的 System V 共享記憶體）、
    `windows`（用於 Windows 共享記憶體），
    以及 `mmap`（使用儲存在資料目錄中、
    以記憶體對映的檔案來模擬共享記憶體）。
    並非所有平台都支援所有的值；對該平台而言
    第一個受支援的選項通常即為預設值。一般不建議使用
    `mmap` 選項（此選項在任何平台上都不是預設值），
    因為作業系統可能會反覆將已修改的頁面寫回磁碟，
    增加系統 I/O 負載；不過在除錯時、
    或當 `pg_dynshmem` 目錄儲存在 RAM 磁碟上時，
    或當其他共享記憶體機制不可用時，此選項可能會有用。
    此參數只能在伺服器啟動時設定。
<a id="GUC-MIN-DYNAMIC-SHARED-MEMORY"></a>

`min_dynamic_shared_memory` (`integer`) <a id="id-1.6.6.7.2.2.22.1.3"></a> [#](#GUC-MIN-DYNAMIC-SHARED-MEMORY)
:   指定伺服器啟動時應配置多少記憶體，供
    平行查詢使用。當這塊記憶體區域不足，或已被
    並行查詢耗盡時，新的平行查詢會嘗試使用
    `dynamic_shared_memory_type` 所設定的方法，
    暫時向作業系統額外配置共享記憶體，
    這可能因記憶體管理額外負擔而較慢。以
    `min_dynamic_shared_memory` 在啟動時配置的記憶體，
    會受到支援此功能之作業系統上 `huge_pages`
    設定的影響，在自動管理此功能的作業系統上，
    也更有可能因較大的分頁而受益。
    預設值為 `0`（無）。此參數只能
    在伺服器啟動時設定。

<a id="RUNTIME-CONFIG-RESOURCE-DISK"></a>

### 19.4.2. 磁碟 [#](#RUNTIME-CONFIG-RESOURCE-DISK)

<a id="GUC-TEMP-FILE-LIMIT"></a>

`temp_file_limit` (`integer`) <a id="id-1.6.6.7.3.2.1.1.3"></a> [#](#GUC-TEMP-FILE-LIMIT)
:   指定一個程序可用於暫存檔案（例如排序與雜湊
    暫存檔案，或保留中游標的儲存檔案）的最大磁碟
    空間量。嘗試超過此上限的交易將被取消。
    若此值指定時未帶單位，則以千位元組為單位。
    `-1`（預設值）代表沒有上限。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。

    此設定限制的是給定 PostgreSQL 程序
    在任一時刻所使用的所有暫存檔案的總空間。
    請注意，明確建立的暫存資料表所使用的磁碟空間，
    與查詢執行期間在幕後使用的暫存檔案不同，
    並*不*計入此上限。
<a id="GUC-FILE-COPY-METHOD"></a>

`file_copy_method` (`enum`) <a id="id-1.6.6.7.3.2.2.1.3"></a> [#](#GUC-FILE-COPY-METHOD)
:   指定用於複製檔案的方法。
    可能的值有 `COPY`（預設值）與
    `CLONE`（若作業系統支援）。

    此參數會影響：

    * `CREATE DATABASE ... STRATEGY=FILE_COPY`
    * `ALTER DATABASE ... SET TABLESPACE ...`

    `CLONE` 會使用
    `copy_file_range()`（Linux、FreeBSD）或
    `copyfile`（macOS）系統呼叫，
    讓核心有機會在某些檔案系統上共享磁碟區塊，
    或將工作下推到較低層。
<a id="GUC-FILE-EXTEND-METHOD"></a>

`file_extend_method` (`enum`) <a id="id-1.6.6.7.3.2.3.1.3"></a> [#](#GUC-FILE-EXTEND-METHOD)
:   指定在批次操作（例如 `COPY`）期間，
    用於擴充資料檔案的方法。根據作業系統，
    會使用第一個可用的選項作為預設值：

    * `posix_fallocate`（Unix）使用標準的
      POSIX 介面配置磁碟空間，但在某些系統上不存在。
      若此功能存在，但底層檔案系統不支援，
      此選項會默默退回 `write_zeros`。
      已知目前版本的 BTRFS 在使用此選項時
      會停用壓縮功能。
      在具備此函式的系統上，這是預設值。
    * `write_zeros` 透過寫出全零位元組的區塊
      來擴充檔案。在不具備
      `posix_fallocate` 函式的系統上，這是預設值。

    當資料檔案擴充 8 個區塊或以下時，
    永遠會使用 `write_zeros` 方法。
<a id="GUC-MAX-NOTIFY-QUEUE-PAGES"></a>

`max_notify_queue_pages` (`integer`) <a id="id-1.6.6.7.3.2.4.1.3"></a> [#](#GUC-MAX-NOTIFY-QUEUE-PAGES)
:   指定為
    [NOTIFY](../../reference/sql-commands/sql-notify.md) / [LISTEN](../../reference/sql-commands/sql-listen.md) 佇列
    配置的最大頁面數。
    預設值為 1048576。對於 8 KB 的頁面，這允許消耗
    最多 8 GB 的磁碟空間。
    此參數只能在伺服器啟動時設定。

<a id="RUNTIME-CONFIG-RESOURCE-KERNEL"></a>

### 19.4.3. 核心資源使用量 [#](#RUNTIME-CONFIG-RESOURCE-KERNEL)

<a id="GUC-MAX-FILES-PER-PROCESS"></a>

`max_files_per_process` (`integer`) <a id="id-1.6.6.7.4.2.1.1.3"></a> [#](#GUC-MAX-FILES-PER-PROCESS)
:   設定每個伺服器子程序允許同時開啟的最大檔案數量；
    postmaster 中已經開啟的檔案不計入此上限。
    預設值為一千個檔案。

    如果核心強制執行安全的逐程序上限，
    你就不需要擔心此設定。但在某些平台上
    （特別是大多數 BSD 系統），若許多程序同時嘗試
    開啟這麼多檔案，核心會允許個別程序開啟
    遠比系統實際能支援還要多的檔案。如果你發現
    出現「開啟的檔案過多」失敗訊息，
    請嘗試降低此設定。
    此參數只能在伺服器啟動時設定。

<a id="RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER"></a>

### 19.4.4. 背景寫入程序 [#](#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER)

有一個獨立的伺服器程序，稱為*背景寫入程序
（background writer）*，其功能是發出對「髒（dirty，
即新增或已修改）」共享緩衝區的寫入。當乾淨的共享
緩衝區數量看起來不足時，背景寫入程序會將部分
髒緩衝區寫入檔案系統，並將其標記為乾淨。這可以
降低處理使用者查詢的伺服器程序找不到乾淨緩衝區、
而必須自行寫入髒緩衝區的可能性。
不過，背景寫入程序確實會導致整體 I/O 負載
淨增加，因為反覆變髒的頁面，原本可能每個檢查點
間隔只會被寫入一次，但背景寫入程序可能在
同一個間隔內就多次寫入該頁面。本小節所討論的
參數，可用於針對本地需求調校此行為。

<a id="GUC-BGWRITER-DELAY"></a>

`bgwriter_delay` (`integer`) <a id="id-1.6.6.7.5.3.1.1.3"></a> [#](#GUC-BGWRITER-DELAY)
:   指定背景寫入程序各輪活動之間的延遲。
    在每一輪中，寫入程序會為若干個髒緩衝區
    （其數量可透過以下參數控制）發出寫入。
    接著它會休眠
    `bgwriter_delay` 的長度，然後重複此過程。
    不過，當緩衝集區中沒有髒緩衝區時，
    無論 `bgwriter_delay` 為何，
    都會進入較長的休眠。
    若此值指定時未帶單位，則以毫秒為單位。
    預設值為 200
    毫秒（`200ms`）。請注意，在某些系統上，
    休眠延遲的有效解析度為 10 毫秒；將
    `bgwriter_delay` 設為非 10 的倍數的值，
    可能會產生與設為下一個較高的 10 倍數相同的結果。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。
<a id="GUC-BGWRITER-LRU-MAXPAGES"></a>

`bgwriter_lru_maxpages` (`integer`) <a id="id-1.6.6.7.5.3.2.1.3"></a> [#](#GUC-BGWRITER-LRU-MAXPAGES)
:   在每一輪中，背景寫入程序寫入的緩衝區數量
    不會超過此值。設為零會停用背景
    寫入。（請注意，由另一個獨立、專責的輔助程序
    管理的檢查點不受此影響。）
    預設值為 100 個緩衝區。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-BGWRITER-LRU-MULTIPLIER"></a>

`bgwriter_lru_multiplier` (`floating point`) <a id="id-1.6.6.7.5.3.3.1.3"></a> [#](#GUC-BGWRITER-LRU-MULTIPLIER)
:   每一輪中寫入的髒緩衝區數量，是根據近期各輪中
    伺服器程序所需的新緩衝區數量計算的。近期平均
    需求乘以
    `bgwriter_lru_multiplier`，即可得出對下一輪
    所需緩衝區數量的估計值。髒緩衝區會持續被寫入，
    直到有這麼多乾淨、可重複使用的緩衝區可用為止。
    （不過，每一輪寫入的緩衝區數量不會超過
    `bgwriter_lru_maxpages`。）
    因此，設為 1.0 代表一種「即時（just in time）」的
    策略，只寫入預測所需的確切緩衝區數量。
    較大的值可以為需求的突然增加提供一些緩衝空間，
    較小的值則刻意將寫入工作留給
    伺服器程序處理。
    預設值為 2.0。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-BGWRITER-FLUSH-AFTER"></a>

`bgwriter_flush_after` (`integer`) <a id="id-1.6.6.7.5.3.4.1.3"></a> [#](#GUC-BGWRITER-FLUSH-AFTER)
:   每當背景寫入程序寫入的資料量超過此值時，
    就嘗試強制作業系統將這些寫入發送到底層儲存裝置。
    這樣做可以限制核心分頁快取中的髒資料量，
    降低在檢查點結束時發出 `fsync`，
    或作業系統在背景以較大批次寫回資料時
    發生停頓的可能性。這通常會大幅降低交易延遲，
    但在某些情況下，尤其是工作負載大於
    [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS)、但小於作業系統
    分頁快取的情況下，效能可能會下降。此設定在
    某些平台上可能沒有效果。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    合法範圍介於
    `0`（停用強制寫回）到
    `2MB` 之間。在 Linux 上預設值為 `512kB`，
    其他平台上預設為 `0`。（若 `BLCKSZ`
    不是 8kB，預設值與最大值會依比例縮放。）
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

較小的 `bgwriter_lru_maxpages` 與
`bgwriter_lru_multiplier` 值，可以減少背景寫入程序
造成的額外 I/O 負載，但會使伺服器程序
更有可能必須自行發出寫入，進而延遲互動式
查詢。

<a id="RUNTIME-CONFIG-RESOURCE-IO"></a>

### 19.4.5. I/O [#](#RUNTIME-CONFIG-RESOURCE-IO)

<a id="GUC-BACKEND-FLUSH-AFTER"></a>

`backend_flush_after` (`integer`) <a id="id-1.6.6.7.6.2.1.1.3"></a> [#](#GUC-BACKEND-FLUSH-AFTER)
:   每當單一後端程序（backend）寫入的資料量超過此值時，
    就嘗試強制作業系統將這些寫入發送到底層儲存裝置。
    這樣做可以限制核心分頁快取中的髒資料量，
    降低在檢查點結束時發出 `fsync`，
    或作業系統在背景以較大批次寫回資料時
    發生停頓的可能性。這通常會大幅降低交易延遲，
    但在某些情況下，尤其是工作負載大於
    [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS)、但小於作業系統
    分頁快取的情況下，效能可能會下降。此
    設定在某些平台上可能沒有效果。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    合法範圍介於 `0`（停用強制寫回）
    到 `2MB` 之間。預設值為 `0`，也就是不
    強制寫回。（若 `BLCKSZ` 不是 8kB，
    最大值會依比例縮放。）
<a id="GUC-EFFECTIVE-IO-CONCURRENCY"></a>

`effective_io_concurrency` (`integer`) <a id="id-1.6.6.7.6.2.2.1.3"></a> [#](#GUC-EFFECTIVE-IO-CONCURRENCY)
:   設定 PostgreSQL 預期可以同時執行的
    並行儲存 I/O 操作數量。提高此值，
    會增加任一個個別 PostgreSQL
    工作階段嘗試平行發起的 I/O 操作數量。
    允許的範圍為
    `1` 到 `1000`，或
    `0`（代表停用非同步 I/O 請求的發出）。
    預設值為 `16`。

    較高的值，對於原本會經歷明顯 I/O 停頓的高延遲
    儲存裝置，以及具有高 IOPS 的裝置，會有最大的影響。
    不必要的高值，可能會增加系統上所有查詢的
    I/O 延遲。

    在支援預先擷取建議（prefetch advice）的系統上，
    `effective_io_concurrency` 也控制
    預先擷取的距離。

    可以透過設定同名的表空間參數，
    針對特定表空間中的資料表覆寫此值（參閱
    [ALTER TABLESPACE](../../reference/sql-commands/sql-altertablespace.md)）。
<a id="GUC-MAINTENANCE-IO-CONCURRENCY"></a>

`maintenance_io_concurrency` (`integer`) <a id="id-1.6.6.7.6.2.3.1.3"></a> [#](#GUC-MAINTENANCE-IO-CONCURRENCY)
:   與 `effective_io_concurrency` 類似，
    但用於代表許多用戶端工作階段執行的維護工作。

    預設值為 `16`。可以透過設定同名的
    表空間參數，針對特定表空間中的資料表覆寫此值
    （參閱 [ALTER TABLESPACE](../../reference/sql-commands/sql-altertablespace.md)）。
<a id="GUC-IO-MAX-COMBINE-LIMIT"></a>

`io_max_combine_limit` (`integer`) <a id="id-1.6.6.7.6.2.4.1.3"></a> [#](#GUC-IO-MAX-COMBINE-LIMIT)
:   控制合併 I/O 操作中最大的 I/O 大小，
    並默默限制使用者可設定的參數 `io_combine_limit`。
    此參數只能在伺服器啟動時設定。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    實際可能的最大大小取決於作業系統與區塊
    大小，但在 Unix 上通常為 1MB，在 Windows 上通常為 128kB。
    預設值為 128kB。
<a id="GUC-IO-COMBINE-LIMIT"></a>

`io_combine_limit` (`integer`) <a id="id-1.6.6.7.6.2.5.1.3"></a> [#](#GUC-IO-COMBINE-LIMIT)
:   控制合併 I/O 操作中最大的 I/O 大小。若設定的值
    高於 `io_max_combine_limit` 參數，
    則會默默改用較低的那個值，因此可能需要同時
    提高兩者，才能增加 I/O 大小。
    若此值指定時未帶單位，則以區塊為單位，
    也就是 `BLCKSZ` 位元組，通常為 8kB。
    實際可能的最大大小取決於作業系統與區塊
    大小，但在 Unix 上通常為 1MB，在 Windows 上通常為 128kB。
    預設值為 128kB。
<a id="GUC-IO-MAX-CONCURRENCY"></a>

`io_max_concurrency` (`integer`) <a id="id-1.6.6.7.6.2.6.1.3"></a> [#](#GUC-IO-MAX-CONCURRENCY)
:   控制單一程序可以同時執行的最大 I/O 操作數量。

    預設設定 `-1` 會根據
    [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS) 與最大程序數
    （[max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS)、[autovacuum_worker_slots](runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS)、[max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) 與 [max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS)）
    選擇一個數值，但不會超過
    `64`。

    此參數只能在伺服器啟動時設定。
<a id="GUC-IO-METHOD"></a>

`io_method` (`enum`) <a id="id-1.6.6.7.6.2.7.1.3"></a> [#](#GUC-IO-METHOD)
:   選擇執行非同步 I/O 的方法。
    可能的值有：

    * `worker`（使用工作程序執行非同步 I/O）
    * `io_uring`（使用
      io_uring 執行非同步 I/O，需要以
      [`--with-liburing`](../installation/install-make.md#CONFIGURE-OPTION-WITH-LIBURING) /
      [`-Dliburing`](../installation/install-meson.md#CONFIGURE-WITH-LIBURING-MESON) 建置）
    * `sync`（以同步方式執行可非同步處理的 I/O）

    預設值為 `worker`。

    此參數只能在伺服器啟動時設定。
<a id="GUC-IO-WORKERS"></a>

`io_workers` (`integer`) <a id="id-1.6.6.7.6.2.8.1.3"></a> [#](#GUC-IO-WORKERS)
:   選擇要使用的 I/O 工作程序數量。預設值為
    3。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定。

    僅在 [io_method](runtime-config-resource.md#GUC-IO-METHOD) 設為
    `worker` 時才有效果。

<a id="RUNTIME-CONFIG-RESOURCE-WORKER-PROCESSES"></a>

### 19.4.6. 工作程序 [#](#RUNTIME-CONFIG-RESOURCE-WORKER-PROCESSES)

<a id="GUC-MAX-WORKER-PROCESSES"></a>

`max_worker_processes` (`integer`) <a id="id-1.6.6.7.7.2.1.1.3"></a> [#](#GUC-MAX-WORKER-PROCESSES)
:   設定叢集所能支援的最大背景程序數量。
    此參數只能在伺服器啟動時設定。
    預設值為 8。

    在執行待命伺服器時，你必須將此參數設為與
    主要伺服器相同或更高的值，否則
    待命伺服器中將不允許執行查詢。

    變更此值時，也請一併考慮調整
    [max_parallel_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS)、
    [max_parallel_maintenance_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS) 與
    [max_parallel_workers_per_gather](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER)。
<a id="GUC-MAX-PARALLEL-WORKERS-PER-GATHER"></a>

`max_parallel_workers_per_gather` (`integer`) <a id="id-1.6.6.7.7.2.2.1.3"></a> [#](#GUC-MAX-PARALLEL-WORKERS-PER-GATHER)
:   設定單一 `Gather` 或 `Gather Merge`
    節點可以啟動的最大工作程序數量。
    平行工作程序取自
    [max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) 所建立的程序集區，
    並受 [max_parallel_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS) 限制。
    請注意，實際執行時可能無法取得
    所請求的工作程序數量。若發生此情況，
    計畫將以比預期更少的工作程序執行，這可能
    效率不彰。預設值為 2。將此值設為 0
    會停用平行查詢執行。

    請注意，平行查詢消耗的資源，
    可能遠比非平行查詢多得多，因為每個工作程序
    都是完全獨立的程序，對系統造成的影響，
    大致上與額外的使用者工作階段相當。選擇此設定值時，
    以及設定其他控制資源使用量的設定（例如
    [work_mem](runtime-config-resource.md#GUC-WORK-MEM)）時，都應將此納入考量。
    `work_mem` 等資源上限，是個別套用於
    每個工作程序的，這代表所有程序的總使用量，
    可能遠高於任一單一程序通常的使用量。
    舉例來說，使用 4 個工作程序的平行查詢，
    使用的 CPU 時間、記憶體、I/O 頻寬等，
    可能高達完全不使用工作程序之查詢的 5 倍。

    有關平行查詢的更多資訊，請參閱
    [第 15 章](../../the-sql-language/parallel-query/README.md)。
<a id="GUC-MAX-PARALLEL-MAINTENANCE-WORKERS"></a>

`max_parallel_maintenance_workers` (`integer`) <a id="id-1.6.6.7.7.2.3.1.3"></a> [#](#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS)
:   設定單一公用程式命令可以啟動的最大平行工作程序
    數量。目前，支援使用平行工作程序的公用程式
    命令有：建置 B-tree、
    GIN 或 BRIN 索引時的
    `CREATE INDEX`，以及不含 `FULL`
    選項的 `VACUUM`。平行工作程序取自
    [max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) 所建立的程序集區，
    並受 [max_parallel_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS) 限制。
    請注意，實際執行時可能無法取得所請求的
    工作程序數量。若發生此情況，公用程式操作
    將以比預期更少的工作程序執行。預設值為 2。
    將此值設為 0，會停用公用程式命令使用
    平行工作程序。

    請注意，平行公用程式命令不應該消耗
    遠比等效的非平行操作更多的記憶體。這種
    策略與平行查詢不同，平行查詢的資源上限
    一般是逐工作程序套用的。平行公用程式命令
    會將資源上限
    `maintenance_work_mem`，視為套用於
    整個公用程式命令的上限，而不論
    平行工作程序的數量為何。不過，平行公用程式
    命令仍可能消耗遠多得多的 CPU 資源
    與 I/O 頻寬。
<a id="GUC-MAX-PARALLEL-WORKERS"></a>

`max_parallel_workers` (`integer`) <a id="id-1.6.6.7.7.2.4.1.3"></a> [#](#GUC-MAX-PARALLEL-WORKERS)
:   設定叢集所能支援用於平行操作的最大工作程序
    數量。預設值為 8。提高或降低此值時，
    也請一併考慮調整
    [max_parallel_maintenance_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS) 與
    [max_parallel_workers_per_gather](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER)。
    另請注意，若此值設定得比
    [max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) 更高，將不會有任何
    效果，因為平行工作程序是從該設定所建立的
    工作程序集區中取得的。
<a id="GUC-PARALLEL-LEADER-PARTICIPATION"></a>

`parallel_leader_participation` (`boolean`) <a id="id-1.6.6.7.7.2.5.1.3"></a> [#](#GUC-PARALLEL-LEADER-PARTICIPATION)
:   允許領導者（leader）程序在
    `Gather` 與 `Gather Merge` 節點下
    執行查詢計畫，而不是等待工作程序。預設值為
    `on`。將此值設為 `off`
    可以降低工作程序因為領導者讀取資料列速度不夠快
    而被阻塞的可能性，但需要領導者程序
    等待工作程序啟動，才能產生第一批
    資料列。領導者能夠幫助或妨礙效能的程度，
    取決於計畫類型、工作程序數量以及查詢持續時間。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-resource.html)（原文版本：18.6；核對日期：2026-09-26）
