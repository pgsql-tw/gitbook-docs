<a id="SPI-SPI-MODIFYTUPLE"></a><a id="id-1.8.12.10.11.1"></a>

# SPI_modifytuple

SPI_modifytuple — create a row by replacing selected fields of a given row

## Synopsis

```

HeapTuple SPI_modifytuple(Relation rel, HeapTuple row, int ncols,
                          int * colnum, Datum * values, const char * nulls)
```

<a id="id-1.8.12.10.11.5"></a>

## Description

`SPI_modifytuple` creates a new row by substituting new values for selected columns, copying the original row's columns at other positions. The input row is not modified. The new row is returned in the upper executor context.

This function can only be used while connected to SPI. Otherwise, it returns NULL and sets `SPI_result` to `SPI_ERROR_UNCONNECTED`.

<a id="id-1.8.12.10.11.6"></a>

## Arguments

<code class="literal">Relation <em class="parameter"><code>rel</code></em></code>

Used only as the source of the row descriptor for the row. (Passing a relation rather than a row descriptor is a misfeature.)

<code class="literal">HeapTuple <em class="parameter"><code>row</code></em></code>

row to be modified

<code class="literal">int <em class="parameter"><code>ncols</code></em></code>

number of columns to be changed

<code class="literal">int &#42; <em class="parameter"><code>colnum</code></em></code>

an array of length <em class="parameter"><code>ncols</code></em>, containing the numbers of the columns that are to be changed (column numbers start at 1)

<code class="literal">Datum &#42; <em class="parameter"><code>values</code></em></code>

an array of length <em class="parameter"><code>ncols</code></em>, containing the new values for the specified columns

<code class="literal">const char &#42; <em class="parameter"><code>nulls</code></em></code>

an array of length <em class="parameter"><code>ncols</code></em>, describing which new values are null

If <em class="parameter"><code>nulls</code></em> is `NULL` then `SPI_modifytuple` assumes that no new values are null. Otherwise, each entry of the <em class="parameter"><code>nulls</code></em> array should be `' '` if the corresponding new value is non-null, or `'n'` if the corresponding new value is null. (In the latter case, the actual value in the corresponding <em class="parameter"><code>values</code></em> entry doesn't matter.) Note that <em class="parameter"><code>nulls</code></em> is not a text string, just an array: it does not need a `'\0'` terminator.

<a id="id-1.8.12.10.11.7"></a>

## Return Value

new row with modifications, allocated in the upper executor context, or `NULL` on error (see `SPI_result` for an error indication)

On error, `SPI_result` is set as follows:

`SPI_ERROR_ARGUMENT`

if <em class="parameter"><code>rel</code></em> is `NULL`, or if <em class="parameter"><code>row</code></em> is `NULL`, or if <em class="parameter"><code>ncols</code></em> is less than or equal to 0, or if <em class="parameter"><code>colnum</code></em> is `NULL`, or if <em class="parameter"><code>values</code></em> is `NULL`.

`SPI_ERROR_NOATTRIBUTE`

if <em class="parameter"><code>colnum</code></em> contains an invalid column number (less than or equal to 0 or greater than the number of columns in <em class="parameter"><code>row</code></em>)

`SPI_ERROR_UNCONNECTED`

if SPI is not active

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-modifytuple.md)（英文原文，待翻譯）
