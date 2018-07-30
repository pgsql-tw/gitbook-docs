---
description: 版本：10
---

# 14.2. 統計資訊

## 14.2.1. 單一欄位統計資訊

正如我們在上一節中看到的那樣，查詢規劃程序需要估計查詢檢索的資料列數量，以便對查詢計劃做出正確的選擇。本節簡要介紹系統用於這些估算的統計訊息。

統計訊息的其中一部分是每個資料表和索引中的項目總數，以及每個資料表和索引佔用的磁磁區塊數。此訊息保存在資料表 [pg\_class](../../internals/system-catalogs/pg_class.md) 中，列在 reltuples 和 relpages 欄位中。我們可以使用與此類似的查詢來查看它：

```text
SELECT relname, relkind, reltuples, relpages
FROM pg_class
WHERE relname LIKE 'tenk1%';

       relname        | relkind | reltuples | relpages
----------------------+---------+-----------+----------
 tenk1                | r       |     10000 |      358
 tenk1_hundred        | i       |     10000 |       30
 tenk1_thous_tenthous | i       |     10000 |       30
 tenk1_unique1        | i       |     10000 |       30
 tenk1_unique2        | i       |     10000 |       30
(5 rows)
```

在這裡我們可以看到 tenk1 包含 10000 個資料列，其索引也是如此，但索引（不出所料）比資料表小得多。

由於效率因素，reltuples 和 relpup 並不會即時更新，因此它們通常包含一些過時的值。它們由 VACUUM，ANALYZE 和一些 DDL 指令（如 CREATE INDEX）更新。不掃描整個資料表的 VACUUM 或 ANALYZE 操作（通常是這種情況）將根據其掃描資料表的部分逐步更新 reltuples 計數，從而得到近似值。在任何情況下，規劃程序將縮放它在 pg\_class 中找到的值以匹配目前實際上資料表大小，從而獲得更接近的近似值。

由於 WHERE 子句會限制要檢查的資料列，因此大多數查詢僅檢索資料表中的一小部分行。因此，規劃程序需要估計 WHERE 子句的篩選性，即與 WHERE 子句中的每個條件匹配的資料列比率。用於此任務的訊息儲存在 [pg\_statistic](../../internals/system-catalogs/51.50.-pg_statistic.md) 系統目錄中。pg\_statistic 中的項目由 ANALYZE 和 VACUUM ANALYZE 指令更新，即使在剛更新時也都是近似值。

除了直接查看 pg\_statistic，最好在手動檢查統計訊息時查看其檢視表 [pg\_stats](../../internals/system-catalogs/pg_stats.md)。pg\_stats 旨在於更容易閱讀。此外，所有人都可以讀取 pg\_stats，而 pg\_statistic 只能由超級使用者讀取。（這可以防止非特權使用者從統計訊息中學習有關其他人表的內容。pg\_stats 檢視表僅限於顯示目前使用者可以讀取的資料表資訊。）例如，我們可能會這樣做：

```text
SELECT attname, inherited, n_distinct,
       array_to_string(most_common_vals, E'\n') as most_common_vals
FROM pg_stats
WHERE tablename = 'road';

 attname | inherited | n_distinct |          most_common_vals
---------+-----------+------------+------------------------------------
 name    | f         |  -0.363388 | I- 580                        Ramp+
         |           |            | I- 880                        Ramp+
         |           |            | Sp Railroad                       +
         |           |            | I- 580                            +
         |           |            | I- 680                        Ramp
 name    | t         |  -0.284859 | I- 880                        Ramp+
         |           |            | I- 580                        Ramp+
         |           |            | I- 680                        Ramp+
         |           |            | I- 580                            +
         |           |            | State Hwy 13                  Ramp
(2 rows)
```

請注意，同一欄位顯示兩行，一行對應於從路徑表開始的完整繼承層次結構（inherited = t），另一行僅包含路徑表本身（inherited = f）。

