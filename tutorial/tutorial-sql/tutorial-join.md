<a id="TUTORIAL-JOIN"></a>

## 2.6. 資料表之間的聯結（JOIN） [#](#TUTORIAL-JOIN)

<a id="id-1.4.4.7.2"></a>

到目前為止，我們的查詢一次都只存取一個資料表。查詢可以同時存取多個資料表，或以同時處理同一資料表中多筆資料列的方式來存取該資料表。同時存取多個資料表（或同一資料表的多個實例）的查詢稱為*聯結*（join）查詢。聯結查詢會把一個資料表的資料列與第二個資料表的資料列組合起來，並以一個運算式指定哪些資料列要配對。例如，要回傳所有天氣記錄以及對應城市的位置，資料庫需要將 `weather` 資料表每一筆資料列的 `city` 欄位，與 `cities` 資料表所有資料列的 `name` 欄位相比較，並選出這些值相符的資料列配對。[<a id="id-1.4.4.7.3.6"></a>[4]](#ftn.id-1.4.4.7.3.6)
這可以透過下列查詢完成：

```

SELECT * FROM weather JOIN cities ON city = name;
```

```

     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(2 rows)
```

請留意結果集合的兩個地方：

* 結果中沒有 Hayward 這個城市的資料列。這是因為 `cities` 資料表中沒有與 Hayward 相符的項目，所以聯結會忽略 `weather` 資料表中沒有相符項目的資料列。我們稍後會說明如何解決這個問題。
* 有兩個欄位包含城市名稱。這是正確的，因為 `weather` 與 `cities` 資料表的欄位清單會串接在一起。不過實務上這並不理想，所以你大概會想明確列出輸出欄位，而不是使用 `*`：

  ```

  SELECT city, temp_lo, temp_hi, prcp, date, location
      FROM weather JOIN cities ON city = name;
  ```

由於這些欄位的名稱都不相同，剖析器會自動找出它們各自屬於哪個資料表。如果兩個資料表中有重複的欄位名稱，你就需要*限定*（qualify）欄位名稱，以表明你指的是哪一個，例如：

```

SELECT weather.city, weather.temp_lo, weather.temp_hi,
       weather.prcp, weather.date, cities.location
    FROM weather JOIN cities ON weather.city = cities.name;
```

一般認為，在聯結查詢中限定所有欄位名稱是良好的寫法，這樣日後即使某個資料表加入了名稱重複的欄位，查詢也不會失敗。

目前看到的這類聯結查詢，也可以寫成下列形式：

```

SELECT *
    FROM weather, cities
    WHERE city = name;
```

這種語法早於 SQL-92 引入的 `JOIN`/`ON` 語法。它只是把資料表列在 `FROM` 子句中，並將比較運算式加到 `WHERE` 子句裡。這種較舊的隱含語法，與較新的明確 `JOIN`/`ON` 語法所得到的結果完全相同。但對閱讀查詢的人來說，明確語法比較容易理解查詢的意思：聯結條件由專屬的關鍵字引入，而舊語法則是把條件與其他條件一起混在 `WHERE` 子句中。

<a id="id-1.4.4.7.7"></a>

現在我們來看看如何把 Hayward 的記錄找回來。我們希望查詢掃描 `weather` 資料表，並為每一筆資料列找出相符的 `cities` 資料列。如果找不到相符的資料列，我們希望以某種「空值」代替 `cities` 資料表的欄位。這種查詢稱為*外部聯結*（outer join）。（目前為止我們看到的聯結都是*內部聯結*（inner join）。）指令如下：

```

SELECT *
    FROM weather LEFT OUTER JOIN cities ON weather.city = cities.name;
```

```

     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 Hayward       |      37 |      54 |      | 1994-11-29 |               |
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(3 rows)
```

這個查詢稱為*左外部聯結*（left outer join），因為在聯結運算子左側的資料表，其每一筆資料列都至少會在輸出中出現一次；而右側的資料表只會輸出與左側資料表某筆資料列相符的那些資料列。當輸出的左側資料表資料列在右側資料表中沒有相符項目時，右側資料表的欄位會以空值（null）代替。

**練習：**
另外還有右外部聯結與完整外部聯結。試著找出它們的作用。

<a id="id-1.4.4.7.10"></a><a id="id-1.4.4.7.11"></a>

我們也可以將資料表與自己聯結，這稱為*自我聯結*（self join）。舉例來說，假設我們想找出所有溫度範圍落在其他天氣記錄溫度範圍之內的天氣記錄。因此我們需要將每一筆 `weather` 資料列的 `temp_lo` 與 `temp_hi` 欄位，與其他所有 `weather` 資料列的 `temp_lo` 與 `temp_hi` 欄位相比較。我們可以用下列查詢做到：

```

SELECT w1.city, w1.temp_lo AS low, w1.temp_hi AS high,
       w2.city, w2.temp_lo AS low, w2.temp_hi AS high
    FROM weather w1 JOIN weather w2
        ON w1.temp_lo < w2.temp_lo AND w1.temp_hi > w2.temp_hi;
```

```

     city      | low | high |     city      | low | high
---------------+-----+------+---------------+-----+------
 San Francisco |  43 |   57 | San Francisco |  46 |   50
 Hayward       |  37 |   54 | San Francisco |  46 |   50
(2 rows)
```

這裡我們把 weather 資料表重新標記為 `w1` 與 `w2`，以便區分聯結的左側與右側。你也可以在其他查詢中使用這類別名來節省輸入，例如：

```

SELECT *
    FROM weather w JOIN cities c ON w.city = c.name;
```

你會很常遇到這種縮寫方式。

<br>

---

<a id="ftn.id-1.4.4.7.3.6"></a>

[[4]](#id-1.4.4.7.3.6) 
這只是概念上的模型。實際執行聯結時，通常會採用比逐一比較每一種可能的資料列配對更有效率的方式，但這對使用者而言是不可見的。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-join.html)（原文版本：18.6；核對日期：2026-09-11）
