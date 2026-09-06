<a id="id-1.8.12.9.8.1"></a>

## SPI_gettype

SPI_gettype — return the data type name of the specified column

## Synopsis

```

char * SPI_gettype(TupleDesc rowdesc, int colnumber)
```

<a id="id-1.8.12.9.8.5"></a>

## Description

`SPI_gettype` returns a copy of the data type name of the
specified column. (You can use `pfree` to
release the copy of the name when you don't need it anymore.)

<a id="id-1.8.12.9.8.6"></a>

## Arguments

`TupleDesc rowdesc`
:   input row description

`int colnumber`
:   column number (count starts at 1)

<a id="id-1.8.12.9.8.7"></a>

## Return Value

The data type name of the specified column, or
`NULL` on error. `SPI_result` is
set to `SPI_ERROR_NOATTRIBUTE` on error.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-gettype.html)（英文原文，待翻譯）
