# 20.9. 執行階段統計資訊

## 19.9.1. 查詢和索引統計收集器

這些參數控制伺服器端的統計數據收集功能。啟用統計數據收集後，可以透過 pg\_stat 和 pg\_statio 系列系統檢視表取得相關的資料。有關更多資訊，請參閱[第 27 章](../monitoring-database-activity/)。

`track_activities` (`boolean`)

啟用收集有關每個連線的當下執行命令的資訊以及該命令開始執行的時間的資訊。預設情況下，此參數是開啓的。請注意，即使啟用此功能，也不是所有使用者都可以取用，而只有超級使用者和擁有該連線的使用者可以檢視這些數據，因此它不會有安全風險。僅超級使用者可以變更此設定。

`track_activity_query_size` (`integer`)

為 pg\_stat\_activity.query 欄位指定保留的字元數，以追踪每個連線查詢當下執行的指令字串。預設值為1024。只能在伺服器啟動時設定此參數。

`track_counts` (`boolean`)

啟用有關資料庫活動的統計資訊收集。預設情況下，此參數是啟用的，因為 autovacuum 背景程序需要收集資訊。僅超級使用者可以變更此設定。

`track_io_timing` (`boolean`)

啟用資料庫 I/O 呼叫的計時。此參數預設情況下是處於關閉狀態，因為它將重複查詢作業系統當下的時間，這可能會導致某些平台上的大量運算成本。您可以使用 [pg\_test\_timing](../../reference/server-applications/pg\_test\_timing.md) 工具來測量系統計時的成本。I/O 時序資訊會顯示在 [pg\_stat\_database](../monitoring-database-activity/the-statistics-collector.md) 中，使用 BUFFERS 選項時在 [EXPLAIN](../../reference/sql-commands/explain.md) 的輸出中以及 [pg\_stat\_statements](../../appendixes/additional-supplied-modules/pg\_stat\_statements.md) 中顯示。僅超級使用者可以變更改此設定。

`track_functions` (`enum`)

啟用對函數呼叫計數和使用時間的追踪。指定 pl 僅追踪程序語言函數，all 則表示也追踪 SQL 和 C 語言函數。預設值為 none，這將停用函數統計資訊追踪。僅超級使用者可以變更此設定。

**注意**\
不管此設定如何，都不會追踪足夠簡單以「inline」到呼叫查詢中的 SQL 語言函數。

`stats_temp_directory` (`string`)

設定用於儲存臨時統計數據的目錄。這可以是相對於資料目錄的路徑，也可以是絕對路徑。預設值為 pg\_stat\_tmp。將其指向基於 RAM 的檔案系統可以降低物理性 I/O 的要求，使得效能提升。只能在 postgresql.conf 檔案或伺服器命令列中設定此參數。

## 19.9.2. 統計監控

`log_statement_stats` (`boolean`)\
`log_parser_stats` (`boolean`)\
`log_planner_stats` (`boolean`)\
`log_executor_stats` (`boolean`)

對於每個查詢，將相對應模組的效能統計數據輸出到伺服器日誌。這是一個粗略的分析工具，類似於 Unix getrusage() 作業系統的工具。log\_statement\_stats 總計整個查詢語句過程的統計數據，而其他的設定是每個查詢模組的統計數據。log\_statement\_stats 不能與任何其他模組選項同時啟用。預設情況下，所有這些選項都是停用的。只有超級使用者可以變更這些設定。
