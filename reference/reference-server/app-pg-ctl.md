<a id="APP-PG-CTL"></a><a id="id-1.9.5.8.1"></a>

## pg_ctl

pg_ctl — 初始化、啟動、停止或控制 PostgreSQL 伺服器

## 語法

<a id="id-1.9.5.8.4.1"></a>

`pg_ctl` `init[db]` [`-D` *`datadir`*] [`-s`] [`-o` *`initdb-options`*]

<a id="id-1.9.5.8.4.2"></a>

`pg_ctl` `start` [`-D` *`datadir`*] [`-l` *`filename`*] [`-W`] [`-t` *`seconds`*] [`-s`] [`-o` *`options`*] [`-p` *`path`*] [`-c`]

<a id="id-1.9.5.8.4.3"></a>

`pg_ctl` `stop` [`-D` *`datadir`*] [`-m`
`s[mart]` | `f[ast]` | `i[mmediate]`
] [`-W`] [`-t` *`seconds`*] [`-s`]

<a id="id-1.9.5.8.4.4"></a>

`pg_ctl` `restart` [`-D` *`datadir`*] [`-m`
`s[mart]` | `f[ast]` | `i[mmediate]`
] [`-W`] [`-t` *`seconds`*] [`-s`] [`-o` *`options`*] [`-c`]

<a id="id-1.9.5.8.4.5"></a>

`pg_ctl` `reload` [`-D` *`datadir`*] [`-s`]

<a id="id-1.9.5.8.4.6"></a>

`pg_ctl` `status` [`-D` *`datadir`*]

<a id="id-1.9.5.8.4.7"></a>

`pg_ctl` `promote` [`-D` *`datadir`*] [`-W`] [`-t` *`seconds`*] [`-s`]

<a id="id-1.9.5.8.4.8"></a>

`pg_ctl` `logrotate` [`-D` *`datadir`*] [`-s`]

<a id="id-1.9.5.8.4.9"></a>

`pg_ctl` `kill` *`signal_name`* *`process_id`*

在 Microsoft Windows 上，另外還有：

<a id="id-1.9.5.8.4.11"></a>

`pg_ctl` `register` [`-D` *`datadir`*] [`-N` *`servicename`*] [`-U` *`username`*] [`-P` *`password`*] [`-S`
`a[uto]` | `d[emand]`
] [`-e` *`source`*] [`-W`] [`-t` *`seconds`*] [`-s`] [`-o` *`options`*]

<a id="id-1.9.5.8.4.12"></a>

`pg_ctl` `unregister` [`-N` *`servicename`*]

<a id="APP-PG-CTL-DESCRIPTION"></a>

## 說明

pg_ctl 是一個工具程式，用來初始化 PostgreSQL 資料庫叢集、啟動、停止或重新啟動 PostgreSQL 資料庫伺服器（[postgres](app-postgres.md)），或顯示執行中伺服器的狀態。雖然伺服器可以手動啟動，但 pg_ctl 封裝了諸如重新導向日誌輸出、以及正確地與終端機和程序群組分離等工作。它也提供了便利的選項，用於受控的關閉。

`init` 或 `initdb` 模式會建立新的 PostgreSQL 資料庫叢集，也就是由單一伺服器執行個體所管理的資料庫集合。此模式會呼叫 `initdb` 命令。詳細資訊請參閱 [initdb](app-initdb.md)。

`start` 模式會啟動新的伺服器。伺服器會在背景啟動，其標準輸入會連接到 `/dev/null`（在 Windows 上則是 `nul`）。在類 Unix 系統上，預設情況下，伺服器的標準輸出與標準錯誤會送到 pg_ctl 的標準輸出（而不是標準錯誤）。接著應該將 pg_ctl 的標準輸出重新導向到檔案，或以管線傳給另一個程序，例如 rotatelogs 這類日誌輪替程式；否則，`postgres` 會將其輸出寫到控制終端機（從背景寫入），而且不會離開 shell 的程序群組。在 Windows 上，預設情況下，伺服器的標準輸出與標準錯誤會送到終端機。這些預設行為可以透過使用 `-l` 將伺服器的輸出附加到日誌檔來改變。建議使用 `-l` 或輸出重新導向兩者之一。

`stop` 模式會關閉在指定資料目錄中執行的伺服器。可以使用 `-m` 選項選擇三種不同的關閉方式。「Smart」模式會不允許新的連線，然後等待所有既有的用戶端中斷連線。若伺服器處於熱待命（hot standby）狀態，一旦所有用戶端都已中斷連線，復原與串流複寫就會終止。「Fast」模式（預設）不會等待用戶端中斷連線。所有進行中的交易都會被回滾，用戶端會被強制中斷連線，然後關閉伺服器。「Immediate」模式會立即中止所有伺服器程序，而不進行正常關閉。這個選擇會導致下次啟動伺服器時進行一輪當機復原。

