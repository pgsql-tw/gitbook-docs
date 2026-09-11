<a id="QUERIES-UNION"></a>

## 7.4. 組合查詢（`UNION`、`INTERSECT`、`EXCEPT`） [#](#QUERIES-UNION)

<a id="id-1.5.6.8.2"></a><a id="id-1.5.6.8.3"></a><a id="id-1.5.6.8.4"></a><a id="id-1.5.6.8.5"></a><a id="id-1.5.6.8.6"></a><a id="id-1.5.6.8.7"></a><a id="id-1.5.6.8.8"></a>

兩個查詢的結果可以使用聯集、交集與差集等集合運算組合起來。語法是

```

query1 UNION [ALL] query2
query1 INTERSECT [ALL] query2
query1 EXCEPT [ALL] query2
```

其中 *`query1`* 與 *`query2`* 是可以使用到目前為止所討論之任何功能的查詢。

`UNION` 實際上是將 *`query2`* 的結果附加到 *`query1`* 的結果之後（但並不保證資料列實際上是以這個順序回傳的）。此外，除非使用 `UNION ALL`，否則它會以與 `DISTINCT` 相同的方式，從結果中排除重複的資料列。

`INTERSECT` 會回傳同時出現在 *`query1`* 結果與 *`query2`* 結果中的所有資料列。除非使用 `INTERSECT ALL`，否則會排除重複的資料列。

`EXCEPT` 會回傳出現在 *`query1`* 結果中、但不在 *`query2`* 結果中的所有資料列。（這有時稱為兩個查詢的*差集*（difference）。）同樣地，除非使用 `EXCEPT ALL`，否則會排除重複的資料列。

要計算兩個查詢的聯集、交集或差集，這兩個查詢必須是「聯集相容」（union compatible）的，也就是說，它們回傳相同數量的欄位，而且對應的欄位具有相容的資料型別，如[第 10.5 節](../typeconv/typeconv-union-case.md)所述。

集合運算可以組合使用，例如

```

query1 UNION query2 EXCEPT query3
```

這等同於

```

(query1 UNION query2) EXCEPT query3
```

如這裡所示，你可以使用括號來控制求值的順序。沒有括號時，`UNION` 與 `EXCEPT` 是由左至右結合的，但 `INTERSECT` 的結合力比這兩個運算子強。因此

```

query1 UNION query2 INTERSECT query3
```

的意思是

```

query1 UNION (query2 INTERSECT query3)
```

你也可以用括號括住個別的 *`query`*。如果 *`query`* 需要使用後續各節所討論的任何子句（例如 `LIMIT`），這一點就很重要。沒有括號的話，你會得到語法錯誤，否則該子句會被理解為套用在集合運算的輸出上，而不是其中一個輸入上。例如，

```

SELECT a FROM b UNION SELECT x FROM y LIMIT 10
```

是可以接受的，但它的意思是

```

(SELECT a FROM b UNION SELECT x FROM y) LIMIT 10
```

而不是

```

SELECT a FROM b UNION (SELECT x FROM y LIMIT 10)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries-union.html)（原文版本：18.6；核對日期：2026-09-11）
