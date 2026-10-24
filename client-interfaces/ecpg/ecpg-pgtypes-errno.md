<a id="ECPG-PGTYPES-ERRNO"></a>

## 34.6.7. pgtypeslib 的 errno 值 [#](#ecpg-pgtypes-errno) <a href="#ecpg-pgtypes-errno" id="ecpg-pgtypes-errno"></a>

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-NUM-BAD-NUMERIC"></a>

### `PGTYPES_NUM_BAD_NUMERIC` [#](#ecpg-pgtypes-errno-pgtypes-num-bad-numeric) <a href="#ecpg-pgtypes-errno-pgtypes-num-bad-numeric" id="ecpg-pgtypes-errno-pgtypes-num-bad-numeric"></a>

引數應該包含一個 numeric 變數（或指向一個 numeric 變數），但它在記憶體中的表示實際上無效。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-NUM-OVERFLOW"></a>

### `PGTYPES_NUM_OVERFLOW` [#](#ecpg-pgtypes-errno-pgtypes-num-overflow) <a href="#ecpg-pgtypes-errno-pgtypes-num-overflow" id="ecpg-pgtypes-errno-pgtypes-num-overflow"></a>

發生溢位。由於 numeric 型別幾乎可以處理任意精確度，將 numeric 變數轉換為其他型別時可能會導致溢位。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-NUM-UNDERFLOW"></a>

### `PGTYPES_NUM_UNDERFLOW` [#](#ecpg-pgtypes-errno-pgtypes-num-underflow) <a href="#ecpg-pgtypes-errno-pgtypes-num-underflow" id="ecpg-pgtypes-errno-pgtypes-num-underflow"></a>

發生下溢。由於 numeric 型別幾乎可以處理任意精確度，將 numeric 變數轉換為其他型別時可能會導致下溢。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-NUM-DIVIDE-ZERO"></a>

### `PGTYPES_NUM_DIVIDE_ZERO` [#](#ecpg-pgtypes-errno-pgtypes-num-divide-zero) <a href="#ecpg-pgtypes-errno-pgtypes-num-divide-zero" id="ecpg-pgtypes-errno-pgtypes-num-divide-zero"></a>

嘗試除以零。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-DATE"></a>

### `PGTYPES_DATE_BAD_DATE` [#](#ecpg-pgtypes-errno-pgtypes-date-bad-date) <a href="#ecpg-pgtypes-errno-pgtypes-date-bad-date" id="ecpg-pgtypes-errno-pgtypes-date-bad-date"></a>

傳給 `PGTYPESdate_from_asc` 函式的日期字串無效。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-EARGS"></a>

### `PGTYPES_DATE_ERR_EARGS` [#](#ecpg-pgtypes-errno-pgtypes-date-err-eargs) <a href="#ecpg-pgtypes-errno-pgtypes-date-err-eargs" id="ecpg-pgtypes-errno-pgtypes-date-err-eargs"></a>

傳給 `PGTYPESdate_defmt_asc` 函式的引數無效。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-ENOSHORTDATE"></a>

### `PGTYPES_DATE_ERR_ENOSHORTDATE` [#](#ecpg-pgtypes-errno-pgtypes-date-err-enoshortdate) <a href="#ecpg-pgtypes-errno-pgtypes-date-err-enoshortdate" id="ecpg-pgtypes-errno-pgtypes-date-err-enoshortdate"></a>

`PGTYPESdate_defmt_asc` 函式在輸入字串中發現無效的語彙單元（token）。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-INTVL-BAD-INTERVAL"></a>

### `PGTYPES_INTVL_BAD_INTERVAL` [#](#ecpg-pgtypes-errno-pgtypes-intvl-bad-interval) <a href="#ecpg-pgtypes-errno-pgtypes-intvl-bad-interval" id="ecpg-pgtypes-errno-pgtypes-intvl-bad-interval"></a>

傳給 `PGTYPESinterval_from_asc` 函式的 interval 字串無效，或傳給 `PGTYPESinterval_to_asc` 函式的 interval 值無效。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-ERR-ENOTDMY"></a>

### `PGTYPES_DATE_ERR_ENOTDMY` [#](#ecpg-pgtypes-errno-pgtypes-date-err-enotdmy) <a href="#ecpg-pgtypes-errno-pgtypes-date-err-enotdmy" id="ecpg-pgtypes-errno-pgtypes-date-err-enotdmy"></a>

`PGTYPESdate_defmt_asc` 函式中的日／月／年指派不相符。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-DAY"></a>

### `PGTYPES_DATE_BAD_DAY` [#](#ecpg-pgtypes-errno-pgtypes-date-bad-day) <a href="#ecpg-pgtypes-errno-pgtypes-date-bad-day" id="ecpg-pgtypes-errno-pgtypes-date-bad-day"></a>

`PGTYPESdate_defmt_asc` 函式發現無效的「該月第幾日」值。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-DATE-BAD-MONTH"></a>

### `PGTYPES_DATE_BAD_MONTH` [#](#ecpg-pgtypes-errno-pgtypes-date-bad-month) <a href="#ecpg-pgtypes-errno-pgtypes-date-bad-month" id="ecpg-pgtypes-errno-pgtypes-date-bad-month"></a>

`PGTYPESdate_defmt_asc` 函式發現無效的月份值。

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-TS-BAD-TIMESTAMP"></a>

### `PGTYPES_TS_BAD_TIMESTAMP` [#](#ecpg-pgtypes-errno-pgtypes-ts-bad-timestamp) <a href="#ecpg-pgtypes-errno-pgtypes-ts-bad-timestamp" id="ecpg-pgtypes-errno-pgtypes-ts-bad-timestamp"></a>

傳給 `PGTYPEStimestamp_from_asc` 函式的 timestamp 字串無效，或傳給 `PGTYPEStimestamp_to_asc` 函式的 timestamp 值無效。（原文此處寫作「pass passed」，應為「was passed」的誤植。）

<a id="ECPG-PGTYPES-ERRNO-PGTYPES-TS-ERR-EINFTIME"></a>

### `PGTYPES_TS_ERR_EINFTIME` [#](#ecpg-pgtypes-errno-pgtypes-ts-err-einftime) <a href="#ecpg-pgtypes-errno-pgtypes-ts-err-einftime" id="ecpg-pgtypes-errno-pgtypes-ts-err-einftime"></a>

在無法處理無限 timestamp 值的情境中遇到了這種值。

[返回 34.6. pgtypes 函式庫](ecpg-pgtypes.md#ecpg-pgtypes)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-pgtypes.html)（原文版本：18.6；核對日期：2026-10-18）
