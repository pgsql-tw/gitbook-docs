<a id="id-1.8.12.10.12.1"></a>

## SPI_freetuple

SPI_freetuple — free a row allocated in the upper executor context

## Synopsis

```

void SPI_freetuple(HeapTuple row)
```

<a id="id-1.8.12.10.12.5"></a>

## Description

`SPI_freetuple` frees a row previously allocated
in the upper executor context.

This function is no longer different from plain
`heap_freetuple`. It's kept just for backward
compatibility of existing code.

<a id="id-1.8.12.10.12.6"></a>

## Arguments

`HeapTuple row`
:   row to free

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-freetuple.html)（英文原文，待翻譯）
