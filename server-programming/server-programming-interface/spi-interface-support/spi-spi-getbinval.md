<a id="SPI-SPI-GETBINVAL"></a><a id="id-1.8.12.9.7.1"></a>

# SPI_getbinval

SPI_getbinval — return the binary value of the specified column

## Synopsis

```

Datum SPI_getbinval(HeapTuple row, TupleDesc rowdesc, int colnumber,
                    bool * isnull)
```

<a id="id-1.8.12.9.7.5"></a>

## Description

`SPI_getbinval` returns the value of the specified column in the internal form (as type `Datum`).

This function does not allocate new space for the datum. In the case of a pass-by-reference data type, the return value will be a pointer into the passed row.

<a id="id-1.8.12.9.7.6"></a>

## Arguments

<code class="literal">HeapTuple <em class="parameter"><code>row</code></em></code>

input row to be examined

<code class="literal">TupleDesc <em class="parameter"><code>rowdesc</code></em></code>

input row description

<code class="literal">int <em class="parameter"><code>colnumber</code></em></code>

column number (count starts at 1)

<code class="literal">bool &#42; <em class="parameter"><code>isnull</code></em></code>

flag for a null value in the column

<a id="id-1.8.12.9.7.7"></a>

## Return Value

The binary value of the column is returned. The variable pointed to by <em class="parameter"><code>isnull</code></em> is set to true if the column is null, else to false.

`SPI_result` is set to `SPI_ERROR_NOATTRIBUTE` on error.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-getbinval.html)（英文原文，待翻譯）
