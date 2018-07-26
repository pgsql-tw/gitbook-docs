# 9.17. 條件表示式

本節介紹 PostgreSQL 中符合 SQL 標準可用的條件表示式。

#### 提示

如果您的需求超出了這些條件表示式的功能，您可能需要考慮使用功能更強的程序語言編寫 stored procedure。

#### 9.17.1. `CASE`

SQL 中的 CASE 表示式是一種通用的條件表示式，類似於其他程序語言中的 if / else 語句：

```text
CASE WHEN condition THEN result
     [WHEN ...]
     [ELSE result]
END
```

CASE子句可用於任何表示式有效的地方。每個條件都是一個回傳布林值的表示式。如果條件結果為 true，則 CASE 表示式的值為該條件之後的結果，而不處理CASE表達式的其餘部分。如果條件的結果不成立，則以相同的方式檢查後續的 WHEN 子句。如果沒有任何 WHEN 條件成立，則 CASE 表示式的值是 ELSE 子句的結果。如果省略了 ELSE 子句並且沒有條件為真，則結果為 null。

範例：

```text
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

所有結果表示式的資料型別都必須可轉換為單一的輸出型別。更多細節請參閱 [10.5 節](../type-conversion/union-case-and-related-constructs.md)。

CASE 表示式的「簡單」語法是上述一般語法的變形：

```text
CASE expression
    WHEN value THEN result
    [WHEN ...]
    [ELSE result]
END
```

計算第一個表示式，然後與 WHEN 子句中的每個表示式的結果值進行比較，直到找到與其相等的值。如果未找到匹配的項目，則回傳 ELSE 子句（或空值）的結果。這與 C 語言中的 switch 語句類似。

上面的例子可以使用簡單的 CASE 語法來撰寫：

```text
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

CASE 表示式不會計算任何不需要的子表示式來確定結果。例如，這是避免除以零例外狀況可能的方法：

```text
SELECT ... WHERE CASE WHEN x <> 0 THEN y/x > 1.5 ELSE false END;
```

#### 注意

如 [4.2.14 節](../sql-syntax/value-expressions.md#4-2-14-expression-evaluation-rules)所述，在不同時候計算表示式的子表示式時會出現各種情況，因此「CASE 只計算必要子表示式」的原則並不是固定的。例如，一個常數 1/0 的子表示式在查詢規畫時通常就會導致一個除以零的錯誤，即使它在 CASE 部分內，在執行時永遠不會被使用。

#### 9.17.2. `COALESCE`

```text
COALESCE(value [, ...])
```

COALESCE 函數回傳非空值的第一個參數。僅當所有參數都為空值時才回傳空值。當檢索資料要進行顯示時，它通常用於將預認值替換為空值，例如：

```text
SELECT COALESCE(description, short_description, '(none)') ...
```

如果它不為 null，則回傳 descrtiption；否則，如果 short\_description 不為null，則傳回 short\_description；否則回傳（none）。

像 CASE 表示式一樣，COALESCE 只計算確定結果所需的參數；也就是說，不會計算第一個非空值參數之後的參數。此 SQL 標準函數提供了與 NVL 和 IFNULL 類似的功能，這些在其他某些資料庫系統中所使用的功能。

#### 9.17.3. `NULLIF`

```text
NULLIF(value1, value2)
```

如果 value1 等於 value2，則 NULLIF 函數回傳空值；否則回傳 value1。這可以用來執行上面 COALESCE 範例的逆操作：

```text
SELECT NULLIF(value, '(none)') ...
```

在這個例子中，如果 value 是（none），則回傳 null，否則回傳 value 的值。

#### 9.17.4. `GREATEST` and `LEAST`

```text
GREATEST(value [, ...])
```

```text
LEAST(value [, ...])
```

GREATEST 和 LEAST 函數從任意數量的表示式列表中選擇最大值或最小值。表示式必須全部轉換為通用的資料型別，這將成為結果的別型（詳見 [10.5 節](../type-conversion/union-case-and-related-constructs.md)）。列表中的 **NULL 值將會被忽略**。僅當所有表示式求值為 NULL 時，結果才會為 NULL。

請注意，GREATEST 和 LEAST 並不在 SQL 標準中，但卻是一個常見的延伸功能。如果任何參數為 NULL，則其他一些資料庫會使其回傳 NULL，而不是僅在所有參數都為 NULL 時回傳 NULL。

