# 7.2. 資料表表示式[^1]

資料表表示式計算結果會是一個資料表。 資料表表示式包含一個 FROM 子句，可以選擇性地加上 WHERE、GROUP BY 和 HAVING 子句。普通資料表表示式只是簡單地引用磁碟上的資料表，即所謂的基本資料表，但是更複雜的表示式可以用來以各種方式修改或組合基本資料表。

資料表表示式中選擇性的 WHERE、GROUP BY 和 HAVING 子句指定在 FROM 子句中執行連續轉換程序後產出衍生的資料表。所有這些轉換都會生成一個虛擬資料表，該資料表提供給資料列表的資料列來計算查詢輸出的欄位。

### 7.2.1. The`FROM`Clause

FROM 子句由逗號分隔的引用資料表列表中給予的一個或多個其他資料表進而衍生出一個資料表。

```
FROM table_reference [,table_reference [, ...]]
```

資料表的引用可以是資料表名稱（可能是帶有完整路徑的），或衍生資料表（如子查詢，JOIN 查詢或這些運算的複合組合）。如果在 FROM 子句中列出了多個資料表引用，則這些資料表會自動交叉連結（cross-join）（也就是說，它們資料列的笛卡爾積 Cartesian product 已經形成了，詳見下文）。 FROM 列表的結果是一個中繼的虛擬資料表，然後可以透過 WHERE、GROUP BY 和HAVING 子句進行轉換，最終成為整個資料表表示式的結果。

當一個資料表引用將一個資料表作為資料表繼承結構的父資料表進行命名時，資料表引用不僅產生了該資料表的所有資料列，還產生了其所有後代資料表的資料列，除非該關鍵字只提供資料表名稱。但是，引用只會產生出現在資料表列表中的欄位 - 忽略在子資料表中增加的任何欄位。

除了在資料表名稱之前指定之外，還可以在表名後面寫「\*」以明確表示包含所有之後的資料表。 現在沒有什麼理由再使用這個語法了，因為搜尋子資料表在目前是預設的行為。但是，它提供了與舊版本支援的相容性。

#### 7.2.1.1. Joined Tables

交叉查詢（JOIN）的資料表是根據特定連接類型的規則從其他兩個（實際或衍生）資料表共同衍生而來的資料表。有 inner、outer、 及 cross-joins 可以使用。 交叉查詢資料表的一般語法是：

```
T1 join_type T2 [join_condition]
```

所有類型的交叉查詢可以連接在一起，也可以是巢狀結構： T1 或 T2 都可以是交叉查詢後的資料表。在 JOIN 子句使用可以小括號來控制交叉查詢的次序。在沒有括號的情況下，JOIN 子句就從左到右巢狀運算。

**Join Types**

* Cross join

```
T1 CROSS JOIN T2
```

對於來自 T1 和 T2（即笛卡爾乘積）資料列的每個可能的組合，交叉查詢的資料表將包含由 T1 中的所有欄位組成的資料列，隨後是 T2 中的所有的欄位。如果這些資料表分別具有 N 個資料列和 M 資料列，則交叉查詢後的資料表將具有 N \* M 個資料列。

`FROM T1 CROSS JOIN T2` 相當於 `FROM T1 INNER JOIN T2 ON TRUE`（詳見下文）。 它也相當於 `FROM T1, T2`。

> ### 注意
>
> 當超過兩個資料表出現時，最後描述的等價關係並不完全適用，因為 JOIN 的綁定比只有逗號的意義更緊密。例如「FROM T1 CROSS JOIN T2 INNER JOIN T3 ON condition」與「FROM T1，T2 INNER JOIN T3 ON condition」不一樣，因為條件 condition 會在第一種情況下引用 T1，而不會在第二種情況下引用 T1。

* Qualified joins

```
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 ON boolean_expression
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 USING (join column list )

T1 NATURAL { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2
```

INNER 和 OUTER 是所有語法上都是可以使用的選項。INNER 是預設的；LEFT、RIGHT 和 FULL 隱含著外部交叉查詢（outer join）的意義。

交叉查詢的條件在 ON 或 USING 子句中指定，或者由NATURAL 隱含指定。交叉查詢條件確定兩個資料表中的哪些欄位被「配對」，詳細說明如下。

