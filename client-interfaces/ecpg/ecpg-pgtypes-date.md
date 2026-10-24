<a id="ECPG-PGTYPES-DATE"></a>

## 34.6.3. date 型別 [#](#ecpg-pgtypes-date) <a href="#ecpg-pgtypes-date" id="ecpg-pgtypes-date"></a>

C 中的 date 型別讓你的程式能夠處理 SQL 型別 date 的資料。PostgreSQL 伺服器中對應的型別請參閱[第 8.5 節](../../the-sql-language/datatype/datatype-datetime.md)。

下列函式可用來處理 date 型別：

<a id="PGTYPESDATEFROMTIMESTAMP"></a>

### `PGTYPESdate_from_timestamp` [#](#pgtypesdatefromtimestamp) <a href="#pgtypesdatefromtimestamp" id="pgtypesdatefromtimestamp"></a>

從 timestamp 中擷取日期部分。

```

    date PGTYPESdate_from_timestamp(timestamp dt);
```

此函式接收一個 timestamp 作為唯一引數，並傳回從這個 timestamp 擷取出的日期部分。

<a id="PGTYPESDATEFROMASC"></a>

### `PGTYPESdate_from_asc` [#](#pgtypesdatefromasc) <a href="#pgtypesdatefromasc" id="pgtypesdatefromasc"></a>

從文字表示法剖析出日期。

```

    date PGTYPESdate_from_asc(char *str, char **endptr);
```

此函式接收一個 C char\* 字串 `str`，以及一個指向 C char\* 字串的指標 `endptr`。目前 ECPG 一律剖析整個字串，因此目前不支援將第一個無效字元的位址存放到 `*endptr` 中。
你可以放心地將 `endptr` 設為 NULL。

請注意，此函式一律假設日期採 MDY 格式，而且 ECPG 中目前沒有可以變更這一點的變數。

