<a id="ECPG-PGTYPES"></a>

## 34.6. pgtypes 函式庫 [#](#ecpg-pgtypes) <a href="#ecpg-pgtypes" id="ecpg-pgtypes"></a>

[34.6.1. 字串](ecpg-pgtypes.md#ecpg-pgtypes-cstrings)

[34.6.2. numeric 型別](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric)

[34.6.3. date 型別](ecpg-pgtypes-date.md#ecpg-pgtypes-date)

[34.6.4. timestamp 型別](ecpg-pgtypes-timestamp.md#ecpg-pgtypes-timestamp)

[34.6.5. interval 型別](ecpg-pgtypes-interval.md#ecpg-pgtypes-interval)

[34.6.6. decimal 型別](ecpg-pgtypes.md#ecpg-pgtypes-decimal)

[34.6.7. pgtypeslib 的 errno 值](ecpg-pgtypes.md#ecpg-pgtypes-errno)

[34.6.8. pgtypeslib 的特殊常數](ecpg-pgtypes.md#ecpg-pgtypes-constants)

pgtypes 函式庫將 PostgreSQL 資料庫的型別對應到可在 C 程式中使用的 C 等價型別。它也提供在 C 之中、亦即不借助 PostgreSQL 伺服器，對這些型別進行基本計算的函式。請參閱下列範例：

```

EXEC SQL BEGIN DECLARE SECTION;
   date date1;
   timestamp ts1, tsout;
   interval iv1;
   char *out;
EXEC SQL END DECLARE SECTION;

PGTYPESdate_today(&date1);
EXEC SQL SELECT started, duration INTO :ts1, :iv1 FROM datetbl WHERE d=:date1;
PGTYPEStimestamp_add_interval(&ts1, &iv1, &tsout);
out = PGTYPEStimestamp_to_asc(&tsout);
printf("Started + duration: %s\n", out);
PGTYPESchar_free(out);
```

<a id="ECPG-PGTYPES-CSTRINGS"></a>

### 34.6.1. 字串 [#](#ecpg-pgtypes-cstrings) <a href="#ecpg-pgtypes-cstrings" id="ecpg-pgtypes-cstrings"></a>

有些函式（例如 `PGTYPESnumeric_to_asc`）會傳回指向新配置字串的指標。這些結果應該以 `PGTYPESchar_free` 釋放，而不是用 `free`。（這只在 Windows 上才重要，因為在 Windows 上，記憶體的配置與釋放有時必須由同一個函式庫完成。）

<a id="ECPG-PGTYPES-NUMERIC"></a>

### 34.6.2. numeric 型別 [#](#ecpg-pgtypes-numeric) <a href="#ecpg-pgtypes-numeric" id="ecpg-pgtypes-numeric"></a>

本節內容請參閱[34.6.2. numeric 型別](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric)。

<a id="ECPG-PGTYPES-DATE"></a>

### 34.6.3. date 型別 [#](#ecpg-pgtypes-date) <a href="#ecpg-pgtypes-date" id="ecpg-pgtypes-date"></a>

本節內容請參閱[34.6.3. date 型別](ecpg-pgtypes-date.md#ecpg-pgtypes-date)。

<a id="ECPG-PGTYPESDATE-FROM-ASC-TABLE"></a>

### 表 34.2. `PGTYPESdate_from_asc` 的有效輸入格式 [#](#ecpg-pgtypesdate-from-asc-table) <a href="#ecpg-pgtypesdate-from-asc-table" id="ecpg-pgtypesdate-from-asc-table"></a>

本表請參閱[表 34.2. `PGTYPESdate_from_asc` 的有效輸入格式](ecpg-pgtypes-date.md#ecpg-pgtypesdate-from-asc-table)。

<a id="ECPG-PGTYPESDATE-FMT-ASC-EXAMPLE-TABLE"></a>

### 表 34.3. `PGTYPESdate_fmt_asc` 的有效輸入格式 [#](#ecpg-pgtypesdate-fmt-asc-example-table) <a href="#ecpg-pgtypesdate-fmt-asc-example-table" id="ecpg-pgtypesdate-fmt-asc-example-table"></a>

本表請參閱[表 34.3. `PGTYPESdate_fmt_asc` 的有效輸入格式](ecpg-pgtypes-date.md#ecpg-pgtypesdate-fmt-asc-example-table)。

<a id="ECPG-RDEFMTDATE-EXAMPLE-TABLE"></a>

### 表 34.4. `rdefmtdate` 的有效輸入格式 [#](#ecpg-rdefmtdate-example-table) <a href="#ecpg-rdefmtdate-example-table" id="ecpg-rdefmtdate-example-table"></a>

本表請參閱[表 34.4. `rdefmtdate` 的有效輸入格式](ecpg-pgtypes-date.md#ecpg-rdefmtdate-example-table)。

<a id="ECPG-PGTYPES-TIMESTAMP"></a>

### 34.6.4. timestamp 型別 [#](#ecpg-pgtypes-timestamp) <a href="#ecpg-pgtypes-timestamp" id="ecpg-pgtypes-timestamp"></a>

本節內容請參閱[34.6.4. timestamp 型別](ecpg-pgtypes-timestamp.md#ecpg-pgtypes-timestamp)。

<a id="ECPG-PGTYPESTIMESTAMP-FROM-ASC-EXAMPLE-TABLE"></a>

### 表 34.5. `PGTYPEStimestamp_from_asc` 的有效輸入格式 [#](#ecpg-pgtypestimestamp-from-asc-example-table) <a href="#ecpg-pgtypestimestamp-from-asc-example-table" id="ecpg-pgtypestimestamp-from-asc-example-table"></a>

本表請參閱[表 34.5. `PGTYPEStimestamp_from_asc` 的有效輸入格式](ecpg-pgtypes-timestamp.md#ecpg-pgtypestimestamp-from-asc-example-table)。

<a id="ECPG-PGTYPES-INTERVAL"></a>

### 34.6.5. interval 型別 [#](#ecpg-pgtypes-interval) <a href="#ecpg-pgtypes-interval" id="ecpg-pgtypes-interval"></a>

本節內容請參閱[34.6.5. interval 型別](ecpg-pgtypes-interval.md#ecpg-pgtypes-interval)。

<a id="ECPG-PGTYPES-DECIMAL"></a>

### 34.6.6. decimal 型別 [#](#ecpg-pgtypes-decimal) <a href="#ecpg-pgtypes-decimal" id="ecpg-pgtypes-decimal"></a>

decimal 型別與 numeric 型別相似，但其精確度上限為 30 位有效數字。numeric 型別只能建立在堆積上；相對地，decimal 型別既可以建立在堆疊上，也可以建立在堆積上（透過 `PGTYPESdecimal_new` 與 `PGTYPESdecimal_free` 函式）。在[第 34.15 節](ecpg-informix-compat.md)所述的 Informix 相容模式中，還有許多其他處理 decimal 型別的函式。

下列函式可用來處理 decimal 型別，而且不只包含在 `libcompat` 函式庫中。

<a id="ECPG-PGTYPES-DECIMAL-NEW"></a>

`PGTYPESdecimal_new` [#](#ECPG-PGTYPES-DECIMAL-NEW)

取得指向新配置之 decimal 變數的指標。

```

    decimal *PGTYPESdecimal_new(void);
```

<a id="ECPG-PGTYPES-DECIMAL-FREE"></a>

`PGTYPESdecimal_free` [#](#ECPG-PGTYPES-DECIMAL-FREE)

釋放 decimal 型別，釋放它所有的記憶體。

```

    void PGTYPESdecimal_free(decimal *var);
```

<a id="ECPG-PGTYPES-ERRNO"></a>

### 34.6.7. pgtypeslib 的 errno 值 [#](#ecpg-pgtypes-errno) <a href="#ecpg-pgtypes-errno" id="ecpg-pgtypes-errno"></a>

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-NUM-BAD-NUMERIC"></a>

`PGTYPES_NUM_BAD_NUMERIC` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-NUM-BAD-NUMERIC)
:   引數應該包含一個 numeric 變數（或指向一個 numeric 變數），但它在記憶體中的表示實際上無效。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-NUM-OVERFLOW"></a>

`PGTYPES_NUM_OVERFLOW` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-NUM-OVERFLOW)
:   發生溢位。由於 numeric 型別幾乎可以處理任意精確度，將 numeric 變數轉換為其他型別時可能會導致溢位。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-NUM-UNDERFLOW"></a>

`PGTYPES_NUM_UNDERFLOW` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-NUM-UNDERFLOW)
:   發生下溢。由於 numeric 型別幾乎可以處理任意精確度，將 numeric 變數轉換為其他型別時可能會導致下溢。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-NUM-DIVIDE-ZERO"></a>

`PGTYPES_NUM_DIVIDE_ZERO` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-NUM-DIVIDE-ZERO)
:   嘗試除以零。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-DATE"></a>

`PGTYPES_DATE_BAD_DATE` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-DATE)
:   傳給 `PGTYPESdate_from_asc` 函式的日期字串無效。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-EARGS"></a>

`PGTYPES_DATE_ERR_EARGS` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-EARGS)
:   傳給 `PGTYPESdate_defmt_asc` 函式的引數無效。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-ENOSHORTDATE"></a>

`PGTYPES_DATE_ERR_ENOSHORTDATE` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-ENOSHORTDATE)
:   `PGTYPESdate_defmt_asc` 函式在輸入字串中發現無效的語彙單元（token）。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-INTVL-BAD-INTERVAL"></a>

`PGTYPES_INTVL_BAD_INTERVAL` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-INTVL-BAD-INTERVAL)
:   傳給 `PGTYPESinterval_from_asc` 函式的 interval 字串無效，或傳給 `PGTYPESinterval_to_asc` 函式的 interval 值無效。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-ENOTDMY"></a>

`PGTYPES_DATE_ERR_ENOTDMY` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-ENOTDMY)
:   `PGTYPESdate_defmt_asc` 函式中的日／月／年指派不相符。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-DAY"></a>

`PGTYPES_DATE_BAD_DAY` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-DAY)
:   `PGTYPESdate_defmt_asc` 函式發現無效的「該月第幾日」值。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-MONTH"></a>

`PGTYPES_DATE_BAD_MONTH` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-MONTH)
:   `PGTYPESdate_defmt_asc` 函式發現無效的月份值。
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-TS-BAD-TIMESTAMP"></a>

`PGTYPES_TS_BAD_TIMESTAMP` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-TS-BAD-TIMESTAMP)
:   傳給 `PGTYPEStimestamp_from_asc` 函式的 timestamp 字串無效，或傳給 `PGTYPEStimestamp_to_asc` 函式的 timestamp 值無效。（原文此處寫作「pass passed」，應為「was passed」的誤植。）
<a id="ECPG-PGTYPES-ERRNO-PGTYPES-TS-ERR-EINFTIME"></a>

`PGTYPES_TS_ERR_EINFTIME` [#](#ECPG-PGTYPES-ERRNO-PGTYPES-TS-ERR-EINFTIME)
:   在無法處理無限 timestamp 值的情境中遇到了這種值。

<a id="ECPG-PGTYPES-CONSTANTS"></a>

### 34.6.8. pgtypeslib 的特殊常數 [#](#ecpg-pgtypes-constants) <a href="#ecpg-pgtypes-constants" id="ecpg-pgtypes-constants"></a>

<a id="PGTYPESINVALIDTIMESTAMP"></a>

`PGTYPESInvalidTimestamp` [#](#PGTYPESINVALIDTIMESTAMP)
:   代表無效時間戳記的 timestamp 型別值。`PGTYPEStimestamp_from_asc` 函式發生剖析錯誤時會傳回此值。
    請注意，由於 `timestamp` 資料型別的內部表示方式，`PGTYPESInvalidTimestamp` 同時也是一個有效的 timestamp。它被設為 `1899-12-31 23:59:59`。為了偵測錯誤，請確保你的應用程式在每次呼叫 `PGTYPEStimestamp_from_asc` 之後，不只檢查 `PGTYPESInvalidTimestamp`，也檢查 `errno != 0`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-pgtypes.html)（原文版本：18.6；核對日期：2026-10-18）
