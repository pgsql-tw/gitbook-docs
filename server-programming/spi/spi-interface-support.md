## 45.2. 介面支援函式 [#](#SPI-INTERFACE-SUPPORT)

[SPI_fname](spi-spi-fname.md) — 判定指定欄位編號的欄位名稱

[SPI_fnumber](spi-spi-fnumber.md) — 判定指定欄位名稱的欄位編號

[SPI_getvalue](spi-spi-getvalue.md) — 傳回指定欄位的字串值

[SPI_getbinval](spi-spi-getbinval.md) — 傳回指定欄位的二進位值

[SPI_gettype](spi-spi-gettype.md) — 傳回指定欄位的資料型別名稱

[SPI_gettypeid](spi-spi-gettypeid.md) — 傳回指定欄位的資料型別 OID

[SPI_getrelname](spi-spi-getrelname.md) — 傳回指定關聯的名稱

[SPI_getnspname](spi-spi-getnspname.md) — 傳回指定關聯的命名空間

[SPI_result_code_string](spi-spi-result-code-string.md) — 將錯誤碼作為字串傳回

此處說明的函式提供介面，可從 `SPI_execute` 與其他 SPI 函式傳回的結果集擷取資訊。

本節說明的所有函式均可供已連線與未連線的 C 函式使用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-interface-support.html)（原文版本：18.6；核對日期：2026-09-10）