ANALYZE 儲存在 pg\_statistic 中的資訊量，特別是每欄位的 most\_common\_vals 和 histogram\_bounds 陣列中的最大項目數，可以使用 ALTER TABLE SET STATISTICS 指令逐個欄位設定，也可以透過設定全域的 [default\_statistics\_target](../../server-administration/server-configuration/query-planning.md#19-7-4-other-planner-options) 組態變數。預設限制目前是 100 個項目。提高限制可能允許進行更準確的計劃程序估算，特別是對於具有不規則資料分佈的欄位，其代價是在 pg\_statistic 中消耗更多空間並且計算估計的時間稍長。相反地，對於具有簡單資料分佈的欄位，下限可能就足夠了。

有關規劃程序使用統計資料的更多詳細訊息，請參閱[第 68 章](../../internals/68.-how-the-planner-uses-statistics.md)。

## 14.2.2. Extended Statistics

It is common to see slow queries running bad execution plans because multiple columns used in the query clauses are correlated. The planner normally assumes that multiple conditions are independent of each other, an assumption that does not hold when column values are correlated. Regular statistics, because of their per-individual-column nature, cannot capture any knowledge about cross-column correlation. However, PostgreSQL has the ability to compute _multivariate statistics_, which can capture such information.

Because the number of possible column combinations is very large, it's impractical to compute multivariate statistics automatically. Instead, _extended statistics objects_, more often called just _statistics objects_, can be created to instruct the server to obtain statistics across interesting sets of columns.

Statistics objects are created using [CREATE STATISTICS](https://www.postgresql.org/docs/10/static/sql-createstatistics.html), which see for more details. Creation of such an object merely creates a catalog entry expressing interest in the statistics. Actual data collection is performed by `ANALYZE` \(either a manual command, or background auto-analyze\). The collected values can be examined in the [`pg_statistic_ext`](https://www.postgresql.org/docs/10/static/catalog-pg-statistic-ext.html) catalog.

`ANALYZE` computes extended statistics based on the same sample of table rows that it takes for computing regular single-column statistics. Since the sample size is increased by increasing the statistics target for the table or any of its columns \(as described in the previous section\), a larger statistics target will normally result in more accurate extended statistics, as well as more time spent calculating them.

The following subsections describe the kinds of extended statistics that are currently supported.

### **14.2.2.1. Functional Dependencies**

The simplest kind of extended statistics tracks _functional dependencies_, a concept used in definitions of database normal forms. We say that column `b` is functionally dependent on column `a` if knowledge of the value of `a` is sufficient to determine the value of `b`, that is there are no two rows having the same value of `a` but different values of `b`. In a fully normalized database, functional dependencies should exist only on primary keys and superkeys. However, in practice many data sets are not fully normalized for various reasons; intentional denormalization for performance reasons is a common example. Even in a fully normalized database, there may be partial correlation between some columns, which can be expressed as partial functional dependency.

The existence of functional dependencies directly affects the accuracy of estimates in certain queries. If a query contains conditions on both the independent and the dependent column\(s\), the conditions on the dependent columns do not further reduce the result size; but without knowledge of the functional dependency, the query planner will assume that the conditions are independent, resulting in underestimating the result size.

To inform the planner about functional dependencies, `ANALYZE` can collect measurements of cross-column dependency. Assessing the degree of dependency between all sets of columns would be prohibitively expensive, so data collection is limited to those groups of columns appearing together in a statistics object defined with the `dependencies` option. It is advisable to create `dependencies` statistics only for column groups that are strongly correlated, to avoid unnecessary overhead in both `ANALYZE` and later query planning.

Here is an example of collecting functional-dependency statistics:

```text
CREATE STATISTICS stts (dependencies) ON zip, city FROM zipcodes;

ANALYZE zipcodes;

SELECT stxname, stxkeys, stxdependencies
  FROM pg_statistic_ext
  WHERE stxname = 'stts';
 stxname | stxkeys |             stxdependencies               
---------+---------+------------------------------------------
 stts    | 1 5     | {"1 => 5": 1.000000, "5 => 1": 0.423130}
(1 row)
```

Here it can be seen that column 1 \(zip code\) fully determines column 5 \(city\) so the coefficient is 1.0, while city only determines zip code about 42% of the time, meaning that there are many cities \(58%\) that are represented by more than a single ZIP code.

When computing the selectivity for a query involving functionally dependent columns, the planner adjusts the per-condition selectivity estimates using the dependency coefficients so as not to produce an underestimate.

#### **14.2.2.1.1. Limitations of Functional Dependencies**

Functional dependencies are currently only applied when considering simple equality conditions that compare columns to constant values. They are not used to improve estimates for equality conditions comparing two columns or comparing a column to an expression, nor for range clauses, `LIKE` or any other type of condition.

When estimating with functional dependencies, the planner assumes that conditions on the involved columns are compatible and hence redundant. If they are incompatible, the correct estimate would be zero rows, but that possibility is not considered. For example, given a query like

```text
SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '94105';
```

the planner will disregard the `city` clause as not changing the selectivity, which is correct. However, it will make the same assumption about

```text
SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '90210';
```

even though there will really be zero rows satisfying this query. Functional dependency statistics do not provide enough information to conclude that, however.

In many practical situations, this assumption is usually satisfied; for example, there might be a GUI in the application that only allows selecting compatible city and ZIP code values to use in a query. But if that's not the case, functional dependencies may not be a viable option.

### **14.2.2.2. Multivariate N-Distinct Counts**

Single-column statistics store the number of distinct values in each column. Estimates of the number of distinct values when combining more than one column \(for example, for `GROUP BY a, b`\) are frequently wrong when the planner only has single-column statistical data, causing it to select bad plans.

To improve such estimates, `ANALYZE` can collect n-distinct statistics for groups of columns. As before, it's impractical to do this for every possible column grouping, so data is collected only for those groups of columns appearing together in a statistics object defined with the `ndistinct` option. Data will be collected for each possible combination of two or more columns from the set of listed columns.

Continuing the previous example, the n-distinct counts in a table of ZIP codes might look like the following:

```text
CREATE STATISTICS stts2 (ndistinct) ON zip, state, city FROM zipcodes;

ANALYZE zipcodes;

SELECT stxkeys AS k, stxndistinct AS nd
  FROM pg_statistic_ext
  WHERE stxname = 'stts2';
-[ RECORD 1 ]--------------------------------------------------------
k  | 1 2 5
nd | {"1, 2": 33178, "1, 5": 33178, "2, 5": 27435, "1, 2, 5": 33178}
(1 row)
```

This indicates that there are three combinations of columns that have 33178 distinct values: ZIP code and state; ZIP code and city; and ZIP code, city and state \(the fact that they are all equal is expected given that ZIP code alone is unique in this table\). On the other hand, the combination of city and state has only 27435 distinct values.

It's advisable to create `ndistinct` statistics objects only on combinations of columns that are actually used for grouping, and for which misestimation of the number of groups is resulting in bad plans. Otherwise, the `ANALYZE` cycles are just wasted.

