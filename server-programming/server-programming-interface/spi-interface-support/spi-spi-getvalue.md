<a id="SPI-SPI-GETVALUE"></a><a id="id-1.8.12.9.6.1"></a>

# SPI_getvalue

SPI_getvalue — return the string value of the specified column

## Synopsis

```

char * SPI_getvalue(HeapTuple row, TupleDesc rowdesc, int colnumber)
```

<a id="id-1.8.12.9.6.5"></a>

## Description

`SPI_getvalue` returns the string representation of the value of the specified column.

The result is returned in memory allocated using `palloc`. (You can use `pfree` to release the memory when you don't need it anymore.)

<a id="id-1.8.12.9.6.6"></a>

## Arguments

<code class="literal">HeapTuple <em class="parameter"><code>row</code></em></code>

input row to be examined

<code class="literal">TupleDesc <em class="parameter"><code>rowdesc</code></em></code>

input row description

<code class="literal">int <em class="parameter"><code>colnumber</code></em></code>

column number (count starts at 1)

<a id="id-1.8.12.9.6.7"></a>

## Return Value

Column value, or `NULL` if the column is null, <em class="parameter"><code>colnumber</code></em> is out of range (`SPI_result` is set to `SPI_ERROR_NOATTRIBUTE`), or no output function is available (`SPI_result` is set to `SPI_ERROR_NOOUTFUNC`).

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-getvalue.md)（英文原文，待翻譯）
