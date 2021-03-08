# 7.2. 資料表表示式

一個 _資料表表示式_ 計算出一個資料表。資料表表示式包含了一個可以選擇在後方跟隨`WHERE`、`GROUP BY`和`HAVING`子句的`FROM`子句。普遍的資料表表示式簡單地在磁碟上引用一個資料表，, 即聲稱的基底資料表（base table）, 但更複雜的表示式可被用於以多種形式修改或組合基底資料表。

在資料表表示式中選擇性的`WHERE`、`GROUP BY`和`HAVING`子句指定一個逐次變換執行在`FROM`子句衍生的資料表上的管道。所有的這些轉換都會產生一個虛擬資料表，該資料表提供了被傳遞到選擇串列的資料列，以計算查詢的輸出資料列。

## 7.2.1. `FROM`子句

The [`FROM`子句](https://docs.postgresql.tw/reference/sql-commands/select#from-clause)從逗號分隔資料表參照串列中給出的一個或多個其他的資料表衍生一個資料表。

```text
FROM table_reference [, table_reference [, ...]]
```

一個資料表參照能是一個表格名稱（也許綱要限定的），或一個衍生出的資料表，例如子查詢，`JOIN`建構或這些的複雜組合。如果多個資料表參照被列在`FROM`子句中， 這些資料表參照則表將被交叉聯接（cross-joined，即形成其資料列的笛卡爾積；請參見下文。）`FROM`串列的結果是一個中間的虛擬表，該表可以受到`WHERE`、`GROUP BY`和`HAVING`子句的轉換，並且最終是整個資料表表示式的結果。

當一個資料表參照命名一個表格繼承層次結構的父級資料表，資料表參照不只是產生該表格的列，還會產生其所有後代表格的列，除非關鍵字`ONLY`在表格名稱之前。然而，該參照僅產生出現在已命名資料表中的欄位—子資料表中添加的任何欄位都將被忽略。

可以在表格名稱之後寫入`*`來明確指定包含後代表格，而不是在表格名稱之前寫入`ONLY`。因為搜索後代表格現在始終是默認行為，沒有真正的理由再使用此語法。但是，支持它是為了與舊版本的兼容性。

### **7.2.1.1. 聯接的資料表**

聯接的資料表（joined table）是一個根據特定聯接型別的規則從兩個（真實的或被衍生的）其他資料表衍生的資料表。可以使用 Inner、outer、及cross-join 。聯接資料表的一般語法是

```text
T1 join_type T2 [ join_condition ]
```

所有型別的聯接可以鏈結或嵌套在一起： _`T1`_ and _`T2`_ 中的一個或兩個都可以被聯接資料表。可以在`JOIN`子句周圍使用括號來控制聯接順序。在沒有括號的情況下，`JOIN`子句從左到右嵌套。

**聯接型別**

`Cross join`

```sql
T1 CROSS JOIN T2
```
對於從 _`T1`_ and _`T2`_ 的列的每種可能的組合(即笛卡爾積), 聯接的資料表將包含一個由 _`T1`_ 所有欄其次是 _`T2`_ 所有欄組成的列。如果資料表分別有 _N_ 列及 _M_ 列， 聯接表將具有 _N \* M_ 列。

`FROM` _`T1`_` CROSS JOIN` _`T2`_ 相當於 `FROM` _`T1`_ `INNER JOIN` _`T2`_ `ON TRUE`（見下文。）它也等同於 `FROM` _`T1`_`,` _`T2`_。

{% hint style="info" %}
**注意**

當出現兩個以上的表時，後者的等價關係並不完全成立，因為`JOIN`的綁定比逗號更緊密。例如，`FROM` _`T1`_ `CROSS JOIN` _`T2`_ `INNER JOIN` _`T3`_ `ON` _`condition`_ 不同於`FROM` _`T1`_`,` _`T2`_ `INNER JOIN` _`T3`_ `ON` _`condition`_ 因為 _`condition`_ 可以第一種情況中但不能在第二個情況中參照 _`T1`_ 。
{% endhint %}

`Qualified joins`

```text
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 ON boolean_expression
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 USING ( join column list )
T1 NATURAL { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2
```

單詞 `INNER` 及 `OUTER`在所有形式中都是可選的。`INNER` 是默認值； `LEFT`、`RIGHT`及 `FULL` 表示外部聯接。

在 `ON` or `USING`子句中指定 _join condition_ ，或由單詞`NATURAL`隱式指定。聯接條件決定兩個來源資料表中的哪些列被視為“匹配”，如下面詳細的說明。

限定聯接（qualified joins）的可能型別為：

`INNER JOIN`

對於`T1`的每一列 `R1` ，聯接表有一列在`T2`中的每一列中滿足`R1`的聯接條件。

`LEFT OUTER JOIN`

首先，執行內部聯接。然後，對於`T1`中每一列與`T2`中任何列不滿足聯接條件，聯接列在`T2`的欄中添加空值。因此，對於`T1`中的每一列聯接表始終至少具有一列。

`RIGHT OUTER JOIN`

首先，執行內部聯接。 然後，對於`T2`中每一列與`T1`中任何列不滿足聯接條件，聯接列在`T1`的欄中添加空值。這是左聯接的反面：對於`T2`中的每一列結果表將始終有一列。

`FULL OUTER JOIN`

首先，執行內部聯接。然後，對於`T1`中每一列與`T2`中任何列不滿足聯接條件，聯接列在`T2`的欄中添加空值。另外，對於`T2`中每一列與`T1`中任何列不滿足聯接條件，聯接列在`T1`的欄中添加空值。

`ON`子句是最通用種類的聯接條件：它採用與`WHERE`子句中使用的種類相同的Boolean值表示式。如果 `ON`表示式評估為真值，來自 _`T1`_ 和 _`T2`_ 的一對資料列匹配。

`USING` 子句是一種簡寫形式，可讓您在特定的情況充分利用，即在聯接兩端使用相同的名稱聯接欄位。它使用逗號分隔的共享欄位名稱串列並形成一個包括每個條件相等性比較的聯接條件。例如，將 _`T1`_ 和 _`T2`_ 與 `USING (a, b)` 進行聯接會產生聯接條件`ON` _`T1`_`.a =`_`T2`_`.a AND`_`T1`_`.b =`_`T2`_`.b`。

此外，`JOIN USING`的輸出抑制多餘的欄：無需打印兩個匹配的欄，因為它們必須具有相等的值。儘管`JOIN ON`會產生 _`T1`_ 的所有欄其次是 _`T2`_ 的所有欄，`JOIN USING`為每個列出的欄配對（按照列出的順序）產生一個輸出欄，其次是 _`T1`_ 的所有剩餘欄，其次是 _`T2`_ 的所有剩餘欄。

最後，`NATURAL`是`USING`的簡寫形式：它形成一個由出現在兩個輸入資料表中的所有欄位名稱組成的`USING`串列。 與`USING`一樣，這些欄在輸出表中僅出現一次。如果沒有共用的欄位名稱，`NATURAL JOIN` 的行為類似於`JOIN ... ON TRUE`，產生外積聯接（cross-product join。

{% hint style="info" %}
**注意**

`USING`對於在聯接關係中變更欄位是相當安全的因為只有列出的欄位被合併。`NATURAL`的風險相當可觀，因為任何綱要（schema）變更為任一導致新的匹配欄位名稱出現的關係，也將會導致聯接合併該新的欄位。
{% endhint %}

綜合以上所述，假設我們有資料表`t1`:

```text
 num | name
-----+------
   1 | a
   2 | b
   3 | c
```

和資料表`t2`:

```text
 num | value
-----+-------
   1 | xxx
   3 | yyy
   5 | zzz
```

然後對於各種聯接我們得到以下結果：

```text
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

以`ON`指定的聯接條件還可以包含與聯接不直接相關的條件。對於某些查詢這可以證明是有用的但需要小心地深思熟慮。例如：

```text
=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num AND t2.value = 'xxx';
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   2 | b    |     |
   3 | c    |     |
(3 rows)
```

請注意，將限制放置在`WHERE`子句中會產生不同的結果：

```text
=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num WHERE t2.value = 'xxx';
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
(1 row)
```

這是因為限制放在 `ON`子句會在聯接**之前**被處理，而限制放在 `WHERE`子句會在聯接**之後**被處理。這與內部聯接無關緊要，但對於外部聯接則很重要。

### **7.2.1.2. 資料表和欄位別名**

可以為資料表和復雜資料表參照給定一個臨時名稱來用在其餘查詢中參照衍生的資料表。這稱為 _資料表別名（table alias）_ 。

要創建資料表別名，請編寫

```sql
FROM table_reference AS alias
```

或者是

```sql
FROM table_reference alias
```

關鍵字`AS`是選擇性的。 _`alias`_ 可以是任何標識符。

資料表別名的典型應用是將短標識符分配給長資料表名稱，以保持連接子句的可讀性。例如：

```sql
SELECT * FROM some_very_long_table_name s JOIN another_fairly_long_name a ON s.id = a.num;
```

以當前查詢而言，別名成為表參照的新名稱 —不允許在查詢其他位置中使用原始名稱引用該表。因此，這是無效的：

```sql
SELECT * FROM my_table AS m WHERE my_table.a > 5;    -- wrong
```

資料表別名主要是為了表示法的方便，但是在將資料表聯接到自身時必須使用它們，例如：

```sql
SELECT * FROM people AS mother JOIN people AS child ON mother.id = child.mother_id;
```

此外，如果表參照是子查詢，則需要別名（詳見[7.2.1.3節](https://docs.postgresql.tw/the-sql-language/queries/table-expressions7-2-1-3-zi-cha-xun)。）

括號被用於解決歧義。在以下範例中，第一條語句將別名`b`分配給`my_table`的第二個實例，但是第二條語句將別名分配給聯接結果：

```sql
SELECT * FROM my_table AS a CROSS JOIN my_table AS b ...
SELECT * FROM (my_table AS a CROSS JOIN my_table) AS b ...
```

資料表別名的另一種形式為資料表欄位以及資料表本身賦予臨時名稱：

```text
FROM table_reference [AS] alias ( column1 [, column2 [, ...]] )
```

如果指定的欄位別名少於實際表中包含的欄位，則不會重命名剩餘的欄位。此語法對於自聯接或子查詢特別有用。

當別名被應用到`JOIN`子句的輸出時，別名將原始名稱隱藏在`JOIN`中。例如：

```sql
SELECT a.* FROM my_table AS a JOIN your_table AS b ON ...
```

是有效的SQL，但是：

```sql
SELECT a.* FROM (my_table AS a JOIN your_table AS b ON ...) AS c
```

是無效的；資料表別名`a`在別名`c`之外並不可見。

### **7.2.1.3. 子查詢**

子查詢指定衍生資料表必須括號括起來必須為資料表分配別名（如[7.2.1.2節](https://docs.postgresql.tw/the-sql-language/queries/table-expressions7-2-1-2-zi-liao-biao-he-lan-wei-bie-ming)。）例如：

```sql
FROM (SELECT * FROM table1) AS alias_name
```

這個例子相當於`FROM table1 AS alias_name`。當子查詢涉及分組或彙總時會出現更有趣的無法簡化為普通聯接的情況。

子查詢也可以是`VALUES`串列：

```sql
FROM (VALUES ('anne', 'smith'), ('bob', 'jones'), ('joe', 'blow'))
     AS names(first, last)
```

同樣，需要資料表別名。為`VALUES`串列的欄位分配別名是選擇性的，但這是一種好的實踐。有關更多訊息，請參見[7.7節](https://docs.postgresql.tw/the-sql-language/queries/values-lists)。

### **7.2.1.4. 資料表函數**

資料表函數是產生一組資料列的函數，這些列由基本資料型別（標量型別）或複合數資料型別（資料表列）組成。在查詢的 `FROM` 子句中，它們像資料表、檢視表或子查詢一樣使用。資料表函數返回的欄位以資料表欄位、檢視表或子查詢相同的方式可以包含在`SELECT`、`JOIN`或`WHERE`子句中。

資料表函數也可以使用`ROWS FROM`語法進行組合，以並行欄位返回結果；在這種情況下結果列的數量是最大的函數結果，較小的結果將填充空值來匹配。

```text
function_call [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
ROWS FROM( function_call [, ... ] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
```

如果`WITH ORDINALITY`子句被指定，一個額外的`bigint`型別欄位将被添加到函數結果欄位。這個欄位從1開始為函數結果集合的列作編號（這是SQL標準語法`UNNEST ... WITH ORDINALITY`的概括。）在默認情況下，序數欄位欄位被稱為`ordinality`，但可以使用`AS`子句分配不同的欄位名稱給它。

特別的資料表函數`UNNEST`也許伴隨著任意數量的陣列參數被調用，並且他返回一個對應數量的欄位，就如同分別對每個參數調用`UNNEST`（[9.19節](https://docs.postgresql.tw/the-sql-language/functions-and-operators/array-functions-and-operators)）並使用`ROWS FROM`建構將其組合在一起。

```text
UNNEST( array_expression [, ... ] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
```

如果沒有指定 _`table_alias`_，該函數名稱被用作資料表名稱；
在`ROWS FROM`建構的情況中使用第一個函數的名稱。

如果沒有提供欄位別名，則對於返回一個基礎資料型別的函數，該欄位名稱也與函數名稱相同。對於返回一個複合資料型別的函數，該結果欄位取得該型別個別屬性的名稱。

舉一些範例：

```sql
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

在一些情況中他對定義能根據它們的調用方式返回不同欄位集合的資料表函數很有用。為了要支持這情況，資料表函數可以被宣告為返回偽型別 `record`。在查詢中使用此種函數時，在查詢本身中必須指定預期的資料列結構，以便讓系統知道如何解析和規劃查詢。這種語法看起來像是：

```text
function_call [AS] alias (column_definition [, ... ])
function_call AS [alias] (column_definition [, ... ])
ROWS FROM( ... function_call AS (column_definition [, ... ]) [, ... ] )
```

沒有使用`ROWS FROM()`語法時，_`column_definition`_ 串列替換原本能被附加到`FROM`項目的欄位別名串列；在欄位定義中的名稱充當欄位別名。當使用`ROWS FROM()`語法時，_`column_definition`_ 串列能被分別附加到每個成員函數；或者如果只有一個成員函數且沒有`WITH ORDINALITY`子句，能編寫_`column_definition`_ 串列來代替`ROWS FROM()`之後的欄位別名串列。

考慮以下範例:

```sql
SELECT *
    FROM dblink('dbname=mydb', 'SELECT proname, prosrc FROM pg_proc')
      AS t1(proname name, prosrc text)
    WHERE proname LIKE 'bytea%';
```

[dblink函數](https://www.postgresql.org/docs/13/contrib-dblink-function.html)（[dblink模組](https://docs.postgresql.tw/appendixes/additional-supplied-modules/dblink)的一部分）執行遠端查詢。它宣告返回`record`，因為它可以用於任何種類的查詢。實際的欄位集合必須被指定在調用的查詢以便讓解析器知道，舉例來說，`*`應該擴展成什麼。

### **7.2.1.5. LATERAL子查詢**

出現在`FROM`中的子查詢的前面可以有關鍵字`LATERAL`。這允許它們參照前面`FROM`項目提供的欄位。（沒有`LATERAL`的話，每一個子查詢被個別評估所以不能交叉參照任何其他`FROM`項目。）

出現在`FROM`中的資料表函數的前面也能有關鍵字`LATERAL`，但對於函數來說該關鍵字是選擇性的；在任何情況下該函數的參數能包含前面`FROM`項目提供的欄位參照。

`LATERAL`項目能出現在`FROM`串列的頂層，或在`JOIN`樹之中。在後面的情況下在`JOIN`右邊的`LATERAL`也能引用在`JOIN`左邊的任何項目。

當`FROM`項目包含`LATERAL`交叉參照，評估過程如下：
對於該`FROM`項目每一個提供交叉參照後欄位的列，或是多個`FROM`項目之提供欄位的列集合，將使用該欄位的列或列集合值來評估`LATERAL`項目。結果資料列照常與運算出它們的資料列聯接。對於欄位來源表的每一列或列集合重複此操作。

`LATERAL`的一個簡單範例是：

```sql
SELECT * FROM foo, LATERAL (SELECT * FROM bar WHERE bar.id = foo.bar_id) ss;
```

這不是特別有用，因為它與完全常規的結果完全相同

```sql
SELECT * FROM foo, bar WHERE bar.id = foo.bar_id;
```

`LATERAL`主要有用的時機是在運算資料列聯接而需要交叉參照後欄位的時候。典型的應用是提供一個參數值給會返回集合的函數。舉例來說，假如`vertices(polygon)`返回多邊形的頂點集合，我們可以經由以下方式識別存儲在表中多邊形的近似頂點：

```sql
SELECT p1.id, p2.id, v1, v2
FROM polygons p1, polygons p2,
     LATERAL vertices(p1.poly) v1,
     LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

這個查詢也可以寫成

```sql
SELECT p1.id, p2.id, v1, v2
FROM polygons p1 CROSS JOIN LATERAL vertices(p1.poly) v1,
     polygons p2 CROSS JOIN LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

或者以其他幾種等效公式表示。（如前所述，關鍵字`LATERAL`在此範例中是不必要的，但為了清楚起見而使用它。）

即使`LATERAL`子查詢沒有產生資料列，通常特別便利將`LEFT JOIN`添加到`LATERAL`子查詢，使得來源資料列將出現在結果中。舉例來說，如果`get_product_names()`返回製造商生產的產品名稱，但是我們表中的某些製造商目前未生產任何產品，我們可以像這樣找出：

```sql
SELECT m.name
FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id) pname ON true
WHERE pname IS NULL;
```

## 7.2.2. `WHERE`子句

The syntax of the [`WHERE`](https://www.postgresql.org/docs/13/sql-select.html#SQL-WHERE) clause is

```text
WHERE search_condition
```

where _`search_condition`_ is any value expression \(see [Section 4.2](https://www.postgresql.org/docs/13/sql-expressions.html)\) that returns a value of type `boolean`.

After the processing of the `FROM` clause is done, each row of the derived virtual table is checked against the search condition. If the result of the condition is true, the row is kept in the output table, otherwise \(i.e., if the result is false or null\) it is discarded. The search condition typically references at least one column of the table generated in the `FROM` clause; this is not required, but otherwise the `WHERE` clause will be fairly useless.

#### Note

The join condition of an inner join can be written either in the `WHERE` clause or in the `JOIN` clause. For example, these table expressions are equivalent:

```text
FROM a, b WHERE a.id = b.id AND b.val > 5
```

and:

```text
FROM a INNER JOIN b ON (a.id = b.id) WHERE b.val > 5
```

or perhaps even:

```text
FROM a NATURAL JOIN b WHERE b.val > 5
```

Which one of these you use is mainly a matter of style. The `JOIN` syntax in the `FROM` clause is probably not as portable to other SQL database management systems, even though it is in the SQL standard. For outer joins there is no choice: they must be done in the `FROM` clause. The `ON` or `USING` clause of an outer join is _not_ equivalent to a `WHERE` condition, because it results in the addition of rows \(for unmatched input rows\) as well as the removal of rows in the final result.

Here are some examples of `WHERE` clauses:

```text
SELECT ... FROM fdt WHERE c1 > 5

SELECT ... FROM fdt WHERE c1 IN (1, 2, 3)

SELECT ... FROM fdt WHERE c1 IN (SELECT c1 FROM t2)

SELECT ... FROM fdt WHERE c1 IN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10)

SELECT ... FROM fdt WHERE c1 BETWEEN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10) AND 100

SELECT ... FROM fdt WHERE EXISTS (SELECT c1 FROM t2 WHERE c2 > fdt.c1)
```

`fdt` is the table derived in the `FROM` clause. Rows that do not meet the search condition of the `WHERE` clause are eliminated from `fdt`. Notice the use of scalar subqueries as value expressions. Just like any other query, the subqueries can employ complex table expressions. Notice also how `fdt` is referenced in the subqueries. Qualifying `c1` as `fdt.c1` is only necessary if `c1` is also the name of a column in the derived input table of the subquery. But qualifying the column name adds clarity even when it is not needed. This example shows how the column naming scope of an outer query extends into its inner queries.

## 7.2.3. `GROUP BY`及 `HAVING`子句

After passing the `WHERE` filter, the derived input table might be subject to grouping, using the `GROUP BY` clause, and elimination of group rows using the `HAVING` clause.

```text
SELECT select_list
    FROM ...
    [WHERE ...]
    GROUP BY grouping_column_reference [, grouping_column_reference]...
```

The [`GROUP BY`](https://www.postgresql.org/docs/13/sql-select.html#SQL-GROUPBY) clause is used to group together those rows in a table that have the same values in all the columns listed. The order in which the columns are listed does not matter. The effect is to combine each set of rows having common values into one group row that represents all rows in the group. This is done to eliminate redundancy in the output and/or compute aggregates that apply to these groups. For instance:

```text
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

In the second query, we could not have written `SELECT * FROM test1 GROUP BY x`, because there is no single value for the column `y` that could be associated with each group. The grouped-by columns can be referenced in the select list since they have a single value in each group.

In general, if a table is grouped, columns that are not listed in `GROUP BY` cannot be referenced except in aggregate expressions. An example with aggregate expressions is:

```text
=> SELECT x, sum(y) FROM test1 GROUP BY x;
 x | sum
---+-----
 a |   4
 b |   5
 c |   2
(3 rows)
```

Here `sum` is an aggregate function that computes a single value over the entire group. More information about the available aggregate functions can be found in [Section 9.21](https://www.postgresql.org/docs/13/functions-aggregate.html).

#### Tip

Grouping without aggregate expressions effectively calculates the set of distinct values in a column. This can also be achieved using the `DISTINCT` clause \(see [Section 7.3.3](https://www.postgresql.org/docs/13/queries-select-lists.html#QUERIES-DISTINCT)\).

Here is another example: it calculates the total sales for each product \(rather than the total sales of all products\):

```text
SELECT product_id, p.name, (sum(s.units) * p.price) AS sales
    FROM products p LEFT JOIN sales s USING (product_id)
    GROUP BY product_id, p.name, p.price;
```

In this example, the columns `product_id`, `p.name`, and `p.price` must be in the `GROUP BY` clause since they are referenced in the query select list \(but see below\). The column `s.units` does not have to be in the `GROUP BY` list since it is only used in an aggregate expression \(`sum(...)`\), which represents the sales of a product. For each product, the query returns a summary row about all sales of the product.

If the products table is set up so that, say, `product_id` is the primary key, then it would be enough to group by `product_id` in the above example, since name and price would be _functionally dependent_ on the product ID, and so there would be no ambiguity about which name and price value to return for each product ID group.

In strict SQL, `GROUP BY` can only group by columns of the source table but PostgreSQL extends this to also allow `GROUP BY` to group by columns in the select list. Grouping by value expressions instead of simple column names is also allowed.

If a table has been grouped using `GROUP BY`, but only certain groups are of interest, the `HAVING` clause can be used, much like a `WHERE` clause, to eliminate groups from the result. The syntax is:

```text
SELECT select_list FROM ... [WHERE ...] GROUP BY ... HAVING boolean_expression
```

Expressions in the `HAVING` clause can refer both to grouped expressions and to ungrouped expressions \(which necessarily involve an aggregate function\).

Example:

```text
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

Again, a more realistic example:

```text
SELECT product_id, p.name, (sum(s.units) * (p.price - p.cost)) AS profit
    FROM products p LEFT JOIN sales s USING (product_id)
    WHERE s.date > CURRENT_DATE - INTERVAL '4 weeks'
    GROUP BY product_id, p.name, p.price, p.cost
    HAVING sum(p.price * s.units) > 5000;
```

In the example above, the `WHERE` clause is selecting rows by a column that is not grouped \(the expression is only true for sales during the last four weeks\), while the `HAVING` clause restricts the output to groups with total gross sales over 5000. Note that the aggregate expressions do not necessarily need to be the same in all parts of the query.

If a query contains aggregate function calls, but no `GROUP BY` clause, grouping still occurs: the result is a single group row \(or perhaps no rows at all, if the single row is then eliminated by `HAVING`\). The same is true if it contains a `HAVING` clause, even without any aggregate function calls or `GROUP BY` clause.

## 7.2.4. `GROUPING SETS`、`CUBE`及 `ROLLUP`

More complex grouping operations than those described above are possible using the concept of _grouping sets_. The data selected by the `FROM` and `WHERE` clauses is grouped separately by each specified grouping set, aggregates computed for each group just as for simple `GROUP BY` clauses, and then the results returned. For example:

```text
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

Each sublist of `GROUPING SETS` may specify zero or more columns or expressions and is interpreted the same way as though it were directly in the `GROUP BY` clause. An empty grouping set means that all rows are aggregated down to a single group \(which is output even if no input rows were present\), as described above for the case of aggregate functions with no `GROUP BY` clause.

References to the grouping columns or expressions are replaced by null values in result rows for grouping sets in which those columns do not appear. To distinguish which grouping a particular output row resulted from, see [Table 9.59](https://www.postgresql.org/docs/13/functions-aggregate.html#FUNCTIONS-GROUPING-TABLE).

A shorthand notation is provided for specifying two common types of grouping set. A clause of the form

```text
ROLLUP ( e1, e2, e3, ... )
```

represents the given list of expressions and all prefixes of the list including the empty list; thus it is equivalent to

```text
GROUPING SETS (
    ( e1, e2, e3, ... ),
    ...
    ( e1, e2 ),
    ( e1 ),
    ( )
)
```

This is commonly used for analysis over hierarchical data; e.g., total salary by department, division, and company-wide total.

A clause of the form

```text
CUBE ( e1, e2, ... )
```

represents the given list and all of its possible subsets \(i.e., the power set\). Thus

```text
CUBE ( a, b, c )
```

is equivalent to

```text
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

The individual elements of a `CUBE` or `ROLLUP` clause may be either individual expressions, or sublists of elements in parentheses. In the latter case, the sublists are treated as single units for the purposes of generating the individual grouping sets. For example:

```text
CUBE ( (a, b), (c, d) )
```

is equivalent to

```text
GROUPING SETS (
    ( a, b, c, d ),
    ( a, b       ),
    (       c, d ),
    (            )
)
```

and

```text
ROLLUP ( a, (b, c), d )
```

is equivalent to

```text
GROUPING SETS (
    ( a, b, c, d ),
    ( a, b, c    ),
    ( a          ),
    (            )
)
```

The `CUBE` and `ROLLUP` constructs can be used either directly in the `GROUP BY` clause, or nested inside a `GROUPING SETS` clause. If one `GROUPING SETS` clause is nested inside another, the effect is the same as if all the elements of the inner clause had been written directly in the outer clause.

If multiple grouping items are specified in a single `GROUP BY` clause, then the final list of grouping sets is the cross product of the individual items. For example:

```text
GROUP BY a, CUBE (b, c), GROUPING SETS ((d), (e))
```

is equivalent to

```text
GROUP BY GROUPING SETS (
    (a, b, c, d), (a, b, c, e),
    (a, b, d),    (a, b, e),
    (a, c, d),    (a, c, e),
    (a, d),       (a, e)
)
```

#### Note

The construct `(a, b)` is normally recognized in expressions as a [row constructor](https://www.postgresql.org/docs/13/sql-expressions.html#SQL-SYNTAX-ROW-CONSTRUCTORS). Within the `GROUP BY` clause, this does not apply at the top levels of expressions, and `(a, b)` is parsed as a list of expressions as described above. If for some reason you _need_ a row constructor in a grouping expression, use `ROW(a, b)`.

## 7.2.5. 窗函數處理

If the query contains any window functions \(see [Section 3.5](https://www.postgresql.org/docs/13/tutorial-window.html), [Section 9.22](https://www.postgresql.org/docs/13/functions-window.html) and [Section 4.2.8](https://www.postgresql.org/docs/13/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)\), these functions are evaluated after any grouping, aggregation, and `HAVING` filtering is performed. That is, if the query uses any aggregates, `GROUP BY`, or `HAVING`, then the rows seen by the window functions are the group rows instead of the original table rows from `FROM`/`WHERE`.

When multiple window functions are used, all the window functions having syntactically equivalent `PARTITION BY` and `ORDER BY` clauses in their window definitions are guaranteed to be evaluated in a single pass over the data. Therefore they will see the same sort ordering, even if the `ORDER BY` does not uniquely determine an ordering. However, no guarantees are made about the evaluation of functions having different `PARTITION BY` or `ORDER BY` specifications. \(In such cases a sort step is typically required between the passes of window function evaluations, and the sort is not guaranteed to preserve ordering of rows that its `ORDER BY` sees as equivalent.\)

Currently, window functions always require presorted data, and so the query output will be ordered according to one or another of the window functions' `PARTITION BY`/`ORDER BY` clauses. It is not recommended to rely on this, however. Use an explicit top-level `ORDER BY` clause if you want to be sure the results are sorted in a particular way.  


