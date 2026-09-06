<a id="id-1.8.12.8.27.1"></a>

## SPI_scroll_cursor_move

SPI_scroll_cursor_move — move a cursor

## Synopsis

```

void SPI_scroll_cursor_move(Portal portal, FetchDirection direction,
                            long count)
```

<a id="id-1.8.12.8.27.5"></a>

## Description

`SPI_scroll_cursor_move` skips over some number of rows
in a cursor. This is equivalent to the SQL command
`MOVE`.

<a id="id-1.8.12.8.27.6"></a>

## Arguments

`Portal portal`
:   portal containing the cursor

`FetchDirection direction`
:   one of `FETCH_FORWARD`,
    `FETCH_BACKWARD`,
    `FETCH_ABSOLUTE` or
    `FETCH_RELATIVE`

`long count`
:   number of rows to move for
    `FETCH_FORWARD` or
    `FETCH_BACKWARD`; absolute row number to move to for
    `FETCH_ABSOLUTE`; or relative row number to move to for
    `FETCH_RELATIVE`

<a id="id-1.8.12.8.27.7"></a>

## Return Value

`SPI_processed` is set as in
`SPI_execute` if successful.
`SPI_tuptable` is set to `NULL`, since
no rows are returned by this function.

<a id="id-1.8.12.8.27.8"></a>

## Notes

See the SQL [FETCH](../../reference/sql-commands/sql-fetch.md) command
for details of the interpretation of the
*`direction`* and
*`count`* parameters.

Direction values other than `FETCH_FORWARD`
may fail if the cursor's plan was not created
with the `CURSOR_OPT_SCROLL` option.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-scroll-cursor-move.html)（英文原文，待翻譯）
