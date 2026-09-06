<a id="id-1.8.12.11.6.1"></a>

## SPI_start_transaction

SPI_start_transaction — obsolete function

## Synopsis

```

void SPI_start_transaction(void)
```

<a id="id-1.8.12.11.6.5"></a>

## Description

`SPI_start_transaction` does nothing, and exists
only for code compatibility with
earlier PostgreSQL releases. It used to
be required after calling `SPI_commit`
or `SPI_rollback`, but now those functions start
a new transaction automatically.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-start-transaction.html)（英文原文，待翻譯）
