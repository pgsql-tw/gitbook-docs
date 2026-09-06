<a id="id-1.8.12.8.24.1"></a>

## SPI_cursor_fetch

SPI_cursor_fetch — 從游標擷取若干資料列

## 語法

```

void SPI_cursor_fetch(Portal portal, bool forward, long count)
```

<a id="id-1.8.12.8.24.5"></a>

## 說明

`SPI_cursor_fetch` 會從游標擷取若干資料列。這相當於 SQL 命令 `FETCH` 的部分功能（更多功能請參閱 `SPI_scroll_cursor_fetch`）。

<a id="id-1.8.12.8.24.6"></a>

## 引數

`Portal portal`
:   包含游標的 portal

`bool forward`
:   true 表示向前擷取，false 表示向後擷取

`long count`
:   最多擷取的資料列數

<a id="id-1.8.12.8.24.7"></a>

## 回傳值

成功時，`SPI_processed` 與 `SPI_tuptable` 的設定方式與 `SPI_execute` 相同。

<a id="id-1.8.12.8.24.8"></a>

## 注意事項

若建立游標的計畫時未使用 `CURSOR_OPT_SCROLL` 選項，向後擷取可能會失敗。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-cursor-fetch.html)（原文版本：18.6；核對日期：2026-09-07）
