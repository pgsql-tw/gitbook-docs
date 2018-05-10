# 19.10. 自動資料庫清理

這些設定控制自動資料清理（autovacuum）功能的行為。有關更多訊息，請參閱[第 24.1.6 節](../maintenance/routine-vacuuming.md#24-1-6-the-autovacuum-daemon)。請注意，許多這些設定可以基於每個資料表進行調整；請參閱[儲存參數](../../reference/sql-commands/create-table.md#storage-parameters)的說明。

`autovacuum` \(`boolean`\)

控制伺服器是否應該執行 autovacuum 啟動程序背景程序。這是預設開啟的；但是，[track\_counts](run-time-statistics.md#19-9-2-statistics-monitoring) 也必須啟用 autovacuum 工作。此參數只能在 postgresql.conf 檔案或伺服器命令行中設定；但是，可以透過變更資料表儲存參數來禁用單個資料表的自動清除。

請注意，即使禁用此參數，系統也會在必要時啟動自動清理過程以防止交易事務 ID 重覆。有關更多訊息，請參閱[第 24.1.5 節](../maintenance/routine-vacuuming.md#24-1-5-preventing-transaction-id-wraparound-failures)。

`log_autovacuum_min_duration` \(`integer`\)

Causes each action executed by autovacuum to be logged if it ran for at least the specified number of milliseconds. Setting this to zero logs all autovacuum actions. Minus-one \(the default\) disables logging autovacuum actions. For example, if you set this to `250ms` then all automatic vacuums and analyzes that run 250ms or longer will be logged. In addition, when this parameter is set to any value other than `-1`, a message will be logged if an autovacuum action is skipped due to the existence of a conflicting lock. Enabling this parameter can be helpful in tracking autovacuum activity. This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

`autovacuum_max_workers` \(`integer`\)

Specifies the maximum number of autovacuum processes \(other than the autovacuum launcher\) that may be running at any one time. The default is three. This parameter can only be set at server start.

`autovacuum_naptime` \(`integer`\)

Specifies the minimum delay between autovacuum runs on any given database. In each round the daemon examines the database and issues `VACUUM` and `ANALYZE` commands as needed for tables in that database. The delay is measured in seconds, and the default is one minute \(`1min`\). This parameter can only be set in the `postgresql.conf` file or on the server command line.

`autovacuum_vacuum_threshold` \(`integer`\)

Specifies the minimum number of updated or deleted tuples needed to trigger a `VACUUM` in any one table. The default is 50 tuples. This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

`autovacuum_analyze_threshold` \(`integer`\)

Specifies the minimum number of inserted, updated or deleted tuples needed to trigger an `ANALYZE` in any one table. The default is 50 tuples. This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

`autovacuum_vacuum_scale_factor` \(`floating point`\)

Specifies a fraction of the table size to add to `autovacuum_vacuum_threshold` when deciding whether to trigger a `VACUUM`. The default is 0.2 \(20% of table size\). This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

`autovacuum_analyze_scale_factor` \(`floating point`\)

Specifies a fraction of the table size to add to `autovacuum_analyze_threshold` when deciding whether to trigger an `ANALYZE`. The default is 0.1 \(10% of table size\). This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

`autovacuum_freeze_max_age` \(`integer`\)

Specifies the maximum age \(in transactions\) that a table's `pg_class`.`relfrozenxid` field can attain before a `VACUUM` operation is forced to prevent transaction ID wraparound within the table. Note that the system will launch autovacuum processes to prevent wraparound even when autovacuum is otherwise disabled.

Vacuum also allows removal of old files from the `pg_xact` subdirectory, which is why the default is a relatively low 200 million transactions. This parameter can only be set at server start, but the setting can be reduced for individual tables by changing table storage parameters. For more information see [Section 24.1.5](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND).

`autovacuum_multixact_freeze_max_age` \(`integer`\)

Specifies the maximum age \(in multixacts\) that a table's `pg_class`.`relminmxid` field can attain before a `VACUUM` operation is forced to prevent multixact ID wraparound within the table. Note that the system will launch autovacuum processes to prevent wraparound even when autovacuum is otherwise disabled.

Vacuuming multixacts also allows removal of old files from the `pg_multixact/members` and `pg_multixact/offsets` subdirectories, which is why the default is a relatively low 400 million multixacts. This parameter can only be set at server start, but the setting can be reduced for individual tables by changing table storage parameters. For more information see [Section 24.1.5.1](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-MULTIXACT-WRAPAROUND).

`autovacuum_vacuum_cost_delay` \(`integer`\)

Specifies the cost delay value that will be used in automatic `VACUUM` operations. If -1 is specified, the regular [vacuum\_cost\_delay](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-VACUUM-COST-DELAY) value will be used. The default value is 20 milliseconds. This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

`autovacuum_vacuum_cost_limit` \(`integer`\)

Specifies the cost limit value that will be used in automatic `VACUUM` operations. If -1 is specified \(which is the default\), the regular [vacuum\_cost\_limit](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-VACUUM-COST-LIMIT) value will be used. Note that the value is distributed proportionally among the running autovacuum workers, if there is more than one, so that the sum of the limits for each worker does not exceed the value of this variable. This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

