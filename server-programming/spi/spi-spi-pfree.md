<a id="id-1.8.12.10.8.1"></a>

## SPI_pfree

SPI_pfree — 釋放上層執行器記憶體環境中的記憶體

## 語法

```

void SPI_pfree(void * pointer)
```

<a id="id-1.8.12.10.8.5"></a>

## 說明

`SPI_pfree` 會釋放先前使用 `SPI_palloc` 或 `SPI_repalloc` 配置的記憶體。

此函式現在與一般的 `pfree` 沒有差異，僅為了維持既有程式碼的向後相容性而保留。

<a id="id-1.8.12.10.8.6"></a>

## 引數

`void * pointer`
:   指向要釋放之既有儲存空間的指標

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-pfree.html)（原文版本：18.6；核對日期：2026-09-07）
