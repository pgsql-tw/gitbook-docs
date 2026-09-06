<a id="id-1.8.12.10.14.1"></a>

## SPI_freeplan

SPI_freeplan — 釋放先前儲存的預備陳述式

## 語法

```

int SPI_freeplan(SPIPlanPtr plan)
```

<a id="id-1.8.12.10.14.5"></a>

## 說明

`SPI_freeplan` 會釋放先前由 `SPI_prepare` 回傳，或由 `SPI_keepplan` 或 `SPI_saveplan` 儲存的預備陳述式。

<a id="id-1.8.12.10.14.6"></a>

## 引數

`SPIPlanPtr plan`
:   指向要釋放之陳述式的指標

<a id="id-1.8.12.10.14.7"></a>

## 回傳值

成功時回傳 0；若 *`plan`* 為 `NULL` 或無效，則回傳 `SPI_ERROR_ARGUMENT`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-freeplan.html)（原文版本：18.6；核對日期：2026-09-07）