支援指定的交叉查詢的類型是：

`INNER JOIN`

對於 T1 的每一資料列 R1，連結在資料表 T2 中每一資料列都有一個滿足與 R1 的交叉查詢條件。

`LEFT OUTER JOIN`

首先，會先執行內部交叉查詢（inner join）。 然後，對於 T1 中不滿足與 T2 中的任何資料列的交叉查詢條件的每一資料列，在 T2 加上空值欄位。因此，交叉查詢最後的資料表中 T1 的每個資料列都至少會出現一次。

`RIGHT OUTER JOIN`

首先，會先執行內部交叉查詢（inner join）。 然後，對於 T2 中不滿足與 T1 中的任何資料列的交叉查詢條件的每一資料列，在 T1 加上空值欄位。也就是左向交叉查詢的反向： 交叉查詢最後的資料表中 T2 的每個資料列都至少會出現一次。

`FULL OUTER JOIN`

首先，會先執行內部交叉查詢（inner join）。 然後，對於 T1 中不滿足與 T2 中的任何資料列的交叉查詢條件的每一資料列，在 T2 加上空值欄位。 同樣地，對於 T2 中不滿足與 T1 中的任何資料列的交叉查詢條件的每一資料列，在 T1 加上空值欄位。

ON 子句是最一般形式的交叉查詢條件：採用與 WHERE 子句中使用的相同形式的布林表示式。 如果 ON 表示式的計算結果為 true，則 T1 和 T2 中的一對資料列形成匹配。

USING 子句是一種簡寫，它允許你利用交叉查詢的兩端對接欄位使用相同名稱的特定情況。它使用逗號分隔的共享欄位名稱列表，並形成包含每個欄位的相等比較的交叉查詢條件。例如，使用USING \(a，b\) 連結 T1 和 T2 產生交叉查詢條件「ON T1.a = T2.a AND T1.b = T2.b」。

此外，JOIN USING 的輸出減少重覆的欄位：不需要輸出兩個連結好的欄位，因為它們一定具有相同的值。雖然 JOIN ON 由 T1 的所有欄位，再接著 T2 的所有欄位，但 JOIN USING 為每個列出的欄位配對（按列出的順序）產生一個輸出欄位，其後是來自 T1 的剩餘欄，隨後是來自 T2 的剩餘欄位。

最後，NATURAL 是 USING 的簡寫形式：它會形成一個 USING 列表，其中包含出現在兩個輸入資料表中的所有的欄位名。和 USING 一樣，這些欄位在輸出資料表中就只會出現一次。如果沒有相同的欄位名稱，NATURAL 可能就像 CROSS JOIN。

### Note

因為只有列出的欄位會被組合，所以 USING 對於交叉查詢關係中的欄位更改是相當安全的。NATURAL 的風險是較大，因為任何資料結構更新都導致新的配對欄位名稱出現，也造成交叉查詢組合新欄位。

把這些東西放在一起來看，假設我們有資料表 t1：

```
 num | name
-----+------
   1 | a
   2 | b
   3 | c
```

資料表`t2`:

```
 num | value
-----+-------
   1 | xxx
   3 | yyy
   5 | zzz
```

那麼我們可以得到以下結果為各種交叉查詢：

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

ON 指定的交叉查詢條件也可以包含與交叉查詢無關的條件。 這可以證明對某些查詢有用，但需要仔細考慮。例如：

```
=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num AND t2.value = 'xxx';

 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   2 | b    |     |
   3 | c    |     |
(3 rows)
```

請注意，將限制條件放在 WHERE 子句中會產生不同的結果：

```
=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num WHERE t2.value = 'xxx';

 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
(1 row)
```

這是因為在 ON 子句中放置的條件會在交叉查詢之前處理，而在交叉查詢之後才會處理在 WHERE 子句中的條件。這在 INNER JOIN 時沒有關係，但 OUTER JOIN 時就很重要。

#### 7.2.1.2. 資料表和欄位的別名

可以為資料表和複雜的資料表引用指定一個臨時名稱，以便在查詢的其餘部分中用於對該衍生資料表引用。這稱作為資料表別名。

要建立一個資料表別名，請使用：

```
FROM table_reference AS alias
```

或

