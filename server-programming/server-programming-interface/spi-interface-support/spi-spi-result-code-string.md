<a id="SPI-SPI-RESULT-CODE-STRING"></a><a id="id-1.8.12.9.12.1"></a>

# SPI_result_code_string

SPI_result_code_string — return error code as string

## Synopsis

```

const char * SPI_result_code_string(int code);
```

<a id="id-1.8.12.9.12.5"></a>

## Description

`SPI_result_code_string` returns a string representation of the result code returned by various SPI functions or stored in `SPI_result`.

<a id="id-1.8.12.9.12.6"></a>

## Arguments

<code class="literal">int <em class="parameter"><code>code</code></em></code>

result code

<a id="id-1.8.12.9.12.7"></a>

## Return Value

A string representation of the result code.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-result-code-string.md)（英文原文，待翻譯）
