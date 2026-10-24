<a id="ECPG-INFORMIX-FUNCTIONS"></a>

## 34.15.4. 額外的函式 [#](#ecpg-informix-functions) <a href="#ecpg-informix-functions" id="ecpg-informix-functions"></a>

<a id="ECPG-INFORMIX-FUNCTIONS-DECADD"></a>

### `decadd` [#](#ecpg-informix-functions-decadd) <a href="#ecpg-informix-functions-decadd" id="ecpg-informix-functions-decadd"></a>

將兩個 decimal 型別的值相加。

```

    int decadd(decimal *arg1, decimal *arg2, decimal *sum);
```

此函式接收一個指向 decimal 型別第一個運算元的指標（`arg1`）、一個指向 decimal 型別第二個運算元的指標（`arg2`），以及一個指向將存放總和之 decimal 型別值的指標（`sum`）。成功時，此函式傳回 0。發生溢位時傳回 `ECPG_INFORMIX_NUM_OVERFLOW`，發生下溢時傳回 `ECPG_INFORMIX_NUM_UNDERFLOW`。其他失敗情況則傳回 -1，並將 `errno` 設為 pgtypeslib 中對應的 `errno` 編號。

<a id="ECPG-INFORMIX-FUNCTIONS-DECCMP"></a>

### `deccmp` [#](#ecpg-informix-functions-deccmp) <a href="#ecpg-informix-functions-deccmp" id="ecpg-informix-functions-deccmp"></a>

比較兩個 decimal 型別的變數。

```

    int deccmp(decimal *arg1, decimal *arg2);
```

此函式接收一個指向第一個 decimal 值的指標（`arg1`）與一個指向第二個 decimal 值的指標（`arg2`），並傳回一個整數值，表示哪一個值較大。

* 1：若 `arg1` 所指的值大於 `var2` 所指的值（原文此處寫作 var2；此函式並沒有名為 var2 的參數，應為 arg2）
* -1：若 `arg1` 所指的值小於 `arg2` 所指的值
* 0：若 `arg1` 所指的值與 `arg2` 所指的值相等

<a id="ECPG-INFORMIX-FUNCTIONS-DECCOPY"></a>

### `deccopy` [#](#ecpg-informix-functions-deccopy) <a href="#ecpg-informix-functions-deccopy" id="ecpg-informix-functions-deccopy"></a>

複製一個 decimal 值。

```

    void deccopy(decimal *src, decimal *target);
```

此函式的第一個引數是指向要複製之 decimal 值的指標（`src`），第二個引數是指向 decimal 型別目標結構的指標（`target`）。

<a id="ECPG-INFORMIX-FUNCTIONS-DECCVASC"></a>

### `deccvasc` [#](#ecpg-informix-functions-deccvasc) <a href="#ecpg-informix-functions-deccvasc" id="ecpg-informix-functions-deccvasc"></a>

將值從其 ASCII 表示法轉換為 decimal 型別。

```

    int deccvasc(char *cp, int len, decimal *np);
```

此函式接收一個指向字串的指標，該字串包含要轉換之數字的字串表示法（`cp`），以及其長度 `len`。`np` 是指向用來儲存運算結果之 decimal 值的指標。

有效格式的例子如：`-2`、`.794`、`+3.44`、`592.49E07` 或 `-32.84e-4`。

此函式成功時傳回 0。若發生溢位或下溢，會傳回 `ECPG_INFORMIX_NUM_OVERFLOW` 或 `ECPG_INFORMIX_NUM_UNDERFLOW`。若無法剖析 ASCII 表示法，會傳回 `ECPG_INFORMIX_BAD_NUMERIC`；若此問題是在剖析指數時發生，則傳回 `ECPG_INFORMIX_BAD_EXPONENT`。

<a id="ECPG-INFORMIX-FUNCTIONS-DECCVDBL"></a>

### `deccvdbl` [#](#ecpg-informix-functions-deccvdbl) <a href="#ecpg-informix-functions-deccvdbl" id="ecpg-informix-functions-deccvdbl"></a>

將 double 型別的值轉換為 decimal 型別的值。

