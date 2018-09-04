# CREATE STATISTICS

CREATE STATISTICS — define extended statistics

### Synopsis

```text
CREATE STATISTICS [ IF NOT EXISTS ] statistics_name
    [ ( statistics_kind [, ... ] ) ]
    ON column_name, column_name [, ...]
    FROM table_name
```

### Description

`CREATE STATISTICS` will create a new extended statistics object tracking data about the specified table, foreign table or materialized view. The statistics object will be created in the current database and will be owned by the user issuing the command.

If a schema name is given \(for example, `CREATE STATISTICS myschema.mystat ...`\) then the statistics object is created in the specified schema. Otherwise it is created in the current schema. The name of the statistics object must be distinct from the name of any other statistics object in the same schema.

### Parameters

`IF NOT EXISTS`

Do not throw an error if a statistics object with the same name already exists. A notice is issued in this case. Note that only the name of the statistics object is considered here, not the details of its definition.

_`statistics_name`_

The name \(optionally schema-qualified\) of the statistics object to be created.

_`statistics_kind`_

A statistics kind to be computed in this statistics object. Currently supported kinds are `ndistinct`, which enables n-distinct statistics, and `dependencies`, which enables functional dependency statistics. If this clause is omitted, all supported statistics kinds are included in the statistics object. For more information, see [Section 14.2.2](https://www.postgresql.org/docs/10/static/planner-stats.html#PLANNER-STATS-EXTENDED) and [Section 68.2](https://www.postgresql.org/docs/10/static/multivariate-statistics-examples.html).

_`column_name`_

The name of a table column to be covered by the computed statistics. At least two column names must be given.

_`table_name`_

The name \(optionally schema-qualified\) of the table containing the column\(s\) the statistics are computed on.

### Notes

You must be the owner of a table to create a statistics object reading it. Once created, however, the ownership of the statistics object is independent of the underlying table\(s\).

### Examples

Create table `t1` with two functionally dependent columns, i.e. knowledge of a value in the first column is sufficient for determining the value in the other column. Then functional dependency statistics are built on those columns:

```text
CREATE TABLE t1 (
    a   int,
    b   int
);

INSERT INTO t1 SELECT i/100, i/500
                 FROM generate_series(1,1000000) s(i);

ANALYZE t1;

-- the number of matching rows will be drastically underestimated:
EXPLAIN ANALYZE SELECT * FROM t1 WHERE (a = 1) AND (b = 0);

CREATE STATISTICS s1 (dependencies) ON a, b FROM t1;

ANALYZE t1;

-- now the row count estimate is more accurate:
EXPLAIN ANALYZE SELECT * FROM t1 WHERE (a = 1) AND (b = 0);
```

Without functional-dependency statistics, the planner would assume that the two `WHERE` conditions are independent, and would multiply their selectivities together to arrive at a much-too-small row count estimate. With such statistics, the planner recognizes that the `WHERE` conditions are redundant and does not underestimate the rowcount.

### Compatibility

There is no `CREATE STATISTICS` command in the SQL standard.

### See Also

[ALTER STATISTICS](https://www.postgresql.org/docs/10/static/sql-alterstatistics.html), [DROP STATISTICS](https://www.postgresql.org/docs/10/static/sql-dropstatistics.html)

