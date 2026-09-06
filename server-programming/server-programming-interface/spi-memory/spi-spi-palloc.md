<a id="SPI-SPI-PALLOC"></a><a id="id-1.8.12.10.6.1"></a>

# SPI_palloc

SPI_palloc — allocate memory in the upper executor context

## Synopsis

```

void * SPI_palloc(Size size)
```

<a id="id-1.8.12.10.6.5"></a>

## Description

`SPI_palloc` allocates memory in the upper executor context.

This function can only be used while connected to SPI. Otherwise, it throws an error.

<a id="id-1.8.12.10.6.6"></a>

## Arguments

<code class="literal">Size <em class="parameter"><code>size</code></em></code>

size in bytes of storage to allocate

<a id="id-1.8.12.10.6.7"></a>

## Return Value

pointer to new storage space of the specified size

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-palloc.html)（英文原文，待翻譯）
