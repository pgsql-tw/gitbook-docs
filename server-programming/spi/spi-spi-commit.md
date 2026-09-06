<a id="id-1.8.12.11.4.1"></a><a id="id-1.8.12.11.4.2"></a>

## SPI_commit

SPI_commit, SPI_commit_and_chain — 提交目前的交易

## 語法

```

void SPI_commit(void)
```

```

void SPI_commit_and_chain(void)
```

<a id="id-1.8.12.11.4.6"></a>

## 說明

`SPI_commit` 會提交目前的交易，大致相當於執行 SQL 命令 `COMMIT`。交易提交後，會使用預設交易特性自動開始新交易，讓呼叫端可以繼續使用 SPI 功能。如果提交時失敗，則會改為回復目前的交易並開始新交易，然後以一般方式拋出錯誤。

`SPI_commit_and_chain` 的作用相同，但新交易會沿用剛結束之交易的交易特性，如同 SQL 命令 `COMMIT AND CHAIN`。

只有在呼叫 `SPI_connect_ext` 時，將 SPI 連線設為非原子模式（nonatomic），才能執行這些函式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-commit.html)（原文版本：18.6；核對日期：2026-09-07）