```

    int deccvdbl(double dbl, decimal *np);
```

此函式的第一個引數是要轉換的 double 型別變數（`dbl`）。第二個引數（`np`）是指向用來存放運算結果之 decimal 變數的指標。

此函式成功時傳回 0，轉換失敗時傳回負值。

<a id="ECPG-INFORMIX-FUNCTIONS-DECCVINT"></a>

### `deccvint` [#](#ecpg-informix-functions-deccvint) <a href="#ecpg-informix-functions-deccvint" id="ecpg-informix-functions-deccvint"></a>

將 int 型別的值轉換為 decimal 型別的值。

```

    int deccvint(int in, decimal *np);
```

此函式的第一個引數是要轉換的 int 型別變數（`in`）。第二個引數（`np`）是指向用來存放運算結果之 decimal 變數的指標。

此函式成功時傳回 0，轉換失敗時傳回負值。

<a id="ECPG-INFORMIX-FUNCTIONS-DECCVLONG"></a>

### `deccvlong` [#](#ecpg-informix-functions-deccvlong) <a href="#ecpg-informix-functions-deccvlong" id="ecpg-informix-functions-deccvlong"></a>

將 long 型別的值轉換為 decimal 型別的值。

```

    int deccvlong(long lng, decimal *np);
```

此函式的第一個引數是要轉換的 long 型別變數（`lng`）。第二個引數（`np`）是指向用來存放運算結果之 decimal 變數的指標。

此函式成功時傳回 0，轉換失敗時傳回負值。

<a id="ECPG-INFORMIX-FUNCTIONS-DECDIV"></a>

### `decdiv` [#](#ecpg-informix-functions-decdiv) <a href="#ecpg-informix-functions-decdiv" id="ecpg-informix-functions-decdiv"></a>

將兩個 decimal 型別的變數相除。

```

    int decdiv(decimal *n1, decimal *n2, decimal *result);
```

此函式接收分別指向第一個運算元（`n1`）與第二個運算元（`n2`）之變數的指標，並計算 `n1`/`n2`。`result` 是指向用來存放運算結果之變數的指標。

成功時傳回 0，除法失敗時傳回負值。若發生溢位或下溢，此函式會分別傳回 `ECPG_INFORMIX_NUM_OVERFLOW` 或 `ECPG_INFORMIX_NUM_UNDERFLOW`。若偵測到除以零的嘗試，此函式會傳回 `ECPG_INFORMIX_DIVIDE_ZERO`。

<a id="ECPG-INFORMIX-FUNCTIONS-DECMUL"></a>

### `decmul` [#](#ecpg-informix-functions-decmul) <a href="#ecpg-informix-functions-decmul" id="ecpg-informix-functions-decmul"></a>

將兩個 decimal 值相乘。

```

    int decmul(decimal *n1, decimal *n2, decimal *result);
```

此函式接收分別指向第一個運算元（`n1`）與第二個運算元（`n2`）之變數的指標，並計算 `n1`\*`n2`。`result` 是指向用來存放運算結果之變數的指標。

成功時傳回 0，乘法失敗時傳回負值。若發生溢位或下溢，此函式會分別傳回 `ECPG_INFORMIX_NUM_OVERFLOW` 或 `ECPG_INFORMIX_NUM_UNDERFLOW`。

<a id="ECPG-INFORMIX-FUNCTIONS-DECSUB"></a>

### `decsub` [#](#ecpg-informix-functions-decsub) <a href="#ecpg-informix-functions-decsub" id="ecpg-informix-functions-decsub"></a>

將一個 decimal 值減去另一個 decimal 值。

```

    int decsub(decimal *n1, decimal *n2, decimal *result);
```

此函式接收分別指向第一個運算元（`n1`）與第二個運算元（`n2`）之變數的指標，並計算 `n1`-`n2`。`result` 是指向用來存放運算結果之變數的指標。

成功時傳回 0，減法失敗時傳回負值。若發生溢位或下溢，此函式會分別傳回 `ECPG_INFORMIX_NUM_OVERFLOW` 或 `ECPG_INFORMIX_NUM_UNDERFLOW`。

