<a id="APP-PGRECVLOGICAL"></a><a id="id-1.9.4.18.1"></a>

## pg_recvlogical

pg_recvlogical — 控制 PostgreSQL 邏輯解碼串流

<a id="id-1.9.4.18.4"></a>

## 語法

<a id="id-1.9.4.18.4.1"></a>

`pg_recvlogical` [*`option`*...]

<a id="id-1.9.4.18.5"></a>

## 說明

`pg_recvlogical` 控制邏輯解碼複寫插槽，並從這類複寫插槽串流資料。

它會建立複寫模式的連線，因此受到與 [pg_receivewal](app-pgreceivewal.md) 相同的限制，另外還有邏輯複寫的限制（請參閱[第 47 章](../../server-programming/logicaldecoding/README.md)）。

`pg_recvlogical` 沒有與邏輯解碼 SQL 介面之 peek 與 get 模式等效的功能。它會在收到資料時延遲地送出資料的重放確認，並在正常結束時送出。若要檢視插槽上待處理的資料而不消耗它，請使用 [`pg_logical_slot_peek_changes`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-REPLICATION)。

在沒有發生嚴重錯誤的情況下，pg_recvlogical 會持續執行，直到被 SIGINT（**Control**+**C**）或 SIGTERM 訊號終止。

當 pg_recvlogical 收到 SIGHUP 訊號時，它會關閉目前的輸出檔，並以 `--file` 選項指定的檔名開啟新的輸出檔。這讓我們能夠先將目前的檔案重新命名，再對 pg_recvlogical 送出 SIGHUP 訊號，藉此輪替輸出檔。

<a id="id-1.9.4.18.6"></a>

## 選項

必須至少指定下列其中一個選項來選擇動作：

`--create-slot`
:   以 `--slot` 指定的名稱、使用 `--plugin` 指定的輸出外掛程式，為 `--dbname` 指定的資料庫建立新的邏輯複寫插槽。

    此動作必須指定 `--slot` 與 `--dbname`。

    `--enable-two-phase` 與 `--enable-failover` 選項可以與 `--create-slot` 一起指定。

`--drop-slot`
:   移除名稱由 `--slot` 指定的複寫插槽，然後結束。

    此動作必須指定 `--slot`。

`--start`
:   開始從 `--slot` 指定的邏輯複寫插槽串流變更，並持續到被訊號終止為止。若伺服器端的變更串流因伺服器關閉或連線中斷而結束，除非指定了 `--no-loop`，否則會在迴圈中重試。

    此動作必須指定 `--slot`、`--dbname` 與 `--file`。

    串流格式由建立插槽時指定的輸出外掛程式決定。

    連線必須連到建立插槽時所用的同一個資料庫。

`--create-slot` 與 `--start` 可以一起指定。`--drop-slot` 不能與其他動作合併使用。

下列命令列選項控制輸出的位置與格式，以及其他複寫行為：

`-E lsn`<br>`--endpos=lsn`
:   在 `--start` 模式下，當接收到達指定的 LSN 時，自動停止複寫並以正常結束狀態 0 結束。若不是在 `--start` 模式下指定此選項，會引發錯誤。

    若有某筆記錄的 LSN 恰好等於 *`lsn`*，該記錄會被輸出。

    `--endpos` 選項不了解交易邊界，可能會在交易進行到一半時截斷輸出。任何只輸出了一部分的交易都不會被消耗，並會在下次讀取該插槽時再次重放。個別訊息絕不會被截斷。

`--enable-failover`
:   讓插槽能夠同步到待命伺服器。此選項只能與 `--create-slot` 一起指定。

`-f filename`<br>`--file=filename`
:   將接收並解碼後的交易資料寫入此檔案。使用 `-` 表示 stdout。

    使用 `--start` 時必須指定此參數。

`-F interval_seconds`<br>`--fsync-interval=interval_seconds`
:   指定 pg_recvlogical 應該多久發出一次 `fsync()` 呼叫，以確保輸出檔安全地刷寫到磁碟。

    伺服器偶爾會要求用戶端執行刷寫，並將刷寫位置回報給伺服器。此設定是在那之外額外加上的，用來更頻繁地執行刷寫。

    將間隔指定為 `0` 會完全停止發出 `fsync()` 呼叫，但仍會向伺服器回報進度。在此情況下，發生當機時資料可能會遺失。

