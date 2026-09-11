<a id="TUTORIAL-AGG"></a>

## 2.7. 彙總函式 [#](#TUTORIAL-AGG)

<a id="id-1.4.4.8.2"></a>

與大多數其他關聯式資料庫產品一樣，PostgreSQL 支援*彙總函式*（aggregate function）。彙總函式會從多筆輸入資料列計算出單一結果。例如，有些彙總函式可以對一組資料列計算 `count`（筆數）、`sum`（總和）、`avg`（平均值）、`max`（最大值）與 `min`（最小值）。

舉例來說，我們可以用下列查詢找出各地最低溫讀數中的最高值：

```

SELECT max(temp_lo) FROM weather;
```

```

 max
-----
  46
(1 row)
```

<a id="id-1.4.4.8.5.1"></a>
如果我們想知道這個讀數出現在哪個（或哪些）城市，可能會嘗試：

```

SELECT city FROM weather WHERE temp_lo = max(temp_lo);     -- WRONG
```

但這樣行不通，因為彙總函式 `max` 不能用在 `WHERE` 子句中。（之所以有這個限制，是因為 `WHERE` 子句決定哪些資料列會納入彙總計算；因此它顯然必須在計算彙總函式之前先求值。）不過，這類查詢通常可以改寫成另一種形式來達到想要的結果，這裡的做法是使用*子查詢*（subquery）：

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

這樣是可行的，因為子查詢是一個獨立的計算，它會自行計算彙總值，與外層查詢中發生的事情無關。

<a id="id-1.4.4.8.6.1"></a>
<a id="id-1.4.4.8.6.2"></a>
彙總函式與 `GROUP
BY` 子句搭配使用時也非常有用。例如，我們可以用下列查詢取得每個城市的讀數筆數，以及該城市觀測到的最低溫最大值：

```

SELECT city, count(*), max(temp_lo)
    FROM weather
    GROUP BY city;
```

```

     city      | count | max
---------------+-------+-----
 Hayward       |     1 |  37
 San Francisco |     2 |  46
(2 rows)
```

這會為每個城市產生一筆輸出資料列。每個彙總結果都是針對與該城市相符的資料表資料列計算而得。我們可以使用 `HAVING` 篩選這些分組後的資料列：

```

SELECT city, count(*), max(temp_lo)
    FROM weather
    GROUP BY city
    HAVING max(temp_lo) < 40;
```

```

  city   | count | max
---------+-------+-----
 Hayward |     1 |  37
(1 row)
```

這會得到相同的結果，但只包含所有 `temp_lo` 值都低於 40 的城市。最後，如果我們只關心名稱以「`S`」開頭的城市，可以這樣做：

```

SELECT city, count(*), max(temp_lo)
    FROM weather
    WHERE city LIKE 'S%'            -- (1)
    GROUP BY city;
```

```

     city      | count | max
---------------+-------+-----
 San Francisco |     2 |  46
(1 row)
```

<table border="0" summary="Callout list"><tr><td align="left" valign="top" width="5%"><p><a href="#co.tutorial-agg-like">(1)</a> </p></td><td align="left" valign="top"><p>
      <code class="literal">LIKE</code> 運算子用於樣式比對，說明請參閱<a class="xref" href="../../the-sql-language/functions/functions-matching.md">第 9.7 節</a>。
     </p></td></tr></table>

瞭解彙總函式與 SQL 的 `WHERE`、`HAVING` 子句之間如何互動是很重要的。`WHERE` 與 `HAVING` 的根本差異在於：`WHERE` 會在計算分組與彙總之前選取輸入資料列（因此它控制哪些資料列會進入彙總計算），而 `HAVING` 則是在計算分組與彙總之後選取分組資料列。因此，`WHERE` 子句中不可以包含彙總函式；試圖用彙總函式來決定哪些資料列要作為彙總函式的輸入是沒有意義的。另一方面，`HAVING` 子句則一定會包含彙總函式。（嚴格來說，你可以寫出不使用彙總函式的 `HAVING` 子句，但這很少有用處。同樣的條件放在 `WHERE` 階段執行會更有效率。）

在前一個例子中，我們可以在 `WHERE` 中套用城市名稱的限制，因為它不需要彙總。這比把限制加到 `HAVING` 更有效率，因為對於所有未通過 `WHERE` 檢查的資料列，我們都可以省去分組與彙總計算。

另一種選取哪些資料列要進入彙總計算的方式是使用 `FILTER`，這是可以個別套用在每個彙總函式上的選項：

```

SELECT city, count(*) FILTER (WHERE temp_lo < 45), max(temp_lo)
    FROM weather
    GROUP BY city;
```

```

     city      | count | max
---------------+-------+-----
 Hayward       |     1 |  37
 San Francisco |     1 |  46
(2 rows)
```

`FILTER` 與 `WHERE` 很像，差別在於它只會從所附加的那個彙總函式的輸入中移除資料列。在這裡，`count` 彙總函式只計算 `temp_lo` 低於 45 的資料列；但 `max` 彙總函式仍然套用在所有資料列上，所以它依然會找到 46 這個讀數。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-agg.html)（原文版本：18.6；核對日期：2026-09-11）
