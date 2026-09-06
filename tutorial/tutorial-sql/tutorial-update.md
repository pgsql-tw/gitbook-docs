## 2.8. Updates [#](#TUTORIAL-UPDATE)

<a id="id-1.4.4.9.2"></a>

You can update existing rows using the
`UPDATE` command.
Suppose you discover the temperature readings are
all off by 2 degrees after November 28. You can correct the
data as follows:

```

UPDATE weather
    SET temp_hi = temp_hi - 2,  temp_lo = temp_lo - 2
    WHERE date > '1994-11-28';
```

Look at the new state of the data:

```

SELECT * FROM weather;

     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      41 |      55 |    0 | 1994-11-29
 Hayward       |      35 |      52 |      | 1994-11-29
(3 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-update.html)（英文原文，待翻譯）