```
FROM table_reference alias
```

AS 關鍵字是選用的。別名可以是任何識別名稱。

資料表別名的一個典型應用是將短識別名稱分配給長資料表名稱，以保持交叉查詢子句的可讀性。例如：

```
SELECT * FROM some_very_long_table_name s JOIN another_fairly_long_name a ON s.id = a.num;
```

就當下的查詢而言，別名將成為資料表引用的新名稱 — 但不允許在查詢中其他地方使用原始名稱來引用資料表。 因此，像這樣是無效的：

```
SELECT * FROM my_table AS m WHERE my_table.a > 5;    -- wrong
```

資料表別名主要是為了符號方便，但是在將資料表和自己交叉查詢時更有必要使用它們，例如：

```
SELECT * FROM people AS mother JOIN people AS child ON mother.id = child.mother_id;
```

此外，如果資料表引用是子查詢，則別名必要的（請向下參閱[第 7.2.1.3 節](#7213-subqueries)）。

括號可以用來解決歧義。在以下範例中，第一個查詢語句將別名 b 分配給 my\_table 的第二個實例，但第二個語句將別名分配給交叉查詢的結果：

```
SELECT * FROM my_table AS a CROSS JOIN my_table AS b ...
SELECT * FROM (my_table AS a CROSS JOIN my_table) AS b ...
```

另一種形式的資料表別名為資料表的欄位所提供的臨時名稱，就如同資料表本身的別名一樣：

```
FROM table_reference [AS] alias ( column1 [, column2 [, ...］] )
```

如果指定的欄位別名少於實際資料表中的欄位，則其餘列就不會重新命名。此語法對於自我交叉查詢或子查詢時特別有用。

將別名應用於 JOIN 子句的輸出時，別名隱藏了 JOIN 中的原始名稱。 例如：

```
SELECT a.* FROM my_table AS a JOIN your_table AS b ON ...
```

是合法的 SQL，但：

```
SELECT a.* FROM (my_table AS a JOIN your_table AS b ON ...) AS c
```

是不合法的；資料表別名 a 在別名 c 以外是不可見的。

#### 7.2.1.3. 子查詢（Subqueries）

指定衍生資料表的子查詢必須用圓括號括起來，並且必須分配一個資料表表別名（如[第 7.2.1.2 節](#7212-table-and-column-aliases)所述）。 例如：

```
FROM (SELECT * FROM table1) AS alias_name
```

這例子等同於`FROM table1 AS alias_name`。當子查詢涉及分組或彙總時，會出現更多有趣的情況，這些情況不能簡化為普通的交叉查詢。

子查詢也可以是一個 VALUES 列表：

```
FROM (VALUES ('anne', 'smith'), ('bob', 'jones'), ('joe', 'blow'))
     AS names(first, last)
```

再一次，這時候一個資料表別名是必須的。 將別名指定給 VALUES 列表的欄位是可選的，但這會是很好的做法。更多資訊請參閱[第 7.7 節](/ii-the-sql-language/queries/77-values-lists.md)。

#### 7.2.1.4. Table Functions

資料表函數是由基本資料類型（scalar types）或複合資料類型（資料表的資料列）所組成的函數。它們在查詢的 FROM 子句中用作資料表、View 或子查詢。資料表函數回傳的資料列可以與資料表、View 或子查詢的資料列相同的方式包含在 SELECT、JOIN 或 WHERE子句中。

資料表函數也可以使用 ROWS FROM 語法進行組合，結果在平行的欄位中回傳；在這種情況下結果資料列的數量是函數結果的最大數量，較小的結果填充空值來搭配。

```
function_call [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ...])]]
ROWS FROM( function_call [, ...] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ...])]]
```

如果使用了 WITH ORDINALITY 子句，則會將另一個型別為 bigint 的欄位增加到函數結果欄位中。此欄位是編號從 1 開始的函數結果資料列數量。（這是 UNNEST ... WITH ORDINALITY 的SQL標準語法的一般寫法。）預設情況下，序號欄位被稱為 ordinality，但是可以使用 AS 子句將不同的欄位名稱指定給它。

可以使用任意數量的陣列參數用於特殊資料表函數 UNNEST，並回傳相應數量的欄位，就像 UNNEST（[第 9.18 節](/ii-the-sql-language/functions-and-operators/918-array-functions-and-operators.md)）分別在每個參數上被呼叫並使用 ROWS FROM 同樣的結構組合起來。

```
UNNEST( array_expression [, ...] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ...])]]
```

如果沒有指定 table\_alias 的話，就會使用函數名稱作為表名；在 ROWS FROM\(\) 的結構中，將使用第一個函數的名字。

如果未提供欄位的別名，則對於回傳基本資料型別的函數，欄位名稱也與函數名稱相同。對於回傳複合型別的函數，結果的欄位將獲取類型的各個屬性的名稱。

這裡有一些例子：

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

在某些情況下，定義可以回傳不同欄位集合的資料表函數是很有用的，這取決於它們是如何被引用的。為了支援這個功能，資料表函數可以宣告為回傳抽象型別 record。在查詢中使用這樣的函數時，必須在查詢本身中指定期望的資料列結構，以便系統知道如何解析和規劃查詢。 這個語法如下所示：

```
function_call [AS] alias (column_definition [, ...])

function_call AS [alias] (column_definition [, ...])
ROWS FROM( ... function_call AS (column_definition [, ...]) [, ...] )
```

當不使用 ROWS FROM\(\) 語法時，column\_definition 列表將替換可能附加到 FROM 項目的欄位別名列表；欄位定義中的名稱用作欄位別名。使用 ROWS FROM\(\) 語法時，可以將 column\_definition 列表分別附加到每個成員函數；或者如果只有一個成員函數並且沒有 WITH ORDINALITY 子句的話，則可以在 ROWS FROM\(\) 之後寫入 column\_definition 列表來代替欄位別名列表。

可以參考這個例子：

```
SELECT *
    FROM dblink('dbname=mydb', 'SELECT proname, prosrc FROM pg_proc')
      AS t1(proname name, prosrc text)
    WHERE proname LIKE 'bytea%';
```

[dblink 函數](/viii-appendixes/additional-supplied-modules/f11-dblink/dblink.md)（[dblink 模組](/viii-appendixes/additional-supplied-modules/f11-dblink.md)的一部分）用於執行遠端查詢。 它宣告為回傳 record，因為它可能被用於任何類型的查詢。必須在呼叫查詢時指定實際的欄位集合，以便語法解析器能夠知道如何解析，例如，「\*」應該展開為什麼樣的東西。

#### 7.2.1.5. `LATERAL`子查詢

在 FROM 中的子查詢可以使用關鍵字 LATERAL 進行前置處理。這使他們能夠引用在 FROM 前面所提供的欄位。（沒有 LATERAL 的話，每個子查詢都是獨立處理的，因此不能交叉引用任何其他 FROM 的項目。）

在 FROM 中出現的資料表函數也可以在關鍵字 LATERAL 之前，但是對於函數來說關鍵字是選擇性的；在任何情況下，函數的參數都可以包含對前面 FROM 項目提供的欄位的引用。

一個 LATERAL 項目可以出現在 FROM 列表的最上層，或在一個 JOIN 樹狀圖中。在後者情況下，它也可以是在 JOIN 右側的任何項目。

當 FROM 項目包含 LATERAL 交叉引用時，處理過程如下：對於提供交叉引用欄位的 FROM 項目的每一行，或者提供欄位的多個 FROM 項目的集合，LATERAL 項目將使用該行或行集合的欄位值進行處理。衍生的資料列如同往常一樣連接到它們從中計算的資料列。 這對於資料列原始資料表中的每一資料列或一組資料列是重複進行的。

LATERAL 的一個簡易的例子：

```
SELECT * FROM foo, LATERAL (SELECT * FROM bar WHERE bar.id = foo.bar_id) ss;
```

這不是特別有用，因為它與一般的結果完全相同

```
SELECT * FROM foo, bar WHERE bar.id = foo.bar_id;
```

當交叉引用列用於計算要連接的欄位時，LATERAL 才會是有用的。一個常見的應用是為回傳函數提供一個參數值。 例如，假設頂點（多邊形）回傳一個多邊形的頂點集合，我們可以識別儲存在資料表中的多邊形相鄰頂點：

```
SELECT p1.id, p2.id, v1, v2
FROM polygons p1, polygons p2,
     LATERAL vertices(p1.poly) v1,
     LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2)< 10 AND p1.id != p2.id;
```

這個查詢也可以寫成：

```
SELECT p1.id, p2.id, v1, v2
FROM polygons p1 CROSS JOIN LATERAL vertices(p1.poly) v1,
     polygons p2 CROSS JOIN LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

或者以幾種其他等同的寫法。（正如已經提到的，在這個例子中，LATERAL關鍵字是不必要的，但我們使用它來讓用法更清楚。）

將 LEFT JOIN 加到 LATERAL 子查詢中通常是很方便的，所以即使 LATERAL 子查詢不為它們產生資料列，來源的資料列也會出現在結果中。例如，如果 get\_product\_names\(\) 回傳製造商生產產品的名稱，但是我們資料表中的一些製造商目前不生產產品，我們可以找出哪些製造商是這樣的情況：

```
SELECT m.name
FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id) pname ON true
WHERE pname IS NULL;
```

### 7.2.2. `WHERE`子句

WHERE 子句的語法是：

```
WHERE search_condition
```

其中的 search\_condition 指的是回傳一個布林型別的表示式（詳見 [4.2 節](/ii-the-sql-language/sql-syntax/42-value-expressions.md)）。

在完成 FROM 子句的處理後，將根據過濾條件檢查衍生虛擬資料表的每一個資料列。如果條件結果為真，則該資料列保留在輸出資料表中，否則（即其結果為假或空）則將其丟棄。過濾條件通常會引用至少一個在 FROM 子句中生成資料表的欄位；但這不是必須的，只是 WHERE 子句將會變得沒有用處。

> ### 注意
>
> 內部交叉查詢的連結條件可以寫入 WHERE 子句或 JOIN 子句中。例如，這些資料表表示式是等價的：
>
> ```
> FROM a, b WHERE a.id = b.id AND b.val > 5
> ```
>
> 和：
>
> ```
> FROM a INNER JOIN b ON (a.id = b.id) WHERE b.val > 5
> ```
>
> 又或可能是：
>
> ```
> FROM a NATURAL JOIN b WHERE b.val > 5
> ```
>
> 你想使用哪一個端看你的風格。FROM 子句中的 JOIN 語法可能不像其他 SQL 資料庫管理系統那樣具有可移植性，即使它在 SQL 標準中。對於外部交叉查詢，沒有其他選擇：它們必須在 FROM 子句中完成。 外部交叉查詢的 ON 或 USING 子句不等於 WHERE 條件，因為它會導致增加資料列（對於無法匹配的輸入資料列）以及刪除最終結果中的資料列。

這裡還有一些 WHERE 子句的例子：

```
SELECT ... FROM fdt WHERE c1 > 5

SELECT ... FROM fdt WHERE c1 IN (1, 2, 3)

SELECT ... FROM fdt WHERE c1 IN (SELECT c1 FROM t2)

SELECT ... FROM fdt WHERE c1 IN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10)

