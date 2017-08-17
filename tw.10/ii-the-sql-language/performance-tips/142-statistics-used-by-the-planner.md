# 14.2. 統計資訊[^1]

[14.2.1. Single-Column Statistics](https://www.postgresql.org/docs/10/static/planner-stats.html#idm46249847406640)

[14.2.2. Extended Statistics](https://www.postgresql.org/docs/10/static/planner-stats.html#planner-stats-extended)



### 14.2.1. Single-Column Statistics

As we saw in the previous section, the query planner needs to estimate the number of rows retrieved by a query in order to make good choices of query plans. This section provides a quick look at the statistics that the system uses for these estimates.

One component of the statistics is the total number of entries in each table and index, as well as the number of disk blocks occupied by each table and index. This information is kept in the table[`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html), in the columns`reltuples`and`relpages`. We can look at it with queries similar to this one:

```
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

Here we can see that`tenk1`contains 10000 rows, as do its indexes, but the indexes are \(unsurprisingly\) much smaller than the table.

For efficiency reasons,`reltuples`and`relpages`are not updated on-the-fly, and so they usually contain somewhat out-of-date values. They are updated by`VACUUM`,`ANALYZE`, and a few DDL commands such as`CREATE INDEX`. A`VACUUM`or`ANALYZE`operation that does not scan the entire table \(which is commonly the case\) will incrementally update the`reltuples`count on the basis of the part of the table it did scan, resulting in an approximate value. In any case, the planner will scale the values it finds in`pg_class`to match the current physical table size, thus obtaining a closer approximation.



Most queries retrieve only a fraction of the rows in a table, due to`WHERE`clauses that restrict the rows to be examined. The planner thus needs to make an estimate of the_selectivity_of`WHERE`clauses, that is, the fraction of rows that match each condition in the`WHERE`clause. The information used for this task is stored in the[`pg_statistic`](https://www.postgresql.org/docs/10/static/catalog-pg-statistic.html)system catalog. Entries in`pg_statistic`are updated by the`ANALYZE`and`VACUUM ANALYZE`commands, and are always approximate even when freshly updated.



Rather than look at`pg_statistic`directly, it's better to look at its view[`pg_stats`](https://www.postgresql.org/docs/10/static/view-pg-stats.html)when examining the statistics manually.`pg_stats`is designed to be more easily readable. Furthermore,`pg_stats`is readable by all, whereas`pg_statistic`is only readable by a superuser. \(This prevents unprivileged users from learning something about the contents of other people's tables from the statistics. The`pg_stats`view is restricted to show only rows about tables that the current user can read.\) For example, we might do:

```
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

Note that two rows are displayed for the same column, one corresponding to the complete inheritance hierarchy starting at the`road`table \(`inherited`=`t`\), and another one including only the`road`table itself \(`inherited`=`f`\).

The amount of information stored in`pg_statistic`by`ANALYZE`, in particular the maximum number of entries in the`most_common_vals`and`histogram_bounds`arrays for each column, can be set on a column-by-column basis using the`ALTER TABLE SET STATISTICS`command, or globally by setting the[default\_statistics\_target](https://www.postgresql.org/docs/10/static/runtime-config-query.html#guc-default-statistics-target)configuration variable. The default limit is presently 100 entries. Raising the limit might allow more accurate planner estimates to be made, particularly for columns with irregular data distributions, at the price of consuming more space in`pg_statistic`and slightly more time to compute the estimates. Conversely, a lower limit might be sufficient for columns with simple data distributions.

Further details about the planner's use of statistics can be found in[Chapter 68](https://www.postgresql.org/docs/10/static/planner-stats-details.html).

### 14.2.2. Extended Statistics







It is common to see slow queries running bad execution plans because multiple columns used in the query clauses are correlated. The planner normally assumes that multiple conditions are independent of each other, an assumption that does not hold when column values are correlated. Regular statistics, because of their per-individual-column nature, cannot capture any knowledge about cross-column correlation. However,PostgreSQLhas the ability to compute_multivariate statistics_, which can capture such information.

Because the number of possible column combinations is very large, it's impractical to compute multivariate statistics automatically. Instead,_extended statistics objects_, more often called just_statistics objects_, can be created to instruct the server to obtain statistics across interesting sets of columns.

Statistics objects are created using[CREATE STATISTICS](https://www.postgresql.org/docs/10/static/sql-createstatistics.html), which see for more details. Creation of such an object merely creates a catalog entry expressing interest in the statistics. Actual data collection is performed by`ANALYZE`\(either a manual command, or background auto-analyze\). The collected values can be examined in the[`pg_statistic_ext`](https://www.postgresql.org/docs/10/static/catalog-pg-statistic-ext.html)catalog.

`ANALYZE`computes extended statistics based on the same sample of table rows that it takes for computing regular single-column statistics. Since the sample size is increased by increasing the statistics target for the table or any of its columns \(as described in the previous section\), a larger statistics target will normally result in more accurate extended statistics, as well as more time spent calculating them.

The following subsections describe the types of extended statistics that are currently supported.

#### 14.2.2.1. Functional Dependencies

The simplest type of extended statistics tracks_functional dependencies_, a concept used in definitions of database normal forms. We say that column`b`is functionally dependent on column`a`if knowledge of the value of`a`is sufficient to determine the value of`b`, that is there are no two rows having the same value of`a`but different values of`b`. In a fully normalized database, functional dependencies should exist only on primary keys and superkeys. However, in practice many data sets are not fully normalized for various reasons; intentional denormalization for performance reasons is a common example. Even in a fully normalized database, there may be partial correlation between some columns, which can be expressed as partial functional dependency.

The existence of functional dependencies directly affects the accuracy of estimates in certain queries. If a query contains conditions on both the independent and the dependent column\(s\), the conditions on the dependent columns do not further reduce the result size; but without knowledge of the functional dependency, the query planner will assume that the conditions are independent, resulting in underestimating the result size.

To inform the planner about functional dependencies,`ANALYZE`can collect measurements of cross-column dependency. Assessing the degree of dependency between all sets of columns would be prohibitively expensive, so data collection is limited to those groups of columns appearing together in a statistics object defined with the`dependencies`option. It is advisable to create`dependencies`statistics only for column groups that are strongly correlated, to avoid unnecessary overhead in both`ANALYZE`and later query planning.

Here is an example of collecting functional-dependency statistics:

```
CREATE STATISTICS stts (dependencies) ON zip, city FROM zipcodes;

ANALYZE zipcodes;

SELECT stxname, stxkeys, stxdependencies
  FROM pg_statistic_ext
  WHERE stxname = 'stts';
 stxname | stxkeys |             stxdependencies               
---------+---------+------------------------------------------
 stts    | 1 5     | {"1 =
>
 5": 1.000000, "5 =
>
 1": 0.423130}
(1 row)

```

Here it can be seen that column 1 \(zip code\) fully determines column 5 \(city\) so the coefficient is 1.0, while city only determines zip code about 42% of the time, meaning that there are many cities \(58%\) that are represented by more than a single ZIP code.

When computing the selectivity for a query involving functionally dependent columns, the planner adjusts the per-condition selectivity estimates using the dependency coefficients so as not to produce an underestimate.

##### 14.2.2.1.1. Limitations of Functional Dependencies

Functional dependencies are currently only applied when considering simple equality conditions that compare columns to constant values. They are not used to improve estimates for equality conditions comparing two columns or comparing a column to an expression, nor for range clauses,`LIKE`or any other type of condition.

When estimating with functional dependencies, the planner assumes that conditions on the involved columns are compatible and hence redundant. If they are incompatible, the correct estimate would be zero rows, but that possibility is not considered. For example, given a query like

```
SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '94105';

```

the planner will disregard the`city`clause as not changing the selectivity, which is correct. However, it will make the same assumption about

```
SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '90210';

```

even though there will really be zero rows satisfying this query. Functional dependency statistics do not provide enough information to conclude that, however.

In many practical situations, this assumption is usually satisfied; for example, there might be a GUI in the application that only allows selecting compatible city and zipcode values to use in a query. But if that's not the case, functional dependencies may not be a viable option.

#### 14.2.2.2. Multivariate N-Distinct Counts

Single-column statistics store the number of distinct values in each column. Estimates of the number of distinct values when combining more than one column \(for example, for`GROUP BY a, b`\) are frequently wrong when the planner only has single-column statistical data, causing it to select bad plans.

To improve such estimates,`ANALYZE`can collect n-distinct statistics for groups of columns. As before, it's impractical to do this for every possible column grouping, so data is collected only for those groups of columns appearing together in a statistics object defined with the`ndistinct`option. Data will be collected for each possible combination of two or more columns from the set of listed columns.

Continuing the previous example, the n-distinct counts in a table of ZIP codes might look like the following:

```
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

It's advisable to create`ndistinct`statistics objects only on combinations of columns that are actually used for grouping, and for which misestimation of the number of groups is resulting in bad plans. Otherwise, the`ANALYZE`cycles are just wasted.

---



[^1]:  [PostgreSQL: Documentation: 10: 14.2. Statistics Used by the Planner](https://www.postgresql.org/docs/10/static/planner-stats.html)

