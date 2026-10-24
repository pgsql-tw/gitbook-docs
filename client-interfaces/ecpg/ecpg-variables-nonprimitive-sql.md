<a id="ECPG-VARIABLES-NONPRIMITIVE-SQL"></a>

## 34.4.5. 處理非基本 SQL 資料型別 [#](#ecpg-variables-nonprimitive-sql) <a href="#ecpg-variables-nonprimitive-sql" id="ecpg-variables-nonprimitive-sql"></a>

本節說明如何在 ECPG 應用程式中處理非純量與使用者自訂的 SQL 層級資料型別。請注意，這與上一節所述的非基本型別主機變數的處理方式不同。

<a id="ECPG-VARIABLES-NONPRIMITIVE-SQL-ARRAYS"></a>

### 34.4.5.1. 陣列 [#](#ecpg-variables-nonprimitive-sql-arrays) <a href="#ecpg-variables-nonprimitive-sql-arrays" id="ecpg-variables-nonprimitive-sql-arrays"></a>

ECPG 並不直接支援多維的 SQL 層級陣列。一維的 SQL 層級陣列可以對應到 C 陣列主機變數，反之亦然。不過，在建立陳述式時，ecpg 並不知道欄位的型別，因此無法檢查 C 陣列是否輸入到對應的 SQL 層級陣列中。在處理 SQL 陳述式的輸出時，ecpg 擁有必要的資訊，因此會檢查兩者是否都是陣列。

如果查詢分別存取陣列的各個*元素*，就可以避免在 ECPG 中使用陣列。此時應該使用型別可以對應到元素型別的主機變數。例如，若欄位型別是 `integer` 陣列，可以使用 `int` 型別的主機變數。另外，若元素型別是 `varchar` 或 `text`，可以使用 `char[]` 或 `VARCHAR[]` 型別的主機變數。

以下是一個範例。假設有下列資料表：

```

CREATE TABLE t3 (
    ii integer[]
);

testdb=> SELECT * FROM t3;
     ii
-------------
 {1,2,3,4,5}
(1 row)
```

下列範例程式取得陣列的第 4 個元素，並把它存放到 `int` 型別的主機變數中：

```

EXEC SQL BEGIN DECLARE SECTION;
int ii;
EXEC SQL END DECLARE SECTION;

EXEC SQL DECLARE cur1 CURSOR FOR SELECT ii[4] FROM t3;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    EXEC SQL FETCH FROM cur1 INTO :ii ;
    printf("ii=%d\n", ii);
}

EXEC SQL CLOSE cur1;
```

這個範例會顯示下列結果：

```

ii=4
```

若要把多個陣列元素對應到陣列型別主機變數中的多個元素，陣列欄位的每個元素與主機變數陣列的每個元素都必須分別處理，例如：

```

EXEC SQL BEGIN DECLARE SECTION;
int ii_a[8];
EXEC SQL END DECLARE SECTION;

EXEC SQL DECLARE cur1 CURSOR FOR SELECT ii[1], ii[2], ii[3], ii[4] FROM t3;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    EXEC SQL FETCH FROM cur1 INTO :ii_a[0], :ii_a[1], :ii_a[2], :ii_a[3];
    ...
}
```

再次提醒，

```

EXEC SQL BEGIN DECLARE SECTION;
int ii_a[8];
EXEC SQL END DECLARE SECTION;

EXEC SQL DECLARE cur1 CURSOR FOR SELECT ii FROM t3;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* WRONG */
    EXEC SQL FETCH FROM cur1 INTO :ii_a;
    ...
}
```

在這種情況下無法正確運作，因為你不能把陣列型別的欄位直接對應到陣列主機變數。

