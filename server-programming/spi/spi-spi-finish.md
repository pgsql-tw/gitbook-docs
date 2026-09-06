<a id="id-1.8.12.8.3.1"></a>

## SPI_finish

SPI_finish — disconnect a C function from the SPI manager

## Synopsis

```

int SPI_finish(void)
```

<a id="id-1.8.12.8.3.5"></a>

## Description

`SPI_finish` closes an existing connection to
the SPI manager. You must call this function after completing the
SPI operations needed during your C function's current invocation.
You do not need to worry about making this happen, however, if you
abort the transaction via `elog(ERROR)`. In that
case SPI will clean itself up automatically.

<a id="id-1.8.12.8.3.6"></a>

## Return Value

`SPI_OK_FINISH`
:   if properly disconnected

`SPI_ERROR_UNCONNECTED`
:   if called from an unconnected C function

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-finish.html)（英文原文，待翻譯）
