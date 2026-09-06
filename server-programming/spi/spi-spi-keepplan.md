<a id="id-1.8.12.8.29.1"></a>

## SPI_keepplan

SPI_keepplan — 儲存預備陳述式

## 語法

```

int SPI_keepplan(SPIPlanPtr plan)
```

<a id="id-1.8.12.8.29.5"></a>

## 說明

`SPI_keepplan` 會儲存傳入的陳述式（由 `SPI_prepare` 準備），使其不會被 `SPI_finish` 或交易管理器釋放。如此一來，你就能在目前工作階段後續呼叫 C 函式時重複使用預備陳述式。

<a id="id-1.8.12.8.29.6"></a>

## 引數

`SPIPlanPtr plan`
:   要儲存的預備陳述式

<a id="id-1.8.12.8.29.7"></a>

## 回傳值

成功時回傳 0；若 *`plan`* 為 `NULL` 或無效，則回傳 `SPI_ERROR_ARGUMENT`。

<a id="id-1.8.12.8.29.8"></a>

## 注意事項

傳入的陳述式會透過調整指標移至永久儲存區（不需要複製資料）。若之後要刪除它，請對其使用 `SPI_freeplan`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-keepplan.html)（原文版本：18.6；核對日期：2026-09-07）
