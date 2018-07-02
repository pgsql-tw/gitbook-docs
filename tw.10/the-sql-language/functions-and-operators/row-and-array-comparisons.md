---
description: 版本：10
---

# 9.23. 資料列與陣列的比較運算

本節介紹了用於在多群組內容之間進行多重比較的幾個專用語法結構。這些功能在語法上與前一節的子查詢形式相關，但不涉及子查詢。涉及陣列子表示式的形式是 PostgreSQL 的延伸功能；其餘的都是相容 SQL 的。本節中記錄的所有表達形式都是回傳布林值（true/false）結果。

## 9.23.1. `IN`

```text
expression IN (value [, ...])
```

右側是 scalar 表示式帶括號的列表。如果左側表示式的結果等於任何右側表示式，結果為「true」。這是一個簡寫的方式

```text
expression = value1
OR
expression = value2
OR
...
```

請注意，如果左側表示式產生空值，或者沒有相等的右側值並且至少有一個右側表示式產生空值，則 IN 的的結果將為空，而不是 false。這符合 SQL 空值布林組合的普遍規則。

## 9.23.2. `NOT IN`

```text
expression NOT IN (value [, ...])
```

右側是 scalar 表示式帶括號的列表。如果左側表示式的結果不等於所有右側表示式，則結果為「true」。 這是一個簡寫的方式

```text
expression <> value1
AND
expression <> value2
AND
...
```

請注意，如果左邊的表示式為空，或者沒有相等的右邊的值，並且至少有一個右邊的表示式為空，則 NOT IN 的結果將為空，而不要天真地認為是 true。這符合 SQL 空值布林組合的普遍規則。

### 小技巧

x NOT IN y 在所有情況下都等於 NOT（x IN y）。但是，使用 NOT IN 時，與使用 IN 時相比，空值更有可能讓新手感到痛苦。如果可能的話，最好積極轉換自己需要的比較內容。

## 9.23.3. `ANY`/`SOME` \(array\)

```text
expression operator ANY (array expression)
expression operator SOME (array expression)
```

右側是一個帶括號的表示式，它必須產生一個陣列。使用給定的運算子評估左側表示式並與陣列的每個元素進行比較，該運算子必須產生布林結果。如果獲得任何 true 結果，則 ANY 的結果為「true」。 如果未找到 true（包括陣列中沒有元素的情況），則結果為「false」。

如果陣列表示式產生一個空的陣列，則 ANY 的結果將為空。如果左邊的表示式為空，則 ANY 的結果通常為空（儘管非嚴格的比較運算子可能會產生不同的結果）。另外，如果右邊的陣列包含任何空元素並且沒有獲得真正的比較結果，則 ANY 的結果將為空，而不是 false（再次假設嚴格的比較運算子）。這符合 SQL 空值布林組合的普遍規則。

`SOME 是 ANY 的同義詞。`

## 9.23.4. `ALL` \(array\)

```text
expression operator ALL (array expression)
```

右側是一個帶括號的表示式，它必須產生一個陣列。使用給定的運算子計算左側表示式並與陣列的每個元素進行比較，該運算子必須產生布林結果。如果所有比較都為真（包括陣列為空的情況），則 ALL 的結果為“真”。如果發現任何錯誤的情況，結果就為“假”。

如果陣列表示式產生一個空陣列，則 ALL 的結果將為 NULL。如果左邊的表示式為NULL，則 ALL 的結果通常為 NULL（儘管非嚴格的比較運算子可能產生不同的結果）。另外，如果右邊的陣列包含任何 NULL 元素，並且沒有獲得錯誤的比較結果，則 ALL 的結果將為 NULL，而不是 TRUE（再次假設一個嚴格的比較運算子）。 這符合 SQL NULL 布林組合的一般性規則。

## 9.23.5. Row Constructor Comparison

```text
row_constructor operator row_constructor
```

