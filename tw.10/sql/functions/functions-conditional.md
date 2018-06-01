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

所有結果表示式的資料型別都必須可轉換為單一的輸出型別。更多細節請參閱 [10.5 節](../typeconv/union-case.md)。

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

如 [4.2.14 節](../syntax/4.2.-can-shu-biao-shi-shi.md#4-2-14-expression-evaluation-rules)所述，在不同時候計算表示式的子表示式時會出現各種情況，因此「CASE 只計算必要子表示式」的原則並不是固定的。例如，一個常數 1/0 的子表示式在查詢規畫時通常就會導致一個除以零的錯誤，即使它在 CASE 部分內，在執行時永遠不會被使用。

#### 9.17.2. `COALESCE`

```text
COALESCE(value [, ...])
```

The `COALESCE` function returns the first of its arguments that is not null. Null is returned only if all arguments are null. It is often used to substitute a default value for null values when data is retrieved for display, for example:

```text
SELECT COALESCE(description, short_description, '(none)') ...
```

This returns `description` if it is not null, otherwise `short_description` if it is not null, otherwise `(none)`.

Like a `CASE` expression, `COALESCE` only evaluates the arguments that are needed to determine the result; that is, arguments to the right of the first non-null argument are not evaluated. This SQL-standard function provides capabilities similar to `NVL` and `IFNULL`, which are used in some other database systems.

#### 9.17.3. `NULLIF`

```text
NULLIF(value1, value2)
```

The `NULLIF` function returns a null value if _`value1`_ equals _`value2`_; otherwise it returns _`value1`_. This can be used to perform the inverse operation of the `COALESCE` example given above:

```text
SELECT NULLIF(value, '(none)') ...
```

In this example, if `value` is `(none)`, null is returned, otherwise the value of `value` is returned.

#### 9.17.4. `GREATEST` and `LEAST`

```text
GREATEST(value [, ...])
```

```text
LEAST(value [, ...])
```

The `GREATEST` and `LEAST` functions select the largest or smallest value from a list of any number of expressions. The expressions must all be convertible to a common data type, which will be the type of the result \(see [Section 10.5](https://www.postgresql.org/docs/10/static/typeconv-union-case.html) for details\). NULL values in the list are ignored. The result will be NULL only if all the expressions evaluate to NULL.

Note that `GREATEST` and `LEAST` are not in the SQL standard, but are a common extension. Some other databases make them return NULL if any argument is NULL, rather than only when all are NULL.

