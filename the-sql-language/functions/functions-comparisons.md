<a id="FUNCTIONS-COMPARISONS"></a>

## 9.25. 資料列與陣列比較 [#](#FUNCTIONS-COMPARISONS)

[9.25.1. `IN`](functions-comparisons.md#FUNCTIONS-COMPARISONS-IN-SCALAR)

[9.25.2. `NOT IN`](functions-comparisons.md#FUNCTIONS-COMPARISONS-NOT-IN)

[9.25.3. `ANY`/`SOME`（陣列）](functions-comparisons.md#FUNCTIONS-COMPARISONS-ANY-SOME)

[9.25.4. `ALL`（陣列）](functions-comparisons.md#FUNCTIONS-COMPARISONS-ALL)

[9.25.5. 資料列建構子比較](functions-comparisons.md#ROW-WISE-COMPARISON)

[9.25.6. 複合型別比較](functions-comparisons.md#COMPOSITE-TYPE-COMPARISON)

<a id="id-1.5.8.31.2"></a><a id="id-1.5.8.31.3"></a><a id="id-1.5.8.31.4"></a><a id="id-1.5.8.31.5"></a><a id="id-1.5.8.31.6"></a><a id="id-1.5.8.31.7"></a><a id="id-1.5.8.31.8"></a><a id="id-1.5.8.31.9"></a><a id="id-1.5.8.31.10"></a><a id="id-1.5.8.31.11"></a><a id="id-1.5.8.31.12"></a>

本節說明幾種用於在多組值之間進行多重比較的特殊結構。這些形式在語法上與前一節的子查詢形式相關，但不涉及子查詢。涉及陣列子運算式的形式是 PostgreSQL 的擴充功能；其餘的則符合 SQL 標準。本節所記載的所有運算式形式，都會回傳布林（true／false）結果。

<a id="FUNCTIONS-COMPARISONS-IN-SCALAR"></a>

### 9.25.1. `IN` [#](#FUNCTIONS-COMPARISONS-IN-SCALAR)

```

expression IN (value [, ...])
```

右側是一個加上括號的運算式清單。如果左側運算式的結果等於右側的任何一個運算式，結果就是「true」。這是下列寫法的簡寫

```

expression = value1
OR
expression = value2
OR
...
```

請注意，如果左側運算式產生 null，或者右側沒有相等的值且至少有一個右側運算式產生 null，`IN` 結構的結果就會是 null，而不是 false。這符合 SQL 對 null 值進行布林組合的一般規則。

<a id="FUNCTIONS-COMPARISONS-NOT-IN"></a>

### 9.25.2. `NOT IN` [#](#FUNCTIONS-COMPARISONS-NOT-IN)

```

expression NOT IN (value [, ...])
```

右側是一個加上括號的運算式清單。如果左側運算式的結果不等於右側的所有運算式，結果就是「true」。這是下列寫法的簡寫

```

expression <> value1
AND
expression <> value2
AND
...
```

請注意，如果左側運算式產生 null，或者右側沒有相等的值且至少有一個右側運算式產生 null，`NOT IN` 結構的結果就會是 null，而不是一般人可能天真地預期的 true。這符合 SQL 對 null 值進行布林組合的一般規則。

### 提示

在所有情況下，`x NOT IN y` 都等價於 `NOT (x IN y)`。不過，比起使用 `IN`，初學者在使用 `NOT IN` 時更容易被 null 值絆倒。可能的話，最好以正面的方式表達你的條件。

<a id="FUNCTIONS-COMPARISONS-ANY-SOME"></a>

### 9.25.3. `ANY`/`SOME`（陣列） [#](#FUNCTIONS-COMPARISONS-ANY-SOME)

```

expression operator ANY (array expression)
expression operator SOME (array expression)
```

右側是一個加上括號的運算式，它必須產生一個陣列值。左側運算式會被評估，並使用給定的 *`operator`* 與陣列的每個元素進行比較，而該運算子必須產生布林結果。如果得到任何 true 結果，`ANY` 的結果就是「true」。如果沒有找到任何 true 結果（包括陣列有零個元素的情況），結果就是「false」。

如果陣列運算式產生 null 陣列，`ANY` 的結果就會是 null。如果左側運算式產生 null，`ANY` 的結果通常是 null（不過非嚴格的比較運算子可能產生不同的結果）。此外，如果右側陣列包含任何 null 元素，而且沒有得到任何 true 的比較結果，`ANY` 的結果就會是 null，而不是 false（同樣假設是嚴格的比較運算子）。這符合 SQL 對 null 值進行布林組合的一般規則。

`SOME` 是 `ANY` 的同義詞。

<a id="FUNCTIONS-COMPARISONS-ALL"></a>

### 9.25.4. `ALL`（陣列） [#](#FUNCTIONS-COMPARISONS-ALL)

```

expression operator ALL (array expression)
```

右側是一個加上括號的運算式，它必須產生一個陣列值。左側運算式會被評估，並使用給定的 *`operator`* 與陣列的每個元素進行比較，而該運算子必須產生布林結果。如果所有的比較都產生 true（包括陣列有零個元素的情況），`ALL` 的結果就是「true」。如果發現任何 false 結果，結果就是「false」。

如果陣列運算式產生 null 陣列，`ALL` 的結果就會是 null。如果左側運算式產生 null，`ALL` 的結果通常是 null（不過非嚴格的比較運算子可能產生不同的結果）。此外，如果右側陣列包含任何 null 元素，而且沒有得到任何 false 的比較結果，`ALL` 的結果就會是 null，而不是 true（同樣假設是嚴格的比較運算子）。這符合 SQL 對 null 值進行布林組合的一般規則。

<a id="ROW-WISE-COMPARISON"></a>

### 9.25.5. 資料列建構子比較 [#](#ROW-WISE-COMPARISON)

```

row_constructor operator row_constructor
```

兩側都是資料列建構子，如[第 4.2.13 節](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)所述。兩個資料列建構子必須有相同數量的欄位。給定的 *`operator`* 會套用到每一對對應的欄位上。（由於欄位可能是不同的型別，這表示每一對欄位可能會選用不同的特定運算子。）所有選用的運算子都必須是某個 B-tree 運算子類別的成員，或是某個 B-tree 運算子類別之 `=` 成員的否定運算子；這表示只有當 *`operator`* 是 `=`、`<>`、`<`、`<=`、`>` 或 `>=`，或具有與其中之一相似的語意時，才能進行資料列建構子比較。

`=` 與 `<>` 的情況運作方式與其他情況稍有不同。如果兩筆資料列所有對應的成員都非 null 且相等，它們就被視為相等；如果有任何對應的成員非 null 且不相等，它們就不相等；否則資料列比較的結果是未知（null）。

對於 `<`、`<=`、`>` 與 `>=` 的情況，資料列元素會由左至右比較，一旦發現不相等或為 null 的元素對就停止。如果這一對元素中有任何一個為 null，資料列比較的結果就是未知（null）；否則就由這一對元素的比較決定結果。例如，`ROW(1,2,NULL) < ROW(1,3,0)` 會產生 true 而不是 null，因為第三對元素不會被考慮。

```

row_constructor IS DISTINCT FROM row_constructor
```

這個結構類似於 `<>` 資料列比較，但它不會因為 null 輸入而產生 null。取而代之的是，任何 null 值都被視為不等於（有別於）任何非 null 值，而任兩個 null 則被視為相等（無區別）。因此結果一定是 true 或 false，永遠不會是 null。

```

row_constructor IS NOT DISTINCT FROM row_constructor
```

這個結構類似於 `=` 資料列比較，但它不會因為 null 輸入而產生 null。取而代之的是，任何 null 值都被視為不等於（有別於）任何非 null 值，而任兩個 null 則被視為相等（無區別）。因此結果一律是 true 或 false，永遠不會是 null。

<a id="COMPOSITE-TYPE-COMPARISON"></a>

### 9.25.6. 複合型別比較 [#](#COMPOSITE-TYPE-COMPARISON)

```

record operator record
```

SQL 規格要求，如果結果取決於比較兩個 NULL 值，或一個 NULL 與一個非 NULL 值，逐列比較就要回傳 NULL。PostgreSQL 只有在比較兩個資料列建構子的結果時（如[第 9.25.5 節](functions-comparisons.md#ROW-WISE-COMPARISON)），或將資料列建構子與子查詢的輸出比較時（如[第 9.24 節](functions-subquery.md)），才會這麼做。在比較兩個複合型別值的其他情境中，兩個 NULL 欄位值被視為相等，而 NULL 被視為大於非 NULL。為了讓複合型別有一致的排序與索引行為，這是必要的。

兩側都會被評估，並逐列進行比較。當 *`operator`* 是 `=`、`<>`、`<`、`<=`、`>` 或 `>=`，或具有與其中之一相似的語意時，就允許進行複合型別比較。（具體來說，如果運算子是某個 B-tree 運算子類別的成員，或是某個 B-tree 運算子類別之 `=` 成員的否定運算子，它就可以是資料列比較運算子。）上述運算子的預設行為，與資料列建構子的 `IS [ NOT ] DISTINCT FROM` 相同（請參閱[第 9.25.5 節](functions-comparisons.md#ROW-WISE-COMPARISON)）。

為了支援比對包含沒有預設 B-tree 運算子類別之元素的資料列，為複合型別比較定義了下列運算子：`*=`、`*<>`、`*<`、`*<=`、`*>` 與 `*>=`。這些運算子比較兩筆資料列的內部二進位表示。即使以相等運算子比較兩筆資料列的結果為 true，它們的二進位表示也可能不同。在這些比較運算子下，資料列的排序是確定的，但除此之外沒有其他意義。這些運算子在內部用於具體化檢視表，對於其他特殊用途（例如複寫與 B-Tree 去重複，請參閱[第 65.1.4.3 節](../../internals/indextypes/btree.md#BTREE-DEDUPLICATION)）也可能有用。不過，它們並不打算一般性地用於撰寫查詢。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-comparisons.html)（原文版本：18.6；核對日期：2026-09-11）