`-I lsn`<br>`--startpos=lsn`
:   在 `--start` 模式下，從指定的 LSN 開始複寫。關於其效果的詳細資訊，請參閱[第 47 章](../../server-programming/logicaldecoding/README.md)與[第 54.4 節](../../internals/protocol/protocol-replication.md)中的文件。在其他模式下會被忽略。

`--if-not-exists`
:   指定了 `--create-slot` 且已存在指定名稱的插槽時，不擲出錯誤。

`-n`<br>`--no-loop`
:   與伺服器的連線中斷時，不在迴圈中重試，直接結束。

`-o name[=value]`<br>`--option=name[=value]`
:   將選項 *`name`* 傳給輸出外掛程式；若有指定，同時傳入選項值 *`value`*。有哪些選項以及它們的效果，取決於所使用的輸出外掛程式。

`-P plugin`<br>`--plugin=plugin`
:   建立插槽時，使用指定的邏輯解碼輸出外掛程式。請參閱[第 47 章](../../server-programming/logicaldecoding/README.md)。若插槽已存在，此選項沒有作用。

`-s interval_seconds`<br>`--status-interval=interval_seconds`
:   此選項與 [pg_receivewal](app-pgreceivewal.md) 中同名選項的效果相同。請參閱該處的說明。

`-S slot_name`<br>`--slot=slot_name`
:   在 `--start` 模式下，使用名為 *`slot_name`* 的現有邏輯複寫插槽。在 `--create-slot` 模式下，以此名稱建立插槽。在 `--drop-slot` 模式下，刪除具有此名稱的插槽。

    任何動作都必須指定此參數。

`-t`<br>`--enable-two-phase`<br>`--two-phase`（已棄用）
:   啟用預備交易的解碼。此選項只能與 `--create-slot` 一起指定。

`-v`<br>`--verbose`
:   啟用詳細模式。

下列命令列選項控制資料庫連線參數。

`-d dbname`<br>`--dbname=dbname`
:   要連線的資料庫。這在細節上代表什麼，請參閱各動作的說明。*`dbname`* 可以是[連線字串](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNSTRING)。若是如此，連線字串參數會覆寫任何衝突的命令列選項。

    使用 `--create-slot` 與 `--start` 時必須指定此參數。

`-h hostname-or-ip`<br>`--host=hostname-or-ip`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則作為 Unix 網域通訊端的目錄。預設值取自 `PGHOST` 環境變數（若有設定），否則會嘗試使用 Unix 網域通訊端連線。

`-p port`<br>`--port=port`
:   指定伺服器監聽連線的 TCP 連接埠或本機 Unix 網域通訊端檔案副檔名。預設為 `PGPORT` 環境變數（若有設定），或編譯時內建的預設值。

`-U user`<br>`--username=user`
:   要用來連線的使用者名稱。預設為目前的作業系統使用者名稱。

`-w`<br>`--no-password`
:   絕不發出密碼提示。若伺服器要求密碼驗證，而密碼無法透過 `.pgpass` 檔案等其他方式取得，連線嘗試將會失敗。此選項在沒有使用者可輸入密碼的批次作業與指令稿中可能很有用。

`-W`<br>`--password`
:   強制 pg_recvlogical 在連線到資料庫之前提示輸入密碼。

    此選項從來都不是必要的，因為若伺服器要求密碼驗證，pg_recvlogical 會自動提示輸入密碼。不過，pg_recvlogical 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

另外也提供下列選項：

`-V`<br>`--version`
:   印出 pg_recvlogical 版本後結束。

`-?`<br>`--help`
:   顯示 pg_recvlogical 命令列引數的說明後結束。

<a id="id-1.9.4.18.7"></a>

## 結束狀態

pg_recvlogical 被 SIGINT 或 SIGTERM 訊號終止時，會以狀態 0 結束。（這是結束它的正常方式，因此不算錯誤。）發生嚴重錯誤或收到其他訊號時，結束狀態將不為零。

<a id="id-1.9.4.18.8"></a>

## 環境

此工具與大多數其他 PostgreSQL 工具一樣，使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可能的值為 `always`、`auto` 與 `never`。

<a id="id-1.9.4.18.9"></a>

## 注意事項

若來源叢集啟用了群組權限，pg_recvlogical 會保留輸出檔案上的群組權限。

<a id="id-1.9.4.18.10"></a>

## 範例

範例請參閱[第 47.1 節](../../server-programming/logicaldecoding/logicaldecoding-example.md)。

<a id="id-1.9.4.18.11"></a>

## 另請參閱

[pg_receivewal](app-pgreceivewal.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgrecvlogical.html)（原文版本：18.6；核對日期：2026-10-09）
