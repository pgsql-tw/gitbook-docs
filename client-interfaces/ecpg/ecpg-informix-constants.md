<a id="ECPG-INFORMIX-CONSTANTS"></a>

## 34.15.5. 額外的常數 [#](#ecpg-informix-constants) <a href="#ecpg-informix-constants" id="ecpg-informix-constants"></a>

請注意，這裡的所有常數都用來描述錯誤，而且全都定義為代表負值。在各個常數的說明中，你也可以找到該常數在目前實作中所代表的值。不過，你不應該依賴這個數字。但你可以依賴這些常數全都定義為代表負值這一點。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-OVERFLOW"></a>

### `ECPG_INFORMIX_NUM_OVERFLOW` [#](#ecpg-informix-constants-ecpg-informix-num-overflow) <a href="#ecpg-informix-constants-ecpg-informix-num-overflow" id="ecpg-informix-constants-ecpg-informix-num-overflow"></a>

若計算中發生溢位，函式會傳回此值。其內部定義為 -1200（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-NUM-UNDERFLOW"></a>

### `ECPG_INFORMIX_NUM_UNDERFLOW` [#](#ecpg-informix-constants-ecpg-informix-num-underflow) <a href="#ecpg-informix-constants-ecpg-informix-num-underflow" id="ecpg-informix-constants-ecpg-informix-num-underflow"></a>

若計算中發生下溢，函式會傳回此值。其內部定義為 -1201（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DIVIDE-ZERO"></a>

### `ECPG_INFORMIX_DIVIDE_ZERO` [#](#ecpg-informix-constants-ecpg-informix-divide-zero) <a href="#ecpg-informix-constants-ecpg-informix-divide-zero" id="ecpg-informix-constants-ecpg-informix-divide-zero"></a>

若偵測到除以零的嘗試，函式會傳回此值。其內部定義為 -1202（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-YEAR"></a>

### `ECPG_INFORMIX_BAD_YEAR` [#](#ecpg-informix-constants-ecpg-informix-bad-year) <a href="#ecpg-informix-constants-ecpg-informix-bad-year" id="ecpg-informix-constants-ecpg-informix-bad-year"></a>

若剖析日期時發現不正確的年份值，函式會傳回此值。其內部定義為 -1204（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-MONTH"></a>

### `ECPG_INFORMIX_BAD_MONTH` [#](#ecpg-informix-constants-ecpg-informix-bad-month) <a href="#ecpg-informix-constants-ecpg-informix-bad-month" id="ecpg-informix-constants-ecpg-informix-bad-month"></a>

若剖析日期時發現不正確的月份值，函式會傳回此值。其內部定義為 -1205（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DAY"></a>

### `ECPG_INFORMIX_BAD_DAY` [#](#ecpg-informix-constants-ecpg-informix-bad-day) <a href="#ecpg-informix-constants-ecpg-informix-bad-day" id="ecpg-informix-constants-ecpg-informix-bad-day"></a>

若剖析日期時發現不正確的日值，函式會傳回此值。其內部定義為 -1206（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOSHORTDATE"></a>

### `ECPG_INFORMIX_ENOSHORTDATE` [#](#ecpg-informix-constants-ecpg-informix-enoshortdate) <a href="#ecpg-informix-constants-ecpg-informix-enoshortdate" id="ecpg-informix-constants-ecpg-informix-enoshortdate"></a>

若剖析常式需要簡短的日期表示法，但取得的日期字串長度不正確，函式會傳回此值。其內部定義為 -1209（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-DATE-CONVERT"></a>

### `ECPG_INFORMIX_DATE_CONVERT` [#](#ecpg-informix-constants-ecpg-informix-date-convert) <a href="#ecpg-informix-constants-ecpg-informix-date-convert" id="ecpg-informix-constants-ecpg-informix-date-convert"></a>

若格式化日期時發生錯誤，函式會傳回此值。其內部定義為 -1210（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-OUT-OF-MEMORY"></a>

### `ECPG_INFORMIX_OUT_OF_MEMORY` [#](#ecpg-informix-constants-ecpg-informix-out-of-memory) <a href="#ecpg-informix-constants-ecpg-informix-out-of-memory" id="ecpg-informix-constants-ecpg-informix-out-of-memory"></a>

若函式在運作期間記憶體耗盡，會傳回此值。其內部定義為 -1211（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-ENOTDMY"></a>

### `ECPG_INFORMIX_ENOTDMY` [#](#ecpg-informix-constants-ecpg-informix-enotdmy) <a href="#ecpg-informix-constants-ecpg-informix-enotdmy" id="ecpg-informix-constants-ecpg-informix-enotdmy"></a>

若剖析常式應取得格式遮罩（例如 `mmddyy`），但並非所有欄位都正確列出，函式會傳回此值。其內部定義為 -1212（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-NUMERIC"></a>

### `ECPG_INFORMIX_BAD_NUMERIC` [#](#ecpg-informix-constants-ecpg-informix-bad-numeric) <a href="#ecpg-informix-constants-ecpg-informix-bad-numeric" id="ecpg-informix-constants-ecpg-informix-bad-numeric"></a>

若剖析常式因數值的文字表示法含有錯誤而無法剖析，或是常式因至少一個數值變數無效而無法完成涉及數值變數的計算，函式會傳回此值。其內部定義為 -1213（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-EXPONENT"></a>

### `ECPG_INFORMIX_BAD_EXPONENT` [#](#ecpg-informix-constants-ecpg-informix-bad-exponent) <a href="#ecpg-informix-constants-ecpg-informix-bad-exponent" id="ecpg-informix-constants-ecpg-informix-bad-exponent"></a>

若剖析常式無法剖析指數，函式會傳回此值。其內部定義為 -1216（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-BAD-DATE"></a>

### `ECPG_INFORMIX_BAD_DATE` [#](#ecpg-informix-constants-ecpg-informix-bad-date) <a href="#ecpg-informix-constants-ecpg-informix-bad-date" id="ecpg-informix-constants-ecpg-informix-bad-date"></a>

若剖析常式無法剖析日期，函式會傳回此值。其內部定義為 -1218（Informix 的定義）。

<a id="ECPG-INFORMIX-CONSTANTS-ECPG-INFORMIX-EXTRA-CHARS"></a>

### `ECPG_INFORMIX_EXTRA_CHARS` [#](#ecpg-informix-constants-ecpg-informix-extra-chars) <a href="#ecpg-informix-constants-ecpg-informix-extra-chars" id="ecpg-informix-constants-ecpg-informix-extra-chars"></a>

若傳給剖析常式的內容含有它無法剖析的多餘字元，函式會傳回此值。其內部定義為 -1264（Informix 的定義）。

[返回 34.15. Informix 相容模式](ecpg-informix-compat.md#ecpg-informix-compat)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-informix-compat.html)（原文版本：18.6；核對日期：2026-10-22）