`restart` 模式實際上會先執行停止，再執行啟動。這讓你可以變更 `postgres` 的命令列選項，或變更那些不重新啟動伺服器就無法變更的設定檔選項。若伺服器啟動時在命令列上使用了相對路徑，則除非 pg_ctl 是在與伺服器啟動時相同的目前目錄中執行，否則 `restart` 可能會失敗。

`reload` 模式只是向 `postgres` 伺服器程序傳送 SIGHUP 訊號，使其重新讀取設定檔（`postgresql.conf`、`pg_hba.conf` 等）。這讓你可以變更那些不需要完整重新啟動伺服器即可生效的設定檔選項。

`status` 模式會檢查指定的資料目錄中是否有伺服器正在執行。若有，則會顯示該伺服器的 PID，以及用來啟動它的命令列選項。若伺服器未在執行，pg_ctl 會傳回結束狀態 3。若未指定可存取的資料目錄，pg_ctl 會傳回結束狀態 4。

`promote` 模式會命令在指定資料目錄中執行的待命伺服器結束待命模式，並開始進行讀寫操作。

`logrotate` 模式會輪替伺服器日誌檔。關於如何搭配外部日誌輪替工具使用此模式的詳細資訊，請參閱[第 24.3 節](../../server-administration/maintenance/logfile-maintenance.md)。

`kill` 模式會傳送訊號給指定的程序。這主要在沒有內建 kill 命令的 Microsoft Windows 上很有用。使用 `--help` 可以查看支援的訊號名稱清單。

`register` 模式會在 Microsoft Windows 上將 PostgreSQL 伺服器註冊為系統服務。`-S` 選項可以選擇服務的啟動類型，可以是「auto」（在系統啟動時自動啟動服務）或「demand」（依需求啟動服務）。

`unregister` 模式會在 Microsoft Windows 上取消註冊系統服務。這會撤銷 `register` 命令的效果。

<a id="APP-PG-CTL-OPTIONS"></a>

## 選項

`-c`<br>`--core-files`
:   在可行的平台上，藉由解除對 core 檔案所設的任何軟性資源限制，嘗試讓伺服器當機時產生 core 檔案。這可以從失敗的伺服器程序取得堆疊追蹤，因此對於除錯或診斷問題很有用。

`-D datadir`<br>`--pgdata=datadir`
:   指定資料庫設定檔在檔案系統中的位置。若省略此選項，則會使用環境變數 `PGDATA`。

`-l filename`<br>`--log=filename`
:   將伺服器日誌輸出附加到 *`filename`*。若檔案不存在，則會建立它。預設情況下，只有叢集擁有者可以存取該日誌檔。若叢集啟用了群組存取，與叢集擁有者同一群組的使用者也可以讀取它。

`-m mode`<br>`--mode=mode`
:   指定關閉模式。*`mode`* 可以是 `smart`、`fast` 或 `immediate`，或這三者之一的第一個字母。若省略此選項，預設為 `fast`。

`-o options`<br>`--options=options`
:   指定要直接傳給 `postgres` 命令的選項。`-o` 可以指定多次，所有給定的選項都會被傳遞過去。

    *`options`* 通常應該以單引號或雙引號括起來，以確保它們會被當作一組傳遞。

`-o initdb-options`<br>`--options=initdb-options`
:   指定要直接傳給 `initdb` 命令的選項。`-o` 可以指定多次，所有給定的選項都會被傳遞過去。

    *`initdb-options`* 通常應該以單引號或雙引號括起來，以確保它們會被當作一組傳遞。

`-p path`
:   指定 `postgres` 執行檔的位置。預設情況下，`postgres` 執行檔取自與 `pg_ctl` 相同的目錄，若找不到，則取自寫死的安裝目錄。除非你在做一些不尋常的事，並且收到找不到 `postgres` 執行檔的錯誤，否則不需要使用此選項。

    在 `init` 模式中，此選項同樣用來指定 `initdb` 執行檔的位置。

`-s`<br>`--silent`
:   只印出錯誤，不印出資訊性訊息。

`-t seconds`<br>`--timeout=seconds`
:   指定等待操作完成時最多等待的秒數（請參閱選項 `-w`）。預設為環境變數 `PGCTLTIMEOUT` 的值；若未設定，則為 60 秒。

`-V`<br>`--version`
:   印出 pg_ctl 的版本後結束。

`-w`<br>`--wait`
:   等待操作完成。`start`、`stop`、`restart`、`promote` 與 `register` 模式支援此選項，而且它是這些模式的預設行為。

    等待期間，`pg_ctl` 會反覆檢查伺服器的 PID 檔案，並在每次檢查之間短暫休眠。當 PID 檔案指出伺服器已準備好接受連線時，啟動即視為完成。當伺服器移除 PID 檔案時，關閉即視為完成。`pg_ctl` 會根據啟動或關閉是否成功傳回結束代碼。

    若操作未在逾時時間內完成（請參閱選項 `-t`），`pg_ctl` 會以非零的結束狀態結束。但請注意，該操作可能會在背景繼續進行，並且最終成功。

