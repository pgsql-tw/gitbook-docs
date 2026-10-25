<a id="APP-PGRECEIVEWAL"></a><a id="id-1.9.4.17.1"></a>

## pg_receivewal

pg_receivewal — 從 PostgreSQL 伺服器串流接收預寫式日誌

## 語法

<a id="id-1.9.4.17.4.1"></a>

`pg_receivewal` [*`option`*...]

<a id="id-1.9.4.17.5"></a>

## 說明

pg_receivewal 用來從執行中的 PostgreSQL 叢集串流接收預寫式日誌。預寫式日誌會使用串流複寫協定進行串流，並寫入本機目錄中的檔案。這個目錄可以作為使用時間點復原進行還原時的封存位置（請參閱[第 25.3 節](../../server-administration/backup/continuous-archiving.md)）。

pg_receivewal 會在預寫式日誌於伺服器上產生的同時即時串流接收，而不像 [archive_command](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-COMMAND) 與 [archive_library](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) 那樣等待區段完成。因此，使用 pg_receivewal 時，不需要設定 [archive_timeout](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-TIMEOUT)。

與 PostgreSQL 待命伺服器的 WAL 接收器不同，pg_receivewal 預設只在 WAL 檔案關閉時才排清（flush）WAL 資料。若要即時排清 WAL 資料，必須指定 `--synchronous` 選項。由於 pg_receivewal 不會套用 WAL，當 [synchronous_commit](../../server-administration/runtime-config/runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT) 等於 `remote_apply` 時，你不應該讓它成為同步待命伺服器。若它成為同步待命伺服器，它看起來會像是一台永遠追不上的待命伺服器，並導致交易提交被阻擋。為了避免這種情況，你應該為 [synchronous_standby_names](../../server-administration/runtime-config/runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES) 設定適當的值，或為 pg_receivewal 指定一個與它不相符的 `application_name`，或將 `synchronous_commit` 的值變更為 `remote_apply` 以外的值。

