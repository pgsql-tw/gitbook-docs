<a id="id-1.8.12.8.18.1"></a>

## SPI_execp

SPI_execp — 以讀寫模式執行陳述式

## 概要

```

int SPI_execp(SPIPlanPtr plan, Datum * values, const char * nulls, long count)
```

<a id="id-1.8.12.8.18.5"></a>

## 描述

`SPI_execp` 與 `SPI_execute_plan` 相同，只是後者的 *`read_only`* 參數永遠被視為 `false`。

<a id="id-1.8.12.8.18.6"></a>

## 引數

`SPIPlanPtr plan`
:   預備陳述式（由 `SPI_prepare` 回傳）

`Datum * values`
:   實際參數值的陣列。長度必須與該陳述式的引數個數相同。

`const char * nulls`
:   描述哪些參數為 NULL 的陣列。長度必須與該陳述式的引數個數相同。

    如果 *`nulls`* 是 `NULL`，則 `SPI_execp` 會假設沒有任何參數是 NULL。否則，*`nulls`* 陣列的每個項目在對應的參數值不為 NULL 時應該是 `' '`，在對應的參數值為 NULL 時則應該是 `'n'`。（在後者的情況下，對應的 *`values`* 項目中的實際值並不重要。）請注意，*`nulls`* 並不是文字字串，而只是一個陣列：它不需要 `'\0'` 結束符號。

`long count`
:   要回傳的最大資料列數，或是以 `0` 表示不限制

<a id="id-1.8.12.8.18.7"></a>

## 回傳值

請參閱 `SPI_execute_plan`。

若執行成功，`SPI_processed` 與 `SPI_tuptable` 的設定方式和 `SPI_execute` 相同。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-execp.html)（原文版本：18.6；核對日期：2026-09-13）
