# 2.7. 彙總查詢[^1]

Like most other relational database products,PostgreSQLsupports_aggregate functions_. An aggregate function computes a single result from multiple input rows. For example, there are aggregates to compute the`count`,`sum`,`avg`\(average\),`max`\(maximum\) and`min`\(minimum\) over a set of rows.

As an example, we can find the highest low-temperature reading anywhere with:

```
SELECT max(temp_lo) FROM weather;

```

```
 max
-----
  46
(1 row)

```

If we wanted to know what city \(or cities\) that reading occurred in, we might try:

```
SELECT city FROM weather WHERE temp_lo = max(temp_lo);     
WRONG
```

but this will not work since the aggregate`max`cannot be used in the`WHERE`clause. \(This restriction exists because the`WHERE`clause determines which rows will be included in the aggregate calculation; so obviously it has to be evaluated before aggregate functions are computed.\) However, as is often the case the query can be restated to accomplish the desired result, here by using a_subquery_:

```
SELECT city FROM weather
    WHERE temp_lo = (SELECT max(temp_lo) FROM weather);

```

```
     city
---------------
 San Francisco
(1 row)

```

This is OK because the subquery is an independent computation that computes its own aggregate separately from what is happening in the outer query.

Aggregates are also very useful in combination with`GROUP BY`clauses. For example, we can get the maximum low temperature observed in each city with:

```
SELECT city, max(temp_lo)
    FROM weather
    GROUP BY city;

```

```
     city      | max
---------------+-----
 Hayward       |  37
 San Francisco |  46
(2 rows)

```

which gives us one output row per city. Each aggregate result is computed over the table rows matching that city. We can filter these grouped rows using`HAVING`:

```
SELECT city, max(temp_lo)
    FROM weather
    GROUP BY city
    HAVING max(temp_lo) 
<
 40;

```

```
  city   | max
---------+-----
 Hayward |  37
(1 row)

```

which gives us the same results for only the cities that have all`temp_lo`values below 40. Finally, if we only care about cities whose names begin with“`S`”, we might do:

```
SELECT city, max(temp_lo)
    FROM weather
    WHERE city LIKE 'S%'            -- 
(1)
    GROUP BY city
    HAVING max(temp_lo) 
<
 40;

```

| [\(1\)](https://www.postgresql.org/docs/10/static/tutorial-agg.html#co.tutorial-agg-like) | The`LIKE`operator does pattern matching and is explained in[Section 9.7](https://www.postgresql.org/docs/10/static/functions-matching.html). |
| :--- | :--- |


It is important to understand the interaction between aggregates andSQL's`WHERE`and`HAVING`clauses. The fundamental difference between`WHERE`and`HAVING`is this:`WHERE`selects input rows before groups and aggregates are computed \(thus, it controls which rows go into the aggregate computation\), whereas`HAVING`selects group rows after groups and aggregates are computed. Thus, the`WHERE`clause must not contain aggregate functions; it makes no sense to try to use an aggregate to determine which rows will be inputs to the aggregates. On the other hand, the`HAVING`clause always contains aggregate functions. \(Strictly speaking, you are allowed to write a`HAVING`clause that doesn't use aggregates, but it's seldom useful. The same condition could be used more efficiently at the`WHERE`stage.\)

In the previous example, we can apply the city name restriction in`WHERE`, since it needs no aggregate. This is more efficient than adding the restriction to`HAVING`, because we avoid doing the grouping and aggregate calculations for all rows that fail the`WHERE`check.

---

[^1]: [PostgreSQL: Documentation: 10: 2.7. Aggregate Functions](https://www.postgresql.org/docs/10/static/tutorial-agg.html)

