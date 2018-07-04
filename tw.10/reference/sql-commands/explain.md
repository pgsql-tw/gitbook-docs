---
description: 版本：10
---

# EXPLAIN

EXPLAIN — 顯示執行計劃的內容

### 語法

```text
EXPLAIN [ ( option [, ...] ) ] statement
EXPLAIN [ ANALYZE ] [ VERBOSE ] statement

where option can be one of:

    ANALYZE [ boolean ]
    VERBOSE [ boolean ]
    COSTS [ boolean ]
    BUFFERS [ boolean ]
    TIMING [ boolean ]
    SUMMARY [ boolean ]
    FORMAT { TEXT | XML | JSON | YAML }
```

### 說明

此命令顯示 PostgreSQL 計劃程序為所提供的查詢語句設計的執行計劃。執行計劃顯示查詢語句如何掃瞄其所引用的資料表 - 通過簡單循序掃描、索引掃描等 - 如果引用了多個資料表，將使用哪些交叉查詢的演算法將每個資料表所需的資料列匯集在一起。

顯示這些資訊的最關鍵部分是估計查詢語句的執行成本，這是計劃程序猜測執行行語句需要多長時間（以成本單位測量，是任何面向的，但通常意味著磁碟頁面讀取）。實際上顯示了兩個數字：可以回傳第一個資料列之前的啟動成本，以及回傳所有資料列的總成本。對於大多數查詢而言，總成本是重要的，但在諸如 EXISTS 中的子查詢之類的查詢中，規劃程序將選擇最小的啟動成本而不是最小的總成本（因為執行程序會在獲得一個資料列之後將停止）。此外，如果使用 LIMIT 子句限制要回傳的資料列數量，則計劃程序會在兩端的成本之間進行適當的插值，以估計哪個計劃確實成本較低。

ANALYZE 選項讓語句實際執行，而不僅僅是計劃而已。然後將實際運行時的統計資訊加到顯示結果中，包括每個計劃節點中消耗的總耗用時間（以毫秒為單位）以及實際回傳的總資料列數。這對於了解規劃程序的估計是否接近現實非常有用。

#### 重點

請記住，當使用 ANALYZE 選項時，實際上會執行該語句。儘管 EXPLAIN 將丟棄 SELECT 回傳的任何輸出，但該語句的其他副作用將照常發生。如果您希望在 INSERT、UPDATE、DELETE、CREATE TABLE AS 或 EXECUTE 語句上使用 EXPLAIN ANALYZE 而不讓命令影響您的資料，請使用以下方法：

```text
BEGIN;
EXPLAIN ANALYZE ...;
ROLLBACK;
```

在未括號的語法中，只有 ANALYZE 和 VERBOSE 選項可以使用，而且也只能依次序使用。在 PostgreSQL 9.0 之前，沒有括號的語法是唯一受支援的語法。預計所有新選項僅在括號語法中受支援。

### Parameters

`ANALYZE`

Carry out the command and show actual run times and other statistics. This parameter defaults to `FALSE`.

`VERBOSE`

Display additional information regarding the plan. Specifically, include the output column list for each node in the plan tree, schema-qualify table and function names, always label variables in expressions with their range table alias, and always print the name of each trigger for which statistics are displayed. This parameter defaults to `FALSE`.

`COSTS`

Include information on the estimated startup and total cost of each plan node, as well as the estimated number of rows and the estimated width of each row. This parameter defaults to `TRUE`.

`BUFFERS`

Include information on buffer usage. Specifically, include the number of shared blocks hit, read, dirtied, and written, the number of local blocks hit, read, dirtied, and written, and the number of temp blocks read and written. A _hit_ means that a read was avoided because the block was found already in cache when needed. Shared blocks contain data from regular tables and indexes; local blocks contain data from temporary tables and indexes; while temp blocks contain short-term working data used in sorts, hashes, Materialize plan nodes, and similar cases. The number of blocks _dirtied_ indicates the number of previously unmodified blocks that were changed by this query; while the number of blocks _written_ indicates the number of previously-dirtied blocks evicted from cache by this backend during query processing. The number of blocks shown for an upper-level node includes those used by all its child nodes. In text format, only non-zero values are printed. This parameter may only be used when `ANALYZE` is also enabled. It defaults to `FALSE`.

`TIMING`

Include actual startup time and time spent in each node in the output. The overhead of repeatedly reading the system clock can slow down the query significantly on some systems, so it may be useful to set this parameter to `FALSE` when only actual row counts, and not exact times, are needed. Run time of the entire statement is always measured, even when node-level timing is turned off with this option. This parameter may only be used when `ANALYZE` is also enabled. It defaults to `TRUE`.

`SUMMARY`

Include summary information \(e.g., totaled timing information\) after the query plan. Summary information is included by default when `ANALYZE` is used but otherwise is not included by default, but can be enabled using this option. Planning time in `EXPLAIN EXECUTE`includes the time required to fetch the plan from the cache and the time required for re-planning, if necessary.

`FORMAT`

Specify the output format, which can be TEXT, XML, JSON, or YAML. Non-text output contains the same information as the text output format, but is easier for programs to parse. This parameter defaults to `TEXT`.

_`boolean`_

Specifies whether the selected option should be turned on or off. You can write `TRUE`, `ON`, or `1` to enable the option, and `FALSE`, `OFF`, or `0` to disable it. The _`boolean`_ value can also be omitted, in which case `TRUE` is assumed.

