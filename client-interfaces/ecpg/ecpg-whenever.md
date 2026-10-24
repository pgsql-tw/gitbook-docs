<a id="ECPG-WHENEVER"></a>

## 34.8.1. 設定回呼 [#](#ecpg-whenever) <a href="#ecpg-whenever" id="ecpg-whenever"></a>

攔截錯誤與警告的一種簡單方法，是設定一個特定動作，每當發生某個特定情況時就執行它。一般形式如下：

```

EXEC SQL WHENEVER condition action;
```

*`condition`* 可以是下列其中之一：

<a id="ECPG-WHENEVER-SQLERROR"></a>

### `SQLERROR` [#](#ecpg-whenever-sqlerror) <a href="#ecpg-whenever-sqlerror" id="ecpg-whenever-sqlerror"></a>

每當 SQL 陳述式執行期間發生錯誤時，就呼叫所指定的動作。

<a id="ECPG-WHENEVER-SQLWARNING"></a>

### `SQLWARNING` [#](#ecpg-whenever-sqlwarning) <a href="#ecpg-whenever-sqlwarning" id="ecpg-whenever-sqlwarning"></a>

每當 SQL 陳述式執行期間發生警告時，就呼叫所指定的動作。

<a id="ECPG-WHENEVER-NOT-FOUND"></a>

### `NOT FOUND` [#](#ecpg-whenever-not-found) <a href="#ecpg-whenever-not-found" id="ecpg-whenever-not-found"></a>

每當 SQL 陳述式擷取到或影響到零個資料列時，就呼叫所指定的動作。（此情況並不是錯誤，但你可能會想特別處理它。）

*`action`* 可以是下列其中之一：

<a id="ECPG-WHENEVER-CONTINUE"></a>

### `CONTINUE` [#](#ecpg-whenever-continue) <a href="#ecpg-whenever-continue" id="ecpg-whenever-continue"></a>

實際上這表示忽略該情況。這是預設值。

<a id="ECPG-WHENEVER-GOTO"></a>

### `GOTO label`<br>`GO TO label` [#](#ecpg-whenever-goto) <a href="#ecpg-whenever-goto" id="ecpg-whenever-goto"></a>

跳至指定的標籤（使用 C 的 `goto` 陳述式）。

<a id="ECPG-WHENEVER-SQLPRINT"></a>

### `SQLPRINT` [#](#ecpg-whenever-sqlprint) <a href="#ecpg-whenever-sqlprint" id="ecpg-whenever-sqlprint"></a>

將訊息輸出到標準錯誤。這對簡單的程式或在雛型開發期間很有用。訊息的細節無法設定。

<a id="ECPG-WHENEVER-STOP"></a>

### `STOP` [#](#ecpg-whenever-stop) <a href="#ecpg-whenever-stop" id="ecpg-whenever-stop"></a>

呼叫 `exit(1)`，這會終止程式。

<a id="ECPG-WHENEVER-DO-BREAK"></a>

### `DO BREAK` [#](#ecpg-whenever-do-break) <a href="#ecpg-whenever-do-break" id="ecpg-whenever-do-break"></a>

執行 C 陳述式 `break`。這應該只用在迴圈或 `switch` 陳述式中。

<a id="ECPG-WHENEVER-DO-CONTINUE"></a>

### `DO CONTINUE` [#](#ecpg-whenever-do-continue) <a href="#ecpg-whenever-do-continue" id="ecpg-whenever-do-continue"></a>

執行 C 陳述式 `continue`。這應該只用在迴圈陳述式中。執行時，控制流程會回到迴圈的開頭。

<a id="ECPG-WHENEVER-CALL"></a>

### `CALL name (args)`<br>`DO name (args)` [#](#ecpg-whenever-call) <a href="#ecpg-whenever-call" id="ecpg-whenever-call"></a>

以指定的引數呼叫指定的 C 函式。（此用法與一般 PostgreSQL 語法中 `CALL` 與 `DO` 的意義不同。）

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

[返回 34.8. 錯誤處理](ecpg-errors.md#ecpg-errors)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-errors.html)（原文版本：18.6；核對日期：2026-10-22）
