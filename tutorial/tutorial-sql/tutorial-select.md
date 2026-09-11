<a id="TUTORIAL-SELECT"></a>

## 2.5. 查詢資料表 [#](#TUTORIAL-SELECT)

<a id="id-1.4.4.6.2.1"></a>
<a id="id-1.4.4.6.2.2"></a>
要從資料表取出資料，就要*查詢*該資料表。這項工作使用 SQL 的 `SELECT` 陳述式來完成。這個陳述式分成選取清單（列出要回傳哪些欄位的部分）、資料表清單（列出要從哪些資料表取出資料的部分），以及選用的限定條件（指定任何限制的部分）。舉例來說，要取出資料表 `weather` 的所有資料列，請輸入：

```

SELECT * FROM weather;
```

這裡的 `*` 是「所有欄位」的簡寫。
[<a id="id-1.4.4.6.2.10"></a>[2]](#ftn.id-1.4.4.6.2.10)
因此，下列查詢也會得到相同的結果：

```

SELECT city, temp_lo, temp_hi, prcp, date FROM weather;
```

輸出應該是：

```

     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      43 |      57 |    0 | 1994-11-29
 Hayward       |      37 |      54 |      | 1994-11-29
(3 rows)
```

選取清單中不只能寫單純的欄位參照，也可以寫運算式。例如，你可以這樣做：

```

SELECT city, (temp_hi+temp_lo)/2 AS temp_avg, date FROM weather;
```

這應該會得到：

```

     city      | temp_avg |    date
---------------+----------+------------
 San Francisco |       48 | 1994-11-27
 San Francisco |       50 | 1994-11-29
 Hayward       |       45 | 1994-11-29
(3 rows)
```

請注意這裡如何使用 `AS` 子句為輸出欄位重新命名。（`AS` 子句可以省略。）

查詢可以加上 `WHERE` 子句來「限定」要取得哪些資料列。`WHERE` 子句包含一個布林（真值）運算式，只有布林運算式為真的資料列才會被回傳。限定條件中可以使用一般的布林運算子（`AND`、`OR` 與 `NOT`）。例如，下列查詢會取出舊金山下雨日子的天氣：

```

SELECT * FROM weather
    WHERE city = 'San Francisco' AND prcp > 0.0;
```

結果：

```

     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
(1 row)
```

<a id="id-1.4.4.6.5.1"></a>
你可以要求查詢結果依排序後的順序回傳：

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

在這個例子中，排序順序並沒有完全指定，因此舊金山的兩筆資料列可能以任一順序出現。但如果你這樣寫，就一定會得到上面所示的結果：

```

SELECT * FROM weather
    ORDER BY city, temp_lo;
```

<a id="id-1.4.4.6.6.1"></a>
<a id="id-1.4.4.6.6.2"></a>
你可以要求從查詢結果中移除重複的資料列：

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

同樣地，結果資料列的順序可能會有所不同。你可以同時使用 `DISTINCT` 與 `ORDER BY` 來確保結果一致：
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
雖然 `SELECT *` 對臨時查詢很方便，但在正式環境的程式碼中，一般認為這是不好的寫法，因為在資料表中新增欄位就會改變查詢結果。

<a id="ftn.id-1.4.4.6.6.7"></a>

[[3]](#id-1.4.4.6.6.7) 
在某些資料庫系統中（包括舊版的 PostgreSQL），`DISTINCT` 的實作會自動將資料列排序，因此不需要 `ORDER BY`。但 SQL 標準並未要求這一點，而且目前的 PostgreSQL 並不保證 `DISTINCT` 會讓資料列依序排列。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-select.html)（原文版本：18.6；核對日期：2026-09-11）
