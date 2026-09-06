<a id="id-1.8.12.8.9.1"></a>

## SPI_prepare_cursor

SPI_prepare_cursor — prepare a statement, without executing it yet

## Synopsis

```

SPIPlanPtr SPI_prepare_cursor(const char * command, int nargs,
                              Oid * argtypes, int cursorOptions)
```

<a id="id-1.8.12.8.9.5"></a>

## Description

`SPI_prepare_cursor` is identical to
`SPI_prepare`, except that it also allows specification
of the planner's “cursor options” parameter. This is a bit mask
having the values shown in `nodes/parsenodes.h`
for the `options` field of `DeclareCursorStmt`.
`SPI_prepare` always takes the cursor options as zero.

This function is now deprecated in favor
of `SPI_prepare_extended`.

<a id="id-1.8.12.8.9.6"></a>

## Arguments

`const char * command`
:   command string

`int nargs`
:   number of input parameters (`$1`, `$2`, etc.)

`Oid * argtypes`
:   pointer to an array containing the OIDs of
    the data types of the parameters

`int cursorOptions`
:   integer bit mask of cursor options; zero produces default behavior

<a id="id-1.8.12.8.9.7"></a>

## Return Value

`SPI_prepare_cursor` has the same return conventions as
`SPI_prepare`.

<a id="id-1.8.12.8.9.8"></a>

## Notes

Useful bits to set in *`cursorOptions`* include
`CURSOR_OPT_SCROLL`,
`CURSOR_OPT_NO_SCROLL`,
`CURSOR_OPT_FAST_PLAN`,
`CURSOR_OPT_GENERIC_PLAN`, and
`CURSOR_OPT_CUSTOM_PLAN`. Note in particular that
`CURSOR_OPT_HOLD` is ignored.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-prepare-cursor.html)（英文原文，待翻譯）
