<a id="ROWTYPES"></a>

## 8.16. 複合型別 [#](#ROWTYPES)

[8.16.1. 複合型別的宣告](rowtypes.md#ROWTYPES-DECLARING)

[8.16.2. 建構複合值](rowtypes.md#ROWTYPES-CONSTRUCTING)

[8.16.3. 存取複合型別](rowtypes.md#ROWTYPES-ACCESSING)

[8.16.4. 修改複合型別](rowtypes.md#ROWTYPES-MODIFYING)

[8.16.5. 在查詢中使用複合型別](rowtypes.md#ROWTYPES-USAGE)

[8.16.6. 複合型別的輸入與輸出語法](rowtypes.md#ROWTYPES-IO-SYNTAX)

<a id="id-1.5.7.24.2"></a><a id="id-1.5.7.24.3"></a>

*複合型別*代表一個資料列或記錄的結構；它本質上就只是一份欄位名稱及其資料型別的清單。PostgreSQL 允許以許多與簡單型別相同的方式來使用複合型別。例如，資料表的欄位可以宣告為複合型別。

<a id="ROWTYPES-DECLARING"></a>

### 8.16.1. 複合型別的宣告 [#](#ROWTYPES-DECLARING)

以下是兩個定義複合型別的簡單例子：

```

CREATE TYPE complex AS (
    r       double precision,
    i       double precision
);

CREATE TYPE inventory_item AS (
    name            text,
    supplier_id     integer,
    price           numeric
);
```

這個語法與 `CREATE TABLE` 相仿，差別在於只能指定欄位名稱與型別；目前還不能加入任何限制條件（例如 `NOT NULL`）。請注意 `AS` 關鍵字是必要的；少了它，系統會以為你指的是另一種 `CREATE TYPE` 指令，於是你會得到奇怪的語法錯誤。

定義好這些型別之後，我們就可以用它們來建立資料表：

```

CREATE TABLE on_hand (
    item      inventory_item,
    count     integer
);

INSERT INTO on_hand VALUES (ROW('fuzzy dice', 42, 1.99), 1000);
```

或建立函式：

```

CREATE FUNCTION price_extension(inventory_item, integer) RETURNS numeric
AS 'SELECT $1.price * $2' LANGUAGE SQL;

SELECT price_extension(item, 10) FROM on_hand;
```

每當你建立一個資料表時，系統也會自動建立一個與該資料表同名的複合型別，用來代表該資料表的資料列型別。例如，假設我們寫了：

```

CREATE TABLE inventory_item (
    name            text,
    supplier_id     integer REFERENCES suppliers,
    price           numeric CHECK (price > 0)
);
```

那麼上面所示的同一個 `inventory_item` 複合型別就會被附帶建立出來，而且可以像上面那樣使用。不過請注意目前實作上的一項重要限制：由於複合型別並不會關聯任何限制條件，資料表定義中所顯示的那些限制條件*並不會套用*到資料表之外的複合型別值。（要解決這個問題，可以在該複合型別之上建立一個 [*[網域](../../appendixes/glossary/README.md#GLOSSARY-DOMAIN)*](../../appendixes/glossary/README.md#GLOSSARY-DOMAIN)，並把想要的限制條件寫成該網域的 `CHECK` 限制條件。）

<a id="ROWTYPES-CONSTRUCTING"></a>

### 8.16.2. 建構複合值 [#](#ROWTYPES-CONSTRUCTING)

<a id="id-1.5.7.24.6.2"></a>

若要將複合值寫成字面常數，請將各欄位的值用小括號括起來，並以逗號分隔。你可以在任何欄位值前後加上雙引號，而且如果該值含有逗號或小括號，就必須這麼做。（更多細節請見[下文](rowtypes.md#ROWTYPES-IO-SYNTAX)。）因此，複合常數的一般格式如下：

```

'( val1 , val2 , ... )'
```

以下是一個例子：

```

'("fuzzy dice",42,1.99)'
```

這會是上面所定義之 `inventory_item` 型別的一個有效值。若要讓某個欄位為 NULL，請在它於清單中的位置完全不寫任何字元。例如，這個常數就指定了第三個欄位為 NULL：

```

'("fuzzy dice",42,)'
```

如果你要的是空字串而不是 NULL，請寫上雙引號：

```

'("",42,)'
```

這裡第一個欄位是一個非 NULL 的空字串，第三個欄位則是 NULL。

（這些常數其實只是[第 4.1.2.7 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC)所討論之通用型別常數的一個特例。這種常數一開始會被當成字串處理，然後傳給複合型別的輸入轉換常式。有時可能需要明確指定型別，以告知要把該常數轉換成哪一種型別。）

也可以使用 `ROW` 運算式語法來建構複合值。在大多數情況下，這比字串字面值語法好用得多，因為你不必去煩惱多層引號的問題。我們在前面已經用過這個方法：

```

ROW('fuzzy dice', 42, 1.99)
ROW('', 42, NULL)
```

只要運算式中有一個以上的欄位，ROW 關鍵字其實就是選用的，所以這些可以簡化成：

```

('fuzzy dice', 42, 1.99)
('', 42, NULL)
```

`ROW` 運算式語法在[第 4.2.13 節](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)中有更詳細的討論。

<a id="ROWTYPES-ACCESSING"></a>

### 8.16.3. 存取複合型別 [#](#ROWTYPES-ACCESSING)

若要存取複合欄位中的某個欄位，就寫上一個點再加上欄位名稱，很像是從資料表名稱中選取欄位。事實上，它實在太像從資料表名稱選取欄位了，以致於你常常必須使用小括號以免讓剖析器混淆。例如，你可能會像這樣試著從我們的 `on_hand` 範例資料表中選取一些子欄位：

```

SELECT item.name FROM on_hand WHERE item.price > 9.99;
```

這樣行不通，因為依照 SQL 的語法規則，`item` 這個名稱會被當成資料表名稱，而不是 `on_hand` 的欄位名稱。你必須寫成這樣：

```

SELECT (item).name FROM on_hand WHERE (item).price > 9.99;
```

或者，如果你同時也需要用到資料表名稱（例如在多資料表查詢中），就寫成這樣：

```

SELECT (on_hand.item).name FROM on_hand WHERE (on_hand.item).price > 9.99;
```

現在括號內的物件才會被正確地解讀為對 `item` 欄位的參照，接著就可以從中選取子欄位。

每當你要從複合值中選取欄位時，都會遇到類似的語法問題。例如，若只要從一個回傳複合值的函式結果中選取一個欄位，你必須寫成像這樣：

```

SELECT (my_func(...)).field FROM ...
```

少了額外的小括號，這會產生語法錯誤。

特殊的欄位名稱 `*` 代表「所有欄位」，[第 8.16.5 節](rowtypes.md#ROWTYPES-USAGE)有進一步的說明。

<a id="ROWTYPES-MODIFYING"></a>

### 8.16.4. 修改複合型別 [#](#ROWTYPES-MODIFYING)

以下是一些新增與更新複合欄位之正確語法的例子。首先是新增或更新整個欄位：

```

INSERT INTO mytab (complex_col) VALUES((1.1,2.2));

UPDATE mytab SET complex_col = ROW(1.1,2.2) WHERE ...;
```

第一個例子省略了 `ROW`，第二個則用了它；兩種寫法我們都可以採用。

我們可以更新複合欄位中的某個個別子欄位：

```

UPDATE mytab SET complex_col.r = (complex_col).r + 1 WHERE ...;
```

請注意，這裡我們不需要（實際上也不能）在緊接於 `SET` 之後的欄位名稱前後加上小括號，但在等號右邊的運算式中參照同一個欄位時，就需要小括號。

我們也可以把子欄位指定為 `INSERT` 的目標：

```

INSERT INTO mytab (complex_col.r, complex_col.i) VALUES(1.1, 2.2);
```

如果我們沒有為該欄位的所有子欄位都提供值，其餘的子欄位就會被填入 NULL 值。

<a id="ROWTYPES-USAGE"></a>

### 8.16.5. 在查詢中使用複合型別 [#](#ROWTYPES-USAGE)

在查詢中使用複合型別時，有各種特殊的語法規則與行為。這些規則提供了好用的捷徑，但如果你不了解背後的邏輯，可能會覺得困惑。

在 PostgreSQL 中，查詢裡對資料表名稱（或別名）的參照，實際上就是對該資料表目前這筆資料列之複合值的參照。例如，如果我們有一個如[前面](rowtypes.md#ROWTYPES-DECLARING)所示的 `inventory_item` 資料表，我們可以寫成：

```

SELECT c FROM inventory_item c;
```

這個查詢會產生單一個複合值欄位，所以我們可能會得到像這樣的輸出：

```

           c
------------------------
 ("fuzzy dice",42,1.99)
(1 row)
```

不過請注意，簡單名稱會先與欄位名稱比對，之後才與資料表名稱比對，所以這個例子之所以行得通，只是因為查詢所用的資料表中沒有名為 `c` 的欄位。

一般的限定欄位名稱語法 *`table_name`*`.`*`column_name`* 可以理解為對該資料表目前這筆資料列的複合值套用[欄位選取](../sql-syntax/sql-expressions.md#FIELD-SELECTION)。（基於效率的考量，實際上並不是這樣實作的。）

當我們寫下

```

SELECT c.* FROM inventory_item c;
```

那麼依照 SQL 標準，我們應該會得到展開成個別欄位的資料表內容：

```

    name    | supplier_id | price
------------+-------------+-------
 fuzzy dice |          42 |  1.99
(1 row)
```

就好像查詢是寫成

```

SELECT c.name, c.supplier_id, c.price FROM inventory_item c;
```

PostgreSQL 會把這種展開行為套用到任何複合值運算式上，不過如同[前面](rowtypes.md#ROWTYPES-ACCESSING)所示，只要 `.*` 所套用的對象不是單純的資料表名稱，你就必須在該值前後加上小括號。例如，如果 `myfunc()` 是一個回傳複合型別、且該型別有 `a`、`b` 與 `c` 三個欄位的函式，那麼這兩個查詢會有相同的結果：

```

SELECT (myfunc(x)).* FROM some_table;
SELECT (myfunc(x)).a, (myfunc(x)).b, (myfunc(x)).c FROM some_table;
```

### 提示

PostgreSQL 處理欄位展開的方式，實際上是把第一種形式轉換成第二種。所以在這個例子中，不論用哪一種語法，`myfunc()` 每筆資料列都會被呼叫三次。如果它是一個成本昂貴的函式，你可能會希望避免這種情況，而這可以透過像這樣的查詢來做到：

```

SELECT m.* FROM some_table, LATERAL myfunc(x) AS m;
```

把函式放進 `LATERAL` 的 `FROM` 項目中，可以避免它在每筆資料列被呼叫超過一次。`m.*` 仍然會被展開成 `m.a, m.b, m.c`，但現在這些變數只是對該 `FROM` 項目輸出的參照而已。（這裡的 `LATERAL` 關鍵字是選用的，但我們把它寫出來，以釐清該函式是從 `some_table` 取得 `x` 的。）

當 *`composite_value`*`.*` 語法出現在 [`SELECT` 輸出清單](../queries/queries-select-lists.md)、`INSERT`／`UPDATE`／`DELETE`／`MERGE` 的 [`RETURNING` 清單](../dml/dml-returning.md)、[`VALUES` 子句](../queries/queries-values.md)或[資料列建構子](../sql-syntax/sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)的最上層時，就會造成這種欄位展開。在其他所有情境中（包括巢狀出現在上述結構之內時），在複合值後面加上 `.*` 並不會改變該值，因為它的意思是「所有欄位」，因此產生出來的還是同一個複合值。例如，如果 `somefunc()` 接受一個複合值引數，下列這些查詢是相同的：

```

SELECT somefunc(c.*) FROM inventory_item c;
SELECT somefunc(c) FROM inventory_item c;
```

在這兩種情況中，`inventory_item` 目前的資料列都會以單一個複合值引數的形式傳給該函式。即使 `.*` 在這種情況下不起任何作用，使用它仍然是良好的風格，因為這樣能清楚表明這裡要的是一個複合值。特別是，剖析器會認為 `c.*` 中的 `c` 指的是資料表名稱或別名，而不是欄位名稱，因此不會有語意不明確的問題；反之，若沒有 `.*`，就不清楚 `c` 指的是資料表名稱還是欄位名稱，而且事實上，如果有一個名為 `c` 的欄位，系統會優先採用欄位名稱的解讀方式。

另一個說明這些概念的例子是，下列這些查詢全都代表同一件事：

```

SELECT * FROM inventory_item c ORDER BY c;
SELECT * FROM inventory_item c ORDER BY c.*;
SELECT * FROM inventory_item c ORDER BY ROW(c.*);
```

所有這些 `ORDER BY` 子句指定的都是資料列的複合值，因此會依照[第 9.25.6 節](../functions/functions-comparisons.md#COMPOSITE-TYPE-COMPARISON)所述的規則來排序資料列。不過，如果 `inventory_item` 含有一個名為 `c` 的欄位，第一種情況就會與其他幾種不同，因為它會變成只依該欄位排序。就前面所列出的欄位名稱而言，下列這些查詢也與上面那些等價：

```

SELECT * FROM inventory_item c ORDER BY ROW(c.name, c.supplier_id, c.price);
SELECT * FROM inventory_item c ORDER BY (c.name, c.supplier_id, c.price);
```

（最後一種情況使用的是省略了 `ROW` 關鍵字的資料列建構子。）

與複合值有關的另一種特殊語法行為是，我們可以使用*函式記法*來取出複合值中的某個欄位。簡單的解釋方式是，`field(table)` 與 `table.field` 這兩種記法是可以互換的。例如，這些查詢是等價的：

```

SELECT c.name FROM inventory_item c WHERE c.price > 1000;
SELECT name(c) FROM inventory_item c WHERE price(c) > 1000;
```

此外，如果我們有一個接受單一複合型別引數的函式，我們用哪一種記法來呼叫它都可以。下列這些查詢全都是等價的：

```

SELECT somefunc(c) FROM inventory_item c;
SELECT somefunc(c.*) FROM inventory_item c;
SELECT c.somefunc FROM inventory_item c;
```

函式記法與欄位記法之間的這種等價性，使得我們可以利用複合型別上的函式來實作「計算欄位」。
<a id="id-1.5.7.24.9.10.2"></a>
<a id="id-1.5.7.24.9.10.3"></a>
使用上面最後那個查詢的應用程式，並不需要直接知道 `somefunc` 其實不是該資料表真正的欄位。

### 提示

由於有這種行為，把一個接受單一複合型別引數的函式，命名成與該複合型別任一欄位相同的名稱，是不明智的做法。如果發生語意不明確的情況，使用欄位名稱語法時會選擇欄位名稱的解讀方式，而使用函式呼叫語法時則會選擇該函式。不過，PostgreSQL 11 之前的版本一律會選擇欄位名稱的解讀方式，除非呼叫的語法要求它必須是函式呼叫。在較舊的版本中，要強制採用函式解讀方式的方法之一，是為函式名稱加上綱要限定，也就是寫成 `schema.func(compositevalue)`。

<a id="ROWTYPES-IO-SYNTAX"></a>

### 8.16.6. 複合型別的輸入與輸出語法 [#](#ROWTYPES-IO-SYNTAX)

複合值的外部文字表示法，是由一些項目所組成，這些項目會依照各個欄位型別的 I/O 轉換規則來解讀，再加上用來標示複合結構的修飾符號。這些修飾符號包括圍繞在整個值前後的小括號（`(` 與 `)`），以及相鄰項目之間的逗號（`,`）。小括號之外的空白字元會被忽略，但小括號之內的空白字元會被視為欄位值的一部分，而且依照該欄位資料型別的輸入轉換規則，它可能有意義也可能沒有意義。例如在：

```

'(  42)'
```

之中，如果欄位型別是 integer，空白字元就會被忽略，但如果是 text 就不會。

如同先前所示，在寫出複合值時，你可以在任何個別的欄位值前後加上雙引號。如果欄位值不加引號會讓複合值的剖析器混淆，你就*必須*這麼做。特別是，含有小括號、逗號、雙引號或反斜線的欄位，都必須以雙引號標示。若要在加了引號的複合欄位值中放入雙引號或反斜線，請在它前面加上一個反斜線。（此外，加了雙引號的欄位值中若出現一對連續的雙引號，會被視為代表一個雙引號字元，這類似於 SQL 字串常數中單引號的規則。）或者，你也可以不使用引號，改用反斜線跳脫來保護所有原本會被當成複合語法的資料字元。

完全空白的欄位值（逗號或小括號之間完全沒有任何字元）代表 NULL。若要寫出一個是空字串而不是 NULL 的值，請寫成 `""`。

如果欄位值是空字串，或含有小括號、逗號、雙引號、反斜線或空白字元，複合型別的輸出常式就會在該欄位值前後加上雙引號。（對空白字元這麼做並非必要，但有助於閱讀。）欄位值中所內嵌的雙引號與反斜線會被寫成兩個。

### 注意

請記得，你在 SQL 指令中所寫的內容會先被解讀成字串常數，然後才被解讀成複合值。這會讓你需要的反斜線數量加倍（假設使用的是跳脫字串語法）。例如，若要在複合值中插入一個含有雙引號與反斜線的 `text` 欄位，你必須寫成：

```

INSERT ... VALUES ('("\"\\")');
```

字串常數的處理程式會移除一層反斜線，因此傳到複合值剖析器的內容看起來會是 `("\"\\")`。接著，餵給 `text` 資料型別輸入常式的字串就變成 `"\`。（如果我們處理的資料型別其輸入常式也對反斜線做特殊處理，例如 `bytea`，那麼我們在指令中可能需要多達八個反斜線，才能讓一個反斜線進到儲存的複合欄位中。）使用錢字號引號標示（請參閱[第 4.1.2.4 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)）可以避免必須把反斜線寫成兩倍。

### 提示

在 SQL 指令中寫出複合值時，`ROW` 建構子語法通常比複合字面值語法更容易使用。在 `ROW` 中，個別欄位值的寫法就跟它們不是複合值成員時的寫法完全相同。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rowtypes.html)（原文版本：18.6；核對日期：2026-09-13）
