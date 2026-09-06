<a id="id-1.8.12.8.13.1"></a>

## SPI_getargtypeid

SPI_getargtypeid — return the data type OID for an argument of
a statement prepared by `SPI_prepare`

## Synopsis

```

Oid SPI_getargtypeid(SPIPlanPtr plan, int argIndex)
```

<a id="id-1.8.12.8.13.5"></a>

## Description

`SPI_getargtypeid` returns the OID representing the type
for the *`argIndex`*'th argument of a statement prepared by
`SPI_prepare`. First argument is at index zero.

<a id="id-1.8.12.8.13.6"></a>

## Arguments

`SPIPlanPtr plan`
:   prepared statement (returned by `SPI_prepare`)

`int argIndex`
:   zero based index of the argument

<a id="id-1.8.12.8.13.7"></a>

## Return Value

The type OID of the argument at the given index.
If the *`plan`* is `NULL` or invalid,
or *`argIndex`* is less than 0 or
not less than the number of arguments declared for the
*`plan`*,
`SPI_result` is set to `SPI_ERROR_ARGUMENT`
and `InvalidOid` is returned.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-getargtypeid.html)（英文原文，待翻譯）
