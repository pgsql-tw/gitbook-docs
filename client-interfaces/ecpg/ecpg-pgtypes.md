<a id="ECPG-PGTYPES"></a>

## 34.6. pgtypes 函式庫 [#](#ecpg-pgtypes) <a href="#ecpg-pgtypes" id="ecpg-pgtypes"></a>

[34.6.1. 字串](ecpg-pgtypes.md#ecpg-pgtypes-cstrings)

[34.6.2. numeric 型別](ecpg-pgtypes-numeric.md#ecpg-pgtypes-numeric)

[34.6.3. date 型別](ecpg-pgtypes-date.md#ecpg-pgtypes-date)

[34.6.4. timestamp 型別](ecpg-pgtypes-timestamp.md#ecpg-pgtypes-timestamp)

[34.6.5. interval 型別](ecpg-pgtypes-interval.md#ecpg-pgtypes-interval)

[34.6.6. decimal 型別](ecpg-pgtypes-decimal.md#ecpg-pgtypes-decimal)

[34.6.7. pgtypeslib 的 errno 值](ecpg-pgtypes-errno.md#ecpg-pgtypes-errno)

[34.6.8. pgtypeslib 的特殊常數](ecpg-pgtypes-constants.md#ecpg-pgtypes-constants)

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

本節內容請參閱[34.6.6. decimal 型別](ecpg-pgtypes-decimal.md#ecpg-pgtypes-decimal)。

<a id="ECPG-PGTYPES-ERRNO"></a>

### 34.6.7. pgtypeslib 的 errno 值 [#](#ecpg-pgtypes-errno) <a href="#ecpg-pgtypes-errno" id="ecpg-pgtypes-errno"></a>

本節內容請參閱[34.6.7. pgtypeslib 的 errno 值](ecpg-pgtypes-errno.md#ecpg-pgtypes-errno)。

<a id="ECPG-PGTYPES-CONSTANTS"></a>

### 34.6.8. pgtypeslib 的特殊常數 [#](#ecpg-pgtypes-constants) <a href="#ecpg-pgtypes-constants" id="ecpg-pgtypes-constants"></a>

本節內容請參閱[34.6.8. pgtypeslib 的特殊常數](ecpg-pgtypes-constants.md#ecpg-pgtypes-constants)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-pgtypes.html)（原文版本：18.6；核對日期：2026-10-18）
