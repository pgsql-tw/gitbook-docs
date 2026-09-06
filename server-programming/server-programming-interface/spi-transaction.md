<a id="SPI-TRANSACTION"></a>

# 47.4. Transaction Management

[SPI_commit](spi-transaction/spi-spi-commit.md) — commit the current transaction

[SPI_rollback](spi-transaction/spi-spi-rollback.md) — abort the current transaction

[SPI_start_transaction](spi-transaction/spi-spi-start-transaction.md) — obsolete function

It is not possible to run transaction control commands such as `COMMIT` and `ROLLBACK` through SPI functions such as `SPI_execute`. There are, however, separate interface functions that allow transaction control through SPI.

It is not generally safe and sensible to start and end transactions in arbitrary user-defined SQL-callable functions without taking into account the context in which they are called. For example, a transaction boundary in the middle of a function that is part of a complex SQL expression that is part of some SQL command will probably result in obscure internal errors or crashes. The interface functions presented here are primarily intended to be used by procedural language implementations to support transaction management in SQL-level procedures that are invoked by the `CALL` command, taking the context of the `CALL` invocation into account. SPI-using procedures implemented in C can implement the same logic, but the details of that are beyond the scope of this documentation.

---

原文：[PostgreSQL 15.19 Documentation](spi-transaction.md)（英文原文，待翻譯）
