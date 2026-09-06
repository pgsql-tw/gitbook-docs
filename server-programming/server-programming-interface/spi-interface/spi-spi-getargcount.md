<a id="SPI-SPI-GETARGCOUNT"></a><a id="id-1.8.12.8.12.1"></a>

# SPI_getargcount

SPI_getargcount — return the number of arguments needed by a statement prepared by `SPI_prepare`

## Synopsis

```

int SPI_getargcount(SPIPlanPtr plan)
```

<a id="id-1.8.12.8.12.5"></a>

## Description

`SPI_getargcount` returns the number of arguments needed to execute a statement prepared by `SPI_prepare`.

<a id="id-1.8.12.8.12.6"></a>

## Arguments

<code class="literal">SPIPlanPtr <em class="parameter"><code>plan</code></em></code>

prepared statement (returned by `SPI_prepare`)

<a id="id-1.8.12.8.12.7"></a>

## Return Value

The count of expected arguments for the <em class="parameter"><code>plan</code></em>. If the <em class="parameter"><code>plan</code></em> is `NULL` or invalid, `SPI_result` is set to `SPI_ERROR_ARGUMENT` and -1 is returned.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-getargcount.html)（英文原文，待翻譯）
