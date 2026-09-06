<a id="id-1.8.12.8.28.1"></a>

## SPI_cursor_close

SPI_cursor_close — close a cursor

## Synopsis

```

void SPI_cursor_close(Portal portal)
```

<a id="id-1.8.12.8.28.5"></a>

## Description

`SPI_cursor_close` closes a previously created
cursor and releases its portal storage.

All open cursors are closed automatically at the end of a
transaction. `SPI_cursor_close` need only be
invoked if it is desirable to release resources sooner.

<a id="id-1.8.12.8.28.6"></a>

## Arguments

`Portal portal`
:   portal containing the cursor

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-cursor-close.html)（英文原文，待翻譯）
