# 2.6. 交叉查詢[^1]

Thus far, our queries have only accessed one table at a time. Queries can access multiple tables at once, or access the same table in such a way that multiple rows of the table are being processed at the same time. A query that accesses multiple rows of the same or different tables at one time is called a_join_query. As an example, say you wish to list all the weather records together with the location of the associated city. To do that, we need to compare the`city`column of each row of the`weather`table with the`name`column of all rows in the`cities`table, and select the pairs of rows where these values match.

### Note

This is only a conceptual model. The join is usually performed in a more efficient manner than actually comparing each possible pair of rows, but this is invisible to the user.

This would be accomplished by the following query:

```
SELECT *
    FROM weather, cities
    WHERE city = name;

```

```
     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(2 rows)

```

Observe two things about the result set:

* There is no result row for the city of Hayward. This is because there is no matching entry in the`cities`table for Hayward, so the join ignores the unmatched rows in the`weather`table. We will see shortly how this can be fixed.

* There are two columns containing the city name. This is correct because the lists of columns from the`weather`and`cities`tables are concatenated. In practice this is undesirable, though, so you will probably want to list the output columns explicitly rather than using`*`:

  ```
  SELECT city, temp_lo, temp_hi, prcp, date, location
      FROM weather, cities
      WHERE city = name;

  ```

**Exercise: **Attempt to determine the semantics of this query when the`WHERE`clause is omitted.

Since the columns all had different names, the parser automatically found which table they belong to. If there were duplicate column names in the two tables you'd need to_qualify_the column names to show which one you meant, as in:

```
SELECT weather.city, weather.temp_lo, weather.temp_hi,
       weather.prcp, weather.date, cities.location
    FROM weather, cities
    WHERE cities.name = weather.city;

```

It is widely considered good style to qualify all column names in a join query, so that the query won't fail if a duplicate column name is later added to one of the tables.

Join queries of the kind seen thus far can also be written in this alternative form:

```
SELECT *
    FROM weather INNER JOIN cities ON (weather.city = cities.name);

```

This syntax is not as commonly used as the one above, but we show it here to help you understand the following topics.

Now we will figure out how we can get the Hayward records back in. What we want the query to do is to scan the`weather`table and for each row to find the matching`cities`row\(s\). If no matching row is found we want some“empty values”to be substituted for the`cities`table's columns. This kind of query is called an_outer join_. \(The joins we have seen so far are inner joins.\) The command looks like this:

```
SELECT *
    FROM weather LEFT OUTER JOIN cities ON (weather.city = cities.name);

     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 Hayward       |      37 |      54 |      | 1994-11-29 |               |
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(3 rows)

```

This query is called a_left outer join_because the table mentioned on the left of the join operator will have each of its rows in the output at least once, whereas the table on the right will only have those rows output that match some row of the left table. When outputting a left-table row for which there is no right-table match, empty \(null\) values are substituted for the right-table columns.

**Exercise: **There are also right outer joins and full outer joins. Try to find out what those do.

We can also join a table against itself. This is called a_self join_. As an example, suppose we wish to find all the weather records that are in the temperature range of other weather records. So we need to compare the`temp_lo`and`temp_hi`columns of each`weather`row to the`temp_lo`and`temp_hi`columns of all other`weather`rows. We can do this with the following query:

```
SELECT W1.city, W1.temp_lo AS low, W1.temp_hi AS high,
    W2.city, W2.temp_lo AS low, W2.temp_hi AS high
    FROM weather W1, weather W2
    WHERE W1.temp_lo 
<
 W2.temp_lo
    AND W1.temp_hi 
>
 W2.temp_hi;

     city      | low | high |     city      | low | high
---------------+-----+------+---------------+-----+------
 San Francisco |  43 |   57 | San Francisco |  46 |   50
 Hayward       |  37 |   54 | San Francisco |  46 |   50
(2 rows)

```

Here we have relabeled the weather table as`W1`and`W2`to be able to distinguish the left and right side of the join. You can also use these kinds of aliases in other queries to save some typing, e.g.:

```
SELECT *
    FROM weather w, cities c
    WHERE w.city = c.name;

```

You will encounter this style of abbreviating quite frequently.

---

[^1]: [PostgreSQL: Documentation: 10: 2.6. Joins Between Tables](https://www.postgresql.org/docs/10/static/tutorial-join.html)

