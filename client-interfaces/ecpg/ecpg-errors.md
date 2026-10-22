<a id="ECPG-ERRORS"></a>

## 34.8. 錯誤處理 [#](#ECPG-ERRORS)

[34.8.1. 設定回呼](ecpg-errors.md#ECPG-WHENEVER)

[34.8.2. sqlca](ecpg-errors.md#ECPG-SQLCA)

[34.8.3. `SQLSTATE` 與 `SQLCODE` 的比較](ecpg-errors.md#ECPG-SQLSTATE-SQLCODE)

本節說明如何在嵌入式 SQL 程式中處理例外情況與警告。為此有兩種機制，兩者並不互斥，可以同時使用。

* 可以使用 `WHENEVER` 命令設定回呼，以處理警告與錯誤情況。
* 可以從 `sqlca` 變數取得關於錯誤或警告的詳細資訊。

<a id="ECPG-WHENEVER"></a>

### 34.8.1. 設定回呼 [#](#ECPG-WHENEVER)

攔截錯誤與警告的一種簡單方法，是設定一個特定動作，每當發生某個特定情況時就執行它。一般形式如下：

```

EXEC SQL WHENEVER condition action;
```

*`condition`* 可以是下列其中之一：

<a id="ECPG-WHENEVER-SQLERROR"></a>

`SQLERROR` [#](#ECPG-WHENEVER-SQLERROR)
:   每當 SQL 陳述式執行期間發生錯誤時，就呼叫所指定的動作。
<a id="ECPG-WHENEVER-SQLWARNING"></a>

`SQLWARNING` [#](#ECPG-WHENEVER-SQLWARNING)
:   每當 SQL 陳述式執行期間發生警告時，就呼叫所指定的動作。
<a id="ECPG-WHENEVER-NOT-FOUND"></a>

`NOT FOUND` [#](#ECPG-WHENEVER-NOT-FOUND)
:   每當 SQL 陳述式擷取到或影響到零個資料列時，就呼叫所指定的動作。（此情況並不是錯誤，但你可能會想特別處理它。）

*`action`* 可以是下列其中之一：

<a id="ECPG-WHENEVER-CONTINUE"></a>

`CONTINUE` [#](#ECPG-WHENEVER-CONTINUE)
:   實際上這表示忽略該情況。這是預設值。
<a id="ECPG-WHENEVER-GOTO"></a>

`GOTO label`<br>`GO TO label` [#](#ECPG-WHENEVER-GOTO)
:   跳至指定的標籤（使用 C 的 `goto` 陳述式）。
<a id="ECPG-WHENEVER-SQLPRINT"></a>

`SQLPRINT` [#](#ECPG-WHENEVER-SQLPRINT)
:   將訊息輸出到標準錯誤。這對簡單的程式或在雛型開發期間很有用。訊息的細節無法設定。
<a id="ECPG-WHENEVER-STOP"></a>

`STOP` [#](#ECPG-WHENEVER-STOP)
:   呼叫 `exit(1)`，這會終止程式。
<a id="ECPG-WHENEVER-DO-BREAK"></a>

`DO BREAK` [#](#ECPG-WHENEVER-DO-BREAK)
:   執行 C 陳述式 `break`。這應該只用在迴圈或 `switch` 陳述式中。
<a id="ECPG-WHENEVER-DO-CONTINUE"></a>

`DO CONTINUE` [#](#ECPG-WHENEVER-DO-CONTINUE)
:   執行 C 陳述式 `continue`。這應該只用在迴圈陳述式中。執行時，控制流程會回到迴圈的開頭。
<a id="ECPG-WHENEVER-CALL"></a>

`CALL name (args)`<br>`DO name (args)` [#](#ECPG-WHENEVER-CALL)
:   以指定的引數呼叫指定的 C 函式。（此用法與一般 PostgreSQL 語法中 `CALL` 與 `DO` 的意義不同。）

SQL 標準只規定了 `CONTINUE` 與 `GOTO`（以及 `GO TO`）這兩種動作。

以下是一個你可能會想在簡單程式中使用的範例。它會在發生警告時輸出一則簡單的訊息，並在發生錯誤時中止程式：

```

EXEC SQL WHENEVER SQLWARNING SQLPRINT;
EXEC SQL WHENEVER SQLERROR STOP;
```

`EXEC SQL WHENEVER` 陳述式是 SQL 前置處理器的指令，而不是 C 陳述式。它所設定的錯誤或警告動作，會套用到設定該處理方式之處以下出現的所有嵌入式 SQL 陳述式，除非在第一個 `EXEC SQL WHENEVER` 與引發該情況的 SQL 陳述式之間，又為同一情況設定了不同的動作；這與 C 程式的控制流程無關。因此，下列兩段 C 程式摘錄都無法達到預期的效果：

```

/*
 * WRONG
 */
int main(int argc, char *argv[])
{
    ...
    if (verbose) {
        EXEC SQL WHENEVER SQLWARNING SQLPRINT;
    }
    ...
    EXEC SQL SELECT ...;
    ...
}
```

```

/*
 * WRONG
 */
int main(int argc, char *argv[])
{
    ...
    set_error_handler();
    ...
    EXEC SQL SELECT ...;
    ...
}

static void set_error_handler(void)
{
    EXEC SQL WHENEVER SQLERROR STOP;
}
```

譯註：上方第二段摘錄在 set_error_handler 的定義（宣告為 static）出現之前就呼叫了它，且事先沒有任何原型宣告；這在 C 中無法正確編譯，實際撰寫時需先在呼叫處之前加上 static void set_error_handler(void); 原型宣告。範例程式碼依原文保留；此問題與本例要說明的 WHENEVER 作用範圍無關。

<a id="ECPG-SQLCA"></a>

### 34.8.2. sqlca [#](#ECPG-SQLCA)

為了提供更強大的錯誤處理，嵌入式 SQL 介面提供了一個名為 `sqlca`（SQL 通訊區，SQL communication area）的全域變數，其結構如下：

```

struct
{
    char sqlcaid[8];
    long sqlabc;
    long sqlcode;
    struct
    {
        int sqlerrml;
        char sqlerrmc[SQLERRMC_LEN];
    } sqlerrm;
    char sqlerrp[8];
    long sqlerrd[6];
    char sqlwarn[8];
    char sqlstate[5];
} sqlca;
```

（在多執行緒程式中，每個執行緒都會自動取得自己的 `sqlca` 副本。這與標準 C 全域變數 `errno` 的處理方式類似。）

`sqlca` 同時涵蓋警告與錯誤。若在執行一個陳述式期間發生多個警告或錯誤，`sqlca` 只會包含最後一個的資訊。

若上一個 SQL 陳述式沒有發生錯誤，`sqlca.sqlcode` 會是 0，而 `sqlca.sqlstate` 會是 `"00000"`。若發生了警告或錯誤，`sqlca.sqlcode` 會是負值，而 `sqlca.sqlstate` 會不同於 `"00000"`。`sqlca.sqlcode` 為正值表示無害的情況，例如上一個查詢傳回零個資料列。`sqlcode` 與 `sqlstate` 是兩種不同的錯誤碼體系；詳情見下文。

若上一個 SQL 陳述式執行成功，則 `sqlca.sqlerrd[1]` 會包含所處理資料列的 OID（若適用），而 `sqlca.sqlerrd[2]` 會包含所處理或傳回的資料列數（若該命令適用）。

發生錯誤或警告時，`sqlca.sqlerrm.sqlerrmc` 會包含描述該錯誤的字串。欄位 `sqlca.sqlerrm.sqlerrml` 包含儲存在 `sqlca.sqlerrm.sqlerrmc` 中之錯誤訊息的長度（即 `strlen()` 的結果，對 C 程式設計師來說其實沒什麼用處）。請注意，有些訊息太長，無法放進固定大小的 `sqlerrmc` 陣列；這些訊息會被截斷。

發生警告時，`sqlca.sqlwarn[2]` 會設為 `W`。（在其他所有情況下，它會設為不同於 `W` 的值。）若 `sqlca.sqlwarn[1]` 設為 `W`，表示有某個值在存入主機變數時被截斷。若其他任何元素被設定為表示警告，`sqlca.sqlwarn[0]` 就會設為 `W`。

欄位 `sqlcaid`、`sqlabc`、`sqlerrp`，以及 `sqlerrd` 與 `sqlwarn` 的其餘元素，目前都不包含有用的資訊。

`sqlca` 結構並未定義在 SQL 標準中，但有其他幾個 SQL 資料庫系統實作了它。各家定義的核心部分相似，但如果你想撰寫可攜的應用程式，應該仔細研究各種不同的實作。

以下範例結合使用 `WHENEVER` 與 `sqlca`，在發生錯誤時輸出 `sqlca` 的內容。在安裝更「使用者友善」的錯誤處理程序之前，這或許有助於應用程式的除錯或雛型開發。

```

EXEC SQL WHENEVER SQLERROR CALL print_sqlca();

void
print_sqlca()
{
    fprintf(stderr, "==== sqlca ====\n");
    fprintf(stderr, "sqlcode: %ld\n", sqlca.sqlcode);
    fprintf(stderr, "sqlerrm.sqlerrml: %d\n", sqlca.sqlerrm.sqlerrml);
    fprintf(stderr, "sqlerrm.sqlerrmc: %s\n", sqlca.sqlerrm.sqlerrmc);
    fprintf(stderr, "sqlerrd: %ld %ld %ld %ld %ld %ld\n", sqlca.sqlerrd[0],sqlca.sqlerrd[1],sqlca.sqlerrd[2],
                                                          sqlca.sqlerrd[3],sqlca.sqlerrd[4],sqlca.sqlerrd[5]);
    fprintf(stderr, "sqlwarn: %d %d %d %d %d %d %d %d\n", sqlca.sqlwarn[0], sqlca.sqlwarn[1], sqlca.sqlwarn[2],
                                                          sqlca.sqlwarn[3], sqlca.sqlwarn[4], sqlca.sqlwarn[5],
                                                          sqlca.sqlwarn[6], sqlca.sqlwarn[7]);
    fprintf(stderr, "sqlstate: %5s\n", sqlca.sqlstate);
    fprintf(stderr, "===============\n");
}
```

譯註：上方範例以 %5s 輸出 sqlca.sqlstate，但 sqlstate 是長度為 5 的字元陣列，不保證以零位元組結尾，而 %5s 中的 5 只是最小欄寬，並不限制讀取長度，可能會讀到陣列範圍之外；應寫作 %.5s 才能只輸出這 5 個字元。範例程式碼依原文保留。

輸出結果可能如下所示（此處是因資料表名稱拼錯而產生的錯誤）：

```

==== sqlca ====
sqlcode: -400
sqlerrm.sqlerrml: 49
sqlerrm.sqlerrmc: relation "pg_databasep" does not exist on line 38
sqlerrd: 0 0 0 0 0 0
sqlwarn: 0 0 0 0 0 0 0 0
sqlstate: 42P01
===============
```

<a id="ECPG-SQLSTATE-SQLCODE"></a>

### 34.8.3. `SQLSTATE` 與 `SQLCODE` 的比較 [#](#ECPG-SQLSTATE-SQLCODE)

欄位 `sqlca.sqlstate` 與 `sqlca.sqlcode` 是提供錯誤碼的兩種不同體系。兩者都源自 SQL 標準，但 `SQLCODE` 在 SQL-92 版標準中已被標示為已棄用，並在之後的版本中被移除。因此，強烈建議新的應用程式使用 `SQLSTATE`。

`SQLSTATE` 是由五個字元組成的陣列。這五個字元包含數字或大寫字母，代表各種錯誤與警告情況的代碼。`SQLSTATE` 採用階層式體系：前兩個字元表示該情況的大類，後三個字元表示該大類下的子類。成功狀態以代碼 `00000` 表示。`SQLSTATE` 代碼大部分定義於 SQL 標準中。PostgreSQL 伺服器原生支援 `SQLSTATE` 錯誤碼；因此，在所有應用程式中一致使用這套錯誤碼體系，可以達到高度的一致性。進一步的資訊請參閱[附錄 A](../../appendixes/errcodes-appendix/README.md)。

`SQLCODE` 是已棄用的錯誤碼體系，它是一個簡單的整數。值為 0 表示成功，正值表示成功但附帶額外資訊，負值表示錯誤。SQL 標準只定義了正值 +100，表示上一個命令傳回或影響了零個資料列，並未定義任何特定的負值。因此，這套體系的可攜性很差，也沒有階層式的代碼分配。歷來，PostgreSQL 的嵌入式 SQL 處理器為自身用途指定了一些特定的 `SQLCODE` 值，以下連同其數值與符號名稱一併列出。請記得，這些值無法移植到其他 SQL 實作。為了簡化將應用程式移植到 `SQLSTATE` 體系的工作，也一併列出了對應的 `SQLSTATE`。不過，這兩套體系之間並不是一對一或一對多的對應關係（實際上是多對多），因此每種情況都應該查閱[附錄 A](../../appendixes/errcodes-appendix/README.md) 中完整的 `SQLSTATE` 清單。

以下是已指定的 `SQLCODE` 值：

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NO-ERROR"></a>

0 (`ECPG_NO_ERROR`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NO-ERROR)
:   表示沒有錯誤。（SQLSTATE 00000）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NOT-FOUND"></a>

100 (`ECPG_NOT_FOUND`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NOT-FOUND)
:   這是無害的情況，表示上一個命令擷取或處理了零個資料列，或是你已到達游標的結尾。（SQLSTATE 02000）

    在迴圈中處理游標時，可以用這個代碼來偵測何時該中止迴圈，例如：

    ```

    while (1)
    {
        EXEC SQL FETCH ... ;
        if (sqlca.sqlcode == ECPG_NOT_FOUND)
            break;
    }
    ```

    不過 `WHENEVER NOT FOUND DO BREAK` 在內部實際上就是這麼做，因此明確寫出這段程式碼通常沒有什麼好處。
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-OUT-OF-MEMORY"></a>

-12 (`ECPG_OUT_OF_MEMORY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-OUT-OF-MEMORY)
:   表示虛擬記憶體已耗盡。其數值定義為 `-ENOMEM`。（SQLSTATE YE001）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-UNSUPPORTED"></a>

-200 (`ECPG_UNSUPPORTED`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-UNSUPPORTED)
:   表示前置處理器產生了函式庫無法識別的內容。可能是你使用的前置處理器與函式庫版本不相容。（SQLSTATE YE002）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TOO-MANY-ARGUMENTS"></a>

-201 (`ECPG_TOO_MANY_ARGUMENTS`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TOO-MANY-ARGUMENTS)
:   這表示命令指定的主機變數多於該命令預期的數量。（SQLSTATE 07001 或 07002）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TOO-FEW-ARGUMENTS"></a>

-202 (`ECPG_TOO_FEW_ARGUMENTS`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TOO-FEW-ARGUMENTS)
:   這表示命令指定的主機變數少於該命令預期的數量。（SQLSTATE 07001 或 07002）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TOO-MANY-MATCHES"></a>

-203 (`ECPG_TOO_MANY_MATCHES`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TOO-MANY-MATCHES)
:   這表示查詢傳回了多個資料列，但該陳述式只準備好儲存一個結果資料列（例如，因為所指定的變數不是陣列）。（SQLSTATE 21000）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INT-FORMAT"></a>

-204 (`ECPG_INT_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INT-FORMAT)
:   主機變數的型別為 `int`，而資料庫中的資料是不同的型別，且其值無法解讀為 `int`。函式庫使用 `strtol()` 進行此轉換。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-UINT-FORMAT"></a>

-205 (`ECPG_UINT_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-UINT-FORMAT)
:   主機變數的型別為 `unsigned int`，而資料庫中的資料是不同的型別，且其值無法解讀為 `unsigned
    int`。函式庫使用 `strtoul()` 進行此轉換。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-FLOAT-FORMAT"></a>

-206 (`ECPG_FLOAT_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-FLOAT-FORMAT)
:   主機變數的型別為 `float`，而資料庫中的資料是其他型別，且其值無法解讀為 `float`。函式庫使用 `strtod()` 進行此轉換。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NUMERIC-FORMAT"></a>

-207 (`ECPG_NUMERIC_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NUMERIC-FORMAT)
:   主機變數的型別為 `numeric`，而資料庫中的資料是其他型別，且其值無法解讀為 `numeric` 值。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INTERVAL-FORMAT"></a>

-208 (`ECPG_INTERVAL_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INTERVAL-FORMAT)
:   主機變數的型別為 `interval`，而資料庫中的資料是其他型別，且其值無法解讀為 `interval` 值。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-DATE-FORMAT"></a>

-209 (`ECPG_DATE_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-DATE-FORMAT)
:   主機變數的型別為 `date`，而資料庫中的資料是其他型別，且其值無法解讀為 `date` 值。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TIMESTAMP-FORMAT"></a>

-210 (`ECPG_TIMESTAMP_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TIMESTAMP-FORMAT)
:   主機變數的型別為 `timestamp`，而資料庫中的資料是其他型別，且其值無法解讀為 `timestamp` 值。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-CONVERT-BOOL"></a>

-211 (`ECPG_CONVERT_BOOL`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-CONVERT-BOOL)
:   這表示主機變數的型別為 `bool`，而資料庫中的資料既不是 `'t'`，也不是 `'f'`。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-EMPTY"></a>

-212 (`ECPG_EMPTY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-EMPTY)
:   送往 PostgreSQL 伺服器的陳述式是空的。（這在嵌入式 SQL 程式中通常不會發生，因此可能表示發生了內部錯誤。）（SQLSTATE YE002）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-MISSING-INDICATOR"></a>

-213 (`ECPG_MISSING_INDICATOR`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-MISSING-INDICATOR)
:   傳回了 null 值，但未提供 null 指示變數。（SQLSTATE 22002）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NO-ARRAY"></a>

-214 (`ECPG_NO_ARRAY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NO-ARRAY)
:   在需要陣列的地方使用了一般變數。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-DATA-NOT-ARRAY"></a>

-215 (`ECPG_DATA_NOT_ARRAY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-DATA-NOT-ARRAY)
:   資料庫在需要陣列值的地方傳回了一般變數。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-ARRAY-INSERT"></a>

-216 (`ECPG_ARRAY_INSERT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-ARRAY-INSERT)
:   無法將該值插入陣列中。（SQLSTATE 42804）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NO-CONN"></a>

-220 (`ECPG_NO_CONN`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NO-CONN)
:   程式嘗試存取不存在的連線。（SQLSTATE 08003）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NOT-CONN"></a>

-221 (`ECPG_NOT_CONN`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NOT-CONN)
:   程式嘗試存取一個確實存在但未開啟的連線。（這是內部錯誤。）（SQLSTATE YE002）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INVALID-STMT"></a>

-230 (`ECPG_INVALID_STMT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INVALID-STMT)
:   你嘗試使用的陳述式尚未預備。（SQLSTATE 26000）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INFORMIX-DUPLICATE-KEY"></a>

-239 (`ECPG_INFORMIX_DUPLICATE_KEY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INFORMIX-DUPLICATE-KEY)
:   重複鍵錯誤，違反唯一限制條件（Informix 相容模式）。（SQLSTATE 23505）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-UNKNOWN-DESCRIPTOR"></a>

-240 (`ECPG_UNKNOWN_DESCRIPTOR`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-UNKNOWN-DESCRIPTOR)
:   找不到所指定的描述區。你嘗試使用的陳述式尚未預備。（SQLSTATE 33000）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INVALID-DESCRIPTOR-INDEX"></a>

-241 (`ECPG_INVALID_DESCRIPTOR_INDEX`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INVALID-DESCRIPTOR-INDEX)
:   所指定的描述區索引超出範圍。（SQLSTATE 07009）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-UNKNOWN-DESCRIPTOR-ITEM"></a>

-242 (`ECPG_UNKNOWN_DESCRIPTOR_ITEM`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-UNKNOWN-DESCRIPTOR-ITEM)
:   要求了無效的描述區項目。（這是內部錯誤。）（SQLSTATE YE002）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-VAR-NOT-NUMERIC"></a>

-243 (`ECPG_VAR_NOT_NUMERIC`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-VAR-NOT-NUMERIC)
:   在執行動態陳述式期間，資料庫傳回了數值，但主機變數不是數值型別。（SQLSTATE 07006）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-VAR-NOT-CHAR"></a>

-244 (`ECPG_VAR_NOT_CHAR`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-VAR-NOT-CHAR)
:   在執行動態陳述式期間，資料庫傳回了非數值的值，但主機變數是數值型別。（SQLSTATE 07006）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INFORMIX-SUBSELECT-NOT-ONE"></a>

-284 (`ECPG_INFORMIX_SUBSELECT_NOT_ONE`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INFORMIX-SUBSELECT-NOT-ONE)
:   子查詢的結果不是單一資料列（Informix 相容模式）。（SQLSTATE 21000）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-PGSQL"></a>

-400 (`ECPG_PGSQL`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-PGSQL)
:   由 PostgreSQL 伺服器所引起的某種錯誤。訊息中包含來自 PostgreSQL 伺服器的錯誤訊息。
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TRANS"></a>

-401 (`ECPG_TRANS`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TRANS)
:   PostgreSQL 伺服器表示無法開始、提交或回復該交易。（SQLSTATE 08007）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-CONNECT"></a>

-402 (`ECPG_CONNECT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-CONNECT)
:   連線到資料庫的嘗試沒有成功。（SQLSTATE 08001）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-DUPLICATE-KEY"></a>

-403 (`ECPG_DUPLICATE_KEY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-DUPLICATE-KEY)
:   重複鍵錯誤，違反唯一限制條件。（SQLSTATE 23505）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-SUBSELECT-NOT-ONE"></a>

-404 (`ECPG_SUBSELECT_NOT_ONE`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-SUBSELECT-NOT-ONE)
:   子查詢的結果不是單一資料列。（SQLSTATE 21000）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-UNKNOWN-PORTAL"></a>

-602 (`ECPG_WARNING_UNKNOWN_PORTAL`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-UNKNOWN-PORTAL)
:   指定了無效的游標名稱。（SQLSTATE 34000）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-IN-TRANSACTION"></a>

-603 (`ECPG_WARNING_IN_TRANSACTION`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-IN-TRANSACTION)
:   交易正在進行中。（SQLSTATE 25001）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-NO-TRANSACTION"></a>

-604 (`ECPG_WARNING_NO_TRANSACTION`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-NO-TRANSACTION)
:   沒有作用中（進行中）的交易。（SQLSTATE 25P01）
<a id="ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-PORTAL-EXISTS"></a>

-605 (`ECPG_WARNING_PORTAL_EXISTS`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-PORTAL-EXISTS)
:   指定了已存在的游標名稱。（SQLSTATE 42P03）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-errors.html)（原文版本：18.6；核對日期：2026-10-22）
