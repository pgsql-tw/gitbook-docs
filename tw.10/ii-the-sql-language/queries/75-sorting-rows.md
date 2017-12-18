# 7.5. 資料排序[^1]

在查詢產生了一個輸出資料表（處理了資料列表之後）之後，可以對其資料列進行排序。如果未選擇排序，則資料列將以未指定的順序回傳。在這種情況下的實際順序將取決於資料掃描和交叉查詢類型以及磁碟上的順序，但不能依賴它。只有明確選擇了排序方式，才能保證特定的輸出排序。

以 ORDER BY 子句指定排序順序：

```
SELECT select_list
    FROM table_expression
    ORDER BY sort_expression1 [ASC | DESC] [NULLS { FIRST | LAST }]
             [, sort_expression2 [ASC | DESC] [NULLS { FIRST | LAST }] ...]
```

排序表示式可以在查詢的資料列表中有效的任何表示式。 一個例子是：

```
SELECT a, b FROM table1 ORDER BY a + b, c;
```

當指定多個表示式時，後面的表示式用於前面表示式都相同的資料進行排序。每個表示式可以跟隨一個選擇性的 ASC 或 DESC 關鍵字來設定排序方向為升冪或降冪。 ASC 排序是預設的選項。升冪首先放置較小的值，其中「較小」是根據「&lt;」運算元定義的。 同樣，降冪也是由「&gt;」運算元決定的。[^2]

NULLS FIRST 和 NULLS LAST 選項可用於確定在排序順序中是否出現空值出現在非空值之前或之後。預設情況下，空值排序大於任何非空值；也就是 NULLS FIRST 是 DESC 選項的預設值，否則就是 NULLS LAST。

請注意，排序選項是針對每個排序欄位獨立考慮的。例如 ORDER BY x, y DESC 是指 ORDER BY x ASC, y DESC，它與 ORDER BY x DESC, y DESC 不同。

排序表示式也可以是輸出欄位的欄位標籤或編號，如下所示：

```
SELECT a + b AS sum, c FROM table1 ORDER BY sum;
SELECT a, max(b) FROM table1 GROUP BY a ORDER BY 1;
```

兩者都按第一個輸出欄位排序。請注意，輸出欄位名稱必須獨立，也就是說，不能在表示式中使用 - 例如，這樣是不正確的：

```
SELECT a + b AS sum, c FROM table1 ORDER BY sum + c;          -- 錯誤
```

這種限制是為了減少歧義。 即使 ORDER BY 項目是一個簡單的名字，可以匹配輸出欄位名稱或者資料表表示式中的一項，這仍然是會混淆的。在這種情況下請使用輸出欄位。如果您使用 AS 來重新命名輸出欄位以匹配其他資料表欄位的名稱，只會導致混淆。

可以將 ORDER BY 應用於 UNION、INTERSECT 或 EXCEPT 組合的結果，但在這種情況下，只允許按輸出欄位名稱或數字進行排序，而不能使用表示式進行排序。

---

[^1]: [PostgreSQL: Documentation: 10: 7.5. Sorting Rows](https://www.postgresql.org/docs/10/static/queries-order.html)

[^2]: 實際上，PostgreSQL 為表示式的資料型別使用預設的 B-tree 運算來確定 ASC 和 DESC 的排序順序。 通常，資料型別將被設定使得 &lt; 和 &gt; 運算元對應於這種排序，但是用戶定義的資料型別的設計者可以選擇做不同的對應。

