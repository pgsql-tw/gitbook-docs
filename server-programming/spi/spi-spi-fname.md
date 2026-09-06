<a id="id-1.8.12.9.4.1"></a>

## SPI_fname

SPI_fname — determine the column name for the specified column number

## Synopsis

```

char * SPI_fname(TupleDesc rowdesc, int colnumber)
```

<a id="id-1.8.12.9.4.5"></a>

## Description

`SPI_fname` returns a copy of the column name of the
specified column. (You can use `pfree` to
release the copy of the name when you don't need it anymore.)

<a id="id-1.8.12.9.4.6"></a>

## Arguments

`TupleDesc rowdesc`
:   input row description

`int colnumber`
:   column number (count starts at 1)

<a id="id-1.8.12.9.4.7"></a>

## Return Value

The column name; `NULL` if
*`colnumber`* is out of range.
`SPI_result` set to
`SPI_ERROR_NOATTRIBUTE` on error.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-fname.html)（英文原文，待翻譯）