<a id="ECPG-INFORMIX-FUNCTIONS-DECTOASC"></a>

### `dectoasc` [#](#ecpg-informix-functions-dectoasc) <a href="#ecpg-informix-functions-dectoasc" id="ecpg-informix-functions-dectoasc"></a>

將 decimal 型別的變數轉換為其 ASCII 表示法，存放在 C 的 char\* 字串中。

```

    int dectoasc(decimal *np, char *cp, int len, int right)
```

此函式接收一個指向 decimal 型別變數的指標（`np`），並將其轉換為文字表示法。`cp` 是用來存放運算結果的緩衝區。參數 `right` 指定輸出中應包含小數點右側的幾位數字。結果會四捨五入到這個小數位數。將 `right` 設為 -1 表示輸出中應包含所有可用的小數位數。若由 `len` 指出的輸出緩衝區長度不足以存放包含結尾零位元組在內的文字表示法，結果中只會存放單一個 `*` 字元，並傳回 -1。

若緩衝區 `cp` 太小，此函式會傳回 -1；若記憶體耗盡，則傳回 `ECPG_INFORMIX_OUT_OF_MEMORY`。

譯註：上方函式宣告依原文保留，原文漏了結尾的分號；正確的 C 宣告應以分號結尾。

<a id="ECPG-INFORMIX-FUNCTIONS-DECTODBL"></a>

### `dectodbl` [#](#ecpg-informix-functions-dectodbl) <a href="#ecpg-informix-functions-dectodbl" id="ecpg-informix-functions-dectodbl"></a>

將 decimal 型別的變數轉換為 double。

```

    int dectodbl(decimal *np, double *dblp);
```

此函式接收一個指向要轉換之 decimal 值的指標（`np`），以及一個指向用來存放運算結果之 double 變數的指標（`dblp`）。

成功時傳回 0，轉換失敗時傳回負值。

<a id="ECPG-INFORMIX-FUNCTIONS-DECTOINT"></a>

### `dectoint` [#](#ecpg-informix-functions-dectoint) <a href="#ecpg-informix-functions-dectoint" id="ecpg-informix-functions-dectoint"></a>

將 decimal 型別的變數轉換為整數。

```

    int dectoint(decimal *np, int *ip);
```

此函式接收一個指向要轉換之 decimal 值的指標（`np`），以及一個指向用來存放運算結果之整數變數的指標（`ip`）。

成功時傳回 0，轉換失敗時傳回負值。若發生溢位，則傳回 `ECPG_INFORMIX_NUM_OVERFLOW`。

請注意，ECPG 的實作與 Informix 的實作不同。Informix 將整數限制在 -32767 到 32767 的範圍內，而 ECPG 實作中的範圍則取決於系統架構（`INT_MIN .. INT_MAX`）。

<a id="ECPG-INFORMIX-FUNCTIONS-DECTOLONG"></a>

### `dectolong` [#](#ecpg-informix-functions-dectolong) <a href="#ecpg-informix-functions-dectolong" id="ecpg-informix-functions-dectolong"></a>

將 decimal 型別的變數轉換為長整數。

```

    int dectolong(decimal *np, long *lngp);
```

此函式接收一個指向要轉換之 decimal 值的指標（`np`），以及一個指向用來存放運算結果之 long 變數的指標（`lngp`）。

成功時傳回 0，轉換失敗時傳回負值。若發生溢位，則傳回 `ECPG_INFORMIX_NUM_OVERFLOW`。

請注意，ECPG 的實作與 Informix 的實作不同。Informix 將長整數限制在 -2,147,483,647 到 2,147,483,647 的範圍內，而 ECPG 實作中的範圍則取決於系統架構（`-LONG_MAX ..
LONG_MAX`）。

<a id="ECPG-INFORMIX-FUNCTIONS-RDATESTR"></a>

### `rdatestr` [#](#ecpg-informix-functions-rdatestr) <a href="#ecpg-informix-functions-rdatestr" id="ecpg-informix-functions-rdatestr"></a>

