<a id="id-1.8.12.10.7.1"></a>

## SPI_repalloc

SPI_repalloc — reallocate memory in the upper executor context

## Synopsis

```

void * SPI_repalloc(void * pointer, Size size)
```

<a id="id-1.8.12.10.7.5"></a>

## Description

`SPI_repalloc` changes the size of a memory
segment previously allocated using `SPI_palloc`.

This function is no longer different from plain
`repalloc`. It's kept just for backward
compatibility of existing code.

<a id="id-1.8.12.10.7.6"></a>

## Arguments

`void * pointer`
:   pointer to existing storage to change

`Size size`
:   size in bytes of storage to allocate

<a id="id-1.8.12.10.7.7"></a>

## Return Value

pointer to new storage space of specified size with the contents
copied from the existing area

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-realloc.html)（英文原文，待翻譯）
