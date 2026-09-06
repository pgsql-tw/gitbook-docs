<a id="id-1.8.12.8.25.1"></a>

## SPI_cursor_move

SPI_cursor_move — 移動游標

## 語法

```

void SPI_cursor_move(Portal portal, bool forward, long count)
```

<a id="id-1.8.12.8.25.5"></a>

## 說明

`SPI_cursor_move` 會略過游標中的若干資料列。這相當於 SQL 命令 `MOVE` 的部分功能（更多功能請參閱 `SPI_scroll_cursor_move`）。

<a id="id-1.8.12.8.25.6"></a>

## 引數

`Portal portal`
:   包含游標的 portal

`bool forward`
:   true 表示向前移動，false 表示向後移動

`long count`
:   最多移動的資料列數

<a id="id-1.8.12.8.25.7"></a>

## 注意事項

若建立游標的計畫時未使用 `CURSOR_OPT_SCROLL` 選項，向後移動可能會失敗。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-cursor-move.html)（原文版本：18.6；核對日期：2026-09-07）
