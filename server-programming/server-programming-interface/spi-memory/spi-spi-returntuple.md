<a id="SPI-SPI-RETURNTUPLE"></a><a id="id-1.8.12.10.10.1"></a>

# SPI_returntuple

SPI_returntuple — prepare to return a tuple as a Datum

## Synopsis

```

HeapTupleHeader SPI_returntuple(HeapTuple row, TupleDesc rowdesc)
```

<a id="id-1.8.12.10.10.5"></a>

## Description

`SPI_returntuple` makes a copy of a row in the upper executor context, returning it in the form of a row type `Datum`. The returned pointer need only be converted to `Datum` via `PointerGetDatum` before returning.

This function can only be used while connected to SPI. Otherwise, it returns NULL and sets `SPI_result` to `SPI_ERROR_UNCONNECTED`.

Note that this should be used for functions that are declared to return composite types. It is not used for triggers; use `SPI_copytuple` for returning a modified row in a trigger.

<a id="id-1.8.12.10.10.6"></a>

## Arguments

<code class="literal">HeapTuple <em class="parameter"><code>row</code></em></code>

row to be copied

<code class="literal">TupleDesc <em class="parameter"><code>rowdesc</code></em></code>

descriptor for row (pass the same descriptor each time for most effective caching)

<a id="id-1.8.12.10.10.7"></a>

## Return Value

`HeapTupleHeader` pointing to copied row, or `NULL` on error (see `SPI_result` for an error indication)

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-returntuple.md)（英文原文，待翻譯）
