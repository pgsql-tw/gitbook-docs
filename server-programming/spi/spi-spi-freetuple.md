<a id="id-1.8.12.10.12.1"></a>

## SPI_freetuple

SPI_freetuple — 釋放於上層執行器環境配置的資料列

## 語法

```

void SPI_freetuple(HeapTuple row)
```

<a id="id-1.8.12.10.12.5"></a>

## 說明

`SPI_freetuple` 釋放先前於上層執行器環境配置的資料列。

此函式已與單純的 `heap_freetuple` 沒有差異，僅為既有程式碼的向後相容性保留。

<a id="id-1.8.12.10.12.6"></a>

## 引數

`HeapTuple row`
:   要釋放的資料列

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-freetuple.html)（原文版本：18.6；核對日期：2026-09-06）
