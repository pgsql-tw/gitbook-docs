<a id="APP-POSTGRES"></a><a id="id-1.9.5.16.1"></a>

## postgres

postgres — PostgreSQL 資料庫伺服器

<a id="id-1.9.5.16.4"></a>

## 語法

<a id="id-1.9.5.16.4.1"></a>

`postgres` [*`option`*...]

<a id="id-1.9.5.16.5"></a>

## 說明

`postgres` 是 PostgreSQL 資料庫伺服器。用戶端應用程式若要存取資料庫，會（透過網路或在本機）連線到正在執行的 `postgres` 執行個體。接著，`postgres` 執行個體會啟動一個獨立的伺服器程序來處理該連線。

一個 `postgres` 執行個體一律只管理恰好一個資料庫叢集的資料。資料庫叢集是儲存在同一個檔案系統位置（即「資料區域」）中的資料庫集合。同一系統上可以同時執行超過一個 `postgres` 執行個體，只要它們使用不同的資料區域與不同的通訊埠（見下文）。`postgres` 啟動時需要知道資料區域的位置。此位置必須以 `-D` 選項或 `PGDATA` 環境變數指定；它沒有預設值。通常，`-D` 或 `PGDATA` 會直接指向由 [initdb](app-initdb.md) 建立的資料區域目錄。其他可能的檔案配置在[第 19.2 節](../../server-administration/runtime-config/runtime-config-file-locations.md)中討論。

預設情況下，`postgres` 會在前景啟動，並將日誌訊息印到標準錯誤串流。在實際應用中，`postgres` 應該以背景程序的方式啟動，或許是在開機時啟動。

`postgres` 命令也可以在單一使用者模式下呼叫。此模式的主要用途是在 [initdb](app-initdb.md) 進行初始建置（bootstrapping）期間。有時它也會用於除錯或災難復原；請注意，執行單一使用者伺服器並不真正適合用來為伺服器除錯，因為不會發生貼近實際情況的程序間通訊與鎖定。從 shell 以單一使用者模式呼叫時，使用者可以輸入查詢，結果會印在螢幕上，但其形式對開發人員比對終端使用者更有用。在單一使用者模式中，工作階段使用者會被設為 ID 為 1 的使用者，並且會隱含地授予此使用者超級使用者的權力。此使用者實際上不必存在，因此單一使用者模式可以用來以手動方式，從系統目錄的某些意外損壞中復原。

<a id="APP-POSTGRES-OPTIONS"></a>

## 選項

`postgres` 接受下列命令列引數。關於這些選項的詳細討論，請參閱[第 19 章](../../server-administration/runtime-config/README.md)。你可以藉由設定組態檔，省去輸入大部分這些選項的麻煩。某些（安全的）選項也可以由連線中的用戶端，以取決於應用程式的方式設定，使其只套用於該工作階段。例如，若設定了環境變數 `PGOPTIONS`，則以 libpq 為基礎的用戶端會將該字串傳給伺服器，伺服器會將它解讀為 `postgres` 的命令列選項。

<a id="id-1.9.5.16.6.3"></a>

### 一般用途

