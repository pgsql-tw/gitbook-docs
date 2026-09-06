<a id="SPI-SPI-EXECP"></a><a id="id-1.8.12.8.18.1"></a>

# SPI_execp

SPI_execp — execute a statement in read/write mode

## Synopsis

```

int SPI_execp(SPIPlanPtr plan, Datum * values, const char * nulls, long count)
```

<a id="id-1.8.12.8.18.5"></a>

## Description

`SPI_execp` is the same as `SPI_execute_plan`, with the latter's <em class="parameter"><code>read&#95;only</code></em> parameter always taken as `false`.

<a id="id-1.8.12.8.18.6"></a>

## Arguments

<code class="literal">SPIPlanPtr <em class="parameter"><code>plan</code></em></code>

prepared statement (returned by `SPI_prepare`)

<code class="literal">Datum &#42; <em class="parameter"><code>values</code></em></code>

An array of actual parameter values. Must have same length as the statement's number of arguments.

<code class="literal">const char &#42; <em class="parameter"><code>nulls</code></em></code>

An array describing which parameters are null. Must have same length as the statement's number of arguments.

If <em class="parameter"><code>nulls</code></em> is `NULL` then `SPI_execp` assumes that no parameters are null. Otherwise, each entry of the <em class="parameter"><code>nulls</code></em> array should be `' '` if the corresponding parameter value is non-null, or `'n'` if the corresponding parameter value is null. (In the latter case, the actual value in the corresponding <em class="parameter"><code>values</code></em> entry doesn't matter.) Note that <em class="parameter"><code>nulls</code></em> is not a text string, just an array: it does not need a `'\0'` terminator.

<code class="literal">long <em class="parameter"><code>count</code></em></code>

maximum number of rows to return, or `0` for no limit

<a id="id-1.8.12.8.18.7"></a>

## Return Value

See `SPI_execute_plan`.

`SPI_processed` and `SPI_tuptable` are set as in `SPI_execute` if successful.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-execp.html)（英文原文，待翻譯）
