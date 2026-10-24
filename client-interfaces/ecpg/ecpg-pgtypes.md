<a id="ECPG-PGTYPES"></a>

## 34.6. pgtypes 函式庫 [#](#ecpg-pgtypes) <a href="#ecpg-pgtypes" id="ecpg-pgtypes"></a>

[34.6.1. 字串](ecpg-pgtypes.md#ecpg-pgtypes-cstrings)

[34.6.2. numeric 型別](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric)

[34.6.3. date 型別](ecpg-pgtypes-date.md#ecpg-pgtypes-date)

[34.6.4. timestamp 型別](ecpg-pgtypes.md#ecpg-pgtypes-timestamp)

[34.6.5. interval 型別](ecpg-pgtypes.md#ecpg-pgtypes-interval)

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

C 中的 timestamp 型別讓你的程式能夠處理 SQL 型別 timestamp 的資料。PostgreSQL 伺服器中對應的型別請參閱[第 8.5 節](../../the-sql-language/datatype/datatype-datetime.md)。

下列函式可用來處理 timestamp 型別：

<a id="PGTYPESTIMESTAMPFROMASC"></a>

`PGTYPEStimestamp_from_asc` [#](#PGTYPESTIMESTAMPFROMASC)

將 timestamp 從文字表示法剖析到 timestamp 變數中。

```

    timestamp PGTYPEStimestamp_from_asc(char *str, char **endptr);
```

此函式接收要剖析的字串（`str`），以及一個指向 C char\* 的指標（`endptr`）。
目前 ECPG 一律剖析整個字串，因此目前不支援將第一個無效字元的位址存放到 `*endptr` 中。
你可以放心地將 `endptr` 設為 NULL。

此函式成功時傳回剖析出的 timestamp。發生錯誤時，傳回 `PGTYPESInvalidTimestamp`，並將 `errno` 設為 `PGTYPES_TS_BAD_TIMESTAMP`。關於這個值的重要注意事項，請參閱 [`PGTYPESInvalidTimestamp`](ecpg-pgtypes.md#PGTYPESINVALIDTIMESTAMP)。

一般而言，輸入字串可以是允許的日期表示、一個空白字元與允許的時間表示的任意組合。請注意，ECPG 不支援時區。它可以剖析時區，但不會像 PostgreSQL 伺服器那樣據以進行任何計算。時區指定符號會被靜默捨棄。

[表 34.5](ecpg-pgtypes.md#ecpg-pgtypestimestamp-from-asc-example-table) 列出幾個輸入字串的範例。表中「結果」欄括號內的英文說明表示「已忽略時區指定符號」。

<a id="ECPG-PGTYPESTIMESTAMP-FROM-ASC-EXAMPLE-TABLE"></a>

### 表 34.5. `PGTYPEStimestamp_from_asc` 的有效輸入格式 [#](#ecpg-pgtypestimestamp-from-asc-example-table) <a href="#ecpg-pgtypestimestamp-from-asc-example-table" id="ecpg-pgtypestimestamp-from-asc-example-table"></a>

<table border="1" class="table" summary="PGTYPEStimestamp_from_asc 的有效輸入格式"><colgroup><col/><col/></colgroup><thead><tr><th>輸入</th><th>結果</th></tr></thead><tbody><tr><td><code class="literal">1999-01-08 04:05:06</code></td><td><code class="literal">1999-01-08 04:05:06</code></td></tr><tr><td><code class="literal">January 8 04:05:06 1999 PST</code></td><td><code class="literal">1999-01-08 04:05:06</code></td></tr><tr><td><code class="literal">1999-Jan-08 04:05:06.789-8</code></td><td><code class="literal">1999-01-08 04:05:06.789 (time zone specifier ignored)</code></td></tr><tr><td><code class="literal">J2451187 04:05-08:00</code></td><td><code class="literal">1999-01-08 04:05:00 (time zone specifier ignored)</code></td></tr></tbody></table>

<br>

<a id="PGTYPESTIMESTAMPTOASC"></a>

`PGTYPEStimestamp_to_asc` [#](#PGTYPESTIMESTAMPTOASC)

將 timestamp 轉換為 C char\* 字串（原文此處寫作「Converts a date」，但此函式轉換的是 timestamp）。

```

    char *PGTYPEStimestamp_to_asc(timestamp tstamp);
```

此函式接收 timestamp `tstamp` 作為唯一引數，並傳回一個已配置的字串，內含該 timestamp 的文字表示法。
結果必須以 `PGTYPESchar_free()` 釋放。

<a id="PGTYPESTIMESTAMPCURRENT"></a>

`PGTYPEStimestamp_current` [#](#PGTYPESTIMESTAMPCURRENT)

取得目前的 timestamp。

```

    void PGTYPEStimestamp_current(timestamp *ts);
```

此函式取得目前的 timestamp，並將它存入 `ts` 所指的 timestamp 變數中。

<a id="PGTYPESTIMESTAMPFMTASC"></a>

`PGTYPEStimestamp_fmt_asc` [#](#PGTYPESTIMESTAMPFMTASC)

使用格式遮罩，將 timestamp 變數轉換為 C char\*。

```

    int PGTYPEStimestamp_fmt_asc(timestamp *ts, char *output, int str_len, char *fmtstr);
```

此函式以指向要轉換之 timestamp 的指標作為第一個引數（`ts`），其後依序是指向輸出緩衝區的指標（`output`）、為輸出緩衝區配置的最大長度（`str_len`），以及轉換時使用的格式遮罩（`fmtstr`）。

成功時，此函式傳回 0；發生錯誤時傳回負值。

格式遮罩可以使用下列格式指定符號。這些格式指定符號與 libc 中 `strftime` 函式所使用的相同。任何非格式指定符號的內容都會被複製到輸出緩衝區。

* `%A` - 以當地語系的表示法取代為星期的完整名稱。
* `%a` - 以當地語系的表示法取代為星期的縮寫名稱。
* `%B` - 以當地語系的表示法取代為月份的完整名稱。
* `%b` - 以當地語系的表示法取代為月份的縮寫名稱。
* `%C` - 取代為以十進位數字表示的（年 / 100）；個位數前面補零。
* `%c` - 以當地語系的表示法取代為時間與日期。
* `%D` - 等同於
  `%m/%d/%y`。
* `%d` - 取代為以十進位數字表示的該月第幾日（01–31）。
* `%E*` `%O*` - POSIX 語系擴充。序列
  `%Ec`
  `%EC`
  `%Ex`
  `%EX`
  `%Ey`
  `%EY`
  `%Od`
  `%Oe`
  `%OH`
  `%OI`
  `%Om`
  `%OM`
  `%OS`
  `%Ou`
  `%OU`
  `%OV`
  `%Ow`
  `%OW`
  `%Oy`
  應該提供替代的表示法。

  此外，`%OB` 已實作，用來表示替代的月份名稱（單獨使用，不提及日）。
* `%e` - 取代為以十進位數字表示的該月第幾日（1–31）；個位數前面補一個空白。
* `%F` - 等同於 `%Y-%m-%d`。
* `%G` - 取代為以十進位數字表示、含世紀的年份。這個年份是包含該週大部分日子的那一年（以星期一為一週的第一天）。
* `%g` - 取代為與
  `%G` 相同的年份，但以不含世紀的十進位數字表示（00–99）。
* `%H` - 取代為以十進位數字表示的小時（24 小時制）（00–23）。
* `%h` - 與 `%b` 相同。
* `%I` - 取代為以十進位數字表示的小時（12 小時制）（01–12）。
* `%j` - 取代為以十進位數字表示的該年第幾日（001–366）。
* `%k` - 取代為以十進位數字表示的小時（24 小時制）（0–23）；個位數前面補一個空白。
* `%l` - 取代為以十進位數字表示的小時（12 小時制）（1–12）；個位數前面補一個空白。
* `%M` - 取代為以十進位數字表示的分鐘（00–59）。
* `%m` - 取代為以十進位數字表示的月份（01–12）。
* `%n` - 取代為換行字元。
* `%O*` - 與 `%E*` 相同。
* `%p` - 視情況以當地語系的表示法取代為「上午」（ante meridiem）或「下午」（post meridiem）。
* `%R` - 等同於 `%H:%M`。
* `%r` - 等同於 `%I:%M:%S
  %p`。
* `%S` - 取代為以十進位數字表示的秒數（00–60）。
* `%s` - 取代為自 Epoch（UTC）以來的秒數。
* `%T` - 等同於 `%H:%M:%S`
* `%t` - 取代為定位字元（tab）。
* `%U` - 取代為以十進位數字表示的該年第幾週（以星期日為一週的第一天）（00–53）。
* `%u` - 取代為以十進位數字表示的星期幾（以星期一為一週的第一天）（1–7）。
* `%V` - 取代為以十進位數字表示的該年第幾週（以星期一為一週的第一天）（01–53）。
  若包含 1 月 1 日的那一週在新的一年中有四天以上，則該週為第 1 週；否則它是前一年的最後一週，而下一週才是第 1 週。
* `%v` - 等同於
  `%e-%b-%Y`。
* `%W` - 取代為以十進位數字表示的該年第幾週（以星期一為一週的第一天）（00–53）。
* `%w` - 取代為以十進位數字表示的星期幾（以星期日為一週的第一天）（0–6）。
* `%X` - 以當地語系的表示法取代為時間。
* `%x` - 以當地語系的表示法取代為日期。
* `%Y` - 取代為以十進位數字表示、含世紀的年份。
* `%y` - 取代為以十進位數字表示、不含世紀的年份（00–99）。
* `%Z` - 取代為時區名稱。
* `%z` - 取代為相對於 UTC 的時區偏移；開頭的加號表示 UTC 以東，減號表示 UTC 以西，其後是各為兩位數的小時與分鐘，兩者之間沒有分隔符號（這是 [RFC 822](https://datatracker.ietf.org/doc/html/rfc822) 日期標頭的常見形式）。
* `%+` - 以當地語系的表示法取代為日期與時間。
* `%-*` - GNU libc 擴充。進行數字輸出時不做任何填補。
* $_\* - GNU libc 擴充。明確指定以空白填補。（譯註：原文此項開頭的格式指定符號顯示有誤，依前後項目與 GNU libc 的 strftime，應為 %\_\*。）
* `%0*` - GNU libc 擴充。明確指定以零填補。
* `%%` - 取代為 `%`。

<a id="PGTYPESTIMESTAMPSUB"></a>

`PGTYPEStimestamp_sub` [#](#PGTYPESTIMESTAMPSUB)

將一個 timestamp 減去另一個 timestamp，並將結果存入 interval 型別的變數。

```

    int PGTYPEStimestamp_sub(timestamp *ts1, timestamp *ts2, interval *iv);
```

此函式會將 `ts1` 所指的 timestamp 變數減去 `ts2` 所指的 timestamp 變數，並將結果存放在 `iv` 所指的 interval 變數中。

成功時，此函式傳回 0；發生錯誤時傳回負值。

<a id="PGTYPESTIMESTAMPDEFMTASC"></a>

`PGTYPEStimestamp_defmt_asc` [#](#PGTYPESTIMESTAMPDEFMTASC)

使用格式遮罩，從文字表示法剖析出 timestamp 值。

```

    int PGTYPEStimestamp_defmt_asc(char *str, char *fmt, timestamp *d);
```

此函式從變數 `str` 接收 timestamp 的文字表示法，並從變數 `fmt` 接收要使用的格式遮罩。結果會存放在 `d` 所指的變數中。

若格式遮罩 `fmt` 為 NULL，此函式會改用預設的格式遮罩，也就是 `%Y-%m-%d
%H:%M:%S`。

這是 [`PGTYPEStimestamp_fmt_asc`](ecpg-pgtypes.md#PGTYPESTIMESTAMPFMTASC) 的反向函式。可用的格式遮罩項目請參閱該處的說明。

<a id="PGTYPESTIMESTAMPADDINTERVAL"></a>

`PGTYPEStimestamp_add_interval` [#](#PGTYPESTIMESTAMPADDINTERVAL)

將 interval 變數加到 timestamp 變數上。

```

    int PGTYPEStimestamp_add_interval(timestamp *tin, interval *span, timestamp *tout);
```

此函式接收一個指向 timestamp 變數的指標 `tin`，以及一個指向 interval 變數的指標 `span`。它將 interval 加到 timestamp 上，並將所得的 timestamp 存放在 `tout` 所指的變數中。

成功時，此函式傳回 0；發生錯誤時傳回負值。

<a id="PGTYPESTIMESTAMPSUBINTERVAL"></a>

`PGTYPEStimestamp_sub_interval` [#](#PGTYPESTIMESTAMPSUBINTERVAL)

將 timestamp 變數減去 interval 變數。

```

    int PGTYPEStimestamp_sub_interval(timestamp *tin, interval *span, timestamp *tout);
```

此函式將 `tin` 所指的 timestamp 變數減去 `span` 所指的 interval 變數，並將結果存入 `tout` 所指的變數中。

成功時，此函式傳回 0；發生錯誤時傳回負值。

<a id="ECPG-PGTYPES-INTERVAL"></a>

### 34.6.5. interval 型別 [#](#ecpg-pgtypes-interval) <a href="#ecpg-pgtypes-interval" id="ecpg-pgtypes-interval"></a>

C 中的 interval 型別讓你的程式能夠處理 SQL 型別 interval 的資料。PostgreSQL 伺服器中對應的型別請參閱[第 8.5 節](../../the-sql-language/datatype/datatype-datetime.md)。

下列函式可用來處理 interval 型別：

<a id="PGTYPESINTERVALNEW"></a>

`PGTYPESinterval_new` [#](#PGTYPESINTERVALNEW)

傳回指向新配置之 interval 變數的指標。

```

    interval *PGTYPESinterval_new(void);
```

<a id="PGTYPESINTERVALFREE"></a>

`PGTYPESinterval_free` [#](#PGTYPESINTERVALFREE)

釋放先前配置之 interval 變數的記憶體。

```

    void PGTYPESinterval_free(interval *intvl);
```

<a id="PGTYPESINTERVALFROMASC"></a>

`PGTYPESinterval_from_asc` [#](#PGTYPESINTERVALFROMASC)

從文字表示法剖析出 interval。

```

    interval *PGTYPESinterval_from_asc(char *str, char **endptr);
```

此函式剖析輸入字串 `str`，並傳回指向已配置之 interval 變數的指標。
目前 ECPG 一律剖析整個字串，因此目前不支援將第一個無效字元的位址存放到 `*endptr` 中。
你可以放心地將 `endptr` 設為 NULL。

<a id="PGTYPESINTERVALTOASC"></a>

`PGTYPESinterval_to_asc` [#](#PGTYPESINTERVALTOASC)

將 interval 型別的變數轉換為它的文字表示法。

```

    char *PGTYPESinterval_to_asc(interval *span);
```

此函式將 `span` 所指的 interval 變數轉換為 C char\*。輸出看起來像這個範例：
`@ 1 day 12 hours 59 mins 10 secs`。
結果必須以 `PGTYPESchar_free()` 釋放。

<a id="PGTYPESINTERVALCOPY"></a>

`PGTYPESinterval_copy` [#](#PGTYPESINTERVALCOPY)

複製 interval 型別的變數。

```

    int PGTYPESinterval_copy(interval *intvlsrc, interval *intvldest);
```

此函式將 `intvlsrc` 所指的 interval 變數複製到 `intvldest` 所指的變數中。請注意，你必須事先為目的變數配置記憶體。

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
