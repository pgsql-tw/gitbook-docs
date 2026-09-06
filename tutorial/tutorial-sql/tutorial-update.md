## 2.8. 更新 [#](#TUTORIAL-UPDATE)

<a id="id-1.4.4.9.2"></a>

你可以使用 `UPDATE` 命令更新既有資料列。假設你發現 11 月 28 日之後的溫度讀數都偏差了 2 度，可以如下修正資料：

```

UPDATE weather
    SET temp_hi = temp_hi - 2,  temp_lo = temp_lo - 2
    WHERE date > '1994-11-28';
```

查看更新後的資料狀態：

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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-update.html)（原文版本：18.6；核對日期：2026-09-07）
