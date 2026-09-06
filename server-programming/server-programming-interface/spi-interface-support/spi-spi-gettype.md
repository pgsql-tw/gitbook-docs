<a id="SPI-SPI-GETTYPE"></a><a id="id-1.8.12.9.8.1"></a>

# SPI_gettype

SPI_gettype — return the data type name of the specified column

## Synopsis

```

char * SPI_gettype(TupleDesc rowdesc, int colnumber)
```

<a id="id-1.8.12.9.8.5"></a>

## Description

`SPI_gettype` returns a copy of the data type name of the specified column. (You can use `pfree` to release the copy of the name when you don't need it anymore.)

<a id="id-1.8.12.9.8.6"></a>

## Arguments

<code class="literal">TupleDesc <em class="parameter"><code>rowdesc</code></em></code>

input row description

<code class="literal">int <em class="parameter"><code>colnumber</code></em></code>

column number (count starts at 1)

<a id="id-1.8.12.9.8.7"></a>

## Return Value

The data type name of the specified column, or `NULL` on error. `SPI_result` is set to `SPI_ERROR_NOATTRIBUTE` on error.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-gettype.md)（英文原文，待翻譯）
