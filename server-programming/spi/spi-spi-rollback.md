<a id="id-1.8.12.11.5.1"></a><a id="id-1.8.12.11.5.2"></a>

## SPI_rollback

SPI_rollback, SPI_rollback_and_chain — 中止目前的交易

## 語法

```

void SPI_rollback(void)
```

```

void SPI_rollback_and_chain(void)
```

<a id="id-1.8.12.11.5.6"></a>

## 說明

`SPI_rollback` 會回復目前的交易，大致相當於執行 SQL 命令 `ROLLBACK`。交易回復後，會使用預設交易特性自動開始新交易，讓呼叫端可以繼續使用 SPI 功能。

`SPI_rollback_and_chain` 的作用相同，但新交易會沿用剛結束之交易的交易特性，如同 SQL 命令 `ROLLBACK AND CHAIN`。

只有在呼叫 `SPI_connect_ext` 時，將 SPI 連線設為非原子模式（nonatomic），才能執行這些函式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-rollback.html)（原文版本：18.6；核對日期：2026-09-07）
