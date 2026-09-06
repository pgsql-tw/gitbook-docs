<a id="SPI-SPI-CURSOR-FETCH"></a><a id="id-1.8.12.8.24.1"></a>

# SPI_cursor_fetch

SPI_cursor_fetch — fetch some rows from a cursor

## Synopsis

```

void SPI_cursor_fetch(Portal portal, bool forward, long count)
```

<a id="id-1.8.12.8.24.5"></a>

## Description

`SPI_cursor_fetch` fetches some rows from a cursor. This is equivalent to a subset of the SQL command `FETCH` (see `SPI_scroll_cursor_fetch` for more functionality).

<a id="id-1.8.12.8.24.6"></a>

## Arguments

<code class="literal">Portal <em class="parameter"><code>portal</code></em></code>

portal containing the cursor

<code class="literal">bool <em class="parameter"><code>forward</code></em></code>

true for fetch forward, false for fetch backward

<code class="literal">long <em class="parameter"><code>count</code></em></code>

maximum number of rows to fetch

<a id="id-1.8.12.8.24.7"></a>

## Return Value

`SPI_processed` and `SPI_tuptable` are set as in `SPI_execute` if successful.

<a id="id-1.8.12.8.24.8"></a>

## Notes

Fetching backward may fail if the cursor's plan was not created with the `CURSOR_OPT_SCROLL` option.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-cursor-fetch.md)（英文原文，待翻譯）