預寫式日誌是透過一般的 PostgreSQL 連線串流傳送，並使用複寫協定。連線必須以具有 `REPLICATION` 權限的使用者（請參閱[第 21.2 節](../../server-administration/user-manag/role-attributes.md)）或超級使用者建立，而且 `pg_hba.conf` 必須允許該複寫連線。伺服器也必須將 [max_wal_senders](../../server-administration/runtime-config/runtime-config-replication.md#GUC-MAX-WAL-SENDERS) 設定得夠高，以便為此串流保留至少一個可用的工作階段。

預寫式日誌串流的起始點會在 pg_receivewal 啟動時計算：

1. 首先，掃描寫入 WAL 區段檔案的目錄，找出最新的已完成區段檔案，並以下一個 WAL 區段檔案的開頭作為起始點。
2. 若無法以前一種方法計算出起始點，且有使用複寫插槽，則會額外發出 `READ_REPLICATION_SLOT` 命令，取得該插槽的 `restart_lsn` 作為起始點。只有在從 PostgreSQL 15 及以上版本串流接收預寫式日誌時，才能使用此選項。
3. 若無法以前一種方法計算出起始點，則會使用伺服器在 `IDENTIFY_SYSTEM` 命令中回報的最新 WAL 排清位置。

若連線因非致命錯誤而中斷，或因非致命錯誤而無法在一開始建立，pg_receivewal 會無限次地重試連線，並盡快重新建立串流。若要避免此行為，請使用 `-n` 參數。

在沒有發生致命錯誤的情況下，pg_receivewal 會一直執行，直到被 SIGINT（**Control**+**C**）或 SIGTERM 訊號終止為止。

<a id="id-1.9.4.17.6"></a>

## 選項

`-D directory`<br>`--directory=directory`
:   寫入輸出的目錄。

    此參數為必要。

`-E lsn`<br>`--endpos=lsn`
:   當接收到達指定的 LSN 時，自動停止複寫並以正常的結束狀態 0 結束。

    若有某筆紀錄的 LSN 恰好等於 *`lsn`*，該紀錄會被處理。

`--if-not-exists`
:   指定了 `--create-slot` 且已存在具有指定名稱的插槽時，不要報錯。

`-n`<br>`--no-loop`
:   發生連線錯誤時不要重複嘗試，而是立即以錯誤結束。

`--no-sync`
:   此選項會讓 `pg_receivewal` 不強制將 WAL 資料排清到磁碟。這樣比較快，但也表示之後若作業系統當機，可能會使 WAL 區段損毀。一般而言，此選項適用於測試，但在正式環境部署中進行 WAL 封存時不應該使用。

    此選項與 `--synchronous` 不相容。

`-s interval`<br>`--status-interval=interval`
:   指定傳回伺服器之狀態封包間隔的秒數。這讓伺服器端更容易監控進度。值為零時會完全停用定期狀態更新，不過伺服器要求時仍會傳送更新，以避免逾時斷線。預設值為 10 秒。

`-S slotname`<br>`--slot=slotname`
:   要求 pg_receivewal 使用現有的複寫插槽（請參閱[第 26.2.6 節](../../server-administration/high-availability/warm-standby.md#STREAMING-REPLICATION-SLOTS)）。使用此選項時，pg_receivewal 會向伺服器回報排清位置，指出每個區段何時已同步到磁碟，讓伺服器在該區段沒有其他用途時可以將其移除。

    當 pg_receivewal 的複寫用戶端在伺服器上被設定為同步待命伺服器時，使用複寫插槽會向伺服器回報排清位置，但只在 WAL 檔案關閉時才回報。因此，這種設定會導致主要伺服器上的交易等待很長的時間，實際上無法令人滿意地運作。必須另外指定 `--synchronous` 選項（見下文），才能使其正確運作。

`--synchronous`
:   在收到 WAL 資料後立即將其排清到磁碟。此外，在排清之後也會立即傳回狀態封包給伺服器，而不受 `--status-interval` 影響。

    若 pg_receivewal 的複寫用戶端在伺服器上被設定為同步待命伺服器，應該指定此選項，以確保能及時將回饋傳送給伺服器。

`-v`<br>`--verbose`
:   啟用詳細模式。

`-Z level`<br>`-Z method[:detail]`<br>`--compress=level`<br>`--compress=method[:detail]`
:   啟用預寫式日誌的壓縮。

    壓縮方法可以設定為 `gzip`、`lz4`（若 PostgreSQL 編譯時使用了 `--with-lz4`），或設定為 `none` 表示不壓縮。可以選擇指定壓縮細節字串。若細節字串是整數，它指定的是壓縮等級。否則，它應該是以逗號分隔的項目清單，每個項目的形式為 *`keyword`* 或 *`keyword=value`*。目前唯一支援的關鍵字是 `level`。

    若未指定壓縮等級，將使用預設的壓縮等級。若只指定了等級而沒有提及演算法，則等級大於 0 時會使用 `gzip` 壓縮，等級為 0 時則不壓縮。

    使用 `gzip` 時，所有檔名都會自動加上後綴 `.gz`；使用 `lz4` 時，則會加上後綴 `.lz4`。

下列命令列選項用來控制資料庫連線參數。

`-d connstr`<br>`--dbname=connstr`
:   以[連線字串](../../client-interfaces/libpq/libpq-connstring.md#libpq-connstring)的形式指定用來連線到伺服器的參數；這些參數會覆寫任何衝突的命令列選項。

    此選項稱為 `--dbname`，是為了與其他用戶端應用程式保持一致，但由於 pg_receivewal 並不會連線到叢集中的任何特定資料庫，連線字串中包含的任何資料庫名稱都會被伺服器忽略。不過，以這種方式提供的資料庫名稱，在 `~/.pgpass` 中查找複寫連線的密碼時，會覆寫預設的資料庫名稱（`replication`）。同樣地，連線到 PostgreSQL 時所使用的中介軟體或代理伺服器，也可能將此名稱用於連線路由等目的。

`-h host`<br>`--host=host`
:   指定伺服器所在機器的主機名稱。若值以斜線開頭，則會作為 Unix 網域通訊端的目錄。預設值取自環境變數 `PGHOST`（若有設定），否則會嘗試以 Unix 網域通訊端連線。

`-p port`<br>`--port=port`
:   指定伺服器用來接聽連線的 TCP 連接埠或本機 Unix 網域通訊端檔案副檔名。預設為環境變數 `PGPORT`（若有設定），否則為編譯時內建的預設值。

`-U username`<br>`--username=username`
:   用來連線的使用者名稱。

`-w`<br>`--no-password`
:   永遠不發出密碼提示。若伺服器要求密碼驗證，而又無法透過其他方式（例如 `.pgpass` 檔案）取得密碼，連線嘗試就會失敗。此選項在沒有使用者在場輸入密碼的批次作業與指令稿中可能很有用。

`-W`<br>`--password`
:   強制 pg_receivewal 在連線到資料庫之前提示輸入密碼。

    此選項從來都不是必要的，因為若伺服器要求密碼驗證，pg_receivewal 會自動提示輸入密碼。不過，pg_receivewal 會浪費一次連線嘗試來得知伺服器需要密碼。在某些情況下，值得輸入 `-W` 以避免額外的連線嘗試。

pg_receivewal 可以執行下列兩種動作之一，以控制實體複寫插槽：

`--create-slot`
:   以 `--slot` 中指定的名稱建立新的實體複寫插槽，然後結束。

`--drop-slot`
:   移除以 `--slot` 中指定之名稱的複寫插槽，然後結束。

另外還有其他選項可用：

`-V`<br>`--version`
:   印出 pg_receivewal 的版本後結束。

`-?`<br>`--help`
:   顯示 pg_receivewal 命令列引數的說明後結束。

<a id="id-1.9.4.17.7"></a>

## 結束狀態

pg_receivewal 被 SIGINT 或 SIGTERM 訊號終止時，會以狀態 0 結束。（這是結束它的正常方式，因此不算錯誤。）若發生致命錯誤或收到其他訊號，結束狀態會是非零。

<a id="id-1.9.4.17.8"></a>

## 環境

此工具與大多數其他 PostgreSQL 工具一樣，會使用 libpq 所支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定診斷訊息是否使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.9.4.17.9"></a>

## 注意事項

使用 pg_receivewal 取代 [archive_command](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-COMMAND) 或 [archive_library](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) 作為主要的 WAL 備份方法時，強烈建議使用複寫插槽。否則，伺服器可以在預寫式日誌檔案備份之前就自由地回收或移除它們，因為伺服器無論從 [archive_command](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-COMMAND)、[archive_library](../../server-administration/runtime-config/runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) 或複寫插槽，都沒有任何關於 WAL 串流已封存到什麼程度的資訊。不過請注意，若接收端跟不上擷取 WAL 資料的速度，複寫插槽會佔滿伺服器的磁碟空間。

若來源叢集啟用了群組權限，pg_receivewal 會在接收到的 WAL 檔案上保留群組權限。

<a id="id-1.9.4.17.10"></a>

## 範例

從位於 `mydbserver` 的伺服器串流接收預寫式日誌，並將其儲存在本機目錄 `/usr/local/pgsql/archive` 中：

```

$ pg_receivewal -h mydbserver -D /usr/local/pgsql/archive
```

<a id="id-1.9.4.17.11"></a>

## 另請參閱

[pg_basebackup](app-pgbasebackup.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgreceivewal.html)（原文版本：18.6；核對日期：2026-10-05）
