# 19.8. 錯誤回報與日誌記錄

## 19.8.1. 記錄在哪裡

### `log_destination` \(`string`\)

PostgreSQL 支援多種記錄伺服器訊息的方法，包括 stderr、csvlog 和 syslog。在 Windows 上，支援 eventlog。 將此參數設定為用逗號分隔的所需日誌目標的列表。 預設情況下僅記錄到 stderr。此參數只能在 postgresql.conf 檔案或伺服器命令中設定。

如果 csvlog 包含在 log\_destination 中的話，則日誌將以「逗號分隔」（CSV）格式輸出，便於將日誌載入到其他程序中。詳情請參閱[第 19.8.4 節](error-reporting-and-logging.md#19-8-4-using-csv-format-log-output)。 必須啟用 [logging\_collector ](error-reporting-and-logging.md#logging_collector-boolean)才能産生 CSV 格式的日誌輸出。

如果包含 stderr 或 csvlog，則會建立 current\_logfiles 檔案以記錄日誌記錄收集器和相關日誌記錄目標目前正在使用的日誌檔案的位置。這提供了一種便捷的方式來查詢目前資料庫實例正在使用的日誌。這裡有這個檔案內容的一個例子：

```text
stderr log/postgresql.log
csvlog log/postgresql.csv
```

當一個新的日誌檔案被建立為循環的效果，並且重新載入 log\_destination 時，會重新建立 current\_logfiles。當 log\_destination 中不包含 stderr 和 csvlog，並且日誌記錄收集器被停用時，它將被刪除。

### 注意

在大多數 Unix 系統上，您需要變更系統 syslog daemon 的配置，以便使用 log\_destination 的 syslog 選項。PostgreSQL 可以登入到系統日誌工具 LOCAL0 到 LOCAL7（請參閱 [syslog\_facility](error-reporting-and-logging.md#syslog_facility-enum)），但大多數平台上的預設 syslog 配置將放棄所有此類訊息。您需要加入如下的內容：

```text
local0.*    /var/log/postgresql
```

變更 syslog 背景程序的配置檔案以使其産生作用。

在 Windows 上，當您為 log\_destination 使用 eventlog 選項時，應該向作業系統註冊事件來源及其函式庫，以便 Windows 事件查詢器可以清楚地顯示事件日誌消息。詳情請參閱[第 18.11 節](../server-setup-and-operation/18.11.-zai-windows-zhu-ce-shi-jian-ri-zhi.md)。

### `logging_collector` \(`boolean`\)

此參數啟用日誌收集器，這是一個後端的程序，用於攔截發送到 stderr 的日誌訊息並將其重新輸出到日誌檔案。這種方法通常比記錄到 syslog 更有用，因為某些類型的訊息可能不會出現在 syslog 輸出之中。（一個常見的案例是動態連結程序失敗訊息；另一個案例是由如 archive\_command 等腳本産生的錯誤訊息。）此參數只能在伺服器啟動時設定。

### 注意

可以在不使用日誌收集器的情況下送到 stderr；日誌訊息將只發送到伺服器的 stderr 所指向的任何地方。但是，該方法僅適用於較低階的日誌程序，因為它不提供日誌檔案覆寫的簡便方法。另外，在某些不使用日誌收集器的平台上可能會導致日誌輸出遺失或出現亂碼，因為同時寫入同一日誌檔案的多個程序可能會覆蓋彼此的輸出。

### 注意

日誌記錄收集器旨在永不遺失訊息。這意味著，如果負載極高，則在收集器落後時嘗試發送其他日誌消息時，伺服器程序可能會被阻止繼續執行。相比之下，如果系統日誌不能寫入訊息，系統日誌更喜歡丟棄訊息，這意味著在這種情況下它可能無法記錄某些訊息，但不會阻塞系統的其餘部分。

### `log_directory` \(`string`\)

當啟用 logging\_collector 時，此參數確定將在其中建立日誌檔案的目錄。它可以被指定為絕對路徑，或相對於叢集的 data 目錄。該參數只能在 postgresql.conf 檔案或伺服器指令行中設定。預設值是 log。

### `log_filename` \(`string`\)

當啟用 logging\_collector 時，此參數設定建立的日誌檔案的檔案名稱。該值被視為 strftime 模式，因此 ％-escapes 可用於指定隨時間變化的檔案名稱。（請注意，如果有任何時區相關的 ％-escapes，計算將在由 [log\_timezone](error-reporting-and-logging.md#log_timezone-string) 指定的區域中完成。）支援的 ％-escapes 與 Open Group 的 [strftime](http://pubs.opengroup.org/onlinepubs/009695399/functions/strftime.html) 規範中列出的類似。請注意，系統的 strftime 並未直接使用，因此特定於平台的（非標準）延伸功能不起作用。預設值是 postgresql-％Y-％m-％d\_％H％M％S.log。

如果您指定的檔案名稱不含跳脫符號，則應該計劃使用日誌覆寫程序來避免最後存滿整個磁碟。在 8.4 之前的版本中，如果不存在 ％ 跳脫符號，PostgreSQL 會追加新日誌檔案建立時間的紀元，但已經不再是這種情況了。

如果在 log\_destination 中啟用 CSV 格式的輸出，則會將時間戳記檔案名稱附加.csv 以建立 CSV 格式輸出的檔案名稱。 （如果 log\_filename 以 .log 結尾，則替換後綴。）

該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

### `log_file_mode` \(`integer`\)

在 Unix 系統上，此參數在啟用 logging\_collector 時設定日誌檔案的權限。（在 Microsoft Windows 上，此參數將被忽略。）參數值預期為以 chmod 和 umask 系統呼叫接受的格式來指定的數字模式。（要使用習慣的八進制格式，數字必須以 0（零）開頭。）

預設權限為 0600，這意味著只有伺服器擁有者才能讀取或寫入日誌檔案。另一個常用的設定是 0640，允許擁有者組群的成員讀取文件。 但是請注意，要使用這種設定，您需要變更 log\_directory 以將檔案儲存在叢集 data 目錄之外的某個位置。無論如何，使日誌檔案讓任何人都可讀是不明智的，因為它們可能包含敏感資料。

該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

### `log_rotation_age` \(`integer`\)

當啟用 logging\_collector 時，此參數決定單個日誌檔案的最長生命週期。經過指定的分鐘後，會建立一個新的日誌檔案。設定為零以停用基於時間的新日誌檔案建立。該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

### `log_rotation_size` \(`integer`\)

當啟用 logging\_collector 時，此參數決定單個日誌檔的大小上限。在超過上限的記錄被發送到日誌檔案後，將建立一個新的日誌檔案。設定為零以禁用基於大小的新日誌檔案創立。該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

### `log_truncate_on_rotation` \(`boolean`\)

當啟用 logging\_collector 時，此參數將導致 PostgreSQL 分割（覆蓋）而不是追加到任何具有相同名稱的現有日誌檔案。 但是，分割只會在由於基於時間的覆寫而打開新檔案時發生，而不是在伺服器啟動或基於大小的覆寫情況進行。關閉時，預先存在的檔案將被附加到所有情況下。例如，將此設定與 log\_filename（如 postgresql-％H.log）結合使用可産生 24 個小時日誌檔案，然後循環覆蓋它們。該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

例如：要保留 7 天的日誌，每天一個名稱為 server\_log.Mon，server\_log.Tue 等的日誌檔案，並自動使用本週的日誌覆蓋上週的日誌，將 log\_filename 設定為server\_log.％a，將 log\_truncate\_on\_rotation 設定為 on，並將 log\_rotation\_age 到 1440。

又例如：要保留 24 小時的日誌，每小時記錄一個日誌檔案，但是如果日誌檔案大小超過 1GB，則會盡快輪換，將 log\_filename 設定為 server\_log.％H％M，log\_truncate\_on\_rotation 為 on，log\_rotation\_age 為 60，log\_rotation\_size 為1000000。在 log\_filename 中包含 ％M 允許可能出現的任何大小驅動的旋轉，以選擇與小時的初始檔案名稱不同的檔案名稱。

### `syslog_facility` \(`enum`\)

當啟用日誌記錄到 syslog 時，此參數確定要使用的系統日誌的「設施」。 您可以選擇 LOCAL0，LOCAL1，LOCAL2，LOCAL3，LOCAL4，LOCAL5，LOCAL6，LOCAL7；預設值是 LOCAL0。另請參閱系統的 syslog 背景程序的文件。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

### `syslog_ident` \(`string`\)

當啟用日誌記錄到系統日誌時，此參數決定用於在系統日誌中識別 PostgreSQL 記錄的程序名稱。預設是 postgres。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

### `syslog_sequence_numbers` \(`boolean`\)

當記錄到系統日誌並且這是啓用的（預設），那麼每筆記錄將以遞增的序列號碼（例如\[2\]）作為前置內容。這規避了「---最後一條記錄重複 N 次---」抑制了許多 syslog 實務上預設執行的操作。在更現代的 syslog 實作中，可以設定重複的記錄抑制（例如，rsyslog 中的 $RepeatedMsgReduction），所以這可能不是必要的。另外，如果你真的想要抑制重複的記錄，就可以關掉它。

此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

### `syslog_split_messages` \(`boolean`\)

當啟用日誌記錄到 syslog 時，此參數決定記錄如何傳遞到系統日誌。啟用時（預設），記錄按行分割，使得行長在 1024 字元以下，這是傳統 syslog 實作的典型大小限制。關閉時，PostgreSQL 伺服器日誌記錄會按原樣傳遞到系統日誌服務，並由系統日誌服務來處理潛在的龐大記錄。

如果 syslog 最終記錄到文字檔案，那麼效果將是相同的，並且最好將設定保留為開啟狀態，因為大多數 syslog 實作無法處理大量記錄，或者需要專門設定以處理它們。但是，如果系統日誌最終寫入其他媒體，將記錄邏輯上地組合在一起可能是必要的或更有用的。

此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

### `event_source` \(`string`\)

當啟用記錄到事件日誌時，此參數確定用於在記錄中識別 PostgreSQL 記錄的程序名稱。預設是 PostgreSQL。 此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

## 19.8.2. 何時要記錄

### `client_min_messages` \(`enum`\)

控制將哪些訊息等級要發送到用戶端。有效的值為 DEBUG5、DEBUG4、DEBUG3、DEBUG2、DEBUG1、LOG、NOTICE、WARNING、ERROR、FATAL 和 PANIC。每個等級包括其後的所有等級。等級越低，發送的訊息越少。預設值為 NOTICE。請注意，LOG 在此處的排名與 log\_min\_messages 中的排序不同。

### `log_min_messages` \(`enum`\)

控制將哪些訊息等級寫入伺服器日誌。有效的值為 DEBUG5、DEBUG4、DEBUG3、DEBUG2、DEBUG1、INFO、NOTICE、WARNING、ERROR、LOG、FATAL 和 PANIC。每個等級包括其後的所有等級。等級越低，發送到日誌的訊息越少。預設值為 WARNING。請注意，LOG 在此處的排序與 client\_min\_messages 中的排名不同。只有超級使用者才能變更此設定。

### `log_min_error_statement` \(`enum`\)

將導致錯誤情況的 SQL 語句記錄在伺服器日誌中。當下的 SQL 語句包含在指定的嚴重性或更高等級的任何訊息日誌項目中。有效值為 DEBUG5、DEBUG4、DEBUG3、DEBUG2、DEBUG1、INFO、NOTICE、WARNING、ERROR、LOG、FATAL 和 PANIC。預設值為 ERROR，這意味著將會記錄 ERROR、LOG、FATL 或 PANIC。要有效地關閉失敗語句的日誌記錄，請將此參數設定為PANIC。只有超級使用者才能變更此設定。

### `log_min_duration_statement` \(`integer`\)

如果語句執行達到指定的毫秒數，則會記錄每個已完成語句的執行時間。將此值設定為零將輸出所有語句的執行時間。減號（預設值）停用日誌記錄語句執行時間。例如，如果將其設定為 250ms，則將記錄執行 250ms 或更長時間的所有 SQL 語句。啟用此參數有助於在應用程序中追踪未優化的查詢。只有超級使用者才能變更此設定。

對於使用延伸查詢協議的用戶端，Parse、Bind 和 Execute 步驟的執行時間是獨立記錄的。

### 注意

將此選項與 log\_statement 一起使用時，由於 log\_statement 而記錄的語句文字將不會在執行時間日誌訊息中重複。如果您不使用 syslog，建議您使用 log\_line\_prefix 記錄 PID 或連線 ID，以便可以使用 PID 或連線 ID將語句訊息連接到之後的執行時間訊息。

[表格 19.1 ](error-reporting-and-logging.md#table-19-1-message-severity-levels)說明了 PostgreSQL 使用的訊息嚴重性等級。如果將日誌記錄輸出發送到 syslog 或 Windows 的事件日誌，則嚴重性等級將按表格中所示進行轉換。

### **Table 19.1. Message Severity Levels**

| Severity | Usage | syslog | eventlog |
| :--- | :--- | :--- | :--- |
| `DEBUG1..DEBUG5` | 提供連續且更詳細的訊息供開發人員使用。 | `DEBUG` | `INFORMATION` |
| `INFO` | 提供隱含用戶請求的訊息，例如來自 VACUUM VERBOSE 的輸出。 | `INFO` | `INFORMATION` |
| `NOTICE` | 提供可能對用戶有幫助的訊息，例如，截斷 long identifier 的通知。 | `NOTICE` | `INFORMATION` |
| `WARNING` | 提供可能出現問題的警告，例如交易事務區塊外的 COMMIT。 | `NOTICE` | `WARNING` |
| `ERROR` | 回報導致當下指令中止的錯誤。 | `WARNING` | `ERROR` |
| `LOG` | 回報管理員感興趣的訊息，例如檢查點的活動。 | `INFO` | `INFORMATION` |
| `FATAL` | 回報導致當下連線中止的錯誤。 | `ERR` | `ERROR` |
| `PANIC` | 回報導致所有資料庫連線中止的錯誤。 | `CRIT` | `ERROR` |

## 19.8.3. 要記錄什麼

### `application_name` \(`string`\)

application\_name 可以是少於 NAMEDATALEN 個字元的任何字串（標準版本中為 64 個字元）。它通常由應用程序在連線到伺服器時設定。此名稱將顯示在 pg\_stat\_activity 檢視表中，並包含在 CSV 日誌項目中。它還可以透過 [log\_line\_prefix](error-reporting-and-logging.md#log_line_prefix-string) 參數包含在日常日誌項目中。application\_name 中只能使用可列印的 ASCII 字元。其他字元將替換為問號（？）。

### `debug_print_parse` \(`boolean`\)  `debug_print_rewritten` \(`boolean`\)  `debug_print_plan` \(`boolean`\)

這些參數可以發出各種除錯輸出。設定後，它們將輸出産生的語法解析樹，查詢重寫程序輸出或每個已執行查詢的執行計劃。這些訊息以 LOG 訊息等級發出，因此預設情況下它們將顯示在伺服器日誌中，但不會發送到客戶端。您可以透過調整 [client\_min\_messages](error-reporting-and-logging.md#client_min_messages-enum) 或 [log\_min\_messages](error-reporting-and-logging.md#log_min_messages-enum) 來變更它。這些參數預設是關閉的。

### `debug_pretty_print` \(`boolean`\)

設定後，debug\_pretty\_print 會放進 debug\_print\_parse，debug\_print\_rewritten 或debug\_print\_plan 産生的訊息。與關閉時使用的緊湊格式相比，這會產生更多可讀但更長的輸出。它預設開啟。

### `log_checkpoints` \(`boolean`\)

使檢查點和重新啟動點記錄在伺服器日誌中。日誌訊息中包含一些統計訊息，包括寫入的緩衝區數和寫入時間。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設為關閉。

### `log_connections` \(`boolean`\)

導致記錄每個嘗試連線到伺服器，以及成功完成用戶端身份驗證。只有超級使用者才能在連線開始時變更此參數，之後在連線中無法更改。預設為關閉。

**注意**  
某些用戶端程序（如 psql）在確定是否需要密碼時會嘗試連線兩次，因此重複的“connection received”訊息不一定表示存在問題。

### `log_disconnections` \(`boolean`\)

導致連線終止會被記錄。日誌輸出提供類似於 log\_connections 的訊息，以及連線的持續時間。只有超級使用者才能在連線開始時變更此參數，並且在連線中無法更改。預設為關閉。

### `log_duration` \(`boolean`\)

記錄每個已完成語句的持續時間。預設為關閉。只有超級使用者才能變更此設定。

對於使用延伸查詢協議的用戶端，Parse、Bind 和 Execute 步驟的持續時間是獨立記錄的。

**注意**  
設定選項和將 log\_min\_duration\_statement 設定為零之間的區別在於，超出 [log\_min\_duration\_statement](error-reporting-and-logging.md#log_min_duration_statement-integer) 會強制記錄查詢的語句，但此選項不會。因此，如果啟用了 log\_duration 且 log\_min\_duration\_statement 具有正值，則會記錄所有持續時間，但僅包含超過閾值的語句的查詢語句。此行為對於在高負載環境中收集統計訊息非常有用。

### `log_error_verbosity` \(`enum`\)

控制記錄的每條訊息在伺服器日誌中寫入的詳細訊息量。有效值為 TERSE，DEFAULT 和 VERBOSE，每個都向顯示的訊息加上更多內容。TERSE 排除記錄DETAIL，HINT，QUERY 和 CONTEXT 錯誤訊息。VERBOSE 輸出包括 SQLSTATE 錯誤代碼（另請參閱[附錄 A](../../appendixes/postgresql-error-codes.md)）以及産生錯誤的原始檔案名稱，函數名稱和行號。只有超級使用者才能更改此設定。

### `log_hostname` \(`boolean`\)

預設情況下，連線日誌訊息僅顯示連線主機的 IP 位址。打開此參數就會記錄主機名。請注意，根據您的主機名稱解析設定，這可能會造成不可忽視的效能損失。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

### `log_line_prefix` \(`string`\)

這是一個 printf 樣式的字串，在每個日誌的開頭輸出。%字元開始「跳脫序列（escape sequence）」，它們會被狀態訊息替換，如下所述。 無法識別的跳脫字元會被忽略。其他字元將直接複製到日誌內容。某些跳脫字元只能由連線程序識別，並且將被背景程序（例如主伺服器程序）視為空。透過在 % 之後和選項之前指定數字文字，可以向左或向右對齊狀態訊息。負值會將狀態信息在右側填充空格以給予一個最小寬度，而正值將填充在左側。填充可用於增加日誌檔案中的可讀性。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設值為'%m \[%p\]'，用於記錄時間戳記和程序 ID。

| Escape | Effect | Session only |
| :--- | :--- | :--- |
| `%a` | 應用名稱 | yes |
| `%u` | 使用者名稱 | yes |
| `%d` | 資料庫名稱 | yes |
| `%r` | 遠端主機名稱或 IP 位址，以及遠端連接埠 | yes |
| `%h` | 遠端主機名稱或 IP 位址 | yes |
| `%p` | 程序 ID | no |
| `%t` | 時間戳記，不含毫秒 | no |
| `%m` | 時間戳記，包含毫秒 | no |
| `%n` | 時間戳記，包含毫秒（Unix epoch） | no |
| `%i` | 指令標記：連線的當下指令類型 | yes |
| `%e` | SQLSTATE 錯誤代碼 | no |
| `%c` | 連線 ID：詳見下文 | no |
| `%l` | 每個連線或程序的日誌行號，從 1 開始 | no |
| `%s` | 開始處理的時間戳記 | no |
| `%v` | 虛擬交易事務 ID（backendID / localXID） | no |
| `%x` | 交易事務 ID（如果沒有分配，則為 0） | no |
| `%q` | 不產生輸出，但告訴非連線程序在此字串中停止；被連線中程序忽略 | no |
| `%%` | 文字 `%` | no |

%c 跳脫字元輸出一個幾乎唯一的連線指標，兩個由點分隔的 4 位元組的十六進制數字（不帶前導零）組成。數字是流程開始時間和程序 ID，因此 %c 也可以用作輸出這些項目的節省空間的方式。例如，要從 pg\_stat\_activity 産生連線指標，請使用以下查詢：

```text
SELECT to_hex(trunc(EXTRACT(EPOCH FROM backend_start))::integer) || '.' ||
       to_hex(pid)
FROM pg_stat_activity;
```

**小技巧**  
如果為 log\_line\_prefix 設定了非空值，則通常應將其最後一個字元設為空格，以便與日誌行的其餘部分進行視覺隔離。也可以使用標點符號。

**小技巧**  
Syslog 會産生成自己的時間戳記和程序 ID 訊息，因此如果要輸出到 syslog，可能不希望包含這些跳脫字元。

**小技巧**  
當包含僅在使用者或資料庫名稱等連線（後端）內容中可用的訊息時，%q 跳脫字元非常有用。例如：

```text
log_line_prefix = '%m [%p] %q%u@%d/%a '
```

### `log_lock_waits` \(`boolean`\)

控制連線等待時間超過 [deadlock\_timeout](19.12.-jiao-yi-suo-ding-guan-li.md) 時是否產生日誌訊息。這對於確定鎖定等待是否導致性能較差很有用。預設是關閉的。只有超級使用者可以變更此設定。

### `log_statement` \(`enum`\)

控制記錄哪些 SQL 語句。有效值為 none（off），ddl，mod 和 all（所有語句）。 ddl 記錄所有資料定義語句，例如 CREATE，ALTER 和 DROP 語句。mod 記錄所有 ddl 語句，以及 INSERT，UPDATE，DELETE，TRUNCATE 和 COPY FROM 等資料修改語句。如果包含的指令屬於適合的類型，也會記錄 PREPARE，EXECUTE 和 EXPLAIN ANALYZE 語句。對於使用延伸查詢協議的用戶端，在收到 Execute 訊息時會發生日誌記錄，並且包含 Bind 參數的值（任何嵌入的單引號標記加倍）。

預設值為 none。只有超級使用者才能變更此設定。

**注意**  
即使是 log\_statement = all 設定也不會記錄包含簡單語法錯誤的語句，因為只有在完成基本分析以確定語句類型後才會發出日誌訊息。在延伸查詢協議的情況下，此設定同樣不記錄在執行階段之前失敗的語句（即，在解析分析或計劃期間）。將 log\_min\_error\_statement 設定為 ERROR（或更低）以記錄此類語句。

### `log_replication_commands` \(`boolean`\)

讓每個複寫指令都記錄在伺服器日誌中。有關複寫指令的更多訊息，請參閱[第 52.4 節](../../internals/52.-frontend-backend-protocol/52.4.-streaming-replication-protocol.md)。預設值為 off。只有超級使用者才能變更此設定。

### `log_temp_files` \(`integer`\)

控制臨時檔案名稱和大小的記錄。可以為排序，雜湊和臨時查詢結果建立臨時檔案。移除時，會為每個臨時檔案建立一個日誌項目。值為 0 時會記錄所有臨時檔案訊息，而正值僅記錄大小大於或等於指定 KB 的檔案。預設設定為 -1，停用此類日誌記錄。只有超級使用者才能變更此設定。

### `log_timezone` \(`string`\)

設定用於在伺服器日誌中寫入的時間戳記的時區。與 [TimeZone](client-connection-defaults.md#timezone-string) 不同，此值是叢集範圍的，因此所有連線都將一致地報告時間戳記。內建的預設值是 GMT，但這通常在 postgresql.conf 中會再設定過；initdb 將在那裡安裝與其系統環境相對應的設定。有關更多訊息，請參閱[第 8.5.3 節](../../the-sql-language/data-types/date-time.md#8-5-3-time-zones)。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

## 19.8.4. 使用 CSV 格式輸出記錄

在 log\_destination 列表中包含 csvlog 提供了將日誌檔案匯入資料庫資料表的便捷方法。此選項以逗號分隔（CSV）格式送出日誌資料，其中包含以下欄位：時間戳記，毫秒，使用者名稱，資料庫名稱，程序 ID，用戶端主機：連接埠號號，連線 ID，每個連線的行號，指令標記，連線開始時間，虛擬交易事務 ID，一般交易事務 ID，錯誤嚴重性，SQLSTATE 代碼，錯誤訊息，錯誤訊息的詳細訊息，提示，導致錯誤的內部查詢（如果有的話），其中錯誤位置的字串位置，錯誤內容，導致錯誤的使用者查詢（如果有的話，由 log\_min\_error\_statement 啟用），其中錯誤位置的字元數，PostgreSQL 原始碼中的錯誤位置（如果 log\_error\_verbosity 設定為 verbose）和應用程序名稱。以下是用於儲存 CSV 格式日誌輸出的範例資料表定義：

```text
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
  PRIMARY KEY (session_id, session_line_num)
);
```

要將日誌檔案匯入此資料表，請使用 COPY FROM 指令：

```text
COPY postgres_log FROM '/full/path/to/logfile.csv' WITH csv;
```

您需要做一些事情來簡化匯入 CSV 日誌檔案：

1. 設定 log\_filename 和 log\_rotation\_age 使日誌檔案提供一致性，可預測的命名方案。這使您可以預測檔案名稱會是什麼，並知道單個日誌檔案何時完成而可以匯入。
2. 將 log\_rotation\_size 設定為 0 可停用基於大小的日誌輪轉，因為它會使日誌檔案名稱難以預測。
3. 將 log\_truncate\_on\_rotation 設定為 on，以便舊的日誌資料不會與同一檔案中的新資料混合。
4. 上面的資料表定義包含主鍵規範。這有助於防止意外匯入兩次相同的訊息。COPY 指令一次提交它匯入的所有資料，因此任何錯誤都會導致整個匯入失敗。如果匯入部分日誌檔案，並在稍後再次匯入該檔案時，主鍵重覆將導致匯入失敗。請等到日誌完成關閉後再匯入。此過程還可以防止意外匯入尚未完全寫入的部分資料列，這也會導致 COPY 失敗。

## 19.8.5. 程序標題（Process Title）

這些設定控制如何修改伺服器程序的程序標題。程序標題通常使用如 ps 或 Windows 上的 Process Explorer 查看。詳情請參閱[第 28.1 節](../monitoring-database-activity/standard-unix-tools.md)。

### `cluster_name` \(`string`\)

設定此叢集中所有伺服器程序的程序標題中顯示的叢集名稱。該名稱可以是任何少於 NAMEDATALEN 字元數的字串（標準版本中為 64 個字元）。cluster\_name 值中只能使用可列印的 ASCII 字元。其他字元將被替換為問號（？）。如果此參數設定為空字串“”（這是預設值），則不顯示名稱。此參數只能在伺服器啟動時設定。

### `update_process_title` \(`boolean`\)

每當伺服器收到新的 SQL 指令時，都可以更新程序標題。此設定在大多數平台上預設為開啟，不過在 Windows 上預設為關閉，因為在 Windows 上更新程序標題的開銷較大。只有超級使用者可以變更此設定。

