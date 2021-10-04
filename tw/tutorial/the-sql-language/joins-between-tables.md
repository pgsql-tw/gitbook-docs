# 2.6. 交叉查詢

到目前為止，我們的一個查詢都只涉及到一個資料表。其實可以在同一個查詢中，同時查詢多個資料表，或者在同一個資料表之中同時處理多個資料列的資料。在一個查詢之中，涉及到同一個或多個不同的資料表中的資料，稱作為交叉查詢（join）。舉個例子來說，你希望同時列出天氣和城市位置的資料。要完成這項工作，我們需要關連資料表 weather 中的 city 欄位與表格 cities 中的 name 欄位，然後回傳符合條件的資料。

## 注意

> 這只是一個概念式的模形，交叉查詢（join）會以更有效率的方式運行，並非真正需要比較每一種組合是否符合條件，不過這些過程對於使用者而言並不會產生操作或結果上的差異。

下列查詢會產生交叉查詢的結果：

```text
SELECT *
    FROM weather, cities
    WHERE city = name;
```

```text
     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(2 rows)
```

在這個結果中可以觀察到兩件事情：

* 不會有關於 Hayward 的結果出現。這是因為在資料表 cities 中未有 Hayward 的資料，所以交叉查詢會忽略資料表 weather 中未能關連的資料。關於這點，我們很快就會有解決辦法。
* 有兩個欄位顯示了城市的名稱。這樣是正確的，因為來自於資料表 weather 和 cities 的欄位被串連起來了。實務上，這樣的結果並不令人滿意，所以也許你可以明確地指出輸出的欄位，取代「 \* 」的使用：

```text
SELECT city, temp_lo, temp_hi, prcp, date, location
    FROM weather, cities
    WHERE city = name;
```

**練習：**試試看，當 WHERE 表示式被省略的話，查詢語句的意義會怎麼樣？

因為所有的欄位都使用不同的名稱，所以解譯器會自動發現他們所屬的資料表為何。如果在兩個資料表之中，存在有相同名稱的欄位時，你最好明確指出確定的欄位，如下所示：

```text
SELECT weather.city, weather.temp_lo, weather.temp_hi,
       weather.prcp, weather.date, cities.location
    FROM weather, cities
    WHERE cities.name = weather.city;
```

多數開發者認為，在交叉查詢中，明確指出確定的欄位名稱，是良好的撰寫習慣。這樣查詢就不會因為有相同的欄位名稱而產生錯誤。而相同名稱的欄位可能是開發後續才加入的，未指明的話，就可能造成意外的結果。

交叉查詢也可以寫成如下的另一種形式：

```text
SELECT *
    FROM weather INNER JOIN cities ON (weather.city = cities.name);
```

這種語法並不如上述的常見，但我們會在這裡說明，以幫助你在後續章節的學習。

現在我們要回到前面的問題，把 Hayward 的資料放在輸出的結果之中。我們要在查詢中做的是，掃描資料表 weather，找到有所關連的每一列資料；沒有關連到的資料列，我們要填上「空值」（null）在資料表 cities 相對的欄位之中。這樣的查詢我們稱作「外部交叉查詢」（outer join）。（先前的交叉查詢為「內部交叉查詢」（inner join））。這樣的查詢指令如下所示：



```text
SELECT *
    FROM weather LEFT OUTER JOIN cities ON (weather.city = cities.name);
```

```text
     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 Hayward       |      37 |      54 |      | 1994-11-29 |               |
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(3 rows)
```

這種查詢稱作為「左側外部查詢」（left outer join），因為這個交叉查詢，放在左側的資料表中的資料列，一定會在結果中至少出現一次，而右側的資料表中，則只有輸出有關連到左側資料表的資料列。當左側資料表的資料列，並沒有在右側資料表中被關連到時，屬於右側資料表的欄位就會被填上空值輸出。

**練習：**也有「右側外部交叉查詢」（right outer join）和「完全外部交叉查詢」（full outer join），試著找出他們都做了些什麼。

我們也可以對同一個資料表做交叉查詢，稱作為「自我交叉查詢」（self join）。接下來的範例，假設我們希望找到所有氣溫範圍的天氣資料。所以我們需要讓 temp\_lo 及 temp\_hi 兩個欄位，和其他的 temp\_lo 及 temp\_high 相比較。我們可以用下列的查詢來符合需求：



```text
SELECT W1.city, W1.temp_lo AS low, W1.temp_hi AS high,
    W2.city, W2.temp_lo AS low, W2.temp_hi AS high
    FROM weather W1, weather W2
    WHERE W1.temp_lo < W2.temp_lo
    AND W1.temp_hi > W2.temp_hi;
```

```text
     city      | low | high |     city      | low | high
---------------+-----+------+---------------+-----+------
 San Francisco |  43 |   57 | San Francisco |  46 |   50
 Hayward       |  37 |   54 | San Francisco |  46 |   50
(2 rows)
```

這裡我們重新命名了資料表 weather 為 W1 及 W2，以在交叉查詢中區分左側及右側。你也可以在其他查詢中使用這個技巧，以節省輸入的複雜度，例如：

```text
SELECT *
    FROM weather w, cities c
    WHERE w.city = c.name;
```

你將會在後續內容中，不斷練習到這樣的使用方式。

