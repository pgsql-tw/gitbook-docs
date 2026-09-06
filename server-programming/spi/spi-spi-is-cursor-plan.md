<a id="id-1.8.12.8.14.1"></a>

## SPI_is_cursor_plan

SPI_is_cursor_plan — return `true` if a statement
prepared by `SPI_prepare` can be used with
`SPI_cursor_open`

## Synopsis

```

bool SPI_is_cursor_plan(SPIPlanPtr plan)
```

<a id="id-1.8.12.8.14.5"></a>

## Description

`SPI_is_cursor_plan` returns `true`
if a statement prepared by `SPI_prepare` can be passed
as an argument to `SPI_cursor_open`, or
`false` if that is not the case. The criteria are that the
*`plan`* represents one single command and that this
command returns tuples to the caller; for example, `SELECT`
is allowed unless it contains an `INTO` clause, and
`UPDATE` is allowed only if it contains a `RETURNING`
clause.

<a id="id-1.8.12.8.14.6"></a>

## Arguments

`SPIPlanPtr plan`
:   prepared statement (returned by `SPI_prepare`)

<a id="id-1.8.12.8.14.7"></a>

## Return Value

`true` or `false` to indicate if the
*`plan`* can produce a cursor or not, with
`SPI_result` set to zero.
If it is not possible to determine the answer (for example,
if the *`plan`* is `NULL` or invalid,
or if called when not connected to SPI), then
`SPI_result` is set to a suitable error code
and `false` is returned.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-is-cursor-plan.html)（英文原文，待翻譯）
