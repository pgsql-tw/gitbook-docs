<a id="ECPG-PGTYPES-TIMESTAMP"></a>

## 34.6.4. timestamp 型別 [#](#ecpg-pgtypes-timestamp) <a href="#ecpg-pgtypes-timestamp" id="ecpg-pgtypes-timestamp"></a>

C 中的 timestamp 型別讓你的程式能夠處理 SQL 型別 timestamp 的資料。PostgreSQL 伺服器中對應的型別請參閱[第 8.5 節](../../the-sql-language/datatype/datatype-datetime.md)。

下列函式可用來處理 timestamp 型別：

<a id="PGTYPESTIMESTAMPFROMASC"></a>

### `PGTYPEStimestamp_from_asc` [#](#pgtypestimestampfromasc) <a href="#pgtypestimestampfromasc" id="pgtypestimestampfromasc"></a>

將 timestamp 從文字表示法剖析到 timestamp 變數中。

```

    timestamp PGTYPEStimestamp_from_asc(char *str, char **endptr);
```

此函式接收要剖析的字串（`str`），以及一個指向 C char\* 的指標（`endptr`）。
目前 ECPG 一律剖析整個字串，因此目前不支援將第一個無效字元的位址存放到 `*endptr` 中。
你可以放心地將 `endptr` 設為 NULL。

