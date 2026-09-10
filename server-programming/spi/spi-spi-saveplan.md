<a id="id-1.8.12.8.30.1"></a>

## SPI_saveplan

SPI_saveplan — 儲存已準備的陳述式

## 語法

```

SPIPlanPtr SPI_saveplan(SPIPlanPtr plan)
```

<a id="id-1.8.12.8.30.5"></a>

## 說明

`SPI_saveplan` 會將傳入、由 `SPI_prepare` 準備的陳述式複製到不會由 `SPI_finish` 或交易管理器釋放的記憶體，並傳回已複製陳述式的指標。因此可在目前工作階段後續呼叫 C 函式時重複使用已準備的陳述式。

<a id="id-1.8.12.8.30.6"></a>

## 引數

`SPIPlanPtr plan`
:   要儲存的已準備陳述式。

<a id="id-1.8.12.8.30.7"></a>

## 回傳值

傳回已複製陳述式的指標；失敗時傳回 `NULL`。發生錯誤時，`SPI_result` 設定如下：

`SPI_ERROR_ARGUMENT`
:   *`plan`* 為 `NULL` 或無效。

`SPI_ERROR_UNCONNECTED`
:   從未連線的 C 函式呼叫。

<a id="id-1.8.12.8.30.8"></a>

## 注意事項

原始傳入的陳述式不會被釋放，因此你可能要對它執行 `SPI_freeplan`，以避免在 `SPI_finish` 前發生記憶體洩漏。

大多數情況下應優先使用 `SPI_keepplan`，因為它不需實際複製已準備陳述式的資料結構，就能大致達成相同結果。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-saveplan.html)（原文版本：18.6；核對日期：2026-09-11）