`-W`<br>`--no-wait`
:   不等待操作完成。這與選項 `-w` 相反。

    若停用等待，所要求的動作會被觸發，但不會有任何關於其是否成功的回饋。在這種情況下，就必須使用伺服器日誌檔或外部監控系統來檢查操作的進度與是否成功。

    在先前的 PostgreSQL 版本中，除了 `stop` 模式之外，這是預設行為。

`-?`<br>`--help`
:   顯示 pg_ctl 命令列引數的說明後結束。

若指定了有效但與所選操作模式無關的選項，pg_ctl 會忽略它。

<a id="APP-PG-CTL-WINDOWS-OPTIONS"></a>

### Windows 專用選項

`-e source`
:   以 Windows 服務執行時，pg_ctl 記錄到事件日誌所使用的事件來源名稱。預設為 `PostgreSQL`。請注意，這只控制從 pg_ctl 本身送出的訊息；伺服器啟動之後，會使用其 [event_source](../../server-administration/runtime-config/runtime-config-logging.md#GUC-EVENT-SOURCE) 參數所指定的事件來源。若伺服器在啟動的極早期、該參數尚未設定之前就失敗，它也可能使用預設的事件來源名稱 `PostgreSQL` 記錄日誌。

`-N servicename`
:   要註冊的系統服務名稱。此名稱會同時用作服務名稱與顯示名稱。預設為 `PostgreSQL`。

`-P password`
:   執行服務之使用者的密碼。

`-S start-type`
:   系統服務的啟動類型。*`start-type`* 可以是 `auto` 或 `demand`，或這兩者之一的第一個字母。若省略此選項，預設為 `auto`。

`-U username`
:   執行服務之使用者的使用者名稱。對於網域使用者，請使用 `DOMAIN\username` 格式。

<a id="id-1.9.5.8.7"></a>

## 環境

`PGCTLTIMEOUT`
:   等待啟動或關閉完成時，最多等待秒數的預設上限。若未設定，預設為 60 秒。

`PGDATA`
:   預設的資料目錄位置。

大多數 `pg_ctl` 模式都需要知道資料目錄的位置；因此，除非有設定 `PGDATA`，否則 `-D` 選項為必要。

關於其他會影響伺服器的變數，請參閱 [postgres](app-postgres.md)。

<a id="id-1.9.5.8.8"></a>

## 檔案

`postmaster.pid`
:   pg_ctl 會檢查資料目錄中的這個檔案，以判斷伺服器目前是否正在執行。

`postmaster.opts`
:   若資料目錄中存在此檔案，pg_ctl（在 `restart` 模式中）會將該檔案的內容作為選項傳給 postgres，除非被 `-o` 選項覆寫。此檔案的內容也會在 `status` 模式中顯示。

<a id="R1-APP-PGCTL-2"></a>

## 範例

<a id="R2-APP-PGCTL-3"></a>

### 啟動伺服器

啟動伺服器，並等待直到伺服器開始接受連線：

```

$ pg_ctl start
```

使用連接埠 5433 並在不使用 `fsync` 的情況下啟動伺服器：

```

$ pg_ctl -o "-F -p 5433" start
```

<a id="R2-APP-PGCTL-4"></a>

### 停止伺服器

停止伺服器：

```

$ pg_ctl stop
```

`-m` 選項可以控制伺服器*如何*關閉：

```

$ pg_ctl stop -m smart
```

<a id="R2-APP-PGCTL-5"></a>

### 重新啟動伺服器

重新啟動伺服器幾乎等同於先停止伺服器再重新啟動，差別在於預設情況下，`pg_ctl` 會儲存並重複使用傳給先前執行之執行個體的命令列選項。若要使用與先前相同的選項重新啟動伺服器：

```

$ pg_ctl restart
```

但若指定了 `-o`，它會取代任何先前的選項。若要使用連接埠 5433 重新啟動，並在重新啟動時停用 `fsync`：

```

$ pg_ctl -o "-F -p 5433" restart
```

<a id="R2-APP-PGCTL-6"></a>

### 顯示伺服器狀態

以下是 pg_ctl 的狀態輸出範例：

```

$ pg_ctl status

pg_ctl: server is running (PID: 13718)
/usr/local/pgsql/bin/postgres "-D" "/usr/local/pgsql/data" "-p" "5433" "-B" "128"
```

第二行是在 restart 模式中會呼叫的命令。

<a id="id-1.9.5.8.10"></a>

## 另請參閱

[initdb](app-initdb.md), [postgres](app-postgres.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pg-ctl.html)（原文版本：18.6；核對日期：2026-10-05）
