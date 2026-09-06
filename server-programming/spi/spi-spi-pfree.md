<a id="id-1.8.12.10.8.1"></a>

## SPI_pfree

SPI_pfree — free memory in the upper executor context

## Synopsis

```

void SPI_pfree(void * pointer)
```

<a id="id-1.8.12.10.8.5"></a>

## Description

`SPI_pfree` frees memory previously allocated
using `SPI_palloc` or
`SPI_repalloc`.

This function is no longer different from plain
`pfree`. It's kept just for backward
compatibility of existing code.

<a id="id-1.8.12.10.8.6"></a>

## Arguments

`void * pointer`
:   pointer to existing storage to free

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-pfree.html)（英文原文，待翻譯）