[表 34.2](ecpg-pgtypes-date.md#ecpg-pgtypesdate-from-asc-table) 列出允許的輸入格式。表中「結果」欄最後三列的英文說明依序表示：年份與該年第幾日、儒略日、西元前 99 年。

<a id="ECPG-PGTYPESDATE-FROM-ASC-TABLE"></a>

### 表 34.2. `PGTYPESdate_from_asc` 的有效輸入格式 [#](#ecpg-pgtypesdate-from-asc-table) <a href="#ecpg-pgtypesdate-from-asc-table" id="ecpg-pgtypesdate-from-asc-table"></a>

<table border="1" class="table" summary="PGTYPESdate_from_asc 的有效輸入格式"><colgroup><col/><col/></colgroup><thead><tr><th>輸入</th><th>結果</th></tr></thead><tbody><tr><td><code class="literal">January 8, 1999</code></td><td><code class="literal">January 8, 1999</code></td></tr><tr><td><code class="literal">1999-01-08</code></td><td><code class="literal">January 8, 1999</code></td></tr><tr><td><code class="literal">1/8/1999</code></td><td><code class="literal">January 8, 1999</code></td></tr><tr><td><code class="literal">1/18/1999</code></td><td><code class="literal">January 18, 1999</code></td></tr><tr><td><code class="literal">01/02/03</code></td><td><code class="literal">February 1, 2003</code></td></tr><tr><td><code class="literal">1999-Jan-08</code></td><td><code class="literal">January 8, 1999</code></td></tr><tr><td><code class="literal">Jan-08-1999</code></td><td><code class="literal">January 8, 1999</code></td></tr><tr><td><code class="literal">08-Jan-1999</code></td><td><code class="literal">January 8, 1999</code></td></tr><tr><td><code class="literal">99-Jan-08</code></td><td><code class="literal">January 8, 1999</code></td></tr><tr><td><code class="literal">08-Jan-99</code></td><td><code class="literal">January 8, 1999</code></td></tr><tr><td><code class="literal">08-Jan-06</code></td><td><code class="literal">January 8, 2006</code></td></tr><tr><td><code class="literal">Jan-08-99</code></td><td><code class="literal">January 8, 1999</code></td></tr><tr><td><code class="literal">19990108</code></td><td><code class="literal">ISO 8601; January 8, 1999</code></td></tr><tr><td><code class="literal">990108</code></td><td><code class="literal">ISO 8601; January 8, 1999</code></td></tr><tr><td><code class="literal">1999.008</code></td><td><code class="literal">year and day of year</code></td></tr><tr><td><code class="literal">J2451187</code></td><td><code class="literal">Julian day</code></td></tr><tr><td><code class="literal">January 8, 99 BC</code></td><td><code class="literal">year 99 before the Common Era</code></td></tr></tbody></table>

譯註：上表中輸入 01/02/03 對應的結果，原文寫作 February 1, 2003，與上文「此函式一律假設日期採 MDY 格式」矛盾；依 MDY 解讀，01/02/03 應為 2003 年 1 月 2 日（January 2, 2003）。表格內容依原文保留。

<br>

<a id="PGTYPESDATETOASC"></a>

### `PGTYPESdate_to_asc` [#](#pgtypesdatetoasc) <a href="#pgtypesdatetoasc" id="pgtypesdatetoasc"></a>

傳回 date 變數的文字表示法。

```

    char *PGTYPESdate_to_asc(date dDate);
```

此函式接收日期 `dDate` 作為唯一參數。
它會以 `1999-01-18` 的形式輸出日期，也就是 `YYYY-MM-DD` 格式。
結果必須以 `PGTYPESchar_free()` 釋放。

<a id="PGTYPESDATEJULMDY"></a>

### `PGTYPESdate_julmdy` [#](#pgtypesdatejulmdy) <a href="#pgtypesdatejulmdy" id="pgtypesdatejulmdy"></a>

從 date 型別的變數中擷取日、月、年的值。

```

    void PGTYPESdate_julmdy(date d, int *mdy);
```

此函式接收日期 `d`，以及一個指向含 3 個整數值之陣列 `mdy` 的指標。變數名稱表示了先後順序：`mdy[0]` 會被設為月份，`mdy[1]` 會被設為日的值，`mdy[2]` 則會包含年份。

<a id="PGTYPESDATEMDYJUL"></a>

### `PGTYPESdate_mdyjul` [#](#pgtypesdatemdyjul) <a href="#pgtypesdatemdyjul" id="pgtypesdatemdyjul"></a>

從指定日期之日、月、年的 3 個整數所組成的陣列建立 date 值。

```

    void PGTYPESdate_mdyjul(int *mdy, date *jdate);
```

此函式以 3 個整數組成的陣列（`mdy`）作為第一個引數，第二個引數則是一個指標，指向用來存放運算結果的 date 型別變數。

<a id="PGTYPESDATEDAYOFWEEK"></a>

### `PGTYPESdate_dayofweek` [#](#pgtypesdatedayofweek) <a href="#pgtypesdatedayofweek" id="pgtypesdatedayofweek"></a>

傳回代表某個 date 值是星期幾的數字。

```

    int PGTYPESdate_dayofweek(date d);
```

此函式接收 date 變數 `d` 作為唯一引數，並傳回一個整數，表示這個日期是星期幾。

* 0 - 星期日
* 1 - 星期一
* 2 - 星期二
* 3 - 星期三
* 4 - 星期四
* 5 - 星期五
* 6 - 星期六

<a id="PGTYPESDATETODAY"></a>

### `PGTYPESdate_today` [#](#pgtypesdatetoday) <a href="#pgtypesdatetoday" id="pgtypesdatetoday"></a>

取得目前日期。

```

    void PGTYPESdate_today(date *d);
```

此函式接收一個指向 date 變數（`d`）的指標，並將該變數設為目前日期。

<a id="PGTYPESDATEFMTASC"></a>

### `PGTYPESdate_fmt_asc` [#](#pgtypesdatefmtasc) <a href="#pgtypesdatefmtasc" id="pgtypesdatefmtasc"></a>

使用格式遮罩，將 date 型別的變數轉換為它的文字表示法。

```

    int PGTYPESdate_fmt_asc(date dDate, char *fmtstring, char *outbuf);
```

此函式接收要轉換的日期（`dDate`）、格式遮罩（`fmtstring`），以及用來存放日期文字表示法的字串（`outbuf`）。

成功時傳回 0，發生錯誤時傳回負值。

下列字面值是你可以使用的欄位指定符號：

* `dd` - 該月中的第幾日。
* `mm` - 該年中的第幾月。
* `yy` - 以兩位數表示的年份。
* `yyyy` - 以四位數表示的年份。
* `ddd` - 星期名稱（縮寫）。
* `mmm` - 月份名稱（縮寫）。

其他所有字元都會原封不動地複製到輸出字串。

[表 34.3](ecpg-pgtypes-date.md#ecpg-pgtypesdate-fmt-asc-example-table) 列出幾種可能的格式，讓你了解如何使用此函式。所有輸出結果都以同一個日期為準：1959 年 11 月 23 日。

<a id="ECPG-PGTYPESDATE-FMT-ASC-EXAMPLE-TABLE"></a>

### 表 34.3. `PGTYPESdate_fmt_asc` 的有效輸入格式 [#](#ecpg-pgtypesdate-fmt-asc-example-table) <a href="#ecpg-pgtypesdate-fmt-asc-example-table" id="ecpg-pgtypesdate-fmt-asc-example-table"></a>

<table border="1" class="table" summary="PGTYPESdate_fmt_asc 的有效輸入格式"><colgroup><col/><col/></colgroup><thead><tr><th>格式</th><th>結果</th></tr></thead><tbody><tr><td><code class="literal">mmddyy</code></td><td><code class="literal">112359</code></td></tr><tr><td><code class="literal">ddmmyy</code></td><td><code class="literal">231159</code></td></tr><tr><td><code class="literal">yymmdd</code></td><td><code class="literal">591123</code></td></tr><tr><td><code class="literal">yy/mm/dd</code></td><td><code class="literal">59/11/23</code></td></tr><tr><td><code class="literal">yy mm dd</code></td><td><code class="literal">59 11 23</code></td></tr><tr><td><code class="literal">yy.mm.dd</code></td><td><code class="literal">59.11.23</code></td></tr><tr><td><code class="literal">.mm.yyyy.dd.</code></td><td><code class="literal">.11.1959.23.</code></td></tr><tr><td><code class="literal">mmm. dd, yyyy</code></td><td><code class="literal">Nov. 23, 1959</code></td></tr><tr><td><code class="literal">mmm dd yyyy</code></td><td><code class="literal">Nov 23 1959</code></td></tr><tr><td><code class="literal">yyyy dd mm</code></td><td><code class="literal">1959 23 11</code></td></tr><tr><td><code class="literal">ddd, mmm. dd, yyyy</code></td><td><code class="literal">Mon, Nov. 23, 1959</code></td></tr><tr><td><code class="literal">(ddd) mmm. dd, yyyy</code></td><td><code class="literal">(Mon) Nov. 23, 1959</code></td></tr></tbody></table>

<br>

譯註：此表列出的是格式遮罩與對應的輸出結果；表標題沿用原文「Valid Input Formats」（有效輸入格式）的字面譯法。

<a id="PGTYPESDATEDEFMTASC"></a>

### `PGTYPESdate_defmt_asc` [#](#pgtypesdatedefmtasc) <a href="#pgtypesdatedefmtasc" id="pgtypesdatedefmtasc"></a>

使用格式遮罩，將 C `char*` 字串轉換為 date 型別的值。

```

    int PGTYPESdate_defmt_asc(date *d, char *fmt, char *str);
```

此函式接收一個指向用來存放運算結果之 date 值的指標（`d`）、剖析日期時使用的格式遮罩（`fmt`），以及內含日期文字表示法的 C char\* 字串（`str`）。文字表示法應該要符合格式遮罩。不過，字串與格式遮罩之間不需要一對一對應。此函式只分析先後順序，並尋找表示年份位置的字面值 `yy` 或 `yyyy`、表示月份位置的 `mm`，以及表示日位置的 `dd`。

[表 34.4](ecpg-pgtypes-date.md#ecpg-rdefmtdate-example-table) 列出幾種可能的格式，讓你了解如何使用此函式。

<a id="ECPG-RDEFMTDATE-EXAMPLE-TABLE"></a>

### 表 34.4. `rdefmtdate` 的有效輸入格式 [#](#ecpg-rdefmtdate-example-table) <a href="#ecpg-rdefmtdate-example-table" id="ecpg-rdefmtdate-example-table"></a>

<table border="1" class="table" summary="rdefmtdate 的有效輸入格式"><colgroup><col/><col/><col/></colgroup><thead><tr><th>格式</th><th>字串</th><th>結果</th></tr></thead><tbody><tr><td><code class="literal">ddmmyy</code></td><td><code class="literal">21-2-54</code></td><td><code class="literal">1954-02-21</code></td></tr><tr><td><code class="literal">ddmmyy</code></td><td><code class="literal">2-12-54</code></td><td><code class="literal">1954-12-02</code></td></tr><tr><td><code class="literal">ddmmyy</code></td><td><code class="literal">20111954</code></td><td><code class="literal">1954-11-20</code></td></tr><tr><td><code class="literal">ddmmyy</code></td><td><code class="literal">130464</code></td><td><code class="literal">1964-04-13</code></td></tr><tr><td><code class="literal">mmm.dd.yyyy</code></td><td><code class="literal">MAR-12-1967</code></td><td><code class="literal">1967-03-12</code></td></tr><tr><td><code class="literal">yy/mm/dd</code></td><td><code class="literal">1954, February 3rd</code></td><td><code class="literal">1954-02-03</code></td></tr><tr><td><code class="literal">mmm.dd.yyyy</code></td><td><code class="literal">041269</code></td><td><code class="literal">1969-04-12</code></td></tr><tr><td><code class="literal">yy/mm/dd</code></td><td><code class="literal">In the year 2525, in the month of July, mankind will be alive on the 28th day</code></td><td><code class="literal">2525-07-28</code></td></tr><tr><td><code class="literal">dd-mm-yy</code></td><td><code class="literal">I said on the 28th of July in the year 2525</code></td><td><code class="literal">2525-07-28</code></td></tr><tr><td><code class="literal">mmm.dd.yyyy</code></td><td><code class="literal">9/14/58</code></td><td><code class="literal">1958-09-14</code></td></tr><tr><td><code class="literal">yy/mm/dd</code></td><td><code class="literal">47/03/29</code></td><td><code class="literal">1947-03-29</code></td></tr><tr><td><code class="literal">mmm.dd.yyyy</code></td><td><code class="literal">oct 28 1975</code></td><td><code class="literal">1975-10-28</code></td></tr><tr><td><code class="literal">mmddyy</code></td><td><code class="literal">Nov 14th, 1985</code></td><td><code class="literal">1985-11-14</code></td></tr></tbody></table>

<br>

譯註：此表標題中的 rdefmtdate 是 Informix 相容模式中的對應函式（原文於該函式的說明與此處相同）；表中格式同樣適用於本項的 PGTYPESdate_defmt_asc。

[返回 34.6. pgtypes 函式庫](ecpg-pgtypes.md#ecpg-pgtypes)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-pgtypes.html)（原文版本：18.6；核對日期：2026-10-18）
