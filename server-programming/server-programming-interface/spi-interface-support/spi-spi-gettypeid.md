<a id="SPI-SPI-GETTYPEID"></a><a id="id-1.8.12.9.9.1"></a>

# SPI_gettypeid

SPI_gettypeid — return the data type OID of the specified column

## Synopsis

```

Oid SPI_gettypeid(TupleDesc rowdesc, int colnumber)
```

<a id="id-1.8.12.9.9.5"></a>

## Description

`SPI_gettypeid` returns the OID of the data type of the specified column.

<a id="id-1.8.12.9.9.6"></a>

## Arguments

<code class="literal">TupleDesc <em class="parameter"><code>rowdesc</code></em></code>

input row description

<code class="literal">int <em class="parameter"><code>colnumber</code></em></code>

column number (count starts at 1)

<a id="id-1.8.12.9.9.7"></a>

## Return Value

The OID of the data type of the specified column or `InvalidOid` on error. On error, `SPI_result` is set to `SPI_ERROR_NOATTRIBUTE`.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-spi-gettypeid.html)（英文原文，待翻譯）
