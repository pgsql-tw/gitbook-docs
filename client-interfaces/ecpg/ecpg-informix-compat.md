<a id="ECPG-INFORMIX-COMPAT"></a>

## 34.15. Informix 相容模式 [#](#ECPG-INFORMIX-COMPAT)

[34.15.1. 額外的型別](ecpg-informix-compat.md#ECPG-INFORMIX-TYPES)

[34.15.2. 額外／缺少的嵌入式 SQL 陳述式](ecpg-informix-compat.md#ECPG-INFORMIX-STATEMENTS)

[34.15.3. 與 Informix 相容的 SQLDA 描述區](ecpg-informix-compat.md#ECPG-INFORMIX-SQLDA)

[34.15.4. 額外的函式](ecpg-informix-compat.md#ECPG-INFORMIX-FUNCTIONS)

[34.15.5. 額外的常數](ecpg-informix-compat.md#ECPG-INFORMIX-CONSTANTS)

`ecpg` 可以在所謂的 *Informix 相容模式*下執行。啟用此模式時，它會嘗試表現得如同 Informix E/SQL 的 Informix 預編譯器一樣。一般來說，這讓你可以用錢字號取代 `EXEC SQL` 基本指令，來引導嵌入式 SQL 命令：

```

$int j = 3;
$CONNECT TO :dbname;
$CREATE TABLE test(i INT PRIMARY KEY, j INT);
$INSERT INTO test(i, j) VALUES (7, :j);
$COMMIT;
```

### 注意

`$` 與其後的前置處理器指令（也就是 `include`、`define`、`ifdef` 等）之間不可以有任何空白。否則，前置處理器會將該語法單元剖析為主機變數。

相容模式有兩種：`INFORMIX`、`INFORMIX_SE`

連結使用此相容模式的程式時，記得要連結 ECPG 隨附的 `libcompat`。

除了前面說明的語法糖之外，Informix 相容模式還將 E/SQL 中常見的一些資料輸入、輸出與轉換函式，以及嵌入式 SQL 陳述式移植到 ECPG。

Informix 相容模式與 ECPG 的 pgtypeslib 函式庫密切相關。pgtypeslib 將 SQL 資料型別對應到 C 主機程式中的資料型別，而 Informix 相容模式的大多數額外函式，讓你可以對這些 C 主機程式型別進行操作。不過請注意，相容的程度是有限的。它並不試圖複製 Informix 的行為；它讓你可以進行大致相同的操作，並提供名稱相同、基本行為也相同的函式，但如果你目前正在使用 Informix，它並不能直接替換。此外，有些資料型別並不相同。例如，PostgreSQL 的 datetime 與 interval 型別不認得像 `YEAR TO MINUTE` 這樣的範圍，因此你在 ECPG 中也找不到對此的支援。

<a id="ECPG-INFORMIX-TYPES"></a>

### 34.15.1. 額外的型別 [#](#ECPG-INFORMIX-TYPES)

Informix 特有的「string」虛擬型別用於儲存已去除右側空白的字元字串資料，現在於 Informix 模式中不需使用 `typedef` 即可支援。事實上，在 Informix 模式中，ECPG 會拒絕處理含有 `typedef sometype string;` 的原始檔。

```

EXEC SQL BEGIN DECLARE SECTION;
string userid; /* this variable will contain trimmed data */
EXEC SQL END DECLARE SECTION;

EXEC SQL FETCH MYCUR INTO :userid;
```

<a id="ECPG-INFORMIX-STATEMENTS"></a>

### 34.15.2. 額外／缺少的嵌入式 SQL 陳述式 [#](#ECPG-INFORMIX-STATEMENTS)

<a id="ECPG-INFORMIX-STATEMENTS-CLOSE-DATABASE"></a>

`CLOSE DATABASE` [#](#ECPG-INFORMIX-STATEMENTS-CLOSE-DATABASE)
:   此陳述式會關閉目前的連線。事實上，它是 ECPG 的 `DISCONNECT CURRENT` 的同義詞：

    ```

    $CLOSE DATABASE;                /* close the current connection */
    EXEC SQL CLOSE DATABASE;
    ```
<a id="ECPG-INFORMIX-STATEMENTS-FREE-CURSOR-NAME"></a>

`FREE cursor_name` [#](#ECPG-INFORMIX-STATEMENTS-FREE-CURSOR-NAME)
:   由於 ECPG 的運作方式與 Informix 的 ESQL/C 不同（也就是哪些步驟純屬語法轉換、哪些步驟仰賴底層的執行時期函式庫），ECPG 中沒有 `FREE cursor_name` 陳述式。這是因為在 ECPG 中，`DECLARE CURSOR` 並不會轉換成對執行時期函式庫、使用該游標名稱的函式呼叫。這表示 ECPG 執行時期函式庫中並不會在執行時期記錄 SQL 游標，只有 PostgreSQL 伺服器會記錄。
<a id="ECPG-INFORMIX-STATEMENTS-FREE-STATEMENT-NAME"></a>

`FREE statement_name` [#](#ECPG-INFORMIX-STATEMENTS-FREE-STATEMENT-NAME)
:   `FREE statement_name` 是 `DEALLOCATE PREPARE statement_name` 的同義詞。

<a id="ECPG-INFORMIX-SQLDA"></a>

### 34.15.3. 與 Informix 相容的 SQLDA 描述區 [#](#ECPG-INFORMIX-SQLDA)

Informix 相容模式支援的結構與[第 34.7.2 節](ecpg-descriptors.md#ECPG-SQLDA-DESCRIPTORS)所述的結構不同。請見下方：

```

struct sqlvar_compat
{
    short   sqltype;
    int     sqllen;
    char   *sqldata;
    short  *sqlind;
    char   *sqlname;
    char   *sqlformat;
    short   sqlitype;
    short   sqlilen;
    char   *sqlidata;
    int     sqlxid;
    char   *sqltypename;
    short   sqltypelen;
    short   sqlownerlen;
    short   sqlsourcetype;
    char   *sqlownername;
    int     sqlsourceid;
    char   *sqlilongdata;
    int     sqlflags;
    void   *sqlreserved;
};

struct sqlda_compat
{
    short  sqld;
    struct sqlvar_compat *sqlvar;
    char   desc_name[19];
    short  desc_occ;
    struct sqlda_compat *desc_next;
    void  *reserved;
};

typedef struct sqlvar_compat    sqlvar_t;
typedef struct sqlda_compat     sqlda_t;
```

整體屬性如下：

<a id="ECPG-INFORMIX-SQLDA-SQLD"></a>

`sqld` [#](#ECPG-INFORMIX-SQLDA-SQLD)
:   `SQLDA` 描述區中的欄位數。
<a id="ECPG-INFORMIX-SQLDA-SQLVAR"></a>

`sqlvar` [#](#ECPG-INFORMIX-SQLDA-SQLVAR)
:   指向各欄位屬性的指標。
<a id="ECPG-INFORMIX-SQLDA-DESC-NAME"></a>

`desc_name` [#](#ECPG-INFORMIX-SQLDA-DESC-NAME)
:   未使用，以零位元組填滿。
<a id="ECPG-INFORMIX-SQLDA-DESC-OCC"></a>

`desc_occ` [#](#ECPG-INFORMIX-SQLDA-DESC-OCC)
:   已配置結構的大小。
<a id="ECPG-INFORMIX-SQLDA-DESC-NEXT"></a>

`desc_next` [#](#ECPG-INFORMIX-SQLDA-DESC-NEXT)
:   若結果集包含超過一筆記錄，則為指向下一個 SQLDA 結構的指標。
<a id="ECPG-INFORMIX-SQLDA-RESERVED"></a>

`reserved` [#](#ECPG-INFORMIX-SQLDA-RESERVED)
:   未使用的指標，內容為 NULL。為了與 Informix 相容而保留。

各欄位的屬性如下，它們儲存在 `sqlvar` 陣列中：

<a id="ECPG-INFORMIX-SQLDA-SQLTYPE"></a>

`sqltype` [#](#ECPG-INFORMIX-SQLDA-SQLTYPE)
:   欄位的型別。常數定義在 `sqltypes.h` 中
<a id="ECPG-INFORMIX-SQLDA-SQLLEN"></a>

`sqllen` [#](#ECPG-INFORMIX-SQLDA-SQLLEN)
:   欄位資料的長度。
<a id="ECPG-INFORMIX-SQLDA-SQLDATA"></a>

`sqldata` [#](#ECPG-INFORMIX-SQLDA-SQLDATA)
:   指向欄位資料的指標。此指標的型別為 `char *`，它所指向的資料採二進位格式。範例：

    ```

    int intval;

    switch (sqldata->sqlvar[i].sqltype)
    {
        case SQLINTEGER:
            intval = *(int *)sqldata->sqlvar[i].sqldata;
            break;
      ...
    }
    ```
<a id="ECPG-INFORMIX-SQLDA-SQLIND"></a>

`sqlind` [#](#ECPG-INFORMIX-SQLDA-SQLIND)
:   指向 NULL 指示變數的指標。若是由 DESCRIBE 或 FETCH 傳回，它一律是有效的指標。若用作 `EXECUTE ... USING sqlda;` 的輸入，則 NULL 指標值表示此欄位的值不是 NULL。否則，必須正確設定有效的指標與 `sqlitype`。範例：

    ```

    if (*(int2 *)sqldata->sqlvar[i].sqlind != 0)
        printf("value is NULL\n");
    ```
<a id="ECPG-INFORMIX-SQLDA-SQLNAME"></a>

`sqlname` [#](#ECPG-INFORMIX-SQLDA-SQLNAME)
:   欄位的名稱。以 0 結尾的字串。
<a id="ECPG-INFORMIX-SQLDA-SQLFORMAT"></a>

`sqlformat` [#](#ECPG-INFORMIX-SQLDA-SQLFORMAT)
:   在 Informix 中為保留欄位；此處為該欄位的 [`PQfformat`](../libpq/libpq-exec.md#LIBPQ-PQFFORMAT) 值。
<a id="ECPG-INFORMIX-SQLDA-SQLITYPE"></a>

`sqlitype` [#](#ECPG-INFORMIX-SQLDA-SQLITYPE)
:   NULL 指示變數資料的型別。從伺服器傳回資料時，它一律是 SQLSMINT。當 `SQLDA` 用於參數化查詢時，資料會依所設定的型別處理。
<a id="ECPG-INFORMIX-SQLDA-SQLILEN"></a>

`sqlilen` [#](#ECPG-INFORMIX-SQLDA-SQLILEN)
:   NULL 指示變數資料的長度。
<a id="ECPG-INFORMIX-SQLDA-SQLXID"></a>

`sqlxid` [#](#ECPG-INFORMIX-SQLDA-SQLXID)
:   欄位的擴充型別，即 [`PQftype`](../libpq/libpq-exec.md#LIBPQ-PQFTYPE) 的結果。
<a id="ECPG-INFORMIX-SQLDA-SQLTYPENAME"></a>

`sqltypename`<br>`sqltypelen`<br>`sqlownerlen`<br>`sqlsourcetype`<br>`sqlownername`<br>`sqlsourceid`<br>`sqlflags`<br>`sqlreserved` [#](#ECPG-INFORMIX-SQLDA-SQLTYPENAME)
:   未使用。
<a id="ECPG-INFORMIX-SQLDA-SQLILONGDATA"></a>

`sqlilongdata` [#](#ECPG-INFORMIX-SQLDA-SQLILONGDATA)
:   若 `sqllen` 大於 32kB，它會等於 `sqldata`。

範例：

```

EXEC SQL INCLUDE sqlda.h;

    sqlda_t        *sqlda; /* This doesn't need to be under embedded DECLARE SECTION */

    EXEC SQL BEGIN DECLARE SECTION;
    char *prep_stmt = "select * from table1";
    int i;
    EXEC SQL END DECLARE SECTION;

    ...

    EXEC SQL PREPARE mystmt FROM :prep_stmt;

    EXEC SQL DESCRIBE mystmt INTO sqlda;

    printf("# of fields: %d\n", sqlda->sqld);
    for (i = 0; i < sqlda->sqld; i++)
      printf("field %d: \"%s\"\n", sqlda->sqlvar[i]->sqlname);

    EXEC SQL DECLARE mycursor CURSOR FOR mystmt;
    EXEC SQL OPEN mycursor;
    EXEC SQL WHENEVER NOT FOUND GOTO out;

    while (1)
    {
      EXEC SQL FETCH mycursor USING sqlda;
    }

    EXEC SQL CLOSE mycursor;

    free(sqlda); /* The main structure is all to be free(),
                  * sqlda and sqlda->sqlvar is in one allocated area */
```

譯註：上方範例程式碼依原文保留，僅在此說明幾點：一是迴圈中 printf 的格式字串含有兩個轉換規格（%d 與 %s），卻只傳入一個引數，缺少欄位序號 i；二是 sqlvar 是指向 struct sqlvar_compat 的指標，sqlda->sqlvar[i] 本身是結構而非指標，因此應寫作 sqlda->sqlvar[i].sqlname（與前文 sqldata 範例的寫法一致），而不是 sqlda->sqlvar[i]->sqlname；也就是說，該行應以 i 與 sqlda->sqlvar[i].sqlname 兩個引數呼叫 printf。此外，WHENEVER NOT FOUND GOTO out 所指的標籤 out 並未出現在摘錄中，實際使用時須自行定義。

更多資訊請參閱 `sqlda.h` 標頭檔與 `src/interfaces/ecpg/test/compat_informix/sqlda.pgc` 迴歸測試。

<a id="ECPG-INFORMIX-FUNCTIONS"></a>

### 34.15.4. 額外的函式 [#](#ECPG-INFORMIX-FUNCTIONS)

<a id="ECPG-INFORMIX-FUNCTIONS-DECADD"></a>

`decadd` [#](#ECPG-INFORMIX-FUNCTIONS-DECADD)
:   將兩個 decimal 型別的值相加。

    ```

    int decadd(decimal *arg1, decimal *arg2, decimal *sum);
    ```

    此函式接收一個指向 decimal 型別第一個運算元的指標（`arg1`）、一個指向 decimal 型別第二個運算元的指標（`arg2`），以及一個指向將存放總和之 decimal 型別值的指標（`sum`）。成功時，此函式傳回 0。發生溢位時傳回 `ECPG_INFORMIX_NUM_OVERFLOW`，發生下溢時傳回 `ECPG_INFORMIX_NUM_UNDERFLOW`。其他失敗情況則傳回 -1，並將 `errno` 設為 pgtypeslib 中對應的 `errno` 編號。
<a id="ECPG-INFORMIX-FUNCTIONS-DECCMP"></a>

`deccmp` [#](#ECPG-INFORMIX-FUNCTIONS-DECCMP)
:   比較兩個 decimal 型別的變數。

    ```

    int deccmp(decimal *arg1, decimal *arg2);
    ```

    此函式接收一個指向第一個 decimal 值的指標（`arg1`）與一個指向第二個 decimal 值的指標（`arg2`），並傳回一個整數值，表示哪一個值較大。

    * 1：若 `arg1` 所指的值大於 `var2` 所指的值（原文此處寫作 var2；此函式並沒有名為 var2 的參數，應為 arg2）
    * -1：若 `arg1` 所指的值小於 `arg2` 所指的值
    * 0：若 `arg1` 所指的值與 `arg2` 所指的值相等
<a id="ECPG-INFORMIX-FUNCTIONS-DECCOPY"></a>

`deccopy` [#](#ECPG-INFORMIX-FUNCTIONS-DECCOPY)
:   複製一個 decimal 值。

    ```

    void deccopy(decimal *src, decimal *target);
    ```

    此函式的第一個引數是指向要複製之 decimal 值的指標（`src`），第二個引數是指向 decimal 型別目標結構的指標（`target`）。
<a id="ECPG-INFORMIX-FUNCTIONS-DECCVASC"></a>

`deccvasc` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVASC)
:   將值從其 ASCII 表示法轉換為 decimal 型別。

    ```

    int deccvasc(char *cp, int len, decimal *np);
    ```

    此函式接收一個指向字串的指標，該字串包含要轉換之數字的字串表示法（`cp`），以及其長度 `len`。`np` 是指向用來儲存運算結果之 decimal 值的指標。

    有效格式的例子如：`-2`、`.794`、`+3.44`、`592.49E07` 或 `-32.84e-4`。

    此函式成功時傳回 0。若發生溢位或下溢，會傳回 `ECPG_INFORMIX_NUM_OVERFLOW` 或 `ECPG_INFORMIX_NUM_UNDERFLOW`。若無法剖析 ASCII 表示法，會傳回 `ECPG_INFORMIX_BAD_NUMERIC`；若此問題是在剖析指數時發生，則傳回 `ECPG_INFORMIX_BAD_EXPONENT`。
<a id="ECPG-INFORMIX-FUNCTIONS-DECCVDBL"></a>

`deccvdbl` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVDBL)
:   將 double 型別的值轉換為 decimal 型別的值。

    ```

    int deccvdbl(double dbl, decimal *np);
    ```

    此函式的第一個引數是要轉換的 double 型別變數（`dbl`）。第二個引數（`np`）是指向用來存放運算結果之 decimal 變數的指標。

    此函式成功時傳回 0，轉換失敗時傳回負值。
<a id="ECPG-INFORMIX-FUNCTIONS-DECCVINT"></a>

`deccvint` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVINT)
:   將 int 型別的值轉換為 decimal 型別的值。

    ```

    int deccvint(int in, decimal *np);
    ```

    此函式的第一個引數是要轉換的 int 型別變數（`in`）。第二個引數（`np`）是指向用來存放運算結果之 decimal 變數的指標。

    此函式成功時傳回 0，轉換失敗時傳回負值。
<a id="ECPG-INFORMIX-FUNCTIONS-DECCVLONG"></a>

`deccvlong` [#](#ECPG-INFORMIX-FUNCTIONS-DECCVLONG)
:   將 long 型別的值轉換為 decimal 型別的值。

    ```

    int deccvlong(long lng, decimal *np);
    ```

    此函式的第一個引數是要轉換的 long 型別變數（`lng`）。第二個引數（`np`）是指向用來存放運算結果之 decimal 變數的指標。

    此函式成功時傳回 0，轉換失敗時傳回負值。
<a id="ECPG-INFORMIX-FUNCTIONS-DECDIV"></a>

`decdiv` [#](#ECPG-INFORMIX-FUNCTIONS-DECDIV)
:   將兩個 decimal 型別的變數相除。

    ```

    int decdiv(decimal *n1, decimal *n2, decimal *result);
    ```

    此函式接收分別指向第一個運算元（`n1`）與第二個運算元（`n2`）之變數的指標，並計算 `n1`/`n2`。`result` 是指向用來存放運算結果之變數的指標。

    成功時傳回 0，除法失敗時傳回負值。若發生溢位或下溢，此函式會分別傳回 `ECPG_INFORMIX_NUM_OVERFLOW` 或 `ECPG_INFORMIX_NUM_UNDERFLOW`。若偵測到除以零的嘗試，此函式會傳回 `ECPG_INFORMIX_DIVIDE_ZERO`。
<a id="ECPG-INFORMIX-FUNCTIONS-DECMUL"></a>

`decmul` [#](#ECPG-INFORMIX-FUNCTIONS-DECMUL)
:   將兩個 decimal 值相乘。

    ```

    int decmul(decimal *n1, decimal *n2, decimal *result);
    ```

    此函式接收分別指向第一個運算元（`n1`）與第二個運算元（`n2`）之變數的指標，並計算 `n1`\*`n2`。`result` 是指向用來存放運算結果之變數的指標。

    成功時傳回 0，乘法失敗時傳回負值。若發生溢位或下溢，此函式會分別傳回 `ECPG_INFORMIX_NUM_OVERFLOW` 或 `ECPG_INFORMIX_NUM_UNDERFLOW`。
<a id="ECPG-INFORMIX-FUNCTIONS-DECSUB"></a>

`decsub` [#](#ECPG-INFORMIX-FUNCTIONS-DECSUB)
:   將一個 decimal 值減去另一個 decimal 值。

    ```

    int decsub(decimal *n1, decimal *n2, decimal *result);
    ```

    此函式接收分別指向第一個運算元（`n1`）與第二個運算元（`n2`）之變數的指標，並計算 `n1`-`n2`。`result` 是指向用來存放運算結果之變數的指標。

    成功時傳回 0，減法失敗時傳回負值。若發生溢位或下溢，此函式會分別傳回 `ECPG_INFORMIX_NUM_OVERFLOW` 或 `ECPG_INFORMIX_NUM_UNDERFLOW`。
<a id="ECPG-INFORMIX-FUNCTIONS-DECTOASC"></a>

`dectoasc` [#](#ECPG-INFORMIX-FUNCTIONS-DECTOASC)
:   將 decimal 型別的變數轉換為其 ASCII 表示法，存放在 C 的 char\* 字串中。

    ```

    int dectoasc(decimal *np, char *cp, int len, int right)
    ```

    此函式接收一個指向 decimal 型別變數的指標（`np`），並將其轉換為文字表示法。`cp` 是用來存放運算結果的緩衝區。參數 `right` 指定輸出中應包含小數點右側的幾位數字。結果會四捨五入到這個小數位數。將 `right` 設為 -1 表示輸出中應包含所有可用的小數位數。若由 `len` 指出的輸出緩衝區長度不足以存放包含結尾零位元組在內的文字表示法，結果中只會存放單一個 `*` 字元，並傳回 -1。

    若緩衝區 `cp` 太小，此函式會傳回 -1；若記憶體耗盡，則傳回 `ECPG_INFORMIX_OUT_OF_MEMORY`。

    譯註：上方函式宣告依原文保留，原文漏了結尾的分號；正確的 C 宣告應以分號結尾。
<a id="ECPG-INFORMIX-FUNCTIONS-DECTODBL"></a>

`dectodbl` [#](#ECPG-INFORMIX-FUNCTIONS-DECTODBL)
:   將 decimal 型別的變數轉換為 double。

    ```

    int dectodbl(decimal *np, double *dblp);
    ```

    此函式接收一個指向要轉換之 decimal 值的指標（`np`），以及一個指向用來存放運算結果之 double 變數的指標（`dblp`）。

    成功時傳回 0，轉換失敗時傳回負值。
<a id="ECPG-INFORMIX-FUNCTIONS-DECTOINT"></a>

`dectoint` [#](#ECPG-INFORMIX-FUNCTIONS-DECTOINT)
:   將 decimal 型別的變數轉換為整數。

    ```

    int dectoint(decimal *np, int *ip);
    ```

    此函式接收一個指向要轉換之 decimal 值的指標（`np`），以及一個指向用來存放運算結果之整數變數的指標（`ip`）。

    成功時傳回 0，轉換失敗時傳回負值。若發生溢位，則傳回 `ECPG_INFORMIX_NUM_OVERFLOW`。

    請注意，ECPG 的實作與 Informix 的實作不同。Informix 將整數限制在 -32767 到 32767 的範圍內，而 ECPG 實作中的範圍則取決於系統架構（`INT_MIN .. INT_MAX`）。
<a id="ECPG-INFORMIX-FUNCTIONS-DECTOLONG"></a>

`dectolong` [#](#ECPG-INFORMIX-FUNCTIONS-DECTOLONG)
:   將 decimal 型別的變數轉換為長整數。

    ```

    int dectolong(decimal *np, long *lngp);
    ```

    此函式接收一個指向要轉換之 decimal 值的指標（`np`），以及一個指向用來存放運算結果之 long 變數的指標（`lngp`）。

    成功時傳回 0，轉換失敗時傳回負值。若發生溢位，則傳回 `ECPG_INFORMIX_NUM_OVERFLOW`。

    請注意，ECPG 的實作與 Informix 的實作不同。Informix 將長整數限制在 -2,147,483,647 到 2,147,483,647 的範圍內，而 ECPG 實作中的範圍則取決於系統架構（`-LONG_MAX ..
    LONG_MAX`）。
<a id="ECPG-INFORMIX-FUNCTIONS-RDATESTR"></a>

`rdatestr` [#](#ECPG-INFORMIX-FUNCTIONS-RDATESTR)
:   將日期轉換為 C 的 char\* 字串。

    ```

    int rdatestr(date d, char *str);
    ```

    此函式接收兩個引數，第一個是要轉換的日期（`d`），第二個是指向目標字串的指標。輸出格式一律為 `yyyy-mm-dd`，因此你需要為該字串配置至少 11 個位元組（包含結尾的零位元組）。

    此函式成功時傳回 0，發生錯誤時傳回負值。

    請注意，ECPG 的實作與 Informix 的實作不同。在 Informix 中，可以透過設定環境變數來影響格式。然而在 ECPG 中，你無法變更輸出格式。
<a id="ECPG-INFORMIX-FUNCTIONS-RSTRDATE"></a>

`rstrdate` [#](#ECPG-INFORMIX-FUNCTIONS-RSTRDATE)
:   剖析日期的文字表示法。

    ```

    int rstrdate(char *str, date *d);
    ```

    此函式接收要轉換之日期的文字表示法（`str`），以及一個指向 date 型別變數的指標（`d`）。此函式不允許你指定格式遮罩。它使用 Informix 的預設格式遮罩，也就是 `mm/dd/yyyy`。在內部，此函式是以 `rdefmtdate` 實作的。因此，`rstrdate` 並不會比較快；如果可以選擇，你應該改用 `rdefmtdate`，它讓你可以明確指定格式遮罩。

    此函式的傳回值與 `rdefmtdate` 相同。
<a id="ECPG-INFORMIX-FUNCTIONS-RTODAY"></a>

`rtoday` [#](#ECPG-INFORMIX-FUNCTIONS-RTODAY)
:   取得目前日期。

    ```

    void rtoday(date *d);
    ```

    此函式接收一個指向 date 變數的指標（`d`），並將該變數設為目前日期。

    在內部，此函式使用 [`PGTYPESdate_today`](ecpg-pgtypes.md#PGTYPESDATETODAY) 函式。
<a id="ECPG-INFORMIX-FUNCTIONS-RJULMDY"></a>

`rjulmdy` [#](#ECPG-INFORMIX-FUNCTIONS-RJULMDY)
:   從 date 型別的變數中取出日、月、年的值。

    ```

    int rjulmdy(date d, short mdy[3]);
    ```

    此函式接收日期 `d`，以及一個指向由 3 個短整數值組成之陣列 `mdy` 的指標。變數名稱表示了先後順序：`mdy[0]` 會設為月份的數字，`mdy[1]` 會設為日的值，而 `mdy[2]` 會包含年份。

    此函式目前一律傳回 0。

    在內部，此函式使用 [`PGTYPESdate_julmdy`](ecpg-pgtypes.md#PGTYPESDATEJULMDY) 函式。
<a id="ECPG-INFORMIX-FUNCTIONS-RDEFMTDATE"></a>

`rdefmtdate` [#](#ECPG-INFORMIX-FUNCTIONS-RDEFMTDATE)
:   使用格式遮罩，將字元字串轉換為 date 型別的值。

    ```

    int rdefmtdate(date *d, char *fmt, char *str);
    ```

    此函式接收一個指向用來存放運算結果之 date 值的指標（`d`）、剖析日期時使用的格式遮罩（`fmt`），以及內含日期文字表示法的 C char\* 字串（`str`）。文字表示法應該要符合格式遮罩。不過，字串與格式遮罩之間不需要一對一對應。此函式只分析先後順序，並尋找表示年份位置的字面值 `yy` 或 `yyyy`、表示月份位置的 `mm`，以及表示日位置的 `dd`。

    此函式會傳回下列值：

    * 0 - 此函式順利結束。
    * `ECPG_INFORMIX_ENOSHORTDATE` - 日期的日、月、年之間沒有分隔符號。在此情況下，輸入字串的長度必須剛好是 6 或 8 個位元組，但實際上並非如此。
    * `ECPG_INFORMIX_ENOTDMY` - 格式字串未正確指出年、月、日的先後順序。
    * `ECPG_INFORMIX_BAD_DAY` - 輸入字串不包含有效的日。
    * `ECPG_INFORMIX_BAD_MONTH` - 輸入字串不包含有效的月份。
    * `ECPG_INFORMIX_BAD_YEAR` - 輸入字串不包含有效的年份。

    在內部，此函式是以 [`PGTYPESdate_defmt_asc`](ecpg-pgtypes.md#PGTYPESDATEDEFMTASC) 函式實作的。輸入範例表請參閱該處的說明。
<a id="ECPG-INFORMIX-FUNCTIONS-RFMTDATE"></a>

`rfmtdate` [#](#ECPG-INFORMIX-FUNCTIONS-RFMTDATE)
:   使用格式遮罩，將 date 型別的變數轉換為其文字表示法。

    ```

    int rfmtdate(date d, char *fmt, char *str);
    ```

    此函式接收要轉換的日期（`d`）、格式遮罩（`fmt`），以及將存放日期文字表示法的字串（`str`）。

    成功時傳回 0，發生錯誤時傳回負值。

    在內部，此函式使用 [`PGTYPESdate_fmt_asc`](ecpg-pgtypes.md#PGTYPESDATEFMTASC) 函式，範例請參閱該處的說明。
<a id="ECPG-INFORMIX-FUNCTIONS-RMDYJUL"></a>

`rmdyjul` [#](#ECPG-INFORMIX-FUNCTIONS-RMDYJUL)
:   從一個由 3 個短整數組成、指定日期之日、月、年的陣列，建立 date 值。

    ```

    int rmdyjul(short mdy[3], date *d);
    ```

    此函式接收由 3 個短整數組成的陣列（`mdy`），以及一個指向用來存放運算結果之 date 型別變數的指標。

    目前此函式一律傳回 0。

    在內部，此函式是以 [`PGTYPESdate_mdyjul`](ecpg-pgtypes.md#PGTYPESDATEMDYJUL) 函式實作的。
<a id="ECPG-INFORMIX-FUNCTIONS-RDAYOFWEEK"></a>

`rdayofweek` [#](#ECPG-INFORMIX-FUNCTIONS-RDAYOFWEEK)
:   傳回一個數字，表示某個日期值是星期幾。

    ```

    int rdayofweek(date d);
    ```

    此函式以日期變數 `d` 作為唯一的引數，並傳回一個整數，表示該日期是星期幾。

    * 0 - 星期日
    * 1 - 星期一
    * 2 - 星期二
    * 3 - 星期三
    * 4 - 星期四
    * 5 - 星期五
    * 6 - 星期六

    在內部，此函式是以 [`PGTYPESdate_dayofweek`](ecpg-pgtypes.md#PGTYPESDATEDAYOFWEEK) 函式實作的。
<a id="ECPG-INFORMIX-FUNCTIONS-DTCURRENT"></a>

`dtcurrent` [#](#ECPG-INFORMIX-FUNCTIONS-DTCURRENT)
:   取得目前的時間戳記。

    ```

    void dtcurrent(timestamp *ts);
    ```

    此函式取得目前的時間戳記，並將它存入 `ts` 所指向的 timestamp 變數。
<a id="ECPG-INFORMIX-FUNCTIONS-DTCVASC"></a>

`dtcvasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTCVASC)
:   將時間戳記從其文字表示法剖析到 timestamp 變數中。

    ```

    int dtcvasc(char *str, timestamp *ts);
    ```

    此函式接收要剖析的字串（`str`），以及一個指向用來存放運算結果之 timestamp 變數的指標（`ts`）。

    此函式成功時傳回 0，發生錯誤時傳回負值。

    在內部，此函式使用 [`PGTYPEStimestamp_from_asc`](ecpg-pgtypes.md#PGTYPESTIMESTAMPFROMASC) 函式。輸入範例表請參閱該處的說明。
<a id="ECPG-INFORMIX-FUNCTIONS-DTCVFMTASC"></a>

`dtcvfmtasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTCVFMTASC)
:   使用格式遮罩，將時間戳記從其文字表示法剖析到 timestamp 變數中。

    ```

    dtcvfmtasc(char *inbuf, char *fmtstr, timestamp *dtvalue)
    ```

    譯註：上方函式宣告依原文保留，原文漏了傳回型別與結尾的分號；依下文「此函式成功時傳回 0」，正確的 C 宣告應以 int 為傳回型別，並以分號結尾。

    此函式接收要剖析的字串（`inbuf`）、要使用的格式遮罩（`fmtstr`），以及一個指向用來存放運算結果之 timestamp 變數的指標（`dtvalue`）。

    此函式是以 [`PGTYPEStimestamp_defmt_asc`](ecpg-pgtypes.md#PGTYPESTIMESTAMPDEFMTASC) 函式實作的。可使用的格式指定符號清單請參閱該處的說明文件。

    此函式成功時傳回 0，發生錯誤時傳回負值。
<a id="ECPG-INFORMIX-FUNCTIONS-DTSUB"></a>

`dtsub` [#](#ECPG-INFORMIX-FUNCTIONS-DTSUB)
:   將一個時間戳記減去另一個時間戳記，並傳回 interval 型別的變數。

    ```

    int dtsub(timestamp *ts1, timestamp *ts2, interval *iv);
    ```

    此函式會將 `ts1` 所指向的 timestamp 變數減去 `ts2` 所指向的 timestamp 變數，並將結果存入 `iv` 所指向的 interval 變數。

    成功時，此函式傳回 0；發生錯誤時傳回負值。
<a id="ECPG-INFORMIX-FUNCTIONS-DTTOASC"></a>

`dttoasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTTOASC)
:   將 timestamp 變數轉換為 C 的 char\* 字串。

    ```

    int dttoasc(timestamp *ts, char *output);
    ```

    此函式接收一個指向要轉換之 timestamp 變數的指標（`ts`），以及用來存放運算結果的字串（`output`）。它會依照 SQL 標準將 `ts` 轉換為其文字表示法，也就是 `YYYY-MM-DD HH:MM:SS`。

    成功時，此函式傳回 0；發生錯誤時傳回負值。
<a id="ECPG-INFORMIX-FUNCTIONS-DTTOFMTASC"></a>

`dttofmtasc` [#](#ECPG-INFORMIX-FUNCTIONS-DTTOFMTASC)
:   使用格式遮罩，將 timestamp 變數轉換為 C 的 char\*。

    ```

    int dttofmtasc(timestamp *ts, char *output, int str_len, char *fmtstr);
    ```

    此函式的第一個引數是指向要轉換之時間戳記的指標（`ts`），其餘依序為指向輸出緩衝區的指標（`output`）、為輸出緩衝區配置的最大長度（`str_len`），以及轉換時使用的格式遮罩（`fmtstr`）。

    成功時，此函式傳回 0；發生錯誤時傳回負值。

    在內部，此函式使用 [`PGTYPEStimestamp_fmt_asc`](ecpg-pgtypes.md#PGTYPESTIMESTAMPFMTASC) 函式。可使用哪些格式遮罩指定符號，請參閱該處的說明。
<a id="ECPG-INFORMIX-FUNCTIONS-INTOASC"></a>

`intoasc` [#](#ECPG-INFORMIX-FUNCTIONS-INTOASC)
:   將 interval 變數轉換為 C 的 char\* 字串。

    ```

    int intoasc(interval *i, char *str);
    ```

    此函式接收一個指向要轉換之 interval 變數的指標（`i`），以及用來存放運算結果的字串（`str`）。它會依照 SQL 標準將 `i` 轉換為其文字表示法，也就是 `YYYY-MM-DD HH:MM:SS`。

    譯註：上述 YYYY-MM-DD HH:MM:SS 是時間戳記的格式，這段說明與前一項 dttoasc 的說明逐字相同，似為沿用；interval（時間間隔）值的文字表示法並非這種日期時間格式，實際輸出格式請參閱 PGTYPESinterval_to_asc 的說明。說明文字依原文翻譯。

    成功時，此函式傳回 0；發生錯誤時傳回負值。
<a id="ECPG-INFORMIX-FUNCTIONS-RFMTLONG"></a>

`rfmtlong` [#](#ECPG-INFORMIX-FUNCTIONS-RFMTLONG)
:   使用格式遮罩，將長整數值轉換為其文字表示法。

    ```

    int rfmtlong(long lng_val, char *fmt, char *outbuf);
    ```

    此函式接收 long 值 `lng_val`、格式遮罩 `fmt`，以及指向輸出緩衝區的指標 `outbuf`。它會依照格式遮罩，將該 long 值轉換為其文字表示法。

    格式遮罩可以由下列格式指定字元組成：

    * `*`（星號）- 若此位置原本會是空白，就以星號填入。
    * `&`（& 符號）- 若此位置原本會是空白，就以零填入。
    * `#` - 將前導零轉換為空白。
    * `<` - 讓數字在字串中靠左對齊。
    * `,`（逗號）- 將四位數以上的數字每三位分成一組，並以逗號分隔。
    * `.`（句點）- 此字元將數字的整數部分與小數部分分開。
    * `-`（減號）- 若數字為負值，就會出現減號。
    * `+`（加號）- 若數字為正值，就會出現加號。
    * `(` - 取代負數前面的減號。減號將不會出現。
    * `)` - 此字元取代減號，並印在負值的後面。
    * `$` - 貨幣符號。
<a id="ECPG-INFORMIX-FUNCTIONS-RUPSHIFT"></a>

`rupshift` [#](#ECPG-INFORMIX-FUNCTIONS-RUPSHIFT)
:   將字串轉換為大寫。

    ```

    void rupshift(char *str);
    ```

    此函式接收一個指向字串的指標，並將每個小寫字元轉換為大寫。
<a id="ECPG-INFORMIX-FUNCTIONS-BYLENG"></a>

`byleng` [#](#ECPG-INFORMIX-FUNCTIONS-BYLENG)

傳回字串中不計結尾空白的字元數。

```

    int byleng(char *str, int len);
```

此函式預期第一個引數是固定長度的字串（`str`），第二個引數是其長度（`len`）。它會傳回有效字元的數量，也就是不含結尾空白的字串長度。

<a id="ECPG-INFORMIX-FUNCTIONS-LDCHAR"></a>

`ldchar` [#](#ECPG-INFORMIX-FUNCTIONS-LDCHAR)

將固定長度的字串複製到以 null 結尾的字串中。

```

    void ldchar(char *src, int len, char *dest);
```

此函式接收要複製的固定長度字串（`src`）、其長度（`len`），以及指向目的記憶體的指標（`dest`）。請注意，你需要為 `dest` 所指向的字串保留至少 `len+1` 個位元組。此函式最多會複製 `len` 個位元組到新位置（若來源字串有結尾空白，則會較少），並加上 null 結尾字元。

<a id="ECPG-INFORMIX-FUNCTIONS-RGETMSG"></a>

`rgetmsg` [#](#ECPG-INFORMIX-FUNCTIONS-RGETMSG)

```

    int rgetmsg(int msgnum, char *s, int maxsize);
```

此函式雖然存在，但目前尚未實作！

<a id="ECPG-INFORMIX-FUNCTIONS-RTYPALIGN"></a>

`rtypalign` [#](#ECPG-INFORMIX-FUNCTIONS-RTYPALIGN)

```

    int rtypalign(int offset, int type);
```

此函式雖然存在，但目前尚未實作！

<a id="ECPG-INFORMIX-FUNCTIONS-RTYPMSIZE"></a>

`rtypmsize` [#](#ECPG-INFORMIX-FUNCTIONS-RTYPMSIZE)

```

    int rtypmsize(int type, int len);
```

此函式雖然存在，但目前尚未實作！

<a id="ECPG-INFORMIX-FUNCTIONS-RTYPWIDTH"></a>

`rtypwidth` [#](#ECPG-INFORMIX-FUNCTIONS-RTYPWIDTH)

```

    int rtypwidth(int sqltype, int sqllen);
```

此函式雖然存在，但目前尚未實作！

<a id="RSETNULL"></a>

`rsetnull` [#](#RSETNULL)
:   將變數設為 NULL。

    ```

    int rsetnull(int t, char *ptr);
    ```

    此函式接收一個表示變數型別的整數，以及一個指向該變數本身、並已轉型為 C char\* 指標的指標。

    有下列型別：

    * `CCHARTYPE` - 用於 `char` 或 `char*` 型別的變數
    * `CSHORTTYPE` - 用於 `short int` 型別的變數
    * `CINTTYPE` - 用於 `int` 型別的變數
    * `CBOOLTYPE` - 用於 `boolean` 型別的變數
    * `CFLOATTYPE` - 用於 `float` 型別的變數
    * `CLONGTYPE` - 用於 `long` 型別的變數
    * `CDOUBLETYPE` - 用於 `double` 型別的變數
    * `CDECIMALTYPE` - 用於 `decimal` 型別的變數
    * `CDATETYPE` - 用於 `date` 型別的變數
    * `CDTIMETYPE` - 用於 `timestamp` 型別的變數

    以下是呼叫此函式的範例：

    ```

    $char c[] = "abc       ";
    $short s = 17;
    $int i = -74874;

    rsetnull(CCHARTYPE, (char *) c);
    rsetnull(CSHORTTYPE, (char *) &s);
    rsetnull(CINTTYPE, (char *) &i);
    ```
<a id="ECPG-INFORMIX-FUNCTIONS-RISNULL"></a>

`risnull` [#](#ECPG-INFORMIX-FUNCTIONS-RISNULL)
:   測試變數是否為 NULL。

    ```

    int risnull(int t, char *ptr);
    ```

    此函式接收要測試之變數的型別（`t`），以及指向該變數的指標（`ptr`）。請注意，後者需要轉型為 char\*。可能的變數型別清單，請參閱函式 [`rsetnull`](ecpg-informix-compat.md#RSETNULL)。

    以下是使用此函式的範例：

    ```

    $char c[] = "abc       ";
    $short s = 17;
    $int i = -74874;

    risnull(CCHARTYPE, (char *) c);
    risnull(CSHORTTYPE, (char *) &s);
    risnull(CINTTYPE, (char *) &i);
    ```

<a id="ECPG-INFORMIX-CONSTANTS"></a>

### 34.15.5. 額外的常數 [#](#ECPG-INFORMIX-CONSTANTS)

請注意，這裡的所有常數都用來描述錯誤，而且全都定義為代表負值。在各個常數的說明中，你也可以找到該常數在目前實作中所代表的值。不過，你不應該依賴這個數字。但你可以依賴這些常數全都定義為代表負值這一點。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-OVERFLOW"></a>

`ECPG_INFORMIX_NUM_OVERFLOW` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-OVERFLOW)
:   若計算中發生溢位，函式會傳回此值。其內部定義為 -1200（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-UNDERFLOW"></a>

`ECPG_INFORMIX_NUM_UNDERFLOW` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-UNDERFLOW)
:   若計算中發生下溢，函式會傳回此值。其內部定義為 -1201（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DIVIDE-ZERO"></a>

`ECPG_INFORMIX_DIVIDE_ZERO` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DIVIDE-ZERO)
:   若偵測到除以零的嘗試，函式會傳回此值。其內部定義為 -1202（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-YEAR"></a>

`ECPG_INFORMIX_BAD_YEAR` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-YEAR)
:   若剖析日期時發現不正確的年份值，函式會傳回此值。其內部定義為 -1204（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-MONTH"></a>

`ECPG_INFORMIX_BAD_MONTH` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-MONTH)
:   若剖析日期時發現不正確的月份值，函式會傳回此值。其內部定義為 -1205（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DAY"></a>

`ECPG_INFORMIX_BAD_DAY` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DAY)
:   若剖析日期時發現不正確的日值，函式會傳回此值。其內部定義為 -1206（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOSHORTDATE"></a>

`ECPG_INFORMIX_ENOSHORTDATE` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOSHORTDATE)
:   若剖析常式需要簡短的日期表示法，但取得的日期字串長度不正確，函式會傳回此值。其內部定義為 -1209（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DATE-CONVERT"></a>

`ECPG_INFORMIX_DATE_CONVERT` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DATE-CONVERT)
:   若格式化日期時發生錯誤，函式會傳回此值。其內部定義為 -1210（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-OUT-OF-MEMORY"></a>

`ECPG_INFORMIX_OUT_OF_MEMORY` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-OUT-OF-MEMORY)
:   若函式在運作期間記憶體耗盡，會傳回此值。其內部定義為 -1211（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOTDMY"></a>

`ECPG_INFORMIX_ENOTDMY` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOTDMY)
:   若剖析常式應取得格式遮罩（例如 `mmddyy`），但並非所有欄位都正確列出，函式會傳回此值。其內部定義為 -1212（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-NUMERIC"></a>

`ECPG_INFORMIX_BAD_NUMERIC` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-NUMERIC)
:   若剖析常式因數值的文字表示法含有錯誤而無法剖析，或是常式因至少一個數值變數無效而無法完成涉及數值變數的計算，函式會傳回此值。其內部定義為 -1213（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-EXPONENT"></a>

`ECPG_INFORMIX_BAD_EXPONENT` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-EXPONENT)
:   若剖析常式無法剖析指數，函式會傳回此值。其內部定義為 -1216（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DATE"></a>

`ECPG_INFORMIX_BAD_DATE` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DATE)
:   若剖析常式無法剖析日期，函式會傳回此值。其內部定義為 -1218（Informix 的定義）。
<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-EXTRA-CHARS"></a>

`ECPG_INFORMIX_EXTRA_CHARS` [#](#ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-EXTRA-CHARS)
:   若傳給剖析常式的內容含有它無法剖析的多餘字元，函式會傳回此值。其內部定義為 -1264（Informix 的定義）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-informix-compat.html)（原文版本：18.6；核對日期：2026-10-22）
