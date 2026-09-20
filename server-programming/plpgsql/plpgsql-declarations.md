<a id="PLPGSQL-DECLARATIONS"></a>

## 41.3. 宣告 [#](#PLPGSQL-DECLARATIONS)

[41.3.1. 宣告函式參數](plpgsql-declarations.md#PLPGSQL-DECLARATION-PARAMETERS)

[41.3.2. `ALIAS`](plpgsql-declarations.md#PLPGSQL-DECLARATION-ALIAS)

[41.3.3. 複製型別](plpgsql-declarations.md#PLPGSQL-DECLARATION-TYPE)

[41.3.4. 資料列型別](plpgsql-declarations.md#PLPGSQL-DECLARATION-ROWTYPES)

[41.3.5. record 型別](plpgsql-declarations.md#PLPGSQL-DECLARATION-RECORDS)

[41.3.6. PL/pgSQL 變數的定序](plpgsql-declarations.md#PLPGSQL-DECLARATION-COLLATION)

在區塊中使用的所有變數，都必須在該區塊的宣告區段中宣告。（唯一的例外是：走訪一段整數值範圍的 `FOR` 迴圈，其迴圈變數會自動被宣告為整數變數；同樣地，走訪某個游標結果的 `FOR` 迴圈，其迴圈變數也會自動被宣告為 record（記錄）變數。）

PL/pgSQL 變數可以是任何 SQL 資料型別，例如 `integer`、`varchar` 與 `char`。

以下是一些變數宣告的範例：

```

user_id integer;
quantity numeric(5);
url varchar;
myrow tablename%ROWTYPE;
myfield tablename.columnname%TYPE;
arow RECORD;
```

變數宣告的一般語法為：

```

name [ CONSTANT ] type [ COLLATE collation_name ] [ NOT NULL ] [ { DEFAULT | := | = } expression ];
```

`DEFAULT` 子句若有給定，會指定進入該區塊時要指派給變數的初始值。若未給定 `DEFAULT` 子句，變數就會被初始化為 SQL 空值（null）。`CONSTANT` 選項可防止變數在初始化之後被指派新值，使其值在整個區塊期間維持不變。`COLLATE` 選項可指定該變數要使用的定序（請參閱[第 41.3.6 節](plpgsql-declarations.md#PLPGSQL-DECLARATION-COLLATION)）。若指定了 `NOT NULL`，則指派空值時會產生執行期錯誤。所有宣告為 `NOT NULL` 的變數，都必須指定一個非空值的預設值。等號（`=`）可以用來取代符合 PL/SQL 規範的 `:=`。

變數的預設值會在每次進入該區塊時重新求值並指派給變數（而不是每次函式呼叫只做一次）。因此舉例來說，把 `now()` 指派給型別為 `timestamp` 的變數，會使該變數取得目前這次函式呼叫的時間，而不是函式被預先編譯時的時間。

範例：

```

quantity integer DEFAULT 32;
url varchar := 'http://mysite.com';
transaction_time CONSTANT timestamp with time zone := now();
```

變數一經宣告，其值就可以用於同一區塊中後續的初始化運算式，例如：

```

DECLARE
  x integer := 1;
  y integer := x + 1;
```

<a id="PLPGSQL-DECLARATION-PARAMETERS"></a>

### 41.3.1. 宣告函式參數 [#](#PLPGSQL-DECLARATION-PARAMETERS)

傳遞給函式的參數是以 `$1`、`$2` 等識別符號來命名的。你也可以選擇為 `$n` 這類參數名稱宣告別名，以提高可讀性。之後不論是別名或是數字識別符號，都可以用來指涉該參數值。

建立別名有兩種方式。建議的方式是在 `CREATE FUNCTION` 指令中為參數命名，例如：

```

CREATE FUNCTION sales_tax(subtotal real) RETURNS real AS $$
BEGIN
    RETURN subtotal * 0.06;
END;
$$ LANGUAGE plpgsql;
```

另一種方式是使用下列宣告語法明確地宣告別名

```

name ALIAS FOR $n;
```

同樣的例子以這種風格撰寫會像這樣：

```

CREATE FUNCTION sales_tax(real) RETURNS real AS $$
DECLARE
    subtotal ALIAS FOR $1;
BEGIN
    RETURN subtotal * 0.06;
END;
$$ LANGUAGE plpgsql;
```

<a id="PLPGSQL-DECLARATION-PARAMETERS-NOTE"></a>

### 注意

這兩個例子並非完全等價。在第一種情況中，`subtotal` 可以用 `sales_tax.subtotal` 來指涉，但在第二種情況中則不行。（如果我們為內層區塊加上標籤，`subtotal` 就可以改用該標籤來限定。）

再看一些例子：

```

CREATE FUNCTION instr(varchar, integer) RETURNS integer AS $$
DECLARE
    v_string ALIAS FOR $1;
    index ALIAS FOR $2;
BEGIN
    -- some computations using v_string and index here
END;
$$ LANGUAGE plpgsql;


CREATE FUNCTION concat_selected_fields(in_t sometablename) RETURNS text AS $$
BEGIN
    RETURN in_t.f1 || in_t.f3 || in_t.f5 || in_t.f7;
END;
$$ LANGUAGE plpgsql;
```

當 PL/pgSQL 函式宣告了輸出參數時，這些輸出參數也會以和一般輸入參數完全相同的方式取得 `$n` 名稱以及可選的別名。輸出參數實際上就是一個一開始為 NULL 的變數，應該在函式執行過程中被指派值。該參數的最終值就是回傳的內容。舉例來說，前面的營業稅範例也可以這樣寫：

```

CREATE FUNCTION sales_tax(subtotal real, OUT tax real) AS $$
BEGIN
    tax := subtotal * 0.06;
END;
$$ LANGUAGE plpgsql;
```

請注意我們省略了 `RETURNS real`——我們原本可以把它寫上，但那會是多餘的。

要呼叫具有 `OUT` 參數的函式時，請在函式呼叫中省略輸出參數：

```

SELECT sales_tax(100.00);
```

輸出參數在要回傳多個值時最為有用。一個很簡單的例子是：

```

CREATE FUNCTION sum_n_product(x int, y int, OUT sum int, OUT prod int) AS $$
BEGIN
    sum := x + y;
    prod := x * y;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM sum_n_product(2, 4);
 sum | prod
-----+------
   6 |    8
```

如[第 36.5.4 節](../extend/xfunc-sql.md#XFUNC-OUTPUT-PARAMETERS)所討論的，這實際上會為函式的結果建立一個匿名的 record 型別。若有給定 `RETURNS` 子句，它必須寫成 `RETURNS record`。

這對程序（procedure）也同樣適用，例如：

```

CREATE PROCEDURE sum_n_product(x int, y int, OUT sum int, OUT prod int) AS $$
BEGIN
    sum := x + y;
    prod := x * y;
END;
$$ LANGUAGE plpgsql;
```

呼叫程序時，所有的參數都必須指定。對於輸出參數，從單純的 SQL 呼叫該程序時可以指定 `NULL`：

```

CALL sum_n_product(2, 4, NULL, NULL);
 sum | prod
-----+------
   6 |    8
```

不過，當你從 PL/pgSQL 呼叫程序時，對於任何輸出參數都應該改寫上一個變數；該變數將會接收呼叫的結果。詳情請參閱[第 41.6.3 節](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)。

宣告 PL/pgSQL 函式的另一種方式是使用 `RETURNS TABLE`，例如：

```

CREATE FUNCTION extended_sales(p_itemno int)
RETURNS TABLE(quantity int, total numeric) AS $$
BEGIN
    RETURN QUERY SELECT s.quantity, s.quantity * s.price FROM sales AS s
                 WHERE s.itemno = p_itemno;
END;
$$ LANGUAGE plpgsql;
```

這完全等同於宣告一個或多個 `OUT` 參數並指定 `RETURNS SETOF
sometype`。

當 PL/pgSQL 函式的回傳型別被宣告為多型型別時（請參閱[第 36.2.5 節](../extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)），系統會建立一個特別的參數 `$0`。它的資料型別就是該函式實際的回傳型別，由實際的輸入型別推導而來。這讓函式能夠取得自己實際的回傳型別，用法如[第 41.3.3 節](plpgsql-declarations.md#PLPGSQL-DECLARATION-TYPE)所示。`$0` 會被初始化為空值，並且可以被函式修改，因此如果需要的話，它可以用來存放回傳值，不過這並非必要。`$0` 也可以被賦予別名。舉例來說，下面這個函式適用於任何具有 `+` 運算子的資料型別：

```

CREATE FUNCTION add_three_values(v1 anyelement, v2 anyelement, v3 anyelement)
RETURNS anyelement AS $$
DECLARE
    result ALIAS FOR $0;
BEGIN
    result := v1 + v2 + v3;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

把一個或多個輸出參數宣告為多型型別，也能得到相同的效果。在這種情況下不會用到特別的 `$0` 參數；輸出參數本身就發揮了相同的作用。例如：

```

CREATE FUNCTION add_three_values(v1 anyelement, v2 anyelement, v3 anyelement,
                                 OUT sum anyelement)
AS $$
BEGIN
    sum := v1 + v2 + v3;
END;
$$ LANGUAGE plpgsql;
```

實務上，使用 `anycompatible` 這一族的型別來宣告多型函式可能更有用，因為這樣會自動把輸入引數提升為共通的型別。例如：

```

CREATE FUNCTION add_three_values(v1 anycompatible, v2 anycompatible, v3 anycompatible)
RETURNS anycompatible AS $$
BEGIN
    RETURN v1 + v2 + v3;
END;
$$ LANGUAGE plpgsql;
```

以這個例子而言，下面這樣的呼叫

```

SELECT add_three_values(1, 2, 4.7);
```

將可以運作，並自動把整數輸入提升為 numeric。而使用 `anyelement` 的函式則會要求你手動把這三個輸入轉型為相同的型別。

<a id="PLPGSQL-DECLARATION-ALIAS"></a>

### 41.3.2. `ALIAS` [#](#PLPGSQL-DECLARATION-ALIAS)

```

newname ALIAS FOR oldname;
```

`ALIAS` 語法比前一節所暗示的更為通用：你可以為任何變數宣告別名，而不只是函式參數。它在實務上的主要用途，是為具有預先決定名稱的變數另外指定一個名稱，例如觸發程序函式中的 `NEW` 或 `OLD`。

範例：

```

DECLARE
  prior ALIAS FOR old;
  updated ALIAS FOR new;
```

由於 `ALIAS` 為同一個物件建立了兩種不同的命名方式，毫無節制地使用可能造成混淆。最好只在要覆蓋預先決定的名稱時才使用它。

<a id="PLPGSQL-DECLARATION-TYPE"></a>

### 41.3.3. 複製型別 [#](#PLPGSQL-DECLARATION-TYPE)

```

name table.column%TYPE
name variable%TYPE
```

`%TYPE` 提供某個資料表欄位或某個先前宣告過的 PL/pgSQL 變數的資料型別。你可以用它來宣告要存放資料庫值的變數。舉例來說，假設你的 `users` 資料表中有一個名為 `user_id` 的欄位。若要宣告一個與 `users.user_id` 具有相同資料型別的變數，你可以寫成：

```

user_id users.user_id%TYPE;
```

在 `%TYPE` 之後也可以加上陣列標示，藉此建立一個存放所參照型別之陣列的變數：

```

user_ids users.user_id%TYPE[];
user_ids users.user_id%TYPE ARRAY[4];  -- equivalent to the above
```

就像宣告陣列型別的資料表欄位一樣，你寫成多組中括號或是指定明確的陣列維度都沒有差別：PostgreSQL 會把某個元素型別的所有陣列視為同一種型別，不論其維度為何。（請參閱[第 8.15.1 節](../../the-sql-language/datatype/arrays.md#ARRAYS-DECLARATION)。）

使用 `%TYPE` 讓你不必知道所參照結構的資料型別；更重要的是，如果所參照項目的資料型別未來有所變更（例如：你把 `user_id` 的型別從 `integer` 改成 `real`），你可能就不需要更動函式定義。

`%TYPE` 在多型函式中特別有價值，因為內部變數所需的資料型別可能每次呼叫都不一樣。只要把 `%TYPE` 套用在函式的引數或結果佔位符上，就可以建立合適的變數。

<a id="PLPGSQL-DECLARATION-ROWTYPES"></a>

### 41.3.4. 資料列型別 [#](#PLPGSQL-DECLARATION-ROWTYPES)

```

name table_name%ROWTYPE;
name composite_type_name;
```

複合型別的變數稱為*資料列*變數（或*資料列型別*變數）。只要查詢的欄位集合與該變數宣告的型別相符，這種變數就能存放 `SELECT` 或 `FOR` 查詢結果的一整筆資料列。資料列值中的個別欄位是以一般的點號標示法來存取，例如 `rowvar.field`。

資料列變數可以使用 *`table_name`*`%ROWTYPE` 標示法，宣告成與某個既有資料表或檢視表的資料列具有相同的型別；也可以透過指定某個複合型別的名稱來宣告。（由於每個資料表都有一個同名的關聯複合型別，因此在 PostgreSQL 中，你寫不寫 `%ROWTYPE` 其實沒有差別。但帶有 `%ROWTYPE` 的寫法可攜性較佳。）

與 `%TYPE` 一樣，`%ROWTYPE` 之後也可以接上陣列標示，以宣告存放所參照複合型別之陣列的變數。

函式的參數可以是複合型別（完整的資料表資料列）。在這種情況下，對應的識別符號 `$n` 會是一個資料列變數，並且可以從中選取欄位，例如 `$1.user_id`。

以下是使用複合型別的一個例子。`table1` 與 `table2` 是既有的資料表，並且至少具有文中提到的那些欄位：

```

CREATE FUNCTION merge_fields(t_row table1) RETURNS text AS $$
DECLARE
    t2_row table2%ROWTYPE;
BEGIN
    SELECT * INTO t2_row FROM table2 WHERE ... ;
    RETURN t_row.f1 || t2_row.f3 || t_row.f5 || t2_row.f7;
END;
$$ LANGUAGE plpgsql;

SELECT merge_fields(t.*) FROM table1 t WHERE ... ;
```

<a id="PLPGSQL-DECLARATION-RECORDS"></a>

### 41.3.5. record 型別 [#](#PLPGSQL-DECLARATION-RECORDS)

```

name RECORD;
```

record 變數與資料列型別變數類似，但它們沒有預先定義的結構。它們會在 `SELECT` 或 `FOR` 指令中被指派資料列時，取得該資料列實際的結構。record 變數的子結構可能在每次被指派時都改變。由此衍生的一個結果是：在 record 變數第一次被指派值之前，它並沒有子結構，任何存取其中欄位的嘗試都會引發執行期錯誤。

請注意 `RECORD` 並不是真正的資料型別，只是一個佔位符。另外也要了解，當 PL/pgSQL 函式被宣告為回傳 `record` 型別時，這與 record 變數並不完全是同一個概念，即使這樣的函式可能會使用 record 變數來存放其結果。在這兩種情況中，撰寫函式時實際的資料列結構都是未知的；但對於回傳 `record` 的函式而言，實際結構是在剖析呼叫端查詢時決定的，而 record 變數則可以隨時動態改變其資料列結構。

<a id="PLPGSQL-DECLARATION-COLLATION"></a>

### 41.3.6. PL/pgSQL 變數的定序 [#](#PLPGSQL-DECLARATION-COLLATION)

<a id="id-1.8.8.5.14.2"></a>

當 PL/pgSQL 函式具有一個以上可定序資料型別的參數時，系統會依據指派給實際引數的定序，為每次函式呼叫識別出一個定序，做法如[第 23.2 節](../../server-administration/charset/collation.md)所述。若成功識別出定序（亦即引數之間的隱含定序沒有衝突），那麼所有可定序的參數都會被視為隱含地具有該定序。這會影響函式內部對定序敏感之操作的行為。例如，考慮以下情況

```

CREATE FUNCTION less_than(a text, b text) RETURNS boolean AS $$
BEGIN
    RETURN a < b;
END;
$$ LANGUAGE plpgsql;

SELECT less_than(text_field_1, text_field_2) FROM table1;
SELECT less_than(text_field_1, text_field_2 COLLATE "C") FROM table1;
```

第一次使用 `less_than` 時，比較會採用 `text_field_1` 與 `text_field_2` 的共通定序，而第二次使用時則會採用 `C` 定序。

此外，被識別出的定序也會被當成任何可定序型別之區域變數的定序。因此，即使把這個函式改寫成下面這樣，其運作方式也不會有任何不同

```

CREATE FUNCTION less_than(a text, b text) RETURNS boolean AS $$
DECLARE
    local_a text := a;
    local_b text := b;
BEGIN
    RETURN local_a < local_b;
END;
$$ LANGUAGE plpgsql;
```

若沒有任何可定序資料型別的參數，或無法為它們識別出共通的定序，則參數與區域變數會使用其資料型別的預設定序（通常就是資料庫的預設定序，但 domain 型別的變數可能會不同）。

在可定序資料型別的區域變數宣告中加入 `COLLATE` 選項，可以讓它關聯到不同的定序，例如

```

DECLARE
    local_a text COLLATE "en_US";
```

這個選項會覆蓋依照上述規則原本會賦予該變數的定序。

此外，當然，如果希望在特定操作中強制使用特定的定序，也可以在函式內部寫上明確的 `COLLATE` 子句。例如，

```

CREATE FUNCTION less_than_c(a text, b text) RETURNS boolean AS $$
BEGIN
    RETURN a < b COLLATE "C";
END;
$$ LANGUAGE plpgsql;
```

這會覆蓋運算式中所用資料表欄位、參數或區域變數所關聯的定序，就像在單純的 SQL 指令中所發生的一樣。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpgsql-declarations.html)（原文版本：18.6；核對日期：2026-09-15）