此函式成功時傳回剖析出的 timestamp。發生錯誤時，傳回 `PGTYPESInvalidTimestamp`，並將 `errno` 設為 `PGTYPES_TS_BAD_TIMESTAMP`。關於這個值的重要注意事項，請參閱 [`PGTYPESInvalidTimestamp`](ecpg-pgtypes-constants.md#pgtypesinvalidtimestamp)。

一般而言，輸入字串可以是允許的日期表示、一個空白字元與允許的時間表示的任意組合。請注意，ECPG 不支援時區。它可以剖析時區，但不會像 PostgreSQL 伺服器那樣據以進行任何計算。時區指定符號會被靜默捨棄。

[表 34.5](ecpg-pgtypes-timestamp.md#ecpg-pgtypestimestamp-from-asc-example-table) 列出幾個輸入字串的範例。表中「結果」欄括號內的英文說明表示「已忽略時區指定符號」。

<a id="ECPG-PGTYPESTIMESTAMP-FROM-ASC-EXAMPLE-TABLE"></a>

### 表 34.5. `PGTYPEStimestamp_from_asc` 的有效輸入格式 [#](#ecpg-pgtypestimestamp-from-asc-example-table) <a href="#ecpg-pgtypestimestamp-from-asc-example-table" id="ecpg-pgtypestimestamp-from-asc-example-table"></a>

<table border="1" class="table" summary="PGTYPEStimestamp_from_asc 的有效輸入格式"><colgroup><col/><col/></colgroup><thead><tr><th>輸入</th><th>結果</th></tr></thead><tbody><tr><td><code class="literal">1999-01-08 04:05:06</code></td><td><code class="literal">1999-01-08 04:05:06</code></td></tr><tr><td><code class="literal">January 8 04:05:06 1999 PST</code></td><td><code class="literal">1999-01-08 04:05:06</code></td></tr><tr><td><code class="literal">1999-Jan-08 04:05:06.789-8</code></td><td><code class="literal">1999-01-08 04:05:06.789 (time zone specifier ignored)</code></td></tr><tr><td><code class="literal">J2451187 04:05-08:00</code></td><td><code class="literal">1999-01-08 04:05:00 (time zone specifier ignored)</code></td></tr></tbody></table>

<br>

<a id="PGTYPESTIMESTAMPTOASC"></a>

### `PGTYPEStimestamp_to_asc` [#](#pgtypestimestamptoasc) <a href="#pgtypestimestamptoasc" id="pgtypestimestamptoasc"></a>

將 timestamp 轉換為 C char\* 字串（原文此處寫作「Converts a date」，但此函式轉換的是 timestamp）。

```

    char *PGTYPEStimestamp_to_asc(timestamp tstamp);
```

此函式接收 timestamp `tstamp` 作為唯一引數，並傳回一個已配置的字串，內含該 timestamp 的文字表示法。
結果必須以 `PGTYPESchar_free()` 釋放。

<a id="PGTYPESTIMESTAMPCURRENT"></a>

### `PGTYPEStimestamp_current` [#](#pgtypestimestampcurrent) <a href="#pgtypestimestampcurrent" id="pgtypestimestampcurrent"></a>

取得目前的 timestamp。

```

    void PGTYPEStimestamp_current(timestamp *ts);
```

此函式取得目前的 timestamp，並將它存入 `ts` 所指的 timestamp 變數中。

<a id="PGTYPESTIMESTAMPFMTASC"></a>

### `PGTYPEStimestamp_fmt_asc` [#](#pgtypestimestampfmtasc) <a href="#pgtypestimestampfmtasc" id="pgtypestimestampfmtasc"></a>

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

### `PGTYPEStimestamp_sub` [#](#pgtypestimestampsub) <a href="#pgtypestimestampsub" id="pgtypestimestampsub"></a>

將一個 timestamp 減去另一個 timestamp，並將結果存入 interval 型別的變數。

```

    int PGTYPEStimestamp_sub(timestamp *ts1, timestamp *ts2, interval *iv);
```

此函式會將 `ts1` 所指的 timestamp 變數減去 `ts2` 所指的 timestamp 變數，並將結果存放在 `iv` 所指的 interval 變數中。

成功時，此函式傳回 0；發生錯誤時傳回負值。

<a id="PGTYPESTIMESTAMPDEFMTASC"></a>

### `PGTYPEStimestamp_defmt_asc` [#](#pgtypestimestampdefmtasc) <a href="#pgtypestimestampdefmtasc" id="pgtypestimestampdefmtasc"></a>

使用格式遮罩，從文字表示法剖析出 timestamp 值。

```

    int PGTYPEStimestamp_defmt_asc(char *str, char *fmt, timestamp *d);
```

此函式從變數 `str` 接收 timestamp 的文字表示法，並從變數 `fmt` 接收要使用的格式遮罩。結果會存放在 `d` 所指的變數中。

若格式遮罩 `fmt` 為 NULL，此函式會改用預設的格式遮罩，也就是 `%Y-%m-%d
%H:%M:%S`。

這是 [`PGTYPEStimestamp_fmt_asc`](ecpg-pgtypes-timestamp.md#pgtypestimestampfmtasc) 的反向函式。可用的格式遮罩項目請參閱該處的說明。

<a id="PGTYPESTIMESTAMPADDINTERVAL"></a>

### `PGTYPEStimestamp_add_interval` [#](#pgtypestimestampaddinterval) <a href="#pgtypestimestampaddinterval" id="pgtypestimestampaddinterval"></a>

將 interval 變數加到 timestamp 變數上。

```

    int PGTYPEStimestamp_add_interval(timestamp *tin, interval *span, timestamp *tout);
```

此函式接收一個指向 timestamp 變數的指標 `tin`，以及一個指向 interval 變數的指標 `span`。它將 interval 加到 timestamp 上，並將所得的 timestamp 存放在 `tout` 所指的變數中。

成功時，此函式傳回 0；發生錯誤時傳回負值。

<a id="PGTYPESTIMESTAMPSUBINTERVAL"></a>

### `PGTYPEStimestamp_sub_interval` [#](#pgtypestimestampsubinterval) <a href="#pgtypestimestampsubinterval" id="pgtypestimestampsubinterval"></a>

將 timestamp 變數減去 interval 變數。

```

    int PGTYPEStimestamp_sub_interval(timestamp *tin, interval *span, timestamp *tout);
```

此函式將 `tin` 所指的 timestamp 變數減去 `span` 所指的 interval 變數，並將結果存入 `tout` 所指的變數中。

成功時，此函式傳回 0；發生錯誤時傳回負值。

[返回 34.6. pgtypes 函式庫](ecpg-pgtypes.md#ecpg-pgtypes)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-pgtypes.html)（原文版本：18.6；核對日期：2026-10-18）
