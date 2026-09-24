<a id="XFUNC-SQL"></a>
## 36.5. 查詢語言（SQL）函式 [#](#XFUNC-SQL)

[36.5.1. SQL 函式的引數](xfunc-sql.md#XFUNC-SQL-FUNCTION-ARGUMENTS)

[36.5.2. 基礎型別上的 SQL 函式](xfunc-sql.md#XFUNC-SQL-BASE-FUNCTIONS)

[36.5.3. 複合型別上的 SQL 函式](xfunc-sql.md#XFUNC-SQL-COMPOSITE-FUNCTIONS)

[36.5.4. 具有輸出參數的 SQL 函式](xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS)

[36.5.5. 具有輸出參數的 SQL 程序](xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS-PROC)

[36.5.6. 具有可變數量引數的 SQL 函式](xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS)

[36.5.7. 具有引數預設值的 SQL 函式](xfunc-sql.md#XFUNC-SQL-PARAMETER-DEFAULTS)

[36.5.8. 作為資料表來源的 SQL 函式](xfunc-sql.md#XFUNC-SQL-TABLE-FUNCTIONS)

[36.5.9. 傳回集合的 SQL 函式](xfunc-sql.md#XFUNC-SQL-FUNCTIONS-RETURNING-SET)

[36.5.10. 傳回 `TABLE` 的 SQL 函式](xfunc-sql.md#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE)

[36.5.11. 多型 SQL 函式](xfunc-sql.md#XFUNC-SQL-POLYMORPHIC-FUNCTIONS)

[36.5.12. 具有定序的 SQL 函式](xfunc-sql.md#XFUNC-SQL-COLLATIONS)

<a id="id-1.8.3.8.2"></a>

SQL 函式會執行一份任意的 SQL 陳述式清單，並傳回
清單中最後一則查詢的結果。
在簡單（非集合）的
情況下，會傳回最後一則查詢結果的第一筆資料列。
（請記住，除非你使用 `ORDER BY`，否則多筆資料列
結果中「第一筆資料列」的定義並不明確。）
若最後一則查詢恰好
完全沒有傳回任何資料列，則會傳回 null 值。

或者，也可以將 SQL 函式宣告為傳回一個集合（也就是
多筆資料列），做法是將函式的傳回型別指定為 `SETOF
sometype`，或者等效地將其宣告為
`RETURNS TABLE(columns)`。在這種情況下，
最後一則查詢結果的所有資料列都會被傳回。詳情
於下方說明。

SQL 函式的主體必須是以分號分隔的一份
SQL 陳述式清單。最後一個陳述式後面的分號是
選擇性的。除非函式被宣告為傳回
`void`，否則最後一個陳述式必須是 `SELECT`，
或是帶有 `RETURNING` 子句的
`INSERT`、`UPDATE`、
`DELETE` 或 `MERGE`。

SQL
語言中的任何指令集合，都可以打包在一起並定義為一個函式。
除了 `SELECT` 查詢之外，這些指令還可以包括資料
修改查詢（`INSERT`、
`UPDATE`、`DELETE` 以及
`MERGE`），
以及其他 SQL 指令。（在 SQL 函式中不能使用交易控制
指令，例如 `COMMIT`、`SAVEPOINT`，
也不能使用某些公用程式指令，例如 `VACUUM`。）
不過，最後一個
指令必須是 `SELECT`，或是帶有 `RETURNING`
子句、傳回函式傳回型別所指定內容的指令。
另外，若你
想定義一個會執行動作、但沒有實用傳回值的 SQL 函式，
可以將其定義為傳回 `void`。
舉例來說，以下這個函式會從
`emp` 資料表中移除薪資為負值的資料列：

```

CREATE FUNCTION clean_emp() RETURNS void AS '
    DELETE FROM emp
        WHERE salary < 0;
' LANGUAGE SQL;

SELECT clean_emp();

 clean_emp
-----------

(1 row)
```

你也可以將其寫成一個程序（procedure），藉此避免傳回型別
的問題。舉例來說：

```

CREATE PROCEDURE clean_emp() AS '
    DELETE FROM emp
        WHERE salary < 0;
' LANGUAGE SQL;

CALL clean_emp();
```

在像這樣的簡單情況下，傳回 `void` 的函式與
程序之間的差異，主要只是風格上的不同。不過，
程序提供了函式所沒有的額外功能，例如交易
控制。此外，程序是 SQL 標準的一部分，
而傳回 `void` 則是 PostgreSQL 的擴充功能。

`CREATE FUNCTION` 指令的語法要求
函式主體必須以字串常值的形式撰寫。通常
使用 dollar quoting（以美元符號 $ 定界的字串常值語法，請參閱[4.1.2.4 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)）來表示這個字串常值是最方便的做法。
若你選擇使用一般的單引號字串常值語法，
則必須在函式主體中將單引號（`'`）與反斜線
（`\`）（假設使用逸出字串語法）各自重複一次
（請參閱[4.1.2.1 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)）。

<a id="XFUNC-SQL-FUNCTION-ARGUMENTS"></a>

### 36.5.1. SQL 函式的引數 [#](#XFUNC-SQL-FUNCTION-ARGUMENTS)

<a id="id-1.8.3.8.9.2"></a>

SQL 函式的引數可以在函式主體中
使用名稱或編號來參照。以下會示範這兩種方法的
範例。

若要使用名稱，請將函式引數宣告為具有名稱，
然後直接在函式主體中寫出該名稱即可。若此引數名稱
與函式內目前 SQL 指令中的任何欄位名稱相同，
則欄位名稱會優先。若要覆寫這項行為，可以用函式本身的名稱
來限定此引數名稱，也就是
`function_name.argument_name`。
（若這樣做會與某個已限定的欄位名稱衝突，欄位名稱
仍然會優先。你可以在 SQL 指令中為該資料表選擇不同的別名，
以避免這種歧義。）

在較早的數字表示法中，引數是以
`$n` 語法來參照的：`$1` 代表第一個輸入
引數，`$2` 代表第二個，依此類推。無論該引數
是否已被宣告為具有名稱，這種方式都可以運作。

若某個引數是複合型別，則可以使用點記法，
例如 `argname.fieldname` 或
`$1.fieldname`，來存取該引數的屬性。同樣地，
你可能需要以函式名稱來限定引數名稱，才能讓使用引數名稱的形式
不產生歧義。

SQL 函式的引數只能被當作資料值使用，
不能被當作識別字使用。因此，舉例來說，以下這樣是合理的：

```

INSERT INTO mytable VALUES ($1);
```

但以下這樣則無法運作：

```

INSERT INTO $1 VALUES (42);
```

### 注意

在 PostgreSQL 9.2 中新增了以名稱參照
SQL 函式引數的能力。要用於較舊伺服器的函式
則必須使用 `$n` 表示法。

<a id="XFUNC-SQL-BASE-FUNCTIONS"></a>

### 36.5.2. 基礎型別上的 SQL 函式 [#](#XFUNC-SQL-BASE-FUNCTIONS)

最簡單的 SQL 函式沒有任何引數，
單純傳回一個基礎型別，例如 `integer`：

```

CREATE FUNCTION one() RETURNS integer AS $$
    SELECT 1 AS result;
$$ LANGUAGE SQL;

-- Alternative syntax for string literal:
CREATE FUNCTION one() RETURNS integer AS '
    SELECT 1 AS result;
' LANGUAGE SQL;

SELECT one();

 one
-----
   1
```

請注意，我們在函式主體中為函式的結果定義了一個欄位別名
（名稱為 `result`），但這個欄位別名在函式
外部並不可見。因此，結果被標示為 `one`，
而不是 `result`。

定義以基礎型別作為引數的 SQL 函式
幾乎同樣簡單：

```

CREATE FUNCTION add_em(x integer, y integer) RETURNS integer AS $$
    SELECT x + y;
$$ LANGUAGE SQL;

SELECT add_em(1, 2) AS answer;

 answer
--------
      3
```

或者，我們也可以不使用引數名稱，
改用編號：

```

CREATE FUNCTION add_em(integer, integer) RETURNS integer AS $$
    SELECT $1 + $2;
$$ LANGUAGE SQL;

SELECT add_em(1, 2) AS answer;

 answer
--------
      3
```

以下是一個更實用的函式，可用於從
銀行帳戶中扣款：

```

CREATE FUNCTION tf1 (accountno integer, debit numeric) RETURNS numeric AS $$
    UPDATE bank
        SET balance = balance - debit
        WHERE accountno = tf1.accountno;
    SELECT 1;
$$ LANGUAGE SQL;
```

使用者可以執行此函式，從帳戶 17 中
扣除 $100.00，方式如下：

```

SELECT tf1(17, 100.0);
```

在此範例中，我們為第一個引數選擇了名稱
`accountno`，但這與 `bank` 資料表中某個欄位的
名稱相同。在 `UPDATE` 指令中，
`accountno` 指的是欄位 `bank.accountno`，
因此必須使用 `tf1.accountno` 來指涉此引數。
我們當然也可以為引數使用不同的名稱，以避免這個問題。

實務上，比起單純傳回常數 1，大家可能會希望
函式能傳回更有用的結果，因此更常見的定義
方式如下：

```

CREATE FUNCTION tf1 (accountno integer, debit numeric) RETURNS numeric AS $$
    UPDATE bank
        SET balance = balance - debit
        WHERE accountno = tf1.accountno;
    SELECT balance FROM bank WHERE accountno = tf1.accountno;
$$ LANGUAGE SQL;
```

這會調整餘額並傳回新的餘額。
同樣的效果也可以用 `RETURNING` 在單一指令中完成：

```

CREATE FUNCTION tf1 (accountno integer, debit numeric) RETURNS numeric AS $$
    UPDATE bank
        SET balance = balance - debit
        WHERE accountno = tf1.accountno
    RETURNING balance;
$$ LANGUAGE SQL;
```

若 SQL 函式中最後的 `SELECT` 或 `RETURNING`
子句所傳回的結果，與函式所宣告的傳回
型別不完全相符，若可以透過隱含轉型或指派轉型
來達成，PostgreSQL 會自動將該值
轉型為所需的型別。否則，你就必須自行撰寫明確的轉型。
舉例來說，假設我們希望
先前的 `add_em` 函式改為傳回
`float8` 型別。只要這樣寫就足夠了：

```

CREATE FUNCTION add_em(integer, integer) RETURNS float8 AS $$
    SELECT $1 + $2;
$$ LANGUAGE SQL;
```

因為 `integer` 的加總結果可以隱含地轉型
為 `float8`。
（關於轉型的更多資訊，請參閱[第 10 章](../../the-sql-language/typeconv/README.md)或 [CREATE CAST](../../reference/sql-commands/sql-createcast.md)。）

<a id="XFUNC-SQL-COMPOSITE-FUNCTIONS"></a>

### 36.5.3. 複合型別上的 SQL 函式 [#](#XFUNC-SQL-COMPOSITE-FUNCTIONS)

在撰寫引數為複合型別的函式時，我們不僅必須指定
要使用哪一個引數，還必須指定該引數所需要的屬性
（欄位）。舉例來說，假設
`emp` 是一個包含員工資料的資料表，因此
也是該資料表每一列複合型別的名稱。以下
是一個名為 `double_salary` 的函式，用來計算某人的
薪資若加倍後會是多少：

```

CREATE TABLE emp (
    name        text,
    salary      numeric,
    age         integer,
    cubicle     point
);

INSERT INTO emp VALUES ('Bill', 4200, 45, '(2,1)');

CREATE FUNCTION double_salary(emp) RETURNS numeric AS $$
    SELECT $1.salary * 2 AS salary;
$$ LANGUAGE SQL;

SELECT name, double_salary(emp.*) AS dream
    FROM emp
    WHERE emp.cubicle ~= point '(2,1)';

 name | dream
------+-------
 Bill |  8400
```

請注意這裡使用 `$1.salary` 語法
來選取引數資料列值的其中一個欄位。另外也請注意
呼叫此函式的 `SELECT` 指令
如何使用 *`table_name`*`.*`
來選取資料表目前整列的內容作為複合值。這個資料表
資料列，也可以只用資料表名稱來參照，
像這樣：

```

SELECT name, double_salary(emp) AS dream
    FROM emp
    WHERE emp.cubicle ~= point '(2,1)';
```

不過這種用法已被淘汰，因為它很容易造成混淆。
（關於資料表資料列之複合值的這兩種表示法的詳情，
請參閱[8.16.5 節](../../the-sql-language/datatype/rowtypes.md#ROWTYPES-USAGE)。）

有時候，即時建構一個複合引數值
會很方便。這可以透過 `ROW` 建構式來完成。
舉例來說，我們可以調整要傳遞給函式的資料：

```

SELECT name, double_salary(ROW(name, salary*1.1, age, cubicle)) AS dream
    FROM emp;
```

我們也可以建立一個傳回複合型別的函式。
以下範例是一個
傳回單一 `emp` 資料列的函式：

```

CREATE FUNCTION new_emp() RETURNS emp AS $$
    SELECT text 'None' AS name,
        1000.0 AS salary,
        25 AS age,
        point '(2,2)' AS cubicle;
$$ LANGUAGE SQL;
```

在此範例中，我們為每個屬性都指定了
常數值，但這些常數也完全可以替換成
任何運算式。

關於定義此函式，有兩個重要事項需要注意：

* 查詢中選取清單的順序，必須與
  複合型別中欄位出現的順序完全一致。
  （如同我們在上面所做的那樣為欄位命名，
  對系統而言並不重要。）
* 我們必須確保每個運算式的型別，都可以轉型為複合型別中
  對應欄位的型別。
  否則我們會得到類似這樣的錯誤：

  ```


  ERROR:  return type mismatch in function declared to return emp
  DETAIL:  Final statement returns text instead of point at column 4.
  ```

  與基礎型別的情況一樣，系統不會自動插入明確的
  轉型，只會處理隱含轉型或指派轉型。

定義同一個函式的另一種方式是：

```

CREATE FUNCTION new_emp() RETURNS emp AS $$
    SELECT ROW('None', 1000.0, 25, '(2,2)')::emp;
$$ LANGUAGE SQL;
```

這裡我們撰寫了一個只傳回單一欄位、且該欄位型別
正確為複合型別的 `SELECT`。在這種情況下，這樣做
其實並沒有比較好，但在某些情況下卻是一種方便的
替代做法——舉例來說，若我們需要藉由呼叫
另一個會傳回所需複合值的函式來計算結果時。
另一個例子是，若我們要撰寫一個
傳回以複合型別為基礎之網域（domain）、而非單純複合型別的函式，
就一定需要將其寫成傳回單一欄位的形式，
因為沒有辦法對整列結果進行強制轉型。

我們可以直接呼叫這個函式，方法是在
值運算式中使用它：

```

SELECT new_emp();

         new_emp
--------------------------
 (None,1000.0,25,"(2,2)")
```

或者將其當作資料表函式來呼叫：

```

SELECT * FROM new_emp();

 name | salary | age | cubicle
------+--------+-----+---------
 None | 1000.0 |  25 | (2,2)
```

第二種方式在[36.5.8 節](xfunc-sql.md#XFUNC-SQL-TABLE-FUNCTIONS)中有更完整的說明。

當你使用一個傳回複合型別的函式時，
你可能只想要其結果中的一個欄位（屬性）。
你可以用類似這樣的語法來達成：

```

SELECT (new_emp()).name;

 name
------
 None
```

這裡需要額外的括號，以免剖析器產生
混淆。若你試著不加括號來這樣做，會得到類似這樣的結果：

```

SELECT new_emp().name;
ERROR:  syntax error at or near "."
LINE 1: SELECT new_emp().name;
                        ^
```

另一個選擇是使用函式表示法來擷取屬性：

```

SELECT name(new_emp());

 name
------
 None
```

如[8.16.5 節](../../the-sql-language/datatype/rowtypes.md#ROWTYPES-USAGE)所述，欄位表示法與
函式表示法是等效的。

使用傳回複合型別之函式的另一種方式，是將
其結果傳遞給另一個接受正確資料列型別作為輸入的函式：

```

CREATE FUNCTION getname(emp) RETURNS text AS $$
    SELECT $1.name;
$$ LANGUAGE SQL;

SELECT getname(new_emp());
 getname
---------
 None
(1 row)
```

<a id="XFUNC-OUTPUT-PARAMETERS"></a>

### 36.5.4. 具有輸出參數的 SQL 函式 [#](#XFUNC-OUTPUT-PARAMETERS)

<a id="id-1.8.3.8.12.2"></a>

描述函式結果的另一種方式，是使用*輸出參數*
（output parameter）來定義它，如下例所示：

```

CREATE FUNCTION add_em (IN x int, IN y int, OUT sum int)
AS 'SELECT x + y'
LANGUAGE SQL;

SELECT add_em(3,7);
 add_em
--------
     10
(1 row)
```

這與[36.5.2 節](xfunc-sql.md#XFUNC-SQL-BASE-FUNCTIONS)中所示的
`add_em` 版本，本質上並沒有什麼不同。輸出
參數真正的價值，在於它們提供了一種方便的方式，
可以定義傳回多個欄位的函式。舉例來說，

```

CREATE FUNCTION sum_n_product (x int, y int, OUT sum int, OUT product int)
AS 'SELECT x + y, x * y'
LANGUAGE SQL;

 SELECT * FROM sum_n_product(11,42);
 sum | product
-----+---------
  53 |     462
(1 row)
```

這裡實際發生的事，是我們為此函式的結果建立了一個
匿名的複合型別。上述範例所得到的最終結果，
與以下方式相同：

```

CREATE TYPE sum_prod AS (sum int, product int);

CREATE FUNCTION sum_n_product (int, int) RETURNS sum_prod
AS 'SELECT $1 + $2, $1 * $2'
LANGUAGE SQL;
```

但不需要另外費心定義獨立的複合型別，
往往相當方便。請注意，附加在輸出參數上的名稱，
並不只是裝飾用途，而是決定了匿名
複合型別的欄位名稱。（若你省略輸出參數的名稱，
系統會自行選擇一個名稱。）

請注意，從 SQL 呼叫這類函式時，輸出參數
並不會包含在呼叫時的引數清單中。這是因為
PostgreSQL 在定義函式的呼叫簽章時，
只考慮輸入參數。這也表示
在諸如刪除函式等用途中參照該函式時，也只有輸入參數
是重要的。我們可以用以下任一種方式
刪除上述函式：

```

DROP FUNCTION sum_n_product (x int, y int, OUT sum int, OUT product int);
DROP FUNCTION sum_n_product (int, int);
```

參數可以被標記為 `IN`（預設值）、
`OUT`、`INOUT` 或 `VARIADIC`。
`INOUT`
參數同時做為輸入參數（呼叫引數清單的一部分）與輸出參數
（結果記錄型別的一部分）。
`VARIADIC` 參數屬於輸入參數，但會依下文所述
以特殊方式處理。

<a id="XFUNC-OUTPUT-PARAMETERS-PROC"></a>

### 36.5.5. 具有輸出參數的 SQL 程序 [#](#XFUNC-OUTPUT-PARAMETERS-PROC)

<a id="id-1.8.3.8.13.2"></a>

程序中也支援輸出參數，但其運作方式與函式
略有不同。在 `CALL` 指令中，
輸出參數必須包含在引數清單中。
舉例來說，先前的銀行帳戶扣款常式可以
寫成這樣：

```

CREATE PROCEDURE tp1 (accountno integer, debit numeric, OUT new_balance numeric) AS $$
    UPDATE bank
        SET balance = balance - debit
        WHERE accountno = tp1.accountno
    RETURNING balance;
$$ LANGUAGE SQL;
```

要呼叫此程序，必須包含一個與 `OUT`
參數相符的引數。習慣上會寫
`NULL`：

```

CALL tp1(17, 100.0, NULL);
```

若你寫的是其他內容，它必須是一個可以隱含地
強制轉型為該參數所宣告型別的運算式，就像輸入
參數一樣。不過請注意，這樣的運算式並不會被求值。

從 PL/pgSQL 呼叫程序時，
你必須寫一個用來接收此程序輸出的變數，而不是寫
`NULL`。詳情請參閱[41.6.3 節](../plpgsql/plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)。

<a id="XFUNC-SQL-VARIADIC-FUNCTIONS"></a>

### 36.5.6. 具有可變數量引數的 SQL 函式 [#](#XFUNC-SQL-VARIADIC-FUNCTIONS)

<a id="id-1.8.3.8.14.2"></a><a id="id-1.8.3.8.14.3"></a>

SQL 函式可以被宣告為接受
可變數量的引數，只要所有「選擇性」
的引數都屬於相同的資料型別即可。這些選擇性引數會以
陣列的形式傳遞給函式。宣告此函式的方式，
是將最後一個參數標記為 `VARIADIC`；這個參數
必須被宣告為陣列型別。舉例來說：

```

CREATE FUNCTION mleast(VARIADIC arr numeric[]) RETURNS numeric AS $$
    SELECT min($1[i]) FROM generate_subscripts($1, 1) g(i);
$$ LANGUAGE SQL;

SELECT mleast(10, -1, 5, 4.4);
 mleast
--------
     -1
(1 row)
```

實際上，所有位於 `VARIADIC` 位置或其後的實際
引數，都會被收集到一個一維
陣列中，效果如同你寫了

```

SELECT mleast(ARRAY[10, -1, 5, 4.4]);    -- doesn't work
```

不過，你實際上並不能這樣寫——或者至少，這樣寫並
不會與此函式定義相符。標記為
`VARIADIC` 的參數，比對的是一個或多個其元素
型別的出現，而不是其本身型別的出現。

有時候能夠將一個已經建構好的陣列傳遞給可變參數
函式相當有用；這在某個可變參數
函式想要將其陣列參數傳遞給另一個可變參數函式時特別方便。此外，
這也是呼叫某個允許不受信任使用者建立物件之綱要中
可變參數函式的唯一安全方式；請參閱
[10.3 節](../../the-sql-language/typeconv/typeconv-func.md)。你可以在呼叫中
指定 `VARIADIC` 來做到這一點：

```

SELECT mleast(VARIADIC ARRAY[10, -1, 5, 4.4]);
```

這樣可以避免此函式的可變參數被展開為其
元素型別，從而讓陣列引數值可以正常
比對。`VARIADIC` 只能附加在函式呼叫的
最後一個實際引數上。

在呼叫中指定 `VARIADIC`，也是將空陣列
傳遞給可變參數函式的唯一方式，舉例來說：

```

SELECT mleast(VARIADIC ARRAY[]::numeric[]);
```

單純寫 `SELECT mleast()` 是無法運作的，因為
可變參數必須至少比對一個實際引數。
（若你想允許這類呼叫，可以定義另一個同樣名為
`mleast`、但不帶任何參數的函式。）

從可變參數所產生的陣列元素參數，
會被視為沒有各自的名稱。這表示除非你指定
`VARIADIC`，否則無法使用具名引數
（[4.3 節](../../the-sql-language/sql-syntax/sql-syntax-calling-funcs.md)）來呼叫可變參數函式。舉例來說，以下這樣可以運作：

```

SELECT mleast(VARIADIC arr => ARRAY[10, -1, 5, 4.4]);
```

但以下這些則不行：

```

SELECT mleast(arr => 10);
SELECT mleast(arr => ARRAY[10, -1, 5, 4.4]);
```

<a id="XFUNC-SQL-PARAMETER-DEFAULTS"></a>

### 36.5.7. 具有引數預設值的 SQL 函式 [#](#XFUNC-SQL-PARAMETER-DEFAULTS)

<a id="id-1.8.3.8.15.2"></a>

函式可以被宣告為對部分或全部輸入
引數具有預設值。每當呼叫函式時所提供的實際
引數不足，就會插入這些預設值。由於
只能從實際引數清單的末端省略引數，因此位於某個
具有預設值之參數之後的所有參數，也都必須具有
預設值。（雖然使用具名引數表示法可以放寬這項
限制，但為了讓位置式引數表示法能夠正常運作，這項限制
仍然會被強制執行。）不論你是否使用這項功能，這項能力
都會讓在某些使用者不信任其他使用者的資料庫中呼叫函式時，
需要採取一些預防措施；請參閱
[10.3 節](../../the-sql-language/typeconv/typeconv-func.md)。

舉例來說：

```

CREATE FUNCTION foo(a int, b int DEFAULT 2, c int DEFAULT 3)
RETURNS int
LANGUAGE SQL
AS $$
    SELECT $1 + $2 + $3;
$$;

SELECT foo(10, 20, 30);
 foo
-----
  60
(1 row)

SELECT foo(10, 20);
 foo
-----
  33
(1 row)

SELECT foo(10);
 foo
-----
  15
(1 row)

SELECT foo();  -- fails since there is no default for the first argument
ERROR:  function foo() does not exist
```

`=` 符號也可以用來取代
關鍵字 `DEFAULT`。

<a id="XFUNC-SQL-TABLE-FUNCTIONS"></a>

### 36.5.8. 作為資料表來源的 SQL 函式 [#](#XFUNC-SQL-TABLE-FUNCTIONS)

所有的 SQL 函式都可以用在查詢的 `FROM` 子句中，
但對於傳回複合型別的函式而言，這特別有用。
若某函式被定義為傳回基礎型別，則此資料表函式
會產生一個單欄的資料表。若某函式被定義為傳回
複合型別，則此資料表函式會為複合型別的每個屬性
產生一個欄位。

以下是一個範例：

```

CREATE TABLE foo (fooid int, foosubid int, fooname text);
INSERT INTO foo VALUES (1, 1, 'Joe');
INSERT INTO foo VALUES (1, 2, 'Ed');
INSERT INTO foo VALUES (2, 1, 'Mary');

CREATE FUNCTION getfoo(int) RETURNS foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT *, upper(fooname) FROM getfoo(1) AS t1;

 fooid | foosubid | fooname | upper
-------+----------+---------+-------
     1 |        1 | Joe     | JOE
(1 row)
```

如這個範例所示，我們可以像處理一般資料表的欄位一樣，
處理此函式結果的欄位。

請注意，我們只從此函式中得到一筆資料列。這是因為
我們沒有使用 `SETOF`。這會在下一節中
說明。

<a id="XFUNC-SQL-FUNCTIONS-RETURNING-SET"></a>

### 36.5.9. 傳回集合的 SQL 函式 [#](#XFUNC-SQL-FUNCTIONS-RETURNING-SET)

<a id="id-1.8.3.8.17.2"></a>

當某個 SQL 函式被宣告為傳回 `SETOF
sometype` 時，該函式的最後一則
查詢會被完整執行，且其輸出的每一列
都會被當作結果集合中的一個元素傳回。

此功能通常用於在 `FROM` 子句中呼叫函式時。
在這種情況下，函式所傳回的每一列，都會成為
查詢所看到的資料表中的一列。舉例來說，假設
資料表 `foo` 的內容與前述相同，且我們寫：

```

CREATE FUNCTION getfoo(int) RETURNS SETOF foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT * FROM getfoo(1) AS t1;
```

那麼我們會得到：

```

 fooid | foosubid | fooname
-------+----------+---------
     1 |        1 | Joe
     1 |        2 | Ed
(2 rows)
```

也可以傳回多筆資料列，其欄位由輸出參數
定義，像這樣：

```

CREATE TABLE tab (y int, z int);
INSERT INTO tab VALUES (1, 2), (3, 4), (5, 6), (7, 8);

CREATE FUNCTION sum_n_product_with_tab (x int, OUT sum int, OUT product int)
RETURNS SETOF record
AS $$
    SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;

SELECT * FROM sum_n_product_with_tab(10);
 sum | product
-----+---------
  11 |      10
  13 |      30
  15 |      50
  17 |      70
(4 rows)
```

這裡的重點是，你必須寫 `RETURNS SETOF record`
來表示此函式傳回多筆資料列，而不是只有一筆。
若只有一個輸出參數，則寫該參數的型別
即可，不需要寫 `record`。

在建構查詢結果時，透過多次呼叫一個傳回集合的
函式、且每次呼叫的參數都來自資料表或子查詢中
接連的資料列，往往相當有用。要達成這個目的，
建議的做法是使用 `LATERAL` 關鍵字，
其說明見於[7.2.1.5 節](../../the-sql-language/queries/queries-table-expressions.md#QUERIES-LATERAL)。
以下是一個使用傳回集合的函式，來列舉樹狀結構
元素的範例：

```

SELECT * FROM nodes;
   name    | parent
-----------+--------
 Top       |
 Child1    | Top
 Child2    | Top
 Child3    | Top
 SubChild1 | Child1
 SubChild2 | Child1
(6 rows)

CREATE FUNCTION listchildren(text) RETURNS SETOF text AS $$
    SELECT name FROM nodes WHERE parent = $1
$$ LANGUAGE SQL STABLE;

SELECT * FROM listchildren('Top');
 listchildren
--------------
 Child1
 Child2
 Child3
(3 rows)

SELECT name, child FROM nodes, LATERAL listchildren(name) AS child;
  name  |   child
--------+-----------
 Top    | Child1
 Top    | Child2
 Top    | Child3
 Child1 | SubChild1
 Child1 | SubChild2
(5 rows)
```

這個範例並沒有做任何用簡單的
連接（join）做不到的事，但在更複雜的計算中，可以把
部分工作放進函式中處理，這個選項會相當方便。

傳回集合的函式，也可以在查詢的選取清單中
呼叫。對於查詢本身所產生的每一列，
都會呼叫此傳回集合的函式，並為函式結果集合中的每個元素
產生一列輸出。
前一個範例也可以用類似這樣的
查詢來完成：

```

SELECT listchildren('Top');
 listchildren
--------------
 Child1
 Child2
 Child3
(3 rows)

SELECT name, listchildren(name) FROM nodes;
  name  | listchildren
--------+--------------
 Top    | Child1
 Top    | Child2
 Top    | Child3
 Child1 | SubChild1
 Child1 | SubChild2
(5 rows)
```

在最後一個 `SELECT` 中，
請注意 `Child2`、`Child3` 等並沒有出現任何輸出列。
這是因為對於這些引數，`listchildren` 傳回的是空集合，
因此沒有產生任何結果列。這與我們在使用
`LATERAL` 語法時，對函式結果做內連接（inner join）所得到的行為相同。

PostgreSQL 對於查詢選取清單中傳回集合函式
的行為，幾乎與該傳回集合函式改寫在
`LATERAL FROM` 子句項目中的行為完全相同。舉例來說，

```

SELECT x, generate_series(1,5) AS g FROM tab;
```

幾乎等同於

```

SELECT x, g FROM tab, LATERAL generate_series(1,5) AS g;
```

之所以說「幾乎」而不是「完全」相同，是因為在這個特定範例中，
規劃器可以選擇將 `g` 放在巢狀迴圈連接的外側，
因為 `g` 實際上並不具有對
`tab` 的橫向（lateral）相依性。這會導致不同的輸出資料列
順序。選取清單中傳回集合的函式，其求值方式
永遠如同它們位於巢狀迴圈連接中 `FROM` 子句其餘部分
的內側一樣，因此在考慮
`FROM` 子句的下一列之前，該函式（或函式們）
會先執行到完成。

若查詢的選取清單中有一個以上傳回集合的
函式，其行為類似於將這些函式放入單一
`LATERAL ROWS FROM( ... )` `FROM` 子句
項目中所得到的結果。對於底層查詢的每一列，
都會產生一列使用各函式第一個結果的輸出列，
接著再產生一列使用各函式第二個結果的輸出列，依此類推。若某些
傳回集合的函式產生的輸出比其他函式少，
則會以 null 值補足缺少的資料，讓對於某一底層
資料列所產生的資料列總數，與產生最多輸出的
傳回集合函式相同。因此，這些傳回集合的函式
會「同步」（in lockstep）執行，直到全部耗盡為止，然後
再繼續處理下一個底層資料列。

傳回集合的函式可以在選取清單中巢狀使用，
不過在 `FROM` 子句項目中並不允許這樣做。在這種情況下，
每一層巢狀都會被個別處理，如同它是一個
獨立的 `LATERAL ROWS FROM( ... )` 項目。舉例來說，在

```

SELECT srf1(srf2(x), srf3(y)), srf4(srf5(z)) FROM tab;
```

中，傳回集合的函式 `srf2`、`srf3`
與 `srf5` 會針對 `tab` 的每一列
同步執行，然後 `srf1` 與 `srf4`
會針對較內層函式所產生的每一列結果，
同步套用。

傳回集合的函式不能在條件求值
結構中使用，例如 `CASE` 或 `COALESCE`。舉例來說，
考慮：

```

SELECT x, CASE WHEN x > 0 THEN generate_series(1, 5) ELSE 0 END FROM tab;
```

看起來這似乎應該對 `x > 0` 的輸入列
重複產生五次，而對不符合此條件的輸入列則只重複一次；
但實際上，由於 `generate_series(1, 5)` 會在
`CASE` 運算式被求值之前，先在一個隱含的
`LATERAL FROM` 項目中執行，因此它會對每一列輸入
都重複產生五次。為了減少混淆，這類情況
會在剖析階段就產生錯誤，而不是這樣執行。

### 注意

若某函式的最後一個指令是帶有 `RETURNING`
的 `INSERT`、
`UPDATE`、`DELETE` 或
`MERGE`，則該指令
永遠會被完整執行，即使此函式並未宣告為
`SETOF`，或呼叫的查詢並未取用所有
結果列也一樣。由 `RETURNING`
子句所產生的任何額外資料列，都會被悄悄捨棄，但
指令所要求的資料表修改仍然會發生（並且會在函式
傳回之前全部完成）。

### 注意

在 PostgreSQL 10 之前，在同一個選取清單中
放入超過一個傳回集合的函式，除非它們一律
產生相同數量的資料列，否則行為並不太合理。否則，
你所得到的輸出列數量，會等於這些傳回集合
函式所產生資料列數量的最小公倍數。此外，
巢狀的傳回集合函式，並不會像上文所描述的那樣運作；
相反地，一個傳回集合的函式最多只能有
一個傳回集合的引數，且每一層巢狀的傳回集合函式
都是獨立執行的。此外，先前也曾允許條件式執行
（`CASE` 等結構內的傳回集合函式），
這讓情況變得更加複雜。
在撰寫需要相容於較舊 PostgreSQL 版本
的查詢時，建議使用 `LATERAL` 語法，
因為這樣可以在不同版本之間得到一致的結果。
若你有一個依賴傳回集合函式條件式執行的查詢，
你或許可以透過將條件測試移到一個自訂的
傳回集合函式中來修正它。舉例來說，

```

SELECT x, CASE WHEN y > 0 THEN generate_series(1, z) ELSE 5 END FROM tab;
```

可以改寫為

```

CREATE FUNCTION case_generate_series(cond bool, start int, fin int, els int)
  RETURNS SETOF int AS $$
BEGIN
  IF cond THEN
    RETURN QUERY SELECT generate_series(start, fin);
  ELSE
    RETURN QUERY SELECT els;
  END IF;
END$$ LANGUAGE plpgsql;

SELECT x, case_generate_series(y > 0, 1, z, 5) FROM tab;
```

這樣的寫法，在所有版本的
PostgreSQL 中，行為都會相同。

<a id="XFUNC-SQL-FUNCTIONS-RETURNING-TABLE"></a>

### 36.5.10. 傳回 `TABLE` 的 SQL 函式 [#](#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE)

<a id="id-1.8.3.8.18.2"></a>

還有另一種方式可以將函式宣告為傳回集合，
那就是使用
`RETURNS TABLE(columns)` 語法。
這等同於使用一個或多個 `OUT` 參數，並且
將函式標記為傳回 `SETOF record`（或視情況
傳回單一輸出參數型別的 `SETOF`）。
此表示法是近期版本 SQL 標準中所規定的，因此
可能比使用 `SETOF` 更具可移植性。

舉例來說，前面的加總與乘積範例，也可以用這種方式
完成：

```

CREATE FUNCTION sum_n_product_with_tab (x int)
RETURNS TABLE(sum int, product int) AS $$
    SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;
```

使用 `RETURNS TABLE` 表示法時，不允許
使用明確的 `OUT` 或 `INOUT`
參數——你必須把所有輸出欄位都放在
`TABLE` 清單中。

<a id="XFUNC-SQL-POLYMORPHIC-FUNCTIONS"></a>

### 36.5.11. 多型 SQL 函式 [#](#XFUNC-SQL-POLYMORPHIC-FUNCTIONS)

SQL 函式可以被宣告為接受並
傳回[36.2.5 節](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)中所述的多型（polymorphic）型別。以下是一個
名為 `make_array` 的多型函式，它會從
兩個任意資料型別的元素建構出一個陣列：

```

CREATE FUNCTION make_array(anyelement, anyelement) RETURNS anyarray AS $$
    SELECT ARRAY[$1, $2];
$$ LANGUAGE SQL;

SELECT make_array(1, 2) AS intarray, make_array('a'::text, 'b') AS textarray;
 intarray | textarray
----------+-----------
 {1,2}    | {a,b}
(1 row)
```

請注意這裡使用了型別轉換 `'a'::text`
來指定此引數的型別為 `text`。若引數只是
字串常值，就需要這麼做，因為否則
它會被視為 `unknown` 型別，而 `unknown`
的陣列並不是有效的型別。
若不加上型別轉換，你會得到類似這樣的錯誤：

```

ERROR:  could not determine polymorphic type because input has type unknown
```

如上所宣告的 `make_array`，你必須
提供兩個完全相同資料型別的引數；
系統不會嘗試解決任何型別上的差異。因此，
舉例來說，以下這樣是行不通的：

```

SELECT make_array(1, 2.5) AS numericarray;
ERROR:  function make_array(integer, numeric) does not exist
```

另一種做法是使用「common」這一系列的
多型型別，讓系統嘗試找出
一個合適的共通型別：

```

CREATE FUNCTION make_array2(anycompatible, anycompatible)
RETURNS anycompatiblearray AS $$
    SELECT ARRAY[$1, $2];
$$ LANGUAGE SQL;

SELECT make_array2(1, 2.5) AS numericarray;
 numericarray
--------------
 {1,2.5}
(1 row)
```

由於共通型別解析的規則，在所有輸入都是
未知型別時，預設會選擇 `text` 型別，因此
以下這樣也可以運作：

```

SELECT make_array2('a', 'b') AS textarray;
 textarray
-----------
 {a,b}
(1 row)
```

允許引數是多型的、但傳回型別固定，
反過來則不允許。舉例來說：

```

CREATE FUNCTION is_greater(anyelement, anyelement) RETURNS boolean AS $$
    SELECT $1 > $2;
$$ LANGUAGE SQL;

SELECT is_greater(1, 2);
 is_greater
------------
 f
(1 row)

CREATE FUNCTION invalid_func() RETURNS anyelement AS $$
    SELECT 1;
$$ LANGUAGE SQL;
ERROR:  cannot determine result data type
DETAIL:  A result of type anyelement requires at least one input of type anyelement, anyarray, anynonarray, anyenum, or anyrange.
```

多型也可以用於具有輸出引數的函式。
舉例來說：

```

CREATE FUNCTION dup (f1 anyelement, OUT f2 anyelement, OUT f3 anyarray)
AS 'select $1, array[$1,$1]' LANGUAGE SQL;

SELECT * FROM dup(22);
 f2 |   f3
----+---------
 22 | {22,22}
(1 row)
```

多型也可以與可變參數函式一起使用。
舉例來說：

```

CREATE FUNCTION anyleast (VARIADIC anyarray) RETURNS anyelement AS $$
    SELECT min($1[i]) FROM generate_subscripts($1, 1) g(i);
$$ LANGUAGE SQL;

SELECT anyleast(10, -1, 5, 4);
 anyleast
----------
       -1
(1 row)

SELECT anyleast('abc'::text, 'def');
 anyleast
----------
 abc
(1 row)

CREATE FUNCTION concat_values(text, VARIADIC anyarray) RETURNS text AS $$
    SELECT array_to_string($2, $1);
$$ LANGUAGE SQL;

SELECT concat_values('|', 1, 4, 2);
 concat_values
---------------
 1|4|2
(1 row)
```

<a id="XFUNC-SQL-COLLATIONS"></a>

### 36.5.12. 具有定序的 SQL 函式 [#](#XFUNC-SQL-COLLATIONS)

<a id="id-1.8.3.8.20.2"></a>

當某個 SQL 函式具有一個或多個可定序資料型別的參數時，
會依照實際引數所指定的定序，為每次函式呼叫識別出
一種定序，詳情見於[23.2 節](../../server-administration/charset/collation.md)。若成功識別出
某種定序（也就是說，各引數的隱含定序之間沒有
衝突），則所有可定序的參數都會被視為
隱含具有該定序。這會影響函式內
定序敏感操作的行為。舉例來說，使用
前面所述的 `anyleast` 函式，

```

SELECT anyleast('abc'::text, 'ABC');
```

的結果，會取決於資料庫的預設定序。在 `C` 語系下，
結果會是 `ABC`，但在許多其他語系下，
會是 `abc`。可以透過在任一引數中加入
`COLLATE` 子句，來強制指定要使用的定序，例如

```

SELECT anyleast('abc'::text, 'ABC' COLLATE "C");
```

另外，若你希望某個函式無論以何種方式呼叫，
都以特定定序運作，可以視需要在函式定義中
插入 `COLLATE` 子句。
以下這個版本的 `anyleast`，會永遠使用 `en_US`
語系來比較字串：

```

CREATE FUNCTION anyleast (VARIADIC anyarray) RETURNS anyelement AS $$
    SELECT min($1[i] COLLATE "en_US") FROM generate_subscripts($1, 1) g(i);
$$ LANGUAGE SQL;
```

但請注意，若將此函式套用於不可定序的
資料型別，會引發錯誤。

若在實際引數中無法識別出共通的定序，
則 SQL 函式會將其參數視為具有其資料型別的
預設定序（通常是資料庫的預設定序，
但對於網域型別的參數則可能不同）。

可定序參數的行為，可以視為一種
有限形式的多型，只適用於文字類型的資料型別。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xfunc-sql.html)（原文版本：18.6；核對日期：2026-09-24）
