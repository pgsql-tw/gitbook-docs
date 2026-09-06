<a id="id-1.8.12.8.12.1"></a>

## SPI_getargcount

SPI_getargcount — 回傳由 `SPI_prepare` 準備的陳述式所需的引數數量

## 語法

```

int SPI_getargcount(SPIPlanPtr plan)
```

<a id="id-1.8.12.8.12.5"></a>

## 說明

`SPI_getargcount` 會回傳執行由 `SPI_prepare` 準備的陳述式所需的引數數量。

<a id="id-1.8.12.8.12.6"></a>

## 引數

`SPIPlanPtr plan`
:   預備陳述式（由 `SPI_prepare` 回傳）

<a id="id-1.8.12.8.12.7"></a>

## 回傳值

*`plan`* 預期的引數數量。若 *`plan`* 為 `NULL` 或無效，則將 `SPI_result` 設為 `SPI_ERROR_ARGUMENT`，並回傳 -1。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-getargcount.html)（原文版本：18.6；核對日期：2026-09-07）
