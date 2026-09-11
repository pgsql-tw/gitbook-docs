<a id="QUERIES-TABLE-EXPRESSIONS"></a>

## 7.2. 資料表運算式 [#](#QUERIES-TABLE-EXPRESSIONS)

[7.2.1. `FROM` 子句](queries-table-expressions.md#QUERIES-FROM)

[7.2.2. `WHERE` 子句](queries-table-expressions.md#QUERIES-WHERE)

[7.2.3. `GROUP BY` 與 `HAVING` 子句](queries-table-expressions.md#QUERIES-GROUP)

[7.2.4. `GROUPING SETS`、`CUBE` 與 `ROLLUP`](queries-table-expressions.md#QUERIES-GROUPING-SETS)

[7.2.5. Window 函式的處理](queries-table-expressions.md#QUERIES-WINDOW)

<a id="id-1.5.6.6.2"></a>

*資料表運算式*（table expression）會計算出一個資料表。資料表運算式包含一個 `FROM` 子句，後面可以選擇接上 `WHERE`、`GROUP BY` 與 `HAVING` 子句。簡單的資料表運算式只是參照磁碟上的一個資料表，也就是所謂的基本資料表（base table），但更複雜的運算式可以用各種方式修改或組合基本資料表。

資料表運算式中選用的 `WHERE`、`GROUP BY` 與 `HAVING` 子句，指定了一連串對 `FROM` 子句所衍生之資料表依序執行的轉換。所有這些轉換都會產生一個虛擬資料表，提供要傳給選取清單以計算查詢輸出資料列的資料列。

<a id="QUERIES-FROM"></a>

### 7.2.1. `FROM` 子句 [#](#QUERIES-FROM)

[`FROM`](../../reference/sql-commands/sql-select.md#SQL-FROM) 子句會從以逗號分隔的資料表參照清單中所給定的一個或多個其他資料表，衍生出一個資料表。

```

FROM table_reference [, table_reference [, ...]]
```

資料表參照可以是資料表名稱（可能以 schema 限定），或是衍生資料表，例如子查詢、`JOIN` 結構，或這些的複雜組合。如果 `FROM` 子句中列出了多個資料表參照，這些資料表會進行交叉聯結（也就是形成它們資料列的笛卡兒積；見下文）。`FROM` 清單的結果是一個中間的虛擬資料表，接著可以經過 `WHERE`、`GROUP BY` 與 `HAVING` 子句的轉換，最後成為整個資料表運算式的結果。

<a id="id-1.5.6.6.5.3"></a>

當資料表參照所指名的資料表是某個資料表繼承階層的父資料表時，除非資料表名稱前面有關鍵字 `ONLY`，否則該資料表參照不只會產生該資料表的資料列，還會產生其所有後代資料表的資料列。不過，該參照只會產生出現在所指名資料表中的欄位；在子資料表中新增的任何欄位都會被忽略。

除了在資料表名稱前面寫 `ONLY` 之外，你也可以在資料表名稱後面寫 `*`，明確指定要包含後代資料表。現在已經沒有真正的理由再使用這種語法，因為搜尋後代資料表現在一律是預設行為。不過，為了與舊版相容，仍然支援這種語法。

<a id="QUERIES-JOIN"></a>

#### 7.2.1.1. 聯結資料表 [#](#QUERIES-JOIN)

<a id="id-1.5.6.6.5.6.2"></a>

聯結資料表是依照特定聯結類型的規則，從另外兩個（實際或衍生的）資料表衍生出來的資料表。可用的聯結有內部聯結、外部聯結與交叉聯結。聯結資料表的一般語法是

```

T1 join_type T2 [ join_condition ]
```

所有類型的聯結都可以串連起來或巢狀使用：*`T1`* 與 *`T2`* 其中之一或兩者都可以是聯結資料表。可以在 `JOIN` 子句的前後加上括號來控制聯結順序。沒有括號時，`JOIN` 子句會由左至右巢狀結合。

**聯結類型**

交叉聯結 <a id="id-1.5.6.6.5.6.4.2.1.1"></a> <a id="id-1.5.6.6.5.6.4.2.1.2"></a>
:   ```

    T1 CROSS JOIN T2
    ```

    對於 *`T1`* 與 *`T2`* 資料列的每一種可能組合（也就是笛卡兒積），聯結資料表都會包含一筆資料列，由 *`T1`* 的所有欄位接著 *`T2`* 的所有欄位組成。如果兩個資料表分別有 N 筆與 M 筆資料列，聯結資料表就會有 N \* M 筆資料列。

    `FROM T1 CROSS JOIN T2` 等同於 `FROM T1 INNER JOIN T2 ON TRUE`（見下文）。它也等同於 `FROM T1, T2`。

    ### 注意

    當出現兩個以上的資料表時，後一種等價關係並不完全成立，因為 `JOIN` 的結合力比逗號強。例如，`FROM T1 CROSS JOIN T2 INNER JOIN T3 ON condition` 與 `FROM T1, T2 INNER JOIN T3 ON condition` 並不相同，因為在第一種情況下 *`condition`* 可以參照 *`T1`*，但在第二種情況下則不行。

限定聯結 <a id="id-1.5.6.6.5.6.4.3.1.1"></a> <a id="id-1.5.6.6.5.6.4.3.1.2"></a>
:   ```

    T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 ON boolean_expression
    T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 USING ( join column list )
    T1 NATURAL { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2
    ```

    在所有形式中，`INNER` 與 `OUTER` 這兩個字都是選用的。`INNER` 是預設值；`LEFT`、`RIGHT` 與 `FULL` 則表示外部聯結。

    *聯結條件*（join condition）是在 `ON` 或 `USING` 子句中指定的，或由 `NATURAL` 這個字隱含指定。聯結條件決定兩個來源資料表中哪些資料列被視為「相符」，詳細說明如下。

    限定聯結可能的類型有：

    `INNER JOIN`
    :   對於 T1 的每一筆資料列 R1，聯結資料表中會為 T2 中每一筆與 R1 滿足聯結條件的資料列各產生一筆資料列。

    `LEFT OUTER JOIN` <a id="id-1.5.6.6.5.6.4.3.2.4.1.2.1.2"></a> <a id="id-1.5.6.6.5.6.4.3.2.4.1.2.1.3"></a>
    :   首先執行內部聯結。接著，對於 T1 中與 T2 的任何資料列都不滿足聯結條件的每一筆資料列，加入一筆聯結資料列，其中 T2 的欄位為 null 值。因此，對於 T1 中的每一筆資料列，聯結資料表中一定至少有一筆資料列。

    `RIGHT OUTER JOIN` <a id="id-1.5.6.6.5.6.4.3.2.4.1.3.1.2"></a> <a id="id-1.5.6.6.5.6.4.3.2.4.1.3.1.3"></a>
    :   首先執行內部聯結。接著，對於 T2 中與 T1 的任何資料列都不滿足聯結條件的每一筆資料列，加入一筆聯結資料列，其中 T1 的欄位為 null 值。這與左聯結相反：對於 T2 中的每一筆資料列，結果資料表中一定會有一筆資料列。

    `FULL OUTER JOIN`
    :   首先執行內部聯結。接著，對於 T1 中與 T2 的任何資料列都不滿足聯結條件的每一筆資料列，加入一筆聯結資料列，其中 T2 的欄位為 null 值。此外，對於 T2 中與 T1 的任何資料列都不滿足聯結條件的每一筆資料列，也會加入一筆聯結資料列，其中 T1 的欄位為 null 值。

    `ON` 子句是最通用的聯結條件：它接受一個布林值運算式，與 `WHERE` 子句中使用的運算式相同。如果 `ON` 運算式求值為真，*`T1`* 與 *`T2`* 的一對資料列就是相符的。

    `USING` 子句是一種簡寫，讓你可以善用聯結兩側對聯結欄位使用相同名稱的特定情況。它接受一份以逗號分隔的共同欄位名稱清單，並形成一個對每個欄位都進行相等比較的聯結條件。例如，以 `USING (a, b)` 聯結 *`T1`* 與 *`T2`*，會產生聯結條件 `ON T1.a = T2.a AND T1.b = T2.b`。

    此外，`JOIN USING` 的輸出會隱藏多餘的欄位：由於相符的兩個欄位必定具有相同的值，因此沒有必要把兩者都印出來。`JOIN ON` 會產生 *`T1`* 的所有欄位，接著是 *`T2`* 的所有欄位；而 `JOIN USING` 則會為所列出的每一對欄位產生一個輸出欄位（依列出的順序），接著是 *`T1`* 的其餘欄位，再接著是 *`T2`* 的其餘欄位。

    <a id="id-1.5.6.6.5.6.4.3.2.8.1"></a>
    <a id="id-1.5.6.6.5.6.4.3.2.8.2"></a>
    最後，`NATURAL` 是 `USING` 的簡寫形式：它會形成一份 `USING` 清單，由同時出現在兩個輸入資料表中的所有欄位名稱組成。與 `USING` 一樣，這些欄位在輸出資料表中只會出現一次。如果沒有共同的欄位名稱，`NATURAL JOIN` 的行為就與 `CROSS JOIN` 相同。

    ### 注意

    `USING` 對於所聯結關聯的欄位變更相當安全，因為只有列出的欄位會被合併。`NATURAL` 則有相當大的風險，因為任一關聯的任何 schema 變更，只要產生了新的相符欄位名稱，就會導致聯結也將這個新欄位合併進來。

綜合以上所述，假設我們有資料表 `t1`：

```

 num | name
-----+------
   1 | a
   2 | b
   3 | c
```

以及 `t2`：

```

 num | value
-----+-------
   1 | xxx
   3 | yyy
   5 | zzz
```

那麼各種聯結會得到下列結果：

```

=> SELECT * FROM t1 CROSS JOIN t2;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   1 | a    |   3 | yyy
   1 | a    |   5 | zzz
   2 | b    |   1 | xxx
   2 | b    |   3 | yyy
   2 | b    |   5 | zzz
   3 | c    |   1 | xxx
   3 | c    |   3 | yyy
   3 | c    |   5 | zzz
(9 rows)

=> SELECT * FROM t1 INNER JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   3 | c    |   3 | yyy
(2 rows)

=> SELECT * FROM t1 INNER JOIN t2 USING (num);
 num | name | value
-----+------+-------
   1 | a    | xxx
   3 | c    | yyy
(2 rows)

=> SELECT * FROM t1 NATURAL INNER JOIN t2;
 num | name | value
-----+------+-------
   1 | a    | xxx
   3 | c    | yyy
(2 rows)

=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   2 | b    |     |
   3 | c    |   3 | yyy
(3 rows)

=> SELECT * FROM t1 LEFT JOIN t2 USING (num);
 num | name | value
-----+------+-------
   1 | a    | xxx
   2 | b    |
   3 | c    | yyy
(3 rows)

=> SELECT * FROM t1 RIGHT JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   3 | c    |   3 | yyy
     |      |   5 | zzz
(3 rows)

=> SELECT * FROM t1 FULL JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   2 | b    |     |
   3 | c    |   3 | yyy
     |      |   5 | zzz
(4 rows)
```

以 `ON` 指定的聯結條件也可以包含與聯結沒有直接關係的條件。這對某些查詢可能很有用，但需要仔細考慮。例如：

```

=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num AND t2.value = 'xxx';
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   2 | b    |     |
   3 | c    |     |
(3 rows)
```

請注意，將限制條件放在 `WHERE` 子句中會產生不同的結果：

```

=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num WHERE t2.value = 'xxx';
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
(1 row)
```

這是因為放在 `ON` 子句中的限制條件是在聯結*之前*處理的，而放在 `WHERE` 子句中的限制條件則是在聯結*之後*處理的。這對內部聯結沒有影響，但對外部聯結的影響很大。

<a id="QUERIES-TABLE-ALIASES"></a>

#### 7.2.1.2. 資料表與欄位別名 [#](#QUERIES-TABLE-ALIASES)

<a id="id-1.5.6.6.5.7.2"></a><a id="id-1.5.6.6.5.7.3"></a>

可以為資料表與複雜的資料表參照指定一個暫時的名稱，用於在查詢的其餘部分參照該衍生資料表。這稱為*資料表別名*（table alias）。

要建立資料表別名，請寫

```

FROM table_reference AS alias
```

或

```

FROM table_reference alias
```

`AS` 關鍵字是可有可無的。*`alias`* 可以是任何識別字。

資料表別名的一個典型應用，是為很長的資料表名稱指定簡短的識別字，讓聯結子句保持易讀。例如：

```

SELECT * FROM some_very_long_table_name s JOIN another_fairly_long_name a ON s.id = a.num;
```

就目前的查詢而言，別名會成為該資料表參照的新名稱；在查詢的其他地方不允許再以原本的名稱參照該資料表。因此，下列寫法是無效的：

```

SELECT * FROM my_table AS m WHERE my_table.a > 5;    -- wrong
```

資料表別名主要是為了書寫方便，但將資料表與自身聯結時就必須使用別名，例如：

```

SELECT * FROM people AS mother JOIN people AS child ON mother.id = child.mother_id;
```

括號用來解決歧義。在下面的範例中，第一個陳述式將別名 `b` 指派給 `my_table` 的第二個實例，而第二個陳述式則將別名指派給聯結的結果：

```

SELECT * FROM my_table AS a CROSS JOIN my_table AS b ...
SELECT * FROM (my_table AS a CROSS JOIN my_table) AS b ...
```

另一種形式的資料表別名，除了為資料表本身命名之外，也會為資料表的欄位指定暫時的名稱：

```

FROM table_reference [AS] alias ( column1 [, column2 [, ...]] )
```

如果指定的欄位別名比資料表實際的欄位少，其餘的欄位就不會被重新命名。這種語法對於自我聯結或子查詢特別有用。

當別名套用在 `JOIN` 子句的輸出上時，該別名會隱藏 `JOIN` 中的原始名稱。例如：

```

SELECT a.* FROM my_table AS a JOIN your_table AS b ON ...
```

是有效的 SQL，但是：

```

SELECT a.* FROM (my_table AS a JOIN your_table AS b ON ...) AS c
```

則是無效的；資料表別名 `a` 在別名 `c` 之外是看不到的。

<a id="QUERIES-SUBQUERIES"></a>

#### 7.2.1.3. 子查詢 [#](#QUERIES-SUBQUERIES)

<a id="id-1.5.6.6.5.8.2"></a>

指定衍生資料表的子查詢必須以括號括住。可以為它們指定資料表別名，也可以選擇指定欄位別名（如[第 7.2.1.2 節](queries-table-expressions.md#QUERIES-TABLE-ALIASES)所述）。例如：

```

FROM (SELECT * FROM table1) AS alias_name
```

這個範例等同於 `FROM table1 AS alias_name`。當子查詢涉及分組或彙總時，就會出現更有趣、無法簡化為單純聯結的情況。

子查詢也可以是 `VALUES` 清單：

```

FROM (VALUES ('anne', 'smith'), ('bob', 'jones'), ('joe', 'blow'))
     AS names(first, last)
```

同樣地，資料表別名是選用的。為 `VALUES` 清單的欄位指定別名是選用的，但這是良好的做法。更多資訊請參閱[第 7.7 節](queries-values.md)。

依照 SQL 標準，必須為子查詢提供資料表別名名稱。PostgreSQL 允許省略 `AS` 與別名，但在可能移植到其他系統的 SQL 程式碼中，寫上別名是良好的做法。

<a id="QUERIES-TABLEFUNCTIONS"></a>

#### 7.2.1.4. 資料表函式 [#](#QUERIES-TABLEFUNCTIONS)

<a id="id-1.5.6.6.5.9.2"></a><a id="id-1.5.6.6.5.9.3"></a>

資料表函式是產生一組資料列的函式，這些資料列由基本資料型別（純量型別）或複合資料型別（資料表資料列）組成。它們在查詢的 `FROM` 子句中的用法，就像資料表、檢視表或子查詢一樣。資料表函式所回傳的欄位，可以用與資料表、檢視表或子查詢的欄位相同的方式，包含在 `SELECT`、`JOIN` 或 `WHERE` 子句中。

資料表函式也可以使用 `ROWS FROM` 語法組合起來，結果會以平行的欄位回傳；在這種情況下，結果資料列的數量等於最大的函式結果，較小的結果則會以 null 值補齊。

```

function_call [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
ROWS FROM( function_call [, ... ] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
```

如果指定了 `WITH ORDINALITY` 子句，函式結果欄位中會額外加入一個 `bigint` 型別的欄位。這個欄位會為函式結果集合的資料列編號，從 1 開始。（這是 SQL 標準 `UNNEST ... WITH ORDINALITY` 語法的一般化。）預設情況下，序號欄位的名稱是 `ordinality`，但可以使用 `AS` 子句為它指定其他的欄位名稱。

特殊的資料表函式 `UNNEST` 可以用任意數量的陣列參數呼叫，它會回傳對應數量的欄位，就如同對每個參數分別呼叫 `UNNEST`（[第 9.19 節](../functions/functions-array.md)），再使用 `ROWS FROM` 結構組合起來一樣。

```

UNNEST( array_expression [, ... ] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
```

如果沒有指定 *`table_alias`*，就會使用函式名稱作為資料表名稱；如果是 `ROWS FROM()` 結構，則使用第一個函式的名稱。

如果沒有提供欄位別名，對於回傳基本資料型別的函式，欄位名稱也會與函式名稱相同。對於回傳複合型別的函式，結果欄位會取得該型別各個屬性的名稱。

一些範例：

```

CREATE TABLE foo (fooid int, foosubid int, fooname text);

CREATE FUNCTION getfoo(int) RETURNS SETOF foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT * FROM getfoo(1) AS t1;

SELECT * FROM foo
    WHERE foosubid IN (
                        SELECT foosubid
                        FROM getfoo(foo.fooid) z
                        WHERE z.fooid = foo.fooid
                      );

CREATE VIEW vw_getfoo AS SELECT * FROM getfoo(1);

SELECT * FROM vw_getfoo;
```

在某些情況下，定義能依呼叫方式回傳不同欄位集合的資料表函式是很有用的。為了支援這一點，可以將資料表函式宣告為回傳虛擬型別 `record`，並且不帶 `OUT` 參數。在查詢中使用這樣的函式時，必須在查詢本身中指定預期的資料列結構，讓系統知道如何剖析與規劃該查詢。這種語法看起來像這樣：

```

function_call [AS] alias (column_definition [, ... ])
function_call AS [alias] (column_definition [, ... ])
ROWS FROM( ... function_call AS (column_definition [, ... ]) [, ... ] )
```

不使用 `ROWS FROM()` 語法時，*`column_definition`* 清單會取代原本可以附加在 `FROM` 項目上的欄位別名清單；欄位定義中的名稱會作為欄位別名。使用 `ROWS FROM()` 語法時，可以為每個成員函式分別附加 *`column_definition`* 清單；或者，如果只有一個成員函式且沒有 `WITH ORDINALITY` 子句，也可以在 `ROWS FROM()` 之後寫 *`column_definition`* 清單來取代欄位別名清單。

考慮下面這個範例：

```

SELECT *
    FROM dblink('dbname=mydb', 'SELECT proname, prosrc FROM pg_proc')
      AS t1(proname name, prosrc text)
    WHERE proname LIKE 'bytea%';
```

[dblink](../../appendixes/contrib/contrib-dblink-function.md) 函式（屬於 [dblink](../../appendixes/contrib/dblink.md) 模組）會執行遠端查詢。由於它可能用於任何種類的查詢，因此被宣告為回傳 `record`。實際的欄位集合必須在呼叫它的查詢中指定，讓剖析器知道例如 `*` 應該展開成什麼。

下面這個範例使用了 `ROWS FROM`：

```

SELECT *
FROM ROWS FROM
    (
        json_to_recordset('[{"a":40,"b":"foo"},{"a":"100","b":"bar"}]')
            AS (a INTEGER, b TEXT),
        generate_series(1, 3)
    ) AS x (p, q, s)
ORDER BY p;

  p  |  q  | s
-----+-----+---
  40 | foo | 1
 100 | bar | 2
     |     | 3
```

它將兩個函式合併為單一的 `FROM` 目標。`json_to_recordset()` 被指示要回傳兩個欄位，第一個是 `integer`，第二個是 `text`。`generate_series()` 的結果則直接使用。`ORDER BY` 子句會將欄位值當作整數排序。

<a id="QUERIES-LATERAL"></a>

#### 7.2.1.5. `LATERAL` 子查詢 [#](#QUERIES-LATERAL)

<a id="id-1.5.6.6.5.10.2"></a>

出現在 `FROM` 中的子查詢，前面可以加上關鍵字 `LATERAL`。這讓它們可以參照前面 `FROM` 項目所提供的欄位。（沒有 `LATERAL` 時，每個子查詢都是獨立求值的，因此無法交叉參照任何其他 `FROM` 項目。）

出現在 `FROM` 中的資料表函式，前面也可以加上關鍵字 `LATERAL`，但對函式而言這個關鍵字是選用的；無論如何，函式的引數都可以包含對前面 `FROM` 項目所提供之欄位的參照。

`LATERAL` 項目可以出現在 `FROM` 清單的最上層，也可以出現在 `JOIN` 樹狀結構中。在後一種情況下，當它位於某個 `JOIN` 的右側時，也可以參照該聯結左側的任何項目。

當 `FROM` 項目包含 `LATERAL` 交叉參照時，求值的過程如下：對於提供被交叉參照欄位之 `FROM` 項目的每一筆資料列，或提供這些欄位之多個 `FROM` 項目的每一組資料列，會使用該資料列或資料列組的欄位值對 `LATERAL` 項目求值。所產生的資料列會照常與計算出它們的資料列聯結。來源資料表的每一筆資料列或每一組資料列都會重複這個過程。

`LATERAL` 的一個簡單範例是

```

SELECT * FROM foo, LATERAL (SELECT * FROM bar WHERE bar.id = foo.bar_id) ss;
```

這並不特別有用，因為它的結果與比較傳統的寫法完全相同

```

SELECT * FROM foo, bar WHERE bar.id = foo.bar_id;
```

`LATERAL` 主要在計算要聯結的資料列需要被交叉參照的欄位時才有用。一個常見的應用是為傳回集合的函式提供引數值。例如，假設 `vertices(polygon)` 會回傳多邊形的頂點集合，我們可以用下列查詢找出資料表中所儲存之多邊形彼此靠近的頂點：

```

SELECT p1.id, p2.id, v1, v2
FROM polygons p1, polygons p2,
     LATERAL vertices(p1.poly) v1,
     LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

這個查詢也可以寫成

```

SELECT p1.id, p2.id, v1, v2
FROM polygons p1 CROSS JOIN LATERAL vertices(p1.poly) v1,
     polygons p2 CROSS JOIN LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

或其他幾種等價的寫法。（如前所述，在這個範例中並不需要 `LATERAL` 關鍵字，但為了清楚起見我們還是使用了它。）

以 `LEFT JOIN` 聯結 `LATERAL` 子查詢往往特別方便，這樣即使 `LATERAL` 子查詢沒有為某些來源資料列產生任何資料列，這些來源資料列仍然會出現在結果中。例如，如果 `get_product_names()` 會回傳某個製造商所製造產品的名稱，但我們資料表中的某些製造商目前沒有生產任何產品，就可以像這樣找出是哪些製造商：

```

SELECT m.name
FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id) pname ON true
WHERE pname IS NULL;
```

<a id="QUERIES-WHERE"></a>

### 7.2.2. `WHERE` 子句 [#](#QUERIES-WHERE)

<a id="id-1.5.6.6.6.2"></a>

[`WHERE`](../../reference/sql-commands/sql-select.md#SQL-WHERE) 子句的語法是

```

WHERE search_condition
```

其中 *`search_condition`* 是任何回傳 `boolean` 型別值的值運算式（請參閱[第 4.2 節](../sql-syntax/sql-expressions.md)）。

`FROM` 子句處理完之後，會以搜尋條件檢查衍生虛擬資料表的每一筆資料列。如果條件的結果為真，該資料列就會保留在輸出資料表中；否則（也就是結果為假或 null 時），就會被捨棄。搜尋條件通常會參照 `FROM` 子句所產生之資料表中的至少一個欄位；這並不是必要的，但否則 `WHERE` 子句就相當沒有用處了。

### 注意

內部聯結的聯結條件可以寫在 `WHERE` 子句中，也可以寫在 `JOIN` 子句中。例如，下列資料表運算式是等價的：

```

FROM a, b WHERE a.id = b.id AND b.val > 5
```

以及：

```

FROM a INNER JOIN b ON (a.id = b.id) WHERE b.val > 5
```

甚至可能是：

```

FROM a NATURAL JOIN b WHERE b.val > 5
```

要使用哪一種，主要是風格的問題。`FROM` 子句中的 `JOIN` 語法雖然屬於 SQL 標準，但移植到其他 SQL 資料庫管理系統時，可攜性可能沒那麼好。至於外部聯結則沒有選擇的餘地：它們必須在 `FROM` 子句中完成。外部聯結的 `ON` 或 `USING` 子句*並不*等同於 `WHERE` 條件，因為它會導致在最終結果中新增資料列（對於沒有相符項目的輸入資料列），也會導致移除資料列。

以下是一些 `WHERE` 子句的範例：

```

SELECT ... FROM fdt WHERE c1 > 5

SELECT ... FROM fdt WHERE c1 IN (1, 2, 3)

SELECT ... FROM fdt WHERE c1 IN (SELECT c1 FROM t2)

SELECT ... FROM fdt WHERE c1 IN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10)

SELECT ... FROM fdt WHERE c1 BETWEEN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10) AND 100

SELECT ... FROM fdt WHERE EXISTS (SELECT c1 FROM t2 WHERE c2 > fdt.c1)
```

`fdt` 是在 `FROM` 子句中衍生出來的資料表。不符合 `WHERE` 子句搜尋條件的資料列會從 `fdt` 中排除。請注意這裡將純量子查詢當作值運算式使用。子查詢就像任何其他查詢一樣，可以使用複雜的資料表運算式。也請注意在子查詢中是如何參照 `fdt` 的。只有在 `c1` 同時也是子查詢衍生輸入資料表中某個欄位的名稱時，才需要將 `c1` 限定為 `fdt.c1`。但即使不需要，限定欄位名稱也能讓查詢更清楚。這個範例說明了外層查詢的欄位命名範圍如何延伸到其內層查詢中。

<a id="QUERIES-GROUP"></a>

### 7.2.3. `GROUP BY` 與 `HAVING` 子句 [#](#QUERIES-GROUP)

<a id="id-1.5.6.6.7.2"></a><a id="id-1.5.6.6.7.3"></a>

通過 `WHERE` 過濾之後，衍生的輸入資料表可能會使用 `GROUP BY` 子句進行分組，並使用 `HAVING` 子句排除群組資料列。

```

SELECT select_list
    FROM ...
    [WHERE ...]
    GROUP BY grouping_column_reference [, grouping_column_reference]...
```

[`GROUP BY`](../../reference/sql-commands/sql-select.md#SQL-GROUPBY) 子句用來將資料表中在所有列出的欄位上都具有相同值的資料列分組在一起。欄位列出的順序並不重要。其效果是將每一組具有共同值的資料列合併為一筆群組資料列，代表該群組中的所有資料列。這麼做是為了排除輸出中的冗餘，或計算套用在這些群組上的彙總函式。例如：

```

=> SELECT * FROM test1;
 x | y
---+---
 a | 3
 c | 2
 b | 5
 a | 1
(4 rows)

=> SELECT x FROM test1 GROUP BY x;
 x
---
 a
 b
 c
(3 rows)
```

在第二個查詢中，我們不能寫 `SELECT * FROM test1 GROUP BY x`，因為欄位 `y` 並沒有可以與每個群組對應的單一值。分組依據的欄位可以在選取清單中參照，因為它們在每個群組中都只有單一值。

一般而言，如果資料表經過分組，未列在 `GROUP BY` 中的欄位就只能在彙總運算式中參照。以下是使用彙總運算式的範例：

```

=> SELECT x, sum(y) FROM test1 GROUP BY x;
 x | sum
---+-----
 a |   4
 b |   5
 c |   2
(3 rows)
```

這裡的 `sum` 是一個彙總函式，會對整個群組計算出單一值。關於可用彙總函式的更多資訊，請參閱[第 9.21 節](../functions/functions-aggregate.md)。

### 提示

不使用彙總運算式的分組，實際上等於計算某個欄位中不同值的集合。這也可以使用 `DISTINCT` 子句來達成（請參閱[第 7.3.3 節](queries-select-lists.md#QUERIES-DISTINCT)）。

以下是另一個範例：它會計算每項產品的總銷售額（而不是所有產品的總銷售額）：

```

SELECT product_id, p.name, (sum(s.units) * p.price) AS sales
    FROM products p LEFT JOIN sales s USING (product_id)
    GROUP BY product_id, p.name, p.price;
```

在這個範例中，欄位 `product_id`、`p.name` 與 `p.price` 必須列在 `GROUP BY` 子句中，因為它們在查詢的選取清單中被參照了（但請參閱下文）。欄位 `s.units` 不必列在 `GROUP BY` 清單中，因為它只用在代表產品銷售額的彙總運算式（`sum(...)`）中。對於每項產品，這個查詢會回傳一筆關於該產品所有銷售的彙總資料列。

<a id="id-1.5.6.6.7.11"></a>

如果 products 資料表被設定為例如以 `product_id` 作為主鍵，那麼在上面的範例中只要依 `product_id` 分組就夠了，因為名稱與價格會*函數相依*（functionally dependent）於產品 ID，因此對於每個產品 ID 群組要回傳哪個名稱與價格值，並不會有歧義。

在嚴格的 SQL 中，`GROUP BY` 只能依來源資料表的欄位分組，但 PostgreSQL 將其擴充為也允許 `GROUP BY` 依選取清單中的欄位分組。也允許依值運算式而非單純的欄位名稱分組。

<a id="id-1.5.6.6.7.14"></a>

如果資料表已經用 `GROUP BY` 分組，但只對某些群組感興趣，可以使用 `HAVING` 子句從結果中排除群組，其用法很像 `WHERE` 子句。語法是：

```

SELECT select_list FROM ... [WHERE ...] GROUP BY ... HAVING boolean_expression
```

`HAVING` 子句中的運算式，可以參照分組的運算式，也可以參照未分組的運算式（這必然涉及彙總函式）。

範例：

```

=> SELECT x, sum(y) FROM test1 GROUP BY x HAVING sum(y) > 3;
 x | sum
---+-----
 a |   4
 b |   5
(2 rows)

=> SELECT x, sum(y) FROM test1 GROUP BY x HAVING x < 'c';
 x | sum
---+-----
 a |   4
 b |   5
(2 rows)
```

同樣地，以下是一個比較貼近現實的範例：

```

SELECT product_id, p.name, (sum(s.units) * (p.price - p.cost)) AS profit
    FROM products p LEFT JOIN sales s USING (product_id)
    WHERE s.date > CURRENT_DATE - INTERVAL '4 weeks'
    GROUP BY product_id, p.name, p.price, p.cost
    HAVING sum(p.price * s.units) > 5000;
```

在上面的範例中，`WHERE` 子句依一個未分組的欄位選取資料列（該運算式只對最近四週的銷售為真），而 `HAVING` 子句則將輸出限制為總銷售毛額超過 5000 的群組。請注意，查詢各部分中的彙總運算式不一定要相同。

如果查詢包含彙總函式呼叫，但沒有 `GROUP BY` 子句，仍然會進行分組：結果是單一的群組資料列（如果該資料列接著被 `HAVING` 排除，也可能完全沒有資料列）。如果查詢包含 `HAVING` 子句，即使沒有任何彙總函式呼叫或 `GROUP BY` 子句，也是如此。

<a id="QUERIES-GROUPING-SETS"></a>

### 7.2.4. `GROUPING SETS`、`CUBE` 與 `ROLLUP` [#](#QUERIES-GROUPING-SETS)

<a id="id-1.5.6.6.8.2"></a><a id="id-1.5.6.6.8.3"></a><a id="id-1.5.6.6.8.4"></a>

使用*分組集合*（grouping set）的概念，可以進行比上述更複雜的分組運算。`FROM` 與 `WHERE` 子句所選取的資料，會依每個指定的分組集合分別分組，並像簡單的 `GROUP BY` 子句一樣為每個群組計算彙總，然後回傳結果。例如：

```

=> SELECT * FROM items_sold;
 brand | size | sales
-------+------+-------
 Foo   | L    |  10
 Foo   | M    |  20
 Bar   | M    |  15
 Bar   | L    |  5
(4 rows)

=> SELECT brand, size, sum(sales) FROM items_sold GROUP BY GROUPING SETS ((brand), (size), ());
 brand | size | sum
-------+------+-----
 Foo   |      |  30
 Bar   |      |  20
       | L    |  15
       | M    |  35
       |      |  50
(5 rows)
```

`GROUPING SETS` 的每個子清單可以指定零個或多個欄位或運算式，其解讀方式就如同它們直接寫在 `GROUP BY` 子句中一樣。空的分組集合表示所有資料列都會彙總為單一群組（即使沒有任何輸入資料列也會輸出），如同前面所述沒有 `GROUP BY` 子句之彙總函式的情況。

在未出現某些分組欄位或運算式的分組集合所產生的結果資料列中，對這些欄位或運算式的參照會被 null 值取代。要區分某筆輸出資料列是由哪一種分組產生的，請參閱[表 9.66](../functions/functions-aggregate.md#FUNCTIONS-GROUPING-TABLE)。

系統提供了簡寫表示法，用來指定兩種常見的分組集合類型。下列形式的子句

```

ROLLUP ( e1, e2, e3, ... )
```

代表所給定的運算式清單及該清單的所有前綴（包括空清單）；因此它等同於

```

GROUPING SETS (
    ( e1, e2, e3, ... ),
    ...
    ( e1, e2 ),
    ( e1 ),
    ( )
)
```

這通常用於階層式資料的分析，例如依部門、事業處以及全公司總計的薪資總額。

下列形式的子句

```

CUBE ( e1, e2, ... )
```

代表所給定的清單及其所有可能的子集合（也就是冪集合）。因此

```

CUBE ( a, b, c )
```

等同於

```

GROUPING SETS (
    ( a, b, c ),
    ( a, b    ),
    ( a,    c ),
    ( a       ),
    (    b, c ),
    (    b    ),
    (       c ),
    (         )
)
```

`CUBE` 或 `ROLLUP` 子句中的個別元素，可以是個別的運算式，也可以是以括號括住的元素子清單。在後一種情況下，產生個別分組集合時，子清單會被視為單一單位。例如：

```

CUBE ( (a, b), (c, d) )
```

等同於

```

GROUPING SETS (
    ( a, b, c, d ),
    ( a, b       ),
    (       c, d ),
    (            )
)
```

而

```

ROLLUP ( a, (b, c), d )
```

等同於

```

GROUPING SETS (
    ( a, b, c, d ),
    ( a, b, c    ),
    ( a          ),
    (            )
)
```

`CUBE` 與 `ROLLUP` 結構可以直接用在 `GROUP BY` 子句中，也可以巢狀放在 `GROUPING SETS` 子句中。如果一個 `GROUPING SETS` 子句巢狀在另一個之中，其效果就如同內層子句的所有元素都直接寫在外層子句中一樣。

如果在單一的 `GROUP BY` 子句中指定了多個分組項目，最終的分組集合清單就是個別項目的笛卡兒積。例如：

```

GROUP BY a, CUBE (b, c), GROUPING SETS ((d), (e))
```

等同於

```

GROUP BY GROUPING SETS (
    (a, b, c, d), (a, b, c, e),
    (a, b, d),    (a, b, e),
    (a, c, d),    (a, c, e),
    (a, d),       (a, e)
)
```

<a id="id-1.5.6.6.8.13.1"></a>
<a id="id-1.5.6.6.8.13.2"></a>
同時指定多個分組項目時，最終的分組集合中可能會包含重複的項目。例如：

```

GROUP BY ROLLUP (a, b), ROLLUP (a, c)
```

等同於

```

GROUP BY GROUPING SETS (
    (a, b, c),
    (a, b),
    (a, b),
    (a, c),
    (a),
    (a),
    (a, c),
    (a),
    ()
)
```

如果不希望有這些重複的項目，可以直接在 `GROUP BY` 上使用 `DISTINCT` 子句來移除它們。因此：

```

GROUP BY DISTINCT ROLLUP (a, b), ROLLUP (a, c)
```

等同於

```

GROUP BY GROUPING SETS (
    (a, b, c),
    (a, b),
    (a, c),
    (a),
    ()
)
```

這與使用 `SELECT DISTINCT` 並不相同，因為輸出資料列仍然可能包含重複的資料列。如果任何未分組的欄位包含 NULL，它將與該欄位被分組時所使用的 NULL 無法區分。

### 注意

在運算式中，`(a, b)` 這種結構通常會被辨識為[資料列建構子](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)。但在 `GROUP BY` 子句中，這一點並不適用於運算式的最上層，`(a, b)` 會如上所述被剖析為運算式清單。如果基於某些原因，你*需要*在分組運算式中使用資料列建構子，請使用 `ROW(a, b)`。

<a id="QUERIES-WINDOW"></a>

### 7.2.5. Window 函式的處理 [#](#QUERIES-WINDOW)

<a id="id-1.5.6.6.9.2"></a>

如果查詢包含任何 window 函式（請參閱[第 3.5 節](../../tutorial/tutorial-advanced/tutorial-window.md)、[第 9.22 節](../functions/functions-window.md)與[第 4.2.8 節](../sql-syntax/sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)），這些函式會在所有分組、彙總與 `HAVING` 過濾完成之後才求值。也就是說，如果查詢使用了任何彙總函式、`GROUP BY` 或 `HAVING`，那麼 window 函式所看到的資料列是群組資料列，而不是來自 `FROM`/`WHERE` 的原始資料表資料列。

使用多個 window 函式時，所有在其視窗定義中具有等價 `PARTITION BY` 與 `ORDER BY` 子句的 window 函式，都保證會看到相同的輸入資料列順序，即使 `ORDER BY` 並未唯一決定該順序也一樣。不過，對於具有不同 `PARTITION BY` 或 `ORDER BY` 規格的函式，其求值則沒有任何保證。（在這種情況下，window 函式求值的各個階段之間通常需要一個排序步驟，而該排序並不保證會保留其 `ORDER BY` 視為等價之資料列的順序。）

目前，window 函式一律需要預先排序的資料，因此查詢的輸出會依某一個 window 函式的 `PARTITION BY`/`ORDER BY` 子句排序。不過，不建議依賴這一點。如果你想確保結果以特定方式排序，請使用明確的最上層 `ORDER BY` 子句。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/queries-table-expressions.html)（原文版本：18.6；核對日期：2026-09-11）
