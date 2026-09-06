<a id="id-1.8.12.8.2.1"></a><a id="id-1.8.12.8.2.2"></a>

## SPI_connect

SPI_connect, SPI_connect_ext — connect a C function to the SPI manager

## Synopsis

```

int SPI_connect(void)
```

```

int SPI_connect_ext(int options)
```

<a id="id-1.8.12.8.2.6"></a>

## Description

`SPI_connect` opens a connection from a
C function invocation to the SPI manager. You must call this
function if you want to execute commands through SPI. Some utility
SPI functions can be called from unconnected C functions.

`SPI_connect_ext` does the same but has an argument that
allows passing option flags. Currently, the following option values are
available:

`SPI_OPT_NONATOMIC`
:   Sets the SPI connection to be *nonatomic*, which
    means that transaction control calls (`SPI_commit`,
    `SPI_rollback`) are allowed. Otherwise,
    calling those functions will result in an immediate error.

`SPI_connect()` is equivalent to
`SPI_connect_ext(0)`.

<a id="id-1.8.12.8.2.7"></a>

## Return Value

`SPI_OK_CONNECT`
:   on success

The fact that these functions return `int`
not `void` is historical. All failure cases are reported
via `ereport` or `elog`.
(In versions before PostgreSQL v10,
some but not all failures would be reported with a result value
of `SPI_ERROR_CONNECT`.)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-connect.html)（英文原文，待翻譯）
