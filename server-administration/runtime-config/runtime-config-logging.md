<a id="RUNTIME-CONFIG-LOGGING"></a>

## 19.8. 錯誤回報與日誌記錄 [#](#runtime-config-logging) <a href="#runtime-config-logging" id="runtime-config-logging"></a>

[19.8.1. 記錄位置](runtime-config-logging.md#runtime-config-logging-where)

[19.8.2. 記錄時機](runtime-config-logging.md#runtime-config-logging-when)

[19.8.3. 記錄內容](runtime-config-logging.md#runtime-config-logging-what)

[19.8.4. 使用 CSV 格式日誌輸出](runtime-config-logging.md#runtime-config-logging-csvlog)

[19.8.5. 使用 JSON 格式日誌輸出](runtime-config-logging.md#runtime-config-logging-jsonlog)

[19.8.6. 程序標題](runtime-config-logging.md#runtime-config-logging-proc-title)

<a id="id-1.6.6.11.2"></a>

<a id="RUNTIME-CONFIG-LOGGING-WHERE"></a>

### 19.8.1. 記錄位置 [#](#runtime-config-logging-where) <a href="#runtime-config-logging-where" id="runtime-config-logging-where"></a>

<a id="id-1.6.6.11.3.2"></a><a id="id-1.6.6.11.3.3"></a>

<a id="GUC-LOG-DESTINATION"></a>

`log_destination` (`string`) <a id="id-1.6.6.11.3.4.1.1.3"></a> [#](#GUC-LOG-DESTINATION)
:   PostgreSQL 支援多種
    記錄伺服器訊息的方法，包括
    stderr、csvlog、
    jsonlog，以及
    syslog。在 Windows 上，
    也支援 eventlog。請將此
    參數設為以逗號分隔的所需記錄目的地清單。
    預設只會記錄到 stderr。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

    若 `log_destination` 中包含 csvlog，
    日誌項目會以「逗號分隔值」（CSV）格式輸出，
    方便匯入其他程式使用。
    詳情請參閱 [第 19.8.4 節](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG)。
    必須啟用 [logging_collector](runtime-config-logging.md#GUC-LOGGING-COLLECTOR)
    才能產生 CSV 格式的日誌輸出。

    若 `log_destination` 中包含
    jsonlog，日誌項目會以
    JSON 格式輸出，方便匯入其他程式使用。
    詳情請參閱 [第 19.8.5 節](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG)。
    必須啟用 [logging_collector](runtime-config-logging.md#GUC-LOGGING-COLLECTOR)
    才能產生 JSON 格式的日誌輸出。

    當 stderr、
    csvlog 或 jsonlog
    其中之一被包含在內時，就會建立 `current_logfiles`
    檔案，用來記錄日誌收集器目前使用中的日誌檔案位置，
    以及對應的記錄目的地。這提供了一個方便的方式，
    可用來找出此執行個體目前正在使用的日誌檔。以下是
    此檔案內容的範例：

    ```

    stderr log/postgresql.log
    csvlog log/postgresql.csv
    jsonlog log/postgresql.json
    ```

    `current_logfiles` 會在因輪替而建立新日誌檔案時，
    以及 `log_destination` 被重新載入時重新建立。
    當 `log_destination` 中不再包含
    stderr、csvlog
    或 jsonlog 任何一項，
    或日誌收集器被停用時，此檔案就會被移除。

    ### 注意

    在大多數 Unix 系統上，你需要變更系統 syslog
    守護程序的組態，才能使用
    `log_destination` 的 syslog 選項。
    PostgreSQL 可以記錄到 syslog 的
    `LOCAL0` 到 `LOCAL7` 設施
    （請參閱 [syslog_facility](runtime-config-logging.md#GUC-SYSLOG-FACILITY)），
    但大多數平台上 syslog 的預設組態，
    會捨棄所有這類訊息。你需要加入類似下列的內容：

    ```

    local0.*    /var/log/postgresql
    ```

    到 syslog 守護程序的組態檔中，才能使其運作。

    在 Windows 上，當你為 `log_destination` 使用
    `eventlog` 選項時，你應該向作業系統
    註冊事件來源及其程式庫，讓 Windows 事件檢視器
    能夠正確地顯示事件日誌訊息。
    詳情請參閱 [第 18.12 節](../runtime/event-log-registration.md)。
<a id="GUC-LOGGING-COLLECTOR"></a>

`logging_collector` (`boolean`) <a id="id-1.6.6.11.3.4.2.1.3"></a> [#](#GUC-LOGGING-COLLECTOR)
:   此參數會啟用*日誌收集器*，這是一個背景程序，
    負責擷取傳送到 stderr 的日誌訊息，
    並將其重新導向至日誌檔案。這種做法通常比
    記錄到 syslog 更實用，因為有些類型的訊息
    可能不會出現在 syslog 輸出中。
    （常見的例子之一是動態連結器失敗訊息；
    另一個例子則是由 `archive_command` 等
    指令碼所產生的錯誤訊息。）
    此參數只能在伺服器啟動時設定。

    ### 注意

    你可以在不使用日誌收集器的情況下記錄到 stderr；
    日誌訊息就只會送往伺服器 stderr 導向的目的地。
    然而，此方法只適合日誌量較低的情況，
    因為它沒有提供方便輪替日誌檔案的方式。此外，
    在某些平台上，不使用日誌收集器可能會導致日誌輸出遺失或
    內容混亂，因為多個程序同時寫入同一個日誌檔案時，
    可能會互相覆寫彼此的輸出。

    ### 注意

    日誌收集器的設計目標是絕不遺失訊息。這代表
    在負載極高的情況下，當收集器的處理進度落後時，
    伺服器程序在嘗試傳送更多日誌訊息時可能會被阻塞。
    相較之下，syslog 在無法寫入訊息時
    傾向於直接捨棄，這代表它在這類情況下
    可能無法記錄部分訊息，但不會阻塞系統其他部分。
<a id="GUC-LOG-DIRECTORY"></a>

`log_directory` (`string`) <a id="id-1.6.6.11.3.4.3.1.3"></a> [#](#GUC-LOG-DIRECTORY)
:   當 `logging_collector` 啟用時，
    此參數決定日誌檔案要建立在哪個目錄中。
    可以指定為絕對路徑，或相對於叢集資料目錄的路徑。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
    預設值為 `log`。
<a id="GUC-LOG-FILENAME"></a>

`log_filename` (`string`) <a id="id-1.6.6.11.3.4.4.1.3"></a> [#](#GUC-LOG-FILENAME)
:   當 `logging_collector` 啟用時，
    此參數設定所建立日誌檔案的檔名。此值會被視為
    `strftime` 樣式字串，因此可使用
    `%`-逸出序列來指定隨時間變化的檔名。
    （請注意，若含有任何與時區相關的
    `%`-逸出序列，計算時會採用
    [log_timezone](runtime-config-logging.md#GUC-LOG-TIMEZONE) 所指定的時區。）
    所支援的 `%`-逸出序列，
    與 Open Group 的 [strftime](https://pubs.opengroup.org/onlinepubs/009695399/functions/strftime.html) 規格
    中所列出的類似。請注意，並不會直接使用
    系統的 `strftime`，因此平台特有（非標準）
    的擴充功能無法運作。
    預設值為 `postgresql-%Y-%m-%d_%H%M%S.log`。

    若你指定的檔名沒有逸出序列，就應規劃使用日誌輪替工具，
    以避免最終塞滿整個磁碟。在 8.4
    之前的版本中，若沒有任何 `%` 逸出序列，
    PostgreSQL 會附加新日誌檔案建立時間的
    epoch 值，但現在已不再如此。

    若 `log_destination` 中啟用了 CSV 格式輸出，
    系統會在加上時間戳記的日誌檔名後附加
    `.csv`，作為 CSV 格式輸出的檔名。
    （若 `log_filename` 以 `.log` 結尾，
    則會改為替換該副檔名。）

    若 `log_destination` 中啟用了 JSON 格式輸出，
    系統會在加上時間戳記的日誌檔名後附加
    `.json`，作為 JSON 格式輸出的檔名。
    （若 `log_filename` 以 `.log` 結尾，
    則會改為替換該副檔名。）

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-LOG-FILE-MODE"></a>

`log_file_mode` (`integer`) <a id="id-1.6.6.11.3.4.5.1.3"></a> [#](#GUC-LOG-FILE-MODE)
:   在 Unix 系統上，此參數會在 `logging_collector`
    啟用時，設定日誌檔案的權限。（在 Microsoft
    Windows 上此參數會被忽略。）
    此參數值應為一個數值模式，
    格式須符合
    `chmod` 與 `umask`
    系統呼叫所接受的格式。（若要使用慣用的八進位格式，
    數字必須以 `0`（零）開頭。）

    預設權限為 `0600`，代表只有
    伺服器擁有者能讀寫日誌檔案。另一個常見且實用的設定是
    `0640`，允許擁有者所屬群組的成員讀取這些檔案。
    然而請注意，若要使用這類設定，你需要變更
    [log_directory](runtime-config-logging.md#GUC-LOG-DIRECTORY)，
    將檔案儲存在叢集資料目錄之外的位置。無論如何，
    將日誌檔案設為所有人皆可讀取並不明智，
    因為其中可能含有敏感資料。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-LOG-ROTATION-AGE"></a>

`log_rotation_age` (`integer`) <a id="id-1.6.6.11.3.4.6.1.3"></a> [#](#GUC-LOG-ROTATION-AGE)
:   當 `logging_collector` 啟用時，
    此參數決定單一日誌檔案的最長使用時間，超過此時間後
    就會建立新的日誌檔案。
    若此值未指定單位，則以分鐘為單位。
    預設值為 24 小時。
    設為零可停用以時間為基礎建立新日誌檔案的功能。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-LOG-ROTATION-SIZE"></a>

`log_rotation_size` (`integer`) <a id="id-1.6.6.11.3.4.7.1.3"></a> [#](#GUC-LOG-ROTATION-SIZE)
:   當 `logging_collector` 啟用時，
    此參數決定單一日誌檔案的最大大小。
    當日誌檔案已寫入此數量的資料後，
    就會建立新的日誌檔案。
    若此值未指定單位，則以 KB 為單位。
    預設值為 10 MB。
    設為零可停用以大小為基礎建立新日誌檔案的功能。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-LOG-TRUNCATE-ON-ROTATION"></a>

`log_truncate_on_rotation` (`boolean`) <a id="id-1.6.6.11.3.4.8.1.3"></a> [#](#GUC-LOG-TRUNCATE-ON-ROTATION)
:   當 `logging_collector` 啟用時，
    此參數會使 PostgreSQL 截斷（覆寫）任何同名的既有日誌檔案，
    而不是附加寫入其後。然而，只有在因時間基礎輪替而開啟
    新檔案時才會發生截斷，伺服器啟動時或因大小基礎輪替時則不會。
    當此參數為 off 時，既有檔案在所有情況下都會被附加寫入。
    舉例來說，若將此設定與類似
    `postgresql-%H.log` 的 `log_filename`
    搭配使用，就會產生二十四個逐小時的日誌檔案，
    並依循環方式覆寫它們。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

    範例：若要保留 7 天的日誌，每天一個日誌檔案，
    分別命名為 `server_log.Mon`、`server_log.Tue`
    等，並自動以本週的日誌覆寫上週的日誌，
    請將 `log_filename` 設為 `server_log.%a`，
    `log_truncate_on_rotation` 設為 `on`，
    並將 `log_rotation_age` 設為 `1440`。

    範例：若要保留 24 小時的日誌，每小時一個日誌檔案，
    但當日誌檔案大小超過 1GB 時也提早輪替，
    請將 `log_filename` 設為 `server_log.%H%M`，
    `log_truncate_on_rotation` 設為 `on`，
    `log_rotation_age` 設為 `60`，
    並將 `log_rotation_size` 設為 `1000000`。
    在 `log_filename` 中加入 `%M`，
    可讓任何因大小觸發的輪替，選用與該小時初始檔名不同的檔名。
<a id="GUC-SYSLOG-FACILITY"></a>

`syslog_facility` (`enum`) <a id="id-1.6.6.11.3.4.9.1.3"></a> [#](#GUC-SYSLOG-FACILITY)
:   當啟用記錄到 syslog 時，此參數決定
    所使用的 syslog「設施（facility）」。
    你可以從 `LOCAL0`、`LOCAL1`、
    `LOCAL2`、`LOCAL3`、`LOCAL4`、
    `LOCAL5`、`LOCAL6`、`LOCAL7`
    中選擇；預設值為 `LOCAL0`。
    另請參閱你系統上
    syslog 守護程序的文件。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-SYSLOG-IDENT"></a>

`syslog_ident` (`string`) <a id="id-1.6.6.11.3.4.10.1.3"></a> [#](#GUC-SYSLOG-IDENT)
:   當啟用記錄到 syslog 時，此參數決定用於在
    syslog 日誌中識別
    PostgreSQL 訊息的程式名稱。預設值為
    `postgres`。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-SYSLOG-SEQUENCE-NUMBERS"></a>

`syslog_sequence_numbers` (`boolean`) <a id="id-1.6.6.11.3.4.11.1.3"></a> [#](#GUC-SYSLOG-SEQUENCE-NUMBERS)
:   當記錄到 syslog 且此設定為 on（預設值）時，
    每則訊息前面都會加上遞增的序號
    （例如 `[2]`）。這能避免許多
    syslog 實作預設會執行的
    「--- last message repeated N times ---」抑制行為。
    在較新版的 syslog 實作中，重複訊息的抑制是可設定的
    （例如 rsyslog 中的
    `$RepeatedMsgReduction`），
    因此可能不需要這麼做。此外，
    若你確實想要抑制重複訊息，也可以將此設定關閉。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-SYSLOG-SPLIT-MESSAGES"></a>

`syslog_split_messages` (`boolean`) <a id="id-1.6.6.11.3.4.12.1.3"></a> [#](#GUC-SYSLOG-SPLIT-MESSAGES)
:   當啟用記錄到 syslog 時，此參數決定訊息傳遞給
    syslog 的方式。當此設定為 on（預設值）時，
    訊息會依行分割，過長的行也會被切分，
    使其符合傳統 syslog 實作常見的 1024 位元組大小限制。
    當設為 off 時，PostgreSQL 伺服器日誌訊息
    會依原樣傳遞給 syslog 服務，
    至於如何處理可能很龐大的訊息，則由 syslog 服務自行負責。

    若 syslog 最終是記錄到文字檔案，
    則不論哪種設定，結果都會相同，此時最好保持此設定為開啟，
    因為大多數 syslog 實作要嘛無法處理大型訊息，
    要嘛需要特別設定才能處理。但若 syslog
    最終是寫入其他媒介，將訊息在邏輯上保持完整，
    可能有其必要性或更為實用。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-EVENT-SOURCE"></a>

`event_source` (`string`) <a id="id-1.6.6.11.3.4.13.1.3"></a> [#](#GUC-EVENT-SOURCE)
:   當啟用記錄到事件日誌時，此參數決定用於在
    日誌中識別 PostgreSQL 訊息的程式名稱。
    預設值為 `PostgreSQL`。
    此參數只能在伺服器啟動時設定。

<a id="RUNTIME-CONFIG-LOGGING-WHEN"></a>

### 19.8.2. 記錄時機 [#](#runtime-config-logging-when) <a href="#runtime-config-logging-when" id="runtime-config-logging-when"></a>

<a id="GUC-LOG-MIN-MESSAGES"></a>

`log_min_messages` (`enum`) <a id="id-1.6.6.11.4.2.1.1.3"></a> [#](#GUC-LOG-MIN-MESSAGES)
:   控制哪些[訊息層級](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS)
    會被寫入伺服器日誌。
    有效值為 `DEBUG5`、`DEBUG4`、
    `DEBUG3`、`DEBUG2`、`DEBUG1`、
    `INFO`、`NOTICE`、`WARNING`、
    `ERROR`、`LOG`、`FATAL`，以及
    `PANIC`。每個層級都涵蓋其後所有層級。
    層級越晚，送到日誌的訊息就越少。
    預設值為 `WARNING`。請注意，
    `LOG` 在此處的層級順序，
    與在 [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) 中不同。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。
<a id="GUC-LOG-MIN-ERROR-STATEMENT"></a>

`log_min_error_statement` (`enum`) <a id="id-1.6.6.11.4.2.2.1.3"></a> [#](#GUC-LOG-MIN-ERROR-STATEMENT)
:   控制哪些導致錯誤情況的 SQL 陳述式，會被記錄在
    伺服器日誌中。對於達到指定
    [嚴重性](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS)
    或更高層級的任何訊息，目前的
    SQL 陳述式都會被包含在該日誌項目中。
    有效值為 `DEBUG5`、
    `DEBUG4`、`DEBUG3`、
    `DEBUG2`、`DEBUG1`、
    `INFO`、`NOTICE`、
    `WARNING`、`ERROR`、
    `LOG`、
    `FATAL`，以及 `PANIC`。
    預設值為 `ERROR`，代表會記錄導致 ERROR、LOG、
    FATAL 或 PANIC 層級訊息的陳述式。
    若要實質上關閉失敗陳述式的記錄，
    請將此參數設為 `PANIC`。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。
<a id="GUC-LOG-MIN-DURATION-STATEMENT"></a>

`log_min_duration_statement` (`integer`) <a id="id-1.6.6.11.4.2.3.1.3"></a> [#](#GUC-LOG-MIN-DURATION-STATEMENT)
:   若某個已完成陳述式的執行時間達到指定的時間長度，
    就會記錄其耗時。例如，若你將此值設為
    `250ms`，則所有執行時間達 250 毫秒
    或以上的 SQL 陳述式都會被記錄。啟用此參數，
    有助於找出應用程式中未經最佳化的查詢。
    若此值未指定單位，則以毫秒為單位。
    將此值設為零會印出所有陳述式的耗時。
    `-1`（預設值）會停用記錄陳述式耗時。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。

    此設定會覆寫 [log_min_duration_sample](runtime-config-logging.md#GUC-LOG-MIN-DURATION-SAMPLE)，
    也就是說，耗時超過此設定的查詢，不受取樣限制，
    一律都會被記錄。

    對於使用延伸查詢協定的用戶端，
    剖析（Parse）、綁定（Bind）與執行（Execute）步驟的耗時，
    會被各自獨立記錄。

    ### 注意

    當此選項與
    [log_statement](runtime-config-logging.md#GUC-LOG-STATEMENT)
    搭配使用時，因 `log_statement`
    而被記錄的陳述式文字，不會在耗時日誌訊息中重複出現。
    若你並未使用 syslog，
    建議你透過
    [log_line_prefix](runtime-config-logging.md#GUC-LOG-LINE-PREFIX)
    記錄程序 ID 或工作階段 ID，
    以便日後可利用程序 ID 或工作階段 ID，
    將該陳述式訊息與稍後的耗時訊息連結起來。
<a id="GUC-LOG-MIN-DURATION-SAMPLE"></a>

`log_min_duration_sample` (`integer`) <a id="id-1.6.6.11.4.2.4.1.3"></a> [#](#GUC-LOG-MIN-DURATION-SAMPLE)
:   允許對執行時間達到指定時間長度的已完成陳述式進行耗時取樣。
    這會產生與
    [log_min_duration_statement](runtime-config-logging.md#GUC-LOG-MIN-DURATION-STATEMENT) 相同種類的日誌項目，
    但僅針對已執行陳述式的一部分子集合，
    取樣率由
    [log_statement_sample_rate](runtime-config-logging.md#GUC-LOG-STATEMENT-SAMPLE-RATE)
    控制。例如，若你將此值設為 `100ms`，
    則所有執行時間達 100 毫秒或以上的
    SQL 陳述式都會被納入取樣考量。當流量過高、
    無法記錄所有查詢時，啟用此參數會很有幫助。
    若此值未指定單位，則以毫秒為單位。
    將此值設為零會對所有陳述式耗時進行取樣。
    `-1`（預設值）會停用陳述式耗時取樣。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。

    此設定的優先順序低於
    `log_min_duration_statement`，
    也就是說，耗時超過 `log_min_duration_statement`
    的陳述式，不受取樣限制，一律都會被記錄。

    適用於 `log_min_duration_statement`
    的其他注意事項，同樣適用於此設定。
<a id="GUC-LOG-STATEMENT-SAMPLE-RATE"></a>

`log_statement_sample_rate` (`floating point`) <a id="id-1.6.6.11.4.2.5.1.3"></a> [#](#GUC-LOG-STATEMENT-SAMPLE-RATE)
:   決定耗時超過
    [log_min_duration_sample](runtime-config-logging.md#GUC-LOG-MIN-DURATION-SAMPLE)
    的陳述式中，會被記錄的比例。
    取樣是隨機性的，例如 `0.5` 代表
    統計上任何給定陳述式，有二分之一的機率會被記錄。
    預設值為 `1.0`，代表會記錄所有被取樣到的
    陳述式。將此值設為零會停用取樣式陳述式耗時記錄，
    效果等同於將
    `log_min_duration_sample` 設為
    `-1`。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。
<a id="GUC-LOG-TRANSACTION-SAMPLE-RATE"></a>

`log_transaction_sample_rate` (`floating point`) <a id="id-1.6.6.11.4.2.6.1.3"></a> [#](#GUC-LOG-TRANSACTION-SAMPLE-RATE)
:   設定除了因其他原因而被記錄的陳述式之外，
    其所有陳述式都會被記錄的交易比例。
    這適用於每一筆新交易，不論其陳述式的耗時為何。
    取樣是隨機性的，例如 `0.1` 代表
    統計上任何給定交易，有十分之一的機率會被記錄。
    `log_transaction_sample_rate` 有助於
    建構交易樣本。
    預設值為 `0`，代表不記錄任何額外交易的陳述式。
    將此值設為 `1` 會記錄所有交易的所有陳述式。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。

    ### 注意

    如同所有陳述式記錄選項一樣，此選項可能會增加可觀的額外負擔。
<a id="GUC-LOG-STARTUP-PROGRESS-INTERVAL"></a>

`log_startup_progress_interval` (`integer`) <a id="id-1.6.6.11.4.2.7.1.3"></a> [#](#GUC-LOG-STARTUP-PROGRESS-INTERVAL)
:   設定啟動程序在多久之後，
    會針對仍在進行中的長時間執行作業記錄一則訊息，
    以及該作業後續進度訊息之間的間隔時間。
    預設值為 10 秒。設為 `0`
    會停用此功能。若此值未指定單位，
    則以毫秒為單位。此設定會分別套用於每項作業。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

    舉例來說，若同步資料目錄花費 25 秒，
    接著重設未記錄（unlogged）的關聯又花費 8 秒，
    而此設定為預設值 10 秒，
    則在同步資料目錄進行 10 秒後，
    以及進行 20 秒後，各會記錄一則訊息，
    但重設未記錄（unlogged）的關聯則不會記錄任何訊息。

[表 19.2](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS) 說明了
PostgreSQL 所使用的訊息嚴重性層級。若日誌輸出
被送往 syslog 或 Windows 的
eventlog，嚴重性層級會依表中所示進行轉換。

<a id="RUNTIME-CONFIG-SEVERITY-LEVELS"></a>

**表 19.2. 訊息嚴重性層級**

<table border="1" class="table" summary="訊息嚴重性層級"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th>嚴重性</th><th>用途</th><th><span class="systemitem">syslog</span></th><th><span class="systemitem">eventlog</span></th></tr></thead><tbody><tr><td><code class="literal">DEBUG1 .. DEBUG5</code></td><td>提供逐漸更詳細的資訊，供開發人員使用。</td><td><code class="literal">DEBUG</code></td><td><code class="literal">INFORMATION</code></td></tr><tr><td><code class="literal">INFO</code></td><td>提供使用者隱含要求的資訊，
         例如 <code class="command">VACUUM VERBOSE</code> 的輸出。</td><td><code class="literal">INFO</code></td><td><code class="literal">INFORMATION</code></td></tr><tr><td><code class="literal">NOTICE</code></td><td>提供可能對使用者有幫助的資訊，
         例如長識別字被截斷的通知。</td><td><code class="literal">NOTICE</code></td><td><code class="literal">INFORMATION</code></td></tr><tr><td><code class="literal">WARNING</code></td><td>提供可能發生問題的警告，
         例如在交易區塊之外執行 <code class="command">COMMIT</code>。</td><td><code class="literal">NOTICE</code></td><td><code class="literal">WARNING</code></td></tr><tr><td><code class="literal">ERROR</code></td><td>回報導致目前命令中止的錯誤。</td><td><code class="literal">WARNING</code></td><td><code class="literal">ERROR</code></td></tr><tr><td><code class="literal">LOG</code></td><td>回報管理人員感興趣的資訊，
         例如檢查點活動。</td><td><code class="literal">INFO</code></td><td><code class="literal">INFORMATION</code></td></tr><tr><td><code class="literal">FATAL</code></td><td>回報導致目前工作階段中止的錯誤。</td><td><code class="literal">ERR</code></td><td><code class="literal">ERROR</code></td></tr><tr><td><code class="literal">PANIC</code></td><td>回報導致所有資料庫工作階段皆中止的錯誤。</td><td><code class="literal">CRIT</code></td><td><code class="literal">ERROR</code></td></tr></tbody></table>

<br>

<a id="RUNTIME-CONFIG-LOGGING-WHAT"></a>

### 19.8.3. 記錄內容 [#](#runtime-config-logging-what) <a href="#runtime-config-logging-what" id="runtime-config-logging-what"></a>

### 注意

你選擇記錄的內容可能涉及安全性議題；請參閱
[第 24.3 節](../maintenance/logfile-maintenance.md)。

<a id="GUC-APPLICATION-NAME"></a>

`application_name` (`string`) <a id="id-1.6.6.11.5.3.1.1.3"></a> [#](#GUC-APPLICATION-NAME)
:   `application_name` 可以是任何長度小於
    `NAMEDATALEN` 個字元（標準組建中為 64 個字元）的字串。
    通常由應用程式在連線至伺服器時進行設定。
    此名稱會顯示在 `pg_stat_activity` 檢視表中，
    並包含在 CSV 日誌項目裡。也可透過
    [log_line_prefix](runtime-config-logging.md#GUC-LOG-LINE-PREFIX) 參數，
    將其納入一般日誌項目中。
    `application_name` 值只能使用
    可列印的 ASCII 字元。
    其他字元會被替換為
    [C 樣式十六進位逸出序列](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE)。
<a id="GUC-DEBUG-PRINT-PARSE"></a>

`debug_print_parse` (`boolean`) <a id="id-1.6.6.11.5.3.2.1.3"></a> <br>`debug_print_rewritten` (`boolean`) <a id="id-1.6.6.11.5.3.2.2.3"></a> <br>`debug_print_plan` (`boolean`) <a id="id-1.6.6.11.5.3.2.3.3"></a> [#](#GUC-DEBUG-PRINT-PARSE)
:   這些參數會啟用各種除錯輸出。
    設定後，它們會印出每個已執行查詢
    所產生的剖析樹、查詢重寫器輸出，
    或執行計畫。這些訊息會以 `LOG`
    訊息層級發出，因此依預設會出現在伺服器日誌中，
    但不會傳送給用戶端。你可以透過調整
    [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) 及／或
    [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) 來改變這一點。
    這些參數預設為關閉。
<a id="GUC-DEBUG-PRETTY-PRINT"></a>

`debug_pretty_print` (`boolean`) <a id="id-1.6.6.11.5.3.3.1.3"></a> [#](#GUC-DEBUG-PRETTY-PRINT)
:   設定後，`debug_pretty_print` 會將
    `debug_print_parse`、
    `debug_print_rewritten`，或
    `debug_print_plan` 所產生的訊息加上縮排。
    這會產生比關閉時所使用「精簡」格式更易讀，
    但也更長的輸出。此參數預設為開啟。
<a id="GUC-LOG-AUTOVACUUM-MIN-DURATION"></a>

`log_autovacuum_min_duration` (`integer`) <a id="id-1.6.6.11.5.3.4.1.3"></a> [#](#GUC-LOG-AUTOVACUUM-MIN-DURATION)
:   若自動 vacuum 所執行的動作耗時達到指定的時間長度，
    就會記錄該動作。將此值設為零會記錄
    所有自動 vacuum 動作。`-1` 會停用
    自動 vacuum 動作記錄。若此值未指定單位，
    則以毫秒為單位。例如，若你將此值設為
    `250ms`，則所有耗時達 250 毫秒
    或以上的自動 vacuum 與 analyze 都會被記錄。此外，
    當此參數設為除 `-1` 以外的任何值時，
    若某個自動 vacuum 動作因鎖定衝突或關聯被同時捨棄
    而被略過，也會記錄一則訊息。預設值為 `10min`。
    啟用此參數有助於追蹤自動 vacuum 活動。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定；但可以透過變更資料表儲存參數，
    針對個別資料表覆寫此設定。
<a id="GUC-LOG-CHECKPOINTS"></a>

`log_checkpoints` (`boolean`) <a id="id-1.6.6.11.5.3.5.1.3"></a> [#](#GUC-LOG-CHECKPOINTS)
:   使檢查點與重新啟動點被記錄在伺服器日誌中。
    日誌訊息中會包含一些統計資訊，
    包括已寫入的緩衝區數量，以及寫入所花費的時間。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。預設值為 on。
<a id="GUC-LOG-CONNECTIONS"></a>

`log_connections` (`string`) <a id="id-1.6.6.11.5.3.6.1.3"></a> [#](#GUC-LOG-CONNECTIONS)
:   使每個連線到伺服器的連線各方面資訊都被記錄。
    預設值為空字串 `''`，
    會停用所有連線記錄。以下選項可單獨指定，
    也可以逗號分隔清單的形式指定：

    <a id="LOG-CONNECTIONS-OPTIONS"></a>

    **表 19.3. 連線記錄選項**

    <table border="1" class="table" summary="連線記錄選項"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>名稱</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">receipt</code></td><td>記錄連線的接收。</td></tr><tr><td><code class="literal">authentication</code></td><td>
                記錄驗證方法用來識別使用者的原始身分。
                在多數情況下，此身分字串
                會與 <span class="productname">PostgreSQL</span> 使用者名稱相符，
                但有些第三方驗證方法，
                可能會在伺服器儲存之前變更原始使用者識別字。
                無論此設定為何值，驗證失敗一律會被記錄。
               </td></tr><tr><td><code class="literal">authorization</code></td><td>
                記錄授權成功完成的情形。此時
                連線已經建立，但後端尚未完全設定完成。
                日誌訊息中包含已授權的使用者名稱、
                資料庫名稱，以及應用程式名稱（若適用）。
               </td></tr><tr><td><code class="literal">setup_durations</code></td><td>
                記錄建立連線，以及設定後端直到連線
                準備好執行第一個查詢為止所花費的時間。
                日誌訊息中包含三項耗時：總設定耗時
                （從 postmaster 接受傳入連線開始，
                到連線準備好接受查詢為止）、
                分岔（fork）新後端所花費的時間，
                以及驗證使用者所花費的時間。
               </td></tr><tr><td><code class="literal">all</code></td><td>
                一個方便使用的別名，等同於指定所有選項。若
                <code class="literal">all</code> 與其他選項一併列於清單中，
                所有連線相關的資訊都會被記錄。
               </td></tr></tbody></table>

    <br>

    中斷連線記錄則由 [log_disconnections](runtime-config-logging.md#GUC-LOG-DISCONNECTIONS)
    另外控制。

    為了向後相容，`on`、
    `off`、`true`、
    `false`、`yes`、
    `no`、`1`，以及 `0`
    目前仍受到支援。其中的啟用值（肯定值）等同於指定
    `receipt`、`authentication`，與
    `authorization` 選項。

    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能在工作階段開始時變更此參數，
    且在工作階段內完全無法變更。

    ### 注意

    某些用戶端程式（例如 psql）在判斷
    是否需要密碼時，會嘗試連線兩次，
    因此重複出現「connection received」訊息，
    未必代表發生了問題。
<a id="GUC-LOG-DISCONNECTIONS"></a>

`log_disconnections` (`boolean`) <a id="id-1.6.6.11.5.3.7.1.3"></a> [#](#GUC-LOG-DISCONNECTIONS)
:   使工作階段終止被記錄。日誌輸出
    提供與 `log_connections` 類似的資訊，
    並額外加上工作階段的持續時間。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能在工作階段開始時變更此參數，
    且在工作階段內完全無法變更。
    預設值為 `off`。
<a id="GUC-LOG-DURATION"></a>

`log_duration` (`boolean`) <a id="id-1.6.6.11.5.3.8.1.3"></a> [#](#GUC-LOG-DURATION)
:   使每個已完成陳述式的耗時都被記錄。
    預設值為 `off`。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。

    對於使用延伸查詢協定的用戶端，
    剖析（Parse）、綁定（Bind）與執行（Execute）步驟的耗時，
    會被各自獨立記錄。

    ### 注意

    啟用 `log_duration` 與將
    [log_min_duration_statement](runtime-config-logging.md#GUC-LOG-MIN-DURATION-STATEMENT) 設為零，
    兩者之間的差異在於：超過
    `log_min_duration_statement` 會強制記錄
    查詢文字，但此選項不會。因此，
    若 `log_duration` 為 `on`，
    而 `log_min_duration_statement` 為正值，
    則所有耗時都會被記錄，但查詢文字只會針對
    超過門檻值的陳述式加入記錄。這種行為，
    對於在高負載環境中蒐集統計資訊很有幫助。
<a id="GUC-LOG-ERROR-VERBOSITY"></a>

`log_error_verbosity` (`enum`) <a id="id-1.6.6.11.5.3.9.1.3"></a> [#](#GUC-LOG-ERROR-VERBOSITY)
:   控制伺服器日誌中，每則被記錄訊息所寫入的詳細程度。
    有效值為 `TERSE`、
    `DEFAULT`，以及 `VERBOSE`，
    各自為顯示的訊息加入更多欄位。`TERSE`
    會排除 `DETAIL`、`HINT`、
    `QUERY`，以及 `CONTEXT`
    錯誤資訊的記錄。`VERBOSE` 輸出
    包含 `SQLSTATE` 錯誤代碼
    （另請參閱 [附錄 A](../../appendixes/errcodes-appendix/README.md)），
    以及產生此錯誤的原始碼檔名、函式名稱，
    與行號。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。
<a id="GUC-LOG-HOSTNAME"></a>

`log_hostname` (`boolean`) <a id="id-1.6.6.11.5.3.10.1.3"></a> [#](#GUC-LOG-HOSTNAME)
:   依預設，連線日誌訊息只會顯示連線主機的 IP 位址。
    開啟此參數會一併記錄主機名稱。請注意，
    依你主機名稱解析的設定而定，這可能會帶來不容忽視的
    效能損耗。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。
<a id="GUC-LOG-LINE-PREFIX"></a>

`log_line_prefix` (`string`) <a id="id-1.6.6.11.5.3.11.1.3"></a> [#](#GUC-LOG-LINE-PREFIX)
:   這是一個 `printf` 樣式的字串，
    會輸出於每一行日誌的開頭。
    `%` 字元開始「逸出序列」，
    會被替換為如下所述的狀態資訊。
    無法識別的逸出序列會被忽略。其他
    字元則會直接複製到日誌行中。有些逸出序列
    僅會被工作階段程序識別，
    在主要伺服器程序等背景程序中，會被視為空字串，不產生任何輸出。
    可在 % 之後、選項之前指定一個數字字面值，
    藉此讓狀態資訊靠左或靠右對齊。負值
    會使狀態資訊在右側以空白填補，
    以達到最小寬度，而正值則會在左側填補。
    填補有助於提升日誌檔案的人工可讀性。

    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。預設值為
    `'%m [%p] '`，會記錄時間戳記與程序 ID。

    <table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>逸出序列</th><th>作用</th><th>僅限工作階段</th></tr></thead><tbody><tr><td><code class="literal">%a</code></td><td>應用程式名稱</td><td>是</td></tr><tr><td><code class="literal">%u</code></td><td>使用者名稱</td><td>是</td></tr><tr><td><code class="literal">%d</code></td><td>資料庫名稱</td><td>是</td></tr><tr><td><code class="literal">%r</code></td><td>遠端主機名稱或 IP 位址，及遠端連接埠</td><td>是</td></tr><tr><td><code class="literal">%h</code></td><td>遠端主機名稱或 IP 位址</td><td>是</td></tr><tr><td><code class="literal">%L</code></td><td>本機位址（用戶端所連線之伺服器上的
                 IP 位址）</td><td>是</td></tr><tr><td><code class="literal">%b</code></td><td>後端類型</td><td>否</td></tr><tr><td><code class="literal">%p</code></td><td>程序 ID</td><td>否</td></tr><tr><td><code class="literal">%P</code></td><td>若此程序為平行查詢工作者，
                  則為其平行群組領導者的程序 ID</td><td>否</td></tr><tr><td><code class="literal">%t</code></td><td>不含毫秒的時間戳記</td><td>否</td></tr><tr><td><code class="literal">%m</code></td><td>含毫秒的時間戳記</td><td>否</td></tr><tr><td><code class="literal">%n</code></td><td>含毫秒的時間戳記（以 Unix epoch 表示）</td><td>否</td></tr><tr><td><code class="literal">%i</code></td><td>命令標籤：工作階段目前命令的類型</td><td>是</td></tr><tr><td><code class="literal">%e</code></td><td>SQLSTATE 錯誤代碼</td><td>否</td></tr><tr><td><code class="literal">%c</code></td><td>工作階段 ID：請參閱下文</td><td>否</td></tr><tr><td><code class="literal">%l</code></td><td>每個工作階段或程序的日誌行編號，從 1 開始</td><td>否</td></tr><tr><td><code class="literal">%s</code></td><td>程序啟動時間戳記</td><td>否</td></tr><tr><td><code class="literal">%v</code></td><td>虛擬交易 ID（procNumber/localXID）；請參閱
                 <a class="xref" href="../../internals/transactions/transaction-id.md">第 67.1 節</a></td><td>否</td></tr><tr><td><code class="literal">%x</code></td><td>交易 ID（若未指派則為 0）；請參閱
                 <a class="xref" href="../../internals/transactions/transaction-id.md">第 67.1 節</a></td><td>否</td></tr><tr><td><code class="literal">%q</code></td><td>不產生任何輸出，但會告知非工作階段
                 程序在字串中此處停止；工作階段
                 程序則會忽略此逸出序列</td><td>否</td></tr><tr><td><code class="literal">%Q</code></td><td>目前查詢的查詢識別碼。查詢
                 識別碼預設不會被計算，因此除非啟用
                 <a class="xref" href="runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID">compute_query_id</a>
                 參數，或設定了會計算查詢識別碼的第三方模組，
                 否則此欄位會為零。</td><td>是</td></tr><tr><td><code class="literal">%%</code></td><td>字面值 <code class="literal">%</code></td><td>否</td></tr></tbody></table>

    後端類型對應於
    [`pg_stat_activity`](../monitoring/monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW)
    檢視表中的 `backend_type` 欄，
    但日誌中可能會出現該檢視表未顯示的其他類型。

    `%c` 逸出序列會印出一個近乎唯一的工作階段識別碼，
    由兩個以點號分隔的 4 位元組十六進位數字（不含前導零）組成。
    這兩個數字分別是程序啟動時間與
    程序 ID，因此 `%c` 也可用來作為
    印出這兩項資訊的節省空間寫法。舉例來說，
    若要從 `pg_stat_activity` 產生工作階段識別碼，
    可使用下列查詢：

    ```

    SELECT to_hex(trunc(EXTRACT(EPOCH FROM backend_start))::integer) || '.' ||
           to_hex(pid)
    FROM pg_stat_activity;
    ```

    ### 提示

    若你將 `log_line_prefix` 設為非空值，
    通常應讓其最後一個字元為空白，
    以與日誌行的其餘部分做視覺上的區隔。
    也可以使用標點符號。

    ### 提示

    Syslog 會產生自己的
    時間戳記與程序 ID 資訊，因此若你將日誌記錄到 syslog，
    可能不會想要一併包含這些逸出序列。

    ### 提示

    `%q` 逸出序列，適合用於加入僅在工作階段
    （後端）情境下才可取得的資訊，例如使用者或資料庫
    名稱。例如：

    ```

    log_line_prefix = '%m [%p] %q%u@%d/%a '
    ```

    ### 注意

    對於因 [log_statement](runtime-config-logging.md#GUC-LOG-STATEMENT)
    而輸出的行，`%Q` 逸出序列一律會回報零識別碼，
    因為 `log_statement` 會在
    識別碼能被計算之前就產生輸出，
    包括那些無法計算出識別碼的無效陳述式。
<a id="GUC-LOG-LOCK-WAITS"></a>

`log_lock_waits` (`boolean`) <a id="id-1.6.6.11.5.3.12.1.3"></a> [#](#GUC-LOG-LOCK-WAITS)
:   控制當某個工作階段等待取得鎖定的時間，
    超過 [deadlock_timeout](runtime-config-locks.md#GUC-DEADLOCK-TIMEOUT)
    時，是否要產生日誌訊息。這對於判斷鎖定等待
    是否導致效能不佳很有用。預設值為 `off`。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。
<a id="GUC-LOG-LOCK-FAILURES"></a>

`log_lock_failures` (`boolean`) <a id="id-1.6.6.11.5.3.13.1.3"></a> [#](#GUC-LOG-LOCK-FAILURES)
:   控制當鎖定取得失敗時，是否要產生詳細的日誌訊息。
    這對於分析鎖定失敗的原因很有用。
    目前僅支援因 `SELECT NOWAIT`
    而導致的鎖定失敗。
    預設值為 `off`。只有超級使用者，
    以及具備適當 `SET` 權限的
    使用者，才能變更此設定。
<a id="GUC-LOG-RECOVERY-CONFLICT-WAITS"></a>

`log_recovery_conflict_waits` (`boolean`) <a id="id-1.6.6.11.5.3.14.1.3"></a> [#](#GUC-LOG-RECOVERY-CONFLICT-WAITS)
:   控制當啟動程序因復原衝突而等待的時間，
    超過 `deadlock_timeout` 時，
    是否要產生日誌訊息。這對於判斷復原衝突
    是否阻礙了復原套用 WAL 很有用。

    預設值為 `off`。此參數只能在
    `postgresql.conf` 檔案中或伺服器
    命令列上設定。
<a id="GUC-LOG-PARAMETER-MAX-LENGTH"></a>

`log_parameter_max_length` (`integer`) <a id="id-1.6.6.11.5.3.15.1.3"></a> [#](#GUC-LOG-PARAMETER-MAX-LENGTH)
:   若大於零，每個隨非錯誤陳述式記錄訊息一併記錄的
    綁定參數值，都會被裁剪至此位元組數。
    零會停用非錯誤陳述式日誌中的綁定參數記錄。
    `-1`（預設值）允許完整記錄綁定參數。
    若此值未指定單位，則以位元組為單位。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。

    此設定僅影響因
    [log_statement](runtime-config-logging.md#GUC-LOG-STATEMENT)、
    [log_min_duration_statement](runtime-config-logging.md#GUC-LOG-MIN-DURATION-STATEMENT)
    及相關設定而印出的日誌訊息。
    此設定的非零值會增加一些額外負擔，
    尤其是當參數以二進位形式傳送時，
    因為此時需要進行轉換為文字的動作。
<a id="GUC-LOG-PARAMETER-MAX-LENGTH-ON-ERROR"></a>

`log_parameter_max_length_on_error` (`integer`) <a id="id-1.6.6.11.5.3.16.1.3"></a> [#](#GUC-LOG-PARAMETER-MAX-LENGTH-ON-ERROR)
:   若大於零，每個在錯誤訊息中回報的
    綁定參數值，都會被裁剪至此位元組數。
    零（預設值）會停用在錯誤訊息中包含綁定參數。
    `-1` 允許完整印出綁定參數。
    若此值未指定單位，則以位元組為單位。

    此設定的非零值會增加額外負擔，
    因為 PostgreSQL 需要在每個陳述式開始時，
    就將參數值的文字表示形式儲存在記憶體中，
    無論最終是否發生錯誤都一樣。當綁定參數
    以二進位形式傳送時，額外負擔會比以文字形式傳送時更大，
    因為前者需要進行資料轉換，
    而後者只需要複製字串。
<a id="GUC-LOG-STATEMENT"></a>

`log_statement` (`enum`) <a id="id-1.6.6.11.5.3.17.1.3"></a> [#](#GUC-LOG-STATEMENT)
:   控制哪些 SQL 陳述式會被記錄。有效值為
    `none`（關閉）、`ddl`、`mod`，
    以及 `all`（所有陳述式）。`ddl`
    會記錄所有資料定義陳述式，例如
    `CREATE`、`ALTER`，以及
    `DROP` 陳述式。`mod` 會記錄所有
    `ddl` 陳述式，再加上資料異動陳述式，
    例如 `INSERT`、
    `UPDATE`、`DELETE`、`TRUNCATE`，
    以及 `COPY FROM`。
    `PREPARE`、`EXECUTE`，以及
    `EXPLAIN ANALYZE` 陳述式，
    若其內含命令屬於適當類型，也會被記錄。
    對於使用延伸查詢協定的用戶端，
    記錄動作會在收到 Execute 訊息時發生，
    並會包含 Bind 參數的值
    （其中任何內嵌的單引號會加倍）。

    預設值為 `none`。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。

    ### 注意

    即使 `log_statement` 設為
    `all`，含有單純語法錯誤的陳述式
    仍不會被記錄，因為日誌訊息只有在完成基本剖析、
    判斷出陳述式類型之後才會發出。在延伸查詢協定的
    情況下，此設定同樣不會記錄在 Execute 階段之前
    就失敗的陳述式（也就是在剖析分析或規劃階段失敗的情況）。
    請將 `log_min_error_statement` 設為
    `ERROR`（或更低），以記錄這類陳述式。

    被記錄的陳述式可能會洩漏敏感資料，
    甚至包含明文密碼。
<a id="GUC-LOG-REPLICATION-COMMANDS"></a>

`log_replication_commands` (`boolean`) <a id="id-1.6.6.11.5.3.18.1.3"></a> [#](#GUC-LOG-REPLICATION-COMMANDS)
:   使每個複寫命令，以及 `walsender`
    程序的複寫插槽取得／釋放動作，
    都被記錄在伺服器日誌中。關於複寫命令的
    更多資訊，請參閱 [第 54.4 節](../../internals/protocol/protocol-replication.md)。
    預設值為
    `off`。只有超級使用者，以及具備適當
    `SET` 權限的使用者，才能變更此設定。
<a id="GUC-LOG-TEMP-FILES"></a>

`log_temp_files` (`integer`) <a id="id-1.6.6.11.5.3.19.1.3"></a> [#](#GUC-LOG-TEMP-FILES)
:   控制暫存檔案名稱與大小的記錄。
    暫存檔案可能會因排序、雜湊，
    以及暫存查詢結果而建立。
    若此設定已啟用，則每個暫存檔案在被刪除時，
    都會發出一則日誌項目，其中含有以位元組表示的檔案大小。
    設為零會記錄所有暫存檔案資訊，正值
    則只會記錄大小達到或超過指定資料量的檔案。
    若此值未指定單位，則以 KB 為單位。
    預設值為 -1，會停用此類記錄。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。
<a id="GUC-LOG-TIMEZONE"></a>

`log_timezone` (`string`) <a id="id-1.6.6.11.5.3.20.1.3"></a> [#](#GUC-LOG-TIMEZONE)
:   設定伺服器日誌中寫入時間戳記所使用的時區。
    與 [TimeZone](runtime-config-client.md#GUC-TIMEZONE) 不同，
    此值是全叢集適用的，因此所有工作階段
    回報的時間戳記都會保持一致。內建的預設值為
    `GMT`，但通常會在 `postgresql.conf`
    中被覆寫；initdb 會依系統環境
    安裝對應的設定。
    詳情請參閱 [第 8.5.3 節](../../the-sql-language/datatype/datatype-datetime.md#datatype-timezones)。
    此參數只能在 `postgresql.conf`
    檔案中或伺服器命令列上設定。

<a id="RUNTIME-CONFIG-LOGGING-CSVLOG"></a>

### 19.8.4. 使用 CSV 格式日誌輸出 [#](#runtime-config-logging-csvlog) <a href="#runtime-config-logging-csvlog" id="runtime-config-logging-csvlog"></a>

在 `log_destination` 清單中包含
`csvlog`，能提供一種方便的方式，
將日誌檔案匯入資料庫資料表。此選項會以逗號分隔值
（CSV）格式輸出日誌行，
包含下列欄位：
含毫秒的時間戳記、
使用者名稱、
資料庫名稱、
程序 ID、
用戶端主機：連接埠號碼、
工作階段 ID、
每個工作階段的行編號、
命令標籤、
工作階段開始時間、
虛擬交易 ID、
一般交易 ID、
錯誤嚴重性、
SQLSTATE 代碼、
錯誤訊息、
錯誤訊息詳情、
提示、
導致此錯誤的內部查詢（若有）、
其中錯誤位置的字元數、
錯誤上下文、
導致此錯誤的使用者查詢（若有，且已由
`log_min_error_statement` 啟用）、
其中錯誤位置的字元數、
此錯誤在 PostgreSQL 原始碼中的位置
（若 `log_error_verbosity` 設為 `verbose`）、
應用程式名稱、後端類型、平行群組領導者的程序 ID，
以及查詢識別碼。
以下是用於儲存 CSV 格式日誌輸出的資料表定義範例：

```

CREATE TABLE postgres_log
(
  log_time timestamp(3) with time zone,
  user_name text,
  database_name text,
  process_id integer,
  connection_from text,
  session_id text,
  session_line_num bigint,
  command_tag text,
  session_start_time timestamp with time zone,
  virtual_transaction_id text,
  transaction_id bigint,
  error_severity text,
  sql_state_code text,
  message text,
  detail text,
  hint text,
  internal_query text,
  internal_query_pos integer,
  context text,
  query text,
  query_pos integer,
  location text,
  application_name text,
  backend_type text,
  leader_pid integer,
  query_id bigint,
  PRIMARY KEY (session_id, session_line_num)
);
```

若要將日誌檔案匯入此資料表，請使用
`COPY FROM` 命令：

```

COPY postgres_log FROM '/full/path/to/logfile.csv' WITH csv;
```

也可以使用所提供的 [file_fdw](../../appendixes/contrib/file-fdw.md)
模組，將此檔案作為外部資料表來存取。

要簡化匯入 CSV 日誌檔案的作業，有幾件事你需要做：

1. 設定 `log_filename` 與
   `log_rotation_age`，
   為你的日誌檔案提供一致、可預測的命名方式。
   這能讓你預測檔名，並得知某個日誌檔案何時完成，
   因而可以匯入。
2. 將 `log_rotation_size` 設為 0，
   以停用以大小為基礎的日誌輪替，
   因為這會使日誌檔名難以預測。
3. 將 `log_truncate_on_rotation` 設為
   `on`，讓舊日誌資料不會與新資料混雜在
   同一個檔案中。
4. 上方的資料表定義中包含主鍵規格。這有助於
   防止意外重複匯入同一份資訊。`COPY`
   命令會一次提交其匯入的所有資料，
   因此任何錯誤都會導致整個匯入失敗。若你匯入了
   部分日誌檔案，之後在其完成後又再次匯入該檔案，
   主鍵違反就會導致匯入失敗。請等到日誌完成並關閉後
   再進行匯入。這種做法也能防止意外匯入
   尚未完全寫入的部分行，這同樣會導致
   `COPY` 失敗。

<a id="RUNTIME-CONFIG-LOGGING-JSONLOG"></a>

### 19.8.5. 使用 JSON 格式日誌輸出 [#](#runtime-config-logging-jsonlog) <a href="#runtime-config-logging-jsonlog" id="runtime-config-logging-jsonlog"></a>

在 `log_destination` 清單中包含
`jsonlog`，能提供一種方便的方式，
將日誌檔案匯入許多不同的程式。此選項會以
JSON 格式輸出日誌行。

值為 null 的字串欄位不會出現在輸出中。
未來可能會加入更多欄位。處理
`jsonlog` 輸出的使用者應用程式，
應忽略未知的欄位。

每一行日誌都會序列化為一個 JSON 物件，其中包含
[表 19.4](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG-KEYS-VALUES)
所示的鍵集合及其對應的值。

<a id="RUNTIME-CONFIG-LOGGING-JSONLOG-KEYS-VALUES"></a>

**表 19.4. JSON 日誌項目的鍵與值**

<table border="1" class="table" summary="JSON 日誌項目的鍵與值"><colgroup><col/><col/><col/></colgroup><thead><tr><th>鍵名稱</th><th>類型</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">timestamp</code></td><td>string</td><td>含毫秒的時間戳記</td></tr><tr><td><code class="literal">user</code></td><td>string</td><td>使用者名稱</td></tr><tr><td><code class="literal">dbname</code></td><td>string</td><td>資料庫名稱</td></tr><tr><td><code class="literal">pid</code></td><td>number</td><td>程序 ID</td></tr><tr><td><code class="literal">remote_host</code></td><td>string</td><td>用戶端主機</td></tr><tr><td><code class="literal">remote_port</code></td><td>number</td><td>用戶端連接埠</td></tr><tr><td><code class="literal">session_id</code></td><td>string</td><td>工作階段 ID</td></tr><tr><td><code class="literal">line_num</code></td><td>number</td><td>每個工作階段的行編號</td></tr><tr><td><code class="literal">ps</code></td><td>string</td><td>目前的 ps 顯示內容</td></tr><tr><td><code class="literal">session_start</code></td><td>string</td><td>工作階段開始時間</td></tr><tr><td><code class="literal">vxid</code></td><td>string</td><td>虛擬交易 ID</td></tr><tr><td><code class="literal">txid</code></td><td>string</td><td>一般交易 ID</td></tr><tr><td><code class="literal">error_severity</code></td><td>string</td><td>錯誤嚴重性</td></tr><tr><td><code class="literal">state_code</code></td><td>string</td><td>SQLSTATE 代碼</td></tr><tr><td><code class="literal">message</code></td><td>string</td><td>錯誤訊息</td></tr><tr><td><code class="literal">detail</code></td><td>string</td><td>錯誤訊息詳情</td></tr><tr><td><code class="literal">hint</code></td><td>string</td><td>錯誤訊息提示</td></tr><tr><td><code class="literal">internal_query</code></td><td>string</td><td>導致此錯誤的內部查詢</td></tr><tr><td><code class="literal">internal_position</code></td><td>number</td><td>內部查詢中的游標索引</td></tr><tr><td><code class="literal">context</code></td><td>string</td><td>錯誤上下文</td></tr><tr><td><code class="literal">statement</code></td><td>string</td><td>用戶端提供的查詢字串</td></tr><tr><td><code class="literal">cursor_position</code></td><td>number</td><td>查詢字串中的游標索引</td></tr><tr><td><code class="literal">func_name</code></td><td>string</td><td>錯誤位置的函式名稱</td></tr><tr><td><code class="literal">file_name</code></td><td>string</td><td>錯誤位置的檔案名稱</td></tr><tr><td><code class="literal">file_line_num</code></td><td>number</td><td>錯誤位置的檔案行號</td></tr><tr><td><code class="literal">application_name</code></td><td>string</td><td>用戶端應用程式名稱</td></tr><tr><td><code class="literal">backend_type</code></td><td>string</td><td>後端類型</td></tr><tr><td><code class="literal">leader_pid</code></td><td>number</td><td>作用中平行工作者之領導者的程序 ID</td></tr><tr><td><code class="literal">query_id</code></td><td>number</td><td>查詢 ID</td></tr></tbody></table>

<br>

<a id="RUNTIME-CONFIG-LOGGING-PROC-TITLE"></a>

### 19.8.6. 程序標題 [#](#runtime-config-logging-proc-title) <a href="#runtime-config-logging-proc-title" id="runtime-config-logging-proc-title"></a>

這些設定控制伺服器程序的程序標題會如何被修改。
程序標題通常透過 ps 等程式檢視，
或在 Windows 上，透過 Process Explorer 檢視。
詳情請參閱 [第 27.1 節](../monitoring/monitoring-ps.md)。

<a id="GUC-CLUSTER-NAME"></a>

`cluster_name` (`string`) <a id="id-1.6.6.11.8.3.1.1.3"></a> [#](#GUC-CLUSTER-NAME)
:   設定一個用於各種用途、識別此資料庫叢集（執行個體）
    的名稱。叢集名稱會出現在此叢集所有伺服器程序的
    程序標題中。此外，它也是待命連線的
    預設應用程式名稱（請參閱
    [synchronous_standby_names](runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES)）。

    此名稱可以是任何長度小於
    `NAMEDATALEN` 個字元（標準組建中為 64 個字元）的字串。
    `cluster_name` 值只能使用
    可列印的 ASCII 字元。
    其他字元會被替換為
    [C 樣式十六進位逸出序列](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE)。
    若此參數設為空字串
    `''`（此為預設值），則不會顯示任何名稱。
    此參數只能在伺服器啟動時設定。
<a id="GUC-UPDATE-PROCESS-TITLE"></a>

`update_process_title` (`boolean`) <a id="id-1.6.6.11.8.3.2.1.3"></a> [#](#GUC-UPDATE-PROCESS-TITLE)
:   啟用每當伺服器收到新的 SQL 命令時，
    就更新程序標題的功能。
    此設定在多數平台上預設為 `on`，
    但在 Windows 上，由於該平台更新程序標題的
    額外負擔較大，因此預設為 `off`。
    只有超級使用者，以及具備適當 `SET`
    權限的使用者，才能變更此設定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-logging.html)（原文版本：18.6；核對日期：2026-10-23）
