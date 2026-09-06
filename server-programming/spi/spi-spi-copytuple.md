<a id="id-1.8.12.10.9.1"></a>

## SPI_copytuple

SPI_copytuple — 在上層執行器記憶體環境中複製資料列

## 語法

```

HeapTuple SPI_copytuple(HeapTuple row)
```

<a id="id-1.8.12.10.9.5"></a>

## 說明

`SPI_copytuple` 會在上層執行器記憶體環境中建立資料列的副本。這通常用於從觸發器回傳修改後的資料列。在宣告為回傳複合型別的函式中，請改用 `SPI_returntuple`。

此函式只能在已連線至 SPI 時使用。否則會回傳 NULL，並將 `SPI_result` 設為 `SPI_ERROR_UNCONNECTED`。

<a id="id-1.8.12.10.9.6"></a>

## 引數

`HeapTuple row`
:   要複製的資料列

<a id="id-1.8.12.10.9.7"></a>

## 回傳值

複製後的資料列；發生錯誤時回傳 `NULL`（錯誤資訊請查看 `SPI_result`）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/spi-spi-copytuple.html)（原文版本：18.6；核對日期：2026-09-07）
