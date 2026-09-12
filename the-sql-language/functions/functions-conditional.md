<a id="FUNCTIONS-CONDITIONAL"></a>

## 9.18. 條件運算式 [#](#FUNCTIONS-CONDITIONAL)

[9.18.1. `CASE`](functions-conditional.md#FUNCTIONS-CASE)

[9.18.2. `COALESCE`](functions-conditional.md#FUNCTIONS-COALESCE-NVL-IFNULL)

[9.18.3. `NULLIF`](functions-conditional.md#FUNCTIONS-NULLIF)

[9.18.4. `GREATEST` 與 `LEAST`](functions-conditional.md#FUNCTIONS-GREATEST-LEAST)

<a id="id-1.5.8.24.2"></a><a id="id-1.5.8.24.3"></a>

本節說明 PostgreSQL 中可用的、符合 SQL 標準的條件運算式。

### 提示

如果你的需求超出了這些條件運算式的能力範圍，你可以考慮以表達能力更強的程式語言撰寫伺服器端函式。

### 注意

雖然 `COALESCE`、`GREATEST` 與 `LEAST` 在語法上與函式相似，但它們並不是一般的函式，因此不能搭配明確的 `VARIADIC` 陣列引數使用。

<a id="FUNCTIONS-CASE"></a>

### 9.18.1. `CASE` [#](#FUNCTIONS-CASE)

SQL 的 `CASE` 運算式是一種通用的條件運算式，類似於其他程式語言中的 if/else 陳述式：

```

CASE WHEN condition THEN result
     [WHEN ...]
     [ELSE result]
END
```

凡是可以使用運算式的地方，都可以使用 `CASE` 子句。每個 *`condition`* 都是回傳 `boolean` 結果的運算式。如果條件的結果為 true，`CASE` 運算式的值就是該條件後面的 *`result`*，而 `CASE` 運算式的其餘部分不會被處理。如果條件的結果不為 true，就以同樣的方式檢查後續的任何 `WHEN` 子句。如果沒有任何 `WHEN` *`condition`* 產生 true，`CASE` 運算式的值就是 `ELSE` 子句的 *`result`*。如果省略了 `ELSE` 子句，而且沒有任何條件為 true，結果就是 null。

一個範例：

```

SELECT * FROM test;

 a
---
 1
 2
 3


SELECT a,
       CASE WHEN a=1 THEN 'one'
            WHEN a=2 THEN 'two'
            ELSE 'other'
       END
    FROM test;

 a | case
---+-------
 1 | one
 2 | two
 3 | other
```

所有 *`result`* 運算式的資料型別，都必須能夠轉換為單一的輸出型別。更多細節請參閱[第 10.5 節](../typeconv/typeconv-union-case.md)。

`CASE` 運算式還有一種「簡單」形式，是上述一般形式的變化：

```

CASE expression
    WHEN value THEN result
    [WHEN ...]
    [ELSE result]
END
```

首先計算第一個 *`expression`*，然後將它與 `WHEN` 子句中的每個 *`value`* 運算式比較，直到找到與它相等的值為止。如果找不到相符的值，就回傳 `ELSE` 子句的 *`result`*（或 null 值）。這類似於 C 語言中的 `switch` 陳述式。

上面的範例可以用簡單的 `CASE` 語法寫成：

```

SELECT a,
       CASE a WHEN 1 THEN 'one'
              WHEN 2 THEN 'two'
              ELSE 'other'
       END
    FROM test;

 a | case
---+-------
 1 | one
 2 | two
 3 | other
```

`CASE` 運算式不會評估任何決定結果時不需要的子運算式。例如，下面是一種避免除以零錯誤的可能做法：

```

SELECT ... WHERE CASE WHEN x <> 0 THEN y/x > 1.5 ELSE false END;
```

### 注意

如[第 4.2.14 節](../sql-syntax/sql-expressions.md#SYNTAX-EXPRESS-EVAL)所述，在許多情況下，運算式的子運算式會在不同的時間被評估，因此「`CASE` 只評估必要的子運算式」這項原則並非牢不可破。例如，常數子運算式 `1/0` 通常會在規劃時就導致除以零的錯誤，即使它位於執行時永遠不會進入的 `CASE` 分支中也一樣。

<a id="FUNCTIONS-COALESCE-NVL-IFNULL"></a>

### 9.18.2. `COALESCE` [#](#FUNCTIONS-COALESCE-NVL-IFNULL)

<a id="id-1.5.8.24.8.2"></a><a id="id-1.5.8.24.8.3"></a><a id="id-1.5.8.24.8.4"></a>

```

COALESCE(value [, ...])
```

`COALESCE` 函式會回傳其引數中第一個不為 null 的值。只有在所有引數都為 null 時才會回傳 null。它常用於在擷取資料以供顯示時，以預設值取代 null 值，例如：

```

SELECT COALESCE(description, short_description, '(none)') ...
```

如果 `description` 不為 null，就回傳它；否則如果 `short_description` 不為 null，就回傳它；否則回傳 `(none)`。

所有引數都必須能夠轉換為一個共同的資料型別，而該型別就是結果的型別（詳情請參閱[第 10.5 節](../typeconv/typeconv-union-case.md)）。

就像 `CASE` 運算式一樣，`COALESCE` 只會評估決定結果所需的引數；也就是說，第一個非 null 引數右邊的引數不會被評估。這個 SQL 標準函式提供的功能，類似於其他一些資料庫系統中所使用的 `NVL` 與 `IFNULL`。

<a id="FUNCTIONS-NULLIF"></a>

### 9.18.3. `NULLIF` [#](#FUNCTIONS-NULLIF)

<a id="id-1.5.8.24.9.2"></a>

```

NULLIF(value1, value2)
```

如果 *`value1`* 等於 *`value2`*，`NULLIF` 函式就會回傳 null 值；否則回傳 *`value1`*。這可以用來執行上面 `COALESCE` 範例的反向操作：

```

SELECT NULLIF(value, '(none)') ...
```

在這個範例中，如果 `value` 是 `(none)`，就回傳 null，否則回傳 `value` 的值。

兩個引數必須是可比較的型別。具體來說，它們的比較方式與你寫出 `value1 = value2` 完全相同，因此必須有合適的 `=` 運算子可用。

結果的型別與第一個引數相同——但有一個細微之處。實際回傳的是隱含之 `=` 運算子的第一個引數，而在某些情況下，它會被提升以符合第二個引數的型別。例如，`NULLIF(1, 2.2)` 會產生 `numeric`，因為沒有 `integer` `=` `numeric` 運算子，只有 `numeric` `=` `numeric`。

<a id="FUNCTIONS-GREATEST-LEAST"></a>

### 9.18.4. `GREATEST` 與 `LEAST` [#](#FUNCTIONS-GREATEST-LEAST)

<a id="id-1.5.8.24.10.2"></a><a id="id-1.5.8.24.10.3"></a>

```

GREATEST(value [, ...])
```

```

LEAST(value [, ...])
```

`GREATEST` 與 `LEAST` 函式會從任意數量的運算式清單中選出最大或最小的值。所有運算式都必須能夠轉換為一個共同的資料型別，而該型別就是結果的型別（詳情請參閱[第 10.5 節](../typeconv/typeconv-union-case.md)）。

引數清單中的 NULL 值會被忽略。只有在所有運算式的結果都為 NULL 時，結果才會是 NULL。（這偏離了 SQL 標準。依照標準，只要有任何引數為 NULL，回傳值就是 NULL。有些其他資料庫的行為就是如此。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-conditional.html)（原文版本：18.6；核對日期：2026-09-11）
