# 20.6. 複寫（Replication）

這些設定控制內建的串流複寫功能行為（請參閱[第 26.2.5 節](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-5-streaming-replication)）。伺服器指的是主伺服務器或備用伺服器。主伺服器可以發送資料，而備用伺服器始終是複寫資料的接收者。當使用串聯複寫（請參閱[第 26.2.7 節](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-7-cascading-replication)）時，備用伺服器也可以是發送者和接收者。參數主要用於發送和備用伺服器，但某些參數僅在主伺服器上有意義。如果需要，設定是跨群集的，不會産生問題。

## 19.6.1. 發送伺服器（Sender Server）

可以在將資料複寫發送到一個或多個備用伺服器的任何伺服器上設定這些參數。主伺服器始終是發送伺服器，因此必須在主伺服器上設定這些參數。備用資料庫成為主資料庫後，這些參數的作用也不會改變。

#### `max_wal_senders` (`integer`)

指定來自備用伺服器或串流複寫備份用戶端的最大同時連線數（即同時運行的 WAL 發送程序的最大數量）。預設值為 10，0 表示停用複寫。WAL 發送方程序也計入連線總數，因此參數不能設定高於 [max\_connections](connections-and-authentication.md#19-3-1-ding)。突然串流用戶端中斷連線可能會導致遺留連線插槽，直到達到超時。因此此參數應設定為略高於預期用戶端的最大數量，以便中斷連線的用戶端可以立即重新連線。此參數只能在伺服器啟動時設定。wal\_level 必須設定為 replica 或更高設定才能允許來自備用伺服器的連線。

#### `max_replication_slots` (`integer`)

指定伺服器可以支援的最大複寫槽數（請參閱[第 26.2.6 節](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-6-replication-slots)）。預設值為 10。此參數只能在伺服器啟動時設定。必須將 wal\_level 設定為 replica 或更高設定才能使用複寫槽。將其設定為低於目前現有複寫插槽數的值將阻止伺服器啟動。

#### `wal_keep_segments` (`integer`)

指定保留在 pg\_wal 目錄中的過時日誌段落檔案的最小數量，以防備用伺服器需要取得它們以進行串流複寫。每個段落段通常為 16 MB。如果連線到發送伺服器的備用伺服器落後於 wal\_keep\_segments 個段落以上，則發送伺服器可能會刪除備用資料庫仍需要的 WAL 段落，在這種情況下，複寫連線將會終止。因此，下游連線最終也會失敗。（但是，如果正在使用 WAL Archive，則備用伺服器可以透過從 Archive 中取得段落來進行回復。）

這僅設定 pg\_wal 中保留的最小段落數量；系統可能需要為 WAL 存檔保留更多段落或從檢查點回復。如果 wal\_keep\_segments 為零（預設值），則系統不會為備用目的保留任何額外的段落，因此備用伺服器可用的舊 WAL 段落數是上一個檢查點的位置和WAL 歸檔狀態的函數。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

#### `max_slot_wal_keep_size` (`integer`)

指定在檢查點時間允許[複寫槽(replication slots)](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-6-replication-slots)保留在 pg\_wal 目錄中的 WAL 檔案最大大小。如果 max\_slot\_wal\_keep\_size 為 -1（預設值），則複寫槽可能會保留無限數量的 WAL 檔案。否則，如果複寫槽的 restart\_lsn 落後於目前 LSN 超過設定大小，就會刪除所需的 WAL 檔案，使用該複寫槽的備用資料庫可能就不再能夠繼續複寫。您可以在 [pg\_replication\_slots](../../internals/system-views/pg\_replication\_slots.md) 中看到複寫槽的 WAL 可用性。

#### `wal_sender_timeout` (`integer`)

終止靜止狀態超過指定毫秒數的複寫連線。這對於發送伺服器檢測備用伺服器當機或網路斷線很有用。值為零會停用超時機制。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設值為 60 秒。

#### `track_commit_timestamp` (`boolean`)

記錄事務的提交時間。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。預設值為 off。

## 19.6.2. 主要伺服器（Master Server）

可以將要複寫資料發送到一個或多個備用伺服器，在主要伺服器上設定這些參數。請注意，除了這些參數之外，還必須在主要伺服器上正確設定 [wal\_level](write-ahead-log.md#19-5-1-settings)，可以選擇啟用 WAL 歸檔（參閱[第 19.5.3 節](write-ahead-log.md#19-5-3-archiving)）。備用伺服器上這些參數的值是無意義的，儘管您可能希望將它們設定在那裡以預備備用資料庫成為主要伺服器的可能性。

#### `synchronous_standby_names` (`string`)

指定可支援同步複寫的備用伺服器列表，如[第 26.2.8 節](../high-availability-load-balancing-and-replication/log-shipping-standby-servers.md#26-2-8-synchronous-replication)中所述。 將有一個或多個線上同步的備用資料庫；在這些備用伺服器確認收到其資料後，將允許等待提交的事務繼續進行。同步備用資料庫將是其名稱出現在此列表中的那些，並且即時以串流傳輸資料（如 [pg\_stat\_replication](../monitoring-database-activity/the-statistics-collector.md) 檢視表中的串流傳輸狀態所示）。指定多個同步備用資料庫可以達到非常高的可用性並防止資料遺失。

用於此目的的備用伺服器的名稱是以備用資料庫的 application\_name 設定，在備用資料庫的連線資訊中設定。如果是物理性複寫的備用，則應在 recovery.conf 中的 primary\_conninfo 設定中進行設定；預設的是 [cluster\_name](error-reporting-and-logging.md#cluster\_name-string) 的內容，不然就會是 walreceiver。對於邏輯性複寫，可以在訂閱的連線訊息中設定，並且預設為訂閱名稱。對於其他複寫的串流使用者，請查閱其文件。

此參數使用以下任一語法指定備用伺服器列表：

```
[FIRST] num_sync ( standby_name [, ...] )
ANY num_sync ( standby_name [, ...] )
standby_name [, ...]
```

其中 num\_sync 是交易事務需要等待回覆的同步備用數量，而 standby\_name 是備用伺服器的名稱。FIRST 和 ANY 指定從列出的伺服器中選擇同步備用資料庫的方法。

關鍵字 FIRST 與 num\_sync 合併使用，指定基於優先的同步複寫，讓事務提交等待，直到將其 WAL 記錄複寫到優先選擇的 num\_sync 同步備用資料庫。例如，FIRST 3（s1，s2，s3，s4）的設定將使得每個提交等待從備用伺服器 s1，s2，s3 和 s4 中選擇的三個較優先的備用資料庫回覆。名稱在列表中較早出現的備用資料庫具有較高的優先等級，並被視為是同步的。此列表中稍後出現的其他備用伺服器代表潛在的同步備用資料庫。如果任何當下的同步備用資料庫因任何原因斷開連線，它將立即被替換為次高優先等級的備用資料庫。關鍵字 FIRST 是選用的。

關鍵字 ANY 與 num\_sync 一起使用，指定需要仲裁的同步複寫，使事務提交等待，直到將其 WAL 記錄複寫到至少 num\_sync 列出的備用資料庫。例如，ANY 3（s1，s2，s3，s4）的設定將使得每個提交在 s1，s2，s3 和 s4 的至少任何三個備用資料回覆時繼續進行。

FIRST 和 ANY 都不區分大小寫。 如果將這些關鍵字用作備用伺服器的名稱，則其 standby\_name 必須使用雙引號。

第三種語法在 PostgreSQL 版本 9.6 之前使用，仍然受支援。它與 FIRST 和 num\_sync 等於 1 的第一個語法相同。例如，FIRST 1（s1，s2）和 s1，s2 具有相同的含義：s1 或 s2 被選為同步的備用伺服器。

特殊符號 \* 表示匹配任何備用名稱。

沒有其他機制來強制備用名稱的唯一性。如果重複的話，其中一個備用資料庫將被視為更優先的，但無法確切說是哪一個。

**注意**\
每個 standby\_name 都應具有有效 SQL 識別字的形式，除非是 \*。如有必要，您可以使用雙引號。但請注意，standby\_names 與備用 application name 都不區分大小寫，無論是否為雙引號。

如果此處未指定同步的備用伺服器名稱，則不啟用同步複寫，事務提交就不會等待複寫。這是預設配置。即使啟用了同步複寫，也可以將單個事務設定為不等待複寫，方法是將 [synchronous\_commit](write-ahead-log.md#19-5-1-settings) 參數設定為 local 或 off。

此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

#### `vacuum_defer_cleanup_age` (`integer`)

指定 VACUUM 和 HOT 更新將延遲清除過期資料列版本的事務數。預設值為 0 事務，這意味著可以盡快刪除過期資料列的版本。也就是說，只要它們不再對任何開放的事務是可見的。您可能希望在支持熱備用伺服器的主要服務器上將其設定為非零值，如[第 26.5 節](../high-availability-load-balancing-and-replication/hot-standby.md)中所述。這樣可以讓備用資料庫上的查詢有更多時間完成，而不會因過早清理資料列而導致衝突。但是，由於該值是根據主要服務器上所發生的寫入事務的數量來衡量的，因此很難預測備用查詢可用多少額外的寬限時間。 此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

您還應該考慮在備用伺服器上設定 hot\_standby\_feedback 作為使用此參數的替代方法。

這不會阻止已達到 old\_snapshot\_threshold 指定期間的過時資料列清除。

## 19.6.3. Standby Servers

這些設定控制要接收複寫資料的備用伺服器行為，與主伺服器上的設定是無關的。

#### `primary_conninfo` (`string`)

Specifies a connection string to be used for the standby server to connect with a sending server. This string is in the format described in [Section 33.1.1](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-CONNSTRING). If any option is unspecified in this string, then the corresponding environment variable (see [Section 33.14](https://www.postgresql.org/docs/13/libpq-envars.html)) is checked. If the environment variable is not set either, then defaults are used.

The connection string should specify the host name (or address) of the sending server, as well as the port number if it is not the same as the standby server's default. Also specify a user name corresponding to a suitably-privileged role on the sending server (see [Section 26.2.5.1](https://www.postgresql.org/docs/13/warm-standby.html#STREAMING-REPLICATION-AUTHENTICATION)). A password needs to be provided too, if the sender demands password authentication. It can be provided in the `primary_conninfo` string, or in a separate `~/.pgpass` file on the standby server (use `replication` as the database name). Do not specify a database name in the `primary_conninfo` string.

This parameter can only be set in the `postgresql.conf` file or on the server command line. If this parameter is changed while the WAL receiver process is running, that process is signaled to shut down and expected to restart with the new setting (except if `primary_conninfo` is an empty string). This setting has no effect if the server is not in standby mode.

#### `primary_slot_name` (`string`)

Optionally specifies an existing replication slot to be used when connecting to the sending server via streaming replication to control resource removal on the upstream node (see [Section 26.2.6](https://www.postgresql.org/docs/13/warm-standby.html#STREAMING-REPLICATION-SLOTS)). This parameter can only be set in the `postgresql.conf` file or on the server command line. If this parameter is changed while the WAL receiver process is running, that process is signaled to shut down and expected to restart with the new setting. This setting has no effect if `primary_conninfo` is not set or the server is not in standby mode.

`promote_trigger_file` (`string`)

Specifies a trigger file whose presence ends recovery in the standby. Even if this value is not set, you can still promote the standby using `pg_ctl promote` or calling `pg_promote()`. This parameter can only be set in the `postgresql.conf` file or on the server command line.

#### `hot_standby` (`boolean`)

指定是否可以在回復期間連線和執行查詢，如[第 26.5 節](../high-availability-load-balancing-and-replication/hot-standby.md)中所述。預設值為 on。 此參數只能在伺服器啟動時設定。它僅在歸檔回復或備機模式下有效。

#### `max_standby_archive_delay` (`integer`)

當 Hot Standby 處於啟用狀態時，此參數確定備用伺服器在取消與即將套用的 WAL 項目衝突的備用查詢之前應等待的時間，如[第 26.5.2 節](../high-availability-load-balancing-and-replication/hot-standby.md#26-5-2-handling-query-conflicts)中所述。當從 WAL 歸檔中讀取 WAL 資料時，max\_standby\_archive\_delay 適用（因此不是當下的）。預設值為 30 秒。如果未指定，則單位為毫秒。值 -1 時允許備用資料庫永遠等待衝突查詢完成。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

請注意，max\_standby\_archive\_delay 與取消前查詢可以執行的最長時間不同；相反地，它是允許套用任何一個 WAL 資料段的最大總時間。因此，如果一個查詢在 WAL 資料段中導致顯著延遲，則後續衝突查詢將具有更少的寬限時間。

#### `max_standby_streaming_delay` (`integer`)

當 Hot Standby 處於啓用狀態時，此參數決定備用伺服器在取消與即將套用的 WAL 項目衝突的備用查詢之前應等待的時間，如[第 26.5.2 節](../high-availability-load-balancing-and-replication/hot-standby.md#26-5-2-handling-query-conflicts)中所述。當透過串流複寫接收 WAL 資料時，套用max\_standby\_streaming\_delay。預設值為 30 秒。如果未指定，則單位為毫秒。值 -1 時允許備用資料庫永遠等待衝突查詢完成。此參數只能在 postgresql.conf 檔案或伺服器命令列中設定。

請注意，max\_standby\_streaming\_delay 與取消前查詢可以執行的最長時間不同；相反地，它是從主伺服器收到 WAL 資料後允許套用的最大總時間。因此，如果一個查詢導致顯著延遲，則後續衝突查詢將具有更少的寬限時間，直到備用伺服器再次趕上。

#### `wal_receiver_create_temp_slot` (`boolean`)

Specifies whether the WAL receiver process should create a temporary replication slot on the remote instance when no permanent replication slot to use has been configured (using [primary\_slot\_name](https://www.postgresql.org/docs/13/runtime-config-replication.html#GUC-PRIMARY-SLOT-NAME)). The default is off. This parameter can only be set in the `postgresql.conf` file or on the server command line. If this parameter is changed while the WAL receiver process is running, that process is signaled to shut down and expected to restart with the new setting.

#### `wal_receiver_status_interval` (`integer`)

Specifies the minimum frequency for the WAL receiver process on the standby to send information about replication progress to the primary or upstream standby, where it can be seen using the [`pg_stat_replication`](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-VIEWS-TABLE) view. The standby will report the last write-ahead log location it has written, the last position it has flushed to disk, and the last position it has applied. This parameter's value is the maximum interval, in seconds, between reports. Updates are sent each time the write or flush positions change, or at least as often as specified by this parameter. Thus, the apply position may lag slightly behind the true position. Setting this parameter to zero disables status updates completely. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default value is 10 seconds.

#### `hot_standby_feedback` (`boolean`)

Specifies whether or not a hot standby will send feedback to the primary or upstream standby about queries currently executing on the standby. This parameter can be used to eliminate query cancels caused by cleanup records, but can cause database bloat on the primary for some workloads. Feedback messages will not be sent more frequently than once per `wal_receiver_status_interval`. The default value is `off`. This parameter can only be set in the `postgresql.conf` file or on the server command line.

If cascaded replication is in use the feedback is passed upstream until it eventually reaches the primary. Standbys make no other use of feedback they receive other than to pass upstream.

This setting does not override the behavior of `old_snapshot_threshold` on the primary; a snapshot on the standby which exceeds the primary's age threshold can become invalid, resulting in cancellation of transactions on the standby. This is because `old_snapshot_threshold` is intended to provide an absolute limit on the time which dead rows can contribute to bloat, which would otherwise be violated because of the configuration of a standby.

#### `wal_receiver_timeout` (`integer`)

Terminate replication connections that are inactive longer than the specified number of milliseconds. This is useful for the receiving standby server to detect a primary node crash or network outage. A value of zero disables the timeout mechanism. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default value is 60 seconds.

#### `wal_retrieve_retry_interval` (`integer`)

Specify how long the standby server should wait when WAL data is not available from any sources (streaming replication, local `pg_wal` or WAL archive) before retrying to retrieve WAL data. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default value is 5 seconds. Units are milliseconds if not specified.

This parameter is useful in configurations where a node in recovery needs to control the amount of time to wait for new WAL data to be available. For example, in archive recovery, it is possible to make the recovery more responsive in the detection of a new WAL log file by reducing the value of this parameter. On a system with low WAL activity, increasing it reduces the amount of requests necessary to access WAL archives, something useful for example in cloud environments where the amount of times an infrastructure is accessed is taken into account.

#### `recovery_min_apply_delay` (`integer`)

By default, a standby server restores WAL records from the sending server as soon as possible. It may be useful to have a time-delayed copy of the data, offering opportunities to correct data loss errors. This parameter allows you to delay recovery by a specified amount of time. For example, if you set this parameter to `5min`, the standby will replay each transaction commit only when the system time on the standby is at least five minutes past the commit time reported by the master. If this value is specified without units, it is taken as milliseconds. The default is zero, adding no delay.

It is possible that the replication delay between servers exceeds the value of this parameter, in which case no delay is added. Note that the delay is calculated between the WAL time stamp as written on master and the current time on the standby. Delays in transfer because of network lag or cascading replication configurations may reduce the actual wait time significantly. If the system clocks on master and standby are not synchronized, this may lead to recovery applying records earlier than expected; but that is not a major issue because useful settings of this parameter are much larger than typical time deviations between servers.

The delay occurs only on WAL records for transaction commits. Other records are replayed as quickly as possible, which is not a problem because MVCC visibility rules ensure their effects are not visible until the corresponding commit record is applied.

The delay occurs once the database in recovery has reached a consistent state, until the standby is promoted or triggered. After that the standby will end recovery without further waiting.

This parameter is intended for use with streaming replication deployments; however, if the parameter is specified it will be honored in all cases except crash recovery. `hot_standby_feedback` will be delayed by use of this feature which could lead to bloat on the master; use both together with care.

#### Warning

Synchronous replication is affected by this setting when `synchronous_commit` is set to `remote_apply`; every `COMMIT` will need to wait to be applied.

This parameter can only be set in the `postgresql.conf` file or on the server command line.

## 19.6.4. Subscribers

這些設定控制著邏輯複寫訂閱伺服器的行為。它們與發佈者的設定無關。

請注意，wal\_receiver\_timeout，wal\_receiver\_status\_interval 和 wal\_retrieve\_retry\_interval 組態參數也會影響邏輯複寫的工作程序。

#### `max_logical_replication_workers` (`int`)

指定邏輯複寫工作程序的最大數量。這包括應用工作程序和資料表同步的工作程序。

邏輯複寫工作程序來自 max\_worker\_processes 定義的資源池。

預設值為 4。

#### `max_sync_workers_per_subscription` (`integer`)

每個訂閱的最大同步工作程序數目。此參數控制訂閱初始化期間或增加新資料表時初始資料副本的平行處理數量。

目前，每個資料表只會有一個同步工作程序。

同步工作程序來自 max\_logical\_replication\_workers 定義的資源池。

預設值為 2。
