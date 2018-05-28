# VACUUM

VACUUM — 資源回收並且選擇性地重整資料庫

### 語法

```text
VACUUM [ ( { FULL | FREEZE | VERBOSE | ANALYZE | DISABLE_PAGE_SKIPPING } [, ...] ) ]
       [ table_name [ (column_name [, ...] ) ] ]
VACUUM [ FULL ] [ FREEZE ] [ VERBOSE ] [ table_name ]
VACUUM [ FULL ] [ FREEZE ] [ VERBOSE ] 
       ANALYZE [ table_name [ (column_name [, ...] ) ] ]
```

### 說明

VACUUM 回收不再使用的儲存空間。在普通的 PostgreSQL 操作中，被刪除或被更新的儲存空間實際上並不會真實在磁碟上刪除；它們會一直存在，直到 VACUUM 完成。因此，必須定期執行 VACUUM，尤其是在經常更新的資料表上。

在沒有參數的情況下，VACUUM 處理目前資料庫中目前使用者有權清理的每個資料表。使用參數的話，VACUUM 就能只處理某個資料表。

VACUUM ANALYZE 為每個選定的資料表執行 VACUUM 然後進行 ANALYZE 分析。 這是日常維護腳本的便捷組合形式。有關其處理的更多詳細訊息，請參閱 [ANALYZE](analyze.md)。

Plain `VACUUM` \(without `FULL`\) simply reclaims space and makes it available for re-use. This form of the command can operate in parallel with normal reading and writing of the table, as an exclusive lock is not obtained. However, extra space is not returned to the operating system \(in most cases\); it's just kept available for re-use within the same table. `VACUUM FULL` rewrites the entire contents of the table into a new disk file with no extra space, allowing unused space to be returned to the operating system. This form is much slower and requires an exclusive lock on each table while it is being processed.

When the option list is surrounded by parentheses, the options can be written in any order. Without parentheses, options must be specified in exactly the order shown above. The parenthesized syntax was added in PostgreSQL 9.0; the unparenthesized syntax is deprecated.

### Parameters

`FULL`

Selects “full” vacuum, which can reclaim more space, but takes much longer and exclusively locks the table. This method also requires extra disk space, since it writes a new copy of the table and doesn't release the old copy until the operation is complete. Usually this should only be used when a significant amount of space needs to be reclaimed from within the table.

`FREEZE`

選擇積極的「凍結」tuple。指定 FREEZE 等同於使用將 [vacuum\_freeze\_min\_age ](../../server-administration/runtime-config/runtime-config-client.md#19-11-1-cha-ju-de-hang)和 [vacuum\_freeze\_table\_age](../../server-administration/runtime-config/runtime-config-client.md#19-11-1-cha-ju-de-hang) 參數設定為零來執行 VACUUM。資料表在重寫時始終執行積極凍結，因此當指定 FULL 時這個選項是多餘的。

`VERBOSE`

為每個資料表輸出詳細的清理活動報告。

`ANALYZE`

更新查詢規劃單元需要使用的統計訊息，以決定最有效執行查詢的方式。

`DISABLE_PAGE_SKIPPING`

Normally, `VACUUM` will skip pages based on the [visibility map](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#VACUUM-FOR-VISIBILITY-MAP). Pages where all tuples are known to be frozen can always be skipped, and those where all tuples are known to be visible to all transactions may be skipped except when performing an aggressive vacuum. Furthermore, except when performing an aggressive vacuum, some pages may be skipped in order to avoid waiting for other sessions to finish using them. This option disables all page-skipping behavior, and is intended to be used only the contents of the visibility map are thought to be suspect, which should happen only if there is a hardware or software issue causing database corruption.

_`table_name`_

The name \(optionally schema-qualified\) of a specific table to vacuum. If omitted, all regular tables and materialized views in the current database are vacuumed. If the specified table is a partitioned table, all of its leaf partitions are vacuumed.

_`column_name`_

The name of a specific column to analyze. Defaults to all columns. If a column list is specified, `ANALYZE` is implied.

### Outputs

When `VERBOSE` is specified, `VACUUM` emits progress messages to indicate which table is currently being processed. Various statistics about the tables are printed as well.

### Notes

To vacuum a table, one must ordinarily be the table's owner or a superuser. However, database owners are allowed to vacuum all tables in their databases, except shared catalogs. \(The restriction for shared catalogs means that a true database-wide `VACUUM` can only be performed by a superuser.\) `VACUUM` will skip over any tables that the calling user does not have permission to vacuum.

`VACUUM` cannot be executed inside a transaction block.

For tables with GIN indexes, `VACUUM` \(in any form\) also completes any pending index insertions, by moving pending index entries to the appropriate places in the main GIN index structure. See [Section 64.4.1](https://www.postgresql.org/docs/10/static/gin-implementation.html#GIN-FAST-UPDATE) for details.

We recommend that active production databases be vacuumed frequently \(at least nightly\), in order to remove dead rows. After adding or deleting a large number of rows, it might be a good idea to issue a `VACUUM ANALYZE` command for the affected table. This will update the system catalogs with the results of all recent changes, and allow the PostgreSQL query planner to make better choices in planning queries.

The `FULL` option is not recommended for routine use, but might be useful in special cases. An example is when you have deleted or updated most of the rows in a table and would like the table to physically shrink to occupy less disk space and allow faster table scans. `VACUUM FULL` will usually shrink the table more than a plain `VACUUM` would.

`VACUUM` causes a substantial increase in I/O traffic, which might cause poor performance for other active sessions. Therefore, it is sometimes advisable to use the cost-based vacuum delay feature. See [Section 19.4.4](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-VACUUM-COST) for details.

PostgreSQL includes an “autovacuum” facility which can automate routine vacuum maintenance. For more information about automatic and manual vacuuming, see [Section 24.1](https://www.postgresql.org/docs/10/static/routine-vacuuming.html).

### Examples

To clean a single table `onek`, analyze it for the optimizer and print a detailed vacuum activity report:

```text
VACUUM (VERBOSE, ANALYZE) onek;
```

### Compatibility

There is no `VACUUM` statement in the SQL standard.

### See Also

vacuumdb, [19.4.4 節](../../server-administration/runtime-config/resource-consumption.md#19-4-4-cost-based-vacuum-delay), [24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#24-1-6-the-autovacuum-daemon)

