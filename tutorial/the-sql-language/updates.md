# 2.8. 更新資料

你可以使用 UPDATE 指令以列為單位來更新資料。假設你發現氣溫的數值測量在 11 月 28 日之後都多了 2 度。你可以以下列語法來修正這些資料：

```
UPDATE weather
    SET temp_hi = temp_hi - 2,  temp_lo = temp_lo - 2
    WHERE date > '1994-11-28';
```

查看一下這些更新後的資料：

```
SELECT * FROM weather;

     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      41 |      55 |    0 | 1994-11-29
 Hayward       |      35 |      52 |      | 1994-11-29
(3 rows)
```