SELECT ... FROM fdt WHERE c1 BETWEEN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10) AND 100

SELECT ... FROM fdt WHERE EXISTS (SELECT c1 FROM t2 WHERE c2 > fdt.c1)
```

fdt 是 FROM 子句中衍生的資料表。不符合 WHERE 子句條件的資料列，將會從 fdt 中消除。注意使用常數子查詢作為值的表示式的用法。就像任何其他查詢一樣，子查詢也可以使用複雜的表示式。也請注意如何在子查詢中引用 fdt。如果 c1 也是子查詢的衍生輸入資料表中欄位的名稱，則只需要將 c1 限定為 fdt.c1 即可。但是，即使在不需要的情況下，對欄位名稱進行限定寫法也能增加可讀性。這個例子表現了外層查詢的欄位命名範圍如何擴展到內層查詢中。

### 7.2.3. `GROUP BY`和`HAVING`子句

在處理完 WHERE 的過濾之後，可以使用 GROUP BY 子句對衍生的輸入資料表進行分組，再使用 HAVING 子句再一次過濾。

```
SELECT select_list
    FROM ...    [WHERE ...]
    GROUP BY grouping_column_reference [, grouping_column_reference]...
```

[GROUP BY 子句](/vi-reference/i-sql-commands/select.md)用於將資料表中所有欄位中具有相同值的資料列組合在一起。 欄位的次序並不重要。其效果是將具有相同內容的每一組資料列組合成一個代表組中所有資料列的資料列。這樣做是為了消除輸出中的多餘和/或計算適用於這些群組的集合。 例如：

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

在第二個查詢中，我們不能寫 SELECT \* FROM test1 GROUP BY x，因為沒有任何內容能使欄位 y 與每個群組構成關聯。可以在選擇列表中引用分組的欄位，因為它們在每個組中都有一個值。

一般來說，如果一個資料表被分組時，那麼除非在彙總表示式中引用，否則不能引用沒有在 GROUP BY 中列出的欄位。彙總表示式如下所示：

```
=> SELECT x, sum(y) FROM test1 GROUP BY x;

 x | sum
