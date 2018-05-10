# 19.10. 自動資料庫清理

這些設定控制自動資料清理（autovacuum）功能的行為。有關更多訊息，請參閱[第 24.1.6 節](../maintenance/routine-vacuuming.md#24-1-6-the-autovacuum-daemon)。請注意，許多這些設定可以基於每個資料表進行調整；請參閱[儲存參數](../../reference/sql-commands/create-table.md#storage-parameters)的說明。

`autovacuum` \(`boolean`\)

控制伺服器是否應該執行 autovacuum 啟動程序背景程序。這是預設開啟的；但是，[track\_counts](run-time-statistics.md#19-9-2-statistics-monitoring) 也必須啟用 autovacuum 工作。此參數只能在 postgresql.conf 檔案或伺服器命令行中設定；但是，可以透過變更資料表儲存參數來禁用單個資料表的自動清除。

請注意，即使禁用此參數，系統也會在必要時啟動自動清理過程以防止交易事務 ID 重覆。有關更多訊息，請參閱[第 24.1.5 節](../maintenance/routine-vacuuming.md#24-1-5-preventing-transaction-id-wraparound-failures)。

`log_autovacuum_min_duration` \(`integer`\)

如果 autovacuum 執行的每個操作至少運行了指定的毫秒數，則會被記錄下來。 將其設定為零會記錄所有自動清理操作。-1（預設值）禁用記錄自動清理操作。例如，如果將此設定為 250ms，則會記錄所有執行 250ms 或更長時間的自動清理和分析。另外，當此參數設定為除 -1 之外的任何值時，如果由於存在衝突鎖定而導致 autovacuum 操作被跳過，則會記錄一條記錄。啟用此參數可以有助於跟踪自動清理活動。此參數只能在 postgresql.conf 檔案或伺服器命令行中設定；但是可以透過變更資料表的儲存參數來覆寫單個資料表的設定。

`autovacuum_max_workers` \(`integer`\)

指定可能在任何時間運行的自動清理程序的最大數目（除了自動清理啟動程序）。預設值是 3。該參數只能在伺服器啟動時設定。

`autovacuum_naptime` \(`integer`\)

指定在任何資料庫上執行 autovacuum 之間的最小延遲。 在每一輪背景程序檢查資料庫並根據需要為該資料庫中的資料表發出 VACUUM 和 ANALYZE 命令。延遲以秒為單位進行測量，預設值為 1 分鐘（1分鐘）。該參數只能在 postgresql.conf 檔案或伺服器命令行中設定。

`autovacuum_vacuum_threshold` \(`integer`\)

指定在任何一個資料表中觸發 VACUUM 所需的更新或刪除 tuple 的最小數目。預設值是 50 個 tuple。此參數只能在 postgresql.conf 檔案或伺服器命令行中設定；但是可以透過變更資料儲存參數來覆寫單個資料表的設定。

`autovacuum_analyze_threshold` \(`integer`\)

指定在任何一個資料表中觸發 ANALYZE 所需的插入、更新或刪除的 tuple 的最小數目。預設值是 50 個 tuple。此參數只能在 postgresql.conf 檔案或伺服器命令行中設定；但是可以透過變更資料表儲存參數來覆寫單個資料表的設定。

`autovacuum_vacuum_scale_factor` \(`floating point`\)

決定觸發 VACUUM 時，指定要加到 autovacuum\_vacuum\_threshold 的資料表大小的比例。預設值是0.2（資料表大小的 20％）。此參數只能在 postgresql.conf 檔案或伺服器命令行中設定；但是可以透過變更資料表儲存參數來覆寫單個資料表的設定。

`autovacuum_analyze_scale_factor` \(`floating point`\)

指定在決定是否觸發 ANALYZE 時加到 autovacuum\_analyze\_threshold 的資料表大小的比例。預設值是 0.1（資料表大小的 10％）。此參數只能在 postgresql.conf 檔案或伺服器命令行中設定；但是可以透過變更資料表儲存參數來覆寫單個資料表的設定。

`autovacuum_freeze_max_age` \(`integer`\)

指定資料表的 pg\_class.relfrozenxid 參數在 VACUUM 操作時被強制阻止資料表中的交易事務 ID 重覆之前可以達到的最大期限（在交易事務中）。請注意，系統將啟動 autovacuum 程序以防止重覆，即使禁用 autovacuum 時也會進行。

Vacuum 還允許從 pg\_xact 子目錄中刪除舊檔案，這就是為什麼預設值是相對較低的 2 億次事務。該參數只能在伺服器啟動時設定，但透過變更資料表儲存參數可以減少單個資表的設定。有關更多訊息，請參閱[第 24.1.5 節](../maintenance/routine-vacuuming.md#24-1-5-preventing-transaction-id-wraparound-failures)。

`autovacuum_multixact_freeze_max_age` \(`integer`\)

Specifies the maximum age \(in multixacts\) that a table's `pg_class`.`relminmxid` field can attain before a `VACUUM` operation is forced to prevent multixact ID wraparound within the table. Note that the system will launch autovacuum processes to prevent wraparound even when autovacuum is otherwise disabled.

Vacuuming multixacts also allows removal of old files from the `pg_multixact/members` and `pg_multixact/offsets` subdirectories, which is why the default is a relatively low 400 million multixacts. This parameter can only be set at server start, but the setting can be reduced for individual tables by changing table storage parameters. For more information see [Section 24.1.5.1](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-MULTIXACT-WRAPAROUND).

`autovacuum_vacuum_cost_delay` \(`integer`\)

Specifies the cost delay value that will be used in automatic `VACUUM` operations. If -1 is specified, the regular [vacuum\_cost\_delay](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-VACUUM-COST-DELAY) value will be used. The default value is 20 milliseconds. This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

`autovacuum_vacuum_cost_limit` \(`integer`\)

Specifies the cost limit value that will be used in automatic `VACUUM` operations. If -1 is specified \(which is the default\), the regular [vacuum\_cost\_limit](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-VACUUM-COST-LIMIT) value will be used. Note that the value is distributed proportionally among the running autovacuum workers, if there is more than one, so that the sum of the limits for each worker does not exceed the value of this variable. This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

