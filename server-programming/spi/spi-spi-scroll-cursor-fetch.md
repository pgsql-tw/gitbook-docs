<a id="id-1.8.12.8.26.1"></a>

## SPI_scroll_cursor_fetch

SPI_scroll_cursor_fetch — 從游標擷取一些資料列

## 語法

```

void SPI_scroll_cursor_fetch(Portal portal, FetchDirection direction,
                             long count)
```

<a id="id-1.8.12.8.26.5"></a>

## 說明

`SPI_scroll_cursor_fetch` 會從游標擷取一些資料列。它等同於 SQL 命令 `FETCH`。

<a id="id-1.8.12.8.26.6"></a>

## 引數

`Portal portal`
:   包含游標的 portal。

`FetchDirection direction`
:   `FETCH_FORWARD`、`FETCH_BACKWARD`、`FETCH_ABSOLUTE` 或 `FETCH_RELATIVE` 之一。

`long count`
:   `FETCH_FORWARD` 或 `FETCH_BACKWARD` 要擷取的資料列數；`FETCH_ABSOLUTE` 要擷取的絕對資料列編號；或 `FETCH_RELATIVE` 要擷取的相對資料列編號。

<a id="id-1.8.12.8.26.7"></a>

## 回傳值

成功時，`SPI_processed` 與 `SPI_tuptable` 的設定方式同 `SPI_execute`。

<a id="id-1.8.12.8.26.8"></a>

## 注意事項

*`direction`* 與 *`count`* 參數的解讀細節，請參閱 SQL [FETCH](../../reference/sql-commands/sql-fetch.md) 命令。

若游標計畫未以 `CURSOR_OPT_SCROLL` 選項建立，`FETCH_FORWARD` 以外的方向值可能失敗。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-scroll-cursor-fetch.html)（原文版本：18.6；核對日期：2026-09-11）