Each side is a row constructor, as described in [Section 4.2.13](https://www.postgresql.org/docs/10/static/sql-expressions.html#SQL-SYNTAX-ROW-CONSTRUCTORS). The two row values must have the same number of fields. Each side is evaluated and they are compared row-wise. Row constructor comparisons are allowed when the _`operator`_ is `=`, `<>`, `<`, `<=`, `>` or `>=`. Every row element must be of a type which has a default B-tree operator class or the attempted comparison may generate an error.

### Note

Errors related to the number or types of elements might not occur if the comparison is resolved using earlier columns.

The `=` and `<>` cases work slightly differently from the others. Two rows are considered equal if all their corresponding members are non-null and equal; the rows are unequal if any corresponding members are non-null and unequal; otherwise the result of the row comparison is unknown \(null\).

For the `<`, `<=`, `>` and `>=` cases, the row elements are compared left-to-right, stopping as soon as an unequal or null pair of elements is found. If either of this pair of elements is null, the result of the row comparison is unknown \(null\); otherwise comparison of this pair of elements determines the result. For example, `ROW(1,2,NULL) < ROW(1,3,0)` yields true, not null, because the third pair of elements are not considered.

### Note

Prior to PostgreSQL 8.2, the `<`, `<=`, `>` and `>=` cases were not handled per SQL specification. A comparison like `ROW(a,b) < ROW(c,d)` was implemented as `a < c AND b < d` whereas the correct behavior is equivalent to `a < c OR (a = c AND b < d)`.

```text
row_constructor IS DISTINCT FROM row_constructor
```

This construct is similar to a `<>` row comparison, but it does not yield null for null inputs. Instead, any null value is considered unequal to \(distinct from\) any non-null value, and any two nulls are considered equal \(not distinct\). Thus the result will either be true or false, never null.

```text
row_constructor IS NOT DISTINCT FROM row_constructor
```

This construct is similar to a `=` row comparison, but it does not yield null for null inputs. Instead, any null value is considered unequal to \(distinct from\) any non-null value, and any two nulls are considered equal \(not distinct\). Thus the result will always be either true or false, never null.

## 9.23.6. 複合型別比較

```text
record operator record
```

如果結果取決於比較兩個 NULL 值或 NULL 和非 NULL，則 SQL 規範要求按資料列進行比較以回傳 NULL。PostgreSQL只在比較兩個資料列建構函數的結果（如 [9.23.5 節](row-and-array-comparisons.md#9-23-5-row-constructor-comparison)）或者將一個資料列建構函數與子查詢的輸出結果進行比較時（如 [9.22 節](9.22.-zi-cha-xun.md)）那樣做。在比較兩個複合型別內容的其他部份中，兩個 NULL 字串會被認為是相等的，並且 NULL 被認為大於非 NULL。為了對複合型別進行一致的排序和索引行為，這是必須的。

評估每一側，並逐個資料列比較它們。 當運算符為 =，&lt;&gt;，&lt;，&lt;=，&gt; 或 &gt;= 時，允許複合型別比較，或者俱有與其中一個類似的語義。（具體而言，如果一個運算子是 B-Tree 運算子類的成員，或者是 B-Tree 運算子類的 = 成員的否定運算，則它可以是資料列比較運算子。）上述運算子的預設行為與資料列建構函數的 IS \[NOT\] DISTINCT FROM 相同（見[第 9.23.5 節](row-and-array-comparisons.md#9-23-5-row-constructor-comparison)）。

為了支援包含沒有預設 B-Tree 運算子類的元素的資料列匹配，以下運算子被定義用於複合型別比較： _=，_ &lt;&gt;， _&lt;，_ &lt;=，_&gt; 和_ &gt;=。這些運算子比較兩個資料列的內部二進製表示形式。即使兩個資料列與等號運算子的比較為真，兩個資料列也可能具有不同的二進製表示形式。 這些比較運算子下的資料列排序是確定性的，但沒有其他意義。這些運算子在內部用於具體化檢視表，並可用於其他專用目的（如複寫），但不打算經常用於撰寫查詢。

