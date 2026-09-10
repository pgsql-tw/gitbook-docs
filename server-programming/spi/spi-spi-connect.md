<a id="id-1.8.12.8.2.1"></a><a id="id-1.8.12.8.2.2"></a>

## SPI_connect

SPI_connect、SPI_connect_ext — 將 C 函式連線至 SPI 管理器

## 語法

```

int SPI_connect(void)
```

```

int SPI_connect_ext(int options)
```

<a id="id-1.8.12.8.2.6"></a>

## 說明

`SPI_connect` 會從 C 函式呼叫開啟至 SPI 管理器的連線。若要透過 SPI 執行命令，必須呼叫此函式。某些公用 SPI 函式可從未連線的 C 函式呼叫。

`SPI_connect_ext` 的功能相同，但具有可傳入選項旗標的引數。目前可使用下列選項值：

`SPI_OPT_NONATOMIC`
:   將 SPI 連線設為*非原子性*，因此允許交易控制呼叫（`SPI_commit`、`SPI_rollback`）；否則呼叫這些函式會立即發生錯誤。

`SPI_connect()` 等同於 `SPI_connect_ext(0)`。

<a id="id-1.8.12.8.2.7"></a>

## 回傳值

`SPI_OK_CONNECT`
:   成功時。

這些函式傳回 `int` 而非 `void` 是歷史因素。所有失敗情況會透過 `ereport` 或 `elog` 回報。（在 PostgreSQL v10 之前，部分但非所有失敗情況會以 `SPI_ERROR_CONNECT` 結果值回報。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-connect.html)（原文版本：18.6；核對日期：2026-09-11）