_`statement`_

Any `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `VALUES`, `EXECUTE`, `DECLARE`, `CREATE TABLE AS`, or `CREATE MATERIALIZED VIEW AS` statement, whose execution plan you wish to see.

### Outputs

The command's result is a textual description of the plan selected for the _`statement`_, optionally annotated with execution statistics. [Section 14.1](https://www.postgresql.org/docs/10/static/using-explain.html) describes the information provided.

### Notes

In order to allow the PostgreSQL query planner to make reasonably informed decisions when optimizing queries, the [`pg_statistic`](https://www.postgresql.org/docs/10/static/catalog-pg-statistic.html) data should be up-to-date for all tables used in the query. Normally the [autovacuum daemon](https://www.postgresql.org/docs/10/static/routine-vacuuming.html#AUTOVACUUM) will take care of that automatically. But if a table has recently had substantial changes in its contents, you might need to do a manual [ANALYZE](https://www.postgresql.org/docs/10/static/sql-analyze.html) rather than wait for autovacuum to catch up with the changes.

In order to measure the run-time cost of each node in the execution plan, the current implementation of `EXPLAIN ANALYZE` adds profiling overhead to query execution. As a result, running `EXPLAIN ANALYZE` on a query can sometimes take significantly longer than executing the query normally. The amount of overhead depends on the nature of the query, as well as the platform being used. The worst case occurs for plan nodes that in themselves require very little time per execution, and on machines that have relatively slow operating system calls for obtaining the time of day.

### Examples

To show the plan for a simple query on a table with a single `integer` column and 10000 rows:

```text
EXPLAIN SELECT * FROM foo;

                       QUERY PLAN
---------------------------------------------------------
 Seq Scan on foo  (cost=0.00..155.00 rows=10000 width=4)
(1 row)
```

Here is the same query, with JSON output formatting:

```text
EXPLAIN (FORMAT JSON) SELECT * FROM foo;
           QUERY PLAN
--------------------------------
 [                             +
   {                           +
     "Plan": {                 +
       "Node Type": "Seq Scan",+
       "Relation Name": "foo", +
       "Alias": "foo",         +
       "Startup Cost": 0.00,   +
       "Total Cost": 155.00,   +
       "Plan Rows": 10000,     +
       "Plan Width": 4         +
     }                         +
   }                           +
 ]
(1 row)
```

If there is an index and we use a query with an indexable `WHERE` condition, `EXPLAIN` might show a different plan:

```text
EXPLAIN SELECT * FROM foo WHERE i = 4;

                         QUERY PLAN
--------------------------------------------------------------
 Index Scan using fi on foo  (cost=0.00..5.98 rows=1 width=4)
   Index Cond: (i = 4)
(2 rows)
```

Here is the same query, but in YAML format:

```text
EXPLAIN (FORMAT YAML) SELECT * FROM foo WHERE i='4';
          QUERY PLAN
-------------------------------
 - Plan:                      +
     Node Type: "Index Scan"  +
     Scan Direction: "Forward"+
     Index Name: "fi"         +
     Relation Name: "foo"     +
     Alias: "foo"             +
     Startup Cost: 0.00       +
     Total Cost: 5.98         +
     Plan Rows: 1             +
     Plan Width: 4            +
     Index Cond: "(i = 4)"    
(1 row)
```

XML format is left as an exercise for the reader.

Here is the same plan with cost estimates suppressed:

```text
EXPLAIN (COSTS FALSE) SELECT * FROM foo WHERE i = 4;

        QUERY PLAN
----------------------------
 Index Scan using fi on foo
   Index Cond: (i = 4)
(2 rows)
```

Here is an example of a query plan for a query using an aggregate function:

```text
EXPLAIN SELECT sum(i) FROM foo WHERE i < 10;

                             QUERY PLAN
---------------------------------------------------------------------
 Aggregate  (cost=23.93..23.93 rows=1 width=4)
   ->  Index Scan using fi on foo  (cost=0.00..23.92 rows=6 width=4)
         Index Cond: (i < 10)
(3 rows)
```

Here is an example of using `EXPLAIN EXECUTE` to display the execution plan for a prepared query:

```text
PREPARE query(int, int) AS SELECT sum(bar) FROM test
    WHERE id > $1 AND id < $2
    GROUP BY foo;

EXPLAIN ANALYZE EXECUTE query(100, 200);

                                                       QUERY PLAN                                                       
------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=9.54..9.54 rows=1 width=8) (actual time=0.156..0.161 rows=11 loops=1)
   Group Key: foo
   ->  Index Scan using test_pkey on test  (cost=0.29..9.29 rows=50 width=8) (actual time=0.039..0.091 rows=99 loops=1)
         Index Cond: ((id > $1) AND (id < $2))
 Planning time: 0.197 ms
 Execution time: 0.225 ms
(6 rows)
```

Of course, the specific numbers shown here depend on the actual contents of the tables involved. Also note that the numbers, and even the selected query strategy, might vary between PostgreSQL releases due to planner improvements. In addition, the `ANALYZE` command uses random sampling to estimate data statistics; therefore, it is possible for cost estimates to change after a fresh run of `ANALYZE`, even if the actual distribution of data in the table has not changed.

### Compatibility

There is no `EXPLAIN` statement defined in the SQL standard.

### See Also

[ANALYZE](https://www.postgresql.org/docs/10/static/sql-analyze.html)

