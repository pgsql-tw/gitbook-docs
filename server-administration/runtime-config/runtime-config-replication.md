<a id="RUNTIME-CONFIG-REPLICATION"></a>

## 19.6. 複寫 [#](#RUNTIME-CONFIG-REPLICATION)

[19.6.1. 傳送端伺服器](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SENDER)

[19.6.2. 主要伺服器](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-PRIMARY)

[19.6.3. 待命伺服器](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY)

[19.6.4. 訂閱端](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SUBSCRIBER)

這些設定控制內建
*串流複寫（streaming replication）*功能（參閱
[26.2.5 節](../high-availability/warm-standby.md#STREAMING-REPLICATION)），以及內建
*邏輯複寫（logical replication）*功能（參閱
[第 29 章](../logical-replication/README.md)）。

對於*串流複寫*而言，伺服器可以是
主要伺服器或待命伺服器。主要伺服器可以傳送資料，而待命伺服器
永遠是被複寫資料的接收端。當使用串接式複寫
（cascading replication，參閱[26.2.7 節](../high-availability/warm-standby.md#CASCADING-REPLICATION)）時，
待命伺服器也可以同時是傳送端與接收端。
這些參數主要用於傳送端與待命伺服器，不過有些
參數僅在主要伺服器上才有意義。如有需要，
整個叢集中的設定值可以不同，不會造成問題。

對於*邏輯複寫*而言，*發布端（publisher）*
（執行 [`CREATE PUBLICATION`](../../reference/sql-commands/sql-createpublication.md) 的伺服器）
會將資料複寫到*訂閱端（subscriber）*
（執行 [`CREATE SUBSCRIPTION`](../../reference/sql-commands/sql-createsubscription.md) 的伺服器）。
伺服器也可以同時身兼發布端與訂閱端。請注意，
以下各節將發布端稱為「傳送端」。有關邏輯複寫組態設定
的更多細節，請參閱
[29.12 節](../logical-replication/logical-replication-config.md)。

<a id="RUNTIME-CONFIG-REPLICATION-SENDER"></a>

### 19.6.1. 傳送端伺服器 [#](#RUNTIME-CONFIG-REPLICATION-SENDER)

這些參數可以在任何要將複寫資料傳送給一個或多個
standby 伺服器的伺服器上設定。
Primary 永遠是傳送端伺服器，因此這些參數必須
永遠在 primary 上設定。
在 standby 成為 primary 之後，這些參數的角色與意義
不會改變。

<a id="GUC-MAX-WAL-SENDERS"></a>

`max_wal_senders` (`integer`) <a id="id-1.6.6.9.5.3.1.1.3"></a> [#](#GUC-MAX-WAL-SENDERS)
:   指定來自 standby 伺服器或串流基礎備份用戶端的
    最大並行連線數（也就是同時執行中的 WAL 傳送程序
    最大數量）。預設值為
    `10`。值為 `0` 代表
    停用複寫功能。串流用戶端的突然斷線，可能會
    留下一個孤兒連線插槽，直到逾時才會釋放，
    因此此參數應設定得比預期的最大用戶端數量
    略高一些，以便斷線的用戶端能夠立即
    重新連線。此參數只能在伺服器啟動時設定。此外，
    必須將 `wal_level` 設為
    `replica` 或更高，才允許來自 standby
    伺服器的連線。

    在執行 standby 伺服器時，你必須將此參數設為與
    primary 伺服器相同或更高的值，否則
    standby 伺服器中將不允許執行查詢。
<a id="GUC-MAX-REPLICATION-SLOTS"></a>

`max_replication_slots` (`integer`) <a id="id-1.6.6.9.5.3.2.1.3"></a> [#](#GUC-MAX-REPLICATION-SLOTS)
:   指定伺服器所能支援的最大複寫插槽
    （replication slot，參閱[26.2.6 節](../high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS)）數量。
    預設值為 10。此參數只能在
    伺服器啟動時設定。
    若設定的值低於目前既有複寫插槽的數量，
    將導致伺服器無法啟動。此外，
    必須將 `wal_level` 設為
    `replica` 或更高，才能使用複寫插槽。
<a id="GUC-OUTPUT-PLUGIN-LIBRARIES"></a>

`output_plugin_libraries` (`string`) <a id="id-1.6.6.9.5.3.3.1.3"></a> [#](#GUC-OUTPUT-PLUGIN-LIBRARIES)
:   列出安裝於 [dynamic_library_path](runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH) 中、
    且同時受信任、可供複寫用戶端作為邏輯輸出外掛程式使用的
    程式庫。任何針對其他程式庫的
    [邏輯解碼](../../server-programming/logicaldecoding/logicaldecoding-example.md)
    或[複寫](../../internals/protocol/protocol-replication.md)請求都會被拒絕。
    所有使用者皆受此限制約束。預設值為
    `'pgoutput, test_decoding'`，這是標準
    PostgreSQL 發行版中所含的兩個邏輯輸出外掛程式。

    格式為以逗號分隔的程式庫名稱清單，每個名稱
    的解讀方式與 [`LOAD`](../../reference/sql-commands/sql-load.md)
    命令相同（但邏輯解碼用戶端必須指定與清單中某一項目
    *完全*相符的外掛程式名稱，
    不能有大小寫或路徑結構上的差異）。項目之間的空白字元
    會被忽略；如果程式庫名稱中需要包含空白字元或
    逗號，請以雙引號括住該名稱。

    確保加入此清單的程式庫在載入伺服器時，不會無意間
    賦予非超級使用者額外的權限，是伺服器管理員的責任。

    ### 注意

    從尚未具備
    `output_plugin_libraries` 參數的版本升級伺服器時，
    以下查詢有助於建立所有永久性邏輯複寫插槽所需的
    外掛程式清單：

    ```

    SELECT DISTINCT plugin FROM pg_replication_slots WHERE plugin IS NOT NULL;
    ```

    在調整
    `output_plugin_libraries` 之前，請仔細檢視此清單以確保安全。

    上述查詢只能顯示過去某個時間點曾成功加入複寫插槽的
    外掛程式。新被拒絕的請求會出現在日誌中，
    訊息類似如下：

    ```

    ERROR:  library "..." may not be used as an output plugin
    DETAIL:  The configuration parameter "output_plugin_libraries" (currently 'pgoutput, test_decoding') does not name this library as a trusted output plugin.
    HINT:  If it is safe for all REPLICATION users to use this library as an output plugin, add it to "output_plugin_libraries" and reload the server configuration.
    ```
<a id="GUC-WAL-KEEP-SIZE"></a>

`wal_keep_size` (`integer`) <a id="id-1.6.6.9.5.3.4.1.3"></a> [#](#GUC-WAL-KEEP-SIZE)
:   指定
    `pg_wal`
    目錄中保留的過往 WAL 檔案最小大小，
    以備 standby 伺服器需要擷取這些檔案以進行串流
    複寫。如果連線到傳送端伺服器的 standby
    伺服器落後超過
    `wal_keep_size` 百萬位元組，傳送端伺服器可能會
    移除該 standby 仍然需要的 WAL 區段，此時
    複寫連線就會被終止。下游連線
    最終也會因此失敗。（不過，如果有使用 WAL
    歸檔，standby 伺服器可以透過從歸檔中擷取該區段來復原。）

    此參數僅設定
    `pg_wal` 中保留區段的最小大小；系統可能需要為 WAL
    歸檔或從檢查點復原而保留更多區段。若
    `wal_keep_size` 為零（預設值），系統
    不會為 standby 保留任何額外區段，因此
    standby 伺服器可用的舊 WAL 區段數量，取決於
    先前檢查點的位置以及 WAL 歸檔的
    狀態。
    若此值指定時未帶單位，則以百萬位元組為單位。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。
<a id="GUC-MAX-SLOT-WAL-KEEP-SIZE"></a>

`max_slot_wal_keep_size` (`integer`) <a id="id-1.6.6.9.5.3.5.1.3"></a> [#](#GUC-MAX-SLOT-WAL-KEEP-SIZE)
:   指定在檢查點時，[複寫
    插槽](../high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS)在
    `pg_wal` 目錄中允許保留的 WAL 檔案最大大小。
    若 `max_slot_wal_keep_size` 為 -1（預設值），
    複寫插槽可保留的 WAL 檔案大小不受限制。否則，如果
    複寫插槽的 restart_lsn 落後目前 LSN 超過指定的大小，
    使用該插槽的 standby 可能因所需 WAL 檔案已被移除，
    而無法繼續複寫。你可以在
    [pg_replication_slots](../../internals/views/view-pg-replication-slots.md) 中檢視複寫插槽的
    WAL 可用性。
    若此值指定時未帶單位，則以百萬位元組為單位。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-IDLE-REPLICATION-SLOT-TIMEOUT"></a>

`idle_replication_slot_timeout` (`integer`) <a id="id-1.6.6.9.5.3.6.1.3"></a> [#](#GUC-IDLE-REPLICATION-SLOT-TIMEOUT)
:   將閒置超過此時間長度（未被
    [複寫連線](../../internals/protocol/protocol-replication.md)使用）的複寫插槽
    設為無效。
    若此值指定時未帶單位，則以秒為單位。
    值為零（預設值）代表停用閒置逾時
    失效機制。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定。

    因閒置逾時而失效的插槽，是在檢查點期間發生的。
    由於檢查點是以
    `checkpoint_timeout` 間隔發生的，
    `idle_replication_slot_timeout` 被超過的時間點，
    與插槽在下一次檢查點被觸發失效的時間點之間，
    可能存在一些延遲。
    為避免這類延遲，使用者可以強制執行檢查點，
    以立即使閒置的插槽失效。插槽閒置時間長度的計算，
    是使用插槽的 [pg_replication_slots](../../internals/views/view-pg-replication-slots.md).`inactive_since`
    值。

    請注意，閒置逾時失效機制不適用於未保留 WAL 的
    插槽，也不適用於 standby 伺服器上正從 primary
    伺服器同步的插槽（也就是
    [pg_replication_slots](../../internals/views/view-pg-replication-slots.md).`synced`
    值為 `true` 的 standby 插槽）。已同步的插槽
    永遠被視為閒置，因為它們並不執行邏輯解碼
    以產生變更。
<a id="GUC-WAL-SENDER-TIMEOUT"></a>

`wal_sender_timeout` (`integer`) <a id="id-1.6.6.9.5.3.7.1.3"></a> [#](#GUC-WAL-SENDER-TIMEOUT)
:   終止閒置時間超過此時間量的複寫連線。
    這對於傳送端伺服器偵測 standby 當機或網路
    中斷很有用。
    若此值指定時未帶單位，則以毫秒為單位。
    預設值為 60 秒。
    值為零則會停用逾時機制。

    對於跨越多個地理位置分散的叢集，
    在不同位置使用不同的值，可以為叢集管理帶來更大的
    彈性。較小的值有助於在 standby 具備低延遲網路
    連線時更快偵測到故障，較大的值則有助於
    在 standby 位於遠端位置、網路延遲較高時，
    更好地判斷該 standby 的健康狀況。
<a id="GUC-TRACK-COMMIT-TIMESTAMP"></a>

`track_commit_timestamp` (`boolean`) <a id="id-1.6.6.9.5.3.8.1.3"></a> [#](#GUC-TRACK-COMMIT-TIMESTAMP)
:   記錄交易的提交時間。
    此參數只能在伺服器啟動時設定。
    預設值為 `off`。

<a id="RUNTIME-CONFIG-REPLICATION-PRIMARY"></a>

### 19.6.2. 主要伺服器 [#](#RUNTIME-CONFIG-REPLICATION-PRIMARY)

這些參數可以在要將複寫資料傳送給一個或多個
standby 伺服器的 primary 伺服器上設定。
請注意，除了這些參數之外，
primary 伺服器上也必須妥善設定
[wal_level](runtime-config-wal.md#GUC-WAL-LEVEL)，並可選擇性啟用 WAL
歸檔（參閱[19.5.3 節](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVING)）。
這些參數在 standby 伺服器上的值無關緊要，
不過你可能會想要先在那裡設定好，
以備 standby 日後成為 primary 之用。

<a id="GUC-SYNCHRONOUS-STANDBY-NAMES"></a>

`synchronous_standby_names` (`string`) <a id="id-1.6.6.9.6.3.1.1.3"></a> [#](#GUC-SYNCHRONOUS-STANDBY-NAMES)
:   指定一份可以支援*同步複寫（synchronous
    replication）*的 standby 伺服器清單，如
    [26.2.8 節](../high-availability/warm-standby.md#SYNCHRONOUS-REPLICATION)所述。
    會有一個或多個作用中的同步 standby；
    等待提交的交易，會在這些 standby 伺服器
    確認收到其資料之後才被允許繼續進行。
    同步 standby 將是那些名稱出現在
    此清單中，且目前既已連線，又以即時方式串流資料的
    伺服器（如
    [`pg_stat_replication`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW) 檢視表中
    狀態為 `streaming` 所示）。
    指定多個同步 standby，可以達成非常高的可用性
    並防止資料遺失。

    此處 standby 伺服器的名稱，是 standby 連線資訊中
    設定的 `application_name` 值。若是
    實體複寫 standby，此值應在
    `primary_conninfo` 設定中設定；預設值
    為 [cluster_name](runtime-config-logging.md#GUC-CLUSTER-NAME) 的設定值
    （若有設定），否則為 `walreceiver`。
    對於邏輯複寫，此值可以在訂閱的連線
    資訊中設定，預設為訂閱
    名稱。對於其他複寫串流消費者，
    請參閱其各自的文件。

    此參數使用以下任一語法指定一份 standby
    伺服器清單：

    ```

    [FIRST] num_sync ( standby_name [, ...] )
    ANY num_sync ( standby_name [, ...] )
    standby_name [, ...]
    ```

    其中 *`num_sync`* 是
    交易需要等待回覆的同步 standby
    數量，
    *`standby_name`*
    則是 standby 伺服器的名稱。
    *`num_sync`*
    必須是大於零的整數值。
    `FIRST` 與 `ANY` 指定從所列伺服器中
    選擇同步 standby 的方式。

    關鍵字 `FIRST` 搭配
    *`num_sync`*，指定一種基於優先順序的
    同步複寫，會讓交易提交等待，直到其 WAL 記錄
    被複寫到根據優先順序選出的
    *`num_sync`* 個同步
    standby 為止。舉例來說，設為
    `FIRST 3 (s1, s2, s3, s4)` 會使每次提交都
    等待從 `s1`、`s2`、`s3` 與 `s4`
    中選出的三個優先順序較高的 standby 回覆。
    在清單中名稱較早出現的 standby，會被賦予較高的
    優先順序，並被視為同步 standby。此清單中稍後
    出現的其他 standby 伺服器，則代表潛在的同步 standby。
    如果目前任何一個同步 standby 因任何原因斷線，
    會立即由下一個優先順序最高的 standby 取代。
    關鍵字 `FIRST` 是選擇性的。

    關鍵字 `ANY` 搭配
    *`num_sync`*，指定一種基於法定人數（quorum）的
    同步複寫，會讓交易提交等待，直到其 WAL 記錄
    被複寫到*至少*
    *`num_sync`* 個列出的 standby
    為止。舉例來說，設為
    `ANY 3 (s1, s2, s3, s4)` 會使每次提交
    在 `s1`、`s2`、`s3` 與 `s4`
    中，只要任意三個 standby 回覆，就繼續進行。

    `FIRST` 與 `ANY` 不區分大小寫。若這些
    關鍵字被用作 standby 伺服器的名稱，
    則其 *`standby_name`* 必須
    以雙引號括住。

    第三種語法是在 PostgreSQL
    9.6 版之前使用的，目前仍受支援。此語法
    等同於第一種語法，並將 `FIRST` 與
    *`num_sync`* 設為 1。
    舉例來說，`FIRST 1 (s1, s2)` 與 `s1, s2`
    意義相同：無論選擇 `s1` 或 `s2`，
    都會作為同步 standby。

    特殊項目 `*` 可以比對任何 standby 名稱。

    目前沒有任何機制可以強制 standby 名稱唯一。若有
    重複的情況，其中一個符合的 standby 會被視為較高
    優先順序，但具體是哪一個則不確定。

    ### 注意

    每個 *`standby_name`*
    都應具有合法 SQL 識別字的形式，除非
    它是 `*`。如有需要，你可以使用雙引號。不過請注意，
    *`standby_name`* 在與 standby
    的 application name 比對時，無論是否加上雙引號，
    都是不區分大小寫的。

    如果此處未指定任何同步 standby 名稱，則不會啟用
    同步複寫，交易提交也不會等待複寫。這是
    預設組態設定。即使啟用了同步複寫，
    個別交易仍然可以透過將
    [synchronous_commit](runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT) 參數設為
    `local` 或 `off`，設定為不等待複寫。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-SYNCHRONIZED-STANDBY-SLOTS"></a>

`synchronized_standby_slots` (`string`) <a id="id-1.6.6.9.6.3.2.1.3"></a> [#](#GUC-SYNCHRONIZED-STANDBY-SLOTS)
:   一份以逗號分隔的串流複寫 standby 伺服器插槽名稱清單，
    邏輯 WAL 傳送程序會等待這些插槽。只有在指定的
    複寫插槽確認收到 WAL 之後，邏輯 WAL 傳送程序才會將
    解碼後的變更傳送給外掛程式。這可確保邏輯複寫
    容錯移轉（failover）插槽，不會在對應實體 standby
    收到並刷寫這些變更之前，就先消耗這些變更。如果
    邏輯複寫連線預定在 standby 被提升後，切換到
    該實體 standby，則應在此處列出該 standby 的
    實體複寫插槽。請注意，若
    `synchronized_standby_slots` 中指定的插槽
    不存在或已失效，邏輯複寫將無法繼續進行。
    此外，複寫管理函式
    [`pg_replication_slot_advance`](../../the-sql-language/functions/functions-admin.md#PG-REPLICATION-SLOT-ADVANCE)、
    [`pg_logical_slot_get_changes`](../../the-sql-language/functions/functions-admin.md#PG-LOGICAL-SLOT-GET-CHANGES) 與
    [`pg_logical_slot_peek_changes`](../../the-sql-language/functions/functions-admin.md#PG-LOGICAL-SLOT-PEEK-CHANGES)，
    在搭配邏輯容錯移轉插槽使用時，會阻塞，
    直到 `synchronized_standby_slots` 中指定的所有
    實體插槽都確認收到 WAL 為止。

    對應 `synchronized_standby_slots` 中實體複寫插槽的
    standby，必須設定
    `sync_replication_slots = true`，才能從
    primary 接收邏輯容錯移轉插槽的變更。

<a id="RUNTIME-CONFIG-REPLICATION-STANDBY"></a>

### 19.6.3. 待命伺服器 [#](#RUNTIME-CONFIG-REPLICATION-STANDBY)

這些設定控制要接收複寫資料的
[standby 伺服器](../high-availability/warm-standby.md#STANDBY-SERVER-OPERATION)
的行為。它們在 primary 伺服器上的值無關緊要。

<a id="GUC-PRIMARY-CONNINFO"></a>

`primary_conninfo` (`string`) <a id="id-1.6.6.9.7.3.1.1.3"></a> [#](#GUC-PRIMARY-CONNINFO)
:   指定 standby 伺服器用來連線到傳送端伺服器的
    連線字串。此字串的格式如
    [32.1.1 節](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNSTRING)所述。若此字串中
    未指定某個選項，則會檢查對應的環境
    變數（參閱[32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。如果
    也未設定該環境變數，則會使用
    預設值。

    此連線字串應指定傳送端伺服器的主機名稱
    （或位址），以及埠號（若與 standby 伺服器的
    預設值不同）。
    也應指定傳送端伺服器上一個具備適當權限的角色所對應的
    使用者名稱（參閱
    [26.2.5.1 節](../high-availability/warm-standby.md#STREAMING-REPLICATION-AUTHENTICATION)）。
    如果傳送端要求密碼驗證，也需要提供密碼。
    密碼可以寫在
    `primary_conninfo` 字串中，或寫在 standby 伺服器上
    一個獨立的
    `~/.pgpass` 檔案中（資料庫名稱請使用
    `replication`）。

    對於複寫插槽同步（參閱
    [47.2.3 節](../../server-programming/logicaldecoding/logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)），
    也需要在 `primary_conninfo` 字串中指定
    合法的 `dbname`。此值僅用於
    插槽同步，串流時會被忽略。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    如果 WAL 接收程序正在執行時變更了此參數，
    該程序會收到訊號並關閉，預期會以新設定
    重新啟動（除非
    `primary_conninfo` 為空字串）。
    如果伺服器不在 standby 模式，此設定沒有效果。
<a id="GUC-PRIMARY-SLOT-NAME"></a>

`primary_slot_name` (`string`) <a id="id-1.6.6.9.7.3.2.1.3"></a> [#](#GUC-PRIMARY-SLOT-NAME)
:   選擇性指定一個既有的複寫插槽，在透過串流複寫連線到
    傳送端伺服器時使用，以控制上游節點的資源
    移除（參閱[26.2.6 節](../high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS)）。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    如果 WAL 接收程序正在執行時變更了此參數，
    該程序會收到訊號並關閉，預期會以新設定
    重新啟動。
    如果未設定 `primary_conninfo`，或伺服器不在
    standby 模式，此設定沒有效果。
<a id="GUC-HOT-STANDBY"></a>

`hot_standby` (`boolean`) <a id="id-1.6.6.9.7.3.3.1.3"></a> [#](#GUC-HOT-STANDBY)
:   指定是否可以在復原期間連線並執行查詢，
    如[26.4 節](../high-availability/hot-standby.md)所述。
    預設值為 `on`。
    此參數只能在伺服器啟動時設定。此參數僅在
    歸檔復原期間或 standby 模式下有效果。
<a id="GUC-MAX-STANDBY-ARCHIVE-DELAY"></a>

`max_standby_archive_delay` (`integer`) <a id="id-1.6.6.9.7.3.4.1.3"></a> [#](#GUC-MAX-STANDBY-ARCHIVE-DELAY)
:   當 hot standby 為作用中狀態時，此參數決定
    standby 伺服器在取消與即將套用的 WAL 項目
    衝突的 standby 查詢之前，應等待多久，如
    [26.4.2 節](../high-availability/hot-standby.md#HOT-STANDBY-CONFLICT)所述。
    `max_standby_archive_delay` 適用於正從 WAL 歸檔
    讀取 WAL 資料（因此並非最新資料）的情況。
    若此值指定時未帶單位，則以毫秒為單位。
    預設值為 30 秒。
    值為 -1 則允許 standby 永遠等待衝突的
    查詢完成。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

    請注意，`max_standby_archive_delay` 與查詢在被取消前
    可執行的最長時間並不相同；它是套用任一個 WAL 區段
    資料所允許的最長總時間。因此，如果某個查詢在
    WAL 區段較早的部分已造成顯著延遲，後續發生衝突的
    查詢，寬限時間就會少得多。
<a id="GUC-MAX-STANDBY-STREAMING-DELAY"></a>

`max_standby_streaming_delay` (`integer`) <a id="id-1.6.6.9.7.3.5.1.3"></a> [#](#GUC-MAX-STANDBY-STREAMING-DELAY)
:   當 hot standby 為作用中狀態時，此參數決定
    standby 伺服器在取消與即將套用的 WAL 項目
    衝突的 standby 查詢之前，應等待多久，如
    [26.4.2 節](../high-availability/hot-standby.md#HOT-STANDBY-CONFLICT)所述。
    `max_standby_streaming_delay` 適用於正透過串流複寫
    接收 WAL 資料的情況。
    若此值指定時未帶單位，則以毫秒為單位。
    預設值為 30 秒。
    值為 -1 則允許 standby 永遠等待衝突的
    查詢完成。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

    請注意，`max_standby_streaming_delay` 與查詢在被取消前
    可執行的最長時間並不相同；它是自從 WAL 資料
    從 primary 伺服器收到之後，套用該資料所允許的
    最長總時間。因此，如果某個查詢已造成顯著延遲，
    在 standby 伺服器再次趕上進度之前，後續發生衝突的
    查詢，寬限時間就會少得多。
<a id="GUC-WAL-RECEIVER-CREATE-TEMP-SLOT"></a>

`wal_receiver_create_temp_slot` (`boolean`) <a id="id-1.6.6.9.7.3.6.1.3"></a> [#](#GUC-WAL-RECEIVER-CREATE-TEMP-SLOT)
:   指定在未設定要使用的永久複寫插槽時
    （透過 [primary_slot_name](runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME) 設定），
    WAL 接收程序是否應該在遠端實例上建立一個臨時複寫插槽。
    預設值為關閉。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。
    如果 WAL 接收程序正在執行時變更了此參數，
    該程序會收到訊號並關閉，預期會以
    新設定重新啟動。
<a id="GUC-WAL-RECEIVER-STATUS-INTERVAL"></a>

`wal_receiver_status_interval` (`integer`) <a id="id-1.6.6.9.7.3.7.1.3"></a> [#](#GUC-WAL-RECEIVER-STATUS-INTERVAL)
:   指定 standby 上的 WAL 接收程序向 primary 或上游
    standby 傳送複寫進度資訊的最小頻率，
    可以透過
    [`pg_stat_replication`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW)
    檢視表查看此資訊。standby 會回報
    最後寫入的預寫日誌位置、最後刷寫到磁碟的位置，
    以及最後套用的位置。
    此參數的值是各次回報之間的最長時間間隔。
    每當寫入或刷寫位置發生變化時，就會傳送更新，
    若設為非零值，則至少會依此參數指定的頻率傳送。
    另有一些情況會不理會此參數而傳送更新，
    例如既有 WAL 處理完畢時，或
    `synchronous_commit` 設為
    `remote_apply` 時。
    因此，套用位置可能會稍微落後於真正的位置。
    若此值指定時未帶單位，則以秒為單位。
    預設值為 10 秒。此參數只能在
    `postgresql.conf` 檔案中或伺服器
    命令列上設定。
<a id="GUC-HOT-STANDBY-FEEDBACK"></a>

`hot_standby_feedback` (`boolean`) <a id="id-1.6.6.9.7.3.8.1.3"></a> [#](#GUC-HOT-STANDBY-FEEDBACK)
:   指定 hot standby 是否應該向 primary 或上游 standby
    傳送有關目前在 standby 上執行之查詢的回饋資訊。
    此參數可用於消除因清理記錄而導致的查詢取消，
    但對某些工作負載而言，可能導致 primary 上的資料庫
    膨脹。回饋訊息傳送的頻率
    不會超過每
    `wal_receiver_status_interval` 一次。預設值為
    `off`。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。

    若正在使用串接式複寫，回饋會向上傳遞，
    直到最終到達 primary。Standby 除了向上傳遞外，
    不會對收到的回饋做其他用途。

    請注意，如果 standby 上的時鐘被調快或調慢，
    回饋訊息可能無法依所需間隔傳送。在
    極端情況下，由於回饋機制是以時間戳記為基礎，
    這可能導致 primary 長時間無法移除死亡資料列的風險
    延長。
<a id="GUC-WAL-RECEIVER-TIMEOUT"></a>

`wal_receiver_timeout` (`integer`) <a id="id-1.6.6.9.7.3.9.1.3"></a> [#](#GUC-WAL-RECEIVER-TIMEOUT)
:   終止閒置時間超過此時間量的複寫連線。
    這對於接收端 standby 伺服器偵測 primary 節點當機
    或網路中斷很有用。
    若此值指定時未帶單位，則以毫秒為單位。
    預設值為 60 秒。
    值為零則會停用逾時機制。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器
    命令列上設定。
<a id="GUC-WAL-RETRIEVE-RETRY-INTERVAL"></a>

`wal_retrieve_retry_interval` (`integer`) <a id="id-1.6.6.9.7.3.10.1.3"></a> [#](#GUC-WAL-RETRIEVE-RETRY-INTERVAL)
:   指定在任何來源（串流複寫、本機
    `pg_wal` 或 WAL 歸檔）皆無法取得 WAL 資料時，
    standby 伺服器在再次嘗試擷取 WAL 資料之前
    應等待多久。
    若此值指定時未帶單位，則以毫秒為單位。
    預設值為 5 秒。
    此參數只能在
    `postgresql.conf` 檔案中或伺服器
    命令列上設定。

    此參數適用於正在復原的節點需要控制等待新 WAL
    資料可用之時間量的組態設定情境。舉例來說，在
    歸檔復原中，可以透過降低此參數的值，
    讓偵測新 WAL 檔案的復原程序更快反應。
    在 WAL 活動較低的系統上，提高此值可以減少
    存取 WAL 歸檔所需的請求數量，這在
    例如雲端環境中很有用，因為那類環境會將
    基礎架構被存取的次數納入考量。

    在邏輯複寫中，此參數也限制了失敗的複寫套用
    工作程序或資料表同步工作程序重新啟動的頻率。
<a id="GUC-RECOVERY-MIN-APPLY-DELAY"></a>

`recovery_min_apply_delay` (`integer`) <a id="id-1.6.6.9.7.3.11.1.3"></a> [#](#GUC-RECOVERY-MIN-APPLY-DELAY)
:   根據預設，standby 伺服器會盡快從傳送端伺服器
    復原 WAL 記錄。擁有延遲一段時間的資料副本
    可能很有用，可以提供機會修正資料遺失錯誤。
    此參數讓你可以將復原延遲指定的時間量。舉例來說，
    如果你將此參數設為 `5min`，standby
    只會在 standby 上的系統時間比 primary 回報的提交時間
    晚至少五分鐘時，才重播各筆交易提交。
    若此值指定時未帶單位，則以毫秒為單位。
    預設值為零，代表不加上任何延遲。

    伺服器之間的複寫延遲有可能超過此參數的值，
    此時就不會再加上額外延遲。
    請注意，此延遲是根據 primary 上寫入的 WAL 時間戳記，
    與 standby 上目前時間之間的差計算的。由於網路延遲
    或串接式複寫組態設定造成的傳輸延遲，
    可能會顯著縮短實際等待時間。如果 primary 與
    standby 上的系統時鐘未同步，這可能導致
    復原程序比預期更早套用記錄；但這並非
    重大問題，因為此參數的有用設定值，通常遠大於
    伺服器之間常見的時間偏差。

    此延遲僅適用於交易提交的 WAL 記錄。
    其他記錄會盡快重播，這並不會造成問題，
    因為 MVCC 可見性規則會確保這些變更的效果，
    在對應的提交記錄被套用之前並不會顯示。

    此延遲會在正在復原的資料庫達到一致狀態之後開始，
    持續到 standby 被提升或觸發為止。在此之後，
    standby 會結束復原，不再等待。

    WAL 記錄必須保留在 standby 上，直到準備好被
    套用為止。因此，延遲越長，累積的 WAL 檔案
    就會越多，這會增加 standby 的
    `pg_wal` 目錄所需的磁碟空間。

    此參數是為串流複寫部署所設計的；
    不過，若有指定此參數，除了當機復原之外，
    在所有情況下都會被遵循。
    使用此功能會延遲 `hot_standby_feedback`，
    這可能導致 primary 上的膨脹；請謹慎搭配兩者使用。

    ### 警告

    當 `synchronous_commit` 設為
    `remote_apply` 時，此設定會影響同步複寫；
    每次 `COMMIT` 都需要等待套用完成。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-SYNC-REPLICATION-SLOTS"></a>

`sync_replication_slots` (`boolean`) <a id="id-1.6.6.9.7.3.12.1.3"></a> [#](#GUC-SYNC-REPLICATION-SLOTS)
:   啟用此設定，可讓實體 standby 從 primary 伺服器
    同步邏輯容錯移轉插槽，使邏輯訂閱端能夠在
    容錯移轉後，從新的 primary 伺服器繼續複寫。

    此設定預設為停用。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令列上設定。

<a id="RUNTIME-CONFIG-REPLICATION-SUBSCRIBER"></a>

### 19.6.4. 訂閱端 [#](#RUNTIME-CONFIG-REPLICATION-SUBSCRIBER)

這些設定控制邏輯複寫訂閱端的行為。
它們在發布端上的值無關緊要。
詳情請參閱[29.12 節](../logical-replication/logical-replication-config.md)。

<a id="GUC-MAX-ACTIVE-REPLICATION-ORIGINS"></a>

`max_active_replication_origins` (`integer`) <a id="id-1.6.6.9.8.3.1.1.3"></a> [#](#GUC-MAX-ACTIVE-REPLICATION-ORIGINS)
:   指定可以同時追蹤多少個複寫來源（replication origin，參閱
    [第 48 章](../../server-programming/replication-origins/README.md)），
    這實質上限制了伺服器上可以建立的邏輯複寫訂閱
    數量。若設定的值低於目前追蹤中的複寫來源數量
    （反映在
    [pg_replication_origin_status](../../internals/views/view-pg-replication-origin-status.md) 中），
    將導致伺服器無法啟動。預設值為 10。此參數
    只能在伺服器啟動時設定。
    `max_active_replication_origins` 必須至少設為
    訂閱端將新增的訂閱數量，再加上一些
    供資料表同步使用的保留額度。
<a id="GUC-MAX-LOGICAL-REPLICATION-WORKERS"></a>

`max_logical_replication_workers` (`integer`) <a id="id-1.6.6.9.8.3.2.1.3"></a> [#](#GUC-MAX-LOGICAL-REPLICATION-WORKERS)
:   指定邏輯複寫工作程序的最大數量。這包括
    領導者（leader）套用工作程序、平行套用工作程序，以及
    資料表同步工作程序。

    邏輯複寫工作程序取自
    `max_worker_processes` 所定義的集區。

    預設值為 4。此參數只能在伺服器
    啟動時設定。
<a id="GUC-MAX-SYNC-WORKERS-PER-SUBSCRIPTION"></a>

`max_sync_workers_per_subscription` (`integer`) <a id="id-1.6.6.9.8.3.3.1.3"></a> [#](#GUC-MAX-SYNC-WORKERS-PER-SUBSCRIPTION)
:   每個訂閱的最大同步工作程序數量。此
    參數控制訂閱初始化期間，或新增資料表時，
    初始資料複製的平行處理程度。

    目前，每個資料表只能有一個同步工作程序。

    同步工作程序取自
    `max_logical_replication_workers` 所定義的集區。

    預設值為 2。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定。
<a id="GUC-MAX-PARALLEL-APPLY-WORKERS-PER-SUBSCRIPTION"></a>

`max_parallel_apply_workers_per_subscription` (`integer`) <a id="id-1.6.6.9.8.3.4.1.3"></a> [#](#GUC-MAX-PARALLEL-APPLY-WORKERS-PER-SUBSCRIPTION)
:   每個訂閱的最大平行套用工作程序數量。此
    參數控制對於帶有訂閱參數
    `streaming = parallel` 之進行中交易，
    串流處理的平行程度。

    平行套用工作程序取自
    `max_logical_replication_workers` 所定義的集區。

    預設值為 2。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-replication.html)（原文版本：18.6；核對日期：2026-09-26）
