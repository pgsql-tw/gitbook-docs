<a id="id-1.8.12.9.7.1"></a>

## SPI_getbinval

SPI_getbinval — return the binary value of the specified column

## Synopsis

```

Datum SPI_getbinval(HeapTuple row, TupleDesc rowdesc, int colnumber,
                    bool * isnull)
```

<a id="id-1.8.12.9.7.5"></a>

## Description

`SPI_getbinval` returns the value of the
specified column in the internal form (as type `Datum`).

This function does not allocate new space for the datum. In the
case of a pass-by-reference data type, the return value will be a
pointer into the passed row.

<a id="id-1.8.12.9.7.6"></a>

## Arguments

`HeapTuple row`
:   input row to be examined

`TupleDesc rowdesc`
:   input row description

`int colnumber`
:   column number (count starts at 1)

`bool * isnull`
:   flag for a null value in the column

<a id="id-1.8.12.9.7.7"></a>

## Return Value

The binary value of the column is returned. The variable pointed
to by *`isnull`* is set to true if the column is
null, else to false.

`SPI_result` is set to
`SPI_ERROR_NOATTRIBUTE` on error.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-getbinval.html)（英文原文，待翻譯）
