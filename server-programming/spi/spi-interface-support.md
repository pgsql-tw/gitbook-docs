## 45.2. Interface Support Functions [#](#SPI-INTERFACE-SUPPORT)

[SPI_fname](spi-spi-fname.md) — determine the column name for the specified column number

[SPI_fnumber](spi-spi-fnumber.md) — determine the column number for the specified column name

[SPI_getvalue](spi-spi-getvalue.md) — return the string value of the specified column

[SPI_getbinval](spi-spi-getbinval.md) — return the binary value of the specified column

[SPI_gettype](spi-spi-gettype.md) — return the data type name of the specified column

[SPI_gettypeid](spi-spi-gettypeid.md) — return the data type OID of the specified column

[SPI_getrelname](spi-spi-getrelname.md) — return the name of the specified relation

[SPI_getnspname](spi-spi-getnspname.md) — return the namespace of the specified relation

[SPI_result_code_string](spi-spi-result-code-string.md) — return error code as string

The functions described here provide an interface for extracting
information from result sets returned by `SPI_execute` and
other SPI functions.

All functions described in this section can be used by both
connected and unconnected C functions.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-interface-support.html)（英文原文，待翻譯）
