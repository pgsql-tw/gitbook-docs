<a id="id-1.8.12.8.28.1"></a>

## SPI_cursor_close

SPI_cursor_close — 關閉游標

## 語法

```

void SPI_cursor_close(Portal portal)
```

<a id="id-1.8.12.8.28.5"></a>

## 說明

`SPI_cursor_close` 會關閉先前建立的游標，並釋放其 portal 的儲存空間。

交易結束時，所有開啟的游標都會自動關閉。只有在希望提早釋放資源時，才需要呼叫 `SPI_cursor_close`。

<a id="id-1.8.12.8.28.6"></a>

## 引數

`Portal portal`
:   包含游標的 portal

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-cursor-close.html)（原文版本：18.6；核對日期：2026-09-07）
