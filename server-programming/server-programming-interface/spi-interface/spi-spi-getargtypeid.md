<a id="SPI-SPI-GETARGTYPEID"></a><a id="id-1.8.12.8.13.1"></a>

# SPI_getargtypeid

SPI_getargtypeid — return the data type OID for an argument of a statement prepared by `SPI_prepare`

## Synopsis

```

Oid SPI_getargtypeid(SPIPlanPtr plan, int argIndex)
```

<a id="id-1.8.12.8.13.5"></a>

## Description

`SPI_getargtypeid` returns the OID representing the type for the <em class="parameter"><code>argIndex</code></em>'th argument of a statement prepared by `SPI_prepare`. First argument is at index zero.

<a id="id-1.8.12.8.13.6"></a>

## Arguments

<code class="literal">SPIPlanPtr <em class="parameter"><code>plan</code></em></code>

prepared statement (returned by `SPI_prepare`)

<code class="literal">int <em class="parameter"><code>argIndex</code></em></code>

zero based index of the argument

<a id="id-1.8.12.8.13.7"></a>

## Return Value

The type OID of the argument at the given index. If the <em class="parameter"><code>plan</code></em> is `NULL` or invalid, or <em class="parameter"><code>argIndex</code></em> is less than 0 or not less than the number of arguments declared for the <em class="parameter"><code>plan</code></em>, `SPI_result` is set to `SPI_ERROR_ARGUMENT` and `InvalidOid` is returned.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-getargtypeid.html)（英文原文，待翻譯）
