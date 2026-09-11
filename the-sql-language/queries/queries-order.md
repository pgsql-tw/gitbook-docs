<a id="QUERIES-ORDER"></a>

## 7.5. 排序資料列（`ORDER BY`） [#](#QUERIES-ORDER)

<a id="id-1.5.6.9.2"></a><a id="id-1.5.6.9.3"></a>

查詢產生輸出資料表之後（在選取清單處理完之後），可以選擇對它進行排序。如果沒有選擇排序，資料列會以未指定的順序回傳。在這種情況下，實際的順序取決於掃描與聯結計畫的類型以及磁碟上的順序，但絕不能依賴它。只有在明確選擇排序步驟時，才能保證特定的輸出順序。

`ORDER BY` 子句指定排序順序：

```

SELECT select_list
    FROM table_expression
    ORDER BY sort_expression1 [ASC | DESC] [NULLS { FIRST | LAST }]
             [, sort_expression2 [ASC | DESC] [NULLS { FIRST | LAST }] ...]
```

排序運算式可以是在查詢的選取清單中有效的任何運算式。例如：

```

SELECT a, b FROM table1 ORDER BY a + b, c;
```

當指定了多個運算式時，後面的值會用來排序依前面的值判定為相等的資料列。每個運算式後面都可以選擇接上 `ASC` 或 `DESC` 關鍵字，將排序方向設為遞增或遞減。`ASC` 順序是預設值。遞增順序會將較小的值排在前面，其中「較小」是依 `<` 運算子定義的。同樣地，遞減順序是依 `>` 運算子決定的。
[<a id="id-1.5.6.9.5.10"></a>[6]](#ftn.id-1.5.6.9.5.10)

`NULLS FIRST` 與 `NULLS LAST` 選項可以用來決定在排序中，null 值要出現在非 null 值之前還是之後。預設情況下，null 值在排序時會被當作比任何非 null 值都大；也就是說，`DESC` 順序的預設值是 `NULLS FIRST`，否則是 `NULLS LAST`。

請注意，排序選項是針對每個排序欄位分別考量的。例如，`ORDER BY x, y DESC` 表示 `ORDER BY x ASC, y DESC`，這與 `ORDER BY x DESC, y DESC` 並不相同。

*`sort_expression`* 也可以是輸出欄位的欄位標籤或編號，例如：

```

SELECT a + b AS sum, c FROM table1 ORDER BY sum;
SELECT a, max(b) FROM table1 GROUP BY a ORDER BY 1;
```

這兩者都依第一個輸出欄位排序。請注意，輸出欄位名稱必須單獨使用，也就是說，它不能用在運算式中；例如，下列寫法是*不*正確的：

```

SELECT a + b AS sum, c FROM table1 ORDER BY sum + c;          -- wrong
```

這項限制是為了減少歧義。如果 `ORDER BY` 的項目是一個簡單的名稱，而它既可能對應輸出欄位名稱，也可能對應資料表運算式中的欄位，那麼仍然會有歧義。在這種情況下，會使用輸出欄位。只有在你使用 `AS` 將某個輸出欄位重新命名為與其他資料表欄位同名時，才會造成混淆。

`ORDER BY` 可以套用在 `UNION`、`INTERSECT` 或 `EXCEPT` 組合的結果上，但在這種情況下，只允許依輸出欄位的名稱或編號排序，不能依運算式排序。

<br>

---

<a id="ftn.id-1.5.6.9.5.10"></a>

[[6]](#id-1.5.6.9.5.10) 
實際上，PostgreSQL 會使用運算式資料型別的*預設 B-tree 運算子類別*（default B-tree operator class）來決定 `ASC` 與 `DESC` 的排序順序。依慣例，資料型別會被設定成讓 `<` 與 `>` 運算子對應這個排序順序，但使用者自訂資料型別的設計者也可以選擇採取不同的做法。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries-order.html)（原文版本：18.6；核對日期：2026-09-11）
