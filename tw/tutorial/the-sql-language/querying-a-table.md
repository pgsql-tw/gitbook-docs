# 2.5. 資料表的查詢

要從資料表（table）中取出資料，稱作資料表的查詢。要進行這個行為，你需要 SQL 中的 SELECT 指令。這個指令由幾個部份所組成，回傳列表（select list，想要回傳的欄位）、資料表列表（資料來源的資料表）、選擇性的條件定義（指定一些限制條件）。舉個例子來說，要取得資料表 weather 中所有的資料的話，請輸入：

```text
SELECT * FROM weather;
```

這裡的星號 \* 表示「所有欄位」。下列的指令會回傳相同的結果。

```text
SELECT city, temp_lo, temp_hi, prcp, date FROM weather;
```

其輸出結果將會如下所示：

```text
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      43 |      57 |    0 | 1994-11-29
 Hayward       |      37 |      54 |      | 1994-11-29
(3 rows)
```

你可以在回傳列表中撰寫一些運算表示式，而不只是簡單的欄位引用。舉例來說，你可以輸入：

```text
SELECT city, (temp_hi+temp_lo)/2 AS temp_avg, date FROM weather;
```

這應該會產生這樣的結果：

```text
     city      | temp_avg |    date
---------------+----------+------------
 San Francisco |       48 | 1994-11-27
 San Francisco |       50 | 1994-11-29
 Hayward       |       45 | 1994-11-29
(3 rows)
```

注意，「AS」被用來重新命名輸出的欄位。（選用）

查詢語句可以加上「WHERE」來設定限制條件，以指定哪些列才需要被回傳。WHERE 的內容是一個布林（truth value）表示式，而只有在其運算值為真（true）時，該列才會被回傳。一般的布林運算子（AND, OR, NOT）都是被允許出現在表示式中的。舉例來說，下列的指令將會回傳 San Francisco 在雨天的天氣數值：

```text
SELECT * FROM weather
    WHERE city = 'San Francisco' AND prcp > 0.0;
```

結果：

```text
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
(1 row)
```

你可以將結果進行排序：

```text
SELECT * FROM weather
    ORDER BY city;
```

```text
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 Hayward       |      37 |      54 |      | 1994-11-29
 San Francisco |      43 |      57 |    0 | 1994-11-29
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
```

在這個例子之中，其次序並沒有完全地被指定，所以你可能會得到 San Francisco 的列以另一種次序呈現。而你如果以下列指令查詢的話，那你就會得到如上但固定的結果：

```text
SELECT * FROM weather
    ORDER BY city, temp_lo;
```

你可以在查詢時去除重覆的列：

```text
SELECT DISTINCT city
    FROM weather;
```

```text
     city
---------------
 Hayward
 San Francisco
(2 rows)
```

再一次，其結果的次序可能每次都不同，你可以同時使用 DISTINCT 及 ORDER BY 來確保能得到一致性的查詢結果：

```text
SELECT DISTINCT city
    FROM weather
    ORDER BY city;
```

