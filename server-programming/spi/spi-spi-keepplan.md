<a id="id-1.8.12.8.29.1"></a>

## SPI_keepplan

SPI_keepplan — save a prepared statement

## Synopsis

```

int SPI_keepplan(SPIPlanPtr plan)
```

<a id="id-1.8.12.8.29.5"></a>

## Description

`SPI_keepplan` saves a passed statement (prepared by
`SPI_prepare`) so that it will not be freed
by `SPI_finish` nor by the transaction manager.
This gives you the ability to reuse prepared statements in the subsequent
invocations of your C function in the current session.

<a id="id-1.8.12.8.29.6"></a>

## Arguments

`SPIPlanPtr plan`
:   the prepared statement to be saved

<a id="id-1.8.12.8.29.7"></a>

## Return Value

0 on success;
`SPI_ERROR_ARGUMENT` if *`plan`*
is `NULL` or invalid

<a id="id-1.8.12.8.29.8"></a>

## Notes

The passed-in statement is relocated to permanent storage by means
of pointer adjustment (no data copying is required). If you later
wish to delete it, use `SPI_freeplan` on it.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-keepplan.html)（英文原文，待翻譯）
