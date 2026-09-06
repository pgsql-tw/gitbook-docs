<a id="SPI-SPI-EXEC"></a><a id="id-1.8.12.8.5.1"></a>

# SPI_exec

SPI_exec — execute a read/write command

## Synopsis

```

int SPI_exec(const char * command, long count)
```

<a id="id-1.8.12.8.5.5"></a>

## Description

`SPI_exec` is the same as `SPI_execute`, with the latter's <em class="parameter"><code>read&#95;only</code></em> parameter always taken as `false`.

<a id="id-1.8.12.8.5.6"></a>

## Arguments

<code class="literal">const char &#42; <em class="parameter"><code>command</code></em></code>

string containing command to execute

<code class="literal">long <em class="parameter"><code>count</code></em></code>

maximum number of rows to return, or `0` for no limit

<a id="id-1.8.12.8.5.7"></a>

## Return Value

See `SPI_execute`.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-exec.html)（英文原文，待翻譯）
