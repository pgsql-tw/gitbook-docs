<a id="SPI-SPI-CURSOR-OPEN"></a><a id="id-1.8.12.8.19.1"></a>

# SPI_cursor_open

SPI_cursor_open — set up a cursor using a statement created with `SPI_prepare`

## Synopsis

```

Portal SPI_cursor_open(const char * name, SPIPlanPtr plan,
                       Datum * values, const char * nulls,
                       bool read_only)
```

<a id="id-1.8.12.8.19.5"></a>

## Description

`SPI_cursor_open` sets up a cursor (internally, a portal) that will execute a statement prepared by `SPI_prepare`. The parameters have the same meanings as the corresponding parameters to `SPI_execute_plan`.

Using a cursor instead of executing the statement directly has two benefits. First, the result rows can be retrieved a few at a time, avoiding memory overrun for queries that return many rows. Second, a portal can outlive the current C function (it can, in fact, live to the end of the current transaction). Returning the portal name to the C function's caller provides a way of returning a row set as result.

The passed-in parameter data will be copied into the cursor's portal, so it can be freed while the cursor still exists.

<a id="id-1.8.12.8.19.6"></a>

## Arguments

<code class="literal">const char &#42; <em class="parameter"><code>name</code></em></code>

name for portal, or `NULL` to let the system select a name

<code class="literal">SPIPlanPtr <em class="parameter"><code>plan</code></em></code>

prepared statement (returned by `SPI_prepare`)

<code class="literal">Datum &#42; <em class="parameter"><code>values</code></em></code>

An array of actual parameter values. Must have same length as the statement's number of arguments.

<code class="literal">const char &#42; <em class="parameter"><code>nulls</code></em></code>

An array describing which parameters are null. Must have same length as the statement's number of arguments.

If <em class="parameter"><code>nulls</code></em> is `NULL` then `SPI_cursor_open` assumes that no parameters are null. Otherwise, each entry of the <em class="parameter"><code>nulls</code></em> array should be `' '` if the corresponding parameter value is non-null, or `'n'` if the corresponding parameter value is null. (In the latter case, the actual value in the corresponding <em class="parameter"><code>values</code></em> entry doesn't matter.) Note that <em class="parameter"><code>nulls</code></em> is not a text string, just an array: it does not need a `'\0'` terminator.

<code class="literal">bool <em class="parameter"><code>read&#95;only</code></em></code>

`true` for read-only execution

<a id="id-1.8.12.8.19.7"></a>

## Return Value

Pointer to portal containing the cursor. Note there is no error return convention; any error will be reported via `elog`.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-cursor-open.md)（英文原文，待翻譯）
