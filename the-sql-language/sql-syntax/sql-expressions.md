<a id="SQL-EXPRESSIONS"></a>

## 4.2. 值運算式 [#](#SQL-EXPRESSIONS)

[4.2.1. 欄位參照](sql-expressions.md#SQL-EXPRESSIONS-COLUMN-REFS)

[4.2.2. 位置參數](sql-expressions.md#SQL-EXPRESSIONS-PARAMETERS-POSITIONAL)

[4.2.3. 下標](sql-expressions.md#SQL-EXPRESSIONS-SUBSCRIPTS)

[4.2.4. 欄位選取](sql-expressions.md#FIELD-SELECTION)

[4.2.5. 運算子呼叫](sql-expressions.md#SQL-EXPRESSIONS-OPERATOR-CALLS)

[4.2.6. 函式呼叫](sql-expressions.md#SQL-EXPRESSIONS-FUNCTION-CALLS)

[4.2.7. 彙總運算式](sql-expressions.md#SYNTAX-AGGREGATES)

[4.2.8. Window 函式呼叫](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)

[4.2.9. 型別轉換](sql-expressions.md#SQL-SYNTAX-TYPE-CASTS)

[4.2.10. 定序運算式](sql-expressions.md#SQL-SYNTAX-COLLATE-EXPRS)

[4.2.11. 純量子查詢](sql-expressions.md#SQL-SYNTAX-SCALAR-SUBQUERIES)

[4.2.12. 陣列建構子](sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS)

[4.2.13. 資料列建構子](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)

[4.2.14. 運算式求值規則](sql-expressions.md#SYNTAX-EXPRESS-EVAL)

<a id="id-1.5.3.6.2"></a><a id="id-1.5.3.6.3"></a><a id="id-1.5.3.6.4"></a>

值運算式用於各種情境，例如 `SELECT` 指令的目標清單、`INSERT` 或 `UPDATE` 中的新欄位值，或許多指令中的搜尋條件。值運算式的結果有時稱為*純量*（scalar），以便與資料表運算式的結果（也就是一個資料表）區分。因此，值運算式也稱為*純量運算式*（scalar expression），甚至簡稱*運算式*（expression）。運算式語法允許使用算術、邏輯、集合及其他運算，從基本的部分計算出值。

值運算式是下列其中之一：

* 常數或字面值
* 欄位參照
* 位置參數參照，用於函式定義主體或預備陳述式中
* 帶下標的運算式
* 欄位選取運算式
* 運算子呼叫
* 函式呼叫
* 彙總運算式
* window 函式呼叫
* 型別轉換
* 定序運算式
* 純量子查詢
* 陣列建構子
* 資料列建構子
* 括號中的另一個值運算式（用來將子運算式分組並覆寫優先順序<a id="id-1.5.3.6.6.1.15.1.1"></a>）

除了這份清單之外，還有許多結構可以歸類為運算式，但不遵循任何一般的語法規則。它們一般具有函式或運算子的語意，並在[第 9 章](../functions/README.md)的適當位置說明。例如 `IS NULL` 子句就是其中之一。

我們已經在[第 4.1.2 節](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS)討論過常數。以下各節討論其餘的選項。

<a id="SQL-EXPRESSIONS-COLUMN-REFS"></a>

### 4.2.1. 欄位參照 [#](#SQL-EXPRESSIONS-COLUMN-REFS)

<a id="id-1.5.3.6.9.2"></a>

欄位可以用下列形式參照：

```

correlation.columnname
```

*`correlation`* 是資料表的名稱（可能以 schema 名稱限定），或是透過 `FROM` 子句為資料表定義的別名。如果欄位名稱在目前查詢所使用的所有資料表中都是唯一的，就可以省略相關名稱與分隔的句點。（另請參閱[第 7 章](../queries/README.md)。）

<a id="SQL-EXPRESSIONS-PARAMETERS-POSITIONAL"></a>

### 4.2.2. 位置參數 [#](#SQL-EXPRESSIONS-PARAMETERS-POSITIONAL)

<a id="id-1.5.3.6.10.2"></a><a id="id-1.5.3.6.10.3"></a>

位置參數參照用來表示從 SQL 陳述式外部提供的值。參數用於 SQL 函式定義與預備查詢中。有些用戶端函式庫也支援將資料值與 SQL 指令字串分開指定，此時就會使用參數來參照這些另外提供的資料值。參數參照的形式是：

```

$number
```

例如，考慮一個函式 `dept` 的定義如下：

```

CREATE FUNCTION dept(text) RETURNS dept
    AS $$ SELECT * FROM dept WHERE name = $1 $$
    LANGUAGE SQL;
```

這裡的 `$1` 會在每次呼叫函式時，參照函式第一個引數的值。

<a id="SQL-EXPRESSIONS-SUBSCRIPTS"></a>

### 4.2.3. 下標 [#](#SQL-EXPRESSIONS-SUBSCRIPTS)

<a id="id-1.5.3.6.11.2"></a>

如果某個運算式產生陣列型別的值，就可以用下列寫法取出陣列值中的特定元素

```

expression[subscript]
```

或是用下列寫法取出多個相鄰的元素（「陣列切片」，array slice）

```

expression[lower_subscript:upper_subscript]
```

（這裡的方括號 `[ ]` 是要按字面出現的。）每個 *`subscript`* 本身都是一個運算式，會被四捨五入到最接近的整數值。

一般而言，陣列 *`expression`* 必須以括號括住，但如果要取下標的運算式只是欄位參照或位置參數，就可以省略括號。此外，當原始陣列是多維陣列時，可以串接多個下標。例如：

```

mytable.arraycolumn[4]
mytable.two_d_column[17][34]
$1[10:42]
(arrayfunction(a,b))[42]
```

最後一個範例中的括號是必要的。關於陣列的更多資訊，請參閱[第 8.15 節](../datatype/arrays.md)。

<a id="FIELD-SELECTION"></a>

### 4.2.4. 欄位選取 [#](#FIELD-SELECTION)

<a id="id-1.5.3.6.12.2"></a>

如果某個運算式產生複合型別（資料列型別）的值，就可以用下列寫法取出資料列中的特定欄位

```

expression.fieldname
```

一般而言，資料列 *`expression`* 必須以括號括住，但如果要從中選取的運算式只是資料表參照或位置參數，就可以省略括號。例如：

```

mytable.mycolumn
$1.somecolumn
(rowfunction(a,b)).col3
```

（因此，限定的欄位參照其實只是欄位選取語法的一個特例。）一個重要的特例，是從複合型別的資料表欄位中取出某個欄位：

```

(compositecol).somefield
(mytable.compositecol).somefield
```

這裡的括號是必要的，用來表明 `compositecol` 是欄位名稱而不是資料表名稱，或者在第二種情況下，表明 `mytable` 是資料表名稱而不是 schema 名稱。

你可以寫 `.*` 來要求取得複合值的所有欄位：

```

(compositecol).*
```

這種表示法的行為會依情境而有所不同；詳情請參閱[第 8.16.5 節](../datatype/rowtypes.md#ROWTYPES-USAGE)。

<a id="SQL-EXPRESSIONS-OPERATOR-CALLS"></a>

### 4.2.5. 運算子呼叫 [#](#SQL-EXPRESSIONS-OPERATOR-CALLS)

<a id="id-1.5.3.6.13.2"></a>

運算子呼叫有兩種可能的語法：

<table border="0" class="simplelist" summary="Simple list"><tr><td><em class="replaceable"><code>expression</code></em> <em class="replaceable"><code>operator</code></em> <em class="replaceable"><code>expression</code></em>（二元中置運算子）</td></tr><tr><td><em class="replaceable"><code>operator</code></em> <em class="replaceable"><code>expression</code></em>（一元前置運算子）</td></tr></table>

其中 *`operator`* 語彙單元遵循[第 4.1.3 節](sql-syntax-lexical.md#SQL-SYNTAX-OPERATORS)的語法規則，或是關鍵字 `AND`、`OR` 與 `NOT` 之一，或是下列形式的限定運算子名稱：

```

OPERATOR(schema.operatorname)
```

有哪些運算子存在，以及它們是一元還是二元，取決於系統或使用者定義了哪些運算子。[第 9 章](../functions/README.md)說明了內建的運算子。

<a id="SQL-EXPRESSIONS-FUNCTION-CALLS"></a>

### 4.2.6. 函式呼叫 [#](#SQL-EXPRESSIONS-FUNCTION-CALLS)

<a id="id-1.5.3.6.14.2"></a>

函式呼叫的語法是函式名稱（可能以 schema 名稱限定），後面接著以括號括住的引數清單：

```

function_name ([expression [, expression ... ]] )
```

例如，下列運算式會計算 2 的平方根：

```

sqrt(2)
```

內建函式的清單請參閱[第 9 章](../functions/README.md)。使用者也可以加入其他函式。

在某些使用者不信任其他使用者的資料庫中發出查詢時，撰寫函式呼叫請遵守[第 10.3 節](../typeconv/typeconv-func.md)的安全注意事項。

引數可以選擇附加名稱。詳情請參閱[第 4.3 節](sql-syntax-calling-funcs.md)。

### 注意

接受單一複合型別引數的函式，可以選擇使用欄位選取語法來呼叫；反過來說，欄位選取也可以寫成函式的形式。也就是說，`col(table)` 與 `table.col` 這兩種表示法可以互換。這種行為不是 SQL 標準，但 PostgreSQL 提供了它，因為它讓函式可以用來模擬「計算欄位」。更多資訊請參閱[第 8.16.5 節](../datatype/rowtypes.md#ROWTYPES-USAGE)。

<a id="SYNTAX-AGGREGATES"></a>

### 4.2.7. 彙總運算式 [#](#SYNTAX-AGGREGATES)

<a id="id-1.5.3.6.15.2"></a><a id="id-1.5.3.6.15.3"></a><a id="id-1.5.3.6.15.4"></a><a id="id-1.5.3.6.15.5"></a>

*彙總運算式*（aggregate expression）代表在查詢所選取的資料列上套用彙總函式。彙總函式會將多個輸入簡化為單一輸出值，例如輸入的總和或平均值。彙總運算式的語法是下列其中之一：

```

aggregate_name (expression [ , ... ] [ order_by_clause ] ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name (ALL expression [ , ... ] [ order_by_clause ] ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name (DISTINCT expression [ , ... ] [ order_by_clause ] ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name ( * ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name ( [ expression [ , ... ] ] ) WITHIN GROUP ( order_by_clause ) [ FILTER ( WHERE filter_clause ) ]
```

其中 *`aggregate_name`* 是先前定義的彙總函式（可能以 schema 名稱限定），而 *`expression`* 是本身不包含彙總運算式或 window 函式呼叫的任何值運算式。選用的 *`order_by_clause`* 與 *`filter_clause`* 說明如下。

第一種形式的彙總運算式會對每一筆輸入資料列呼叫一次彙總函式。第二種形式與第一種相同，因為 `ALL` 是預設值。第三種形式會對輸入資料列中找到的每一個不同的運算式值（如果有多個運算式，則是每一組不同的值）呼叫一次彙總函式。第四種形式會對每一筆輸入資料列呼叫一次彙總函式；由於沒有指定任何特定的輸入值，它一般只對 `count(*)` 彙總函式有用。最後一種形式用於*有序集合*（ordered-set）彙總函式，說明如下。

大多數彙總函式會忽略 null 輸入，因此會捨棄一個或多個運算式產生 null 的資料列。除非另有說明，可以假設所有內建彙總函式都是如此。

例如，`count(*)` 會產生輸入資料列的總數；`count(f1)` 會產生 `f1` 不為 null 的輸入資料列數量，因為 `count` 會忽略 null；而 `count(distinct f1)` 則會產生 `f1` 中不同的非 null 值的數量。

一般而言，輸入資料列會以未指定的順序傳給彙總函式。在許多情況下這並不重要；例如，無論以什麼順序接收輸入，`min` 都會產生相同的結果。不過，有些彙總函式（例如 `array_agg` 與 `string_agg`）產生的結果會取決於輸入資料列的順序。使用這類彙總函式時，可以用選用的 *`order_by_clause`* 指定想要的順序。*`order_by_clause`* 的語法與查詢層級的 `ORDER BY` 子句相同（說明見[第 7.5 節](../queries/queries-order.md)），只是其中的運算式永遠只能是運算式，不能是輸出欄位的名稱或編號。例如：

```

WITH vals (v) AS ( VALUES (1),(3),(4),(3),(2) )
SELECT array_agg(v ORDER BY v DESC) FROM vals;
  array_agg
-------------
 {4,3,3,2,1}
```

由於 `jsonb` 只會保留最後一個相符的鍵，因此其鍵的順序可能很重要：

```

WITH vals (k, v) AS ( VALUES ('key0','1'), ('key1','3'), ('key1','2') )
SELECT jsonb_object_agg(k, v ORDER BY v) FROM vals;
      jsonb_object_agg
----------------------------
 {"key0": "1", "key1": "3"}
```

處理多引數的彙總函式時，請注意 `ORDER BY` 子句要放在所有彙總引數之後。例如，要這樣寫：

```

SELECT string_agg(a, ',' ORDER BY a) FROM table;
```

而不是這樣寫：

```

SELECT string_agg(a ORDER BY a, ',') FROM table;  -- incorrect
```

後者在語法上是有效的，但它代表呼叫一個單引數的彙總函式，並帶有兩個 `ORDER BY` 鍵（第二個鍵因為是常數，所以相當沒有用處）。

如果同時指定了 `DISTINCT` 與 *`order_by_clause`*，`ORDER BY` 運算式就只能參照 `DISTINCT` 清單中的欄位。例如：

```

WITH vals (v) AS ( VALUES (1),(3),(4),(3),(2) )
SELECT array_agg(DISTINCT v ORDER BY v DESC) FROM vals;
 array_agg
-----------
 {4,3,2,1}
```

如上所述，將 `ORDER BY` 放在彙總函式的一般引數清單中，是用於為通用與統計彙總函式排序輸入資料列，而這類彙總函式的排序是選用的。另有一類彙總函式稱為*有序集合彙總函式*（ordered-set aggregate），它們*必須*有 *`order_by_clause`*，這通常是因為這類彙總函式的計算只有在輸入資料列具有特定順序時才有意義。有序集合彙總函式的典型例子包括排名與百分位數的計算。對於有序集合彙總函式，*`order_by_clause`* 要寫在 `WITHIN GROUP (...)` 之中，如上面最後一種語法所示。*`order_by_clause`* 中的運算式會像一般彙總引數一樣，對每一筆輸入資料列求值一次，依 *`order_by_clause`* 的要求排序，再作為輸入引數傳給彙總函式。（這與非 `WITHIN GROUP` 的 *`order_by_clause`* 不同，後者不會被當作彙總函式的引數。）`WITHIN GROUP` 之前的引數運算式（如果有的話）稱為*直接引數*（direct argument），以便與 *`order_by_clause`* 中列出的*彙總引數*（aggregated argument）區分。與一般的彙總引數不同，直接引數在每次彙總呼叫中只會求值一次，而不是每一筆輸入資料列求值一次。這表示只有在變數是透過 `GROUP BY` 分組時，直接引數中才能包含這些變數；這項限制就如同直接引數完全不在彙總運算式中一樣。直接引數通常用於百分位數比例這類在每次彙總計算中只以單一值才有意義的東西。直接引數清單可以是空的；在這種情況下，只要寫 `()`，而不是 `(*)`。（PostgreSQL 實際上兩種寫法都接受，但只有第一種符合 SQL 標準。）

<a id="id-1.5.3.6.15.14.1"></a>
以下是有序集合彙總函式呼叫的範例：

```

SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY income) FROM households;
 percentile_cont
-----------------
           50489
```

這會取得資料表 `households` 中 `income` 欄位的第 50 百分位數，也就是中位數。這裡的 `0.5` 是直接引數；讓百分位數比例成為在各資料列之間變動的值是沒有意義的。

如果指定了 `FILTER`，那麼只有 *`filter_clause`* 求值為真的輸入資料列才會傳給彙總函式；其他資料列則會被捨棄。例如：

```

SELECT
    count(*) AS unfiltered,
    count(*) FILTER (WHERE i < 5) AS filtered
FROM generate_series(1,10) AS s(i);
 unfiltered | filtered
------------+----------
         10 |        4
(1 row)
```

預先定義的彙總函式說明請參閱[第 9.21 節](../functions/functions-aggregate.md)。使用者也可以加入其他彙總函式。

彙總運算式只能出現在 `SELECT` 指令的結果清單或 `HAVING` 子句中。在其他子句（例如 `WHERE`）中則禁止使用，因為在邏輯上，這些子句會在形成彙總結果之前求值。

當彙總運算式出現在子查詢中時（請參閱[第 4.2.11 節](sql-expressions.md#SQL-SYNTAX-SCALAR-SUBQUERIES)與[第 9.24 節](../functions/functions-subquery.md)），彙總函式通常會在子查詢的資料列上求值。但如果彙總函式的引數（以及 *`filter_clause`*，如果有的話）只包含外層的變數，就會出現例外：此時彙總函式屬於最近的那個外層，並在該查詢的資料列上求值。這時整個彙總運算式對它所在的子查詢而言，就是一個外部參照，並且在該子查詢的任何一次求值中都表現得像常數。只能出現在結果清單或 `HAVING` 子句中的限制，是就彙總函式所屬的查詢層級而言。

<a id="SYNTAX-WINDOW-FUNCTIONS"></a>

### 4.2.8. Window 函式呼叫 [#](#SYNTAX-WINDOW-FUNCTIONS)

<a id="id-1.5.3.6.16.2"></a><a id="id-1.5.3.6.16.3"></a>

*window 函式呼叫*（window function call）代表在查詢所選取資料列的某個部分上，套用一個類似彙總的函式。與非 window 的彙總呼叫不同，它並不會將所選取的資料列分組為單一輸出資料列；每一筆資料列在查詢輸出中都保持獨立。不過，window 函式可以存取依照 window 函式呼叫的分組規格（`PARTITION BY` 清單），屬於目前資料列所在群組的所有資料列。window 函式呼叫的語法是下列其中之一：

```

function_name ([expression [, expression ... ]]) [ FILTER ( WHERE filter_clause ) ] OVER window_name
function_name ([expression [, expression ... ]]) [ FILTER ( WHERE filter_clause ) ] OVER ( window_definition )
function_name ( * ) [ FILTER ( WHERE filter_clause ) ] OVER window_name
function_name ( * ) [ FILTER ( WHERE filter_clause ) ] OVER ( window_definition )
```

其中 *`window_definition`* 的語法是

```

[ existing_window_name ]
[ PARTITION BY expression [, ...] ]
[ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
[ frame_clause ]
```

選用的 *`frame_clause`* 可以是下列其中之一

```

{ RANGE | ROWS | GROUPS } frame_start [ frame_exclusion ]
{ RANGE | ROWS | GROUPS } BETWEEN frame_start AND frame_end [ frame_exclusion ]
```

其中 *`frame_start`* 與 *`frame_end`* 可以是下列其中之一

```

UNBOUNDED PRECEDING
offset PRECEDING
CURRENT ROW
offset FOLLOWING
UNBOUNDED FOLLOWING
```

而 *`frame_exclusion`* 可以是下列其中之一

```

EXCLUDE CURRENT ROW
EXCLUDE GROUP
EXCLUDE TIES
EXCLUDE NO OTHERS
```

這裡的 *`expression`* 代表本身不包含 window 函式呼叫的任何值運算式。

*`window_name`* 是對查詢的 `WINDOW` 子句中所定義之具名視窗規格的參照。另外，也可以在括號中提供完整的 *`window_definition`*，其語法與在 `WINDOW` 子句中定義具名視窗的語法相同；詳情請參閱 [SELECT](../../reference/sql-commands/sql-select.md) 參考頁面。值得指出的是，`OVER wname` 並不完全等同於 `OVER (wname ...)`；後者意味著複製並修改視窗定義，而如果所參照的視窗規格包含框架子句，後者就會被拒絕。

`PARTITION BY` 子句會將查詢的資料列分組成若干*分割區*（partition），由 window 函式分別處理。`PARTITION BY` 的運作方式與查詢層級的 `GROUP BY` 子句類似，只是其中的運算式永遠只能是運算式，不能是輸出欄位的名稱或編號。沒有 `PARTITION BY` 時，查詢產生的所有資料列會被視為單一分割區。`ORDER BY` 子句決定 window 函式處理分割區中資料列的順序。它的運作方式與查詢層級的 `ORDER BY` 子句類似，但同樣不能使用輸出欄位的名稱或編號。沒有 `ORDER BY` 時，資料列會以未指定的順序處理。

*`frame_clause`* 指定構成*視窗框架*（window frame）的資料列集合；對於作用在框架上而不是整個分割區上的 window 函式而言，視窗框架是目前分割區的子集合。框架中的資料列集合會依哪一筆是目前資料列而有所不同。框架可以用 `RANGE`、`ROWS` 或 `GROUPS` 模式指定；在每一種模式下，框架都是從 *`frame_start`* 延伸到 *`frame_end`*。如果省略 *`frame_end`*，結尾預設為 `CURRENT ROW`。

*`frame_start`* 為 `UNBOUNDED PRECEDING` 表示框架從分割區的第一筆資料列開始；同樣地，*`frame_end`* 為 `UNBOUNDED FOLLOWING` 表示框架在分割區的最後一筆資料列結束。

在 `RANGE` 或 `GROUPS` 模式下，*`frame_start`* 為 `CURRENT ROW` 表示框架從目前資料列的第一筆*同儕*（peer）資料列開始（也就是 window 的 `ORDER BY` 子句排序為與目前資料列相等的資料列），而 *`frame_end`* 為 `CURRENT ROW` 則表示框架在目前資料列的最後一筆同儕資料列結束。在 `ROWS` 模式下，`CURRENT ROW` 就只是指目前資料列。

在 *`offset`* `PRECEDING` 與 *`offset`* `FOLLOWING` 框架選項中，*`offset`* 必須是不包含任何變數、彙總函式或 window 函式的運算式。*`offset`* 的意義取決於框架模式：

* 在 `ROWS` 模式下，*`offset`* 必須產生非 null、非負的整數，而該選項表示框架從目前資料列之前或之後指定數量的資料列處開始或結束。
* 在 `GROUPS` 模式下，*`offset`* 同樣必須產生非 null、非負的整數，而該選項表示框架從目前資料列所屬同儕群組之前或之後指定數量的*同儕群組*（peer group）處開始或結束；同儕群組是在 `ORDER BY` 排序中相等的一組資料列。（要使用 `GROUPS` 模式，視窗定義中必須有 `ORDER BY` 子句。）
* 在 `RANGE` 模式下，這些選項要求 `ORDER BY` 子句恰好指定一個欄位。*`offset`* 指定目前資料列中該欄位的值，與框架中前面或後面資料列中該欄位的值之間的最大差距。*`offset`* 運算式的資料型別會依排序欄位的資料型別而有所不同。對於數值型別的排序欄位，它通常與排序欄位的型別相同；但對於日期時間型別的排序欄位，它是 `interval`。例如，如果排序欄位的型別是 `date` 或 `timestamp`，就可以寫 `RANGE BETWEEN
  '1 day' PRECEDING AND '10 days' FOLLOWING`。
  *`offset`* 仍然必須是非 null 且非負的，不過「非負」的意義取決於它的資料型別。

無論如何，到框架結尾的距離都受限於到分割區結尾的距離，因此對於靠近分割區兩端的資料列，框架中包含的資料列可能會比其他地方少。

請注意，在 `ROWS` 與 `GROUPS` 模式下，`0 PRECEDING` 與 `0 FOLLOWING` 都等同於 `CURRENT ROW`。在 `RANGE` 模式下，只要以適合特定資料型別的方式解讀「零」，這通常也成立。

*`frame_exclusion`* 選項可以將目前資料列周圍的資料列排除在框架之外，即使依照框架開始與框架結束選項它們原本會被包含在內。`EXCLUDE CURRENT ROW` 會將目前資料列排除在框架之外。`EXCLUDE GROUP` 會將目前資料列及其排序同儕排除在框架之外。`EXCLUDE TIES` 會將目前資料列的所有同儕排除在框架之外，但不包括目前資料列本身。`EXCLUDE NO OTHERS` 只是明確指定預設行為，也就是不排除目前資料列或其同儕。

預設的框架選項是 `RANGE UNBOUNDED PRECEDING`，它與 `RANGE BETWEEN UNBOUNDED PRECEDING AND
CURRENT ROW` 相同。有 `ORDER BY` 時，這會將框架設為從分割區開頭到目前資料列最後一個 `ORDER BY` 同儕為止的所有資料列。沒有 `ORDER BY` 時，這表示分割區中的所有資料列都包含在視窗框架中，因為所有資料列都會成為目前資料列的同儕。

限制條件是：*`frame_start`* 不能是 `UNBOUNDED FOLLOWING`，*`frame_end`* 不能是 `UNBOUNDED PRECEDING`，而且在上述 *`frame_start`* 與 *`frame_end`* 選項清單中，*`frame_end`* 的選擇不能比 *`frame_start`* 的選擇出現得更早；例如，`RANGE BETWEEN CURRENT ROW AND offset
PRECEDING` 是不允許的。
但是，例如 `ROWS BETWEEN 7 PRECEDING AND 8
PRECEDING` 則是允許的，即使它永遠不會選取任何資料列。

如果指定了 `FILTER`，那麼只有 *`filter_clause`* 求值為真的輸入資料列才會傳給 window 函式；其他資料列則會被捨棄。只有屬於彙總函式的 window 函式才接受 `FILTER` 子句。

內建的 window 函式說明請參閱[表 9.67](../functions/functions-window.md#FUNCTIONS-WINDOW-TABLE)。使用者也可以加入其他 window 函式。此外，任何內建或使用者自訂的通用或統計彙總函式，都可以作為 window 函式使用。（有序集合與假設集合彙總函式目前無法作為 window 函式使用。）

使用 `*` 的語法用於將無參數的彙總函式當作 window 函式呼叫，例如 `count(*) OVER (PARTITION BY x ORDER BY y)`。星號（`*`）通常不用於 window 專用函式。window 專用函式不允許在函式引數清單中使用 `DISTINCT` 或 `ORDER BY`。

window 函式呼叫只能用在查詢的 `SELECT` 清單與 `ORDER BY` 子句中。

關於 window 函式的更多資訊，請參閱[第 3.5 節](../../tutorial/tutorial-advanced/tutorial-window.md)、[第 9.22 節](../functions/functions-window.md)與[第 7.2.5 節](../queries/queries-table-expressions.md#QUERIES-WINDOW)。

<a id="SQL-SYNTAX-TYPE-CASTS"></a>

### 4.2.9. 型別轉換 [#](#SQL-SYNTAX-TYPE-CASTS)

<a id="id-1.5.3.6.17.2"></a><a id="id-1.5.3.6.17.3"></a><a id="id-1.5.3.6.17.4"></a>

型別轉換指定從一種資料型別到另一種資料型別的轉換。PostgreSQL 接受兩種等價的型別轉換語法：

```

CAST ( expression AS type )
expression::type
```

`CAST` 語法符合 SQL 標準；使用 `::` 的語法則是 PostgreSQL 的歷史用法。

對已知型別的值運算式套用型別轉換時，它代表執行期間的型別轉換。只有在定義了適當的型別轉換運算時，型別轉換才會成功。請注意，這與對常數使用型別轉換有些微的不同，如[第 4.1.2.7 節](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC)所示。對未加修飾的字串字面值套用型別轉換，代表為字面常數值指派初始型別，因此對任何型別都會成功（只要字串字面值的內容是該資料型別可接受的輸入語法）。

如果值運算式必須產生什麼型別沒有歧義（例如，當它被指派給資料表欄位時），通常可以省略明確的型別轉換；在這種情況下，系統會自動套用型別轉換。不過，只有在系統目錄中被標記為「可以隱含套用」的型別轉換，才會自動進行。其他型別轉換必須以明確的型別轉換語法呼叫。這項限制是為了防止令人意外的轉換在不知不覺中被套用。

也可以使用類似函式的語法來指定型別轉換：

```

typename ( expression )
```

不過，這只適用於名稱同時也是有效函式名稱的型別。例如，`double precision` 就不能這樣使用，但等價的 `float8` 則可以。此外，由於語法衝突，`interval`、`time` 與 `timestamp` 這些名稱只有在加上雙引號時才能以這種方式使用。因此，使用類似函式的型別轉換語法會造成不一致，或許應該避免使用。

### 注意

類似函式的語法實際上就只是一個函式呼叫。當使用兩種標準型別轉換語法之一進行執行期間的轉換時，系統會在內部呼叫一個已註冊的函式來執行轉換。依慣例，這些轉換函式的名稱與其輸出型別相同，因此「類似函式的語法」只不過是直接呼叫底層的轉換函式而已。顯然，可攜的應用程式不應該依賴這一點。更多細節請參閱 [CREATE CAST](../../reference/sql-commands/sql-createcast.md)。

<a id="SQL-SYNTAX-COLLATE-EXPRS"></a>

### 4.2.10. 定序運算式 [#](#SQL-SYNTAX-COLLATE-EXPRS)

<a id="id-1.5.3.6.18.2"></a>

`COLLATE` 子句會覆寫運算式的定序（collation）。它附加在所要套用的運算式之後：

```

expr COLLATE collation
```

其中 *`collation`* 是可能以 schema 限定的識別字。`COLLATE` 子句的結合力比運算子強；必要時可以使用括號。

如果沒有明確指定定序，資料庫系統會從運算式中涉及的欄位推導出定序；如果運算式中沒有涉及任何欄位，則預設使用資料庫的預設定序。

`COLLATE` 子句的兩種常見用途，一是覆寫 `ORDER BY` 子句中的排序順序，例如：

```

SELECT a, b, c FROM tbl WHERE ... ORDER BY a COLLATE "C";
```

二是覆寫具有 locale 相關結果之函式或運算子呼叫的定序，例如：

```

SELECT * FROM tbl WHERE a > 'foo' COLLATE "C";
```

請注意，在後一種情況下，`COLLATE` 子句是附加在我們想要影響之運算子的某個輸入引數上。`COLLATE` 子句附加在運算子或函式呼叫的哪一個引數上並不重要，因為運算子或函式所套用的定序是綜合考量所有引數推導出來的，而明確的 `COLLATE` 子句會覆寫所有其他引數的定序。（不過，將不相符的 `COLLATE` 子句附加到多個引數上是錯誤的。更多細節請參閱[第 23.2 節](../../server-administration/charset/collation.md)。）因此，下列寫法會得到與前一個範例相同的結果：

```

SELECT * FROM tbl WHERE a COLLATE "C" > 'foo';
```

但這樣寫則是錯誤的：

```

SELECT * FROM tbl WHERE (a > 'foo') COLLATE "C";
```

因為它試圖將定序套用到 `>` 運算子的結果上，而該結果的資料型別是不可定序的 `boolean`。

<a id="SQL-SYNTAX-SCALAR-SUBQUERIES"></a>

### 4.2.11. 純量子查詢 [#](#SQL-SYNTAX-SCALAR-SUBQUERIES)

<a id="id-1.5.3.6.19.2"></a>

純量子查詢是以括號括住、恰好回傳一筆資料列且只有一個欄位的一般 `SELECT` 查詢。（關於撰寫查詢的資訊，請參閱[第 7 章](../queries/README.md)。）系統會執行該 `SELECT` 查詢，並將回傳的單一值用在外圍的值運算式中。將回傳多筆資料列或多個欄位的查詢當作純量子查詢使用是錯誤的。（但如果在某次特定的執行中，子查詢沒有回傳任何資料列，就不會發生錯誤；純量結果會被視為 null。）子查詢可以參照外圍查詢中的變數，這些變數在子查詢的任何一次求值中都會表現得像常數。其他涉及子查詢的運算式，另請參閱[第 9.24 節](../functions/functions-subquery.md)。

例如，下列查詢會找出每個州人口最多的城市人口數：

```

SELECT name, (SELECT max(pop) FROM cities WHERE cities.state = states.name)
    FROM states;
```

<a id="SQL-SYNTAX-ARRAY-CONSTRUCTORS"></a>

### 4.2.12. 陣列建構子 [#](#SQL-SYNTAX-ARRAY-CONSTRUCTORS)

<a id="id-1.5.3.6.20.2"></a><a id="id-1.5.3.6.20.3"></a>

陣列建構子是一種運算式，會使用其成員元素的值來建立陣列值。簡單的陣列建構子由關鍵字 `ARRAY`、左方括號 `[`、陣列元素值的運算式清單（以逗號分隔），以及最後的右方括號 `]` 組成。例如：

```

SELECT ARRAY[1,2,3+4];
  array
---------
 {1,2,7}
(1 row)
```

預設情況下，陣列元素型別是各成員運算式的共同型別，其決定方式與 `UNION` 或 `CASE` 結構的規則相同（請參閱[第 10.5 節](../typeconv/typeconv-union-case.md)）。你可以明確將陣列建構子轉換為想要的型別來覆寫這一點，例如：

```

SELECT ARRAY[1,2,22.7]::integer[];
  array
----------
 {1,2,23}
(1 row)
```

這與個別將每個運算式轉換為陣列元素型別的效果相同。關於型別轉換的更多資訊，請參閱[第 4.2.9 節](sql-expressions.md#SQL-SYNTAX-TYPE-CASTS)。

多維陣列值可以透過巢狀的陣列建構子來建立。在內層的建構子中，可以省略關鍵字 `ARRAY`。例如，下列兩種寫法會產生相同的結果：

```

SELECT ARRAY[ARRAY[1,2], ARRAY[3,4]];
     array
---------------
 {{1,2},{3,4}}
(1 row)

SELECT ARRAY[[1,2],[3,4]];
     array
---------------
 {{1,2},{3,4}}
(1 row)
```

由於多維陣列必須是矩形的，同一層的內層建構子必須產生維度完全相同的子陣列。套用在外層 `ARRAY` 建構子上的任何型別轉換，都會自動傳播到所有內層建構子。

多維陣列建構子的元素可以是任何能產生適當種類陣列的東西，而不只是子 `ARRAY` 結構。例如：

```

CREATE TABLE arr(f1 int[], f2 int[]);

INSERT INTO arr VALUES (ARRAY[[1,2],[3,4]], ARRAY[[5,6],[7,8]]);

SELECT ARRAY[f1, f2, '{{9,10},{11,12}}'::int[]] FROM arr;
                     array
------------------------------------------------
 {{{1,2},{3,4}},{{5,6},{7,8}},{{9,10},{11,12}}}
(1 row)
```

你可以建構空陣列，但由於不可能有沒有型別的陣列，你必須明確將空陣列轉換為想要的型別。例如：

```

SELECT ARRAY[]::integer[];
 array
-------
 {}
(1 row)
```

也可以從子查詢的結果建構陣列。在這種形式中，陣列建構子寫成關鍵字 `ARRAY` 後面接著以圓括號（而非方括號）括住的子查詢。例如：

```

SELECT ARRAY(SELECT oid FROM pg_proc WHERE proname LIKE 'bytea%');
                              array
------------------------------------------------------------------
 {2011,1954,1948,1952,1951,1244,1950,2005,1949,1953,2006,31,2412}
(1 row)

SELECT ARRAY(SELECT ARRAY[i, i*2] FROM generate_series(1,5) AS a(i));
              array
----------------------------------
 {{1,2},{2,4},{3,6},{4,8},{5,10}}
(1 row)
```

子查詢必須回傳單一欄位。如果子查詢的輸出欄位是非陣列型別，產生的一維陣列會為子查詢結果的每一筆資料列包含一個元素，而元素型別與子查詢輸出欄位的型別相符。如果子查詢的輸出欄位是陣列型別，結果會是相同型別但維度多一層的陣列；在這種情況下，所有子查詢資料列都必須產生維度相同的陣列，否則結果就不會是矩形的。

以 `ARRAY` 建立的陣列值，其下標一律從一開始。關於陣列的更多資訊，請參閱[第 8.15 節](../datatype/arrays.md)。

<a id="SQL-SYNTAX-ROW-CONSTRUCTORS"></a>

### 4.2.13. 資料列建構子 [#](#SQL-SYNTAX-ROW-CONSTRUCTORS)

<a id="id-1.5.3.6.21.2"></a><a id="id-1.5.3.6.21.3"></a><a id="id-1.5.3.6.21.4"></a>

資料列建構子是一種運算式，會使用其成員欄位的值來建立資料列值（也稱為複合值）。資料列建構子由關鍵字 `ROW`、左括號、零個或多個資料列欄位值的運算式（以逗號分隔），以及最後的右括號組成。例如：

```

SELECT ROW(1,2.5,'this is a test');
```

當清單中有多個運算式時，關鍵字 `ROW` 是選用的。

資料列建構子可以包含 *`rowvalue`*`.*` 語法，它會展開為該資料列值的元素清單，就如同在 `SELECT` 清單的最上層使用 `.*` 語法時一樣（請參閱[第 8.16.5 節](../datatype/rowtypes.md#ROWTYPES-USAGE)）。例如，如果資料表 `t` 有欄位 `f1` 與 `f2`，下列兩者是相同的：

```

SELECT ROW(t.*, 42) FROM t;
SELECT ROW(t.f1, t.f2, 42) FROM t;
```

### 注意

在 PostgreSQL 8.2 之前，資料列建構子中的 `.*` 語法不會展開，因此寫 `ROW(t.*, 42)` 會建立一個具有兩個欄位的資料列，其第一個欄位是另一個資料列值。新的行為通常比較有用。如果你需要舊有的巢狀資料列值行為，請將內層的資料列值寫成不含 `.*` 的形式，例如 `ROW(t, 42)`。

預設情況下，`ROW` 運算式所建立的值是匿名的 record 型別。必要時，可以將它轉換為具名的複合型別，也就是資料表的資料列型別，或是以 `CREATE TYPE AS` 建立的複合型別。可能需要明確的型別轉換來避免歧義。例如：

```

CREATE TABLE mytable(f1 int, f2 float, f3 text);

CREATE FUNCTION getf1(mytable) RETURNS int AS 'SELECT $1.f1' LANGUAGE SQL;

-- No cast needed since only one getf1() exists
SELECT getf1(ROW(1,2.5,'this is a test'));
 getf1
-------
     1
(1 row)

CREATE TYPE myrowtype AS (f1 int, f2 text, f3 numeric);

CREATE FUNCTION getf1(myrowtype) RETURNS int AS 'SELECT $1.f1' LANGUAGE SQL;

-- Now we need a cast to indicate which function to call:
SELECT getf1(ROW(1,2.5,'this is a test'));
ERROR:  function getf1(record) is not unique

SELECT getf1(ROW(1,2.5,'this is a test')::mytable);
 getf1
-------
     1
(1 row)

SELECT getf1(CAST(ROW(11,'this is a test',2.5) AS myrowtype));
 getf1
-------
    11
(1 row)
```

資料列建構子可以用來建立要儲存在複合型別資料表欄位中的複合值，或是傳給接受複合參數的函式。此外，也可以使用[第 9.2 節](../functions/functions-comparison.md)所述的標準比較運算子來測試資料列，如[第 9.25 節](../functions/functions-comparisons.md)所述將一筆資料列與另一筆資料列比較，以及如[第 9.24 節](../functions/functions-subquery.md)所述搭配子查詢使用。

<a id="SYNTAX-EXPRESS-EVAL"></a>

### 4.2.14. 運算式求值規則 [#](#SYNTAX-EXPRESS-EVAL)

<a id="id-1.5.3.6.22.2"></a>

子運算式的求值順序是沒有定義的。特別是，運算子或函式的輸入不一定會由左至右或以任何其他固定的順序求值。

此外，如果只求值運算式的某些部分就能決定其結果，其他子運算式可能根本不會被求值。例如，如果寫成：

```

SELECT true OR somefunc();
```

那麼 `somefunc()`（很可能）根本不會被呼叫。如果寫成下面這樣，也會是同樣的情形：

```

SELECT somefunc() OR true;
```

請注意，這與某些程式語言中布林運算子由左至右的「短路求值」（short-circuiting）並不相同。

因此，在複雜的運算式中使用具有副作用的函式是不明智的。在 `WHERE` 與 `HAVING` 子句中依賴副作用或求值順序特別危險，因為在制定執行計畫的過程中，這些子句會被大量地重新處理。這些子句中的布林運算式（`AND`/`OR`/`NOT` 組合）可能會以布林代數定律所允許的任何方式重新組織。

當必須強制求值順序時，可以使用 `CASE` 結構（請參閱[第 9.18 節](../functions/functions-conditional.md)）。例如，下面這種試圖在 `WHERE` 子句中避免除以零的方式是不可靠的：

```

SELECT ... WHERE x > 0 AND y/x > 1.5;
```

但這樣寫是安全的：

```

SELECT ... WHERE CASE WHEN x > 0 THEN y/x > 1.5 ELSE false END;
```

以這種方式使用的 `CASE` 結構會使最佳化的嘗試失效，因此只應在必要時使用。（在這個特定的例子中，最好改寫成 `y > 1.5*x` 來迴避這個問題。）

不過，`CASE` 並不是解決這類問題的萬靈丹。上述技巧的一個限制是，它無法防止常數子運算式被提早求值。如[第 36.7 節](../../server-programming/extend/xfunc-volatility.md)所述，標記為 `IMMUTABLE` 的函式與運算子，可能會在規劃查詢時就被求值，而不是在執行時。因此，例如

```

SELECT CASE WHEN x > 0 THEN x ELSE 1/0 END FROM tab;
```

很可能會因為規劃器試圖簡化常數子運算式而導致除以零的錯誤，即使資料表中的每一筆資料列都滿足 `x > 0`，使得執行時永遠不會進入 `ELSE` 分支也一樣。

雖然這個特定的例子看起來可能很傻，但在函式中執行的查詢，可能會出現不那麼明顯涉及常數的相關情況，因為函式引數與區域變數的值，可能會為了規劃而以常數的形式插入查詢中。例如，在 PL/pgSQL 函式中，使用 `IF`-`THEN`-`ELSE` 陳述式來保護有風險的計算，會比單純將它包在 `CASE` 運算式中安全得多。

另一個同類型的限制是，`CASE` 無法阻止其中所包含的彙總運算式被求值，因為彙總運算式會在考量 `SELECT` 清單或 `HAVING` 子句中的其他運算式之前就先計算。例如，下列查詢看似已經防範了除以零的情況，卻仍然可能造成除以零的錯誤：

```

SELECT CASE WHEN min(employees) > 0
            THEN avg(expenses / employees)
       END
    FROM departments;
```

`min()` 與 `avg()` 彙總函式會同時在所有輸入資料列上計算，因此只要有任何一筆資料列的 `employees` 等於零，就會在有機會測試 `min()` 的結果之前發生除以零的錯誤。請改用 `WHERE` 或 `FILTER` 子句，從一開始就防止有問題的輸入資料列進入彙總函式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-expressions.html)（原文版本：18.6；核對日期：2026-09-11）
