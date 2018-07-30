---
description: 版本：10
---

# ANALYZE

ANALYZE — 收集有關資料庫的統計資訊

### 語法

```text
ANALYZE [ VERBOSE ] [ table_name [ ( column_name [, ...] ) ] ]
```

### 說明

ANALYZE 收集有關資料庫中資料表內容的統計資訊，並將結果儲在在 pg\_statistic 系統目錄中。然後，查詢計劃程序會使用這些統計資訊來幫助決定查詢的最有效執行計劃。

如果沒有參數，ANALYZE 會檢查目前資料庫中的每個資料表。使用參數時，ANALYZE 僅檢查該資料表。還可以輸出欄位名稱列表，在這種情況下，僅收集這些欄位的統計資訊。

### 參數

`VERBOSE`

啟用進度訊息的顯示。

_`table_name`_

要分析的特定資料表的名稱（可以加入綱要名稱）。如果省略，則分析目前資料庫中的所有一般資料表，分割資料表和具體化檢視表（但不包括外部資料表）。如果指定的資料表是分割資料表，則更新分割資料表的繼承統計資訊和各個分割區的統計資訊。

_`column_name`_

要分析特定欄位的名稱。預設為所有欄位。

### 輸出

指定 VERBOSE 時，ANALYZE 會輸出進度訊息以顯示目前正在處理哪個資料表。還會列出有關資料表的各種統計資訊。

### Notes

Foreign tables are analyzed only when explicitly selected. Not all foreign data wrappers support `ANALYZE`. If the table's wrapper does not support `ANALYZE`, the command prints a warning and does nothing.

In the default PostgreSQL configuration, the autovacuum daemon \(see [Section 24.1.6](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#AUTOVACUUM)\) takes care of automatic analyzing of tables when they are first loaded with data, and as they change throughout regular operation. When autovacuum is disabled, it is a good idea to run `ANALYZE` periodically, or just after making major changes in the contents of a table. Accurate statistics will help the planner to choose the most appropriate query plan, and thereby improve the speed of query processing. A common strategy for read-mostly databases is to run [VACUUM](https://www.postgresql.org/docs/10/static/sql-vacuum.html) and `ANALYZE` once a day during a low-usage time of day. \(This will not be sufficient if there is heavy update activity.\)

`ANALYZE` requires only a read lock on the target table, so it can run in parallel with other activity on the table.

The statistics collected by `ANALYZE` usually include a list of some of the most common values in each column and a histogram showing the approximate data distribution in each column. One or both of these can be omitted if `ANALYZE` deems them uninteresting \(for example, in a unique-key column, there are no common values\) or if the column data type does not support the appropriate operators. There is more information about the statistics in [Chapter 24](https://www.postgresql.org/docs/10/static/maintenance.html).

For large tables, `ANALYZE` takes a random sample of the table contents, rather than examining every row. This allows even very large tables to be analyzed in a small amount of time. Note, however, that the statistics are only approximate, and will change slightly each time `ANALYZE` is run, even if the actual table contents did not change. This might result in small changes in the planner's estimated costs shown by [EXPLAIN](https://www.postgresql.org/docs/10/static/sql-explain.html). In rare situations, this non-determinism will cause the planner's choices of query plans to change after `ANALYZE` is run. To avoid this, raise the amount of statistics collected by `ANALYZE`, as described below.

The extent of analysis can be controlled by adjusting the [default\_statistics\_target](https://www.postgresql.org/docs/10/static/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET) configuration variable, or on a column-by-column basis by setting the per-column statistics target with `ALTER TABLE ... ALTER COLUMN ... SET STATISTICS` \(see [ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html)\). The target value sets the maximum number of entries in the most-common-value list and the maximum number of bins in the histogram. The default target value is 100, but this can be adjusted up or down to trade off accuracy of planner estimates against the time taken for `ANALYZE` and the amount of space occupied in `pg_statistic`. In particular, setting the statistics target to zero disables collection of statistics for that column. It might be useful to do that for columns that are never used as part of the `WHERE`, `GROUP BY`, or `ORDER BY` clauses of queries, since the planner will have no use for statistics on such columns.

The largest statistics target among the columns being analyzed determines the number of table rows sampled to prepare the statistics. Increasing the target causes a proportional increase in the time and space needed to do `ANALYZE`.

One of the values estimated by `ANALYZE` is the number of distinct values that appear in each column. Because only a subset of the rows are examined, this estimate can sometimes be quite inaccurate, even with the largest possible statistics target. If this inaccuracy leads to bad query plans, a more accurate value can be determined manually and then installed with `ALTER TABLE ... ALTER COLUMN ... SET (n_distinct = ...)` \(see [ALTER TABLE](https://www.postgresql.org/docs/10/static/sql-altertable.html)\).

If the table being analyzed has one or more children, `ANALYZE` will gather statistics twice: once on the rows of the parent table only, and a second time on the rows of the parent table with all of its children. This second set of statistics is needed when planning queries that traverse the entire inheritance tree. The autovacuum daemon, however, will only consider inserts or updates on the parent table itself when deciding whether to trigger an automatic analyze for that table. If that table is rarely inserted into or updated, the inheritance statistics will not be up to date unless you run `ANALYZE` manually.

If any of the child tables are foreign tables whose foreign data wrappers do not support `ANALYZE`, those child tables are ignored while gathering inheritance statistics.

If the table being analyzed is completely empty, `ANALYZE` will not record new statistics for that table. Any existing statistics will be retained.

### 相容性

SQL 標準中沒有 ANALYZE 語句。

### 參閱

[VACUUM](vacuum.md), [vacuumdb](../ii.-postgresql-yong-hu-duan-gong-ju/vacuumdb.md), [Section 19.4.4](../../server-administration/server-configuration/resource-consumption.md#19-4-4-cheng-ben-kao-liang-de-vacuum-yan), [Section 24.1.6](../../server-administration/routine-database-maintenance-tasks/routine-vacuuming.md#24-1-6-autovacuum-bei-jing-cheng-xu)

