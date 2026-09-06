<a id="id-1.8.12.8.5.1"></a>

## SPI_exec

SPI_exec — execute a read/write command

## Synopsis

```

int SPI_exec(const char * command, long count)
```

<a id="id-1.8.12.8.5.5"></a>

## Description

`SPI_exec` is the same as
`SPI_execute`, with the latter's
*`read_only`* parameter always taken as
`false`.

<a id="id-1.8.12.8.5.6"></a>

## Arguments

`const char * command`
:   string containing command to execute

`long count`
:   maximum number of rows to return,
    or `0` for no limit

<a id="id-1.8.12.8.5.7"></a>

## Return Value

See `SPI_execute`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-exec.html)（英文原文，待翻譯）
