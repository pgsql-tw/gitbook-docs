<a id="FUNCTIONS-SUBQUERY"></a>

## 9.24. 子查詢運算式 [#](#FUNCTIONS-SUBQUERY)

[9.24.1. `EXISTS`](functions-subquery.md#FUNCTIONS-SUBQUERY-EXISTS)

[9.24.2. `IN`](functions-subquery.md#FUNCTIONS-SUBQUERY-IN)

[9.24.3. `NOT IN`](functions-subquery.md#FUNCTIONS-SUBQUERY-NOTIN)

[9.24.4. `ANY`/`SOME`](functions-subquery.md#FUNCTIONS-SUBQUERY-ANY-SOME)

[9.24.5. `ALL`](functions-subquery.md#FUNCTIONS-SUBQUERY-ALL)

[9.24.6. 單列比較](functions-subquery.md#FUNCTIONS-SUBQUERY-SINGLE-ROW-COMP)

<a id="id-1.5.8.30.2"></a><a id="id-1.5.8.30.3"></a><a id="id-1.5.8.30.4"></a><a id="id-1.5.8.30.5"></a><a id="id-1.5.8.30.6"></a><a id="id-1.5.8.30.7"></a><a id="id-1.5.8.30.8"></a>

本節說明 PostgreSQL 中可用的、符合 SQL 標準的子查詢運算式。本節所記載的所有運算式形式，都會回傳布林（true／false）結果。

<a id="FUNCTIONS-SUBQUERY-EXISTS"></a>

### 9.24.1. `EXISTS` [#](#FUNCTIONS-SUBQUERY-EXISTS)

```

EXISTS (subquery)
```

`EXISTS` 的引數是任意的 `SELECT` 陳述式，也就是*子查詢*（subquery）。系統會評估子查詢，以判斷它是否回傳任何資料列。如果它至少回傳一筆資料列，`EXISTS` 的結果就是「true」；如果子查詢沒有回傳任何資料列，`EXISTS` 的結果就是「false」。

子查詢可以參照外圍查詢的變數，在子查詢的每一次評估中，這些變數都會作為常數。

子查詢通常只會執行到足以判斷是否至少回傳一筆資料列為止，而不會一路執行到完成。撰寫具有副作用（例如呼叫序列函式）的子查詢是不明智的；副作用是否會發生可能無法預測。

由於結果只取決於是否回傳任何資料列，而不取決於這些資料列的內容，因此子查詢的輸出清單通常並不重要。一種常見的撰寫慣例，是將所有 `EXISTS` 測試寫成 `EXISTS(SELECT 1 WHERE ...)` 的形式。不過這項規則也有例外，例如使用 `INTERSECT` 的子查詢。

這個簡單的範例類似於在 `col2` 上的內部聯結，但即使有好幾筆相符的 `tab2` 資料列，它對每一筆 `tab1` 資料列最多也只會產生一筆輸出資料列：

```

SELECT col1
FROM tab1
WHERE EXISTS (SELECT 1 FROM tab2 WHERE col2 = tab1.col2);
```

<a id="FUNCTIONS-SUBQUERY-IN"></a>

### 9.24.2. `IN` [#](#FUNCTIONS-SUBQUERY-IN)

```

expression IN (subquery)
```

右側是一個加上括號的子查詢，它必須正好回傳一個欄位。左側運算式會被評估，並與子查詢結果的每一筆資料列比較。如果找到任何相等的子查詢資料列，`IN` 的結果就是「true」。如果沒有找到相等的資料列（包括子查詢沒有回傳任何資料列的情況），結果就是「false」。

請注意，如果左側運算式產生 null，或者右側沒有相等的值且至少有一筆右側資料列產生 null，`IN` 結構的結果就會是 null，而不是 false。這符合 SQL 對 null 值進行布林組合的一般規則。

與 `EXISTS` 一樣，假設子查詢會被完整地評估是不明智的。

```

row_constructor IN (subquery)
```

這種形式的 `IN` 的左側是一個資料列建構子，如[第 4.2.13 節](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)所述。右側是一個加上括號的子查詢，它回傳的欄位數必須與左側資料列中的運算式數量完全相同。左側的運算式會被評估，並逐列與子查詢結果的每一筆資料列比較。如果找到任何相等的子查詢資料列，`IN` 的結果就是「true」。如果沒有找到相等的資料列（包括子查詢沒有回傳任何資料列的情況），結果就是「false」。

和平常一樣，資料列中的 null 值會依照 SQL 布林運算式的一般規則組合。如果兩筆資料列所有對應的成員都非 null 且相等，它們就被視為相等；如果有任何對應的成員非 null 且不相等，它們就不相等；否則該資料列比較的結果是未知（null）。如果所有逐列的結果都是不相等或 null，且至少有一個 null，那麼 `IN` 的結果就是 null。

<a id="FUNCTIONS-SUBQUERY-NOTIN"></a>

### 9.24.3. `NOT IN` [#](#FUNCTIONS-SUBQUERY-NOTIN)

```

expression NOT IN (subquery)
```

右側是一個加上括號的子查詢，它必須正好回傳一個欄位。左側運算式會被評估，並與子查詢結果的每一筆資料列比較。如果只找到不相等的子查詢資料列（包括子查詢沒有回傳任何資料列的情況），`NOT IN` 的結果就是「true」。如果找到任何相等的資料列，結果就是「false」。

請注意，如果左側運算式產生 null，或者右側沒有相等的值且至少有一筆右側資料列產生 null，`NOT IN` 結構的結果就會是 null，而不是 true。這符合 SQL 對 null 值進行布林組合的一般規則。

與 `EXISTS` 一樣，假設子查詢會被完整地評估是不明智的。

```

row_constructor NOT IN (subquery)
```

這種形式的 `NOT IN` 的左側是一個資料列建構子，如[第 4.2.13 節](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)所述。右側是一個加上括號的子查詢，它回傳的欄位數必須與左側資料列中的運算式數量完全相同。左側的運算式會被評估，並逐列與子查詢結果的每一筆資料列比較。如果只找到不相等的子查詢資料列（包括子查詢沒有回傳任何資料列的情況），`NOT IN` 的結果就是「true」。如果找到任何相等的資料列，結果就是「false」。

和平常一樣，資料列中的 null 值會依照 SQL 布林運算式的一般規則組合。如果兩筆資料列所有對應的成員都非 null 且相等，它們就被視為相等；如果有任何對應的成員非 null 且不相等，它們就不相等；否則該資料列比較的結果是未知（null）。如果所有逐列的結果都是不相等或 null，且至少有一個 null，那麼 `NOT IN` 的結果就是 null。

<a id="FUNCTIONS-SUBQUERY-ANY-SOME"></a>

### 9.24.4. `ANY`/`SOME` [#](#FUNCTIONS-SUBQUERY-ANY-SOME)

```

expression operator ANY (subquery)
expression operator SOME (subquery)
```

右側是一個加上括號的子查詢，它必須正好回傳一個欄位。左側運算式會被評估，並使用給定的 *`operator`* 與子查詢結果的每一筆資料列比較，而該運算子必須產生布林結果。如果得到任何 true 結果，`ANY` 的結果就是「true」。如果沒有找到任何 true 結果（包括子查詢沒有回傳任何資料列的情況），結果就是「false」。

`SOME` 是 `ANY` 的同義詞。`IN` 等價於 `= ANY`。

請注意，如果沒有任何成功的比較，而且至少有一筆右側資料列使運算子的結果為 null，`ANY` 結構的結果就會是 null，而不是 false。這符合 SQL 對 null 值進行布林組合的一般規則。

與 `EXISTS` 一樣，假設子查詢會被完整地評估是不明智的。

```

row_constructor operator ANY (subquery)
row_constructor operator SOME (subquery)
```

這種形式的 `ANY` 的左側是一個資料列建構子，如[第 4.2.13 節](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)所述。右側是一個加上括號的子查詢，它回傳的欄位數必須與左側資料列中的運算式數量完全相同。左側的運算式會被評估，並使用給定的 *`operator`* 逐列與子查詢結果的每一筆資料列比較。如果比較對任何一筆子查詢資料列回傳 true，`ANY` 的結果就是「true」。如果比較對每一筆子查詢資料列都回傳 false（包括子查詢沒有回傳任何資料列的情況），結果就是「false」。如果與子查詢資料列的比較都沒有回傳 true，而且至少有一次比較回傳 NULL，結果就是 NULL。

關於資料列建構子比較之意義的細節，請參閱[第 9.25.5 節](functions-comparisons.md#ROW-WISE-COMPARISON)。

<a id="FUNCTIONS-SUBQUERY-ALL"></a>

### 9.24.5. `ALL` [#](#FUNCTIONS-SUBQUERY-ALL)

```

expression operator ALL (subquery)
```

右側是一個加上括號的子查詢，它必須正好回傳一個欄位。左側運算式會被評估，並使用給定的 *`operator`* 與子查詢結果的每一筆資料列比較，而該運算子必須產生布林結果。如果所有資料列都產生 true（包括子查詢沒有回傳任何資料列的情況），`ALL` 的結果就是「true」。如果發現任何 false 結果，結果就是「false」。如果與子查詢資料列的比較都沒有回傳 false，而且至少有一次比較回傳 NULL，結果就是 NULL。

`NOT IN` 等價於 `<> ALL`。

與 `EXISTS` 一樣，假設子查詢會被完整地評估是不明智的。

```

row_constructor operator ALL (subquery)
```

這種形式的 `ALL` 的左側是一個資料列建構子，如[第 4.2.13 節](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)所述。右側是一個加上括號的子查詢，它回傳的欄位數必須與左側資料列中的運算式數量完全相同。左側的運算式會被評估，並使用給定的 *`operator`* 逐列與子查詢結果的每一筆資料列比較。如果比較對所有子查詢資料列都回傳 true（包括子查詢沒有回傳任何資料列的情況），`ALL` 的結果就是「true」。如果比較對任何一筆子查詢資料列回傳 false，結果就是「false」。如果與子查詢資料列的比較都沒有回傳 false，而且至少有一次比較回傳 NULL，結果就是 NULL。

關於資料列建構子比較之意義的細節，請參閱[第 9.25.5 節](functions-comparisons.md#ROW-WISE-COMPARISON)。

<a id="FUNCTIONS-SUBQUERY-SINGLE-ROW-COMP"></a>

### 9.24.6. 單列比較 [#](#FUNCTIONS-SUBQUERY-SINGLE-ROW-COMP)

<a id="id-1.5.8.30.15.2"></a>

```

row_constructor operator (subquery)
```

左側是一個資料列建構子，如[第 4.2.13 節](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)所述。右側是一個加上括號的子查詢，它回傳的欄位數必須與左側資料列中的運算式數量完全相同。此外，子查詢回傳的資料列不能超過一筆。（如果它回傳零筆資料列，結果就視為 null。）左側會被評估，並逐列與子查詢的單一結果資料列比較。

關於資料列建構子比較之意義的細節，請參閱[第 9.25.5 節](functions-comparisons.md#ROW-WISE-COMPARISON)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-subquery.html)（原文版本：18.6；核對日期：2026-09-11）
