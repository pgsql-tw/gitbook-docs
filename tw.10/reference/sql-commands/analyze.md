# ANALYZE

### Name

ANALYZE -- collect statistics about a database

### Synopsis

```text
ANALYZE [ VERBOSE ] [ table [ ( column [, ...] ) ] ]
```

### Description

ANALYZE collects statistics about the contents of tables in the database, and stores the results in the [pg\_statistic](https://www.postgresql.org/docs/9.1/static/catalog-pg-statistic.html) system catalog. Subsequently, the query planner uses these statistics to help determine the most efficient execution plans for queries.

With no parameter, ANALYZE examines every table in the current database. With a parameter, ANALYZE examines only that table. It is further possible to give a list of column names, in which case only the statistics for those columns are collected.

### Parameters

VERBOSE

Enables display of progress messages.table

The name \(possibly schema-qualified\) of a specific table to analyze. Defaults to all tables in the current database.column

The name of a specific column to analyze. Defaults to all columns.

### Outputs

When VERBOSE is specified, ANALYZE emits progress messages to indicate which table is currently being processed. Various statistics about the tables are printed as well.

### Notes

In the default PostgreSQL configuration, the autovacuum daemon \(see [Section 23.1.5](https://www.postgresql.org/docs/9.1/static/routine-vacuuming.html#AUTOVACUUM)\) takes care of automatic analyzing of tables when they are first loaded with data, and as they change throughout regular operation. When autovacuum is disabled, it is a good idea to run ANALYZE periodically, or just after making major changes in the contents of a table. Accurate statistics will help the planner to choose the most appropriate query plan, and thereby improve the speed of query processing. A common strategy is to run [VACUUM](https://www.postgresql.org/docs/9.1/static/sql-vacuum.html) and ANALYZEonce a day during a low-usage time of day.

ANALYZE requires only a read lock on the target table, so it can run in parallel with other activity on the table.

The statistics collected by ANALYZE usually include a list of some of the most common values in each column and a histogram showing the approximate data distribution in each column. One or both of these can be omitted if ANALYZE deems them uninteresting \(for example, in a unique-key column, there are no common values\) or if the column data type does not support the appropriate operators. There is more information about the statistics in [Chapter 23](https://www.postgresql.org/docs/9.1/static/maintenance.html).

For large tables, ANALYZE takes a random sample of the table contents, rather than examining every row. This allows even very large tables to be analyzed in a small amount of time. Note, however, that the statistics are only approximate, and will change slightly each time ANALYZE is run, even if the actual table contents did not change. This might result in small changes in the planner's estimated costs shown by [EXPLAIN](https://www.postgresql.org/docs/9.1/static/sql-explain.html). In rare situations, this non-determinism will cause the planner's choices of query plans to change after ANALYZE is run. To avoid this, raise the amount of statistics collected by ANALYZE, as described below.

The extent of analysis can be controlled by adjusting the [default\_statistics\_target](https://www.postgresql.org/docs/9.1/static/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET) configuration variable, or on a column-by-column basis by setting the per-column statistics target with ALTER TABLE ... ALTER COLUMN ... SET STATISTICS \(see [ALTER TABLE](https://www.postgresql.org/docs/9.1/static/sql-altertable.html)\). The target value sets the maximum number of entries in the most-common-value list and the maximum number of bins in the histogram. The default target value is 100, but this can be adjusted up or down to trade off accuracy of planner estimates against the time taken for ANALYZEand the amount of space occupied in pg\_statistic. In particular, setting the statistics target to zero disables collection of statistics for that column. It might be useful to do that for columns that are never used as part of the WHERE, GROUP BY, or ORDER BY clauses of queries, since the planner will have no use for statistics on such columns.

The largest statistics target among the columns being analyzed determines the number of table rows sampled to prepare the statistics. Increasing the target causes a proportional increase in the time and space needed to do ANALYZE.

One of the values estimated by ANALYZE is the number of distinct values that appear in each column. Because only a subset of the rows are examined, this estimate can sometimes be quite inaccurate, even with the largest possible statistics target. If this inaccuracy leads to bad query plans, a more accurate value can be determined manually and then installed with ALTER TABLE ... ALTER COLUMN ... SET \(n\_distinct = ...\) \(see [ALTER TABLE](https://www.postgresql.org/docs/9.1/static/sql-altertable.html)\).

If the table being analyzed has one or more children, ANALYZE will gather statistics twice: once on the rows of the parent table only, and a second time on the rows of the parent table with all of its children. The autovacuum daemon, however, will only consider inserts or updates on the parent table when deciding whether to trigger an automatic analyze. If that table is rarely inserted into or updated, the inheritance statistics will not be up to date unless you run ANALYZE manually.

### Compatibility

There is no ANALYZE statement in the SQL standard.

### See Also

[VACUUM](https://www.postgresql.org/docs/9.1/static/sql-vacuum.html), [vacuumdb](https://www.postgresql.org/docs/9.1/static/app-vacuumdb.html), [Section 18.4.3](https://www.postgresql.org/docs/9.1/static/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-VACUUM-COST), [Section 23.1.5](https://www.postgresql.org/docs/9.1/static/routine-vacuuming.html#AUTOVACUUM)

