<a id="SPI-SPI-EXECUTE-PLAN"></a><a id="id-1.8.12.8.15.1"></a>

# SPI_execute_plan

SPI_execute_plan — execute a statement prepared by `SPI_prepare`

## Synopsis

```

int SPI_execute_plan(SPIPlanPtr plan, Datum * values, const char * nulls,
                     bool read_only, long count)
```

<a id="id-1.8.12.8.15.5"></a>

## Description

`SPI_execute_plan` executes a statement prepared by `SPI_prepare` or one of its siblings. <em class="parameter"><code>read&#95;only</code></em> and <em class="parameter"><code>count</code></em> have the same interpretation as in `SPI_execute`.

<a id="id-1.8.12.8.15.6"></a>

## Arguments

<code class="literal">SPIPlanPtr <em class="parameter"><code>plan</code></em></code>

prepared statement (returned by `SPI_prepare`)

<code class="literal">Datum &#42; <em class="parameter"><code>values</code></em></code>

An array of actual parameter values. Must have same length as the statement's number of arguments.

<code class="literal">const char &#42; <em class="parameter"><code>nulls</code></em></code>

An array describing which parameters are null. Must have same length as the statement's number of arguments.

If <em class="parameter"><code>nulls</code></em> is `NULL` then `SPI_execute_plan` assumes that no parameters are null. Otherwise, each entry of the <em class="parameter"><code>nulls</code></em> array should be `' '` if the corresponding parameter value is non-null, or `'n'` if the corresponding parameter value is null. (In the latter case, the actual value in the corresponding <em class="parameter"><code>values</code></em> entry doesn't matter.) Note that <em class="parameter"><code>nulls</code></em> is not a text string, just an array: it does not need a `'\0'` terminator.

<code class="literal">bool <em class="parameter"><code>read&#95;only</code></em></code>

`true` for read-only execution

<code class="literal">long <em class="parameter"><code>count</code></em></code>

maximum number of rows to return, or `0` for no limit

<a id="id-1.8.12.8.15.7"></a>

## Return Value

The return value is the same as for `SPI_execute`, with the following additional possible error (negative) results:

`SPI_ERROR_ARGUMENT`

if <em class="parameter"><code>plan</code></em> is `NULL` or invalid, or <em class="parameter"><code>count</code></em> is less than 0

`SPI_ERROR_PARAM`

if <em class="parameter"><code>values</code></em> is `NULL` and <em class="parameter"><code>plan</code></em> was prepared with some parameters

`SPI_processed` and `SPI_tuptable` are set as in `SPI_execute` if successful.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-execute-plan.md)（英文原文，待翻譯）
