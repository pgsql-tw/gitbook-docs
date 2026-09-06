<a id="id-1.8.12.10.14.1"></a>

## SPI_freeplan

SPI_freeplan — free a previously saved prepared statement

## Synopsis

```

int SPI_freeplan(SPIPlanPtr plan)
```

<a id="id-1.8.12.10.14.5"></a>

## Description

`SPI_freeplan` releases a prepared statement
previously returned by `SPI_prepare` or saved by
`SPI_keepplan` or `SPI_saveplan`.

<a id="id-1.8.12.10.14.6"></a>

## Arguments

`SPIPlanPtr plan`
:   pointer to statement to free

<a id="id-1.8.12.10.14.7"></a>

## Return Value

0 on success;
`SPI_ERROR_ARGUMENT` if *`plan`*
is `NULL` or invalid

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-freeplan.html)（英文原文，待翻譯）
