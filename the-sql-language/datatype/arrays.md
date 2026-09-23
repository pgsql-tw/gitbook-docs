<a id="ARRAYS"></a>
## 8.15. 陣列 [#](#ARRAYS)

[8.15.1. 陣列型別的宣告](arrays.md#ARRAYS-DECLARATION)

[8.15.2. 陣列值輸入](arrays.md#ARRAYS-INPUT)

[8.15.3. 存取陣列](arrays.md#ARRAYS-ACCESSING)

[8.15.4. 修改陣列](arrays.md#ARRAYS-MODIFYING)

[8.15.5. 在陣列中搜尋](arrays.md#ARRAYS-SEARCHING)

[8.15.6. 陣列輸出入語法](arrays.md#ARRAYS-IO)

<a id="id-1.5.7.23.2"></a>

PostgreSQL 允許將資料表的欄位，
定義為可變長度的多維陣列。可以建立任何
內建或使用者自訂的基礎型別、列舉型別、複合型別、範圍型別，
或網域的陣列。

<a id="ARRAYS-DECLARATION"></a>

### 8.15.1. 陣列型別的宣告 [#](#ARRAYS-DECLARATION)

<a id="id-1.5.7.23.4.2"></a>

為了說明陣列型別的用法，我們建立這個資料表：

```

CREATE TABLE sal_emp (
    name            text,
    pay_by_quarter  integer[],
    schedule        text[][]
);
```

如上所示，陣列資料型別的命名方式，是在陣列元素的
資料型別名稱後面，加上方括號
（`[]`）。上述指令，會建立一個名為
`sal_emp` 的資料表，其中包含一個
`text` 型別的欄位（`name`）、
一個 `integer` 型別的一維陣列
（`pay_by_quarter`），代表
員工每一季的薪資，以及一個
`text` 型別的二維陣列（`schedule`），
代表員工每週的排班表。

`CREATE TABLE` 的語法，允許指定陣列的
確切大小，舉例來說：

```

CREATE TABLE tictactoe (
    squares   integer[3][3]
);
```

不過，目前的實作，會忽略任何給定的陣列大小
限制，也就是說，其行為與未指定長度的陣列
相同。

目前的實作，同樣也不會強制執行宣告的
維度數量。特定元素型別的陣列，
無論大小或維度數量為何，
都被視為相同的型別。因此，在
`CREATE TABLE` 中宣告陣列大小或維度數量，
單純只是文件用途；並不會影響執行時期的行為。

對於一維陣列，也可以使用另一種語法，
使用關鍵字 `ARRAY`，以符合 SQL 標準。
`pay_by_quarter` 原本也可以定義為：

```

    pay_by_quarter  integer ARRAY[4],
```

或者，若不指定陣列大小：

```

    pay_by_quarter  integer ARRAY,
```

不過，與先前相同，PostgreSQL 在任何情況下，
都不會強制執行大小限制。

<a id="ARRAYS-INPUT"></a>

### 8.15.2. 陣列值輸入 [#](#ARRAYS-INPUT)

<a id="id-1.5.7.23.5.2"></a>

要將陣列值寫成一個常值，
請將元素值放在大括號內，並以逗號分隔。
（若您懂 C 語言，這與 C 語言初始化結構的
語法有點類似。）您可以在任何元素值外
加上雙引號，若該元素值中包含逗號或大括號，
則必須這麼做。（更多細節
於下文說明。）因此，陣列常值的一般格式如下：

```

'{ val1 delim val2 delim ... }'
```

其中 *`delim`* 是該型別的分隔符字元，
記錄在其 `pg_type` 項目中。
在 PostgreSQL 發行版本所提供的
標準資料型別中，除了 `box` 型別
使用分號（`;`）之外，其餘全部使用逗號
（`,`）。每個 *`val`*，
可以是陣列元素型別的常數，也可以是子陣列。以下是
陣列常值的一個範例：

```

'{{1,2,3},{4,5,6},{7,8,9}}'
```

這個常值是一個二維、3x3 的陣列，
由三個整數子陣列組成。

若要將陣列常值中的某個元素設為 NULL，
請為該元素值寫上 `NULL`（`NULL` 的任何大小寫
變體皆可）。若您想要的是實際的字串值
「NULL」，則必須在它外面加上雙引號。

（這類陣列常值，實際上只是
[4.1.2.7 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC)中所討論的
通用型別常值的一個特例。該常值一開始，
會被當作字串處理，並傳遞給陣列輸入轉換
常式。可能需要明確的型別指定。）

現在我們可以展示一些 `INSERT` 陳述式：

```

INSERT INTO sal_emp
    VALUES ('Bill',
    '{10000, 10000, 10000, 10000}',
    '{{"meeting", "lunch"}, {"training", "presentation"}}');

INSERT INTO sal_emp
    VALUES ('Carol',
    '{20000, 25000, 25000, 25000}',
    '{{"breakfast", "consulting"}, {"meeting", "lunch"}}');
```

前面這兩則插入指令的結果，看起來像這樣：

```

SELECT * FROM sal_emp;
 name  |      pay_by_quarter       |                 schedule
-------+---------------------------+-------------------------------------------
 Bill  | {10000,10000,10000,10000} | {{meeting,lunch},{training,presentation}}
 Carol | {20000,25000,25000,25000} | {{breakfast,consulting},{meeting,lunch}}
(2 rows)
```

多維陣列的每個維度，其範圍必須相符。
不相符會導致錯誤，舉例來說：

```

INSERT INTO sal_emp
    VALUES ('Bill',
    '{10000, 10000, 10000, 10000}',
    '{{"meeting", "lunch"}, {"meeting"}}');
ERROR:  malformed array literal: "{{"meeting", "lunch"}, {"meeting"}}"
DETAIL:  Multidimensional arrays must have sub-arrays with matching dimensions.
```

也可以使用 `ARRAY` 建構子語法：

```

INSERT INTO sal_emp
    VALUES ('Bill',
    ARRAY[10000, 10000, 10000, 10000],
    ARRAY[['meeting', 'lunch'], ['training', 'presentation']]);

INSERT INTO sal_emp
    VALUES ('Carol',
    ARRAY[20000, 25000, 25000, 25000],
    ARRAY[['breakfast', 'consulting'], ['meeting', 'lunch']]);
```

請注意，陣列元素是一般的 SQL 常數或
運算式；舉例來說，字串常值使用單引號，
而不像陣列常值那樣使用雙引號。
[4.2.12 節](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS)中，
對 `ARRAY` 建構子語法有更詳細的討論。

<a id="ARRAYS-ACCESSING"></a>

### 8.15.3. 存取陣列 [#](#ARRAYS-ACCESSING)

<a id="id-1.5.7.23.6.2"></a>

現在，我們可以對這個資料表執行一些查詢。
首先，我們展示如何存取陣列的單一元素。
以下查詢，會取回第二季薪資有變動的
員工姓名：

```

SELECT name FROM sal_emp WHERE pay_by_quarter[1] <> pay_by_quarter[2];

 name
-------
 Carol
(1 row)
```

陣列下標編號，寫在方括號內。
預設情況下，PostgreSQL 對陣列
採用從 1 開始編號的慣例，也就是說，
一個有 *`n`* 個元素的陣列，
從 `array[1]` 開始，到 `array[n]` 結束。

以下查詢，會取回所有員工的第三季薪資：

```

SELECT pay_by_quarter[3] FROM sal_emp;

 pay_by_quarter
----------------
          10000
          25000
(2 rows)
```

我們也可以存取陣列任意的矩形切片，
也就是子陣列。陣列切片，
是透過為一個或多個陣列維度，
寫上 `lower-bound:upper-bound` 來表示的。舉例來說，
以下查詢，會取回 Bill 排班表中，
一週前兩天的第一項：

```

SELECT schedule[1:2][1:1] FROM sal_emp WHERE name = 'Bill';

        schedule
------------------------
 {{meeting},{training}}
(1 row)
```

若任何一個維度，被寫成切片形式，
也就是包含冒號，則所有維度，
都會被視為切片。任何只有單一數字
（沒有冒號）的維度，都會被視為從 1
到指定數字。舉例來說，`[2]` 會被視為
`[1:2]`，如以下範例所示：

```

SELECT schedule[1:2][2] FROM sal_emp WHERE name = 'Bill';

                 schedule
-------------------------------------------
 {{meeting,lunch},{training,presentation}}
(1 row)
```

為了避免與非切片情況混淆，最好對所有維度，
都使用切片語法，例如 `[1:2][1:1]`，
而不要用 `[2][1:1]`。

在切片指定符中，*`lower-bound`* 及／或
*`upper-bound`* 都可以省略；
缺少的邊界，會被替換為該陣列下標的
下限或上限。舉例來說：

```

SELECT schedule[:2][2:] FROM sal_emp WHERE name = 'Bill';

        schedule
------------------------
 {{lunch},{presentation}}
(1 row)

SELECT schedule[:][1:1] FROM sal_emp WHERE name = 'Bill';

        schedule
------------------------
 {{meeting},{training}}
(1 row)
```

若陣列本身，或任何一個下標運算式為 null，
則陣列下標運算式會傳回 null。此外，
若下標超出陣列邊界，
也會傳回 null（這種情況不會引發錯誤）。
舉例來說，若 `schedule`
目前的維度是 `[1:3][1:2]`，那麼參照
`schedule[3][3]`，就會得到 NULL。同樣地，
下標數量錯誤的陣列參照，
也會得到 null，而不是錯誤。

若陣列本身，或任何一個下標運算式為 null，
陣列切片運算式同樣也會得到 null。不過，
在其他情況下，例如選取的陣列切片
完全落在目前陣列邊界之外，
切片運算式會得到一個空的（零維）陣列，
而不是 null。（這與非切片的行為不符，
是基於歷史因素而如此。）若要求的切片，
與陣列邊界部分重疊，則它會被悄悄地
縮減為僅重疊的區域，而不是傳回 null。

任何陣列值目前的維度，都可以透過
`array_dims` 函式取回：

```

SELECT array_dims(schedule) FROM sal_emp WHERE name = 'Carol';

 array_dims
------------
 [1:2][1:2]
(1 row)
```

`array_dims` 會產生一個 `text` 結果，
這對人類閱讀而言很方便，但對程式而言，
可能不太方便。維度也可以透過
`array_upper` 與 `array_lower` 取回，
它們分別會傳回
指定陣列維度的上限與下限：

```

SELECT array_upper(schedule, 1) FROM sal_emp WHERE name = 'Carol';

 array_upper
-------------
           2
(1 row)
```

`array_length` 會傳回指定
陣列維度的長度：

```

SELECT array_length(schedule, 1) FROM sal_emp WHERE name = 'Carol';

 array_length
--------------
            2
(1 row)
```

`cardinality` 會傳回某個陣列，
跨所有維度的元素總數。它實際上，等同於
呼叫 `unnest` 所會產生的資料列數：

```

SELECT cardinality(schedule) FROM sal_emp WHERE name = 'Carol';

 cardinality
-------------
           4
(1 row)
```

<a id="ARRAYS-MODIFYING"></a>

### 8.15.4. 修改陣列 [#](#ARRAYS-MODIFYING)

<a id="id-1.5.7.23.7.2"></a>

可以完全取代一個陣列值：

```

UPDATE sal_emp SET pay_by_quarter = '{25000,25000,27000,27000}'
    WHERE name = 'Carol';
```

或使用 `ARRAY` 運算式語法：

```

UPDATE sal_emp SET pay_by_quarter = ARRAY[25000,25000,27000,27000]
    WHERE name = 'Carol';
```

也可以在單一元素上更新陣列：

```

UPDATE sal_emp SET pay_by_quarter[4] = 15000
    WHERE name = 'Bill';
```

或在一個切片上更新：

```

UPDATE sal_emp SET pay_by_quarter[1:2] = '{27000,27000}'
    WHERE name = 'Carol';
```

省略 *`lower-bound`* 及／或
*`upper-bound`* 的切片語法，
也同樣可以使用，但僅限於更新的陣列值
不是 NULL 或零維的情況（否則，
就沒有既有的下標限制可供替代）。

透過指定給尚未存在的元素，
可以擴大已儲存的陣列值。原本已存在的位置，
與新指定元素之間的任何位置，都會被填入
null。舉例來說，若陣列
`myarray` 目前有 4 個元素，
在一次指定給 `myarray[6]` 的更新之後，
它就會有六個元素；
`myarray[5]` 會包含 null。
目前，以這種方式擴大，僅適用於一維
陣列，不適用於多維陣列。

帶下標的指定，允許建立不使用從 1 開始
下標的陣列。舉例來說，可以指定給
`myarray[-2:7]`，
建立一個下標值從 -2 到 7 的陣列。

也可以使用串接運算子
`||`，來建構新的陣列值：

```

SELECT ARRAY[1,2] || ARRAY[3,4];
 ?column?
-----------
 {1,2,3,4}
(1 row)

SELECT ARRAY[5,6] || ARRAY[[1,2],[3,4]];
      ?column?
---------------------
 {{5,6},{1,2},{3,4}}
(1 row)
```

串接運算子，允許將單一元素
加入一維陣列的開頭或結尾。它也接受兩個
*`N`* 維陣列，或一個 *`N`* 維陣列
與一個 *`N+1`* 維陣列。

當單一元素，被推入一維陣列的開頭
或結尾時，結果會是一個與該陣列運算元
下限下標相同的陣列。舉例來說：

```

SELECT array_dims(1 || '[0:1]={2,3}'::int[]);
 array_dims
------------
 [0:2]
(1 row)

SELECT array_dims(ARRAY[1,2] || 3);
 array_dims
------------
 [1:3]
(1 row)
```

當兩個維度數量相同的陣列被串接時，
結果會保留左側運算元外層維度的
下限下標。結果是一個陣列，
包含左側運算元的每一個元素，
後面接著右側運算元的每一個元素。舉例來說：

```

SELECT array_dims(ARRAY[1,2] || ARRAY[3,4,5]);
 array_dims
------------
 [1:5]
(1 row)

SELECT array_dims(ARRAY[[1,2],[3,4]] || ARRAY[[5,6],[7,8],[9,0]]);
 array_dims
------------
 [1:5][1:2]
(1 row)
```

當一個 *`N`* 維陣列，
被推入一個 *`N+1`* 維陣列的開頭
或結尾時，結果類似上面所述的元素-陣列情況。
每個 *`N`* 維子陣列，
基本上就是 *`N+1`* 維
陣列外層維度中的一個元素。舉例來說：

```

SELECT array_dims(ARRAY[1,2] || ARRAY[[3,4],[5,6]]);
 array_dims
------------
 [1:3][1:2]
(1 row)
```

也可以使用函式
`array_prepend`、`array_append`
或 `array_cat` 來建構陣列。前兩個函式，
只支援一維陣列，但 `array_cat`
則支援多維陣列。
以下是一些範例：

```

SELECT array_prepend(1, ARRAY[2,3]);
 array_prepend
---------------
 {1,2,3}
(1 row)

SELECT array_append(ARRAY[1,2], 3);
 array_append
--------------
 {1,2,3}
(1 row)

SELECT array_cat(ARRAY[1,2], ARRAY[3,4]);
 array_cat
-----------
 {1,2,3,4}
(1 row)

SELECT array_cat(ARRAY[[1,2],[3,4]], ARRAY[5,6]);
      array_cat
---------------------
 {{1,2},{3,4},{5,6}}
(1 row)

SELECT array_cat(ARRAY[5,6], ARRAY[[1,2],[3,4]]);
      array_cat
---------------------
 {{5,6},{1,2},{3,4}}
```

在簡單的情況下，比起直接使用這些函式，
更偏好使用上面所討論的串接運算子。不過，
由於串接運算子被多載以服務全部三種情況，
在某些情況下，使用其中一個函式，
有助於避免歧義。舉例來說，請考慮：

```

SELECT ARRAY[1, 2] || '{3, 4}';  -- the untyped literal is taken as an array
 ?column?
-----------
 {1,2,3,4}

SELECT ARRAY[1, 2] || '7';                 -- so is this one
ERROR:  malformed array literal: "7"

SELECT ARRAY[1, 2] || NULL;                -- so is an undecorated NULL
 ?column?
----------
 {1,2}
(1 row)

SELECT array_append(ARRAY[1, 2], NULL);    -- this might have been meant
 array_append
--------------
 {1,2,NULL}
```

在上面的範例中，剖析器看到串接運算子
一側是整數陣列，另一側是型別未定的
常數。它用來解析該常數型別的推斷做法，
是假設它與運算子另一個輸入的型別相同 —
在這個例子中，也就是整數陣列。因此，
串接運算子，會被假定為代表
`array_cat`，而不是 `array_append`。當
這是錯誤的選擇時，可以透過將該常數轉型為
該陣列的元素型別來修正；但明確使用
`array_append`，可能是比較好的解法。

<a id="ARRAYS-SEARCHING"></a>

### 8.15.5. 在陣列中搜尋 [#](#ARRAYS-SEARCHING)

<a id="id-1.5.7.23.8.2"></a>

要在陣列中搜尋某個值，必須逐一檢查每個值。
若您知道該陣列的大小，這可以手動完成。
舉例來說：

```

SELECT * FROM sal_emp WHERE pay_by_quarter[1] = 10000 OR
                            pay_by_quarter[2] = 10000 OR
                            pay_by_quarter[3] = 10000 OR
                            pay_by_quarter[4] = 10000;
```

不過，對於大型陣列而言，這很快就會變得繁瑣，
而且若陣列大小未知，這種做法也沒有幫助。
[9.25 節](../functions/functions-comparisons.md)中，
說明了另一種做法。上面的
查詢，可以改寫成：

```

SELECT * FROM sal_emp WHERE 10000 = ANY (pay_by_quarter);
```

此外，您也可以用以下方式，
找出陣列中所有值都等於 10000 的資料列：

```

SELECT * FROM sal_emp WHERE 10000 = ALL (pay_by_quarter);
```

另一種做法，是使用 `generate_subscripts` 函式。
舉例來說：

```

SELECT * FROM
   (SELECT pay_by_quarter,
           generate_subscripts(pay_by_quarter, 1) AS s
      FROM sal_emp) AS foo
 WHERE pay_by_quarter[s] = 10000;
```

這個函式，說明於[表 9.70](../functions/functions-srf.md#FUNCTIONS-SRF-SUBSCRIPTS)中。

您也可以使用 `&&` 運算子來搜尋陣列，
該運算子會檢查左運算元，
是否與右運算元重疊。舉例來說：

```

SELECT * FROM sal_emp WHERE pay_by_quarter && ARRAY[10000];
```

關於這個運算子及其他陣列運算子的更多說明，
請見[9.19 節](../functions/functions-array.md)。可以透過適當的
索引來加速這類搜尋，說明請見[11.2 節](../indexes/indexes-types.md)。

您也可以使用 `array_position`
與 `array_positions` 函式，
在陣列中搜尋特定的值。前者會傳回
某個值在陣列中第一次出現的下標；後者
會傳回一個陣列，其中包含該值在陣列中
所有出現位置的下標。舉例來說：

```

SELECT array_position(ARRAY['sun','mon','tue','wed','thu','fri','sat'], 'mon');
 array_position
----------------
              2
(1 row)

SELECT array_positions(ARRAY[1, 4, 3, 1, 3, 4, 2, 1], 1);
 array_positions
-----------------
 {1,4,8}
(1 row)
```

### 提示

陣列並非集合；若需要搜尋特定的陣列元素，
這可能是資料庫設計不當的一個徵兆。請考慮
改用一個獨立的資料表，其中每一列，
對應到原本會作為陣列元素的一個項目。
這樣會更容易搜尋，
對於大量元素而言，也可能有較好的擴充性。

<a id="ARRAYS-IO"></a>

### 8.15.6. 陣列輸出入語法 [#](#ARRAYS-IO)

<a id="id-1.5.7.23.9.2"></a>

陣列值的外部文字表示法，
是由依照該陣列元素型別的輸出入轉換規則
解讀的項目所組成，再加上用來表示陣列結構的
裝飾符號。這些裝飾符號，
包括陣列值外圍的大括號（`{` 與 `}`），
以及相鄰項目之間的分隔符字元。
分隔符字元通常是逗號（`,`），
但也可以是其他字元：這是由該陣列
元素型別的 `typdelim` 設定所決定的。
在 PostgreSQL 發行版本所提供的
標準資料型別中，除了 `box` 型別
使用分號（`;`）之外，其餘全部使用逗號。
在多維陣列中，每個維度（列、平面、
立方體等）都有自己一層的大括號，
且分隔符必須寫在同一層相鄰的
大括號實體之間。

若陣列元素值是空字串、包含大括號、
分隔符字元、雙引號、反斜線或空白，
或符合單字 `NULL`，
陣列輸出常式會在該元素值外圍加上雙引號。
元素值中內嵌的雙引號與反斜線，
會以反斜線逸出。對於數值資料型別而言，
可以安全地假設不會出現雙引號，但對於文字
資料型別，則應該做好準備，因應有無引號的
兩種情況。

預設情況下，陣列維度的下限索引值，
設定為 1。若要表示下限不同的陣列，
可以在陣列內容之前，明確指定
陣列下標範圍。
這種裝飾符號，
是在每個陣列維度的下限與上限外圍，
加上方括號（`[]`），中間以
冒號（`:`）分隔符字元隔開。
陣列維度裝飾符號之後，會接著一個等號（`=`）。
舉例來說：

```

SELECT f1[1][-2][3] AS e1, f1[1][-1][5] AS e2
 FROM (SELECT '[1:1][-2:-1][3:5]={{{1,2,3},{4,5,6}}}'::int[] AS f1) AS ss;

 e1 | e2
----+----
  1 |  6
(1 row)
```

只有在存在一個或多個不等於 1 的下限時，
陣列輸出常式才會在其結果中，
包含明確的維度。

若為某個元素所寫入的值是 `NULL`
（任何大小寫變體皆可），該元素會被視為 NULL。
只要出現任何引號或反斜線，
就會停用這項規則，並允許輸入字面上的字串值
「NULL」。此外，為了與 8.2 之前的
PostgreSQL 版本保持向後相容，
可以將 [array_nulls](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-ARRAY-NULLS) 組態參數
關閉（`off`），以抑制將 `NULL`
辨識為 NULL。

如前所示，在寫入陣列值時，
您可以在任何個別的陣列元素外圍，加上雙引號。
若該元素值在其他情況下，
會讓陣列值剖析器感到困惑，您就*必須*這麼做。
舉例來說，包含大括號、逗號（或該資料型別的
分隔符字元）、雙引號、反斜線，或開頭或結尾
空白的元素，都必須加上雙引號。空字串，
以及符合單字 `NULL` 的字串，
同樣也必須加上引號。若要在
帶引號的陣列元素值中，放入雙
引號或反斜線，請在它前面加上反斜線。
另一種做法，是不使用引號，
改用反斜線逸出，來保護所有原本
會被視為陣列語法的資料字元。

您可以在左大括號之前，或右大括號之後，
加上空白。您也可以在任何個別的項目字串
之前或之後，加上空白。在所有這些情況下，
空白都會被忽略。不過，
帶雙引號元素內部的空白，
或某個元素兩側都被非空白字元包圍的空白，
則不會被忽略。

### 提示

在 SQL 指令中撰寫陣列值時，
`ARRAY` 建構子語法（請參閱
[4.2.12 節](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS)），
通常比陣列常值語法更容易使用。在 `ARRAY` 中，
個別的元素值，是以不作為陣列成員時
相同的方式撰寫的。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/arrays.html)（原文版本：18.6；核對日期：2026-09-22）
