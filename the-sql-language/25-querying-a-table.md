# 2.5. 表格的查詢[^1]

To retrieve data from a table, the table is_queried_. AnSQL`SELECT`statement is used to do this. The statement is divided into a select list \(the part that lists the columns to be returned\), a table list \(the part that lists the tables from which to retrieve the data\), and an optional qualification \(the part that specifies any restrictions\). For example, to retrieve all the rows of table`weather`, type:

```
SELECT * FROM weather;

```

Here`*`is a shorthand for“all columns”.[\[2\]](https://www.postgresql.org/docs/10/static/tutorial-select.html#ftn.idm46249860326688)So the same result would be had with:

```
SELECT city, temp_lo, temp_hi, prcp, date FROM weather;

```

The output should be:

```
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      43 |      57 |    0 | 1994-11-29
 Hayward       |      37 |      54 |      | 1994-11-29
(3 rows)

```

You can write expressions, not just simple column references, in the select list. For example, you can do:

```
SELECT city, (temp_hi+temp_lo)/2 AS temp_avg, date FROM weather;

```

This should give:

```
     city      | temp_avg |    date
---------------+----------+------------
 San Francisco |       48 | 1994-11-27
 San Francisco |       50 | 1994-11-29
 Hayward       |       45 | 1994-11-29
(3 rows)

```

Notice how the`AS`clause is used to relabel the output column. \(The`AS`clause is optional.\)

A query can be“qualified”by adding a`WHERE`clause that specifies which rows are wanted. The`WHERE`clause contains a Boolean \(truth value\) expression, and only rows for which the Boolean expression is true are returned. The usual Boolean operators \(`AND`,`OR`, and`NOT`\) are allowed in the qualification. For example, the following retrieves the weather of San Francisco on rainy days:

```
SELECT * FROM weather
    WHERE city = 'San Francisco' AND prcp 
>
 0.0;

```

Result:

```
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
(1 row)

```

You can request that the results of a query be returned in sorted order:

```
SELECT * FROM weather
    ORDER BY city;

```

```
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 Hayward       |      37 |      54 |      | 1994-11-29
 San Francisco |      43 |      57 |    0 | 1994-11-29
 San Francisco |      46 |      50 | 0.25 | 1994-11-27

```

In this example, the sort order isn't fully specified, and so you might get the San Francisco rows in either order. But you'd always get the results shown above if you do:

```
SELECT * FROM weather
    ORDER BY city, temp_lo;

```

You can request that duplicate rows be removed from the result of a query:

```
SELECT DISTINCT city
    FROM weather;

```

```
     city
---------------
 Hayward
 San Francisco
(2 rows)

```

Here again, the result row ordering might vary. You can ensure consistent results by using`DISTINCT`and`ORDER BY`together:[\[3\]](https://www.postgresql.org/docs/10/static/tutorial-select.html#ftn.idm46249860306864)

```
SELECT DISTINCT city
    FROM weather
    ORDER BY city;

```

  


---

[\[2\]](https://www.postgresql.org/docs/10/static/tutorial-select.html#idm46249860326688)While`SELECT *`is useful for off-the-cuff queries, it is widely considered bad style in production code, since adding a column to the table would change the results.

[\[3\]](https://www.postgresql.org/docs/10/static/tutorial-select.html#idm46249860306864)In some database systems, including older versions ofPostgreSQL, the implementation of`DISTINCT`automatically orders the rows and so`ORDER BY`is unnecessary. But this is not required by the SQL standard, and currentPostgreSQLdoes not guarantee that`DISTINCT`causes the rows to be ordered.

---



[^1]: [PostgreSQL: Documentation: 10: 2.5. Querying a Table](https://www.postgresql.org/docs/10/static/tutorial-select.html)

