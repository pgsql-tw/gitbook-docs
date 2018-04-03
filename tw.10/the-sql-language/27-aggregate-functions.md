# 2.7. 彙總查詢[^1]

如同其他的關連式資料庫產品，PostgreSQL 也支援彙總查詢的功能。彙總查詢指的是能夠把多個列的資料經過計算，產生單一結果的功能。舉例來說， count、sum、avg（平均值）、max（最大值）、min（最小值）都是彙總查詢的函式。

這裡的例子，我們可以得到所有低溫中的最大值：

```
SELECT max(temp_lo) FROM weather;
```

```
 max
-----
  46
(1 row)
```

如果我們想要知道，這個數值是發生在哪一個城市？也許可以試試：

```
SELECT city FROM weather WHERE temp_lo = max(temp_lo);     
WRONG
```

不過，這行不通，因為 max 不能使用在 WHERE 條件式當中。（會有這樣的限制，是因為 WHERE 條件式目的是要判斷有哪些列的資料應該被彙總計算，所以很明顯地，這件事必須要在彙整計算前發生，這就產生了矛盾。）所以，像本例的查詢一般會使用子查詢（subquery）來取得適當的結果：

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

這樣就對了，因為子查詢是一個獨立的查詢，它可以獨立進行彙總查詢，有別於括號以外的查詢語句。

彙總查詢和 GROUP BY 一起使用會很方便的。舉例來說，我們可以得到每個城市所觀測到的最高氣溫：

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

這個查詢對每個城市都輸出一列的結果。每一個彙總的結果，將整個資料表，以關連到的城市進行計算。  
而我們可以進一步過濾資料內容，使用 HAVING：

```
SELECT city, max(temp_lo)
    FROM weather
    GROUP BY city
    HAVING max(temp_lo) < 40;
```

```
  city   | max
---------+-----
 Hayward |  37
(1 row)
```

如果限制所有 temp\_lo 的數值必須要小於 40 （WHERE temp\_lo &lt; 40）的話，也可能得到相同的結果。  
最後，如果我們只關心以＂S＂開頭的城市的話，可以這樣做：

```
SELECT city, max(temp_lo)
    FROM weather
    WHERE city LIKE 'S%'            -- (1)
    GROUP BY city
    HAVING max(temp_lo) < 40;
```

1. LIKE 運算子進行特徵比對運算，這將會在 [9.7. 特徵比對](/ii-the-sql-language/functions-and-operators/97-pattern-matching.md)中進一步說明。

這裡很重要的是，瞭解 SQL 中 WHERE 和 HAVING 之間的行為。其根本上的差異是：WHERE 會在合併和彙總計算之前進行選擇資料的動作（也就是它控制著，哪些資料需要被彙總計算）；而 HAVING 是在合併及彙整計算之後，才進行過濾資料的動作。所以，在 WHERE 條件式當中，絕不可以使用彙整運算式；另一方面，HAVING 條件式總是使用彙整運算式。（嚴格來說，你也可以不在 HAVING 條件式中使用彙整運算式，但很少人這樣使用，通常就會改寫到 WHERE 條式件當中，那會更有效率。）

在先前的例子當中，我們可以把城市名稱的限制放在 WHERE 條件式之中，因為它不需要彙總。這將會比放在 HAVING 條件式中更有效率，因為這樣可以避免合併及彙整運算整個表格，不用浪費時間在本來就會被過濾掉的資料上。

---

[^1]: [PostgreSQL: Documentation: 10: 2.7. Aggregate Functions](https://www.postgresql.org/docs/10/static/tutorial-agg.html)

