---
description: 版本：10
---

# 19.8. 錯誤回報與日誌記錄

## 19.8.1. 記錄在哪裡

#### `log_destination` \(`string`\)

PostgreSQL 支援多種記錄伺服器訊息的方法，包括 stderr、csvlog 和 syslog。在 Windows 上，支援 eventlog。 將此參數設定為用逗號分隔的所需日誌目標的列表。 預設情況下僅記錄到 stderr。此參數只能在 postgresql.conf 檔案或伺服器命令中設定。

如果 csvlog 包含在 log\_destination 中的話，則日誌將以「逗號分隔」（CSV）格式輸出，便於將日誌載入到其他程序中。詳情請參閱[第 19.8.4 節](error-reporting-and-logging.md#19-8-4-using-csv-format-log-output)。 必須啟用 [logging\_collector ](error-reporting-and-logging.md#logging_collector-boolean)才能産生 CSV 格式的日誌輸出。

如果包含 stderr 或 csvlog，則會建立 current\_logfiles 檔案以記錄日誌記錄收集器和相關日誌記錄目標目前正在使用的日誌檔案的位置。這提供了一種便捷的方式來查詢目前資料庫實例正在使用的日誌。這裡有這個檔案內容的一個例子：

```text
stderr log/postgresql.log
csvlog log/postgresql.csv
```

當一個新的日誌檔案被建立為循環的效果，並且重新載入 log\_destination 時，會重新建立 current\_logfiles。當 log\_destination 中不包含 stderr 和 csvlog，並且日誌記錄收集器被停用時，它將被刪除。

#### 注意

在大多數 Unix 系統上，您需要變更系統 syslog daemon 的配置，以便使用 log\_destination 的 syslog 選項。PostgreSQL 可以登入到系統日誌工具 LOCAL0 到 LOCAL7（請參閱 [syslog\_facility](error-reporting-and-logging.md#syslog_facility-enum)），但大多數平台上的預設 syslog 配置將放棄所有此類訊息。您需要加入如下的內容：

```text
local0.*    /var/log/postgresql
```

變更 syslog 背景程序的配置檔案以使其産生作用。

在 Windows 上，當您為 log\_destination 使用 eventlog 選項時，應該向作業系統註冊事件來源及其函式庫，以便 Windows 事件查詢器可以清楚地顯示事件日誌消息。詳情請參閱[第 18.11 節](../18.-fu-wu-pei-zhi-yu-wei-yun/18.11.-zai-windows-zhu-ce-shi-jian-ri-zhi.md)。

#### `logging_collector` \(`boolean`\)

此參數啟用日誌收集器，這是一個後端的程序，用於攔截發送到 stderr 的日誌訊息並將其重新輸出到日誌檔案。這種方法通常比記錄到 syslog 更有用，因為某些類型的訊息可能不會出現在 syslog 輸出之中。（一個常見的案例是動態連結程序失敗訊息；另一個案例是由如 archive\_command 等腳本産生的錯誤訊息。）此參數只能在伺服器啟動時設定。

#### 注意

可以在不使用日誌收集器的情況下送到 stderr；日誌訊息將只發送到伺服器的 stderr 所指向的任何地方。但是，該方法僅適用於較低階的日誌程序，因為它不提供日誌檔案覆寫的簡便方法。另外，在某些不使用日誌收集器的平台上可能會導致日誌輸出遺失或出現亂碼，因為同時寫入同一日誌檔案的多個程序可能會覆蓋彼此的輸出。

#### 注意

日誌記錄收集器旨在永不遺失訊息。這意味著，如果負載極高，則在收集器落後時嘗試發送其他日誌消息時，伺服器程序可能會被阻止繼續執行。相比之下，如果系統日誌不能寫入訊息，系統日誌更喜歡丟棄訊息，這意味著在這種情況下它可能無法記錄某些訊息，但不會阻塞系統的其餘部分。

#### `log_directory` \(`string`\)

當啟用 logging\_collector 時，此參數確定將在其中建立日誌檔案的目錄。它可以被指定為絕對路徑，或相對於叢集的 data 目錄。該參數只能在 postgresql.conf 檔案或伺服器指令行中設定。預設值是 log。

#### `log_filename` \(`string`\)

當啟用 logging\_collector 時，此參數設定建立的日誌檔案的檔案名稱。該值被視為 strftime 模式，因此 ％-escapes 可用於指定隨時間變化的檔案名稱。（請注意，如果有任何時區相關的 ％-escapes，計算將在由 [log\_timezone](error-reporting-and-logging.md#log_timezone-string) 指定的區域中完成。）支援的 ％-escapes 與 Open Group 的 [strftime](http://pubs.opengroup.org/onlinepubs/009695399/functions/strftime.html) 規範中列出的類似。請注意，系統的 strftime 並未直接使用，因此特定於平台的（非標準）延伸功能不起作用。預設值是 postgresql-％Y-％m-％d\_％H％M％S.log。

如果您指定的檔案名稱不含跳脫符號，則應該計劃使用日誌覆寫程序來避免最後存滿整個磁碟。在 8.4 之前的版本中，如果不存在 ％ 跳脫符號，PostgreSQL 會追加新日誌檔案建立時間的紀元，但已經不再是這種情況了。

如果在 log\_destination 中啟用 CSV 格式的輸出，則會將時間戳記檔案名稱附加.csv 以建立 CSV 格式輸出的檔案名稱。 （如果 log\_filename 以 .log 結尾，則替換後綴。）

該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

#### `log_file_mode` \(`integer`\)

在 Unix 系統上，此參數在啟用 logging\_collector 時設定日誌檔案的權限。（在 Microsoft Windows 上，此參數將被忽略。）參數值預期為以 chmod 和 umask 系統呼叫接受的格式來指定的數字模式。（要使用習慣的八進制格式，數字必須以 0（零）開頭。）

預設權限為 0600，這意味著只有伺服器擁有者才能讀取或寫入日誌檔案。另一個常用的設定是 0640，允許擁有者組群的成員讀取文件。 但是請注意，要使用這種設定，您需要變更 log\_directory 以將檔案儲存在叢集 data 目錄之外的某個位置。無論如何，使日誌檔案讓任何人都可讀是不明智的，因為它們可能包含敏感資料。

該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

#### `log_rotation_age` \(`integer`\)

當啟用 logging\_collector 時，此參數決定單個日誌檔案的最長生命週期。經過指定的分鐘後，會建立一個新的日誌檔案。設定為零以停用基於時間的新日誌檔案建立。該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

#### `log_rotation_size` \(`integer`\)

當啟用 logging\_collector 時，此參數決定單個日誌檔的大小上限。在超過上限的記錄被發送到日誌檔案後，將建立一個新的日誌檔案。設定為零以禁用基於大小的新日誌檔案創立。該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

#### `log_truncate_on_rotation` \(`boolean`\)

當啟用 logging\_collector 時，此參數將導致 PostgreSQL 分割（覆蓋）而不是追加到任何具有相同名稱的現有日誌檔案。 但是，分割只會在由於基於時間的覆寫而打開新檔案時發生，而不是在伺服器啟動或基於大小的覆寫情況進行。關閉時，預先存在的檔案將被附加到所有情況下。例如，將此設定與 log\_filename（如 postgresql-％H.log）結合使用可産生 24 個小時日誌檔案，然後循環覆蓋它們。該參數只能在 postgresql.conf 檔案或伺服器指令中設定。

例如：要保留 7 天的日誌，每天一個名稱為 server\_log.Mon，server\_log.Tue 等的日誌檔案，並自動使用本週的日誌覆蓋上週的日誌，將 log\_filename 設定為server\_log.％a，將 log\_truncate\_on\_rotation 設定為 on，並將 log\_rotation\_age 到 1440。

又例如：要保留 24 小時的日誌，每小時記錄一個日誌檔案，但是如果日誌檔案大小超過 1GB，則會盡快輪換，將 log\_filename 設定為 server\_log.％H％M，log\_truncate\_on\_rotation 為 on，log\_rotation\_age 為 60，log\_rotation\_size 為1000000。在 log\_filename 中包含 ％M 允許可能出現的任何大小驅動的旋轉，以選擇與小時的初始檔案名稱不同的檔案名稱。

#### `syslog_facility` \(`enum`\)

當啟用日誌記錄到 syslog 時，此參數確定要使用的系統日誌的「設施」。 您可以選擇 LOCAL0，LOCAL1，LOCAL2，LOCAL3，LOCAL4，LOCAL5，LOCAL6，LOCAL7；預設值是 LOCAL0。另請參閱系統的 syslog 背景程序的文件。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

#### `syslog_ident` \(`string`\)

當啟用日誌記錄到系統日誌時，此參數決定用於在系統日誌中識別 PostgreSQL 記錄的程序名稱。預設是 postgres。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

#### `syslog_sequence_numbers` \(`boolean`\)

當記錄到系統日誌並且這是啓用的（預設），那麼每筆記錄將以遞增的序列號碼（例如\[2\]）作為前置內容。這規避了「---最後一條記錄重複 N 次---」抑制了許多 syslog 實務上預設執行的操作。在更現代的 syslog 實作中，可以設定重複的記錄抑制（例如，rsyslog 中的 $RepeatedMsgReduction），所以這可能不是必要的。另外，如果你真的想要抑制重複的記錄，就可以關掉它。

此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

#### `syslog_split_messages` \(`boolean`\)

當啟用日誌記錄到 syslog 時，此參數決定記錄如何傳遞到系統日誌。啟用時（預設），記錄按行分割，使得行長在 1024 字元以下，這是傳統 syslog 實作的典型大小限制。關閉時，PostgreSQL 伺服器日誌記錄會按原樣傳遞到系統日誌服務，並由系統日誌服務來處理潛在的龐大記錄。

如果 syslog 最終記錄到文字檔案，那麼效果將是相同的，並且最好將設定保留為開啟狀態，因為大多數 syslog 實作無法處理大量記錄，或者需要專門設定以處理它們。但是，如果系統日誌最終寫入其他媒體，將記錄邏輯上地組合在一起可能是必要的或更有用的。

此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

#### `event_source` \(`string`\)

當啟用記錄到事件日誌時，此參數確定用於在記錄中識別 PostgreSQL 記錄的程序名稱。預設是 PostgreSQL。 此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

## 19.8.2. When To Log

#### `client_min_messages` \(`enum`\)

Controls which message levels are sent to the client. Valid values are `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `LOG`, `NOTICE`, `WARNING`, `ERROR`, `FATAL`, and `PANIC`. Each level includes all the levels that follow it. The later the level, the fewer messages are sent. The default is `NOTICE`. Note that `LOG` has a different rank here than in `log_min_messages`.

#### `log_min_messages` \(`enum`\)

Controls which message levels are written to the server log. Valid values are `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `INFO`, `NOTICE`, `WARNING`, `ERROR`, `LOG`, `FATAL`, and `PANIC`. Each level includes all the levels that follow it. The later the level, the fewer messages are sent to the log. The default is `WARNING`. Note that `LOG` has a different rank here than in `client_min_messages`. Only superusers can change this setting.

#### `log_min_error_statement` \(`enum`\)

Controls which SQL statements that cause an error condition are recorded in the server log. The current SQL statement is included in the log entry for any message of the specified severity or higher. Valid values are `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `INFO`, `NOTICE`, `WARNING`, `ERROR`, `LOG`, `FATAL`, and `PANIC`. The default is `ERROR`, which means statements causing errors, log messages, fatal errors, or panics will be logged. To effectively turn off logging of failing statements, set this parameter to `PANIC`. Only superusers can change this setting.

#### `log_min_duration_statement` \(`integer`\)

Causes the duration of each completed statement to be logged if the statement ran for at least the specified number of milliseconds. Setting this to zero prints all statement durations. Minus-one \(the default\) disables logging statement durations. For example, if you set it to `250ms` then all SQL statements that run 250ms or longer will be logged. Enabling this parameter can be helpful in tracking down unoptimized queries in your applications. Only superusers can change this setting.

For clients using extended query protocol, durations of the Parse, Bind, and Execute steps are logged independently.

#### Note

When using this option together with [log\_statement](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#GUC-LOG-STATEMENT), the text of statements that are logged because of `log_statement` will not be repeated in the duration log message. If you are not using syslog, it is recommended that you log the PID or session ID using [log\_line\_prefix](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#GUC-LOG-LINE-PREFIX) so that you can link the statement message to the later duration message using the process ID or session ID.

[Table 19.1](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#RUNTIME-CONFIG-SEVERITY-LEVELS) explains the message severity levels used by PostgreSQL. If logging output is sent to syslog or Windows' eventlog, the severity levels are translated as shown in the table.

**Table 19.1. Message Severity Levels**

| Severity | Usage | syslog | eventlog |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DEBUG1..DEBUG5` | Provides successively-more-detailed information for use by developers. | `DEBUG` | `INFORMATION` |
| `INFO` | Provides information implicitly requested by the user, e.g., output from `VACUUM VERBOSE`. | `INFO` | `INFORMATION` |
| `NOTICE` | Provides information that might be helpful to users, e.g., notice of truncation of long identifiers. | `NOTICE` | `INFORMATION` |
| `WARNING` | Provides warnings of likely problems, e.g., `COMMIT` outside a transaction block. | `NOTICE` | `WARNING` |
| `ERROR` | Reports an error that caused the current command to abort. | `WARNING` | `ERROR` |
| `LOG` | Reports information of interest to administrators, e.g., checkpoint activity. | `INFO` | `INFORMATION` |
| `FATAL` | Reports an error that caused the current session to abort. | `ERR` | `ERROR` |
| `PANIC` | Reports an error that caused all database sessions to abort. | `CRIT` | `ERROR` |

## 19.8.3. What To Log

#### `application_name` \(`string`\)

The `application_name` can be any string of less than `NAMEDATALEN` characters \(64 characters in a standard build\). It is typically set by an application upon connection to the server. The name will be displayed in the `pg_stat_activity` view and included in CSV log entries. It can also be included in regular log entries via the [log\_line\_prefix](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#GUC-LOG-LINE-PREFIX) parameter. Only printable ASCII characters may be used in the `application_name` value. Other characters will be replaced with question marks \(`?`\).

#### `debug_print_parse` \(`boolean`\)  `debug_print_rewritten` \(`boolean`\)  `debug_print_plan` \(`boolean`\)

These parameters enable various debugging output to be emitted. When set, they print the resulting parse tree, the query rewriter output, or the execution plan for each executed query. These messages are emitted at `LOG` message level, so by default they will appear in the server log but will not be sent to the client. You can change that by adjusting [client\_min\_messages](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#GUC-CLIENT-MIN-MESSAGES) and/or [log\_min\_messages](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#GUC-LOG-MIN-MESSAGES). These parameters are off by default.

#### `debug_pretty_print` \(`boolean`\)

When set, `debug_pretty_print` indents the messages produced by `debug_print_parse`, `debug_print_rewritten`, or `debug_print_plan`. This results in more readable but much longer output than the “compact” format used when it is off. It is on by default.

#### `log_checkpoints` \(`boolean`\)

Causes checkpoints and restartpoints to be logged in the server log. Some statistics are included in the log messages, including the number of buffers written and the time spent writing them. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is off.

#### `log_connections` \(`boolean`\)

Causes each attempted connection to the server to be logged, as well as successful completion of client authentication. Only superusers can change this parameter at session start, and it cannot be changed at all within a session. The default is `off`.

#### Note

Some client programs, like psql, attempt to connect twice while determining if a password is required, so duplicate “connection received” messages do not necessarily indicate a problem.

#### `log_disconnections` \(`boolean`\)

Causes session terminations to be logged. The log output provides information similar to `log_connections`, plus the duration of the session. Only superusers can change this parameter at session start, and it cannot be changed at all within a session. The default is `off`.

#### `log_duration` \(`boolean`\)

Causes the duration of every completed statement to be logged. The default is `off`. Only superusers can change this setting.

For clients using extended query protocol, durations of the Parse, Bind, and Execute steps are logged independently.

#### Note

The difference between setting this option and setting [log\_min\_duration\_statement](https://www.postgresql.org/docs/10/static/runtime-config-logging.html#GUC-LOG-MIN-DURATION-STATEMENT) to zero is that exceeding `log_min_duration_statement` forces the text of the query to be logged, but this option doesn't. Thus, if `log_duration` is `on` and `log_min_duration_statement` has a positive value, all durations are logged but the query text is included only for statements exceeding the threshold. This behavior can be useful for gathering statistics in high-load installations.

#### `log_error_verbosity` \(`enum`\)

Controls the amount of detail written in the server log for each message that is logged. Valid values are `TERSE`, `DEFAULT`, and `VERBOSE`, each adding more fields to displayed messages. `TERSE` excludes the logging of `DETAIL`, `HINT`, `QUERY`, and `CONTEXT` error information.`VERBOSE` output includes the `SQLSTATE` error code \(see also [Appendix A](https://www.postgresql.org/docs/10/static/errcodes-appendix.html)\) and the source code file name, function name, and line number that generated the error. Only superusers can change this setting.

#### `log_hostname` \(`boolean`\)

By default, connection log messages only show the IP address of the connecting host. Turning this parameter on causes logging of the host name as well. Note that depending on your host name resolution setup this might impose a non-negligible performance penalty. This parameter can only be set in the `postgresql.conf` file or on the server command line.

#### `log_line_prefix` \(`string`\)

This is a `printf`-style string that is output at the beginning of each log line. `%` characters begin “escape sequences” that are replaced with status information as outlined below. Unrecognized escapes are ignored. Other characters are copied straight to the log line. Some escapes are only recognized by session processes, and will be treated as empty by background processes such as the main server process. Status information may be aligned either left or right by specifying a numeric literal after the % and before the option. A negative value will cause the status information to be padded on the right with spaces to give it a minimum width, whereas a positive value will pad on the left. Padding can be useful to aid human readability in log files. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `'%m [%p] '` which logs a time stamp and the process ID.

| Escape | Effect | Session only |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `%a` | Application name | yes |
| `%u` | User name | yes |
| `%d` | Database name | yes |
| `%r` | Remote host name or IP address, and remote port | yes |
| `%h` | Remote host name or IP address | yes |
| `%p` | Process ID | no |
| `%t` | Time stamp without milliseconds | no |
| `%m` | Time stamp with milliseconds | no |
| `%n` | Time stamp with milliseconds \(as a Unix epoch\) | no |
| `%i` | Command tag: type of session's current command | yes |
| `%e` | SQLSTATE error code | no |
| `%c` | Session ID: see below | no |
| `%l` | Number of the log line for each session or process, starting at 1 | no |
| `%s` | Process start time stamp | no |
| `%v` | Virtual transaction ID \(backendID/localXID\) | no |
| `%x` | Transaction ID \(0 if none is assigned\) | no |
| `%q` | Produces no output, but tells non-session processes to stop at this point in the string; ignored by session processes | no |
| `%%` | Literal `%` | no |

The `%c` escape prints a quasi-unique session identifier, consisting of two 4-byte hexadecimal numbers \(without leading zeros\) separated by a dot. The numbers are the process start time and the process ID, so `%c` can also be used as a space saving way of printing those items. For example, to generate the session identifier from `pg_stat_activity`, use this query:

```text
SELECT to_hex(trunc(EXTRACT(EPOCH FROM backend_start))::integer) || '.' ||
       to_hex(pid)
FROM pg_stat_activity;
```

#### Tip

If you set a nonempty value for `log_line_prefix`, you should usually make its last character be a space, to provide visual separation from the rest of the log line. A punctuation character can be used too.

#### Tip

Syslog produces its own time stamp and process ID information, so you probably do not want to include those escapes if you are logging to syslog.

#### Tip

The `%q` escape is useful when including information that is only available in session \(backend\) context like user or database name. For example:

```text
log_line_prefix = '%m [%p] %q%u@%d/%a '
```

#### `log_lock_waits` \(`boolean`\)

控制連線等待時間超過 [deadlock\_timeout](19.12.-jiao-yi-suo-ding-guan-li.md) 時是否產生日誌訊息。這對於確定鎖定等待是否導致性能較差很有用。預設是關閉的。只有超級使用者可以變更此設定。

#### `log_statement` \(`enum`\)

Controls which SQL statements are logged. Valid values are `none` \(off\), `ddl`, `mod`, and `all` \(all statements\). `ddl` logs all data definition statements, such as `CREATE`, `ALTER`, and `DROP` statements. `mod` logs all `ddl` statements, plus data-modifying statements such as `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, and `COPY FROM`. `PREPARE`, `EXECUTE`, and `EXPLAIN ANALYZE` statements are also logged if their contained command is of an appropriate type. For clients using extended query protocol, logging occurs when an Execute message is received, and values of the Bind parameters are included \(with any embedded single-quote marks doubled\).

The default is `none`. Only superusers can change this setting.

#### Note

Statements that contain simple syntax errors are not logged even by the `log_statement` = `all` setting, because the log message is emitted only after basic parsing has been done to determine the statement type. In the case of extended query protocol, this setting likewise does not log statements that fail before the Execute phase \(i.e., during parse analysis or planning\). Set `log_min_error_statement` to `ERROR` \(or lower\) to log such statements.

#### `log_replication_commands` \(`boolean`\)

Causes each replication command to be logged in the server log. See [Section 52.4](https://www.postgresql.org/docs/10/static/protocol-replication.html) for more information about replication command. The default value is `off`. Only superusers can change this setting.

#### `log_temp_files` \(`integer`\)

Controls logging of temporary file names and sizes. Temporary files can be created for sorts, hashes, and temporary query results. A log entry is made for each temporary file when it is deleted. A value of zero logs all temporary file information, while positive values log only files whose size is greater than or equal to the specified number of kilobytes. The default setting is -1, which disables such logging. Only superusers can change this setting.

#### `log_timezone` \(`string`\)

Sets the time zone used for timestamps written in the server log. Unlike [TimeZone](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-TIMEZONE), this value is cluster-wide, so that all sessions will report timestamps consistently. The built-in default is `GMT`, but that is typically overridden in `postgresql.conf`; initdb will install a setting there corresponding to its system environment. See [Section 8.5.3](https://www.postgresql.org/docs/10/static/datatype-datetime.html#DATATYPE-TIMEZONES) for more information. This parameter can only be set in the `postgresql.conf` file or on the server command line.

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

## 19.8.5. Process Title

這些設定控制如何修改伺服器程序的程序標題。程序標題通常使用如 ps 或 Windows 上的 Process Explorer 查看。詳情請參閱[第 28.1 節](../28.-jian-kong-zi-liao-ku-huo-dong/28.1.-standard-unix-tools.md)。

#### `cluster_name` \(`string`\)

設定此叢集中所有伺服器程序的程序標題中顯示的叢集名稱。該名稱可以是任何少於 NAMEDATALEN 字元數的字串（標準版本中為 64 個字元）。cluster\_name 值中只能使用可列印的 ASCII 字元。其他字元將被替換為問號（？）。如果此參數設定為空字串“”（這是預設值），則不顯示名稱。此參數只能在伺服器啟動時設定。

#### `update_process_title` \(`boolean`\)

每當伺服器收到新的 SQL 指令時，都可以更新程序標題。此設定在大多數平台上預設為開啟，不過在 Windows 上預設為關閉，因為在 Windows 上更新程序標題的開銷較大。只有超級使用者可以變更此設定。

