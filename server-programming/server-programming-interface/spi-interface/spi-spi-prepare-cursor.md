<a id="SPI-SPI-PREPARE-CURSOR"></a><a id="id-1.8.12.8.9.1"></a>

# SPI_prepare_cursor

SPI_prepare_cursor — prepare a statement, without executing it yet

## Synopsis

```

SPIPlanPtr SPI_prepare_cursor(const char * command, int nargs,
                              Oid * argtypes, int cursorOptions)
```

<a id="id-1.8.12.8.9.5"></a>

## Description

`SPI_prepare_cursor` is identical to `SPI_prepare`, except that it also allows specification of the planner's “cursor options” parameter. This is a bit mask having the values shown in `nodes/parsenodes.h` for the `options` field of `DeclareCursorStmt`. `SPI_prepare` always takes the cursor options as zero.

This function is now deprecated in favor of `SPI_prepare_extended`.

<a id="id-1.8.12.8.9.6"></a>

## Arguments

<code class="literal">const char &#42; <em class="parameter"><code>command</code></em></code>

command string

<code class="literal">int <em class="parameter"><code>nargs</code></em></code>

number of input parameters (`$1`, `$2`, etc.)

<code class="literal">Oid &#42; <em class="parameter"><code>argtypes</code></em></code>

pointer to an array containing the OIDs of the data types of the parameters

<code class="literal">int <em class="parameter"><code>cursorOptions</code></em></code>

integer bit mask of cursor options; zero produces default behavior

<a id="id-1.8.12.8.9.7"></a>

## Return Value

`SPI_prepare_cursor` has the same return conventions as `SPI_prepare`.

<a id="id-1.8.12.8.9.8"></a>

## Notes

Useful bits to set in <em class="parameter"><code>cursorOptions</code></em> include `CURSOR_OPT_SCROLL`, `CURSOR_OPT_NO_SCROLL`, `CURSOR_OPT_FAST_PLAN`, `CURSOR_OPT_GENERIC_PLAN`, and `CURSOR_OPT_CUSTOM_PLAN`. Note in particular that `CURSOR_OPT_HOLD` is ignored.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-prepare-cursor.md)（英文原文，待翻譯）