---+-----
 a |   4
 b |   5
 c |   2
(3 rows)
```

這裡 sum 是一個計算整個群組成為一個值的彙總函數。可用的彙總函數更多信息可以參閱[第 9.20 節](/ii-the-sql-language/functions-and-operators/920-aggregate-functions.md)。

> ### 小技巧
>
> 不包含彙總表示式的群組（grouping）計算能有效地計算欄位間相異值的集合。 這也可以使用 DISTINCT 子句來達成（詳見 [7.3.3 節](/ii-the-sql-language/queries/73-select-lists.md)）。

下面是另一個例子：它計算每個產品的總銷售額（而不是所有產品的總銷售額）：

```
SELECT product_id, p.name, (sum(s.units) * p.price) AS sales
    FROM products p LEFT JOIN sales s USING (product_id)
    GROUP BY product_id, p.name, p.price;
```

在這個例子中，product\_id、p.name 和 p.price這三個欄位必須在 GROUP BY 子句中，因為它們在查詢資料列表中被引用（見下文）。 欄位 s.units 不必存在於 GROUP BY 列表中，因為它只用於表示產品銷售的彙總表示式（sum\(...\)）。 對於每個產品，查詢回傳關於產品所有銷售的彙總資料列。

如果產品資料表設定 product\_id 為主鍵，則在上面的例子中，按照 product\_id 進行分組就足夠了，因為名稱和價格在功能上依賴於產品 ID，因此將會有 對於每個產品 ID 組回傳哪個名稱和價格值沒有歧義。

在嚴格的 SQL 中，GROUP BY 只能按來源資料表的欄位進行分組，但 PostgreSQL 對此進行擴展以允許 GROUP BY 按資料列表中的欄位進行分組。也可以使用數值表示式而不是簡單的欄位名稱進行分組。

如果一個表已經使用 GROUP BY 分組，但只對某些組感興趣，則可以使用 HAVING 子句，就像 WHERE 子句一樣，從結果中消除某些分組。其語法是：

```
SELECT 
select_list
 FROM ... [WHERE ...] GROUP BY ... HAVING boolean_expression
