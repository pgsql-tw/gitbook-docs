## 2.5. Querying a Table [#](#TUTORIAL-SELECT)

<a id="id-1.4.4.6.2.1"></a>
<a id="id-1.4.4.6.2.2"></a>
To retrieve data from a table, the table is
*queried*. An SQL
`SELECT` statement is used to do this. The
statement is divided into a select list (the part that lists the
columns to be returned), a table list (the part that lists the
tables from which to retrieve the data), and an optional
qualification (the part that specifies any restrictions). For
example, to retrieve all the rows of table
`weather`, type:

```

SELECT * FROM weather;
```

Here `*` is a shorthand for “all columns”.
[<a id="id-1.4.4.6.2.10"></a>[2]](#ftn.id-1.4.4.6.2.10)
So the same result would be had with:

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

You can write expressions, not just simple column references, in the
select list. For example, you can do:

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

Notice how the `AS` clause is used to relabel the
output column. (The `AS` clause is optional.)

A query can be “qualified” by adding a `WHERE`
clause that specifies which rows are wanted. The `WHERE`
clause contains a Boolean (truth value) expression, and only rows for
which the Boolean expression is true are returned. The usual
Boolean operators (`AND`,
`OR`, and `NOT`) are allowed in
the qualification. For example, the following
retrieves the weather of San Francisco on rainy days:

```

SELECT * FROM weather
    WHERE city = 'San Francisco' AND prcp > 0.0;
```

Result:

```

     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
(1 row)
```

<a id="id-1.4.4.6.5.1"></a>
You can request that the results of a query
be returned in sorted order:

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

In this example, the sort order isn't fully specified, and so you
might get the San Francisco rows in either order. But you'd always
get the results shown above if you do:

```

SELECT * FROM weather
    ORDER BY city, temp_lo;
```

<a id="id-1.4.4.6.6.1"></a>
<a id="id-1.4.4.6.6.2"></a>
You can request that duplicate rows be removed from the result of
a query:

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

Here again, the result row ordering might vary.
You can ensure consistent results by using `DISTINCT` and
`ORDER BY` together:
[<a id="id-1.4.4.6.6.7"></a>[3]](#ftn.id-1.4.4.6.6.7)

```

SELECT DISTINCT city
    FROM weather
    ORDER BY city;
```

<br>

---

<a id="ftn.id-1.4.4.6.2.10"></a>

[[2]](#id-1.4.4.6.2.10) 
While `SELECT *` is useful for off-the-cuff
queries, it is widely considered bad style in production code,
since adding a column to the table would change the results.

<a id="ftn.id-1.4.4.6.6.7"></a>

[[3]](#id-1.4.4.6.6.7) 
In some database systems, including older versions of
PostgreSQL, the implementation of
`DISTINCT` automatically orders the rows and
so `ORDER BY` is unnecessary. But this is not
required by the SQL standard, and current
PostgreSQL does not guarantee that
`DISTINCT` causes the rows to be ordered.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-select.html)（英文原文，待翻譯）
