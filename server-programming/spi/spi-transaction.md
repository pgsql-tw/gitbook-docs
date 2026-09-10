## 45.4. 交易管理 [#](#SPI-TRANSACTION)

[SPI_commit](spi-spi-commit.md) — 提交目前交易

[SPI_rollback](spi-spi-rollback.md) — 中止目前交易

[SPI_start_transaction](spi-spi-start-transaction.md) — 已淘汰函式

無法透過 `SPI_execute` 等 SPI 函式執行 `COMMIT` 與 `ROLLBACK` 等交易控制命令。不過，另有獨立介面函式允許透過 SPI 控制交易。

若不考量呼叫情境，在任意使用者定義的 SQL 可呼叫函式中開始及結束交易，通常既不安全也不合理。舉例來說，在 SQL 命令中複雜 SQL 運算式的一部分函式中間設置交易邊界，可能造成難以理解的內部錯誤或當機。此處介紹的介面函式主要供程序語言實作使用，以支援由 `CALL` 命令呼叫的 SQL 層級程序中的交易管理，並考量 `CALL` 呼叫情境。以 C 實作的使用 SPI 程序可實作相同邏輯，但細節超出本文範圍。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-transaction.html)（原文版本：18.6；核對日期：2026-09-11）
