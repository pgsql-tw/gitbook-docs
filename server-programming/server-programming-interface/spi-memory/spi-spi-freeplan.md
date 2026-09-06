<a id="SPI-SPI-FREEPLAN"></a><a id="id-1.8.12.10.14.1"></a>

# SPI_freeplan

SPI_freeplan — free a previously saved prepared statement

## Synopsis

```

int SPI_freeplan(SPIPlanPtr plan)
```

<a id="id-1.8.12.10.14.5"></a>

## Description

`SPI_freeplan` releases a prepared statement previously returned by `SPI_prepare` or saved by `SPI_keepplan` or `SPI_saveplan`.

<a id="id-1.8.12.10.14.6"></a>

## Arguments

<code class="literal">SPIPlanPtr <em class="parameter"><code>plan</code></em></code>

pointer to statement to free

<a id="id-1.8.12.10.14.7"></a>

## Return Value

0 on success; `SPI_ERROR_ARGUMENT` if <em class="parameter"><code>plan</code></em> is `NULL` or invalid

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-freeplan.html)（英文原文，待翻譯）