將日期轉換為 C 的 char\* 字串。

```

    int rdatestr(date d, char *str);
```

此函式接收兩個引數，第一個是要轉換的日期（`d`），第二個是指向目標字串的指標。輸出格式一律為 `yyyy-mm-dd`，因此你需要為該字串配置至少 11 個位元組（包含結尾的零位元組）。

此函式成功時傳回 0，發生錯誤時傳回負值。

請注意，ECPG 的實作與 Informix 的實作不同。在 Informix 中，可以透過設定環境變數來影響格式。然而在 ECPG 中，你無法變更輸出格式。

<a id="ECPG-INFORMIX-FUNCTIONS-RSTRDATE"></a>

### `rstrdate` [#](#ecpg-informix-functions-rstrdate) <a href="#ecpg-informix-functions-rstrdate" id="ecpg-informix-functions-rstrdate"></a>

剖析日期的文字表示法。

```

    int rstrdate(char *str, date *d);
```

此函式接收要轉換之日期的文字表示法（`str`），以及一個指向 date 型別變數的指標（`d`）。此函式不允許你指定格式遮罩。它使用 Informix 的預設格式遮罩，也就是 `mm/dd/yyyy`。在內部，此函式是以 `rdefmtdate` 實作的。因此，`rstrdate` 並不會比較快；如果可以選擇，你應該改用 `rdefmtdate`，它讓你可以明確指定格式遮罩。

此函式的傳回值與 `rdefmtdate` 相同。

<a id="ECPG-INFORMIX-FUNCTIONS-RTODAY"></a>

### `rtoday` [#](#ecpg-informix-functions-rtoday) <a href="#ecpg-informix-functions-rtoday" id="ecpg-informix-functions-rtoday"></a>

取得目前日期。

```

    void rtoday(date *d);
```

此函式接收一個指向 date 變數的指標（`d`），並將該變數設為目前日期。

