<a id="SPI-SPI-CURSOR-MOVE"></a><a id="id-1.8.12.8.25.1"></a>

# SPI_cursor_move

SPI_cursor_move — move a cursor

## Synopsis

```

void SPI_cursor_move(Portal portal, bool forward, long count)
```

<a id="id-1.8.12.8.25.5"></a>

## Description

`SPI_cursor_move` skips over some number of rows in a cursor. This is equivalent to a subset of the SQL command `MOVE` (see `SPI_scroll_cursor_move` for more functionality).

<a id="id-1.8.12.8.25.6"></a>

## Arguments

<code class="literal">Portal <em class="parameter"><code>portal</code></em></code>

portal containing the cursor

<code class="literal">bool <em class="parameter"><code>forward</code></em></code>

true for move forward, false for move backward

<code class="literal">long <em class="parameter"><code>count</code></em></code>

maximum number of rows to move

<a id="id-1.8.12.8.25.7"></a>

## Notes

Moving backward may fail if the cursor's plan was not created with the `CURSOR_OPT_SCROLL` option.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-cursor-move.md)（英文原文，待翻譯）
