<a id="SPI-INTERFACE-SUPPORT"></a>

# 47.2. Interface Support Functions

[SPI_fname](spi-interface-support/spi-spi-fname.md) — determine the column name for the specified column number

[SPI_fnumber](spi-interface-support/spi-spi-fnumber.md) — determine the column number for the specified column name

[SPI_getvalue](spi-interface-support/spi-spi-getvalue.md) — return the string value of the specified column

[SPI_getbinval](spi-interface-support/spi-spi-getbinval.md) — return the binary value of the specified column

[SPI_gettype](spi-interface-support/spi-spi-gettype.md) — return the data type name of the specified column

[SPI_gettypeid](spi-interface-support/spi-spi-gettypeid.md) — return the data type OID of the specified column

[SPI_getrelname](spi-interface-support/spi-spi-getrelname.md) — return the name of the specified relation

[SPI_getnspname](spi-interface-support/spi-spi-getnspname.md) — return the namespace of the specified relation

[SPI_result_code_string](spi-interface-support/spi-spi-result-code-string.md) — return error code as string

The functions described here provide an interface for extracting information from result sets returned by `SPI_execute` and other SPI functions.

All functions described in this section can be used by both connected and unconnected C functions.

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/spi-interface-support.html)（英文原文，待翻譯）