在內部，此函式使用 [`PGTYPESdate_today`](ecpg-pgtypes-date.md#pgtypesdatetoday) 函式。

<a id="ECPG-INFORMIX-FUNCTIONS-RJULMDY"></a>

### `rjulmdy` [#](#ecpg-informix-functions-rjulmdy) <a href="#ecpg-informix-functions-rjulmdy" id="ecpg-informix-functions-rjulmdy"></a>

從 date 型別的變數中取出日、月、年的值。

```

    int rjulmdy(date d, short mdy[3]);
```

此函式接收日期 `d`，以及一個指向由 3 個短整數值組成之陣列 `mdy` 的指標。變數名稱表示了先後順序：`mdy[0]` 會設為月份的數字，`mdy[1]` 會設為日的值，而 `mdy[2]` 會包含年份。

此函式目前一律傳回 0。

在內部，此函式使用 [`PGTYPESdate_julmdy`](ecpg-pgtypes-date.md#pgtypesdatejulmdy) 函式。

<a id="ECPG-INFORMIX-FUNCTIONS-RDEFMTDATE"></a>

### `rdefmtdate` [#](#ecpg-informix-functions-rdefmtdate) <a href="#ecpg-informix-functions-rdefmtdate" id="ecpg-informix-functions-rdefmtdate"></a>

使用格式遮罩，將字元字串轉換為 date 型別的值。

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

在內部，此函式是以 [`PGTYPESdate_defmt_asc`](ecpg-pgtypes-date.md#pgtypesdatedefmtasc) 函式實作的。輸入範例表請參閱該處的說明。

<a id="ECPG-INFORMIX-FUNCTIONS-RFMTDATE"></a>

### `rfmtdate` [#](#ecpg-informix-functions-rfmtdate) <a href="#ecpg-informix-functions-rfmtdate" id="ecpg-informix-functions-rfmtdate"></a>

使用格式遮罩，將 date 型別的變數轉換為其文字表示法。

```

    int rfmtdate(date d, char *fmt, char *str);
```

此函式接收要轉換的日期（`d`）、格式遮罩（`fmt`），以及將存放日期文字表示法的字串（`str`）。

成功時傳回 0，發生錯誤時傳回負值。

在內部，此函式使用 [`PGTYPESdate_fmt_asc`](ecpg-pgtypes-date.md#pgtypesdatefmtasc) 函式，範例請參閱該處的說明。

<a id="ECPG-INFORMIX-FUNCTIONS-RMDYJUL"></a>

### `rmdyjul` [#](#ecpg-informix-functions-rmdyjul) <a href="#ecpg-informix-functions-rmdyjul" id="ecpg-informix-functions-rmdyjul"></a>

從一個由 3 個短整數組成、指定日期之日、月、年的陣列，建立 date 值。

```

    int rmdyjul(short mdy[3], date *d);
```

此函式接收由 3 個短整數組成的陣列（`mdy`），以及一個指向用來存放運算結果之 date 型別變數的指標。

目前此函式一律傳回 0。

在內部，此函式是以 [`PGTYPESdate_mdyjul`](ecpg-pgtypes-date.md#pgtypesdatemdyjul) 函式實作的。

<a id="ECPG-INFORMIX-FUNCTIONS-RDAYOFWEEK"></a>

### `rdayofweek` [#](#ecpg-informix-functions-rdayofweek) <a href="#ecpg-informix-functions-rdayofweek" id="ecpg-informix-functions-rdayofweek"></a>

傳回一個數字，表示某個日期值是星期幾。

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

在內部，此函式是以 [`PGTYPESdate_dayofweek`](ecpg-pgtypes-date.md#pgtypesdatedayofweek) 函式實作的。

<a id="ECPG-INFORMIX-FUNCTIONS-DTCURRENT"></a>

### `dtcurrent` [#](#ecpg-informix-functions-dtcurrent) <a href="#ecpg-informix-functions-dtcurrent" id="ecpg-informix-functions-dtcurrent"></a>

取得目前的時間戳記。

```

    void dtcurrent(timestamp *ts);
```

此函式取得目前的時間戳記，並將它存入 `ts` 所指向的 timestamp 變數。

<a id="ECPG-INFORMIX-FUNCTIONS-DTCVASC"></a>

### `dtcvasc` [#](#ecpg-informix-functions-dtcvasc) <a href="#ecpg-informix-functions-dtcvasc" id="ecpg-informix-functions-dtcvasc"></a>

將時間戳記從其文字表示法剖析到 timestamp 變數中。

```

    int dtcvasc(char *str, timestamp *ts);
```

此函式接收要剖析的字串（`str`），以及一個指向用來存放運算結果之 timestamp 變數的指標（`ts`）。

此函式成功時傳回 0，發生錯誤時傳回負值。

在內部，此函式使用 [`PGTYPEStimestamp_from_asc`](ecpg-pgtypes-timestamp.md#pgtypestimestampfromasc) 函式。輸入範例表請參閱該處的說明。

<a id="ECPG-INFORMIX-FUNCTIONS-DTCVFMTASC"></a>

### `dtcvfmtasc` [#](#ecpg-informix-functions-dtcvfmtasc) <a href="#ecpg-informix-functions-dtcvfmtasc" id="ecpg-informix-functions-dtcvfmtasc"></a>

使用格式遮罩，將時間戳記從其文字表示法剖析到 timestamp 變數中。

```

    dtcvfmtasc(char *inbuf, char *fmtstr, timestamp *dtvalue)
```

譯註：上方函式宣告依原文保留，原文漏了傳回型別與結尾的分號；依下文「此函式成功時傳回 0」，正確的 C 宣告應以 int 為傳回型別，並以分號結尾。

此函式接收要剖析的字串（`inbuf`）、要使用的格式遮罩（`fmtstr`），以及一個指向用來存放運算結果之 timestamp 變數的指標（`dtvalue`）。

此函式是以 [`PGTYPEStimestamp_defmt_asc`](ecpg-pgtypes-timestamp.md#pgtypestimestampdefmtasc) 函式實作的。可使用的格式指定符號清單請參閱該處的說明文件。

此函式成功時傳回 0，發生錯誤時傳回負值。

<a id="ECPG-INFORMIX-FUNCTIONS-DTSUB"></a>

### `dtsub` [#](#ecpg-informix-functions-dtsub) <a href="#ecpg-informix-functions-dtsub" id="ecpg-informix-functions-dtsub"></a>

將一個時間戳記減去另一個時間戳記，並傳回 interval 型別的變數。

```

    int dtsub(timestamp *ts1, timestamp *ts2, interval *iv);
```

此函式會將 `ts1` 所指向的 timestamp 變數減去 `ts2` 所指向的 timestamp 變數，並將結果存入 `iv` 所指向的 interval 變數。

成功時，此函式傳回 0；發生錯誤時傳回負值。

<a id="ECPG-INFORMIX-FUNCTIONS-DTTOASC"></a>

### `dttoasc` [#](#ecpg-informix-functions-dttoasc) <a href="#ecpg-informix-functions-dttoasc" id="ecpg-informix-functions-dttoasc"></a>

將 timestamp 變數轉換為 C 的 char\* 字串。

```

    int dttoasc(timestamp *ts, char *output);
```

此函式接收一個指向要轉換之 timestamp 變數的指標（`ts`），以及用來存放運算結果的字串（`output`）。它會依照 SQL 標準將 `ts` 轉換為其文字表示法，也就是 `YYYY-MM-DD HH:MM:SS`。

成功時，此函式傳回 0；發生錯誤時傳回負值。

<a id="ECPG-INFORMIX-FUNCTIONS-DTTOFMTASC"></a>

### `dttofmtasc` [#](#ecpg-informix-functions-dttofmtasc) <a href="#ecpg-informix-functions-dttofmtasc" id="ecpg-informix-functions-dttofmtasc"></a>

使用格式遮罩，將 timestamp 變數轉換為 C 的 char\*。

```

    int dttofmtasc(timestamp *ts, char *output, int str_len, char *fmtstr);
```

此函式的第一個引數是指向要轉換之時間戳記的指標（`ts`），其餘依序為指向輸出緩衝區的指標（`output`）、為輸出緩衝區配置的最大長度（`str_len`），以及轉換時使用的格式遮罩（`fmtstr`）。

成功時，此函式傳回 0；發生錯誤時傳回負值。

在內部，此函式使用 [`PGTYPEStimestamp_fmt_asc`](ecpg-pgtypes-timestamp.md#pgtypestimestampfmtasc) 函式。可使用哪些格式遮罩指定符號，請參閱該處的說明。

<a id="ECPG-INFORMIX-FUNCTIONS-INTOASC"></a>

### `intoasc` [#](#ecpg-informix-functions-intoasc) <a href="#ecpg-informix-functions-intoasc" id="ecpg-informix-functions-intoasc"></a>

將 interval 變數轉換為 C 的 char\* 字串。

```

    int intoasc(interval *i, char *str);
```

此函式接收一個指向要轉換之 interval 變數的指標（`i`），以及用來存放運算結果的字串（`str`）。它會依照 SQL 標準將 `i` 轉換為其文字表示法，也就是 `YYYY-MM-DD HH:MM:SS`。

譯註：上述 YYYY-MM-DD HH:MM:SS 是時間戳記的格式，這段說明與前一項 dttoasc 的說明逐字相同，似為沿用；interval（時間間隔）值的文字表示法並非這種日期時間格式，實際輸出格式請參閱 PGTYPESinterval_to_asc 的說明。說明文字依原文翻譯。

成功時，此函式傳回 0；發生錯誤時傳回負值。

<a id="ECPG-INFORMIX-FUNCTIONS-RFMTLONG"></a>

### `rfmtlong` [#](#ecpg-informix-functions-rfmtlong) <a href="#ecpg-informix-functions-rfmtlong" id="ecpg-informix-functions-rfmtlong"></a>

使用格式遮罩，將長整數值轉換為其文字表示法。

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

### `rupshift` [#](#ecpg-informix-functions-rupshift) <a href="#ecpg-informix-functions-rupshift" id="ecpg-informix-functions-rupshift"></a>

將字串轉換為大寫。

```

    void rupshift(char *str);
```

此函式接收一個指向字串的指標，並將每個小寫字元轉換為大寫。

<a id="ECPG-INFORMIX-FUNCTIONS-BYLENG"></a>

### `byleng` [#](#ecpg-informix-functions-byleng) <a href="#ecpg-informix-functions-byleng" id="ecpg-informix-functions-byleng"></a>

傳回字串中不計結尾空白的字元數。

```

    int byleng(char *str, int len);
```

此函式預期第一個引數是固定長度的字串（`str`），第二個引數是其長度（`len`）。它會傳回有效字元的數量，也就是不含結尾空白的字串長度。

<a id="ECPG-INFORMIX-FUNCTIONS-LDCHAR"></a>

### `ldchar` [#](#ecpg-informix-functions-ldchar) <a href="#ecpg-informix-functions-ldchar" id="ecpg-informix-functions-ldchar"></a>

將固定長度的字串複製到以 null 結尾的字串中。

```

    void ldchar(char *src, int len, char *dest);
```

此函式接收要複製的固定長度字串（`src`）、其長度（`len`），以及指向目的記憶體的指標（`dest`）。請注意，你需要為 `dest` 所指向的字串保留至少 `len+1` 個位元組。此函式最多會複製 `len` 個位元組到新位置（若來源字串有結尾空白，則會較少），並加上 null 結尾字元。

<a id="ECPG-INFORMIX-FUNCTIONS-RGETMSG"></a>

### `rgetmsg` [#](#ecpg-informix-functions-rgetmsg) <a href="#ecpg-informix-functions-rgetmsg" id="ecpg-informix-functions-rgetmsg"></a>

```

    int rgetmsg(int msgnum, char *s, int maxsize);
```

此函式雖然存在，但目前尚未實作！

<a id="ECPG-INFORMIX-FUNCTIONS-RTYPALIGN"></a>

### `rtypalign` [#](#ecpg-informix-functions-rtypalign) <a href="#ecpg-informix-functions-rtypalign" id="ecpg-informix-functions-rtypalign"></a>

```

    int rtypalign(int offset, int type);
```

此函式雖然存在，但目前尚未實作！

<a id="ECPG-INFORMIX-FUNCTIONS-RTYPMSIZE"></a>

### `rtypmsize` [#](#ecpg-informix-functions-rtypmsize) <a href="#ecpg-informix-functions-rtypmsize" id="ecpg-informix-functions-rtypmsize"></a>

```

    int rtypmsize(int type, int len);
```

此函式雖然存在，但目前尚未實作！

<a id="ECPG-INFORMIX-FUNCTIONS-RTYPWIDTH"></a>

### `rtypwidth` [#](#ecpg-informix-functions-rtypwidth) <a href="#ecpg-informix-functions-rtypwidth" id="ecpg-informix-functions-rtypwidth"></a>

```

    int rtypwidth(int sqltype, int sqllen);
```

此函式雖然存在，但目前尚未實作！

<a id="RSETNULL"></a>

### `rsetnull` [#](#rsetnull) <a href="#rsetnull" id="rsetnull"></a>

將變數設為 NULL。

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

### `risnull` [#](#ecpg-informix-functions-risnull) <a href="#ecpg-informix-functions-risnull" id="ecpg-informix-functions-risnull"></a>

測試變數是否為 NULL。

```

    int risnull(int t, char *ptr);
```

此函式接收要測試之變數的型別（`t`），以及指向該變數的指標（`ptr`）。請注意，後者需要轉型為 char\*。可能的變數型別清單，請參閱函式 [`rsetnull`](ecpg-informix-functions.md#rsetnull)。

以下是使用此函式的範例：

```

    $char c[] = "abc       ";
    $short s = 17;
    $int i = -74874;

    risnull(CCHARTYPE, (char *) c);
    risnull(CSHORTTYPE, (char *) &s);
    risnull(CINTTYPE, (char *) &i);
```

[返回 34.15. Informix 相容模式](ecpg-informix-compat.md#ecpg-informix-compat)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-informix-compat.html)（原文版本：18.6；核對日期：2026-10-22）
