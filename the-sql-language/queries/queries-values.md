<a id="QUERIES-VALUES"></a>

## 7.7. `VALUES` 清單 [#](#QUERIES-VALUES)

<a id="id-1.5.6.11.2"></a>

`VALUES` 提供了一種產生「常數資料表」的方式，可以在查詢中使用，而不必實際在磁碟上建立並填入資料表。語法是

```

VALUES ( expression [, ...] ) [, ...]
```

每個以括號括住的運算式清單都會在資料表中產生一筆資料列。所有清單的元素數量都必須相同（也就是資料表的欄位數），而且各清單中對應的項目必須具有相容的資料型別。指派給結果中每個欄位的實際資料型別，是依與 `UNION` 相同的規則決定的（請參閱[第 10.5 節](../typeconv/typeconv-union-case.md)）。

例如：

```

VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

會回傳一個兩個欄位、三筆資料列的資料表。它實際上等同於：

```

SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';
```

預設情況下，PostgreSQL 會將名稱 `column1`、`column2` 等等指派給 `VALUES` 資料表的欄位。SQL 標準並未規定這些欄位名稱，不同的資料庫系統有不同的做法，因此通常最好以資料表別名清單覆寫預設名稱，像這樣：

```

=> SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three')) AS t (num,letter);
 num | letter
-----+--------
   1 | one
   2 | two
   3 | three
(3 rows)
```

在語法上，後面接著運算式清單的 `VALUES` 會被視為等同於：

```

SELECT select_list FROM table_expression
```

並且可以出現在任何可以使用 `SELECT` 的地方。例如，你可以將它作為 `UNION` 的一部分使用，或為它附加 *`sort_specification`*（`ORDER BY`、`LIMIT` 與／或 `OFFSET`）。`VALUES` 最常用作 `INSERT` 指令的資料來源，其次則是作為子查詢。

更多資訊請參閱 [VALUES](../../reference/sql-commands/sql-values.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries-values.html)（原文版本：18.6；核對日期：2026-09-11）
