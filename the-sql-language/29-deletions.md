# 2.9. 刪除資料[^1]

Rows can be removed from a table using the`DELETE`command. Suppose you are no longer interested in the weather of Hayward. Then you can do the following to delete those rows from the table:

```
DELETE FROM weather WHERE city = 'Hayward';

```

All weather records belonging to Hayward are removed.

```
SELECT * FROM weather;

```

```
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      41 |      55 |    0 | 1994-11-29
(2 rows)

```

One should be wary of statements of the form

```
DELETE FROM 
tablename
;

```

Without a qualification,`DELETE`will remove_all_rows from the given table, leaving it empty. The system will not request confirmation before doing this!

---



[^1]: [PostgreSQL: Documentation: 10: 2.9. Deletions](https://www.postgresql.org/docs/10/static/tutorial-delete.html)

