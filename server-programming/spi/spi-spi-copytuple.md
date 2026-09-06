<a id="id-1.8.12.10.9.1"></a>

## SPI_copytuple

SPI_copytuple — make a copy of a row in the upper executor context

## Synopsis

```

HeapTuple SPI_copytuple(HeapTuple row)
```

<a id="id-1.8.12.10.9.5"></a>

## Description

`SPI_copytuple` makes a copy of a row in the
upper executor context. This is normally used to return a modified
row from a trigger. In a function declared to return a composite
type, use `SPI_returntuple` instead.

This function can only be used while connected to SPI.
Otherwise, it returns NULL and sets `SPI_result` to
`SPI_ERROR_UNCONNECTED`.

<a id="id-1.8.12.10.9.6"></a>

## Arguments

`HeapTuple row`
:   row to be copied

<a id="id-1.8.12.10.9.7"></a>

## Return Value

the copied row, or `NULL` on error
(see `SPI_result` for an error indication)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-copytuple.html)（英文原文，待翻譯）
