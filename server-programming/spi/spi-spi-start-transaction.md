<a id="id-1.8.12.11.6.1"></a>

## SPI_start_transaction

SPI_start_transaction — 已淘汰的函式

## 語法

```

void SPI_start_transaction(void)
```

<a id="id-1.8.12.11.6.5"></a>

## 說明

`SPI_start_transaction` 不執行任何動作，僅為了與較早 PostgreSQL 版本的程式碼相容而保留。過去在呼叫 `SPI_commit` 或 `SPI_rollback` 後必須呼叫此函式，但現在這些函式會自動開始新的交易。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-start-transaction.html)（原文版本：18.6；核對日期：2026-09-07）
