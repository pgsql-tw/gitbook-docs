<a id="id-1.8.12.8.27.1"></a>

## SPI_scroll_cursor_move

SPI_scroll_cursor_move — 移動游標

## 概要

```

void SPI_scroll_cursor_move(Portal portal, FetchDirection direction,
                            long count)
```

<a id="id-1.8.12.8.27.5"></a>

## 描述

`SPI_scroll_cursor_move` 會在游標中跳過若干資料列。這等同於 SQL 指令 `MOVE`。

<a id="id-1.8.12.8.27.6"></a>

## 引數

`Portal portal`
:   含有該游標的 portal

`FetchDirection direction`
:   `FETCH_FORWARD`、`FETCH_BACKWARD`、`FETCH_ABSOLUTE` 或 `FETCH_RELATIVE` 其中之一

`long count`
:   對 `FETCH_FORWARD` 或 `FETCH_BACKWARD` 而言是要移動的資料列數；對 `FETCH_ABSOLUTE` 而言是要移動到的絕對資料列編號；對 `FETCH_RELATIVE` 而言則是要移動到的相對資料列編號

<a id="id-1.8.12.8.27.7"></a>

## 回傳值

若執行成功，`SPI_processed` 的設定方式和 `SPI_execute` 相同。`SPI_tuptable` 會被設為 `NULL`，因為這個函式不會回傳任何資料列。

<a id="id-1.8.12.8.27.8"></a>

## 註記

關於 *`direction`* 與 *`count`* 參數如何解讀的細節，請參閱 SQL 的 [FETCH](../../reference/sql-commands/sql-fetch.md) 指令。

如果該游標的執行計畫在建立時未使用 `CURSOR_OPT_SCROLL` 選項，那麼除了 `FETCH_FORWARD` 以外的方向值都可能會失敗。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-scroll-cursor-move.html)（原文版本：18.6；核對日期：2026-09-13）
