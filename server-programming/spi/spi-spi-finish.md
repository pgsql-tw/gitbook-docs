<a id="id-1.8.12.8.3.1"></a>

## SPI_finish

SPI_finish — 中斷 C 函式與 SPI 管理器的連線

## 語法

```

int SPI_finish(void)
```

<a id="id-1.8.12.8.3.5"></a>

## 說明

`SPI_finish` 會關閉與 SPI 管理器的既有連線。在 C 函式本次呼叫所需的 SPI 操作完成後，必須呼叫此函式。不過，若透過 `elog(ERROR)` 中止交易，則不必另外確保呼叫此函式；在這種情況下，SPI 會自動清理。

<a id="id-1.8.12.8.3.6"></a>

## 回傳值

`SPI_OK_FINISH`
:   已正確中斷連線

`SPI_ERROR_UNCONNECTED`
:   從尚未連線的 C 函式呼叫

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-finish.html)（原文版本：18.6；核對日期：2026-09-07）