`-B nbuffers`
:   設定伺服器程序所使用的共享緩衝區數量。此參數的預設值由 initdb 自動選定。指定此選項等同於設定組態參數 [shared_buffers](../../server-administration/runtime-config/runtime-config-resource.md#GUC-SHARED-BUFFERS)。

`-c name=value`
:   設定一個具名的執行時期參數。PostgreSQL 支援的組態參數在[第 19 章](../../server-administration/runtime-config/README.md)中說明。其他大多數命令列選項實際上都是這類參數設定的簡寫形式。`-c` 可以出現多次，以設定多個參數。

`-C name`
:   印出具名執行時期參數的值後結束。（細節請參閱上方的 `-c` 選項。）此選項傳回的是 `postgresql.conf` 中的值，並依這次呼叫所提供的任何參數加以修改。它不會反映叢集啟動時所提供的參數。

    對大多數參數而言，這可以在執行中的伺服器上使用。不過，對於某些在執行時期計算的參數（例如 [shared_memory_size](../../server-administration/runtime-config/runtime-config-preset.md#GUC-SHARED-MEMORY-SIZE)、[shared_memory_size_in_huge_pages](../../server-administration/runtime-config/runtime-config-preset.md#GUC-SHARED-MEMORY-SIZE-IN-HUGE-PAGES) 與 [wal_segment_size](../../server-administration/runtime-config/runtime-config-preset.md#GUC-WAL-SEGMENT-SIZE)），伺服器必須處於關閉狀態。

    此選項是供與伺服器執行個體互動的其他程式（例如 [pg_ctl](app-pg-ctl.md)）查詢組態參數值之用。面向使用者的應用程式應改用 [`SHOW`](../sql-commands/sql-show.md) 或 `pg_settings` 檢視表。

`-d debug-level`
:   設定除錯層級。此值設得越高，寫入伺服器日誌的除錯輸出就越多。值的範圍為 1 到 5。也可以針對特定工作階段傳入 `-d
    0`，這會防止上層 `postgres` 程序的伺服器日誌層級傳遞到此工作階段。

`-D datadir`
:   指定資料庫組態檔在檔案系統中的位置。細節請參閱[第 19.2 節](../../server-administration/runtime-config/runtime-config-file-locations.md)。

`-e`
:   將預設日期樣式設為「European」，也就是輸入日期欄位採 `DMY` 順序。這也會使某些日期輸出格式中，日印在月之前。更多資訊請參閱[第 8.5 節](../../the-sql-language/datatype/datatype-datetime.md)。

`-F`
:   停用 `fsync` 呼叫以提升效能，但要承擔系統當機時資料損毀的風險。指定此選項等同於停用組態參數 [fsync](../../server-administration/runtime-config/runtime-config-wal.md#GUC-FSYNC)。使用前請先閱讀詳細文件！

`-h hostname`
:   指定 `postgres` 要接聽用戶端應用程式 TCP/IP 連線的 IP 主機名稱或位址。此值也可以是以逗號分隔的位址清單，或以 `*` 指定接聽所有可用的介面。空值表示不接聽任何 IP 位址，此時只能使用 Unix 網域通訊端連線到伺服器。預設只接聽 localhost。指定此選項等同於設定組態參數 [listen_addresses](../../server-administration/runtime-config/runtime-config-connection.md#GUC-LISTEN-ADDRESSES)。

`-i`
:   允許遠端用戶端透過 TCP/IP（網際網路網域）連線進行連線。若沒有此選項，則只接受本機連線。此選項等同於在 `postgresql.conf` 中或透過 `-h` 將 `listen_addresses` 設為 `*`。

    此選項已被棄用，因為它無法使用 [listen_addresses](../../server-administration/runtime-config/runtime-config-connection.md#GUC-LISTEN-ADDRESSES) 的完整功能。通常直接設定 `listen_addresses` 會比較好。

`-k directory`
:   指定 `postgres` 用來接聽用戶端應用程式連線的 Unix 網域通訊端目錄。此值也可以是以逗號分隔的目錄清單。空值表示不接聽任何 Unix 網域通訊端，此時只能使用 TCP/IP 通訊端連線到伺服器。預設值通常是 `/tmp`，但可以在建置時變更。指定此選項等同於設定組態參數 [unix_socket_directories](../../server-administration/runtime-config/runtime-config-connection.md#GUC-UNIX-SOCKET-DIRECTORIES)。

`-l`
:   啟用使用 SSL 的安全連線。PostgreSQL 必須在編譯時加入 SSL 支援，此選項才能使用。關於使用 SSL 的更多資訊，請參閱[第 18.9 節](../../server-administration/runtime/ssl-tcp.md)。

`-N max-connections`
:   設定此伺服器可接受的用戶端連線數上限。此參數的預設值由 initdb 自動選定。指定此選項等同於設定組態參數 [max_connections](../../server-administration/runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS)。

`-p port`
:   指定 `postgres` 用來接聽用戶端應用程式連線的 TCP/IP 連接埠，或本機 Unix 網域通訊端檔案的副檔名。預設為環境變數 `PGPORT` 的值；若未設定 `PGPORT`，則預設為編譯時設定的值（通常是 5432）。若你指定了預設連接埠以外的連接埠，則所有用戶端應用程式都必須使用命令列選項或 `PGPORT` 指定相同的連接埠。

`-s`
:   在每個命令結束時印出時間資訊與其他統計資料。這對效能評測或調整緩衝區數量很有用。

`-S` *`work-mem`*
:   指定排序與雜湊表在改用暫存磁碟檔案之前所使用的基本記憶體量。請參閱[第 19.4.1 節](../../server-administration/runtime-config/runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY)中組態參數 `work_mem` 的說明。

`-V`<br>`--version`
:   印出 postgres 的版本後結束。

`--name=value`
:   設定一個具名的執行時期參數；這是 `-c` 的較短形式。

`--describe-config`
:   此選項會以定位字元（tab）分隔的 `COPY` 格式，傾印出伺服器內部的組態變數、說明與預設值。它主要是設計給管理工具使用。

`-?`<br>`--help`
:   顯示 postgres 命令列引數的說明後結束。

<a id="id-1.9.5.16.6.4"></a>

### 半內部選項

此處說明的選項主要用於除錯，在某些情況下也用來協助復原嚴重損壞的資料庫。在正式環境的資料庫設定中，應該沒有理由使用它們。將它們列在這裡，只是供 PostgreSQL 系統開發人員使用。此外，這些選項可能在未來的版本中變更或移除，且不另行通知。

`-f` `{ s | i | o | b | t | n | m | h }`
:   禁止使用特定的掃描與連接方法：`s` 與 `i` 分別停用循序掃描與索引掃描，`o`、`b` 與 `t` 分別停用僅索引掃描、點陣圖索引掃描與 TID 掃描，而 `n`、`m` 與 `h` 則分別停用巢狀迴圈連接、合併連接與雜湊連接。

    循序掃描與巢狀迴圈連接都無法完全停用；`-fs` 與 `-fn` 選項只是在最佳化器有其他任何替代方案時，不鼓勵它使用這些計畫類型。

`-O`
:   允許修改系統資料表的結構。`initdb` 會使用此選項。

`-P`
:   讀取系統資料表時忽略系統索引，但修改資料表時仍會更新這些索引。這在從損壞的系統索引中復原時很有用。

`-t` `pa[rser] | pl[anner] | e[xecutor]`
:   針對每個查詢，印出與各主要系統模組相關的計時統計資料。此選項不能與 `-s` 選項一起使用。

`-T`
:   此選項用於對導致伺服器程序異常終止的問題進行除錯。在這種情況下，一般的策略是傳送 SIGQUIT 訊號給所有其他伺服器程序，通知它們必須終止。使用此選項時，會改為傳送 SIGABRT，從而產生核心傾印（core dump）檔案。

`-v` *`protocol`*
:   指定特定工作階段所要使用的前端／後端協定版本號碼。此選項僅供內部使用。

`-W` *`seconds`*
:   啟動新的伺服器程序時，在它執行驗證程序之後，會延遲這麼多秒。這是為了提供機會，讓你用除錯器附加到該伺服器程序。

<a id="id-1.9.5.16.6.5"></a>

### 單一使用者模式的選項

<a id="id-1.9.5.16.6.5.2"></a>

下列選項只適用於單一使用者模式（請參閱下文的[單一使用者模式](app-postgres.md#APP-POSTGRES-SINGLE-USER)）。

`--single`
:   選擇單一使用者模式。這必須是命令列上的第一個引數。

*`database`*
:   指定要存取的資料庫名稱。這必須是命令列上的最後一個引數。若省略，則預設為使用者名稱。

`-E`
:   在執行每個命令之前，先將所有命令回顯到標準輸出。

`-j`
:   使用分號後接兩個換行字元（而不只是換行字元）作為命令輸入的結束符號。

`-r` *`filename`*
:   將所有伺服器日誌輸出送到 *`filename`*。只有以命令列選項提供時，此選項才會生效。

<a id="id-1.9.5.16.7"></a>

## 環境

`PGCLIENTENCODING`
:   用戶端使用的預設字元編碼。（用戶端可以個別覆寫此設定。）此值也可以在組態檔中設定。

`PGDATA`
:   預設資料目錄位置

`PGDATESTYLE`
:   執行時期參數 [DateStyle](../../server-administration/runtime-config/runtime-config-client.md#GUC-DATESTYLE) 的預設值。（此環境變數的使用已被棄用。）

`PGPORT`
:   預設連接埠號碼（最好在組態檔中設定）

<a id="id-1.9.5.16.8"></a>

## 診斷

提到 `semget` 或 `shmget` 的失敗訊息，很可能表示你需要設定核心，以提供足夠的共享記憶體與號誌。更多討論請參閱[第 18.4 節](../../server-administration/runtime/kernel-resources.md)。你或許可以藉由降低 [shared_buffers](../../server-administration/runtime-config/runtime-config-resource.md#GUC-SHARED-BUFFERS) 以減少 PostgreSQL 的共享記憶體用量，和／或降低 [max_connections](../../server-administration/runtime-config/runtime-config-connection.md#GUC-MAX-CONNECTIONS) 以減少號誌用量，來延後重新設定核心。

若失敗訊息暗示已有另一個伺服器在執行，應該仔細檢查，例如依你的系統使用下列命令

```

$ ps ax | grep postgres
```

或

```

$ ps -ef | grep postgres
```

來檢查。若你確定沒有發生衝突的伺服器正在執行，可以移除訊息中提到的鎖定檔，然後再試一次。

表示無法繫結到某個連接埠的失敗訊息，可能表示該連接埠已被某個非 PostgreSQL 的程序使用。若你終止 `postgres` 後立即使用相同連接埠重新啟動它，也可能會收到此錯誤；在這種情況下，你只需等待幾秒，直到作業系統關閉該連接埠，再重試即可。最後，若你指定了作業系統視為保留的連接埠號碼，也可能會收到此錯誤。例如，許多版本的 Unix 將小於 1024 的連接埠號碼視為「受信任」的，並只允許 Unix 超級使用者存取它們。

<a id="id-1.9.5.16.9"></a>

## 注意事項

可以使用工具程式命令 [pg_ctl](app-pg-ctl.md)，安全且方便地啟動與關閉 `postgres` 伺服器。

只要有可能，*不要*使用 `SIGKILL` 來終止主 `postgres` 伺服器。這麼做會使 `postgres` 無法在終止前釋放它所持有的系統資源（例如共享記憶體與號誌）。這可能會在啟動新的 `postgres` 執行時造成問題。

若要正常終止 `postgres` 伺服器，可以使用 `SIGTERM`、`SIGINT` 或 `SIGQUIT` 訊號。第一種會等待所有用戶端終止後才結束，第二種會強制中斷所有用戶端的連線，第三種則會立即結束而不進行正常關閉，導致重新啟動時執行復原。

`SIGHUP` 訊號會重新載入伺服器組態檔。也可以將 `SIGHUP` 傳送給個別的伺服器程序，但這通常沒有意義。

若要取消正在執行的查詢，請將 `SIGINT` 訊號傳送給執行該命令的程序。若要乾淨地終止某個後端程序，請將 `SIGTERM` 傳送給該程序。這兩個動作在 SQL 中可呼叫的對應方式，另請參閱[第 9.28.2 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL)中的 `pg_cancel_backend` 與 `pg_terminate_backend`。

`postgres` 伺服器使用 `SIGQUIT` 通知下層的伺服器程序終止，而不進行正常的清理。使用者*不應*使用此訊號。將 `SIGKILL` 傳送給伺服器程序也是不明智的——主 `postgres` 程序會將此解讀為當機，並在其標準的當機復原程序中，強制所有同層程序結束。

<a id="APP-POSTGRES-BUGS"></a>

## 程式錯誤

`--` 選項在 FreeBSD 或 OpenBSD 上無法運作。請改用 `-c`。這是受影響作業系統中的錯誤；若此問題未被修正，未來的 PostgreSQL 版本將會提供因應措施。

<a id="APP-POSTGRES-SINGLE-USER"></a>

## 單一使用者模式

若要以單一使用者模式啟動伺服器，請使用類似下列的命令

```

postgres --single -D /usr/local/pgsql/data other-options my_database
```

以 `-D` 提供資料庫目錄的正確路徑，或確認已設定環境變數 `PGDATA`。另外也要指定你想在其中工作的特定資料庫名稱。

通常，單一使用者模式伺服器會將換行字元視為命令輸入的結束符號；它不像 psql 那樣能聰明地處理分號。若要讓命令跨越多行，你必須在除了最後一個以外的每個換行字元之前輸入反斜線。反斜線與緊鄰的換行字元都會從輸入的命令中移除。請注意，即使是在字串常數或註解之中，也會發生這種情況。

但如果你使用 `-j` 命令列參數，單一換行字元並不會結束命令輸入；改為由「分號—換行—換行」的序列結束。也就是說，輸入一個分號，緊接著一個完全空白的行。在此模式中，反斜線加換行不會被特別處理。同樣地，對於出現在字串常數或註解中的這種序列，也不會有任何聰明的處理。

在任一種輸入模式中，若你輸入的分號既不是緊接在命令輸入結束符號之前，也不是其中的一部分，它會被視為命令分隔符號。當你確實輸入了命令輸入結束符號時，你已輸入的多個陳述式會作為單一交易執行。

若要結束工作階段，請輸入 EOF（通常是 **Control**+**D**）。若你在上一個命令輸入結束符號之後已輸入任何文字，則 EOF 會被當作命令輸入結束符號，此時需要再輸入一個 EOF 才能結束。

請注意，單一使用者模式伺服器不提供進階的行編輯功能（例如沒有命令歷程）。單一使用者模式也不會進行任何背景處理，例如自動檢查點或複寫。

<a id="APP-POSTGRES-EXAMPLES"></a>

## 範例

若要使用預設值在背景啟動 `postgres`，請輸入：

```

$ nohup postgres >logfile 2>&1 </dev/null &
```

若要以特定連接埠（例如 1234）啟動 `postgres`：

```

$ postgres -p 1234
```

若要使用 psql 連線到此伺服器，請以 -p 選項指定此連接埠：

```

$ psql -p 1234
```

或設定環境變數 `PGPORT`：

```

$ export PGPORT=1234
$ psql
```

具名的執行時期參數可以用下列任一種寫法設定：

```

$ postgres -c work_mem=1234
$ postgres --work-mem=1234
```

任一種形式都會覆寫 `postgresql.conf` 中可能存在的 `work_mem` 設定。請注意，在命令列上，參數名稱中的底線可以寫成底線或破折號。除了短期實驗之外，比較好的做法或許是在 `postgresql.conf` 中編輯設定，而不是依賴命令列參數來設定參數。

<a id="id-1.9.5.16.13"></a>

## 另請參閱

[initdb](app-initdb.md),
[pg_ctl](app-pg-ctl.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-postgres.html)（原文版本：18.6；核對日期：2026-10-10）