```

HAVING 子句中的表示式既可以引用分組表示式也可以引用未分組的表示式（這些表示式必然涉及彙總函數）。

範例如下：

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

繼續來看，一個更真實的例子：

```
SELECT product_id, p.name, (sum(s.units) * (p.price - p.cost)) AS profit
    FROM products p LEFT JOIN sales s USING (product_id)
    WHERE s.date > CURRENT_DATE - INTERVAL '4 weeks'
    GROUP BY product_id, p.name, p.price, p.cost
    HAVING sum(p.price * s.units) > 5000;
```

在上面的示例中，WHERE 子句按未分組的欄位進行過濾（表示式意思是，只有最近四周內的資料列為真），而 HAVING 子句將輸出限制為總銷售額超過 5000 的分組。請注意，彙總表示式不一定需要在查詢的所有部分都是相同的。

如果查詢包含了彙總函數的使用，但沒有 GROUP BY 子句，則仍然會發生分組：結果會是單個組的資料列（如果單個行被 HAVING 消除了，那可能根本沒有資料列輸出）。如果包含了 HAVING 子句，即使沒有任何彙總函數或GROUP BY 子句，也是如此。

### 7.2.4. `GROUPING SETS`,`CUBE`, 和`ROLLUP`

使用分組集合的概念，可以進行比上述更複雜的分組查詢。 由FROM和WHERE子句選擇的資料由每個指定的分組集合分別分組，為每個分組計算的彙總就像簡單的GROUP BY子句一樣，然後回傳結果。 例如：

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

GROUPING SETS 的每個子列表可以指定零個或多個欄位或表示式，與其在GROUP BY 子句中的解釋方式相同。一個空的分組集合意味著所有的行都被彙總到一個單獨的組中（即使沒有輸入資料列存在，也是輸出），就如上面沒有 GROUP BY 子句的集合函數所描述的那樣。

對分組欄位或表示式的引用被替換為結果資料列中的空值，用於對其中不顯示這些欄位的分組進行分組。要區分特定輸出資料列的分組，請參見[表 9.56](/ii-the-sql-language/functions-and-operators/920-aggregate-functions.md)。

提供簡寫符號來指定兩種常見的分組類型。一種形式的子句內容：

```
ROLLUP ( e1, e2, e3, ... )
```

表示給定的表示式列表和列表的所有前置式，包括空列表；因此它相當於

```
GROUPING SETS (
    ( e1, e2, e3, ... ),
    ...
    ( e1, e2 ),
    ( e1 ),
    ( )
)
```

這通常用於對分層數據進行分析; 例如：按部門、小組和全公司總薪資總額。

一個子句的形式：

```
CUBE ( e1, e2, ... )
```

代表給定的列表及其所有可能的子集（即功率集合）。也就是

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

CUBE 或 ROLLUP 子句的各個元素可以是單獨的表示式，也可以是括號中元素的子列表。在後面的例子中，為了生成單獨的分組集合，子列表被視為單個單元。 例如：

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

還有

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

CUBE 和 ROLLUP 結構可以直接在 GROUP BY 子句中使用，也可以嵌入在 GROUPING SETS 子句中。如果一個 GROUPING SETS 子句嵌入在另一個子句中，則效果與內部子句的所有元素都直接寫入外部子句的效果相同。

如果在單個 GROUP BY 子句中指定了多個分組項目，則分組集合的最終列表是各個項目的乘積。例如：

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

> ### 注意
>
> construct\(a, b\) 通常在表示式中被識別為資料列的初始化函數（[row constructor](/ii-the-sql-language/sql-syntax/42-value-expressions.md)）。 在 GROUP BY 子句中，不會應用於最上層的表示式，並且 \(a, b\) 會被解析為如上所述的表示式列表。如果由於某種原因需要在分組表示式中使用行初始化函數，請使用 ROW\(a, b\)。

### 7.2.5. Window Function Processing

If the query contains any window functions \(see[Section 3.5](https://www.postgresql.org/docs/10/static/tutorial-window.html),[Section 9.21](https://www.postgresql.org/docs/10/static/functions-window.html)and[Section 4.2.8](https://www.postgresql.org/docs/10/static/sql-expressions.html#syntax-window-functions)\), these functions are evaluated after any grouping, aggregation, and`HAVING`filtering is performed. That is, if the query uses any aggregates,`GROUP BY`, or`HAVING`, then the rows seen by the window functions are the group rows instead of the original table rows from`FROM`/`WHERE`.

When multiple window functions are used, all the window functions having syntactically equivalent`PARTITION BY`and`ORDER BY`clauses in their window definitions are guaranteed to be evaluated in a single pass over the data. Therefore they will see the same sort ordering, even if the`ORDER BY`does not uniquely determine an ordering. However, no guarantees are made about the evaluation of functions having different`PARTITION BY`or`ORDER BY`specifications. \(In such cases a sort step is typically required between the passes of window function evaluations, and the sort is not guaranteed to preserve ordering of rows that its`ORDER BY`sees as equivalent.\)

Currently, window functions always require presorted data, and so the query output will be ordered according to one or another of the window functions'`PARTITION BY`/`ORDER BY`clauses. It is not recommended to rely on this, however. Use an explicit top-level`ORDER BY`clause if you want to be sure the results are sorted in a particular way.

---

[^1]: [PostgreSQL: Documentation: 10: 7.2. Table Expressions](https://www.postgresql.org/docs/10/static/queries-table-expressions.html)