另一種變通方法是把陣列以其外部字串表示形式存放在 `char[]` 或 `VARCHAR[]` 型別的主機變數中。關於這種表示形式的更多細節，請參閱[第 8.15.2 節](../../the-sql-language/datatype/arrays.md#ARRAYS-INPUT)。請注意，這表示在主機程式中無法自然地把該陣列當作陣列來存取（除非再做剖析文字表示形式的進一步處理）。

<a id="ECPG-VARIABLES-NONPRIMITIVE-SQL-COMPOSITE"></a>

### 34.4.5.2. 複合型別 [#](#ecpg-variables-nonprimitive-sql-composite) <a href="#ecpg-variables-nonprimitive-sql-composite" id="ecpg-variables-nonprimitive-sql-composite"></a>

ECPG 並不直接支援複合型別，但可以採用簡單的變通方法。可用的變通方法與上面針對陣列所述的方法類似：分別存取每個屬性，或使用外部字串表示形式。

在下列範例中，假設有下列型別與資料表：

```

CREATE TYPE comp_t AS (intval integer, textval varchar(32));
CREATE TABLE t4 (compval comp_t);
INSERT INTO t4 VALUES ( (256, 'PostgreSQL') );
```

最直接的解法是分別存取每個屬性。下列程式分別選取 `comp_t` 型別的每個屬性，從範例資料表取得資料：

```

EXEC SQL BEGIN DECLARE SECTION;
int intval;
varchar textval[33];
EXEC SQL END DECLARE SECTION;

/* Put each element of the composite type column in the SELECT list. */
EXEC SQL DECLARE cur1 CURSOR FOR SELECT (compval).intval, (compval).textval FROM t4;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* Fetch each element of the composite type column into host variables. */
    EXEC SQL FETCH FROM cur1 INTO :intval, :textval;

    printf("intval=%d, textval=%s\n", intval, textval.arr);
}

EXEC SQL CLOSE cur1;
```

為了改進這個範例，可以把用來存放 `FETCH` 命令中值的主機變數集中到一個結構中。關於結構形式主機變數的更多細節，請參閱[第 34.4.4.3.2 節](ecpg-variables-nonprimitive-c.md#ecpg-variables-struct)。若要改用結構，可以把範例修改如下。兩個主機變數 `intval` 與 `textval` 成為 `comp_t` 結構的成員，並在 `FETCH` 命令中指定該結構。

```

EXEC SQL BEGIN DECLARE SECTION;
typedef struct
{
    int intval;
    varchar textval[33];
} comp_t;

comp_t compval;
EXEC SQL END DECLARE SECTION;

/* Put each element of the composite type column in the SELECT list. */
EXEC SQL DECLARE cur1 CURSOR FOR SELECT (compval).intval, (compval).textval FROM t4;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* Put all values in the SELECT list into one structure. */
    EXEC SQL FETCH FROM cur1 INTO :compval;

    printf("intval=%d, textval=%s\n", compval.intval, compval.textval.arr);
}

EXEC SQL CLOSE cur1;
```

雖然 `FETCH` 命令中使用了結構，但 `SELECT` 子句中的屬性名稱仍是逐一指定的。這可以改用 `*` 來要求取得複合型別值的所有屬性，加以改進。

```

...
EXEC SQL DECLARE cur1 CURSOR FOR SELECT (compval).* FROM t4;
EXEC SQL OPEN cur1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    /* Put all values in the SELECT list into one structure. */
    EXEC SQL FETCH FROM cur1 INTO :compval;

    printf("intval=%d, textval=%s\n", compval.intval, compval.textval.arr);
}
...
```

如此一來，即使 ECPG 本身並不理解複合型別，複合型別也幾乎可以無縫地對應到結構。

最後，也可以把複合型別的值以其外部字串表示形式存放在 `char[]` 或 `VARCHAR[]` 型別的主機變數中。但用這種方式，從主機程式存取該值的各個欄位就不太容易。

<a id="ECPG-VARIABLES-NONPRIMITIVE-SQL-USER-DEFINED-BASE-TYPES"></a>

### 34.4.5.3. 使用者自訂基本型別 [#](#ecpg-variables-nonprimitive-sql-user-defined-base-types) <a href="#ecpg-variables-nonprimitive-sql-user-defined-base-types" id="ecpg-variables-nonprimitive-sql-user-defined-base-types"></a>

ECPG 並不直接支援新的使用者自訂基本型別。你可以使用外部字串表示形式與 `char[]` 或 `VARCHAR[]` 型別的主機變數，而這個解法對許多型別而言確實恰當且足夠。

以下範例使用[第 36.13 節](../../server-programming/extend/xtypes.md)範例中的 `complex` 資料型別。該型別的外部字串表示形式是 `(%f,%f)`，定義於[第 36.13 節](../../server-programming/extend/xtypes.md)中的函式 `complex_in()` 與 `complex_out()`。下列範例把 complex 型別的值 `(1,1)` 與 `(3,3)` 插入欄位 `a` 與 `b`，之後再從資料表中把它們選取出來。

```

EXEC SQL BEGIN DECLARE SECTION;
    varchar a[64];
    varchar b[64];
EXEC SQL END DECLARE SECTION;

    EXEC SQL INSERT INTO test_complex VALUES ('(1,1)', '(3,3)');

    EXEC SQL DECLARE cur1 CURSOR FOR SELECT a, b FROM test_complex;
    EXEC SQL OPEN cur1;

    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        EXEC SQL FETCH FROM cur1 INTO :a, :b;
        printf("a=%s, b=%s\n", a.arr, b.arr);
    }

    EXEC SQL CLOSE cur1;
```

這個範例會顯示下列結果：

```

a=(1,1), b=(3,3)
```

另一種變通方法是避免在 ECPG 中直接使用使用者自訂型別，改為建立一個函式或型別轉換，在使用者自訂型別與 ECPG 能處理的基本型別之間進行轉換。不過請注意，型別轉換（尤其是隱含轉換）應該非常謹慎地引入型別系統。

例如：

```

CREATE FUNCTION create_complex(r double, i double) RETURNS complex
LANGUAGE SQL
IMMUTABLE
AS $$ SELECT $1 * complex '(1,0')' + $2 * complex '(0,1)' $$;
```

譯註：原文此範例有兩處問題，範例程式碼依原文保留：一是字串常數 '(1,0')' 引號位置有誤，正確應為 '(1,0)'；二是 create_complex 的參數型別寫作 double，但 PostgreSQL 內建的 SQL 型別名稱是 double precision（SQL 中沒有單獨的 double 型別），正確寫法為 create_complex(r double precision, i double precision)。

在這個定義之後，下列程式

```

EXEC SQL BEGIN DECLARE SECTION;
double a, b, c, d;
EXEC SQL END DECLARE SECTION;

a = 1;
b = 2;
c = 3;
d = 4;

EXEC SQL INSERT INTO test_complex VALUES (create_complex(:a, :b), create_complex(:c, :d));
```

的效果等同於

```

EXEC SQL INSERT INTO test_complex VALUES ('(1,2)', '(3,4)');
```

[返回 34.4. 使用主機變數](ecpg-variables.md#ecpg-variables)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-variables.html)（原文版本：18.6；核對日期：2026-10-18）
