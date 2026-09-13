<a id="id-1.8.12.8.15.1"></a>

## SPI_execute_plan

SPI_execute_plan — 執行由 `SPI_prepare` 預備好的陳述式

## 概要

```

int SPI_execute_plan(SPIPlanPtr plan, Datum * values, const char * nulls,
                     bool read_only, long count)
```

<a id="id-1.8.12.8.15.5"></a>

## 描述

`SPI_execute_plan` 會執行由 `SPI_prepare` 或其同類函式所預備的陳述式。*`read_only`* 與 *`count`* 的意義和 `SPI_execute` 中的相同。

<a id="id-1.8.12.8.15.6"></a>

## 引數

`SPIPlanPtr plan`
:   預備陳述式（由 `SPI_prepare` 回傳）

`Datum * values`
:   實際參數值的陣列。長度必須與該陳述式的引數個數相同。

`const char * nulls`
:   描述哪些參數為 NULL 的陣列。長度必須與該陳述式的引數個數相同。

    如果 *`nulls`* 是 `NULL`，則 `SPI_execute_plan` 會假設沒有任何參數是 NULL。否則，*`nulls`* 陣列的每個項目在對應的參數值不為 NULL 時應該是 `' '`，在對應的參數值為 NULL 時則應該是 `'n'`。（在後者的情況下，對應的 *`values`* 項目中的實際值並不重要。）請注意，*`nulls`* 並不是文字字串，而只是一個陣列：它不需要 `'\0'` 結束符號。

`bool read_only`
:   `true` 表示唯讀執行

`long count`
:   要回傳的最大資料列數，或是以 `0` 表示不限制

<a id="id-1.8.12.8.15.7"></a>

## 回傳值

回傳值與 `SPI_execute` 相同，另外還可能出現以下的錯誤（負值）結果：

`SPI_ERROR_ARGUMENT`
:   如果 *`plan`* 是 `NULL` 或無效，或 *`count`* 小於 0

`SPI_ERROR_PARAM`
:   如果 *`values`* 是 `NULL`，而 *`plan`* 在預備時帶有一些參數

若執行成功，`SPI_processed` 與 `SPI_tuptable` 的設定方式和 `SPI_execute` 相同。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-execute-plan.html)（原文版本：18.6；核對日期：2026-09-13）
